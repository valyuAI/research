"""Independent second implementation of the nonsingular-graph enumeration (cross-check of nsbfs.py).

Differences from nsbfs.py: determinant and inverse by fraction-free Bareiss elimination and Gauss-Jordan
over Python Fractions (no FLINT); inertia by symmetric LDL^T over the rationals with Sylvester's law of
inertia (no characteristic polynomial); isomorphism rejection by invariant buckets + networkx VF2 (no
nauty). Same mathematical generation scheme (single extensions from order N-1, isotropic double
extensions from order N-2). Prints per-order counts by n^- and the maximum n^+.

Usage: python enumerate_check.py k
"""
import sys, time
from fractions import Fraction
import numpy as np
import networkx as nx


def bareiss_det(A):
  n = len(A)
  if n == 0:
    return 1
  M = [list(map(int, r)) for r in A]
  sign = 1
  prev = 1
  for k in range(n - 1):
    if M[k][k] == 0:
      sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
      if sw is None:
        return 0
      M[k], M[sw] = M[sw], M[k]
      sign = -sign
    for i in range(k + 1, n):
      for j in range(k + 1, n):
        M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
    prev = M[k][k]
  return sign * M[n - 1][n - 1]


def inverse(A):
  n = len(A)
  M = [[Fraction(int(x)) for x in r] + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(A)]
  for c in range(n):
    p = next(i for i in range(c, n) if M[i][c] != 0)
    M[c], M[p] = M[p], M[c]
    piv = M[c][c]
    M[c] = [x / piv for x in M[c]]
    for i in range(n):
      if i != c and M[i][c] != 0:
        f = M[i][c]
        M[i] = [a - f * b for a, b in zip(M[i], M[c])]
  return [r[n:] for r in M]


def ldl_inertia(A):
  """Inertia of a symmetric rational matrix by congruence (Sylvester), with 2x2 handling of zero pivots."""
  M = [[Fraction(int(x)) for x in r] for r in A]
  n = len(M)
  pos = neg = 0
  idx = list(range(n))
  while idx:
    piv = next((i for i in idx if M[i][i] != 0), None)
    if piv is not None:
      d = M[piv][piv]
      pos += d > 0; neg += d < 0
      rest = [i for i in idx if i != piv]
      for i in rest:
        if M[i][piv] != 0:
          f = M[i][piv] / d
          for j in rest:
            M[i][j] -= f * M[piv][j]
      idx = rest
      continue
    pair = next(((i, j) for i in idx for j in idx if i < j and M[i][j] != 0), None)
    if pair is None:
      break  # remaining block is zero
    i, j = pair
    # replace row/col i by i + j: congruence that creates nonzero diagonal 2*M[i][j]
    for t in range(n):
      M[i][t] += M[j][t]
    for t in range(n):
      M[t][i] += M[t][j]
  return pos, neg


def invariant(G):
  A = G.astype(np.float64)
  ev = np.round(np.linalg.eigvalsh(A), 6) + 0.0
  deg = tuple(sorted(G.sum(axis=1).tolist()))
  return (G.shape[0], deg, tuple(ev.tolist()))


class Store:
  def __init__(self):
    self.buckets = {}
    self.items = []

  def add(self, G, p, q):
    key = invariant(G)
    bucket = self.buckets.setdefault(key, [])
    g = nx.from_numpy_array(G)
    for j in bucket:
      if nx.is_isomorphic(g, self.items[j][3]):
        return False
    bucket.append(len(self.items))
    self.items.append((G, p, q, g))
    return True


def main():
  k = int(sys.argv[1])
  levels = {0: [(np.zeros((0, 0), dtype=np.int8), 0, 0)]}
  vec = {}
  best = {}
  N = 0
  empty = 0
  t_start = time.time()
  while True:
    N += 1
    t0 = time.time()
    st = Store()
    for A, p, q in levels.get(N - 1, []):
      h = A.shape[0]
      if h == 0:
        continue
      if h not in vec:
        s = np.arange(1 << h, dtype=np.int64)
        vec[h] = ((s[:, None] >> np.arange(h)[None, :]) & 1).astype(np.int64)
      V = vec[h]
      d = bareiss_det(A.tolist())
      inv = inverse(A.tolist())
      adj = np.array([[int(x * d) for x in r] for r in inv], dtype=np.int64)
      sgn = 1 if d > 0 else -1
      Q = sgn * np.sign(np.einsum('ni,ij,nj->n', V, adj, V))
      ok = (Q != 0) & ((q + (Q > 0)) <= k)
      for i in np.nonzero(ok)[0]:
        b = V[i].astype(np.int8)
        G = np.zeros((h + 1, h + 1), dtype=np.int8)
        G[:h, :h] = A; G[:h, h] = b; G[h, :h] = b
        st.add(G, p + int(Q[i] < 0), q + int(Q[i] > 0))
    for A, p, q in levels.get(N - 2, []):
      if q > k - 1:
        continue
      h = A.shape[0]
      if h == 0:
        st.add(np.array([[0, 1], [1, 0]], dtype=np.int8), 1, 1)
        continue
      V = vec[h]
      d = bareiss_det(A.tolist())
      inv = inverse(A.tolist())
      adj = np.array([[int(x * d) for x in r] for r in inv], dtype=np.int64)
      Qv = np.einsum('ni,ij,nj->n', V, adj, V)
      Z = V[Qv == 0]
      if len(Z) == 0:
        continue
      Bil = Z @ adj @ Z.T
      for a in (0, 1):
        nz = (a * d - Bil) != 0
        for u, w in zip(*np.nonzero(np.triu(nz, 0))):
          G = np.zeros((h + 2, h + 2), dtype=np.int8)
          G[:h, :h] = A
          G[:h, h] = Z[u]; G[h, :h] = Z[u]
          G[:h, h + 1] = Z[w]; G[h + 1, :h] = Z[w]
          G[h, h + 1] = G[h + 1, h] = a
          st.add(G, p + 1, q + 1)
    lvl = []
    for G, p, q, g in st.items:
      pe, qe = ldl_inertia(G.tolist())
      assert (pe, qe) == (p, q) and pe + qe == G.shape[0], 'inertia mismatch'
      lvl.append((G, p, q))
    levels[N] = lvl
    levels.pop(N - 3, None)
    stat = {}
    for G, p, q in lvl:
      stat[q] = stat.get(q, 0) + 1
      if q not in best or p > best[q]:
        best[q] = p
    print(f'[check] k={k} order={N}: nonsingular={len(lvl)} by n^-: {dict(sorted(stat.items()))} '
          f'({time.time()-t0:.0f}s, total {time.time()-t_start:.0f}s)', flush=True)
    empty = empty + 1 if not lvl else 0
    if empty >= 2:
      break
  print('[check] FINAL max n^+ by n^-:', dict(sorted(best.items())), flush=True)


if __name__ == '__main__':
  main()
