#!/usr/bin/env python3
"""Reconcile retained independent-encoder and unmarked comparison logs."""
import json
from pathlib import Path
import re

from check_ledger import canon

import sys

if not __debug__:
  raise SystemExit('FAIL: verification requires Python assertions enabled')

HERE = Path(__file__).resolve().parent
tiles = json.loads((HERE / 'results.json').read_text())['tiles']
expected = {(t['grid'], t['name'], k, outcome) for t in tiles
            if t['name'] not in ('straight tetrahex', 'straight pentahex')
            for k, outcome in [(t['h'], 'SAT'), (t['h'] + 1, 'UNSAT')]}
actual = []
for line in (HERE / 'logs/second_encoder.log').read_text().splitlines():
  match = re.fullmatch(r'(hex|sq) (.+) k=(\d+): marked_gen (SAT|UNSAT) \(expected \4\) OK \(\d+s\)', line)
  assert match, ('unrecognized or failed comparison', line)
  g, name, k, outcome = match.groups()
  actual.append((g, name, int(k), outcome))
assert len(actual) == len(set(actual)) and set(actual) == expected
external = {}
lines = (HERE / 'logs/unmarked/heesch_sat.txt').read_text().splitlines()
assert len(lines) % 2 == 0
for cells_line, outcome in zip(lines[::2], lines[1::2]):
  assert cells_line.startswith('H ') and outcome.startswith('~ ')
  coords = list(map(int, cells_line.split()[1:]))
  key = canon('hex', list(zip(coords[::2], coords[1::2])))
  hh, hc, transitive = map(int, outcome.split()[1:])
  assert key not in external
  external[key] = hc
ours = {}
for line in (HERE / 'logs/unmarked/ours.jsonl').read_text().splitlines():
  row = json.loads(line)
  key = canon('hex', row['cells'])
  assert key not in ours
  ours[key] = row['Hc']
assert len(ours) == 41 and ours == external
print(f'Retained comparisons: {len(actual)} marked SAT/UNSAT agreements; {len(ours)} unmarked Hc agreements')
