"""Complete generation of point-determining (PD) graphs with at most k negative adjacency eigenvalues,
level by level in the order, with pruned extension for saturated parents and a process pool.

Completeness argument (see README): Sumner's lemma (every PD graph on >= 2 vertices has a vertex whose
deletion is PD) + interlacing (n^- does not increase under vertex deletion) => every PD graph with
n^- <= k on h+1 vertices is a one-vertex PD extension of a PD graph with n^- <= k on h vertices.
Rejections use only eigenvalues certified negative (computed < -TOL, float error << TOL), so no true
extension is lost; every stored graph is then verified exactly (integer charpoly + Descartes).

Usage: python point_determining_bfs.py k [workers] [maxorder]
Outputs output/pdk{k}/level{h}.g6 and progress lines on stdout.
"""
import sys, os, time
import numpy as np
from multiprocessing import Pool

TOL = 1e-6
K = None


def g6_encode(A):
  n = A.shape[0]
  bits = []
  for j in range(1, n):
    for i in range(j):
      bits.append(int(A[i, j]))
  while len(bits) % 6:
    bits.append(0)
  out = [n + 63]
  for t in range(0, len(bits), 6):
    v = 0
    for b in bits[t:t + 6]:
      v = 2 * v + b
    out.append(v + 63)
  return bytes(out)


def g6_decode(s):
  n = s[0] - 63
  A = np.zeros((n, n), dtype=np.int8)
  bits = []
  for ch in s[1:]:
    v = ch - 63
    for t in range(5, -1, -1):
      bits.append((v >> t) & 1)
  k = 0
  for j in range(1, n):
    for i in range(j):
      A[i, j] = A[j, i] = bits[k]
      k += 1
  return A


def cert(A):
  import pynauty
  n = A.shape[0]
  adj = {i: [int(j) for j in np.nonzero(A[i])[0] if j > i] for i in range(n)}
  return pynauty.certificate(pynauty.Graph(n, adjacency_dict=adj)) + bytes([n])


def exact_inertia(A):
  from flint import fmpz_mat
  n = A.shape[0]
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


def nneg_lower(Ms):
  ev = np.linalg.eigvalsh(Ms.astype(np.float64))
  return (ev < -TOL).sum(axis=1)


def critical_order(A, k):
  """Vertex order whose prefixes reach n^- = n^-(A) as early as possible (greedy deletion)."""
  h = A.shape[0]
  target = nneg_lower(A[None])[0]
  keep = list(range(h))
  for v in range(h):
    trial = [u for u in keep if u != v]
    if trial and nneg_lower(A[np.ix_(trial, trial)][None])[0] == target:
      keep = trial
  rest = [u for u in range(h) if u not in keep]
  return keep + rest, len(keep), int(target)


def extensions(A, k):
  """All neighbourhood vectors b (as bool arrays over V(A)) such that A+b is PD and the certified
  lower bound on n^-(A+b) is <= k. Pruned DFS (batched by depth) along a critical vertex order."""
  h = A.shape[0]
  order, t0, target = critical_order(A, k)
  if target < k:
    # n^-(A+v) <= n^-(A)+1 <= k for every v: no spectral pruning needed
    s = np.arange(1 << h, dtype=np.int64)
    b = ((s[:, None] >> np.arange(h)[None, :]) & 1).astype(np.int8)
    w = (1 << np.arange(h)).astype(np.int64)
    rows = (A.astype(np.int64) * w[None, :]).sum(axis=1)
    bad = np.zeros(1 << h, dtype=bool); bad[rows] = True
    return b[~bad]
  Ap = A[np.ix_(order, order)]
  # depth-wise batched enumeration; candidates are (N, t) 0/1 arrays over the first t vertices of order
  cand = np.zeros((1, 0), dtype=np.int8)
  for t in range(1, h + 1):
    N = cand.shape[0]
    new = np.empty((2 * N, t), dtype=np.int8)
    new[:N, :t - 1] = cand; new[:N, t - 1] = 0
    new[N:, :t - 1] = cand; new[N:, t - 1] = 1
    cand = new
    if t >= t0 or t == h:
      # check prefix graph A[:t,:t] + v
      sub = Ap[:t, :t]
      keep = np.ones(cand.shape[0], dtype=bool)
      CH = 1 << 15
      for st in range(0, cand.shape[0], CH):
        c = cand[st:st + CH]
        M = np.zeros((c.shape[0], t + 1, t + 1), dtype=np.int8)
        M[:, :t, :t] = sub[None]
        M[:, :t, t] = c
        M[:, t, :t] = c
        keep[st:st + CH] = nneg_lower(M) <= k
      cand = cand[keep]
  # map back to original vertex labels
  b = np.zeros((cand.shape[0], h), dtype=np.int8)
  b[:, order] = cand
  # PD filter: b != row of any vertex
  w = (1 << np.arange(h)).astype(np.int64)
  rows = set(int(x) for x in (A.astype(np.int64) * w[None, :]).sum(axis=1))
  bm = (b.astype(np.int64) * w[None, :]).sum(axis=1)
  ok = np.array([int(x) not in rows for x in bm], dtype=bool)
  return b[ok]


def work_extend(g6):
  A = g6_decode(g6)
  h = A.shape[0]
  out = {}
  for bvec in extensions(A, K):
    M = np.zeros((h + 1, h + 1), dtype=np.int8)
    M[:h, :h] = A; M[:h, h] = bvec; M[h, :h] = bvec
    c = cert(M)
    if c not in out:
      out[c] = g6_encode(M)
  return out


def work_exact(item):
  c, g6 = item
  A = g6_decode(g6)
  p, z, q = exact_inertia(A)
  red = int(A.sum(axis=1).min() > 0)
  return c, g6, p, z, q, red


def init(k):
  global K
  K = k


def main():
  k = int(sys.argv[1]); workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
  maxorder = int(sys.argv[3]) if len(sys.argv) > 3 else 100
  outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', f'pdk{k}'); os.makedirs(outdir, exist_ok=True)
  level = {b'start': g6_encode(np.zeros((1, 1), dtype=np.int8))}
  h = 1
  best = {}
  with Pool(workers, initializer=init, initargs=(k,)) as pool:
    while level and h < maxorder:
      t0 = time.time()
      merged = {}
      done = 0
      items = list(level.values())
      for res in pool.imap_unordered(work_extend, items, chunksize=max(1, len(items) // (workers * 20) or 1)):
        for c, g in res.items():
          if c not in merged:
            merged[c] = g
        done += 1
        if done % 2000 == 0:
          print(f'   order {h+1}: extended {done}/{len(items)} parents, {len(merged)} candidates ({time.time()-t0:.0f}s)', flush=True)
      t1 = time.time()
      nxt = {}
      stats = {}
      with open(f'{outdir}/level{h+1}.g6', 'wb') as f:
        for c, g6, p, z, q, red in pool.imap_unordered(work_exact, list(merged.items()), chunksize=256):
          if q <= k:
            nxt[c] = g6
            f.write(g6 + b' %d %d %d %d\n' % (p, z, q, red))
            if red:
              s = stats.setdefault(q, [0, 0])
              s[0] += 1; s[1] = max(s[1], p)
      h += 1
      level = nxt
      for q, (cnt, mp) in stats.items():
        best[q] = max(best.get(q, 0), mp)
      print(f'k={k} order={h}: PD={len(level)} (cand {len(merged)}) reduced by n^- (count,max n^+): '
            f'{dict(sorted((q, tuple(v)) for q, v in stats.items()))} ext {t1-t0:.0f}s exact {time.time()-t1:.0f}s', flush=True)
  print('FINAL max n^+ by n^- over reduced graphs:', best, 'last nonempty order', h - 1, flush=True)


if __name__ == '__main__':
  main()
