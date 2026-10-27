#!/usr/bin/env python3
"""Exhaustive check (standard library) of Lemma 3.4: for every split [n] = X u Y with the given sizes and
every phylogenetic tree T on [n], some edge of T splits [n] into Z, W such that one of the pairs
(X n Z, Y n W), (X n W, Y n Z) has sizes at least 3 and 4 in some order.
Since relabelling is free, it suffices to check every unrooted shape on n leaves (enumerated by leaf insertion
and deduplicated, as in sat/indep/indep_cnf.py) with every choice of |X| leaves as X.
Usage: bipartition_check.py n u   (checks |X| = u, |Y| = n - u). Prints the number of (shape, X) pairs
without such an edge; 0 means the lemma holds for these sizes."""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sat', 'indep'))
from indep_cnf import shapes_by_insertion, adjacency

def leaf_sides(edges, n):
    adj = adjacency(edges); out = []
    for a, b in edges:
        seen = {a, b}; st = [b]; side = 0
        while st:
            x = st.pop()
            if x < n: side |= 1 << x
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        out.append(side)
    return out

def good(i, j, u, v):
    # pair (i, v - j) or (u - i, j) dominates sizes 3 and 4 in some order
    def ok(a, b): return min(a, b) >= 3 and max(a, b) >= 4
    return ok(i, v - j) or ok(u - i, j)

def main(n, u, expected_shapes=None):
    v = n - u
    shapes = shapes_by_insertion(n)
    if expected_shapes is not None and len(shapes) != expected_shapes:
        raise ValueError(f'expected {expected_shapes} shapes, got {len(shapes)}')
    bad = 0
    for index, edges in enumerate(shapes, 1):
        sides = leaf_sides(edges, n)
        for X in itertools.combinations(range(n), u):
            xm = sum(1 << x for x in X)
            if not any(good((s & xm).bit_count(), (s & ~xm).bit_count(), u, v) for s in sides):
                bad += 1
        if index % 15 == 0 or index == len(shapes):
            print(f'n={n} |X|={u}: {index}/{len(shapes)} shapes done, bad={bad}', flush=True)
    print(f'n={n} |X|={u} |Y|={v}: {len(shapes)} shapes, {bad} (shape, X) pairs with no good edge', flush=True)
    return bad

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    parser.add_argument('u', type=int)
    parser.add_argument('--expect-bad', type=int)
    parser.add_argument('--expect-shapes', type=int)
    args = parser.parse_args()
    bad = main(args.n, args.u, args.expect_shapes)
    if args.expect_bad is not None and bad != args.expect_bad:
        raise ValueError(f'expected {args.expect_bad} bad colourings, got {bad}')
