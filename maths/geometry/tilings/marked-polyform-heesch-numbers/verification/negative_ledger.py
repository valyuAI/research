#!/usr/bin/env python3
"""Reject incomplete ledgers and mismatched or ambiguous retained-log scope."""
import copy
import json
from pathlib import Path
import re
import tempfile

from check_ledger import main as check

import sys

if not __debug__:
  raise SystemExit('FAIL: verification requires Python assertions enabled')

HERE = Path(__file__).resolve().parent
original = json.loads((HERE / 'results.json').read_text())


def verify_case(label, data, expected_error=None):
  with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
    json.dump(data, f)
    f.flush()
    try:
      check(f.name)
    except (AssertionError, FileNotFoundError) as exc:
      if expected_error is None or expected_error not in str(exc):
        raise
      print(f'PASS {label}: rejected ({exc})', flush=True)
    else:
      assert expected_error is None, ('corrupted ledger accepted', label)
      print(f'PASS {label}: accepted', flush=True)


def verify_log(label, tile_index, text, expected_error=None):
  with tempfile.NamedTemporaryFile(mode='w', suffix='.log') as f:
    f.write(text)
    f.flush()
    data = copy.deepcopy(original)
    data['tiles'][tile_index]['upper_bound']['evidence_log'] = f.name
    verify_case(label, data, expected_error)


for field, value, error in [
  ('drat_verified', False, 'no verified upper bound'),
  ('k', 99, 'upper bound is not at k = h + 1'),
  ('proof_sha256', '0' * 64, 'hash not in log'),
  ('evidence_log', 'logs/drat/missing.log', 'missing.log'),
]:
  data = copy.deepcopy(original)
  data['tiles'][0]['upper_bound'][field] = value
  verify_case('metadata ' + field, data, error)
data = copy.deepcopy(original)
data['tiles'].pop()
verify_case('missing tile', data, 'ledger does not match the enumeration')
data = copy.deepcopy(original)
data['tiles'][0]['h'] += 1
verify_case('wrong witness corona count', data, 'coronas')
print('Ledger controls: all 6 corrupted metadata ledgers rejected', flush=True)

# Use an intact proof record and log for a different tile with the same h.
data = copy.deepcopy(original)
donor = next(t for t in original['tiles'] if t['name'] == 'dihex')
recipient = next(t for t in data['tiles'] if t['name'] == 'straight trihex')
cells = recipient['upper_bound']['cells']
recipient['upper_bound'] = copy.deepcopy(donor['upper_bound'])
recipient['upper_bound']['cells'] = cells
verify_case('genuine dihex proof substituted for straight trihex', data, 'formula log is for another tile')

log = (HERE / original['tiles'][0]['upper_bound']['evidence_log']).read_text()
scope = next(line for line in log.splitlines() if 'cells=' in line)
scope_errors = [
  ('missing scope', '', 'missing or ambiguous formula scope'),
  ('duplicate scope', scope + '\n' + scope, 'missing or ambiguous formula scope'),
  ('conflicting scope', scope + '\n' + scope.replace(' k=4 ', ' k=5 '), 'missing or ambiguous formula scope'),
  ('malformed second scope', scope + '\n' + scope.replace(' k=4 ', ' k=bad '), 'missing or ambiguous formula scope'),
  ('unknown-grid second scope', scope + '\n' + scope.replace('hex cells=', 'tri cells='), 'missing or ambiguous formula scope'),
  ('wrong grid', scope.replace('hex cells=', 'sq cells='), 'formula log is for another tile'),
  ('wrong k', scope.replace(' k=4 ', ' k=5 '), 'formula log has wrong bound or imbalance'),
  ('zero imbalance', scope.replace(' imb=1 ', ' imb=0 '), 'formula log has wrong bound or imbalance'),
  ('wrong positive imbalance', scope.replace(' imb=1 ', ' imb=2 '), 'formula log has wrong bound or imbalance'),
  ('negative imbalance', scope.replace(' imb=1 ', ' imb=-1 '), 'invalid formula scope'),
  ('malformed k', scope.replace(' k=4 ', ' k=4x '), 'invalid formula scope'),
  ('unexpected slots field', scope.replace(' radius=', ' slots=2 radius='), 'invalid formula scope'),
  ('truncated scope', scope.split(' radius=')[0] + ' radius=', 'invalid formula scope'),
  ('trailing scope text', scope + ' k=5', 'invalid formula scope'),
]
for field in ('placements', 'vars', 'clauses'):
  changed = re.sub(r'\b' + field + r' [0-9]+', field + ' 0', scope)
  scope_errors.append(('wrong ' + field, changed, 'formula log has wrong dimensions'))
for label, cells, error in [
  ('extra coordinate', '[[0, 0, 999]]', 'invalid formula cells'),
  ('missing coordinate', '[[0]]', 'invalid formula cells'),
  ('float coordinate', '[[0.0, 0]]', 'invalid formula cells'),
  ('boolean coordinate', '[[false, 0]]', 'invalid formula cells'),
  ('string coordinate', '[["0", 0]]', 'invalid formula cells'),
  ('empty cells', '[]', 'invalid formula cells'),
  ('null cell', '[null]', 'invalid formula cells'),
  ('invalid JSON cells', '[[0, 0],]', 'invalid formula cells'),
  ('duplicate cells', '[[0, 0], [0, 0]]', 'formula log is for another tile'),
]:
  scope_errors.append((label, scope.replace('[[0, 0]]', cells), error))
for label, changed, error in scope_errors:
  verify_log(label, 0, log.replace(scope, changed), error)

# Change geometry without changing cell count, k, hashes or success markers.
index = next(i for i, t in enumerate(original['tiles']) if t['name'] == 'straight trihex')
log = (HERE / original['tiles'][index]['upper_bound']['evidence_log']).read_text()
changed = log.replace('cells=[[0, 0], [0, 1], [0, 2]]', 'cells=[[0, 0], [0, 1], [1, 0]]')
assert changed != log
verify_log('same-size wrong tile', index, changed, 'formula log is for another tile')
print(f'Log controls: all {len(scope_errors) + 2} swapped-record/scope corruptions rejected', flush=True)

# Positive fixtures use explicit coordinate maps, independently of canon/syms.
for grid, name in [('hex', 'tetrahex 1'), ('sq', '4-omino sq05')]:
  index = next(i for i, t in enumerate(original['tiles']) if t['name'] == name)
  upper = original['tiles'][index]['upper_bound']
  log = (HERE / upper['evidence_log']).read_text()
  cells = upper['cells']
  transforms = {
    'translated': [[x + 7, y - 11] for x, y in cells],
    'rotated': [[-y, x + y if grid == 'hex' else x] for x, y in cells],
    'reflected': [[x + y if grid == 'hex' else x, -y] for x, y in cells],
    'reordered': list(reversed(cells)),
  }
  for label, transformed in transforms.items():
    changed = re.sub(r'cells=\[.*\] k=', 'cells=' + json.dumps(transformed) + ' k=', log)
    assert changed != log
    verify_log(grid + ' ' + label, index, changed)
print('Log controls: all 8 equivalent-geometry fixtures accepted', flush=True)
