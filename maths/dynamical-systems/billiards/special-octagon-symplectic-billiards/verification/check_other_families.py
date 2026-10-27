#!/usr/bin/env python3
"""Instance checks for the Hexhouse (Conjecture 6.1) and Penthouse (Conjecture 4.1) of Albers et al.

These are checked computations, not proofs of the conjectures: for each listed instance the
critical set C is computed exactly; when it is finite, the periodicity criterion (Theorem 2.4 of the
paper, after Albers-Lander-Westermann) shows that every orbit of that instance is periodic.
For Penthouses the generic periods are also compared with 16m-4, 16m+4, 16m+12.
Writes other_families_results.json.
"""
import json
import sys
import time
from fractions import Fraction as Fr
from functools import reduce
from itertools import product
from math import floor, gcd
from symplectic_billiard import Polygon, critical_set, generic_periods, hexhouse, penthouse


def hexhouses(N):
  rows = []
  t0 = time.time()
  for s, h, p, q in product(range(1, N + 1), repeat=4):
    if not (0 < p < q < s) or reduce(gcd, (s, h, p, q)) != 1 or p + q > s:
      continue                                  # p + q > s is the mirror image of p' + q' < s
    fin, C, ns = critical_set(Polygon(hexhouse(s, h, p, q)))
    rows.append({'s': s, 'h': h, 'p': p, 'q': q, 'finite': fin, 'C_size': len(C), 'states': ns})
    if len(rows) % 100 == 0:
      print(f'  hexhouses: {len(rows)} done, {time.time() - t0:.0f}s', flush=True)
  return rows


def penthouses():
  rows = []
  avals = [Fr(3, 2), Fr(3, 4), Fr(51, 100), Fr(2, 5), Fr(53, 150), Fr(2, 7), Fr(11, 40), Fr(13, 60), Fr(83, 462), Fr(1, 7) + Fr(1, 97)]
  bvals = [Fr(1, 7), Fr(1, 3), Fr(1, 2), Fr(3, 5), Fr(5, 6), Fr(19, 20)]
  for a in avals:
    m = floor((a + 1) / a)
    for b in bvals:
      poly = Polygon(penthouse(a, b))
      fin, C, ns = critical_set(poly)
      gp = sorted(generic_periods(poly, C)) if fin else None
      exp = [16 * m - 4, 16 * m + 4, 16 * m + 12]
      rows.append({'a': str(a), 'b': str(b), 'm': m, 'finite': fin, 'C_size': len(C),
                   'generic_periods': gp, 'conjectured': exp, 'match': gp == exp})
      print(f'  penthouse a={a} b={b} m={m} |C|={len(C)} periods={gp} match={gp == exp}', flush=True)
  return rows


if __name__ == '__main__':
  N = int(sys.argv[1]) if len(sys.argv) > 1 else 11
  hx = hexhouses(N)
  ph = penthouses()
  out = {'hexhouse_N': N, 'hexhouses': len(hx), 'hexhouses_all_finite': all(r['finite'] for r in hx),
         'hexhouse_max_C': max(r['C_size'] for r in hx), 'penthouses': len(ph),
         'penthouses_all_finite': all(r['finite'] for r in ph),
         'penthouses_all_match_conjectured_periods': all(r['match'] for r in ph),
         'hexhouse_rows': hx, 'penthouse_rows': ph}
  with open('other_families_results.json', 'w') as f:
    json.dump(out, f, indent=1)
  print('hexhouses', len(hx), 'all finite', out['hexhouses_all_finite'], 'penthouses', len(ph),
        'all match', out['penthouses_all_match_conjectured_periods'], flush=True)
  ok = out['hexhouses_all_finite'] and out['penthouses_all_finite'] and out['penthouses_all_match_conjectured_periods']
  sys.exit(0 if ok else 1)
