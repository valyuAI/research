"""Exact check of the four reduced graphs of order 30 with four negative eigenvalues.

Reads order30_graphs.g6 (written from classify_max_order.log), and for each graph checks exactly
(LDL^T over the rationals) that the inertia is (4, 22, 4), that it is reduced and connected, and that
the four graphs are pairwise non-isomorphic (distinct edge counts). It then builds two iterated
constructions starting from K2, on vertex set V u V' u {x, y} with A(V u V') = [[A, A], [A, A]]
(v and its copy v' are non-adjacent, and each is joined to u and u' for every neighbour u of v), x ~ y:
  (a) x ~ V and y ~ V'      (degree d -> 2d + 1; from K2 gives a 15-regular graph on 30 vertices)
  (b) y ~ V' only (x pendant)
and checks with networkx that after three steps they are isomorphic to two of the four graphs.

Usage: python order30_check.py
"""
import json, os, sys
import networkx as nx
import numpy as np
from verify_extremal import ldl_inertia, reduced, connected
from check_census import g6_decode

HERE = os.path.dirname(os.path.abspath(__file__))


def step(A, x_to_v, y_to_v):
  n = len(A)
  N = 2 * n + 2
  M = [[0] * N for _ in range(N)]
  for i in range(n):
    for j in range(n):
      for a in (0, n):
        for b in (0, n):
          M[a + i][b + j] = A[i][j]
  x, y = 2 * n, 2 * n + 1
  M[x][y] = M[y][x] = 1
  for i in range(n):
    if x_to_v:
      M[x][i] = M[i][x] = 1
    M[y][n + i] = M[n + i][y] = 1
  return M


def build(x_to_v):
  A = [[0, 1], [1, 0]]
  for _ in range(3):
    A = step(A, x_to_v, True)
  return A


def main():
  graphs = [g6_decode(l.strip()) for l in open(os.path.join(HERE, 'order30_graphs.g6')) if l.strip()]
  rows = []
  for A in graphs:
    rows.append({'order': len(A), 'edges': sum(map(sum, A)) // 2, 'inertia': list(ldl_inertia(A)),
                 'reduced': reduced(A), 'connected': connected(A)})
  ok = all(r['order'] == 30 and r['inertia'] == [4, 22, 4] and r['reduced'] and r['connected'] for r in rows)
  ok = ok and len({r['edges'] for r in rows}) == len(rows) == 4
  G = [nx.from_numpy_array(np.array(A)) for A in graphs]
  match = {}
  for name, xv in (('a: x~V, y~V\'', True), ('b: y~V\' only', False)):
    H = nx.from_numpy_array(np.array(build(xv)))
    match[name] = [i for i, g in enumerate(G) if nx.is_isomorphic(g, H)]
  out = {'graphs': rows, 'constructions_match_graph_index': match,
         'all_checks_passed': ok and all(len(v) == 1 for v in match.values())}
  print(json.dumps(out, indent=1))
  sys.exit(0 if out['all_checks_passed'] else 1)


if __name__ == '__main__':
  main()
