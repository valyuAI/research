"""Reconstruct every saved coefficient using the standard-library enumerator."""

import json
import threading
import time
from pathlib import Path

from enumerate_python import compute


def main():
  data = json.loads(Path(__file__).with_name('certificates.json').read_text())
  started = time.monotonic()
  stopped = threading.Event()

  def heartbeat():
    while not stopped.wait(20):
      print(f'Python reconstruction running, elapsed={time.monotonic()-started:.0f}s', flush=True)

  thread = threading.Thread(target=heartbeat, daemon=True)
  thread.start()
  try:
    for k, rows in data['cases'].items():
      for index, row in enumerate(rows, 1):
        coefficients, _ = compute(tuple(row['pattern']), row['cutoff'])
        if coefficients != row['coefficients']:
          raise RuntimeError(f'Coefficient mismatch: {row["pattern"]}')
        if k == '4' or index % 20 == 0 or index == len(rows):
          print(f'Python k={k}, {index}/{len(rows)} MATCH, elapsed={time.monotonic()-started:.1f}s', flush=True)
  finally:
    stopped.set()
    thread.join()
  print('All 2952 Python coefficient reconstructions MATCH', flush=True)


if __name__ == '__main__':
  main()
