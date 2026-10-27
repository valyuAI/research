"""Complete enumeration of nonsingular graphs with at most k negative adjacency eigenvalues.

Why this suffices for n^+(k): if G is reduced with n^-(G)=k and n^+(G)=p, a principal submatrix of
full rank p+k is nonsingular with the same inertia (interlacing), so
  n^+(k) = max{ p : some nonsingular graph has inertia (p, 0, k) }.

Completeness (Jacobi): a nonsingular graph G of order N >= 2 has a vertex v with G-v nonsingular,
unless G^{-1} has zero diagonal; then some pair {u,w} has (G^{-1})_{uw} != 0 and G-u-w is nonsingular,
and the Schur complement S of G-u-w in G is [[0,s],[s,0]] (s != 0), so both added vertices are
isotropic (b^T M b = 0 with M = A(H)^{-1}), the new edge value satisfies a - b_u^T M b_w != 0, and
n^-(G) = n^-(H) + 1. Interlacing gives n^-(H) <= n^-(G). So level N is generated from level N-1
(single extensions) and level N-2 (isotropic double extensions), and every step is exact integer
arithmetic: with adj = det(A) A^{-1}, sign(b^T M b) = sign(det A) * sign(b^T adj b).

Usage: python enumerate_nonsingular.py k [maxorder]   (writes output/ns_k{k}/order{N}.txt)
"""
import sys, time, os
import numpy as np
import pynauty
from flint import fmpz_mat

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')


def cert(A):
  n = A.shape[0]
  adj = {i: [int(j) for j in np.nonzero(A[i])[0] if j > i] for i in range(n)}
  return pynauty.certificate(pynauty.Graph(n, adjacency_dict=adj)) + bytes([n]) if n > 0 else b'empty'


def adjugate(A):
  """Exact (det, adj) with adj = det * A^{-1}, as python int and numpy object->int64 array."""
  n = A.shape[0]
  M = fmpz_mat(n, n, [int(x) for x in A.flatten()])
  d = int(M.det())
  inv = M.inv()  # fmpq_mat
  adj = np.zeros((n, n), dtype=object)
  for i in range(n):
    for j in range(n):
      q = inv[i, j] * d
      assert q.q == 1
      adj[i, j] = int(q.p)
  return d, adj


def exact_inertia(A):
  n = A.shape[0]
  if n == 0:
    return 0, 0, 0
  M = fmpz_mat(n, n, [int(x) for x in A.flatten()])
  p = M.charpoly()
  c = [int(p[i]) for i in range(n + 1)]
  z = 0
  while c[z] == 0:
    z += 1
  nz = c[z:]
  def sc(seq):
    s = [x for x in seq if x != 0]
    return sum(1 for a, b in zip(s, s[1:]) if (a > 0) != (b > 0))
  return sc(nz), z, sc([x * (-1) ** i for i, x in enumerate(nz)])


def all_vectors(h):
  s = np.arange(1 << h, dtype=np.int64)
  return ((s[:, None] >> np.arange(h)[None, :]) & 1).astype(np.int64)


def quad_forms(adj, V):
  """b^T adj b for all rows b of V, exactly (int64 with overflow guard, else object)."""
  h = adj.shape[0]
  mx = max(abs(int(x)) for x in adj.flatten()) if h else 0
  if mx * h * h < 2 ** 62:
    a = adj.astype(np.int64)
    return np.einsum('ni,ij,nj->n', V, a, V), (V @ a)
  raise OverflowError('adjugate too large for int64 path')


def main():
  k = int(sys.argv[1]); maxorder = int(sys.argv[2]) if len(sys.argv) > 2 else 40
  levels = {0: {b'empty': (np.zeros((0, 0), dtype=np.int8), 0, 0)}}
  vec_cache = {}
  best = {}
  t_start = time.time()
  N = 0
  empty_run = 0
  while N < maxorder:
    N += 1
    t0 = time.time()
    new = {}
    # single extensions from level N-1
    for c, (A, p, q) in levels.get(N - 1, {}).items():
      h = A.shape[0]
      if h == 0:
        continue  # K1 is singular
      if h not in vec_cache:
        vec_cache[h] = all_vectors(h)
      V = vec_cache[h]
      d, adj = adjugate(A)
      sgn = 1 if d > 0 else -1
      Q, _ = quad_forms(adj, V)
      s = sgn * np.sign(Q)  # sign of b^T M b
      ok = (s != 0) & ((q + (s > 0)) <= k)
      for i in np.nonzero(ok)[0]:
        b = V[i].astype(np.int8)
        G = np.zeros((h + 1, h + 1), dtype=np.int8)
        G[:h, :h] = A; G[:h, h] = b; G[h, :h] = b
        cg = cert(G)
        if cg not in new:
          new[cg] = (G, p + int(s[i] < 0), q + int(s[i] > 0))
    # isotropic double extensions from level N-2 (only possible if q <= k-1)
    for c, (A, p, q) in levels.get(N - 2, {}).items():
      if q > k - 1:
        continue
      h = A.shape[0]
      if h == 0:
        G = np.array([[0, 1], [1, 0]], dtype=np.int8)
        cg = cert(G)
        if cg not in new:
          new[cg] = (G, 1, 1)
        continue
      if h not in vec_cache:
        vec_cache[h] = all_vectors(h)
      V = vec_cache[h]
      d, adj = adjugate(A)
      Q, VA = quad_forms(adj, V)
      iso = np.nonzero(Q == 0)[0]
      if len(iso) == 0:
        continue
      Z = V[iso]                      # isotropic vectors
      Bil = Z @ adj.astype(np.int64) @ Z.T   # d * b_u^T M b_w
      for a in (0, 1):
        # need a*d - Bil != 0 (i.e. a - b_u^T M b_w != 0)
        nzm = (a * d - Bil) != 0
        ii, jj = np.nonzero(np.triu(nzm, 0))  # same type vector allowed (then a=1)
        for u, w in zip(ii, jj):
          G = np.zeros((h + 2, h + 2), dtype=np.int8)
          G[:h, :h] = A
          G[:h, h] = Z[u]; G[h, :h] = Z[u]
          G[:h, h + 1] = Z[w]; G[h + 1, :h] = Z[w]
          G[h, h + 1] = G[h + 1, h] = a
          cg = cert(G)
          if cg not in new:
            new[cg] = (G, p + 1, q + 1)
    # exact verification of every new graph
    lvl = {}
    for cg, (G, p, q) in new.items():
      pe, ze, qe = exact_inertia(G)
      assert ze == 0 and pe == p and qe == q, ('inertia mismatch', pe, ze, qe, p, q)
      lvl[cg] = (G, p, q)
    levels[N] = lvl
    if N - 3 in levels:
      del levels[N - 3]
    stat = {}
    for G, p, q in lvl.values():
      stat[q] = stat.get(q, 0) + 1
    for G, p, q in lvl.values():
      if q not in best or p > best[q][0]:
        best[q] = (p, N)
    print(f'k={k} order={N}: nonsingular graphs={len(lvl)} by n^-: {dict(sorted(stat.items()))} ({time.time()-t0:.1f}s, total {time.time()-t_start:.0f}s)', flush=True)
    os.makedirs(os.path.join(OUT, f'ns_k{k}'), exist_ok=True)
    with open(os.path.join(OUT, f'ns_k{k}', f'order{N}.txt'), 'w') as f:
      for G, p, q in lvl.values():
        f.write(''.join(map(str, G[np.triu_indices(N, 1)])) + f' {p} {q}\n')
    if not lvl:
      empty_run += 1
      if empty_run >= 2:
        break
    else:
      empty_run = 0
  print('FINAL: max n^+ for each n^- among nonsingular graphs (p, order):', dict(sorted(best.items())), flush=True)


if __name__ == '__main__':
  main()
