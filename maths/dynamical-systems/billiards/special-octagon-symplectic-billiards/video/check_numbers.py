#!/usr/bin/env python3
"""Recompute every number and example shown in the explainer video, exactly.

Run: python3 check_numbers.py   (standard library only, a few seconds)

It imports the paper's own library ../verification/symplectic_billiard.py (exact Fraction
arithmetic) wherever possible, and asserts every value that appears on screen:

 1. the rule in the rectangle [0,4] x [0,3]: (1,0), (4,2), (1,3), (0,2), back after 4 steps;
 2. an ordinary (angle in = angle out) billiard path in the same rectangle that closes;
 3. the octagon O(5,6,1,2): vertices, side lines with whole-number constants, the mirror;
 4. the hook orbit (period 92) and the gallery of periods 4, 16, 32, 44, 68, 92;
 5. the critical set C (20 points) and the dot set S (16 green + 6 blue + 4 orange = 26);
 6. the corner trajectory of the paper's figure (46 steps), its even chain and every move type;
 7. the hypothetical "bad" diagonal moves from (7/2, 6): (5, 9/2) then (5/4, 3/4);
 8. the box (cell) hopping in the phase square for the period-16 orbit, home after 16 hops;
 9. the naive closure under all four directions: denominators grow (16384 reported in
    ../verification/filled_set_results.txt; here a short run shows the growth);
10. the asymmetric octagon Q: the 6-point loop, multipliers -2 and -1/2, nudged laps;
11. the symmetric Hexhouse X(3,2,1,2) -> O(6,5,2,0) and the bounds 26 and 2600.
"""

import math
import sys
from collections import deque
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'verification'))
from symplectic_billiard import Polygon, special_octagon, critical_set, orbit_period, _image_parameter  # noqa: E402


def s(p):
  return '(' + ', '.join(str(c) for c in p) + ')'


def locate(P, pt):
  """Boundary parameter (side, t) of a point in the relative interior of a side (or a vertex)."""
  pt = (Fr(pt[0]), Fr(pt[1]))
  for i in range(P.n):
    if P.V[i] == pt:
      return (i, Fr(0))
  for i in range(P.n):
    a, e = P.V[i], P.E[i]
    t = (pt[0] - a[0]) / e[0] if e[0] != 0 else (pt[1] - a[1]) / e[1]
    if 0 < t < 1 and P.point((i, t)) == pt:
      return (i, t)
  raise ValueError(f'{pt} is not on the boundary')


def orbit(P, x, y, steps):
  pts = [x, y]
  for _ in range(steps - 1):
    z = P.step(pts[-2], pts[-1])
    pts.append(z)
  return pts


# 1. The rule in a rectangle -------------------------------------------------------------
R = Polygon([(0, 0), (4, 0), (4, 3), (0, 3)])
rect = orbit(R, locate(R, (1, 0)), locate(R, (4, 2)), 6)
rect_pts = [R.point(p) for p in rect]
assert rect_pts[:5] == [(1, 0), (4, 2), (1, 3), (0, 2), (1, 0)] and rect_pts[5] == (4, 2)
print('1. rectangle rule:', ' -> '.join(s(p) for p in rect_pts), '(period 4)')


# 2. Ordinary billiards in the same rectangle --------------------------------------------
def ordinary(start, d, W=4, Hh=3, bounces=40):
  """Reflection billiard in [0,W]x[0,Hh] with exact arithmetic; returns the bounce points."""
  p, (dx, dy) = start, d
  pts = [p]
  for _ in range(bounces):
    ts = []
    if dx > 0:
      ts.append((W - p[0]) / dx)
    if dx < 0:
      ts.append(-p[0] / dx)
    if dy > 0:
      ts.append((Hh - p[1]) / dy)
    if dy < 0:
      ts.append(-p[1] / dy)
    t = min(ts)
    p = (p[0] + t * dx, p[1] + t * dy)
    if p[0] in (0, W):
      dx = -dx
    if p[1] in (0, Hh):
      dy = -dy
    assert not (p[0] in (0, W) and p[1] in (0, Hh)), 'hit a corner'
    pts.append(p)
    if p == start and (dx, dy) == d:
      return pts
  return pts


ob = ordinary((Fr(1, 2), Fr(0)), (Fr(1), Fr(1)))
assert ob[-1] == ob[0] and len(ob) - 1 == 14
print('2. ordinary billiard from (1/2, 0) at 45 degrees closes after', len(ob) - 1, 'bounces')

# 3. The octagon O(5,6,1,2) --------------------------------------------------------------
W, H, c1, c2 = 5, 6, 1, 2
OCT = special_octagon(W, H, c1, c2)
P = Polygon(OCT)
assert OCT == [(2, 0), (3, 0), (5, 2), (5, 5), (4, 6), (1, 6), (0, 5), (0, 2)]
lines = []
for i in range(8):
  (ax, ay), (ex, ey) = P.V[i], P.E[i]
  # line through V[i] with direction E[i]: ey*x - ex*y = ey*ax - ex*ay; normalise to small integers
  g = math.gcd(int(ex), int(ey)) or 1
  a, b = ey / g, -ex / g
  lines.append((a, b, a * ax + b * ay))
const = [ln[2] for ln in lines]
assert all(c.denominator == 1 for c in const)
print('3. side lines (a x + b y = c):', [(int(a), int(b), int(c)) for a, b, c in lines])
mirror = [(W - x, y) for x, y in OCT]
assert sorted(mirror) == sorted(OCT)
print('   mirror x -> 5 - x maps the octagon to itself')

# 4. Hook orbit and gallery --------------------------------------------------------------
HOOK = ((Fr(7, 3), Fr(0)), (Fr(11, 3), Fr(2, 3)))
hook_per = orbit_period(P, locate(P, HOOK[0]), locate(P, HOOK[1]))
assert hook_per == 92
print('4. hook orbit from', s(HOOK[0]), s(HOOK[1]), 'has period', hook_per)
GALLERY = {4: ((Fr(7, 3), 0), (5, 3)), 16: ((Fr(17, 5), Fr(2, 5)), (Fr(9, 2), Fr(11, 2))),
           32: ((Fr(7, 3), 0), (Fr(14, 3), Fr(16, 3))), 44: ((Fr(17, 5), Fr(2, 5)), (5, Fr(7, 2))),
           68: ((Fr(7, 3), 0), (Fr(17, 5), Fr(2, 5))), 92: HOOK}
for per, (a, b) in GALLERY.items():
  assert orbit_period(P, locate(P, a), locate(P, b)) == per
print('   gallery periods', sorted(GALLERY))

# 5. Critical set C and dot set S --------------------------------------------------------
fin, C, nstates = critical_set(P)
Cpts = sorted(P.point(c) for c in C)
assert fin and len(Cpts) == 20


def side_kind(pt):
  """'h' horizontal, 'v' vertical, 'd' diagonal side containing pt (first match)."""
  for i in range(8):
    a, b, c = lines[i]
    if a * pt[0] + b * pt[1] == c:
      lo = [min(P.V[i][k], P.V[(i + 1) % 8][k]) for k in (0, 1)]
      hi = [max(P.V[i][k], P.V[(i + 1) % 8][k]) for k in (0, 1)]
      if lo[0] <= pt[0] <= hi[0] and lo[1] <= pt[1] <= hi[1]:
        return 'h' if b != 0 and a == 0 else 'v' if a != 0 and b == 0 else 'd'
  return None


S0, Sd, Sh = [], [], []
for i in range(2 * W + 1):
  for j in range(2 * H + 1):
    pt = (Fr(i, 2), Fr(j, 2))
    k = side_kind(pt)
    if k is None:
      continue
    if pt[0].denominator == 1 and pt[1].denominator == 1:
      S0.append(pt)
    elif k == 'd' and pt[0].denominator == 2 and pt[1].denominator == 2:
      Sd.append(pt)
    elif k == 'h' and pt[0].denominator == 2 and pt[1].denominator == 1:
      Sh.append(pt)
S = set(S0) | set(Sd) | set(Sh)
assert (len(S0), len(Sd), len(Sh), len(S)) == (16, 6, 4, 26) == (16, 6, 4, 4 * W + 2 * H - 2 * (c1 + c2))
assert set(Cpts) <= S
cg = sum(1 for p in Cpts if p in S0)
cb = sum(1 for p in Cpts if p in Sd)
co = sum(1 for p in Cpts if p in Sh)
assert (cg, cb, co) == (16, 2, 2)
print('5. |C| =', len(Cpts), '(green, blue, orange =', (cg, cb, co), ') inside |S| = 26 = 16 + 6 + 4')
print('   C =', ' '.join(s(p) for p in Cpts))
print('   blue dots', ' '.join(s(p) for p in sorted(Sd)), '| orange dots', ' '.join(s(p) for p in sorted(Sh)))

# 6. The corner trajectory of the paper's figure -----------------------------------------
traj = [(0, Fr(0)), (1, Fr(37, 100))]
while not P.is_vertex(traj[-1]):
  traj.append(P.step(traj[-2], traj[-1]))
tp = [P.point(p) for p in traj]
assert len(tp) - 1 == 46 and tp[0] == (2, 0) and tp[-1] == (3, 0)
even = tp[::2]
assert all(p in S for p in even)
assert (Fr(7, 2), Fr(1, 2)) in even and (Fr(7, 2), 6) in even
print('6. corner trajectory: 46 steps from (2,0) to (3,0); first even points',
      ' -> '.join(s(p) for p in even[:9]))
moves = []
for k in range(0, 16, 2):
  p, q, odd = tp[k], tp[k + 2], tp[k + 1]
  d = (q[0] - p[0], q[1] - p[1])
  kind = 'vertical' if d[0] == 0 else 'horizontal' if d[1] == 0 else 'slope 1' if d[0] == d[1] else 'slope -1'
  inv = {'vertical': f'x = {p[0]}', 'horizontal': f'y = {p[1]}', 'slope 1': f'x - y = {p[0] - p[1]}',
         'slope -1': f'x + y = {p[0] + p[1]}'}[kind]
  moves.append((s(p), s(q), kind, inv, s(odd)))
  print(f'   x{k} {s(p)} -> x{k + 2} {s(q)}: {kind} ({inv}), steered by x{k + 1} = {s(odd)}')
# the halving step and the mirror
assert tp[10] == (0, 4) and tp[12] == (Fr(7, 2), Fr(1, 2))
assert (Fr(4) + 3) / 2 == Fr(7, 2) and (Fr(4) - 3) / 2 == Fr(1, 2)
assert tp[2] == (5, 3) and tp[4] == (0, 3)
# coupling at the orange dot: x13 on the right side, x15 its mirror, x16 straight below x14
assert tp[14] == (Fr(7, 2), 6) and tp[13] == (5, Fr(112, 25)) and tp[15] == (0, Fr(112, 25))
assert tp[16] == (Fr(7, 2), Fr(1, 2))
print('   coupling: x13 =', s(tp[13]), 'x14 =', s(tp[14]), 'x15 =', s(tp[15]), 'x16 =', s(tp[16]))

# 7. The hypothetical bad moves from the orange dot (7/2, 6) ------------------------------
p = locate(P, (Fr(7, 2), 6))
q = P.sigma(p, (1, -1))
assert P.point(q) == (5, Fr(9, 2))
r = P.sigma(q, (1, 1))
assert P.point(r) == (Fr(5, 4), Fr(3, 4))
print('7. bad case: (7/2, 6) -> slope -1 ->', s(P.point(q)), '-> slope 1 ->', s(P.point(r)), '(quarters)')


# 8. The phase square: boxes and one box hopping home ------------------------------------
def arc(pt_param):
  i, t = pt_param
  L = 0.0
  for k in range(i):
    L += math.hypot(*map(float, P.E[k]))
  return L + float(t) * math.hypot(*map(float, P.E[i]))


perim = sum(math.hypot(*map(float, e)) for e in P.E)
assert abs(perim - (10 + 6 * math.sqrt(2))) < 1e-12
br = {i: sorted({Fr(0), Fr(1)} | {t for (j, t) in C if j == i}) for i in range(8)}
assert sum(len(b) - 1 for b in br.values()) == 20   # 20 arcs between the 20 red dots


def cell_of(pp):
  i, t = pp
  for a, b in zip(br[i], br[i][1:]):
    if a < t < b:
      return (i, a, b)
  return None


x16 = locate(P, GALLERY[16][0])
y16 = locate(P, GALLERY[16][1])
o16 = orbit(P, x16, y16, 18)
cells = [(cell_of(o16[0]), cell_of(o16[1]))]
cur = cells[0]
for k in range(16):
  I, J = cur
  mid = P.sigma((I[0], (I[1] + I[2]) / 2), P.E[J[0]])
  kk = mid[0]
  ta = _image_parameter(P, I[0], I[1], P.E[J[0]], kk)
  tb = _image_parameter(P, I[0], I[2], P.E[J[0]], kk)
  cur = (J, (kk, min(ta, tb), max(ta, tb)))
  assert cur[1] in [(i, a, b) for i in br for a, b in zip(br[i], br[i][1:])], 'image is not a whole box'
  assert cur[1] == cell_of(o16[k + 2])
  cells.append(cur)
assert cells[16] == cells[0] and len(set(cells[:16])) == 16
print('8. perimeter 10 + 6 sqrt 2 =', round(perim, 3), '; 20 arcs, at most 20^2 - 20 = 380 boxes;',
      'the period-16 box visits 16 different boxes and returns to itself')


# 9. Naive closure under all four directions ---------------------------------------------
def naive(cap):
  F = set((i, Fr(0)) for i in range(8))
  queue = deque(F)
  dirs = [(1, 0), (0, 1), (1, 1), (1, -1)]
  while queue and len(F) < cap:
    pp = queue.popleft()
    for d in dirs:
      qq = P.sigma(pp, d)
      if qq is not None and qq not in F:
        F.add(qq)
        queue.append(qq)
  return F


Fn = naive(2000)
den = max(math.lcm(*(c.denominator for c in P.point(pp))) for pp in Fn)
assert len(Fn) >= 2000 and den >= 64
print('9. naive closure: first', len(Fn), 'points already have denominators up to', den,
      '(20000 points reach 16384: ../verification/filled_set_results.txt)')

# 10. The asymmetric octagon Q -----------------------------------------------------------
QV = [(1, 0), (3, 0), (4, 1), (4, 4), (3, 5), (2, 5), (0, 3), (0, 1)]
Q = Polygon(QV)
LOOP = [(4, Fr(11, 3)), (Fr(5, 3), 0), (Fr(2, 3), Fr(11, 3)), (4, Fr(7, 3)), (Fr(2, 3), Fr(1, 3)), (Fr(5, 3), Fr(14, 3))]
lp = orbit(Q, locate(Q, LOOP[0]), locate(Q, LOOP[1]), 8)
assert [Q.point(pp) for pp in lp[:6]] == [(Fr(a), Fr(b)) for a, b in LOOP]
assert lp[6] == lp[0] and lp[7] == lp[1]
print('10. Q loop:', ' -> '.join(s(Q.point(pp)) for pp in lp[:6]), '-> back')
# nudge the odd point x1 along the bottom side by 1/4 (in x): returns as -1/8, then 1/16, ...
NUDGE_ODD = Fr(1, 4)
y = locate(Q, (LOOP[1][0] + NUDGE_ODD, 0))
x = locate(Q, LOOP[0])
offs = []
for lap in range(5):
  pts = orbit(Q, x, y, 7)
  assert [pp[0] for pp in pts[:6]] == [pp[0] for pp in lp[:6]], 'left the neighbourhood'
  offs.append(Q.point(pts[1])[0] - LOOP[1][0])
  assert pts[6] == x            # the even point x0 returns exactly
  x, y = pts[6], pts[7]
assert offs == [Fr(1, 4), Fr(-1, 8), Fr(1, 16), Fr(-1, 32), Fr(1, 64)]
print('    nudge x1 by 1/4: offsets after each lap', [str(o) for o in offs])
# nudge the even point x0 up its side by 1/24: returns as -1/12, then 1/6
NUDGE_EVEN = Fr(1, 24)
x = locate(Q, (4, LOOP[0][1] + NUDGE_EVEN))
y = locate(Q, LOOP[1])
eoffs = []
for lap in range(4):
  pts = orbit(Q, x, y, 7)
  assert [pp[0] for pp in pts[:6]] == [pp[0] for pp in lp[:6]]
  eoffs.append(Q.point(pts[0])[1] - LOOP[0][1])
  if lap < 3:
    assert pts[7] == y
  x, y = pts[6], pts[7]
assert eoffs == [Fr(1, 24), Fr(-1, 12), Fr(1, 6), Fr(-1, 3)]
assert Q.point(x) == (Fr(23, 6), Fr(25, 6))   # the fourth lap ends off the loop's sides altogether
print('    nudge x0 by 1/24: offsets after each lap', [str(o) for o in eoffs], 'then it is thrown off the loop')
assert all(Fr(c).denominator == 3 for pt in LOOP for c in pt if Fr(c).denominator != 1)
print('    every loop coordinate is whole or in thirds, so none is on the half-grid')

# 11. Hexhouse and bounds ----------------------------------------------------------------
hexh = [(0, 0), (3, 0), (3, 3), (2, 5), (1, 5), (0, 3)]
stretched = [(2 * a, 1 * b) for a, b in hexh]
assert stretched == [(0, 0), (6, 0), (6, 3), (4, 5), (2, 5), (0, 3)]
N = 4 * W + 2 * H - 2 * (c1 + c2)
assert N == 26 and 4 * (N * N - N) == 2600 and 20 * 20 - 20 == 380
print('11. Hexhouse X(3,2,1,2) stretched by 2 sideways = O(6,5,2,0); N = 26, bound 4(N^2 - N) = 2600')
print('PASS: every number on screen recomputed')
