"""Quartet encodings for unrooted binary phylogenetic trees (leaves 0..n-1)."""
import itertools

def quartet_index(n):
    qs = list(itertools.combinations(range(n), 4))
    return qs, {q: i for i, q in enumerate(qs)}

def topo_of_split(q, pair):
    """q=(a,b,c,d) sorted; pair = frozenset of the two leaves on one side. 0: ab|cd, 1: ac|bd, 2: ad|bc"""
    a, b, c, d = q
    s = set(pair)
    if s == {a, b} or s == {c, d}: return 0
    if s == {a, c} or s == {b, d}: return 1
    return 2

def five_patterns():
    """For a sorted 5-tuple of positions (0..4), list the 15 consistent assignments as dict quartet(sub-4-tuple of positions)->topo."""
    pos = (0, 1, 2, 3, 4)
    pats = []
    for m in pos:
        rest = [p for p in pos if p != m]
        x = rest[0]
        for y in rest[1:]:
            z, w = [p for p in rest[1:] if p != y]
            # tree xy | m | zw
            pat = {}
            for drop in pos:
                q = tuple(p for p in pos if p != drop)
                if drop == m: pair = (x, y)
                elif drop == x: pair = (y, m)
                elif drop == y: pair = (x, m)
                elif drop == z: pair = (x, y)
                else: pair = (x, y)
                pat[q] = topo_of_split(q, pair)
            pats.append(pat)
    assert len(pats) == 15 and len({tuple(sorted(p.items())) for p in pats}) == 15
    return pats

# --- trees as adjacency dicts; leaves 0..n-1, internal nodes n.. ---
def tree_quartets(adj, n):
    """Return list topo[qi] for all 4-subsets, computed via path intersections (independent of SAT encoding)."""
    # distances between leaves via BFS
    import collections
    dist = {}
    for s in range(n):
        d = {s: 0}; dq = collections.deque([s])
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1; dq.append(v)
        dist[s] = d
    qs, _ = quartet_index(n)
    out = []
    for (a, b, c, d) in qs:
        s0 = dist[a][b] + dist[c][d]
        s1 = dist[a][c] + dist[b][d]
        s2 = dist[a][d] + dist[b][c]
        m = min(s0, s1, s2)
        cnt = [s0, s1, s2].count(m)
        assert cnt == 1, "unresolved quartet: tree not binary?"
        out.append([s0, s1, s2].index(m))
    return out
