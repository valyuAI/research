#!/usr/bin/env python3
"""A positive 4x4 strict strategy and six deliberately invalid variants."""
import gzip
from pathlib import Path
import subprocess
import sys
import tempfile

if not __debug__:
  raise SystemExit('FAIL: verification requires Python assertions enabled')

HERE = Path(__file__).resolve().parent
checker = HERE / 'py/check_strict.py'
with gzip.open(HERE / 'certs/strict4_5_3.txt.gz', 'rt') as f:
  original = f.read().splitlines()


def evaluate(lines):
  with tempfile.NamedTemporaryFile(mode='w', suffix='.txt') as f:
    f.write('\n'.join(lines) + '\n')
    f.flush()
    result = subprocess.run([sys.executable, checker, f.name], capture_output=True, text=True)
  return result


positive = evaluate(original)
assert positive.returncode == 0 and 'VERIFIED [strict n=4 bound=5 first=3]' in positive.stdout
print('Strict positive control:', positive.stdout.splitlines()[-1], flush=True)
mutants = [
  [original[0]],
  [original[0].replace('bound=5', 'bound=4')] + original[1:],
  [original[0].replace('first=3', 'first=0')] + original[1:],
  [original[0].replace('n=4', 'n=1')] + original[1:],
  [original[0]] + [' '.join(line.split()[:3] + ['16']) for line in original[1:]],
  [original[0]] + [' '.join(line.split()[:3] + [str((int(line.split()[0], 16) & -int(line.split()[0], 16)).bit_length() - 1)])
                  for line in original[1:]],
]
for index, lines in enumerate(mutants, 1):
  result = evaluate(lines)
  assert result.returncode != 0 and 'VERIFIED' not in result.stdout, ('strict mutant accepted', index)
print(f'Strict controls: all {len(mutants)} corrupted certificates rejected')
