"""Run one existing pipeline stage with a heartbeat and durable local log."""
import datetime
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
TOOLS = next(p / 'tools/video' for p in ROOT.parents if (p / 'tools/video/render.py').exists())
STATUS = Path(os.environ.get('VIDEO_STATUS_FILE', os.devnull))
stage = sys.argv[1]
commands = {
  'sharp-preview': [sys.executable, str(TOOLS/'render.py'), str(ROOT), '--quality', 'l', '--scenes', 'Budget', 'ManyTrees', '--contact', '--output', 'sharp-preview.mp4'],
  'witness-preview': [sys.executable, str(TOOLS/'render.py'), str(ROOT), '--quality', 'l', '--scenes', 'Witness', '--contact', '--output', 'witness-restriction-preview.mp4'],
  'preview': [sys.executable, str(TOOLS/'render.py'), str(ROOT), '--quality', 'l', '--contact', '--output', 'preview.mp4'],
  'audio': [sys.executable, str(TOOLS/'make_audio.py'), str(ROOT)],
  'dry-audio': [sys.executable, str(TOOLS/'make_audio.py'), str(ROOT), '--dry-run'],
  'final': [sys.executable, str(TOOLS/'render.py'), str(ROOT), '--quality', 'h', '--contact'],
}
cmd = ['nice', '-n', '10', *commands[stage]]
log = ROOT/f'{stage}.log'
start = time.monotonic()
with log.open('w') as f:
  child = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, env={**os.environ, 'PYTHONUNBUFFERED':'1', 'PYTHONDONTWRITEBYTECODE':'1'})
  while True:
    rc = child.poll()
    elapsed = int(time.monotonic()-start)
    lines = log.read_text(errors='replace').replace('\r','\n').splitlines()
    last = lines[-1][-220:] if lines else 'starting'
    print(f'{ROOT.parent.name} {stage}: {elapsed}s; pid {child.pid}; {last}', flush=True)
    with STATUS.open('a') as sf:
      sf.write(f'\n- {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}: {ROOT.parent.name} {stage}, {elapsed}s, pid {child.pid}, '+ ('running' if rc is None else f'exit {rc}')+'.\n')
    if rc is not None:
      sys.exit(rc)
    time.sleep(15)
