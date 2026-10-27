"""Technical media audit; visual and listening claims require separate human notes."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
QA = ROOT/'qa'
QA.mkdir(exist_ok=True)


def probe(path):
  return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))


data = probe(ROOT/'video.mp4')
(QA/'ffprobe.json').write_text(json.dumps(data,indent=2))
v = next(s for s in data['streams'] if s['codec_type']=='video')
a = next(s for s in data['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])==(1920,1080,'30/1','h264')
assert a['codec_name']=='aac' and float(a['duration'])>0
total = float(data['format']['duration'])
spec = json.loads((ROOT/'narration.json').read_text())
durations = json.loads((ROOT/'audio/durations.json').read_text())
manifest = json.loads((ROOT/'audio/manifest.json').read_text())
sys.path.insert(0,str(next(p / 'tools/video' for p in ROOT.parents if (p / 'tools/video/render.py').exists())))
from make_audio import digest, DEFAULT_INSTRUCTIONS
for c in spec['clips']:
  measured = float(probe(ROOT/'audio'/f'{c["id"]}.mp3')['format']['duration'])
  assert measured<=25, (c['id'],measured)
  assert abs(measured-durations[c['id']])<.002
  assert manifest[c['id']]['hash']==digest(c['text'],spec['voice'],spec.get('instructions',DEFAULT_INSTRUCTIONS))
print(f'PASS native 1920x1080 30fps H264/AAC; {total:.3f}s; {len(durations)} clips; max {max(durations.values()):.3f}s',flush=True)
parsed = ast.parse((ROOT/'scenes.py').read_text())
names = next(ast.literal_eval(n.value) for n in parsed.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SCENES' for t in n.targets))
offset = 0
samples = [('start',5),('middle',total/2),('end',total-4)]
timing_ids=[]
timeline=[]
for name in names:
  p = ROOT/'media/videos/scenes/1080p30'/f'{name}.mp4'
  d = float(probe(p)['format']['duration'])
  timing = json.loads((ROOT/'media/timings'/f'{name}.json').read_text())
  for clip in timing['clips']:
    timing_ids.append(clip['id'])
    timeline.append({**clip,'start':clip['start']+offset,'scene':name})
  samples.extend([(f'{name}-start',offset+min(3,d/3)),(f'{name}-end',offset+d-1.5)])
  offset += d
assert timing_ids == [c['id'] for c in spec['clips']]
(QA/'timeline.json').write_text(json.dumps(timeline,indent=2))
# Every narration beat is also sampled, after its visual action normally settles.
for clip in timeline:
  samples.append((clip['id'],clip['start']+min(6,clip['duration']*.65)))
frames=[]
for i,(name,t) in enumerate(samples,1):
  out=QA/f'{name}.png'
  subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(t),'-i',str(ROOT/'video.mp4'),'-frames:v','1',str(out)],check=True)
  im=Image.open(out).convert('RGB'); im.thumbnail((480,270))
  thumb=Image.new('RGB',(480,300),'#0d0f12');thumb.paste(im,(0,0));ImageDraw.Draw(thumb).text((12,278),f'{name}  {t:.2f}s',fill='white')
  frames.append(thumb)
  print(f'frame {i}/{len(samples)} {name} at {t:.2f}s',flush=True)
for prefix,subset in [('boundaries',frames[:3+2*len(names)]),('beats',frames[3+2*len(names):])]:
  sheet=Image.new('RGB',(480*4,300*((len(subset)+3)//4)),'#0d0f12')
  for i,im in enumerate(subset):sheet.paste(im,((i%4)*480,(i//4)*300))
  sheet.save(QA/f'{prefix}.png')
print('Full video+audio decode beginning',flush=True)
with (QA/'decode.log').open('w') as log:
  p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',str(ROOT/'video.mp4'),'-map','0:v:0','-map','0:a:0','-f','null','-','-progress','pipe:1','-stats_period','10'],stdout=subprocess.PIPE,stderr=log,text=True)
  for line in p.stdout:
    if line.startswith(('out_time=','progress=')):print('decode '+line.strip(),flush=True)
  assert p.wait()==0
assert not (QA/'decode.log').read_text().strip()
print('PASS complete decode',flush=True)
vol=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-i',str(ROOT/'video.mp4'),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True)
(QA/'audio-levels.log').write_text(vol.stderr)
files=[ROOT/'scenes.py',ROOT/'narration.json',ROOT/'storyboard.md',ROOT/'video.mp4',ROOT/'subtitles.srt',ROOT/'poster.png',ROOT/'contact.png',*sorted((ROOT/'audio').glob('*.mp3')),ROOT/'audio/durations.json',ROOT/'audio/manifest.json']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(QA/'artifact-sha256.json').write_text(json.dumps(hashes,indent=2))
(ROOT/'QA.md').write_text(f'''# Media QA

- Final video: {total:.3f} seconds, native 1920x1080 at 30 fps, H.264, AAC. Source scene outputs are in media/videos/scenes/1080p30. This is a fresh high-quality Manim render, not an enlarged preview.
- {len(durations)} Cedar clips; maximum measured length {max(durations.values()):.3f} seconds. All are <=25 seconds. ffprobe measurements agree with durations.json.
- All narration manifest digests match final narration text, voice and instructions. Every clip appears once in final scene order. Final source/audio/media hashes are in qa/artifact-sha256.json.
- Full video and audio decode passed with zero error output. Stream metadata: qa/ffprobe.json. Decode record: qa/decode.log. Audio signal statistics: qa/audio-levels.log.
- Representative start/middle/end, both sides of every scene, and every narration beat were extracted from the final media. Contact sheets: qa/boundaries.png and qa/beats.png. Extraction alone is not visual inspection; manual findings are recorded below.
- Subtitles are phrase chunks distributed over measured clip times, not a word-aligned transcript. Narration durations drive picture timing, with a brief pause between clips.
- No audio listening is claimed. This environment audit checks audio presence, duration, level and decodability; subjective pronunciation and listening pace remain unverified.
''')
print('Technical QA and hashes written',flush=True)
