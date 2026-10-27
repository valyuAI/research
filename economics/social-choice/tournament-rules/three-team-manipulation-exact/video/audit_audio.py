"""Check every narrated clip against the encoded soundtrack by waveform correlation."""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
from scipy.signal import correlate

ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa'
RATE=12000


def decode(path):
  raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(RATE),'-f','f32le','pipe:1'])
  return np.frombuffer(raw,dtype='<f4').astype(np.float64)


print('Decoding final soundtrack for objective alignment checks',flush=True)
actual=decode(ROOT/'video.mp4')
timeline=json.loads((QA/'timeline.json').read_text())
records=[]
for i,clip in enumerate(timeline,1):
  path=ROOT/'audio'/f'{clip["id"]}.mp3'
  expected=decode(path)
  length=min(2*RATE,len(expected)//3)
  starts=range(int(.15*len(expected)),max(int(.15*len(expected))+1,int(.75*len(expected))-length),RATE//2)
  at=max(starts,key=lambda k:np.dot(expected[k:k+length],expected[k:k+length]))
  ref=expected[at:at+length]
  ref=ref-ref.mean()
  center=int(round(clip['start']*RATE))+at
  margin=int(.24*RATE)
  start=max(0,center-margin);window=actual[start:center+len(ref)+margin]
  dots=correlate(window,ref,mode='valid',method='fft')
  sq=np.r_[0,np.cumsum(window*window)]
  sums=np.r_[0,np.cumsum(window)]
  energy=sq[len(ref):]-sq[:-len(ref)]-(sums[len(ref):]-sums[:-len(ref)])**2/len(ref)
  corr=dots/np.sqrt(np.maximum(energy*np.dot(ref,ref),1e-20))
  peak=int(np.argmax(corr));score=float(corr[peak]);lag=(start+peak-center)/RATE
  rec={'id':clip['id'],'scene':clip['scene'],'expected_start':clip['start'],'sample_offset':at/RATE,'correlation':score,'lag_seconds':lag,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
  records.append(rec)
  print(f'audio {i}/{len(timeline)} {clip["id"]}: correlation {score:.5f}, offset {lag:+.4f}s',flush=True)
  assert score>.9,rec
  assert abs(lag)<.2,rec
result={'method':'Normalized waveform cross-correlation of a high-energy two-second window from every source clip against its expected location in the final AAC soundtrack. No subjective listening performed.','all_passed':True,'sample_rate':RATE,'min_correlation':min(r['correlation'] for r in records),'max_absolute_lag_seconds':max(abs(r['lag_seconds']) for r in records),'clips':records}
(QA/'audio-alignment.json').write_text(json.dumps(result,indent=2))
print('PASS every source clip is present at its expected position in the final soundtrack',flush=True)
