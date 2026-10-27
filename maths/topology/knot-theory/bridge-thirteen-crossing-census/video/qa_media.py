"""Check final streams, complete decode, clip provenance and representative frames.

This is technical QA, not an assertion that a human listened to narration.
"""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'qa'


def need(value, message):
  if not value:
    raise ValueError(message)


def probe(path):
  return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))


def sha(path):
  h=hashlib.sha256()
  with path.open('rb') as f:
    for block in iter(lambda:f.read(1024*1024),b''):
      h.update(block)
  return h.hexdigest()


def main():
  spec=json.loads((ROOT/'narration.json').read_text())
  durations=json.loads((ROOT/'audio/durations.json').read_text())
  manifest=json.loads((ROOT/'audio/manifest.json').read_text())
  source=ast.parse((ROOT/'scenes.py').read_text())
  scenes=next(ast.literal_eval(n.value) for n in source.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SCENES' for t in n.targets))
  tools=next(p/'tools/video' for p in ROOT.parents if (p/'tools/video/make_audio.py').exists())
  import sys
  sys.path.insert(0,str(tools))
  import make_audio
  instructions=spec.get('instructions',make_audio.DEFAULT_INSTRUCTIONS)
  clip_hashes={}
  for c in spec['clips']:
    key=c['id']; path=ROOT/'audio'/f'{key}.mp3'
    measured=float(probe(path)['format']['duration'])
    need(measured<=25,f'{key} exceeds 25 seconds')
    need(abs(measured-durations[key])<.002,f'{key} duration mismatch')
    need(manifest[key]['hash']==make_audio.digest(c['text'],spec['voice'],instructions),f'{key} audio text provenance mismatch')
    clip_hashes[key]=sha(path)
  final=probe(ROOT/'video.mp4')
  video=next(s for s in final['streams'] if s['codec_type']=='video')
  audio=next(s for s in final['streams'] if s['codec_type']=='audio')
  need((video['width'],video['height'],video['codec_name'],video['r_frame_rate'])==(1920,1080,'h264','30/1'),'Final video spec mismatch')
  need(audio['codec_name']=='aac' and float(audio['duration'])>0,'Missing AAC audio')
  print('Final streams: native 1920x1080, 30 fps, H.264/AAC',flush=True)
  with (QA/'full-decode.log').open('w') as log:
    cmd=['ffmpeg','-v','error','-stats','-i',str(ROOT/'video.mp4'),'-f','null','-']
    proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
    while proc.poll() is None:
      try: proc.wait(timeout=20)
      except subprocess.TimeoutExpired: print('Full decode still running...',flush=True)
    need(proc.returncode==0,'Full decode failed')
  print('Full video and audio decode: PASS',flush=True)
  with (QA/'audio-levels.log').open('w') as log:
    subprocess.run(['ffmpeg','-hide_banner','-i',str(ROOT/'video.mp4'),'-vn','-af','volumedetect','-f','null','-'],stdout=log,stderr=subprocess.STDOUT,check=True)
  frames=[]; offset=0.; timeline=[]; encountered=[]
  (QA/'frames').mkdir(exist_ok=True)
  for index,name in enumerate(scenes):
    part=ROOT/'media/videos/scenes/1080p30'/f'{name}.mp4'
    part_info=probe(part)
    part_video=next(s for s in part_info['streams'] if s['codec_type']=='video')
    need((part_video['width'],part_video['height'],part_video['r_frame_rate'])==(1920,1080,'30/1'),f'{name} is not a native final-resolution scene')
    part_duration=float(part_info['format']['duration'])
    timing=json.loads((ROOT/'media/timings'/f'{name}.json').read_text())
    for clip in timing['clips']:
      encountered.append(clip['id'])
      need(clip['start']+clip['duration']<=part_duration+.04,'Narration extends beyond scene')
      timeline.append({**clip,'scene':name,'global_start':offset+clip['start']})
    for label,t in [('start',offset+.35),('middle',offset+part_duration/2),('end',offset+part_duration-.4)]:
      path=QA/'frames'/f'{index+1:02d}-{name}-{label}.png'
      subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(ROOT/'video.mp4'),'-frames:v','1',str(path)],check=True)
      frames.append({'scene':name,'kind':label,'time':round(t,3),'file':str(path.relative_to(ROOT))})
    print(f'Frames {index+1}/{len(scenes)}: {name}, {offset:.2f} to {offset+part_duration:.2f}s',flush=True)
    offset+=part_duration
  need(encountered==[c['id'] for c in spec['clips']],'Timeline differs from narration order')
  canvas=Image.new('RGB',(1440,len(scenes)*294),'#15171a'); draw=ImageDraw.Draw(canvas)
  for i,frame in enumerate(frames):
    x=(i%3)*480; y=(i//3)*294
    with Image.open(ROOT/frame['file']) as im:
      canvas.paste(im.resize((480,270)),(x,y+24))
    draw.text((x+8,y+5),f"{frame['scene']} {frame['kind']} {frame['time']:.2f}s",fill='white')
  canvas.save(QA/'boundary-contact.png')
  (QA/'timeline.json').write_text(json.dumps(timeline,indent=2))
  (QA/'frame-index.json').write_text(json.dumps(frames,indent=2))
  (QA/'ffprobe.json').write_text(json.dumps(final,indent=2))
  files=['scenes.py','narration.json','storyboard.md','video.mp4','subtitles.srt','audio/durations.json','audio/manifest.json']
  if (ROOT/'geometry.json').exists(): files.append('geometry.json')
  if (ROOT/'example.json').exists(): files.append('example.json')
  report={'stream_checks':'pass','full_decode':'pass','duration_seconds':float(final['format']['duration']),'max_clip_seconds':max(durations.values()),'clip_count':len(durations),'audio_provenance_hashes_match':True,'timeline_ids_match_script_order':True,'listening_performed':False,'visual_inspection':'pending review of extracted frames','source_and_media_sha256':{f:sha(ROOT/f) for f in files},'audio_sha256':clip_hashes}
  (QA/'media-check.json').write_text(json.dumps(report,indent=2))
  print(json.dumps({k:v for k,v in report.items() if not k.endswith('sha256')}),flush=True)


if __name__=='__main__': main()
