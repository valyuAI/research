"""Run the shared Manim pipeline with progress and durable job state."""
import datetime
import fcntl
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
TOOLS = next(p / 'tools/video' for p in ROOT.parents if (p / 'tools/video/render.py').exists())
STATUS = Path(os.environ.get('VIDEO_STATUS_FILE', os.devnull))
stage = sys.argv[1]
render_lock = None
if stage == 'final':
  render_lock = open(os.environ.get('VIDEO_RENDER_LOCK', '/tmp/valyu-research-final-render.lock'), 'a')
  while True:
    try:
      os.kill(96759, 0)
      reason = 'legacy render PID 96759'
    except ProcessLookupError:
      try:
        fcntl.flock(render_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print('Acquired shared final-render lock.', flush=True)
        break
      except BlockingIOError:
        reason = 'shared final-render lock'
    message = f'{ROOT.parent.name}: waiting for {reason}'
    print(message, flush=True)
    with STATUS.open('a') as sf:
      sf.write('\n- '+datetime.datetime.now(datetime.timezone.utc).isoformat()+': '+message+'\n')
    time.sleep(15)
commands = {
  'preview': [sys.executable, str(TOOLS/'render.py'), str(ROOT), '--quality', 'l', '--contact', '--output', 'preview.mp4'],
  'audio': [sys.executable, str(TOOLS/'make_audio.py'), str(ROOT)],
  'dry-audio': [sys.executable, str(TOOLS/'make_audio.py'), str(ROOT), '--dry-run'],
  'final': [sys.executable, str(TOOLS/'render.py'), str(ROOT), '--quality', 'h', '--contact'],
  'qa': [sys.executable, '-B', str(ROOT/'verify_media.py')],
}
log = ROOT/f'{stage}.log'
start = time.monotonic()
env = {**os.environ, 'PYTHONUNBUFFERED':'1', 'PYTHONDONTWRITEBYTECODE':'1', 'OPENBLAS_NUM_THREADS':'1', 'OMP_NUM_THREADS':'1', 'MKL_NUM_THREADS':'1', 'VECLIB_MAXIMUM_THREADS':'1', 'NUMEXPR_NUM_THREADS':'1'}
with log.open('w') as f:
  child = subprocess.Popen(['nice','-n','10',*commands[stage]], stdout=f, stderr=subprocess.STDOUT, env=env)
  while True:
    rc = child.poll()
    elapsed = int(time.monotonic()-start)
    lines = log.read_text(errors='replace').replace('\r','\n').splitlines()
    last = lines[-1][-180:] if lines else 'starting'
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    state = {'utc':now,'stage':stage,'pid':child.pid,'runner_pid':os.getpid(),'elapsed':elapsed,'exit_code':rc,'log':str(log),'last_output':last}
    (ROOT/'active-job.json').write_text(__import__('json').dumps(state,indent=2))
    print(f'{ROOT.parent.name} {stage}: {elapsed}s; pid {child.pid}; {last}',flush=True)
    with STATUS.open('a') as sf:
      sf.write(f'\n- {now}: {ROOT.parent.name}, {stage}, PID {child.pid}, {elapsed}s, '+('running' if rc is None else f'exit {rc}')+f'. Log: {log}\n')
    if rc is not None:sys.exit(rc)
    time.sleep(15)
