"""Extract every concept and transition, retaining preview evidence separately."""
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
preview='--preview' in sys.argv
kind='preview-evidence' if preview else 'final-evidence'
OUT=ROOT/kind
OUT.mkdir(exist_ok=True)
movie=ROOT/('preview.mp4' if preview else 'video.mp4')
res='480p15' if preview else '1080p30'
tree=ast.parse((ROOT/'scenes.py').read_text())
scenes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(getattr(t,'id',None)=='SCENES' for t in n.targets))
def dur(p):
  return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)],text=True))
offset=0
samples=[]
timeline=[]
for scene in scenes:
  part=ROOT/'media/videos/scenes'/res/f'{scene}.mp4'
  timing=json.loads((ROOT/'media/timings'/f'{scene}.json').read_text())
  (OUT/f'{scene}-timings.json').write_text(json.dumps(timing,indent=2))
  d=dur(part)
  samples.extend([(f'{scene}-in',offset+.15),(f'{scene}-out',offset+d-.2)])
  for clip in timing['clips']:
    timeline.append({**clip,'start':offset+clip['start'],'scene':scene})
    for portion in [.35,.85]:samples.append((f'{clip["id"]}-{int(portion*100)}',offset+clip['start']+clip['duration']*portion))
  offset+=d
(OUT/'timeline.json').write_text(json.dumps(timeline,indent=2))
for name in ['contact.png','poster.png','subtitles.srt']:
  if (ROOT/name).exists():shutil.copy2(ROOT/name,OUT/name)
thumbs=[]
for i,(name,t) in enumerate(samples,1):
  path=OUT/f'{name}.png'
  subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss',str(t),'-i',str(movie),'-frames:v','1',str(path)],check=True)
  im=Image.open(path).convert('RGB');im.thumbnail((480,270))
  card=Image.new('RGB',(480,295),'#0d0f12');card.paste(im,(0,0));ImageDraw.Draw(card).text((10,277),f'{name}  {t:.2f}s',fill='white');thumbs.append(card)
  print(f'{kind} frame {i}/{len(samples)}: {name}',flush=True)
for page in range((len(thumbs)+15)//16):
  sheet=Image.new('RGB',(1920,1180),'#0d0f12')
  for i,im in enumerate(thumbs[page*16:(page+1)*16]):sheet.paste(im,((i%4)*480,(i//4)*295))
  sheet.save(OUT/f'sheet-{page+1:02}.png')
print(f'{kind}: {len(samples)} frames, {len(timeline)} clips, {offset:.3f}s',flush=True)
