"""Run one recorded Singular input with a wall-clock limit and progress."""

import argparse
import json
import select
import subprocess
import time
from pathlib import Path


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("input", type=Path)
  parser.add_argument("--seconds", type=float, default=120)
  args = parser.parse_args()
  start = time.monotonic()
  timed_out = False
  with args.input.with_suffix(".log").open("w") as log:
    proc = subprocess.Popen(
      ["Singular", "-q", str(args.input)], stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT, text=True, bufsize=1,
    )
    last = start
    while proc.poll() is None:
      now = time.monotonic()
      if now - start >= args.seconds:
        timed_out = True
        proc.kill()
        print(f"TIME LIMIT {args.seconds}s: killed pass", flush=True)
        break
      ready, _, _ = select.select([proc.stdout], [], [], 1)
      if ready:
        line = proc.stdout.readline()
        if line:
          log.write(line)
          log.flush()
          print(line, end="", flush=True)
      if now - last >= 10:
        print(f"heartbeat elapsed={now - start:.1f}s", flush=True)
        last = now
    rest = proc.communicate()[0]
    log.write(rest)
    print(rest, flush=True)
  result = {
    "input": args.input.name,
    "returncode": proc.returncode,
    "elapsed_seconds": round(time.monotonic() - start, 2),
    "timeout": timed_out,
  }
  args.input.with_name(args.input.stem + "_run.json").write_text(
    json.dumps(result, indent=2) + "\n"
  )
  print(result, flush=True)


if __name__ == "__main__":
  main()
