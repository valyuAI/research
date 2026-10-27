"""Re-render the two changed native Manim scenes and rejoin the existing final parts."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
TOOLS=next(p / 'tools/video' for p in ROOT.parents if (p / 'tools/video/render.py').exists())
sys.path.insert(0,str(TOOLS))
from render import probe, scene_list

print('Repairing connector spacing in Robustness and SharpSizes only.',flush=True)
subprocess.run([sys.executable,'-B',str(TOOLS/'render.py'),str(ROOT),'--quality','h','--scenes','Robustness','SharpSizes','--output','repaired-sections.mp4'],check=True)
parts=[ROOT/'media/videos/scenes/1080p30'/f'{name}.mp4' for name in scene_list(ROOT)]
assert all(probe(p)[1] for p in parts)
inputs=sum((['-i',str(p)] for p in parts),[])
streams=''.join(f'[{i}:v:0][{i}:a:0]' for i in range(len(parts)))
filt=f'{streams}concat=n={len(parts)}:v=1:a=1[v][a]'
print('Rejoining all eight native1080p parts.',flush=True)
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-stats',*inputs,'-filter_complex',filt,'-map','[v]','-map','[a]',
                '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',str(ROOT/'video.mp4')],check=True)
duration,_=probe(ROOT/'video.mp4')
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-ss','12','-i',str(ROOT/'video.mp4'),'-frames:v','1',str(ROOT/'poster.png')],check=True)
subprocess.run(['ffmpeg','-nostdin','-y','-v','error','-i',str(ROOT/'video.mp4'),'-vf',f'fps=1/{duration/30:.3f},scale=480:-1,tile=5x6','-frames:v','1',str(ROOT/'contact.png')],check=True)
print('Repair render complete; full QA must run again.',flush=True)
