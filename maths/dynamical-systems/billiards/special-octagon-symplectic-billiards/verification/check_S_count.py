#!/usr/bin/env python3
"""Check |S| = 4W + 2H - 2(c1 + c2) for all admissible octagons with parameters <= 12."""
import itertools
from fractions import Fraction as Fr
from symplectic_billiard import special_octagon


def S_points(W, H, c1, c2):
  V = [(Fr(a), Fr(b)) for a, b in special_octagon(W, H, c1, c2)]
  S = set()
  for i in range(2 * W + 1):
    for j in range(2 * H + 1):
      X, Y = Fr(i, 2), Fr(j, 2)
      for k in range(8):
        a, b = V[k], V[(k + 1) % 8]
        e = (b[0] - a[0], b[1] - a[1])
        on = (e[0] * (Y - a[1]) - e[1] * (X - a[0]) == 0 and min(a[0], b[0]) <= X <= max(a[0], b[0])
              and min(a[1], b[1]) <= Y <= max(a[1], b[1]))
        if not on:
          continue
        if (X.denominator == 1 and Y.denominator == 1) or (k in (1, 3, 5, 7) and X.denominator == 2 and Y.denominator == 2) \
           or (k in (0, 4) and X.denominator == 2):
          S.add((X, Y))
  return S


if __name__ == '__main__':
  n = bad = 0
  for W, H, c1, c2 in itertools.product(range(1, 13), repeat=4):
    if not (2 * c1 < W and 2 * c2 < W and c1 + c2 < H):
      continue
    n += 1
    if len(S_points(W, H, c1, c2)) != 4 * W + 2 * H - 2 * (c1 + c2):
      bad += 1
  print(f'{n} octagons checked, {bad} mismatches')
  raise SystemExit(1 if bad else 0)
