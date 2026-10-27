#!/usr/bin/env python3
"""Check Corollary 3.4 on instances: mirror-symmetric Hexhouses (p + q = s).

The affine map (x, y) -> (h x, p y) sends the Hexhouse with vertices (0,0), (s,0), (s,s), (q,s+h),
(p,s+h), (0,s) to the lattice hexagon O(W, H, c1, 0) with W = h s, H = p (s + h), c1 = h p.
For every such Hexhouse with parameters <= N this script computes the critical set C exactly,
maps it to O(W, H, c1, 0) and checks that C is finite and contained in the half-lattice set S
(lattice points of the boundary, points with both coordinates in Z + 1/2 on a diagonal side,
points of a horizontal side with half-integer abscissa).
Usage: check_symmetric_hexhouses.py [N] (default 11).
"""
import sys
from math import gcd
from symplectic_billiard import Polygon, critical_set, generic_periods, hexhouse


def in_S(X, Y, W, H, c1):
  if X.denominator == 1 and Y.denominator == 1:
    return True
  if Y == 0 or Y == H:                                   # horizontal sides
    return X.denominator == 2
  if X == 0 or X == W:                                   # vertical sides: only lattice points
    return False
  return X.denominator == 2 and Y.denominator == 2       # diagonal sides


N = int(sys.argv[1]) if len(sys.argv) > 1 else 11
count, maxC = 0, 0
for s in range(3, N + 1):
  for h in range(1, N + 1):
    for p in range(1, s):
      q = s - p
      if not p < q or gcd(gcd(s, h), p) != 1:
        continue
      P = Polygon(hexhouse(s, h, p, q))
      fin, C, ns = critical_set(P)
      W, H, c1 = h * s, p * (s + h), h * p
      pts = [P.point(c) for c in C]
      img = [(h * x, p * y) for x, y in pts]
      assert fin, (s, h, p, q)
      assert all(in_S(X, Y, W, H, c1) for X, Y in img), (s, h, p, q)
      count += 1
      maxC = max(maxC, len(C))
  print(f'  s <= {s}: {count} symmetric Hexhouses ok, max |C| = {maxC}', flush=True)
print(f'PASS: {count} symmetric Hexhouses with parameters <= {N}: C finite and inside S', flush=True)
P = Polygon(hexhouse(3, 1, 1, 2))
fin, C, ns = critical_set(P)
print('generic periods of X(3,1,1,2):', sorted(generic_periods(P, C)), '(ABS Figure 18 reports 4, 44, 68, 92)', flush=True)
