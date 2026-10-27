#!/usr/bin/env python3
"""Brute force (stdlib): for two trees given in Newick (leaves 1..n), find max over edge pairs (e1,e2) and
orientations of the separated pair sizes (|P1 & P2|, |Q1 & Q2|); report whether a pair with min >= s and
sum >= s+t exists."""
import sys, itertools
from check_family import parse
def splits(adj, leaves):
    labs = {v: k for k, v in leaves.items()}
    out = []
    for u in adj:
        for v in adj[u]:
            if str(u) < str(v):
                seen = {u, v}; st = [v]; side = set()
                while st:
                    x = st.pop()
                    if x in labs: side.add(labs[x])
                    for y in adj[x]:
                        if y not in seen: seen.add(y); st.append(y)
                out.append(frozenset(side))
    return out
def best(t1, t2, s, t):
    a1, l1 = parse(t1); a2, l2 = parse(t2)
    L = frozenset(l1)
    S1 = splits(a1, l1); S2 = splits(a2, l2)
    for P1 in S1:
        Q1 = L - P1
        for P2 in S2:
            Q2 = L - P2
            for X, Y in ((P1 & P2, Q1 & Q2), (P1 & Q2, Q1 & P2)):
                if min(len(X), len(Y)) >= s and len(X) + len(Y) >= s + t:
                    return (sorted(X), sorted(Y))
    return None
if __name__ == '__main__':
    lines = [l for l in open(sys.argv[1]).read().splitlines() if l.strip()]
    s, t = int(sys.argv[2]), int(sys.argv[3])
    for i, j in itertools.combinations(range(len(lines)), 2):
        print(f'pair ({i+1},{j+1}): separated ({s},{t}) pair:', best(lines[i], lines[j], s, t))
