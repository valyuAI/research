"""External cross-check against Akbari, Cameron and Khosrovshahi, "Ranks and signatures of adjacency
matrices" (preprint, 2004), Table 2: numbers of reduced graphs without isolated vertices by rank r,
number t of negative eigenvalues and order n, for r <= 7.

We regenerate those numbers from our own data: every reduced graph of rank r with t negative eigenvalues
arises from a nonsingular basis X of order r with t negative eigenvalues (from enumerate_nonsingular.py
output, k = 4 run) and a clique of pairwise compatible isotropic 0/1 vectors (Section 6 of the paper).
All cliques are enumerated, graphs are built, and isomorphism classes are counted by order.

Usage: python ack_check.py   (needs output/ns_k4 from `enumerate_nonsingular.py 4`)
"""
import os, sys
import numpy as np
import networkx as nx
from max_reduced_order import load
from enumerate_nonsingular import adjugate, all_vectors, cert, OUT

ACK = {  # (r, t): {n: count}  transcribed from ACK Table 2
  (4, 2): {4: 3, 5: 3, 6: 2}, (4, 3): {4: 1},
  (5, 2): {5: 1}, (5, 3): {5: 7, 6: 7, 7: 7, 8: 2}, (5, 4): {5: 1},
  (6, 3): {6: 39, 7: 142, 8: 315, 9: 428, 10: 371, 11: 204, 12: 70, 13: 15, 14: 3},
  (6, 4): {6: 17, 7: 19, 8: 19, 9: 9, 10: 2},
  (7, 3): {7: 25, 8: 50, 9: 61, 10: 30, 11: 11, 12: 2},
  (7, 4): {7: 295, 8: 1304, 9: 3368, 10: 5346, 11: 5634, 12: 4027, 13: 2037, 14: 778, 15: 238,
           16: 65, 17: 13, 18: 3},
}


def all_reduced_from_basis(A):
  h = A.shape[0]
  d, adj = adjugate(A)
  adj = adj.astype(np.int64)
  V = all_vectors(h)
  Q = np.einsum('ni,ij,nj->n', V, adj, V)
  w = (1 << np.arange(h)).astype(np.int64)
  colmasks = [int(x) for x in (A.astype(np.int64) * w[None, :]).sum(axis=1)]
  cols = set(colmasks)
  ids = [int(i) for i in np.nonzero(Q == 0)[0] if i != 0 and int(i) not in cols]
  Z = V[ids]
  B = Z @ adj @ Z.T
  ok = (B == 0) | (B == d)
  np.fill_diagonal(ok, False)
  C = nx.Graph()
  C.add_nodes_from(range(len(ids)))
  ii, jj = np.nonzero(np.triu(ok, 1))
  C.add_edges_from(zip(ii.tolist(), jj.tolist()))
  base = [V[m] for m in colmasks]
  out = [A]
  for cl in nx.enumerate_all_cliques(C):
    T = np.array(base + [Z[c] for c in cl], dtype=np.int64)
    G = T @ adj @ T.T
    assert np.all((G == 0) | (G == d))
    out.append((G // d).astype(np.int8))
  return out


def main():
  ok_all = True
  for (r, t), ref in sorted(ACK.items()):
    bases = [A for (A, p, q) in load(os.path.join(OUT, 'ns_k4', f'order{r}.txt'), r) if q == t]
    classes = {}
    for A in bases:
      for G in all_reduced_from_basis(A):
        c = cert(G)
        if c not in classes:
          classes[c] = G.shape[0]
    got = {}
    for n in classes.values():
      got[n] = got.get(n, 0) + 1
    got = dict(sorted(got.items()))
    status = 'OK' if got == ref else 'MISMATCH'
    ok_all &= got == ref
    print(f'r={r} t={t}: ours {got}  ACK {ref}  {status}', flush=True)
  print('ALL MATCH' if ok_all else 'SOME MISMATCH')
  sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
  main()
