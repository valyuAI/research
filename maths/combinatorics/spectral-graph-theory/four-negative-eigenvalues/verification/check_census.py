"""Soundness and distinctness check of the census certificate, independent of nauty and FLINT.

For every graph in census_nonsingular_nneg_le4.txt.gz this script
  1. recomputes the inertia exactly by symmetric LDL^T congruence over the rationals (Sylvester's law),
     and checks that the graph is nonsingular with the recorded (n^+, n^-) and n^- <= 4;
  2. checks that the graphs of each order are pairwise non-isomorphic (invariant buckets + networkx VF2);
  3. checks the recorded counts, and that the two graphs of order 15 are W5 and the AG(2,3) graph X
     built by verify_extremal.py.
Together with an independent complete enumeration that produces the same counts (enumerate_check.py),
1-2 imply that the census is exactly the set of nonsingular graphs with at most four negative eigenvalues.

Usage: python check_census.py [census.txt.gz]
"""
import gzip, json, os, sys, time, hashlib
from collections import defaultdict
import networkx as nx
from verify_extremal import ldl_inertia, w5, affine_x

HERE = os.path.dirname(os.path.abspath(__file__))


def g6_decode(s):
  n = ord(s[0]) - 63
  bits = []
  for ch in s[1:]:
    v = ord(ch) - 63
    bits.extend((v >> t) & 1 for t in range(5, -1, -1))
  A = [[0] * n for _ in range(n)]
  k = 0
  for j in range(1, n):
    for i in range(j):
      A[i][j] = A[j][i] = bits[k]
      k += 1
  return A


def invariant(A):
  n = len(A)
  deg = sorted(sum(r) for r in A)
  # number of triangles and sorted (degree, neighbour-degree multiset) pairs
  nb = [sorted(sum(A[j]) for j in range(n) if A[i][j]) for i in range(n)]
  tri = sum(A[i][j] * A[j][k] * A[i][k] for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n))
  return (n, tuple(deg), tri, tuple(sorted(map(tuple, nb))))


def main():
  path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'census_nonsingular_nneg_le4.txt.gz')
  counts = defaultdict(lambda: defaultdict(int))
  buckets = defaultdict(list)
  order15 = []
  bad = 0
  last_progress = time.monotonic()
  for done, line in enumerate(gzip.open(path, 'rt'), 1):
    if time.monotonic() - last_progress >= 15:
      print(f'census: {done}/45242 exact inertia and isomorphism checks', file=sys.stderr, flush=True)
      last_progress = time.monotonic()
    g6, N, p, q = line.split()
    N, p, q = int(N), int(p), int(q)
    A = g6_decode(g6)
    assert len(A) == N
    pos, zero, neg = ldl_inertia(A)
    if not (zero == 0 and pos == p and neg == q and q <= 4):
      bad += 1
      print('INERTIA MISMATCH', g6, (pos, zero, neg), (p, q))
    counts[N][q] += 1
    G = nx.from_edgelist([(i, j) for i in range(N) for j in range(i + 1, N) if A[i][j]])
    G.add_nodes_from(range(N))
    key = invariant(A)
    for H in buckets[key]:
      if nx.is_isomorphic(G, H):
        bad += 1
        print('DUPLICATE', g6)
        break
    buckets[key].append(G)
    if N == 15:
      order15.append(G)
  metadata = json.load(open(os.path.join(HERE, 'census_counts.json')))
  digest = hashlib.sha256(gzip.open(path, 'rb').read()).hexdigest()
  if digest != metadata['sha256_uncompressed']:
    sys.exit('FAIL: uncompressed census hash differs from metadata')
  ref = metadata['counts_by_order_and_nneg']
  got = {str(N): {str(q): c for q, c in d.items()} for N, d in counts.items()}
  same = got == {N: {q: c for q, c in d.items()} for N, d in ref.items()}
  ext = [nx.from_numpy_array(__import__('numpy').array(M)) for M in (w5(), affine_x())]
  ext_ok = len(order15) == 2 and all(any(nx.is_isomorphic(E, G) for G in order15) for E in ext)
  print(json.dumps({'graphs': sum(sum(d.values()) for d in counts.values()), 'inertia_or_duplicate_failures': bad,
                    'counts_match_json': same, 'order15_are_W5_and_X': ext_ok,
                    'max_order': max(counts), 'counts': got, 'sha256_uncompressed': digest}, indent=1))
  sys.exit(0 if (bad == 0 and same and ext_ok) else 1)


if __name__ == '__main__':
  main()
