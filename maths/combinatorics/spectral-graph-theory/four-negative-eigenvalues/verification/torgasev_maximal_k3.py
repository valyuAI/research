"""Cross-check against Torgasev (1989): count the maximal connected reduced graphs with exactly three
negative eigenvalues (maximal under induced subgraphs), from the complete point-determining census
written by `python point_determining_bfs.py 3`. Torgasev proved there are exactly 32, of orders 9..14.
"""
import glob, os
from collections import Counter
import numpy as np
import networkx as nx
from point_determining_bfs import g6_decode, cert

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'pdk3')


def reduce(A):
  keep = [i for i in range(A.shape[0]) if A[i].sum() > 0]
  A = A[np.ix_(keep, keep)]
  seen, idx = set(), []
  for i in range(A.shape[0]):
    r = A[i].tobytes()
    if r not in seen:
      seen.add(r); idx.append(i)
  B = A[np.ix_(idx, idx)]
  return B if B.shape[0] == A.shape[0] else reduce(B)


def main():
  graphs = {}
  for f in glob.glob(os.path.join(OUT, 'level*.g6')):
    for line in open(f, 'rb'):
      g6, p, z, q, red = line.split()
      if int(red) == 1 and int(q) == 3:
        A = g6_decode(g6)
        graphs[cert(A)] = A
  children = {}
  for c, A in graphs.items():
    s = set()
    for v in range(A.shape[0]):
      R = reduce(np.delete(np.delete(A, v, 0), v, 1))
      if R.shape[0]:
        s.add(cert(R))
    children[c] = s
  memo = {}
  def below(c):
    if c not in memo:
      out = set()
      for d in children[c]:
        if d in graphs:
          out.add(d); out |= below(d)
      memo[c] = out
    return memo[c]
  contained = set()
  for c in graphs:
    contained |= below(c)
  conn = [c for c, A in graphs.items() if nx.is_connected(nx.from_numpy_array(A))]
  maximal = [c for c in conn if c not in contained]
  orders = sorted(Counter(graphs[c].shape[0] for c in maximal).items())
  print(f'reduced graphs with n^-=3: {len(graphs)}; connected: {len(conn)}; maximal connected: {len(maximal)}; orders: {orders}')
  assert len(maximal) == 32 and [o for o, _ in orders] == list(range(9, 15))


if __name__ == '__main__':
  main()
