#!/usr/bin/env python3
"""Independent checker (standard library only) for the one-pair game bounds of Theorem 2.9.

Input: a JSON file with 'thresholds' (thr[m][u] = claimed least v such that sizes (u, v) are m-safe, or null)
and 'bounds' ({k: n}). Every claim that is used is re-derived here:
  (u, v) is 0-safe iff min(u, v) >= 2.
  (u, v) is m-safe (m >= 1) if it dominates (componentwise, in some order) a pair (u', v') for which no
  phylogenetic tree with u' red and v' blue leaves has all its edges bad, where an edge whose one side holds
  i red and j blue leaves is good iff (i, v'-j) or (u'-i, j) is (m-1)-safe.
  'Some tree has all edges bad' is decided by dynamic programming over clusters: a cluster (i, j) is realisable
  if it is bad and is a leaf or the union of two realisable clusters; a tree with all edges bad exists iff
  (u', v') is the sum of three realisable clusters (root the tree at an internal vertex).
  First tree: k trees on n leaves have a common quartet if no tree on n leaves has all edges bad, where an
  edge with s leaves on one side is good iff (s, n-s) is (k-1)-safe.
Only the claims needed for the stated bounds are checked (lazily)."""
import json, sys
from functools import lru_cache

def main(path, kmax):
    C = json.load(open(path))
    thr = C['thresholds']
    bounds = {int(k): n for k, n in C['bounds'].items() if n is not None and int(k) <= kmax}

    def claimed(m, a, b):
        t = thr[m]
        def one(x, y): return 0 <= x < len(t) and t[x] is not None and y >= t[x]
        return one(a, b) or one(b, a)

    @lru_cache(None)
    def safe(m, a, b):
        """claimed AND verified"""
        if a > b: a, b = b, a
        if m == 0: return a >= 2
        if not claimed(m, a, b): return False
        # find a base pair (u', v') <= (a, b) in some order whose safety is verified directly
        for u in range(2, b + 1):
            t = thr[m][u] if u < len(thr[m]) else None
            if t is None: continue
            for (x, y) in ((u, t), (t, u)):
                if x <= a and y <= b or x <= b and y <= a:
                    if direct(m, x, y): return True
        raise AssertionError(f'claim not verified: level {m}, pair {(a, b)}')

    @lru_cache(None)
    def direct(m, u, v):
        bad = {(i, j): not (safe(m - 1, i, v - j) or safe(m - 1, u - i, j))
               for i in range(u + 1) for j in range(v + 1)}
        R = set()
        cells = sorted(bad, key=lambda c: c[0] + c[1])
        for (i, j) in cells:
            if i + j == 0 or not bad[(i, j)]: continue
            if i + j == 1:
                R.add((i, j)); continue
            if any((i - a, j - b) in R for (a, b) in R if a <= i and b <= j and (a, b) != (i, j)):
                R.add((i, j))
        Rl = list(R)
        for (a1, b1) in Rl:
            for (a2, b2) in Rl:
                if (u - a1 - a2, v - b1 - b2) in R:
                    return False
        return True

    for k in sorted(bounds):
        n = bounds[k]
        bad = [not safe(k - 1, s, n - s) for s in range(n + 1)]
        R = set()
        for s in range(1, n + 1):
            if bad[s] and (s == 1 or any(t in R and s - t in R for t in range(1, s))):
                R.add(s)
        adversary = any(a in R and b in R and n - a - b in R for a in range(1, n) for b in range(1, n - a))
        assert not adversary, (k, n)
        print(f'k={k}: verified that every {k} trees on {n} leaves have a common quartet (h({k}) <= {n})', flush=True)
    print('OK')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
