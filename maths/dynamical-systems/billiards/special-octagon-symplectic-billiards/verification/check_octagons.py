#!/usr/bin/env python3
"""Scan special octagons O(W,H,c1,c2) with all parameters <= N (default 14).

For each octagon: compute the critical set C exactly, check that C is finite and contained in
the half-lattice set S of the paper (Lemma 3.2), and record |C| and the number of explored states.
Also computes generic periods for the octagon of Figure 23 of Albers et al.
Usage: check_octagons.py [N] [output.json]  (default N = 14, output octagon_results.json).
"""
import json
import sys
import time
from symplectic_billiard import Polygon, critical_set, generic_periods, special_octagon


def in_S(poly, p):
  x, y = poly.point(p)
  side = p[0]
  if x.denominator == 1 and y.denominator == 1:
    return True                                   # I: lattice point
  if side in (1, 3, 5, 7) and x.denominator == 2 and y.denominator == 2:
    return True                                   # S_d: half-lattice point on a 45-degree side
  if side in (0, 4) and x.denominator == 2:
    return True                                   # S_h: half-integer abscissa on a horizontal side
  return False


def main(N, out_path='octagon_results.json'):
  t0 = time.time()
  rows = []
  ok = True
  for W in range(1, N + 1):
    for H in range(1, N + 1):
      for c1 in range(1, N + 1):
        for c2 in range(1, N + 1):
          if not (2 * c1 < W and 2 * c2 < W and c1 + c2 < H):
            continue
          poly = Polygon(special_octagon(W, H, c1, c2))
          fin, C, ns = critical_set(poly)
          inS = all(in_S(poly, p) for p in C)
          ok = ok and fin and inS
          rows.append({'W': W, 'H': H, 'c1': c1, 'c2': c2, 'finite': fin, 'C_subset_S': inS,
                       'C_size': len(C), 'states': ns, 'period_bound': 2 * (len(C) ** 2 - len(C))})
    print(f'W <= {W}: {len(rows)} octagons, all ok: {ok}, {time.time() - t0:.0f}s', flush=True)
  poly = Polygon(special_octagon(5, 6, 1, 2))
  fin, C, _ = critical_set(poly)
  fig23 = sorted(generic_periods(poly, C))
  print('generic periods of O(5,6,1,2):', fig23, flush=True)
  out = {'N': N, 'octagons': len(rows), 'all_finite_and_in_S': ok,
         'max_C_size': max(r['C_size'] for r in rows),
         'example_O_5_6_1_2_generic_periods': fig23, 'rows': rows}
  with open(out_path, 'w') as f:
    json.dump(out, f, indent=1)
  print('RESULT', 'PASS' if ok else 'FAIL', len(rows), 'octagons', flush=True)
  return ok


if __name__ == '__main__':
  n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
  path = sys.argv[2] if len(sys.argv) > 2 else 'octagon_results.json'
  sys.exit(0 if main(n, path) else 1)
