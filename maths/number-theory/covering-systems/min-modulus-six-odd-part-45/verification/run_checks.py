#!/usr/bin/env python3
"""Run the exact checks; require completion, expected counts and survivor files."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time


def run(command):
  print('RUN ' + ' '.join(map(str, command)), flush=True)
  with tempfile.TemporaryFile(mode='w+') as log:
    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
    start = time.monotonic()
    while True:
      try:
        code = process.wait(timeout=20)
        break
      except subprocess.TimeoutExpired:
        print(f'  running {time.monotonic() - start:.0f}s', flush=True)
    log.seek(0)
    output = log.read()
  print(output, end='', flush=True)
  if code != 0:
    raise RuntimeError(f'command failed with exit {code}')
  return output


def validate(output, expected, survivor_file):
  totals = re.findall(r'^TOTAL nodes (\d+) survivors (\d+)$', output, re.M)
  if totals != [tuple(map(str, expected))]:
    raise RuntimeError(f'missing or wrong completion: expected {expected}, got {totals}')
  lines = survivor_file.read_text().splitlines()
  if len(lines) != expected[1] or any(len(line.split()) != 4 for line in lines):
    raise RuntimeError('survivor file disagrees with completed search')


def main():
  if not __debug__:
    raise SystemExit('FAIL: verification requires Python assertions enabled')
  root = Path(__file__).resolve().parent
  build = Path(sys.argv[1]).resolve()
  family = [list(map(int, line.split())) for line in (root / 'prices.txt').read_text().splitlines()]
  generic = [list(map(int, line.split())) for line in (root / 'prices_gen_order.txt').read_text().splitlines()]
  if len(family) != 11 or any(len(row) != 6 or min(row) < 0 or sum(row) == 0 for row in family):
    raise RuntimeError('invalid price family')
  if generic != [[row[i] for i in [0, 2, 1, 4, 3, 5]] for row in family]:
    raise RuntimeError('price order does not match the generic implementation')
  first10 = [list(map(int, line.split())) for line in (root / 'prices_first10.txt').read_text().splitlines()]
  if first10 != family[:10]:
    raise RuntimeError('negative-control family is not the first ten prices')
  if run([build / 'test_phi']).strip() != 'mismatches 0':
    raise RuntimeError('exact-cover self-test failed')
  for name, args, expected in [
    ('dfs2', [root / 'prices.txt', '1', '-1'], (498464, 0)),
    ('gen', ['2', '6', '2', root / 'prices_gen_order.txt', '1'], (66821, 0)),
    ('dfs2', [root / 'prices_first10.txt', '100000', '-1'], (708955, 1704)),
  ]:
    survivor_file = build / f'{name}_{expected[1]}.txt'
    output = run([build / name, *args, survivor_file])
    validate(output, expected, survivor_file)
  # Wrong counts and incomplete searches must not pass merely because they exit 0.
  for bad in ['TOTAL nodes 498464 survivors 1\n', 'max survivors reached\n', '']:
    try:
      validate(bad, (498464, 0), build / 'dfs2_0.txt')
    except RuntimeError:
      continue
    raise RuntimeError('completion-control failure')
  print('ALL EXACT CHECKS PASSED; three completion controls rejected', flush=True)


if __name__ == '__main__':
  main()
