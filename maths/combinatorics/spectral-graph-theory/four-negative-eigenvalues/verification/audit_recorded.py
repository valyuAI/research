"""Cross-check complete recorded runs against the census, including both terminating levels.

This audits existing evidence; it does not replace rerunning the enumerators with build.sh --full.
"""
import ast
import argparse
import gzip
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--require-generated', action='store_true')
args = parser.parse_args()

def require(ok, message):
  if not ok:
    sys.exit('FAIL: ' + message)

meta = json.loads((here / 'census_counts.json').read_text())
raw = gzip.decompress((here / 'census_nonsingular_nneg_le4.txt.gz').read_bytes())
require(hashlib.sha256(raw).hexdigest() == meta['sha256_uncompressed'], 'census checksum')
expected = {int(n): {int(q): c for q, c in d.items()} for n, d in meta['counts_by_order_and_nneg'].items()}
require(sum(map(sum, [d.values() for d in expected.values()])) == meta['total'] == 45242, 'census total')
counts = Counter()
census_rows = set()
for line in raw.decode().splitlines():
  g6, order, p, q = line.split()
  n, p, q = int(order), int(p), int(q)
  require(ord(g6[0]) - 63 == n and p + q == n, 'census header')
  bits = ''.join(f'{ord(c)-63:06b}' for c in g6[1:])
  a = [[0] * n for _ in range(n)]
  t = 0
  for j in range(1, n):
    for i in range(j):
      a[i][j] = a[j][i] = int(bits[t]); t += 1
  upper = ''.join(str(a[i][j]) for i in range(n) for j in range(i + 1, n))
  census_rows.add((n, p, q, upper))
  counts[n, q] += 1
require(dict(counts) == {(n, q): c for n, d in expected.items() for q, c in d.items()}, 'census per-order counts')
require(len(census_rows) == 45242, 'duplicate encoded census row')
for filename in ('enumerate_nonsingular.log', 'enumerate_check.log'):
  text = (here / filename).read_text()
  levels = {int(n): ast.literal_eval(d) for n, d in re.findall(r'order=(\d+).*?by n\^-: (\{[^\n]*?\})', text)}
  require(levels == {n: expected.get(n, {}) for n in range(1, 18)}, filename + ': levels/counts/termination')
generated = here / 'output/ns_k4'
if args.require_generated or generated.exists():
  output_rows = set()
  for n in range(1, 18):
    for line in (generated / f'order{n}.txt').read_text().splitlines():
      bits, p, q = line.split()
      output_rows.add((n, int(p), int(q), bits))
  require(output_rows == census_rows, 'enumerator output differs from census')
maxima = {5: 5, 6: 10, 7: 18, 8: 30, 9: 26, 10: 22, 11: 20, 12: 17, 13: 15, 14: 15, 15: 15}
primary = {int(n): int(m) for n, m in re.findall(r'rank=(\d+).*?max reduced order=(\d+)', (here / 'max_reduced_order.log').read_text())}
secondary_match = re.search(r'largest reduced order by rank: (\{[^\n]*?\})', (here / 'max_reduced_order_check.log').read_text())
require(primary == maxima and secondary_match is not None and ast.literal_eval(secondary_match[1]) == maxima, 'per-rank maxima disagree')
result = json.loads((here / 'check_census_result.json').read_text())
require(result['graphs'] == 45242 and result['inertia_or_duplicate_failures'] == 0 and result['counts_match_json'] and result['order15_are_W5_and_X'], 'census replay failed')
for filename in ('extremal_result.json', 'order30_check.json'):
  require(json.loads((here / filename).read_text())['all_checks_passed'] is True, filename)
require((here / 'extremal_doubling_check.log').read_text().rstrip().endswith('ALL OK'), 'doubling run incomplete')
print(json.dumps({'ok': True, 'census_graphs': 45242, 'sha256_uncompressed': meta['sha256_uncompressed'],
                  'generated_output_compared': generated.exists(),
                  'terminating_orders': [16, 17], 'max_reduced_order_by_rank': maxima,
                  'scope': 'complete recorded evidence audited; use --full for a fresh enumeration'}, indent=2))
