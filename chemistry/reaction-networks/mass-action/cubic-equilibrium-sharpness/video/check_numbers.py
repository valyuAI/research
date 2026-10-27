"""Reproduce every number shown or spoken in the explainer video.

Run from anywhere with Python 3 and NumPy:  python3 check_numbers.py
Exact data come from ../verification/cubic-sharpness-certificate.json; everything else is
recomputed here with exact fractions where it matters.
"""

import itertools
import json
import random
from fractions import Fraction as F
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CERT = json.loads((HERE.parent / 'verification' / 'cubic-sharpness-certificate.json').read_text())
CASES = {c['n']: c for c in CERT['cases']}
assert CERT['status'] == 'PASS'


def ok(msg):
  print('PASS', msg, flush=True)


# ---------------------------------------------------------------- n = 2 running example
c2 = CASES[2]
assert c2['source_rows'] == [['2', '1'], ['0', '2']]            # 2X+Y and 2Y
assert c2['product_rows'] == [['1', '0'], ['1', '3']]           # X and X+3Y
assert c2['rate_constants'] == ['1/9', '1']
assert c2['conservation_vector'] == [-1, 1] and c2['class_level'] == '-2'   # -X+Y = -2, so X-Y = 2
assert [e['concentrations'] for e in c2['equilibria']] == [['3', '1'], ['6', '4']]
for x, y in [(3, 1), (6, 4)]:
  assert F(1, 9) * x * x * y == y * y          # both rates equal
  assert F(y) == F(x * x, 9) and x - y == 2   # on the parabola and on the slice
assert all(x * x - 9 * x + 18 == 0 for x in (3, 6))
ok('n=2: rates X^2Y/9 and Y^2, slice X-Y=2, parabola Y=X^2/9, resting states (3,1) and (6,4)')

# Counter demo: start (5,3), first reaction (-1,-1), second (+1,+1)
assert (5 - 3, 4 - 2, 5 - 3) == (2, 2, 2)
ok('n=2: counter demo 5,3 -> 4,2 -> 5,3 keeps X-Y = 2')


def flow2(x):
  """Rate of change of X (and of Y) on the slice Y = X - 2."""
  y = x - 2
  return y * y - x * x * y / 9


# Along the slice dX/dt = -(X-2)(X-3)(X-6)/9: check the factorisation numerically
for x in np.linspace(2.0, 9.0, 57):
  assert abs(flow2(x) + (x - 2) * (x - 3) * (x - 6) / 9) < 1e-12
# Slope of the flow at each resting state equals the certificate's restricted Jacobian determinant
dets = [F(e['restricted_jacobian_determinant']) for e in c2['equilibria']]
assert dets == [F(1, 3), F(-4, 3)]
for x0, d in [(3, 1 / 3), (6, -4 / 3)]:
  h = 1e-6
  assert abs((flow2(x0 + h) - flow2(x0 - h)) / (2 * h) - d) < 1e-6


def settle(x, t_end=200.0, dt=0.01):
  for _ in range(int(t_end / dt)):
    k1 = flow2(x)
    k2 = flow2(x + dt * k1 / 2)
    k3 = flow2(x + dt * k2 / 2)
    k4 = flow2(x + dt * k3)
    x += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
  return x


ends = {x0: settle(x0) for x0 in (2.9, 3.1, 4.5, 5.9, 6.1, 8.0)}
assert ends[2.9] < 2.01                                       # leaves (3,1) towards Y = 0
assert all(abs(ends[x0] - 6) < 1e-6 for x0 in (3.1, 4.5, 5.9, 6.1, 8.0))
ok('n=2: on the slice (3,1) repels (slope +1/3) and (6,4) attracts (slope -4/3); not a claim of the paper')

# ---------------------------------------------------------------- n = 2 with pair collisions only
# Two species, two reactions, rank one. Enumerate every pair of sources with at most two molecules,
# every pair of opposite integer reaction directions with small entries and valid products, and
# random rate constants and slices. Count simple positive crossings of the slice with the balance set.


def complexes(max_mol):
  return [(a, b) for a in range(max_mol + 1) for b in range(max_mol + 1) if a + b <= max_mol]


def crossings(y1, y2, g1, g2, k1, k2, x0):
  """Positive simple equilibria on the line x0 + u*g, where gamma1 = -s1*g and gamma2 = s2*g."""
  ga, gb = g1
  s1, s2 = k1, k2
  # balance: s1 * x^y1 = s2 * x^y2 along X = x0[0] + ga u, Y = x0[1] + gb u
  px = np.poly1d([ga, x0[0]])
  py = np.poly1d([gb, x0[1]])
  lhs = s1 * px ** y1[0] * py ** y1[1]
  rhs = s2 * px ** y2[0] * py ** y2[1]
  p = lhs - rhs
  if np.allclose(p.coeffs, 0):
    return None  # every point balances: no isolated, nondegenerate equilibrium
  roots = [r.real for r in p.roots if abs(r.imag) < 1e-9]
  dp = p.deriv()
  good = []
  for u in roots:
    X, Y = x0[0] + ga * u, x0[1] + gb * u
    if X > 1e-9 and Y > 1e-9 and abs(dp(u)) > 1e-7 * max(1.0, abs(p.coeffs).max()):
      good.append(u)
  return len(set(np.round(good, 7)))


def max_crossings(max_mol, trials=60, seed=1):
  rng = random.Random(seed)
  best = 0
  dirs = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if (a, b) != (0, 0)]
  for y1, y2 in itertools.product(complexes(max_mol), repeat=2):
    if y1 == y2:
      continue
    for g in dirs:
      # reaction 1 moves by -m1*g, reaction 2 by +m2*g; products must be nonnegative integers
      for m1, m2 in [(1, 1), (1, 2), (2, 1)]:
        p1 = (y1[0] - m1 * g[0], y1[1] - m1 * g[1])
        p2 = (y2[0] + m2 * g[0], y2[1] + m2 * g[1])
        if min(p1) < 0 or min(p2) < 0:
          continue
        for _ in range(trials):
          k1, k2 = 10 ** rng.uniform(-2, 2), 10 ** rng.uniform(-2, 2)
          x0 = (10 ** rng.uniform(-1.5, 1.5), 10 ** rng.uniform(-1.5, 1.5))
          c = crossings(y1, y2, g, g, m1 * k1, m2 * k2, x0)
          if c is not None:
            best = max(best, c)
  return best


assert max_crossings(2) == 1
assert max_crossings(3, trials=25) >= 2
ok('n=2: random search over all pair-collision networks never finds 2 clean crossings; three-body does')

# ---------------------------------------------------------------- n = 3
c3 = CASES[3]
assert c3['source_rows'] == [['2', '1', '0'], ['0', '2', '1'], ['0', '0', '2']]
assert c3['product_rows'] == [['1', '0', '0'], ['0', '1', '2'], ['1', '2', '1']]
assert c3['rate_constants'] == ['1/306000', '1/79475', '1/121']
assert c3['conservation_vector'] == [-1, 1, 1] and c3['class_level'] == '36'
assert c3['powers'] == [3, 2, 4]
assert c3['polynomial_coefficients_constant_then_species_order'] == ['-36', '-60', '85', '11']
pts3 = [tuple(int(v) for v in e['concentrations']) for e in c3['equilibria']]
assert pts3 == [(60, 85, 11), (480, 340, 176), (1620, 765, 891)]
assert [F(e['polynomial_derivative']) for e in c3['equilibria']] == [34, -28, 78]
assert 60 ** 2 * 85 == 306000 and 85 ** 2 * 11 == 79475 and 11 ** 2 == 121
for t in (F(1), F(2), F(3), F(5, 2)):
  X, Y, Z = 60 * t ** 3, 85 * t ** 2, 11 * t ** 4
  assert X * X * Y / 306000 == Y * Y * Z / 79475 == Z * Z / 121 == t ** 8
# reaction changes (product - source) and the conserved combination Y + Z - X
gam = [(-1, -1, 0), (0, -1, 1), (1, 2, -1)]
for g in gam:
  assert -g[0] + g[1] + g[2] == 0
# resting rule: X: -a + c = 0, Z: b - c = 0, Y: -a - b + 2c = 0
for (X, Y, Z), t in zip(pts3, (1, 2, 3)):
  assert (X, Y, Z) == (60 * t ** 3, 85 * t ** 2, 11 * t ** 4) and -X + Y + Z == 36


def Q(t):
  return 11 * t ** 4 - 60 * t ** 3 + 85 * t ** 2


for t in (1, 2, 3):
  assert Q(t) == 36
P = np.poly1d([11, -60, 85, 0, -36])
assert np.allclose(np.polymul(np.polymul([1, -1], [1, -2]), np.polymul([1, -3], [11, 6])), P.coeffs)
crit = sorted(r.real for r in np.poly1d([44, -180, 170]).roots)
qmax, qmin = Q(crit[0]), Q(crit[1])
print(f'      n=3: local max of Q at t={crit[0]:.3f} is {qmax:.2f}; local min at t={crit[1]:.3f} is {qmin:.2f}')
assert 22 < qmin < 23 and 44 < qmax < 45 and min(Q(t) for t in np.linspace(0, 3.35, 400)) >= 0
assert Q(3.35) < 90
ok('n=3: rates all t^8 on (60t^3, 85t^2, 11t^4); Y+Z-X conserved; Q(t)=36 exactly at t=1,2,3')
ok('n=3: 11t^4-60t^3+85t^2-36 = (t-1)(t-2)(t-3)(11t+6); three crossings for any level in (22.7, 44.4)')

# ---------------------------------------------------------------- n = 4 polynomial on screen
c4 = CASES[4]
assert c4['powers'] == [5, 6, 4, 8]
coef = [int(v) for v in c4['polynomial_coefficients_constant_then_species_order']]
assert coef == [82944, 258300, -66025, -276388, 1169]
terms = sorted(zip([0] + c4['powers'], coef), reverse=True)    # by exponent, highest first
assert terms == [(8, 1169), (6, -66025), (5, 258300), (4, -276388), (0, 82944)]
flips = sum(1 for (_, a), (_, b) in zip(terms, terms[1:]) if (a > 0) != (b > 0))
assert flips == 4
for t in (1, 2, 3, 4):
  assert sum(a * t ** e for e, a in terms) == 0
ok('n=4: 1169t^8 - 66025t^6 + 258300t^5 - 276388t^4 + 82944 has 4 sign flips and roots 1,2,3,4')

# ---------------------------------------------------------------- general facts on screen
for n in range(2, 9):
  p = [(2 ** n + (-1) ** (n - i) * 2 ** (i - 1)) // 3 for i in range(1, n + 1)]
  assert p == CASES[n]['powers'] and len(set(p)) == n
  assert CASES[n]['maximum_source_molecularity'] == 3
assert sum(len(CASES[n]['equilibria']) for n in range(2, 9)) == 35
assert CASES[3]['maximum_product_molecularity'] == 4
ok('powers for n=2,3,4: (1,2), (3,2,4), (5,6,4,8); 35 checked equilibria for n=2..8')
