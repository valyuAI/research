"""Enumerate unlabeled unrooted binary tree shapes with n leaves; return labeled representatives as adjacency dicts."""
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)

@lru_cache(maxsize=None)
def rooted_shapes(m):
    """All rooted binary shapes with m leaves as canonical nested tuples ('L' = leaf)."""
    if m == 1:
        return ('L',)
    out = []
    for a in range(1, m // 2 + 1):
        b = m - a
        A = rooted_shapes(a); B = rooted_shapes(b)
        for i, s in enumerate(A):
            for j, t in enumerate(B):
                if a == b and j < i: continue
                out.append(tuple(sorted((s, t), key=repr)))
    return tuple(out)

def to_adj(shape_with_extra_leaf_root):
    """Build unrooted tree: rooted shape S plus extra leaf attached to S's root. Leaves labelled 0..n-1, internal n.."""
    S = shape_with_extra_leaf_root
    leaves = []; edges = []; counter = [0]
    internal = []
    def build(s):
        if s == 'L':
            node = ('leaf', len(leaves)); leaves.append(node); return node
        node = ('int', len(internal)); internal.append(node)
        for c in s:
            edges.append((node, build(c)))
        return node
    r = build(S)
    extra = ('leaf', len(leaves)); leaves.append(extra)
    edges.append((r, extra))
    n = len(leaves)
    idx = {}
    for i, l in enumerate(leaves): idx[l] = i
    for j, v in enumerate(internal): idx[v] = n + j
    adj = {i: [] for i in range(n + len(internal))}
    for u, v in edges:
        adj[idx[u]].append(idx[v]); adj[idx[v]].append(idx[u])
    return adj, n

def canon_unrooted(adj):
    # find centre(s)
    deg = {v: len(adj[v]) for v in adj}
    remaining = set(adj)
    layer = [v for v in adj if deg[v] <= 1]
    while len(remaining) > 2:
        nxt = []
        for v in layer:
            remaining.discard(v)
            for u in adj[v]:
                if u in remaining:
                    deg[u] -= 1
                    if deg[u] == 1: nxt.append(u)
        layer = nxt
    cs = sorted(remaining)
    def enc(v, p):
        ch = sorted(enc(u, v) for u in adj[v] if u != p)
        return '(' + ''.join(ch) + ')'
    if len(cs) == 1:
        return 'C' + enc(cs[0], None)
    a, b = cs
    return 'E' + ''.join(sorted([enc(a, b), enc(b, a)]))

def unrooted_shapes(n):
    seen = {}
    for S in rooted_shapes(n - 1):
        if n - 1 == 1:
            S = 'L'
        adj, nn = to_adj(S)
        assert nn == n
        key = canon_unrooted(adj)
        if key not in seen:
            seen[key] = adj
    return list(seen.values())

if __name__ == '__main__':
    for n in range(4, 16):
        print(n, len(rooted_shapes(n - 1)), len(unrooted_shapes(n)))
