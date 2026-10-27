#!/usr/bin/env python3
"""Check completeness of retained replay records; this does not replay large strategies."""
import hashlib
import json
from pathlib import Path
import re

import sys

if not __debug__:
  raise SystemExit('FAIL: verification requires Python assertions enabled')

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / 'results.json').read_text())
seen = {}
for name in data['regenerated']['n6L7_red']['replay_logs']:
  text = (HERE / 'logs' / name).read_text()
  for r, c, count in re.findall(r'VERIFIED.*?first move \((\d+),(\d+)\); Red-to-move positions checked=(\d+)', text):
    first = (int(r) - 1) * 6 + int(c) - 1
    if first in seen:
      assert seen[first] == int(count)
    seen[first] = int(count)
assert set(seen) == set(range(36)) and sum(seen.values()) == 22780097
assert {str(k): v for k, v in seen.items()} == data['regenerated']['n6L7_red']['per_opening']
assert data['regenerated']['n6L7_red']['openings'] == 36
assert data['regenerated']['n6L7_red']['positions_total'] == sum(seen.values())
delta = (HERE / 'logs/replay_6x6_delta.log').read_text()
red = re.findall(r'== D9 opening (\d+) [^\n]+\nVERIFIED:.*?checked=(\d+)', delta)
assert {int(i) for i, _ in red} == set(range(36)) and len(red) == 36
assert sum(int(n) for _, n in red) == 1472836
assert 'Blue-to-move positions checked=5158730, max Blue stones=10' in delta
strict = (HERE / 'logs/replay_strict5.log').read_text()
assert 'strict n=5 l=6 first=(3,3)' in strict and 'keys checked=875938, max Blue stones=13' in strict
for name, record in data['shipped_5x5'].items():
  path = HERE / 'certs' / (name + '.txt.gz')
  assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256_gz'], ('certificate hash changed', name)
assert len(data['shipped_5x5']) == 100
D = '- - - - 8 - 8 9 7 10 - 9 7 9 - 10 7 9 8 - 8 - - - -'.split()
L = '- - - - 7 - 8 8 7 8 - 9 6 9 - 8 7 8 8 - 7 - - - -'.split()
expected = set()
for i in range(25):
  if D[i] == '-':
    expected.add(('D', 13, i, 'Red'))
  else:
    for mode, values in [('D', D), ('L', L)]:
      expected.add((mode, int(values[i]), i, 'Blue'))
      expected.add((mode, int(values[i]) - 1, i, 'Red'))
actual = re.findall(r'^([DL]) bound=(\d+) opening=(\d+): VERIFIED(?: \[[^\]]+\])?: (Blue|Red)',
                    (HERE / 'logs/table5.log').read_text(), re.M)
assert len(actual) == 64 and {(m, int(b), int(i), side) for m, b, i, side in actual} == expected
print('Retained Hex records: L7 36/36; D9 36/36; D10 and strict5 complete; table 64/64; 100 shipped hashes match')
