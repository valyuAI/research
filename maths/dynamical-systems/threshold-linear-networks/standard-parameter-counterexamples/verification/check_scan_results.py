"""Require complete scan counts and bind each rational recheck to its candidate files."""
import hashlib
import json
import re
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
expected = {2: 3, 3: 16, 4: 218, 5: 9608, 6: 1540944}

def require(ok, message):
  if not ok:
    sys.exit('FAIL: ' + message)

def check_replay(path, files, count, stable):
  d = json.loads(path.read_text())
  require(d['ok'] is True and d['candidates'] == count and d['stable'] == stable, str(path))
  require(d['inputs_sha256'] == {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
          'recheck/input hash mismatch: ' + str(path))

for n, count in expected.items():
  stem = f'n{n}_std'
  d = json.loads((here / 'scan_results' / f'{stem}.summary.json').read_text())
  require(d['total'] == count and d['nonzero'] == count - 1 and d['undecided'] == 0,
          'incomplete standard scan ' + stem)
  check_replay(here / 'scan_results' / f'{stem}.recheck.json',
               [here / 'scan_results' / f'{stem}.txt'], d['coefpos'], 0)
control = json.loads((here / 'scan_results/n6_control.summary.json').read_text())
require(control['total'] == expected[6] and control['nonzero'] == expected[6] - 1, 'control count')
check_replay(here / 'scan_results/n6_control.recheck.json', [here / 'scan_results/n6_control.txt'], control['coefpos'], 2)

total = candidates = permitted = floatrej = 0
files = []
for shard, expected_total in enumerate((139411110, 193878344, 548743986)):
  stem = f'n7_std_{shard}'
  path = here / 'recovery' / f'{stem}.txt'
  lines = (here / 'recovery' / f'{stem}.err').read_text().splitlines()
  d = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', lines[-1])}
  require(d.get('total') == expected_total and d.get('beta') == d.get('t') == 3 and d.get('den') == 1,
          'missing or mismatched final shard summary')
  require(d['hits'] == d['undecided'] == 0 and sum(1 for _ in path.open()) == d['coefpos'], 'shard candidates')
  total += d['total']; candidates += d['coefpos']; permitted += d['permitted']; floatrej += d['floatrej']
  files.append(path)
require(total == 882033440 and candidates == 35842, 'aggregate n7 count')
check_replay(here / 'scan_results/n7_recovered.recheck.json', files, candidates, 0)
print(json.dumps({'ok': True, 'n7_digraphs': total, 'n7_exact_candidates': candidates,
                  'n7_exact_stable': 0, 'n7_permitted': permitted,
                  'n7_residual_bound_rejections': floatrej,
                  'n2_to_n6': expected, 'positive_control_stable': 2}, indent=2))
