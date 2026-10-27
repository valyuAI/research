#!/usr/bin/env python3
"""Size of the filled set of vertices F (closure of the vertices under chords parallel to all sides).

Used for Remark 3.5 of the paper: for several special octagons the exploration of F has not closed
after the cap, so the filled-set criterion of Albers-Lander-Westermann (their Theorem 3.1) does not
currently supply a proof for the family. Reaching the cap does not prove that F is infinite.
Reports |F| up to a cap and the largest denominator met.
"""
from collections import deque
from fractions import Fraction as Fr
from math import lcm
from symplectic_billiard import Polygon, special_octagon


def filled_set(poly, cap=20000):
  F = set((i, Fr(0)) for i in range(poly.n))
  queue = deque(F)
  dirs = []
  for e in poly.E:
    if all(e[0] * d[1] - e[1] * d[0] != 0 for d in dirs):
      dirs.append(e)
  while queue and len(F) < cap:
    p = queue.popleft()
    for d in dirs:
      q = poly.sigma(p, d)
      if q is not None and q not in F:
        F.add(q)
        queue.append(q)
  den = max(lcm(*(c.denominator for c in poly.point(p))) for p in F)
  return len(F), len(F) >= cap, den


if __name__ == '__main__':
  for params in [(3, 3, 1, 1), (4, 4, 1, 1), (5, 6, 1, 2), (6, 5, 2, 1), (7, 9, 3, 2)]:
    size, capped, den = filled_set(Polygon(special_octagon(*params)))
    print(params, '|F| >=' if capped else '|F| =', size, 'max denominator', den, flush=True)
