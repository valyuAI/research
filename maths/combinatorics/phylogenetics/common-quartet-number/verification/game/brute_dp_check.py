# Validate the coloured-tree DP of exact_game.py against brute-force enumeration of all labelled trees.
import random, itertools, sys
import numpy as np
from exact_game import realisable, three_sum

def all_trees(L):
    """all unrooted binary trees on leaves 0..L-1 as lists of edge clusters (frozenset of leaves on one side)"""
    # represent tree by edge list over nodes; insertion
    def rec(edges, nxt_leaf, nxt_int):
        if nxt_leaf == L:
            yield edges; return
        for idx in range(len(edges)):
            a, b = edges[idx]
            w = nxt_int
            new = edges[:idx] + edges[idx + 1:] + [(a, w), (w, b), (w, nxt_leaf)]
            yield from rec(new, nxt_leaf + 1, nxt_int + 1)
    base = [(0, 1000), (1, 1000), (2, 1000)]
    yield from rec(base, 3, 1001)

def clusters(edges, L):
    adj = {}
    for a, b in edges: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    out = []
    for a, b in edges:
        seen = {a, b}; st = [b]; side = set()
        while st:
            x = st.pop()
            if x < L: side.add(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        out.append(side)
    return out

def brute(u, v, bad, trees_clusters):
    for cl in trees_clusters:
        if all(bad[sum(1 for x in c if x < u), sum(1 for x in c if x >= u)] for c in cl):
            return True
    return False

rng = random.Random(5)
for L in (5, 6, 7, 8):
    TC = [clusters(e, L) for e in all_trees(L)]
    print('L', L, 'trees', len(TC), flush=True)
    tests = 0
    for u in range(1, L):
        v = L - u
        for trial in range(60 if L < 8 else 25):
            bad = np.ones((u + 1, v + 1), dtype=bool)
            p = rng.random()
            for i in range(u + 1):
                for j in range(v + 1):
                    if (i, j) <= (u - i, v - j):
                        val = rng.random() < p
                        bad[i, j] = val; bad[u - i, v - j] = val
            dp = three_sum(realisable(bad), u, v)
            bf = brute(u, v, bad, TC)
            assert dp == bf, (u, v, bad.astype(int).tolist(), dp, bf)
            tests += 1
    print('  agree on', tests, 'random complement-symmetric bad sets', flush=True)
