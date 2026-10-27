#!/usr/bin/env python3
"""Critical-set exploration for lattice octagons with slopes 0, +-1, infinity but no mirror axis.

Exploratory evidence only (not used in any proof). The exploration of C is capped at 40000 states;
'CAP' means it had not closed up by then. Corner legs are listed as
(bottom-left, bottom-right, top-right, top-left). The first octagon is Q of Proposition 3.6.
"""
import sys
import time
from symplectic_billiard import Polygon, critical_set


def octagon(W, H, a, b, c, d):
  return [(a, 0), (W - b, 0), (W, b), (W, H - c), (W - c, H), (d, H), (0, H - d), (0, a)]


CASES = [(4, 5, 1, 1, 1, 2), (4, 8, 1, 1, 2, 1), (5, 6, 1, 3, 1, 1), (4, 7, 1, 2, 1, 2)]

if __name__ == '__main__':
  cap = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
  for case in CASES:
    t0 = time.time()
    fin, C, ns = critical_set(Polygon(octagon(*case)), max_states=cap)
    W, H, a, b, c, d = case
    kind = 'centrally symmetric' if (a, b) == (c, d) else 'no symmetry'
    print(f'{case} ({kind}): {"finite" if fin else "CAP"} |C| >= {len(C)} states {ns} {time.time() - t0:.0f}s', flush=True)
