"""Run the shared renderer with a bounded heartbeat and retained log."""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = next(p / 'tools/video' for p in ROOT.parents if (p / 'tools/video/render.py').exists())
STATUS = Path(os.environ.get('VIDEO_STATUS_FILE', os.devnull))

parser = argparse.ArgumentParser()
parser.add_argument('--quality', choices=['l', 'h'], default='h')
args = parser.parse_args()
label = 'preview' if args.quality == 'l' else 'final'
log = ROOT / 'qa' / f'{label}-render.log'
cmd = [sys.executable, str(TOOLS / 'render.py'), str(ROOT), '--quality', args.quality, '--contact', '--output', 'preview.mp4' if label == 'preview' else 'video.mp4']
start = time.monotonic()
with log.open('w') as out:
  proc = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT)
  print(f'{label} render started pid={proc.pid}, nice={os.getpriority(os.PRIO_PROCESS,0)}', flush=True)
  while proc.poll() is None:
    try:
      proc.wait(timeout=25)
    except subprocess.TimeoutExpired:
      lines = log.read_text(errors='replace').splitlines()
      progress = next((s for s in reversed(lines) if 'rendering ' in s or 'joining ' in s), 'renderer active')
      message = f'{label} render: {int(time.monotonic()-start)}s elapsed; {progress}'
      print(message, flush=True)
      with STATUS.open('a') as status:
        status.write('\n- '+time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime())+' Johnson: '+message+'\n')
  print(f'{label} render exited {proc.returncode} after {int(time.monotonic()-start)}s; log={log}', flush=True)
  if proc.returncode:
    print(log.read_text(errors='replace')[-4000:], flush=True)
sys.exit(proc.returncode)
