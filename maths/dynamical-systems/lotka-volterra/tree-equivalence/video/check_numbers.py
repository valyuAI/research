"""Check every number shown in the video against the verifier's own rules.

  python3 check_numbers.py      (needs networkx and sympy)

Uses generic_matrix, completeness and reconstruction from ../verification/verify_lv_tree.py,
so the tables in the video are the verifier's explicit generic parameters (species k+1 in
the video is vertex k in the verifier).
"""

import json
import sys
from pathlib import Path

import networkx as nx
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'verification'))
import verify_lv_tree as v  # noqa: E402

chain = nx.path_graph(4)                      # 1-2-3-4
star = nx.star_graph(3)                       # centre 1, leaves 2, 3, 4
x = sp.symbols('x1:5')


def table(tree):
  return v.generic_matrix(tree)


def field(A):
  n = len(A)
  return [x[i] * sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]


def edge_form(A, u, w):
  """Paper: P_uv = (A_vu - a_u) x_u + (a_v - A_uv) x_v."""
  return (A[w][u] - A[u][u]) * x[u] + (A[w][w] - A[u][w]) * x[w]


def is_darboux(A, L):
  F = field(A)
  dL = sp.expand(sum(sp.diff(L, x[i]) * F[i] for i in range(len(A))))
  q = sp.div(dL, L, *x)
  return q[1] == 0, sp.expand(q[0])


out = {}
for name, tree in [('chain', chain), ('star', star)]:
  A = table(tree)
  print(f'{name} table (rows = affected species):')
  for row in A:
    print('   ', row)
  assert v.completeness(tree) == 7          # complete support enumeration: 4 singles + 3 edges
  assert v.reconstruction(tree) == 3        # three dependent triples, tree rebuilt
  forms = {}
  for u, w in sorted(tree.edges()):
    L = edge_form(A, u, w)
    ok, C = is_darboux(A, L)
    assert ok
    forms[f'{u + 1}{w + 1}'] = {'form': str(L), 'cofactor': str(C)}
    print(f'  edge {u + 1}-{w + 1}: L = {L}, rate of L = L * ({C})')
  out[name] = {'table': A, 'edge_forms': forms}

# The two-species plane (species 3 and 4 absent) of the chain.
A = out['chain']['table']
x1, x2 = x[0], x[1]
F2 = [x1 * (A[0][0] * x1 + A[0][1] * x2), x2 * (A[1][0] * x1 + A[1][1] * x2)]
L = 26 * x1 - 27 * x2
dL = sp.expand(26 * F2[0] - 27 * F2[1])
print('plane: rate of (26x1 - 27x2) =', dL, '=', sp.factor(dL))
assert sp.expand(L * (-25 * x1 - 26 * x2) - dL) == 0

# Mixing on the plane: y1 = x1, y2 = 27x2 - 26x1.
y1, y2 = sp.symbols('y1 y2')
sub = {x1: y1, x2: (y2 + 26 * y1) / 27}
dy1 = sp.expand(F2[0].subs(sub))
dy2 = sp.expand((27 * F2[1] - 26 * F2[0]).subs(sub))
B = [[sp.Rational(dy1.coeff(y1, 2)), sp.Rational(sp.expand(dy1 / y1).coeff(y2))],
     [sp.Rational(sp.expand(dy2 / y2).coeff(y1)), sp.Rational(dy2.coeff(y2, 2))]]
assert sp.expand(dy1 - y1 * (B[0][0] * y1 + B[0][1] * y2)) == 0
assert sp.expand(dy2 - y2 * (B[1][0] * y1 + B[1][1] * y2)) == 0
print('mixed table B =', [[27 * b for b in r] for r in B], '/ 27')
out['plane_B_times_27'] = [[int(27 * b) for b in r] for r in B]

# Three in a row (species 1, 2, 3 of the chain): pair equations from the paper,
# p_i (A_jj - A_ij) = p_j (A_ji - A_ii), written as a p_i + b p_j = 0.
p = sp.symbols('p1:4')
eqs = []
for i, j in [(0, 1), (1, 2), (0, 2)]:
  eqs.append(sp.expand(-(p[i] * (A[j][j] - A[i][j]) - p[j] * (A[j][i] - A[i][i]))))
print('pair equations:', [str(e) + ' = 0' for e in eqs])
combo = sp.expand(eqs[0] - 26 * sp.expand(eqs[1] / 28) + eqs[2])
print('E1 - 26*(E2/28) + E3 =', combo)
assert combo == 55 * p[0]
assert v.admitted_support(A, (0, 1, 2)) is False
assert v.admitted_support(A, (0, 2)) is False   # skips species 2: column-2 mismatch 1 vs 2
assert A[0][1] == 1 and A[2][1] == 2

# A scrambling mixing x = N y (integer, determinant 1) for the label-scramble animation.
N = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [1, 0, 1, 1], [0, 0, 1, 1]])
print('det N =', N.det())
assert N.det() in (1, -1)
ys = sp.symbols('y1:5')
chain_forms = [x[0], x[1], x[2], x[3], 26 * x[0] - 27 * x[1], x[1] - x[2], x[2] - x[3]]
subN = dict(zip(x, list(N * sp.Matrix(ys))))
mixed = [sp.expand(f.subs(subN)) for f in chain_forms]
print('chain invariants rewritten after mixing:', mixed)
assert sp.expand(mixed[4] - (26 * mixed[0] - 27 * mixed[1])) == 0
# On screen the pair mixture is written with the opposite sign, 27x2 - 26x1 (same invariant).
L2 = 27 * x2 - 26 * x1
assert sp.expand(sp.expand(27 * F2[1] - 26 * F2[0]) - (650 * x1**2 + x1 * x2 - 702 * x2**2)) == 0
assert sp.expand(L2 * (-25 * x1 - 26 * x2) - (650 * x1**2 + x1 * x2 - 702 * x2**2)) == 0
assert sp.expand(-mixed[4] - (27 * mixed[1] - 26 * mixed[0])) == 0
print('after mixing, 27x2 - 26x1 becomes', sp.expand(-mixed[4]))
out['mixed_chain_forms'] = [str(m) for m in mixed]
out['N'] = [list(map(int, N.row(i))) for i in range(4)]

# Degenerate example from the paper's remark: equal rows make every linear form Darboux.
Aeq = [[1, 2, 3, 4]] * 4
ok, _ = is_darboux(Aeq, 5 * x[0] - 3 * x[1] + 7 * x[2] + x[3])
assert ok
print('equal rows: an arbitrary mixture is a Darboux polynomial:', ok)

res = json.loads((HERE.parent / 'verification' / 'lv_tree_exact_checks.json').read_text())
assert res['status'] == 'all_checks_pass'
assert res['triad_reconstruction_trees'] == 986 and res['support_enumeration_trees'] == 200
counts = {r['n']: r['unlabelled_trees'] for r in res['rows']}
assert counts[4] == 2 and counts[7] == 11
print('verifier results: 986 trees (orders 2-12) and 200 trees (orders 2-10) pass')
(HERE / 'data.json').write_text(json.dumps(out, indent=2) + '\n')
print('all video numbers check out')
