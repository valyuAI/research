#!/usr/bin/env python3
"""Independent check of the half-lattice invariant for special octagons (standard library only).

Special octagon O(W,H,c1,c2): the rectangle [0,W]x[0,H] with the two top corners cut by 45-degree
segments of leg c1 and the two bottom corners cut by 45-degree segments of leg c2.
It is symmetric under x -> W - x.

For every vertex v and every side j, the script follows all symplectic billiard trajectories
(x0 = v, x1 in the open side j) exactly, splitting the odd interval whenever an odd point can hit
a vertex, and checks at every even point x_{2l}:
  (A) x_{2l} is in S = I u Hd u Hh, where
      I  = integer points of the boundary,
      Hd = points on a 45-degree side with both coordinates in Z + 1/2,
      Hh = points on a horizontal side with x in Z + 1/2;
  (B) if x_{2l} is in Hh then x_{2l+1} lies on a vertical side.
It also reports whether the exploration closes up (finitely many states), i.e. whether the
critical set C of Albers-Lander-Westermann is finite, and |C|.
"""
from fractions import Fraction as F
from collections import deque
import sys

DIRS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


class Octagon:
  def __init__(self, W, H, c1, c2):
    assert c1 > 0 and c2 > 0 and 2 * c1 < W and 2 * c2 < W and c1 + c2 < H
    self.W, self.H, self.c1, self.c2 = W, H, c1, c2
    self.verts = [(c2, 0), (W - c2, 0), (W, c2), (W, H - c1), (W - c1, H), (c1, H), (0, H - c1), (0, c2)]
    self.verts = [(F(x), F(y)) for x, y in self.verts]

  def inside(self, x, y):
    W, H, c1, c2 = self.W, self.H, self.c1, self.c2
    return (0 < x < W and 0 < y < H and x + y > c2 and x - y < W - c2 and x + y < W + H - c1
            and y - x < H - c1)

  def side_of(self, x, y):
    """Return (side, is_vertex) for a boundary point; side = index of a side containing the point."""
    for i, v in enumerate(self.verts):
      if (x, y) == v:
        return i, True
    W, H, c1, c2 = self.W, self.H, self.c1, self.c2
    tests = [
      y == 0 and c2 < x < W - c2,
      x - y == W - c2 and W - c2 < x < W,
      x == W and c2 < y < H - c1,
      x + y == W + H - c1 and W - c1 < x < W,
      y == H and c1 < x < W - c1,
      y - x == H - c1 and 0 < x < c1,
      x == 0 and c2 < y < H - c1,
      x + y == c2 and 0 < x < c2,
    ]
    hits = [i for i, t in enumerate(tests) if t]
    assert len(hits) == 1, (x, y, hits)
    return hits[0], False

  def chord(self, p, d):
    """Other endpoint of the chord through boundary point p in direction +-d, or None."""
    x0, y0 = p
    dx, dy = d
    cands = []
    W, H, c1, c2 = self.W, self.H, self.c1, self.c2
    # supporting lines of the eight sides as a*x + b*y = c
    lines = [(0, 1, 0), (1, -1, W - c2), (1, 0, W), (1, 1, W + H - c1), (0, 1, H), (-1, 1, H - c1),
             (1, 0, 0), (1, 1, c2)]
    for a, b, c in lines:
      den = a * dx + b * dy
      if den == 0:
        continue
      t = F(c - a * x0 - b * y0) / den
      if t == 0:
        continue
      q = (x0 + t * dx, y0 + t * dy)
      mid = ((x0 + q[0]) / 2, (y0 + q[1]) / 2)
      if not self.inside(*mid):
        continue
      try:
        self.side_of(*q)
      except AssertionError:
        continue
      cands.append(q)
    cands = list(set(cands))
    if not cands:
      return None
    assert len(cands) == 1, (p, d, cands)
    return cands[0]


def classify(O, p):
  x, y = p
  side, isv = O.side_of(x, y)
  if x.denominator == 1 and y.denominator == 1:
    return 'I'
  if side in (1, 3, 5, 7) and x.denominator == 2 and y.denominator == 2:
    return 'Hd'
  if side in (0, 4) and x.denominator == 2:
    return 'Hh'
  return 'BAD'


def point_on_side(O, j, u):
  """Point on side j with running coordinate u (u = x except on vertical sides where u = y)."""
  W, H, c1, c2 = O.W, O.H, O.c1, O.c2
  if j == 0: return (u, F(0))
  if j == 1: return (u, u - (W - c2))
  if j == 2: return (F(W), u)
  if j == 3: return (u, (W + H - c1) - u)
  if j == 4: return (u, F(H))
  if j == 5: return (u, u + (H - c1))
  if j == 6: return (F(0), u)
  if j == 7: return (u, c2 - u)


def coord(j, p):
  return p[1] if j in (2, 6) else p[0]


def side_range(O, j):
  a, b = O.verts[j], O.verts[(j + 1) % 8]
  lo, hi = sorted((coord(j, a), coord(j, b)))
  return lo, hi


def run(W, H, c1, c2, cap=10 ** 6):
  O = Octagon(W, H, c1, c2)
  verts = O.verts
  C = set(verts)
  seen = set()
  dq = deque()
  for v in verts:
    for j in range(8):
      lo, hi = side_range(O, j)
      dq.append((v, j, lo, hi))
  bad = []
  while dq:
    st = dq.popleft()
    if st in seen:
      continue
    seen.add(st)
    if len(seen) > cap:
      return False, C, bad, len(seen)
    e, j, lo, hi = st
    # coupling check (B) at the current state: even point e, odd side j
    if classify(O, e) == 'Hh' and j not in (2, 6):
      bad.append(('B', e, j))
    e2 = O.chord(e, DIRS[j])
    if e2 is None:
      continue
    C.add(e2)
    if classify(O, e2) == 'BAD':
      bad.append(('A', e2))
    k, isv = O.side_of(*e2)
    if isv:
      continue
    dk = DIRS[k]
    if DIRS[j][0] * dk[1] - DIRS[j][1] * dk[0] == 0:
      continue
    # odd interval (lo,hi) on side j moves along dk; split where the chord hits a vertex
    cuts = set()
    for w in verts:
      q = O.chord(w, dk)
      if q is None:
        continue
      try:
        sq, qv = O.side_of(*q)
      except AssertionError:
        continue
      if not qv and sq == j and lo < coord(j, q) < hi:
        cuts.add(coord(j, q))
    pts = [lo] + sorted(cuts) + [hi]
    for a, b in zip(pts, pts[1:]):
      mid = point_on_side(O, j, (a + b) / 2)
      qm = O.chord(mid, dk)
      sm, _ = O.side_of(*qm)
      # image endpoints by extending the affine chord map to the closed interval
      ims = []
      for u in (a, b):
        p = point_on_side(O, j, u)
        # intersect line p + t dk with the supporting line of side sm
        x0, y0 = p
        A2, B2, C2 = [(0, 1, 0), (1, -1, W - c2), (1, 0, W), (1, 1, W + H - c1), (0, 1, H),
                      (-1, 1, H - c1), (1, 0, 0), (1, 1, c2)][sm]
        den = A2 * dk[0] + B2 * dk[1]
        t = F(C2 - A2 * x0 - B2 * y0) / den
        ims.append(coord(sm, (x0 + t * dk[0], y0 + t * dk[1])))
      ia, ib = sorted(ims)
      dq.append((e2, sm, ia, ib))
  return True, C, bad, len(seen)


if __name__ == '__main__':
  N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
  from math import gcd
  total = 0
  allok = True
  maxC = 0
  for W in range(1, N + 1):
    for H in range(1, N + 1):
      for c1 in range(1, N + 1):
        for c2 in range(1, N + 1):
          if not (2 * c1 < W and 2 * c2 < W and c1 + c2 < H):
            continue
          fin, C, bad, ns = run(W, H, c1, c2)
          total += 1
          maxC = max(maxC, len(C))
          if not fin or bad:
            allok = False
            print('FAIL', (W, H, c1, c2), fin, bad[:5], flush=True)
    print(f'W <= {W}: {total} octagons checked, all ok so far: {allok}, max |C| = {maxC}', flush=True)
  print('RESULT', 'PASS' if allok else 'FAIL', total, 'octagons', flush=True)
  sys.exit(0 if allok else 1)
