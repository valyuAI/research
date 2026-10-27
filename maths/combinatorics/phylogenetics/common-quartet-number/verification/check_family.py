#!/usr/bin/env python3
"""Standalone checker (standard library only).
Reads unrooted binary trees in Newick format (one per line, leaves labelled 1..n), checks that all trees are
binary on the same leaf set, and counts 4-subsets resolved identically in every tree (common quartets).
Quartet topology is computed by the four-point condition on unit-length path distances."""
import sys, itertools
from collections import deque

def parse(s):
    s = s.strip().rstrip(';')
    adj = {}; stack = []; nxt = [0]; leaves = {}
    def node():
        nxt[0] += 1; v = ('i', nxt[0]); adj[v] = []; return v
    i = 0; cur = None; root = None
    while i < len(s):
        ch = s[i]
        if ch == '(':
            v = node()
            if stack: adj[stack[-1]].append(v); adj[v].append(stack[-1])
            else: root = v
            stack.append(v); i += 1
        elif ch == ')':
            stack.pop(); i += 1
        elif ch == ',':
            i += 1
        else:
            j = i
            while j < len(s) and s[j] not in '(),': j += 1
            lab = int(s[i:j]); v = ('l', lab); adj[v] = []
            adj[stack[-1]].append(v); adj[v].append(stack[-1]); leaves[lab] = v; i = j
    return adj, leaves

def check(lines):
    trees = [parse(l) for l in lines if l.strip()]
    labs = sorted(trees[0][1])
    n = len(labs)
    assert labs == list(range(1, n + 1)), 'leaves must be 1..n'
    tops = []
    for adj, leaves in trees:
        assert sorted(leaves) == labs, 'different leaf sets'
        for v, nb in adj.items():
            assert len(nb) == (1 if v[0] == 'l' else 3), 'not an unrooted binary tree'
        D = {}
        for a in labs:
            dist = {leaves[a]: 0}; dq = deque([leaves[a]])
            while dq:
                x = dq.popleft()
                for y in adj[x]:
                    if y not in dist: dist[y] = dist[x] + 1; dq.append(y)
            D[a] = {b: dist[leaves[b]] for b in labs}
        t = {}
        for a, b, c, d in itertools.combinations(labs, 4):
            s = (D[a][b] + D[c][d], D[a][c] + D[b][d], D[a][d] + D[b][c])
            m = min(s); assert s.count(m) == 1
            t[(a, b, c, d)] = s.index(m)
        tops.append(t)
    common = [q for q in tops[0] if len({t[q] for t in tops}) == 1]
    return n, len(trees), common

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--expect-common', type=int)
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    for path in args.paths:
        n, k, common = check(open(path).read().splitlines())
        print(f'{path}: {k} trees on {n} leaves, common quartets: {len(common)}' + (f' e.g. {common[0]}' if common else ''), flush=True)
        if args.expect_common is not None and len(common) != args.expect_common:
            raise ValueError(f'expected {args.expect_common} common quartets, got {len(common)}')
