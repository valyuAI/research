"""Run one command with a 20-second heartbeat and preserve its exit status."""
import subprocess
import sys
import tempfile
import time


def run(command):
  with tempfile.TemporaryFile(mode='w+') as log:
    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
    start = time.monotonic()
    while True:
      try:
        code = process.wait(timeout=20)
        break
      except subprocess.TimeoutExpired:
        print(f'  running {time.monotonic() - start:.0f}s: {command[-1]}', flush=True)
    log.seek(0)
    output = log.read()
  print(output, end='', flush=True)
  if code:
    raise SystemExit(code)
  return output


if __name__ == '__main__':
  run(sys.argv[1:])
