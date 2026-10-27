#!/usr/bin/env python3
"""Compare the two octagon implementations on every admissible O(W,H,c1,c2) with parameters <= N.

Checks that symplectic_billiard.critical_set and independent_octagon_check.run report the same
finiteness, the same critical set (as a set of points in the plane) and the same number of
explored states. Usage: compare_implementations.py [N] (default 8).
"""
import sys
from itertools import product
from symplectic_billiard import Polygon, critical_set, special_octagon
import independent_octagon_check as ind

N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
count = 0
for W, H, c1, c2 in product(range(1, N + 1), repeat=4):
  if not (2 * c1 < W and 2 * c2 < W and c1 + c2 < H):
    continue
  P = Polygon(special_octagon(W, H, c1, c2))
  fin1, C1, ns1 = critical_set(P)
  fin2, C2, bad, ns2 = ind.run(W, H, c1, c2)
  pts1 = {P.point(p) for p in C1}
  pts2 = set(C2)
  assert fin1 and fin2 and not bad, (W, H, c1, c2)
  assert pts1 == pts2 and ns1 == ns2, (W, H, c1, c2, len(pts1), len(pts2), ns1, ns2)
  count += 1
print(f'PASS: {count} octagons with parameters <= {N}: identical critical sets and state counts', flush=True)
