"""Measure final media, audit narration/captions and extract inspection evidence."""
import ast
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import re
import subprocess
import textwrap

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa'
QA.mkdir(exist_ok=True)


def probe(path):
  return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], text=True))


def sha(path):
  return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
  (QA / name).write_text(json.dumps(value, indent=2) + '\n')


def timestamp(value):
  h, rem = divmod(round(value * 1000), 3600000)
  m, rem = divmod(rem, 60000)
  s, ms = divmod(rem, 1000)
  return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def seconds(value):
  h,m,s,ms = map(int, re.split('[:,]', value))
  return 3600*h+60*m+s+ms/1000


def sheet(records, output, columns=4):
  width, height, footer = 480, 270, 24
  canvas = Image.new('RGB', (columns*width, ((len(records)+columns-1)//columns)*(height+footer)), '#20242a')
  draw = ImageDraw.Draw(canvas)
  for i, item in enumerate(records):
    x, y = (i%columns)*width, (i//columns)*(height+footer)
    im = Image.open(QA/item['file']).convert('RGB').resize((width,height))
    canvas.paste(im,(x,y))
    draw.text((x+8,y+height+5), f'{item["label"]} | {item["time"]:.2f}s', fill='white')
  canvas.save(output)


def main():
  if not __debug__:
    raise SystemExit("Media verification requires Python assertions enabled.")
  print('1/7: native final stream metadata', flush=True)
  metadata = probe(ROOT/'video.mp4')
  save('ffprobe.json', metadata)
  video = next(s for s in metadata['streams'] if s['codec_type']=='video')
  audio = next(s for s in metadata['streams'] if s['codec_type']=='audio')
  assert (video['width'], video['height'], video['codec_name'], video['avg_frame_rate']) == (1920,1080,'h264','30/1')
  assert audio['codec_name']=='aac' and int(audio['sample_rate'])==48000
  total = float(metadata['format']['duration'])

  print('2/7: measured clips, source digests and ordered timeline', flush=True)
  spec = json.loads((ROOT/'narration.json').read_text())
  durations = json.loads((ROOT/'audio/durations.json').read_text())
  manifest = json.loads((ROOT/'audio/manifest.json').read_text())
  ids = [c['id'] for c in spec['clips']]
  texts = {c['id']:c['text'] for c in spec['clips']}
  assert len(ids)==len(set(ids)) and spec['voice']=='cedar'
  records = []
  for i, clip in enumerate(spec['clips'],1):
    key = clip['id']
    seconds_clip = float(probe(ROOT/'audio'/f'{key}.mp3')['format']['duration'])
    assert 0 < seconds_clip < 25, (key, seconds_clip)
    assert abs(seconds_clip-durations[key]) < .002
    item = manifest[key]
    expected = hashlib.sha256(f'{item["model"]}|{spec["voice"]}|{spec["instructions"]}|{clip["text"]}'.encode()).hexdigest()[:16]
    assert item['voice']=='cedar' and expected==item['hash'], key
    records.append({'id':key,'seconds':seconds_clip,'sha256':sha(ROOT/'audio'/f'{key}.mp3')})
    print(f'  {i}/{len(ids)} {key}: {seconds_clip:.3f}s',flush=True)
  save('clips.json',records)
  tree = ast.parse((ROOT/'scenes.py').read_text())
  scenes = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SCENES' for t in n.targets))
  timeline, boundaries, native_streams, offset = [], [], [], 0.
  for name in scenes:
    part = ROOT/'media/videos/scenes/1080p30'/f'{name}.mp4'
    data = probe(part)
    v = next(s for s in data['streams'] if s['codec_type']=='video')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    # Manim partial-clip packet rounding can accumulate several milliseconds.
    # Require native 30fps and total frame-count duration within one frame.
    # The joined final movie must still have exactly 30/1 average frame rate.
    assert abs(float(v['duration'])-int(v['nb_frames'])/30)<1/30
    native_streams.append({'scene':name,'video':v})
    duration = float(data['format']['duration'])
    timing = json.loads((ROOT/'media/timings'/f'{name}.json').read_text())
    previous = 0.
    for clip in timing['clips']:
      assert clip['start'] >= previous-.04
      assert abs(clip['duration']-durations[clip['id']])<.002
      end = clip['start']+clip['duration']
      assert end <= duration+.05
      timeline.append({'id':clip['id'],'scene':name,'start':offset+clip['start'],'duration':clip['duration'],'end':offset+end})
      previous = end
    boundaries.append({'scene':name,'start':offset,'end':offset+duration})
    offset += duration
  assert [c['id'] for c in timeline]==ids
  assert abs(total-offset) < .15, (total,offset)
  save('timeline.json',timeline)
  save('scenes.json',boundaries)
  save('native-source-streams.json',native_streams)

  print('3/7: readable phrase captions and transcript identity',flush=True)
  cues=[]
  for clip in timeline:
    words=texts[clip['id']].split()
    chunks=[]
    current=[]
    for word in words:
      if current and len(' '.join(current+[word]))>78:
        chunks.append(' '.join(current));current=[]
      current.append(word)
      if word.endswith(('.', '?', '!')) and len(' '.join(current))>=34:
        chunks.append(' '.join(current));current=[]
    if current:
      chunks.append(' '.join(current))
    bounded=[]
    for chunk in chunks:
      wrapped=textwrap.wrap(chunk,width=43,break_long_words=False,break_on_hyphens=False)
      bounded.extend(' '.join(wrapped[i:i+2]) for i in range(0,len(wrapped),2))
    chunks=bounded
    size=sum(len(c) for c in chunks)
    t=clip['start']
    for chunk in chunks:
      length=clip['duration']*len(chunk)/size
      lines=textwrap.wrap(chunk,width=43,break_long_words=False,break_on_hyphens=False)
      assert len(lines)<=2
      cues.append({'start':t,'end':t+length,'text':'\n'.join(lines),'id':clip['id']})
      t+=length
  assert ' '.join(c['text'].replace('\n',' ') for c in cues)==' '.join(c['text'] for c in spec['clips'])
  assert all(c['start']<c['end'] for c in cues)
  assert all(a['end'] <= b['start']+.002 for a,b in zip(cues,cues[1:]))
  assert cues[-1]['end']<=total
  srt='\n\n'.join(f'{i}\n{timestamp(c["start"])} --> {timestamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues,1))+'\n'
  (ROOT/'subtitles.srt').write_text(srt)
  (ROOT/'subtitles.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d\d:\d\d:\d\d),(\d{3})',r'\1.\2',srt))
  save('subtitle-check.json',{'cues':len(cues),'text_matches':True,'nonoverlapping':True,'max_lines':2,'last_end':cues[-1]['end'],'timing':'Phrase timing proportional to character counts within measured clips; not forced word alignment.'})
  captioned = ROOT / 'media/captioned.mp4'
  subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(ROOT/'video.mp4'),'-i',str(ROOT/'subtitles.srt'),
                  '-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text',
                  '-metadata:s:s:0','language=eng','-disposition:s:0','default','-movflags','+faststart',str(captioned)],check=True)
  captioned.replace(ROOT/'video.mp4')
  metadata = probe(ROOT/'video.mp4')
  assert any(s['codec_type']=='subtitle' and s['codec_name']=='mov_text' for s in metadata['streams'])
  total = float(metadata['format']['duration'])
  save('ffprobe.json',metadata)

  print('4/7: complete video/audio decode and signal measurement',flush=True)
  with (QA/'decode.log').open('w') as log:
    decode=subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(ROOT/'video.mp4'),'-map','0:v:0','-map','0:a:0','-f','null','-'],stdout=log,stderr=subprocess.STDOUT)
  assert decode.returncode==0 and (QA/'decode.log').stat().st_size==0
  with (QA/'audio-levels.log').open('w') as log:
    level=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(ROOT/'video.mp4'),'-vn','-af','volumedetect','-f','null','-'],stdout=log,stderr=subprocess.STDOUT)
  assert level.returncode==0
  levels=(QA/'audio-levels.log').read_text()
  peak=float(re.search(r'max_volume: ([\d.-]+) dB',levels).group(1))
  mean=float(re.search(r'mean_volume: ([\d.-]+) dB',levels).group(1))
  assert peak < 0 and mean > -45, (mean,peak)

  print('5/7: representative and boundary frames',flush=True)
  frames=[]
  for clip in timeline:
    frames.append({'label':clip['id'],'time':clip['start']+.7*clip['duration'],'file':f'{clip["id"]}.png','kind':'beat'})
  for i, scene in enumerate(boundaries):
    for edge,tm in [('start',scene['start']+.25),('end',scene['end']-.2)]:
      frames.append({'label':f'{scene["scene"]} {edge}','time':max(.05,min(total-.1,tm)),'file':f'boundary-{i:02d}-{edge}.png','kind':'boundary'})
  for i, frame in enumerate(frames,1):
    subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(frame['time']),'-i',str(ROOT/'video.mp4'),'-frames:v','1',str(QA/frame['file'])],check=True)
    print(f'  frame {i}/{len(frames)} {frame["label"]}',flush=True)
  save('frames.json',frames)
  sheet([f for f in frames if f['kind']=='beat'],QA/'beats.png')
  sheet([f for f in frames if f['kind']=='boundary'],QA/'boundaries.png')

  print('6/7: locked scientific inputs still match',flush=True)
  snapshot=json.loads((ROOT/'scientific-input-sha256.json').read_text())
  expected = dict(snapshot['sha256'])
  approved = {}
  supplement_path = ROOT/'scientific-input-supplement.json'
  if supplement_path.exists():
    supplement = json.loads(supplement_path.read_text())
    original_path=ROOT/supplement.get('originalSnapshot','scientific-input-sha256.json')
    assert supplement['validated'] and supplement['originalSnapshotSha256']==sha(original_path)
    historical=json.loads(original_path.read_text())['sha256']
    if 'currentSnapshotSha256' in supplement:
      assert supplement['currentSnapshotSha256']==sha(ROOT/'scientific-input-sha256.json')
    approved = supplement['approvedChanges']
    for name, change in approved.items():
      assert historical[name]==change['before'] and expected[name] in [change['before'],change['after']]
      expected[name]=change['after']
  mismatch=[name for name,digest in expected.items() if not (ROOT.parent/name).exists() or sha(ROOT.parent/name)!=digest]
  save('scientific-input-check.json',{'checked':len(expected),'changed':mismatch,'approvedChanges':approved,'originalSnapshotPreserved':True})
  assert not mismatch, mismatch

  print('7/7: machine summary and editable preview',flush=True)
  summary={'duration':total,'width':1920,'height':1080,'fps':30,'video_codec':'h264','audio_codec':'aac','clip_count':len(ids),'max_clip_seconds':max(c['seconds'] for c in records),'full_decode':'passed','mean_db':mean,'peak_db':peak,'listening_performed':False,'visual_inspection':'pending human-style image review by production agent','source_hashes_unchanged':not bool(approved),'source_provenance_validated':True}
  save('summary.json',summary)
  files=[ROOT/'video.mp4',ROOT/'scenes.py',ROOT/'narration.json',ROOT/'subtitles.srt',ROOT/'subtitles.vtt',*sorted((ROOT/'audio').glob('*.mp3'))]
  save('artifact-sha256.json',{str(p.relative_to(ROOT)):sha(p) for p in files})
  (ROOT/'preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Mathematical explainer</title><style>body{margin:40px auto;max-width:1100px;padding:0 24px;font:18px system-ui;background:#0d0f12;color:#eee}video{width:100%}a{color:#67c8c4}</style><h1>'+ROOT.parent.name.replace('-',' ')+'</h1><video controls preload="metadata" poster="poster.png"><source src="video.mp4" type="video/mp4"><track default kind="captions" src="subtitles.vtt" srclang="en" label="English"></video><p><a href="subtitles.srt">Captions</a> · <a href="sources.md">Sources</a> · <a href="QA.md">QA record</a></p><p>Narration uses a synthetic voice.</p></html>')
  print(json.dumps(summary),flush=True)


if __name__=='__main__':
  main()
