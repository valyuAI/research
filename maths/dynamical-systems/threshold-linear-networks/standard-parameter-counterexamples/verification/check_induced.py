"""Exact check (standard library) that no proper induced subgraph of a given graph, on at least 2 vertices and not a
clique, has a stable permitted full support at eps = 1/4, delta = 1/2 (beta = t = 3).
Usage: python3 check_induced.py examples/G11.json"""
import json, sys, os
from itertools import combinations
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_ctln import berkowitz, lienard_chipart_stable, solve

d = json.load(open(sys.argv[1])); n = d['n']; E = set(map(tuple, d['edges']))
if F(d['eps']) != F(1, 4) or F(d['delta']) != F(1, 2):
  sys.exit('FAIL: this checker is restricted to the standard parameters')
N = [[0 if (i == j or (j, i) in E) else 1 for j in range(n)] for i in range(n)]
counts = {'subsets': 0, 'clique': 0, 'not_permitted': 0, 'not_stable': 0, 'stable': 0}
for r in range(2, n):
  for S in combinations(range(n), r):
    counts['subsets'] += 1
    M = [[N[i][j] for j in S] for i in S]
    if not any(map(any, M)): counts['clique'] += 1; continue
    C = [[(1 if a == b else 0) + 3 * M[a][b] for b in range(r)] for a in range(r)]
    if not all(v > 0 for v in solve(C, [1] * r)): counts['not_permitted'] += 1; continue
    c = berkowitz([[C[a][b] + 3 for b in range(r)] for a in range(r)])
    if lienard_chipart_stable([c[k] * (-1) ** k for k in range(r + 1)]):
      counts['stable'] += 1; print('STABLE induced subgraph', S)
    else: counts['not_stable'] += 1
print(json.dumps(counts))
print('NO PROPER INDUCED SUBGRAPH WORKS' if counts['stable'] == 0 else 'FOUND SMALLER')
sys.exit(0 if counts['stable'] == 0 and counts['subsets'] == 2 ** n - n - 2 else 1)
