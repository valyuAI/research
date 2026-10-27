"""Exact data (Q(sqrt5), theta = sqrt5) for the regular dodecahedron and the truncated icosahedron with unit
edges, for the prestress check of check_prestress.py. Faces from a floating-point hull; everything is validated
exactly by nfsolid.validate."""
import json, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import ConvexHull

# elements a + b sqrt5 as (a, b)
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def mul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def f(x): return x[0] + x[1] * 5 ** 0.5
PHI = (Fr(1, 2), Fr(1, 2)); IPHI = (Fr(-1, 2), Fr(1, 2)); ONE = (Fr(1), Fr(0)); ZERO = (Fr(0), Fr(0))
def neg(x): return (-x[0], -x[1])

def faces_of(V):
  X = np.array([[f(c) for c in v] for v in V])
  h = ConvexHull(X)
  groups = []
  for simp, eq in zip(h.simplices, h.equations):
    for g in groups:
      if np.allclose(g[0], eq, atol=1e-9):
        g[1].update(simp.tolist()); break
    else:
      groups.append((eq, set(simp.tolist())))
  F = []
  for eq, S in groups:
    S = list(S); c = X[S].mean(0); n = eq[:3]
    u = X[S[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
    F.append([int(S[k]) for k in np.argsort([np.arctan2((X[i] - c) @ w, (X[i] - c) @ u) for i in S])])
  return F

def dump(name, V, path):
  s = mul(PHI, (Fr(1, 2), Fr(0)))  # scale phi/2 gives unit edges for the dodecahedron coordinates below
  json.dump({'name': name, 'minpoly': [-5, 0, 1], 'interval': ['2', '3'],
             'vertices': [[[str(c[0]), str(c[1])] for c in v] for v in V], 'faces': faces_of(V)}, open(path, 'w'))

# dodecahedron: (+-1,+-1,+-1), (0, +-1/phi, +-phi) and cyclic; edge 2/phi; scale by phi/2
s = mul(PHI, (Fr(1, 2), Fr(0)))
D = []
for a, b, c in itertools.product((1, -1), repeat=3):
  D.append([(Fr(a), Fr(0)), (Fr(b), Fr(0)), (Fr(c), Fr(0))])
for a, b in itertools.product((1, -1), repeat=2):
  y, z = (Fr(a) * IPHI[0], Fr(a) * IPHI[1]), (Fr(b) * PHI[0], Fr(b) * PHI[1])
  for perm in ((ZERO, y, z), (y, z, ZERO), (z, ZERO, y)):
    D.append(list(perm))
D = [[mul(s, c) for c in v] for v in D]
dump('Regular Dodecahedron', D, 'data_extra/dodecahedron.json')

# truncated icosahedron: cyclic permutations of (0, +-1, +-3phi), (+-1, +-(2+phi), +-2phi), (+-phi, +-2, +-phi^3); edge 2
T = []
def cyc(v):
  return [v, [v[1], v[2], v[0]], [v[2], v[0], v[1]]]
phi3 = mul(PHI, mul(PHI, PHI))
gens = [(ZERO, ONE, mul((Fr(3), Fr(0)), PHI)), (ONE, add((Fr(2), Fr(0)), PHI), mul((Fr(2), Fr(0)), PHI)),
        (PHI, (Fr(2), Fr(0)), phi3)]
seen = set()
for g in gens:
  for signs in itertools.product((1, -1), repeat=3):
    v = [(sg * c[0], sg * c[1]) for sg, c in zip(signs, g)]
    for w in cyc(v):
      key = tuple(w)
      if key not in seen:
        seen.add(key); T.append(w)
half = (Fr(1, 2), Fr(0))
T = [[mul(half, c) for c in v] for v in T]
print(len(D), len(T))
json.dump({'name': 'Truncated Icosahedron', 'minpoly': [-5, 0, 1], 'interval': ['2', '3'],
           'vertices': [[[str(c[0]), str(c[1])] for c in v] for v in T], 'faces': faces_of(T)},
          open('data_extra/truncated_icosahedron.json', 'w'))
