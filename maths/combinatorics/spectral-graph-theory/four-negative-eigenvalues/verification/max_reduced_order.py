"""Maximum order of reduced graphs with n^- = k, from the complete list of nonsingular graphs X with
inertia (p, 0, k) (output of nsbfs.py).

Every reduced graph G with n^-(G)=k and rank r has a nonsingular induced subgraph X on r vertices with
the same inertia (a basis). With M = A(X)^{-1}, every vertex u of G is determined by b_u = A[X,u] in
{0,1}^X, A(G)_{uw} = b_u^T M b_w, b_u^T M b_u = 0, distinct vertices have distinct b_u, and b_u != 0
(no isolated vertices). Conversely any set T of nonzero isotropic 0/1 vectors containing the columns of
A(X), with all pairwise values b^T M b' in {0,1}, defines a reduced graph with basis X and the same
inertia as X. So the largest reduced graph with basis X has |X| + omega(C_X) vertices, where C_X is the
compatibility graph on the non-column nonzero isotropic vectors (the columns are compatible with all).

Usage: python max_reduced_order.py k  (reads output/ns_k{k}/order*.txt)
"""
import sys, glob, time, re, os
import numpy as np
import networkx as nx
from enumerate_nonsingular import adjugate, all_vectors, quad_forms, OUT


def load(path, N):
  out = []
  iu = np.triu_indices(N, 1)
  for line in open(path):
    bits, p, q = line.split()
    A = np.zeros((N, N), dtype=np.int8)
    A[iu] = np.frombuffer(bits.encode(), dtype=np.uint8) - 48
    A = A + A.T
    out.append((A, int(p), int(q)))
  return out


def best_for_basis(A):
  h = A.shape[0]
  d, adj = adjugate(A)
  V = all_vectors(h)
  Q, _ = quad_forms(adj, V)
  adj = adj.astype(np.int64)
  iso = np.nonzero(Q == 0)[0]
  w = (1 << np.arange(h)).astype(np.int64)
  cols = set(int(x) for x in (A.astype(np.int64) * w[None, :]).sum(axis=1))
  ids = [i for i in iso if i != 0 and int(i) not in cols]
  if not ids:
    return h, []
  Z = V[ids]
  B = Z @ adj @ Z.T  # d * b^T M b'
  ok = (B == 0) | (B == d)
  np.fill_diagonal(ok, False)
  G = nx.Graph()
  G.add_nodes_from(range(len(ids)))
  ii, jj = np.nonzero(np.triu(ok, 1))
  G.add_edges_from(zip(ii.tolist(), jj.tolist()))
  clique, size = nx.max_weight_clique(G, weight=None)
  return h + size, [ids[c] for c in clique]


def main():
  k = int(sys.argv[1])
  files = sorted(glob.glob(os.path.join(OUT, f'ns_k{k}', 'order*.txt')), key=lambda s: int(re.findall(r'order(\d+)', s)[0]))
  overall = (0, None)
  for f in files:
    N = int(re.findall(r'order(\d+)', f)[0])
    t0 = time.time()
    data = [(A, p, q) for (A, p, q) in load(f, N) if q == k]
    if not data:
      continue
    best = (0, None)
    hist = {}
    last_progress = time.monotonic()
    for done, (A, p, q) in enumerate(data, 1):
      if time.monotonic() - last_progress >= 15:
        print(f'  rank={N}: {done}/{len(data)} bases', flush=True)
        last_progress = time.monotonic()
      size, extra = best_for_basis(A)
      hist[size] = hist.get(size, 0) + 1
      if size > best[0]:
        best = (size, (A, extra))
    if best[0] > overall[0]:
      overall = (best[0], (N, best[1]))
    print(f'k={k} rank={N} (n^+={N-k}): bases={len(data)} max reduced order={best[0]} hist={dict(sorted(hist.items()))} ({time.time()-t0:.1f}s)', flush=True)
  print('OVERALL max order of reduced graph with n^-=%d: %d (rank %s)' % (k, overall[0], overall[1][0] if overall[1] else None), flush=True)


if __name__ == '__main__':
  main()
