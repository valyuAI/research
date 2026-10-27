#!/usr/bin/env python3
"""Exact one-pair game. safe[m](u,v): if disjoint X, Y with |X|=u, |Y|=v are separated in some trees, then for
EVERY further m trees one can, one tree at a time, choose an edge and a diagonal pair (and shrink), ending with
two sets of size >= 2 separated in all trees. For one tree T' the restriction T'|(X u Y) is an arbitrary binary
tree with u red and v blue leaves; an edge with cluster (i,j) (red, blue counts on one side) is good if
(i, v-j) or (u-i, j) dominates a safe[m-1] pair. The adversary wins iff some coloured tree has no good edge:
rooted at an internal vertex, all subtree clusters are bad. DP: R = clusters realisable by rooted trees all of
whose clusters are bad; adversary wins iff (u,v) = r1+r2+r3 with r1,r2,r3 in R.
First tree: an uncoloured tree on n leaves; an edge splitting s | n-s is good if (s, n-s) is safe[k-1]."""
import sys, time, json
import numpy as np
INF = 10 ** 9

def realisable(bad):
    """bad: bool array (U+1)x(V+1) over clusters; returns R (rooted trees with all clusters bad)."""
    U, V = bad.shape[0] - 1, bad.shape[1] - 1
    R = np.zeros_like(bad)
    if U >= 1: R[1, 0] = bad[1, 0]
    if V >= 1: R[0, 1] = bad[0, 1]
    for s in range(2, U + V + 1):
        for i in range(max(0, s - V), min(U, s) + 1):
            j = s - i
            if not bad[i, j]: continue
            # exists r1 <= (i,j) with r1 in R and (i,j)-r1 in R
            A = R[:i + 1, :j + 1]
            if np.any(A & A[::-1, ::-1]):
                R[i, j] = True
    return R

def three_sum(R, u, v):
    """exists r1+r2+r3 = (u,v), all in R"""
    A = R[:u + 1, :v + 1]
    # S2 = R (+) R restricted
    pts = np.argwhere(A)
    S2 = np.zeros_like(A)
    for (a, b) in pts:
        S2[a:, b:] |= A[:u + 1 - a, :v + 1 - b]
    # need r3 in A with (u,v)-r3 in S2
    return bool(np.any(A & S2[::-1, ::-1]))

def make_safe(thr):
    def safe(a, b):
        if a < 0 or b < 0: return False
        return b >= thr[a] if a < len(thr) else b >= thr[-1]
    return lambda a, b: safe(a, b) or safe(b, a)

def level(prev_thr, N, vcap):
    safe = make_safe(prev_thr)
    new = [INF] * (N + 1)
    best = INF
    for u in range(2, N + 1):
        cur = best
        for v in range(u, min(cur, N + 1, vcap * u + 10)):
            bad = np.ones((u + 1, v + 1), dtype=bool)
            for i in range(u + 1):
                for j in range(v + 1):
                    if safe(i, v - j) or safe(u - i, j): bad[i, j] = False
            R = realisable(bad)
            if not three_sum(R, u, v):
                cur = v; break
        best = min(best, cur); new[u] = best
    for u in range(2, N + 1):
        for v in range(2, u):
            if new[v] <= u: new[u] = min(new[u], v); break
    for u in range(3, N + 1): new[u] = min(new[u], new[u - 1])
    return new

def first_tree_bound(thr, nmax):
    safe = make_safe(thr)
    for n in range(4, nmax + 1):
        bad = [not safe(s, n - s) for s in range(n + 1)]
        R = [False] * (n + 1)
        R[1] = bad[1]
        for s in range(2, n + 1):
            R[s] = bad[s] and any(R[t] and R[s - t] for t in range(1, s))
        adv = any(R[a] and R[b] and R[n - a - b] for a in range(1, n) for b in range(1, n - a))
        if not adv: return n
    return None

if __name__ == '__main__':
    K, N, vcap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    thr = [[INF, INF] + [2] * (N - 1)]
    out = {'thresholds': [], 'bounds': {}}
    print('k 1 h <=', first_tree_bound(thr[0], N), flush=True)
    for m in range(1, K):
        t0 = time.time()
        thr.append(level(thr[-1], N, vcap))
        b = first_tree_bound(thr[-1], N)
        out['bounds'][m + 1] = b
        print(time.strftime('%H:%M:%S'), f'level {m} ({time.time()-t0:.0f}s) thr[2..14]', [x if x < INF else None for x in thr[-1][2:15]], f'=> k {m+1} h <= {b}', flush=True)
    out['thresholds'] = [[x if x < INF else None for x in t] for t in thr]
    json.dump(out, open(f'thresholds_K{K}_N{N}.json', 'w'))
