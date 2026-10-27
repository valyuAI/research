"""Serial local production stage with bounded heartbeat and durable status."""
import datetime
import fcntl
import json
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
  'preview': [sys.executable, '-B', str(TOOLS/'render.py'), str(ROOT), '--quality', 'l', '--contact', '--output', 'preview.mp4'],
  'dry-audio': [sys.executable, '-B', str(TOOLS/'make_audio.py'), str(ROOT), '--dry-run'],
  'audio': [sys.executable, '-B', str(TOOLS/'make_audio.py'), str(ROOT)],
  'final': [sys.executable, '-B', str(TOOLS/'render.py'), str(ROOT), '--quality', 'h', '--contact'],
  'qa': [sys.executable, '-B', str(ROOT/'verify_media.py')],
  'alignment': [sys.executable, '-B', str(ROOT/'verify_audio_alignment.py')],
}
if stage not in commands:
  raise SystemExit('Choose '+', '.join(commands))
env = {**os.environ, 'PYTHONUNBUFFERED':'1', 'PYTHONDONTWRITEBYTECODE':'1', 'OPENBLAS_NUM_THREADS':'1', 'OMP_NUM_THREADS':'1', 'MKL_NUM_THREADS':'1', 'VECLIB_MAXIMUM_THREADS':'1', 'NUMEXPR_NUM_THREADS':'1'}
if stage == 'final':
  spec=json.loads((ROOT/'narration.json').read_text())
  lengths=json.loads((ROOT/'audio/durations.json').read_text())
  assert [c['id'] for c in spec['clips']]==list(lengths), 'Audio manifest order differs'
  assert max(lengths.values())<=25, 'Split narration clips longer than25 seconds'
  assert all((ROOT/'audio'/f'{c["id"]}.mp3').exists() for c in spec['clips'])
render_lock=None
if stage in {'preview','final','qa','alignment'}:
  lock_path=Path(os.environ.get('VIDEO_RENDER_LOCK', '/tmp/valyu-research-final-render.lock'))
  render_lock=lock_path.open('a')
  while True:
    legacy=subprocess.run(['ps','-p','96759','-o','command='],capture_output=True,text=True).stdout
    reason='legacy algebra render PID96759' if 'tools/video/render.py' in legacy and 'mu-q-2-2/video' in legacy else None
    if reason is None:
      try:
        fcntl.flock(render_lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        print(f'Acquired shared final render lock: {lock_path}',flush=True)
        break
      except BlockingIOError:
        reason='another final render holds the shared lock'
    message=f'{ROOT.parent.name} {stage}: waiting for {reason}; lock {lock_path}'
    print(message,flush=True)
    with (ROOT/f'{stage}-wait.log').open('a') as wait_log:
      wait_log.write(datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')+' '+message+'\n')
    with STATUS.open('a') as sf:
      sf.write('\n- '+message+'.\n')
    time.sleep(15)
log=ROOT/f'{stage}.log'
start=time.monotonic()
with log.open('w') as f:
  child=subprocess.Popen(['nice','-n','10',*commands[stage]],stdout=f,stderr=subprocess.STDOUT,env=env)
  while True:
    rc=child.poll()
    elapsed=int(time.monotonic()-start)
    lines=log.read_text(errors='replace').replace('\r','\n').splitlines()
    last=lines[-1][-180:] if lines else 'starting'
    state='running' if rc is None else f'exit {rc}'
    message=f'{ROOT.parent.name} {stage}: {elapsed}s; pid {child.pid}; {state}; {last}'
    print(message,flush=True)
    with STATUS.open('a') as sf:
      sf.write(f'\n- {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}: {message}. Log: `{log}`.\n')
    if rc is not None:
      if render_lock is not None:
        fcntl.flock(render_lock.fileno(),fcntl.LOCK_UN)
        render_lock.close()
      raise SystemExit(rc)
    time.sleep(15)
