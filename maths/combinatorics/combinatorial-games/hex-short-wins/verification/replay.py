#!/usr/bin/env python3
"""Replay a certificate and bind successful output to its expected filename scope."""
from pathlib import Path
import re
import sys

from progress import run

checker, certificate = sys.argv[1:]
base = Path(certificate).name.removesuffix('.gz').removesuffix('.txt')
match = re.fullmatch(r'n(\d+)([LD])(\d+)_(\d+)(_red)?', base)
strict = re.fullmatch(r'strict(\d+)_(\d+)_(\d+)', base)
if match and Path(checker).name == 'check_cert.py':
  n, mode, bound, first, red = match.groups()
  expect = f"VERIFIED [n={n} mode={mode} bound={bound} first={first} side={'red' if red else 'blue'}]"
elif strict and Path(checker).name == 'check_strict.py':
  n, bound, first = strict.groups()
  expect = f'VERIFIED [strict n={n} bound={bound} first={first}]'
else:
  raise SystemExit('FAIL: unrecognized certificate filename or wrong checker')
print(f'Replay {certificate}', flush=True)
output = run([sys.executable, checker, certificate])
lines = output.strip().splitlines()
if not lines or not lines[-1].startswith(expect + ':') and not lines[-1].startswith(expect + ' (strict reading):'):
  raise SystemExit(f'FAIL: expected scoped conclusion {expect}')
