"""Classify the reduced graphs of maximum order with n^- = k obtained from bases of a given rank.

For every nonsingular basis X of the given rank with n^-(X) = k, enumerate ALL maximal cliques of the
compatibility graph C_X (see maxorder.py), build the reduced graph for each clique of the target
size, and collect isomorphism classes (pynauty certificates). Also re-verifies inertia exactly.

Usage: python classify_max_order.py k rank target_order
"""
import sys
import numpy as np
import networkx as nx
import os
from max_reduced_order import load
from enumerate_nonsingular import adjugate, all_vectors, cert, exact_inertia, OUT


def graphs_for_basis(A, target):
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
  out = []
  for cl in nx.find_cliques(C):
    if h + len(cl) != target:
      continue
    T = [V[m] for m in colmasks] + [Z[c] for c in cl]
    T = np.array(T, dtype=np.int64)
    G = T @ adj @ T.T
    assert np.all((G == 0) | (G == d))
    G = (G // d).astype(np.int8)
    out.append(G)
  return out


def main():
  k, rank, target = map(int, sys.argv[1:4])
  bases = [(A, p, q) for (A, p, q) in load(os.path.join(OUT, f'ns_k{k}', f'order{rank}.txt'), rank) if q == k]
  classes = {}
  for A, p, q in bases:
    for G in graphs_for_basis(A, target):
      c = cert(G)
      if c not in classes:
        classes[c] = G
  print(f'k={k} rank={rank}: {len(classes)} isomorphism classes of reduced graphs of order {target}')
  for c, G in classes.items():
    g = nx.from_numpy_array(G)
    inert = exact_inertia(G)
    rows = set(map(tuple, G.tolist()))
    print('  inertia', inert, 'reduced', len(rows) == G.shape[0] and G.sum(1).min() > 0,
          'connected', nx.is_connected(g), 'edges', g.number_of_edges(),
          'degrees', sorted(set(G.sum(1).tolist())), nx.to_graph6_bytes(g, header=False).strip().decode())


if __name__ == '__main__':
  main()
