"""Bind replay results to the exact certificates and every retained theorem claim."""
import hashlib
import json
import math
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
quick = sys.argv[1:] == ['--quick']
if sys.argv[1:] not in ([], ['--quick']):
  sys.exit('Usage: check_results.py [--quick]')
names = [f'n{n}_k3{suffix}' for n in range(3, 8) for suffix in ('', '_mt')]
names += ['n5_k3_mt_small']
if not quick:
  names += ['n7_k4', 'n8_k3', 'n8_k3_mt']
classes = {3: 2, 4: 4, 5: 12, 6: 56, 7: 456, 8: 6880}
for name in names:
  path = here / 'certificates' / f'rule_{name}.json'
  raw = path.read_bytes()
  cert = json.loads(raw)
  result = json.loads((here / 'results' / f'rule_{name}.result.json').read_text())
  n, k = cert['n'], cert['k']
  alpha = '3/7' if k == 4 else '1/3' if n <= 4 else '2/5'
  expected = classes[n] * sum(math.comb(n, s) * (2 ** math.comb(s, 2) - 1) for s in range(2, k + 1))
  checks = [
    result.get('ok') is True,
    result.get('certificate_sha256') == hashlib.sha256(raw).hexdigest(),
    result.get('classes') == len(cert['classes']) == classes[n],
    result.get('manipulations') == expected,
    result.get('max_gain') == result.get('alpha') == cert['alpha'] == alpha,
    result.get('mode') == cert['mode'] == 'le',
    result.get('n') == n and result.get('k') == k,
    result.get('shard', '0/1') == '0/1',
  ]
  if '_mt' in name:
    checks += [cert.get('monotone') is True, cert.get('top_cycle') is True]
    checks += ['top-cycle consistent' in result.get('properties', [])]
    checks += [f'monotone ({classes[n] * math.comb(n, 2)} single-match reversals checked)' in result.get('properties', [])]
  if not all(checks):
    sys.exit(f'FAIL: incomplete or mismatched evidence for {name}: {checks}')
  print(f'{name}: certificate hash, exact value, properties and {expected} manipulations confirmed', flush=True)
