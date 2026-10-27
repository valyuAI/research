"""List the implicitly tight rows (slack < tol at the relative-interior point) with their (class, S, T') meaning."""
import sys, numpy as np
pre, alpha, n = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
tol = float(sys.argv[4]) if len(sys.argv) > 4 else 1e-9
x = np.load(pre + '_relint_x.npy')
with open(pre + '.vars') as f:
  ncls, nvars = map(int, f.readline().split())
  codes = [int(l.split()[0]) for l in f]
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
def adj(code):
  a = [[0] * n for _ in range(n)]
  for t, (i, j) in enumerate(pairs):
    if code >> t & 1: a[i][j] = 1
    else: a[j][i] = 1
  return a
seen = {}
with open(pre + '.ub') as fu, open(pre + '.meta') as fm:
  for lu, lm in zip(fu, fm):
    p = lu.split()
    ent = [(int(a), int(b)) for a, b in (q.split(':') for q in p[1:]) if int(a) != nvars]
    val = sum(b * x[a] for a, b in ent)
    if alpha - val < tol:
      key = tuple(sorted(ent))
      ci, mask, bits = map(int, lm.split())
      if key in seen: continue
      seen[key] = 1
      A = adj(codes[ci]); S = [v for v in range(n) if mask >> v & 1]
      print('class', ci, 'scores', sorted((sum(r) for r in A), reverse=True), 'S', S, 'S-scores', [sum(A[v]) for v in S], 'bits', bits, 'value', val)
