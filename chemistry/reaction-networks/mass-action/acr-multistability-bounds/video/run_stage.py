"""Serial Manim production with durable state and fifteen-second heartbeats."""
import datetime
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = next(p for p in ROOT.parents if (p / 'tools/video/render.py').exists())
TOOLS = REPO / 'tools/video'
STATUS = Path(os.environ.get('VIDEO_STATUS_FILE', os.devnull))
FINAL_LOCK = Path(os.environ.get('VIDEO_RENDER_LOCK', '/tmp/valyu-research-final-render.lock'))
PACKAGES = [
  'chemistry/reaction-networks/mass-action/acr-multistability-bounds',
  'maths/combinatorics/combinatorial-games/hex-short-wins',
  'maths/number-theory/covering-systems/min-modulus-six-odd-part-45',
  'maths/geometry/tilings/marked-polyform-heesch-numbers',
]


def update_status(state):
  (ROOT / 'production-state.json').write_text(json.dumps(state, indent=2) + '\n')
  lines = ['# Chemistry, Hex, covering systems and tilings: video production', '',
           'Shared worktree, campaign/2026-10-25-discoveries. Research is locked. Only the four video folders and this status file are owned.', '',
           'One heavy stage at a time for this worker; nice 10; BLAS single-thread. No nested agents, commits, pushes or public actions.', '']
  for package in PACKAGES:
    folder = REPO / package / 'video'
    path = folder / 'production-state.json'
    data = json.loads(path.read_text()) if path.exists() else {'stage': 'pending', 'status': 'pending'}
    lines += [f'## {folder.parent.name}', '', f'- State: {data.get("status")}; stage: {data.get("stage")}.',
              f'- Updated: {data.get("updatedUtc", "not started")}.',
              f'- Active process IDs: {data.get("activePids", [])}.',
              f'- Log: {data.get("log", "none")}.',
              f'- Scientific hashes: `{folder / "scientific-input-sha256.json"}`.',
              f'- QA: `{folder / "QA.md"}`; machine records: `{folder / "qa"}`.',
              f'- Final path (complete only when state says complete): `{folder / "video.mp4"}`.', '']
    provenance = folder / 'provenance-status.json'
    if provenance.exists():
      provenance_data = json.loads(provenance.read_text())
      lines += [f'- Scientific provenance: {provenance_data["status"]}; see `{provenance}`.', '']
    hashes = folder / 'qa/artifact-sha256.json'
    if hashes.exists():
      artifact = json.loads(hashes.read_text())
      lines += [f'- Artifact hashes: `{hashes}`.', f'- Final MP4 SHA-256: `{artifact.get("video.mp4", "pending")}`.', '']
    if data.get('note'):
      lines += [data['note'], '']
  STATUS.write_text('\n'.join(lines))


def descendants(pid):
  rows = subprocess.check_output(['ps', '-axo', 'pid=,ppid='], text=True).splitlines()
  pairs = [tuple(map(int, row.split())) for row in rows if len(row.split()) == 2]
  result = {pid}
  while True:
    new = result | {p for p, parent in pairs if parent in result}
    if new == result:
      return sorted(result)
    result = new


def main():
  if not __debug__:
    raise SystemExit("Video production requires Python assertions enabled.")
  stage = sys.argv[1]
  commands = {
    'preview': [str(TOOLS / 'render.py'), str(ROOT), '--quality', 'l', '--contact', '--output', 'preview.mp4'],
    'dry-audio': [str(TOOLS / 'make_audio.py'), str(ROOT), '--dry-run'],
    'audio': [str(TOOLS / 'make_audio.py'), str(ROOT)],
    'final': [str(TOOLS / 'render.py'), str(ROOT), '--quality', 'h', '--contact'],
    'final-repair': [str(ROOT / 'render_patch.py')],
    'qa': [str(ROOT / 'verify_media.py')],
    'alignment': [str(ROOT / 'verify_audio_alignment.py')],
  }
  env = {**os.environ, 'PYTHONUNBUFFERED': '1', 'PYTHONDONTWRITEBYTECODE': '1',
         'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
         'VECLIB_MAXIMUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1'}
  log = ROOT / f'{stage}.log'
  started = time.monotonic()
  lock_handle = None
  if stage.startswith('final'):
    lock_handle = FINAL_LOCK.open('a+')
    while True:
      legacy = subprocess.run(['ps', '-p', '96759', '-o', 'command='], capture_output=True, text=True)
      legacy_running = legacy.returncode == 0 and 'render.py' in legacy.stdout
      acquired = False
      if not legacy_running:
        try:
          fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
          acquired = True
        except BlockingIOError:
          pass
      if acquired:
        print(f'Final render lock acquired: {FINAL_LOCK}', flush=True)
        break
      reason = 'legacy render PID 96759' if legacy_running else 'shared final-render lock'
      print(f'{ROOT.parent.name}: waiting for {reason}; elapsed {int(time.monotonic()-started)}s', flush=True)
      update_status({'stage':'final lock wait','status':'waiting','activePids':[os.getpid()],
                     'updatedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     'log':str(log),'note':f'Waiting for {reason}. Lock file retained, never replaced.'})
      time.sleep(15)
  with log.open('w') as stream:
    child = subprocess.Popen(['nice', '-n', '10', sys.executable, '-B', *commands[stage]],
                             stdout=stream, stderr=subprocess.STDOUT, env=env)
    while True:
      rc = child.poll()
      elapsed = int(time.monotonic() - started)
      content = log.read_text(errors='replace').replace('\r', '\n').splitlines()
      tail = content[-1][-190:] if content else 'starting'
      print(f'{ROOT.parent.name} {stage}: {elapsed}s; pid {child.pid}; {tail}', flush=True)
      update_status({'stage': stage, 'status': 'running' if rc is None else ('stage passed' if rc == 0 else 'stage failed'),
                     'updatedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     'activePids': descendants(child.pid) if rc is None else [],
                     'runnerPid': os.getpid() if rc is None else None, 'log': str(log),
                     'elapsedSeconds': elapsed, 'exitCode': rc})
      if rc is not None:
        if lock_handle is not None:
          fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
          lock_handle.close()
        sys.exit(rc)
      time.sleep(15)


if __name__ == '__main__':
  main()
