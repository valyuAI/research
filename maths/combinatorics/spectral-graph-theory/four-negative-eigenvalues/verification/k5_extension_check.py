"""k = 5 evidence: the known 21-vertex graphs with inertia (16,0,5) admit no 22nd vertex keeping n^- = 5.

Builds W6 (K6 plus the Kneser graph K(6,2), each point joined to the pairs containing it), the three CFJK
variants with the K6 replaced by K5+K1, K4+K2, K3+K3, and all graphs 'Clebsch + K5' in which each clique
vertex is joined to an 8-set of the Clebsch graph inducing 4K2 (CFJK's G6 construction). Keeps those with
exact inertia (16,0,5), merges isomorphic ones, and for each computes, over all 2^21 neighbourhood
vectors b, the sign of b^T adj(A) b (exact integers). A positive eigenvalue is gained iff
det(A) * b^T adj(A) b < 0. By Lemma 3.2 and A_4 = 11, every nonsingular (17,0,5) graph arises this way
from some nonsingular (16,0,5) graph; this script checks only the known ones.

Usage: python k5_extension_check.py
"""
import itertools, json
import numpy as np
from enumerate_nonsingular import adjugate, exact_inertia, cert


def from_edges(n, E):
  A = np.zeros((n, n), dtype=np.int8)
  for u, v in E:
    A[u, v] = A[v, u] = 1
  return A


def w_graph(k, parts):
  pairs = list(itertools.combinations(range(k), 2))
  E, off = [], 0
  for p in parts:
    E += [(off + i, off + j) for i, j in itertools.combinations(range(p), 2)]
    off += p
  idx = {P: k + i for i, P in enumerate(pairs)}
  E += [(idx[P], idx[Q]) for P, Q in itertools.combinations(pairs, 2) if not set(P) & set(Q)]
  E += [(i, idx[P]) for P in pairs for i in P]
  return from_edges(k + len(pairs), E)


def clebsch_k5():
  C = from_edges(16, [(u, u ^ g) for u in range(16) for g in (1, 2, 4, 8, 15) if u < u ^ g])
  sets = [S for S in itertools.combinations(range(16), 8) if (C[np.ix_(S, S)].sum(1) == 1).all()]
  for ch in itertools.combinations(sets, 5):
    A = np.zeros((21, 21), dtype=np.int8)
    A[:16, :16] = C
    for i, S in enumerate(ch):
      for v in S:
        A[16 + i, v] = A[v, 16 + i] = 1
      for j in range(i):
        A[16 + i, 16 + j] = A[16 + j, 16 + i] = 1
    yield A


def positive_extensions(A):
  h = A.shape[0]
  d, adj = adjugate(A)
  a = adj.astype(np.int64)
  assert int(np.abs(a).max()) * h * h < 2 ** 62
  sd = 1 if d > 0 else -1
  count = 0
  for start in range(0, 1 << h, 1 << 16):
    s = np.arange(start, start + (1 << 16), dtype=np.int64)
    V = (s[:, None] >> np.arange(h)[None, :]) & 1
    q = np.einsum('ni,ni->n', V @ a, V)
    count += int((sd * q < 0).sum())
  return count


def main():
  cands = [('W6', w_graph(6, [6]))] + [(f'W6 with K{a}+K{b}', w_graph(6, [a, b])) for a, b in ((5, 1), (4, 2), (3, 3))]
  cands += [('Clebsch+K5', A) for A in clebsch_k5()]
  seen, rows = set(), []
  for name, A in cands:
    if exact_inertia(A) != (16, 0, 5):
      continue
    c = cert(A)
    if c in seen:
      continue
    seen.add(c)
    rows.append({'graph': name, 'edges': int(A.sum()) // 2, 'inertia': [16, 0, 5],
                 'positive_22nd_vertex_extensions': positive_extensions(A)})
    print(json.dumps(rows[-1]), flush=True)
  print(json.dumps({'classes': len(rows), 'any_extension': any(r['positive_22nd_vertex_extensions'] for r in rows)}))


if __name__ == '__main__':
  main()
