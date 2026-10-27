"""Reconstruct an unrooted binary tree from a full quartet system (if tree-like), by stepwise leaf insertion."""
import itertools
from qlib import quartet_index, tree_quartets

def reconstruct(qsys, n):
    qs, qid = quartet_index(n)
    def topo(a, b, c, d):
        q = tuple(sorted((a, b, c, d)))
        return q, qsys[qid[q]]
    # tree on leaves 0,1,2 with centre node
    nxt = [n]
    adj = {0: [n], 1: [n], 2: [n], n: [0, 1, 2]}
    nxt[0] += 1
    placed = [0, 1, 2]
    for x in range(3, n):
        edges = [(u, v) for u in adj for v in adj[u] if u < v]
        good = []
        for (u, v) in edges:
            w = nxt[0]
            A = {k: list(vs) for k, vs in adj.items()}
            A[u].remove(v); A[v].remove(u)
            A[u].append(w); A[v].append(w); A[w] = [u, v, x]; A[x] = [w]
            # check quartets involving x and three placed leaves
            ok = True
            # compute quartet topologies of candidate restricted to placed+x using distances
            lv = placed + [x]
            import collections
            dist = {}
            for s in lv:
                d = {s: 0}; dq = collections.deque([s])
                while dq:
                    a = dq.popleft()
                    for b in A[a]:
                        if b not in d: d[b] = d[a] + 1; dq.append(b)
                dist[s] = d
            for tri in itertools.combinations(placed, 3):
                a, b, c, d = sorted(tri + (x,))
                s0 = dist[a][b] + dist[c][d]; s1 = dist[a][c] + dist[b][d]; s2 = dist[a][d] + dist[b][c]
                t = [s0, s1, s2].index(min(s0, s1, s2))
                if t != qsys[qid[(a, b, c, d)]]:
                    ok = False; break
            if ok: good.append(A)
        if len(good) != 1:
            return None
        adj = good[0]; nxt[0] += 1; placed.append(x)
    # relabel internal nodes compactly
    if tree_quartets(adj, n) != list(qsys):
        return None
    return adj
