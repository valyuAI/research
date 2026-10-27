"""Run the shared Manim pipeline with UTC heartbeats and a preserved log."""
import os
import queue
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
repo = next(p for p in root.parents if (p / "tools/video/render.py").exists())
env = dict(os.environ, PYTHONUNBUFFERED="1", PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1",
           OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
cmd = [sys.executable, "-u", str(repo / "tools/video/render.py"), str(root),
       "--quality", "h", "--fps", "30", "--contact", "--output", "video-1080p-candidate.mp4"]
events = queue.Queue()
logPath = root / "audit/render-1080p.log"
start = time.monotonic()
lastHeartbeat = start
with logPath.open("a") as log:
  def emit(message):
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"{stamp} {message}"
    print(line, flush=True)
    log.write(line + "\n")
    log.flush()

  emit("Start native 1920x1080, 30 fps render; one scene worker.")
  proc = subprocess.Popen(cmd, cwd=repo, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, bufsize=1)

  def readOutput():
    for line in proc.stdout:
      events.put(line.rstrip())
    events.put(None)

  reader = threading.Thread(target=readOutput, daemon=True)
  reader.start()
  ended = False
  while not ended:
    try:
      line = events.get(timeout=1)
      if line is None:
        ended = True
      elif line:
        emit(line)
    except queue.Empty:
      pass
    if time.monotonic() - lastHeartbeat >= 15:
      logs = list((root / "media/logs").glob("*.log"))
      current = max(logs, key=lambda p: p.stat().st_mtime).name if logs else "starting"
      emit(f"Progress: {int(time.monotonic() - start)} seconds elapsed; current scene log {current}")
      lastHeartbeat = time.monotonic()
  rc = proc.wait()
  emit(f"Render exit {rc}; elapsed {int(time.monotonic() - start)} seconds")
  sys.exit(rc)

