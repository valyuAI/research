"""Second, independent implementation of the maximum-order computation (Section 6 of the paper).

Differences from max_reduced_order.py: reads the bases from the census certificate (not from the
enumerator's output), inverts A(X) over Python Fractions by Gauss-Jordan (no FLINT; numpy only for integer arithmetic on
the scaled inverse), and computes the
clique number of the compatibility graph with a self-contained bitset Bron-Kerbosch search with pivoting
(no networkx). Prints the largest reduced order for each rank.

Usage: python max_reduced_order_check.py [k]   (default k = 4)
"""
import gzip, os, sys, time
from fractions import Fraction
from check_census import g6_decode

HERE = os.path.dirname(os.path.abspath(__file__))


def inverse(A):
  n = len(A)
  M = [[Fraction(x) for x in r] + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(A)]
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


def max_clique(adj):
  """adj: list of int bitmasks. Returns the clique number (Bron-Kerbosch with pivoting)."""
  best = 0
  def bk(R, P, X):
    nonlocal best
    if P == 0:
      if X == 0:
        best = max(best, R)
      return
    if R + bin(P).count('1') <= best:
      return
    u = max(((P | X) >> i & 1, bin(P & adj[i]).count('1'), i) for i in range(len(adj)) if (P | X) >> i & 1)[2]
    cand = P & ~adj[u]
    while cand:
      v = (cand & -cand).bit_length() - 1
      bk(R + 1, P & adj[v], X & adj[v])
      P &= ~(1 << v)
      X |= 1 << v
      cand &= ~(1 << v)
  bk(0, (1 << len(adj)) - 1, 0)
  return best


def order_for_basis(A):
  import numpy as np
  h = len(A)
  M = inverse(A)
  d = 1
  for r in M:
    for x in r:
      d = d * x.denominator // __import__('math').gcd(d, x.denominator)
  scaled = [[int(x * d) for x in r] for r in M]
  if max(abs(x) for r in scaled for x in r) * h * h >= 2 ** 62:
    raise OverflowError('scaled inverse exceeds the audited int64 range')
  adj = np.array(scaled, dtype=np.int64)  # adj = d * A^{-1}, exact
  s = np.arange(1, 1 << h, dtype=np.int64)
  V = ((s[:, None] >> np.arange(h)[None, :]) & 1).astype(np.int64)
  Q = np.einsum('ni,ij,nj->n', V, adj, V)
  colset = set(tuple(r) for r in A)
  keep = [i for i in np.nonzero(Q == 0)[0] if tuple(V[i].tolist()) not in colset]
  m = len(keep)
  if m == 0:
    return h
  Z = V[keep]
  B = Z @ adj @ Z.T
  ok = (B == 0) | (B == d)
  adjm = [0] * m
  for x in range(m):
    row = ok[x]
    mask = 0
    for y in np.nonzero(row)[0]:
      if y != x:
        mask |= 1 << int(y)
    adjm[x] = mask
  return h + max_clique(adjm)


def main():
  k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
  best = {}
  t0 = time.time()
  done = 0
  last_progress = time.monotonic()
  for line in gzip.open(os.path.join(HERE, 'census_nonsingular_nneg_le4.txt.gz'), 'rt'):
    g6, N, p, q = line.split()
    if int(q) != k:
      continue
    N = int(N)
    o = order_for_basis(g6_decode(g6))
    best[N] = max(best.get(N, 0), o)
    done += 1
    if done % 2000 == 0 or time.monotonic() - last_progress >= 15:
      print(f'  {done} bases done ({time.time()-t0:.0f}s) current {dict(sorted(best.items()))}', flush=True)
      last_progress = time.monotonic()
  print(f'k={k}: largest reduced order by rank: {dict(sorted(best.items()))}; overall {max(best.values())}', flush=True)


if __name__ == '__main__':
  main()
