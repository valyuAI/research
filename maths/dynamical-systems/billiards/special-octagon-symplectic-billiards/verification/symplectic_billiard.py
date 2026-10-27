#!/usr/bin/env python3
"""Exact symplectic billiards on convex polygons with rational vertices (standard library only).

A boundary point is a pair (i, t): side i runs from vertex V[i] to V[i+1], the point is
V[i] + t * E[i] with 0 <= t < 1, and t == 0 means the vertex V[i].

The symplectic billiard map sends a chord (x, y) to (y, z), where z is the other endpoint of the
chord through x parallel to the side containing y (Albers-Tabachnikov).

critical_set() computes the set C of critical points of Albers-Lander-Westermann for a single
convex table: the even-indexed points x_0, x_2, x_4, ... of all trajectories that start at a
vertex x_0 (x_1 ranging over every open side). It explores states (even point, open interval of odd
points on one side); an odd interval is split wherever an odd point can be sent to a vertex.
The exploration terminates exactly when C is finite (the state space is then finite).
"""
from collections import deque
from fractions import Fraction as Fr
import random


def cross(a, b):
  return a[0] * b[1] - a[1] * b[0]


class Polygon:
  def __init__(self, verts):
    self.V = [(Fr(x), Fr(y)) for x, y in verts]
    n = len(self.V)
    self.n = n
    self.E = [(self.V[(i + 1) % n][0] - self.V[i][0], self.V[(i + 1) % n][1] - self.V[i][1]) for i in range(n)]
    if sum(cross(self.V[i], self.V[(i + 1) % n]) for i in range(n)) <= 0:
      raise ValueError('vertices must be listed counterclockwise')
    for i in range(n):
      if cross(self.E[i], self.E[(i + 1) % n]) <= 0:
        raise ValueError(f'not strictly convex at vertex {(i + 1) % n}')

  def point(self, p):
    i, t = p
    return (self.V[i][0] + t * self.E[i][0], self.V[i][1] + t * self.E[i][1])

  def normalize(self, i, t):
    return ((i + 1) % self.n, Fr(0)) if t == 1 else (i, t)

  @staticmethod
  def is_vertex(p):
    return p[1] == 0

  def strictly_inside(self, X):
    return all(cross(self.E[i], (X[0] - self.V[i][0], X[1] - self.V[i][1])) > 0 for i in range(self.n))

  def sigma(self, p, d):
    """Other endpoint of the interior chord through boundary point p parallel to d (None if none)."""
    P = self.point(p)
    found = None
    for k in range(self.n):
      ek = self.E[k]
      den = cross(ek, d)
      if den == 0:
        continue
      w = (P[0] - self.V[k][0], P[1] - self.V[k][1])
      u = cross(w, d) / den
      s = cross(w, ek) / den
      if u < 0 or u > 1 or s == 0:
        continue
      Q = (P[0] + s * d[0], P[1] + s * d[1])
      if not self.strictly_inside(((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)):
        continue
      cand = self.normalize(k, u)
      if found is not None and self.point(found) != self.point(cand):
        raise RuntimeError('chord with two distinct far endpoints')
      found = cand
    return found

  def step(self, x, y):
    """One application of the symplectic billiard map; y must not be a vertex."""
    return self.sigma(x, self.E[y[0]])


def _image_parameter(poly, j, t, d, k):
  """Parameter on side k of the point reached from (j, t) along direction d (affine extension)."""
  P = (poly.V[j][0] + t * poly.E[j][0], poly.V[j][1] + t * poly.E[j][1])
  ek = poly.E[k]
  w = (P[0] - poly.V[k][0], P[1] - poly.V[k][1])
  u = cross(w, d) / cross(ek, d)
  assert 0 <= u <= 1
  return u


def critical_set(poly, max_states=10 ** 6):
  """Return (finite, C, number_of_states). finite is False if max_states was exceeded."""
  n = poly.n
  C = set((i, Fr(0)) for i in range(n))
  seen = set()
  queue = deque(((v, Fr(0)), (j, Fr(0), Fr(1))) for v in range(n) for j in range(n))
  while queue:
    state = queue.popleft()
    if state in seen:
      continue
    seen.add(state)
    if len(seen) > max_states:
      return False, C, len(seen)
    e, (j, lo, hi) = state
    dj = poly.E[j]
    e2 = poly.sigma(e, dj)              # next even point: chord from e parallel to the odd side
    if e2 is None:
      continue
    C.add(e2)
    if poly.is_vertex(e2):
      continue
    k = e2[0]
    dk = poly.E[k]
    if cross(dj, dk) == 0:
      continue
    cuts = set()                         # odd points on (lo, hi) whose image is a vertex
    for w in range(n):
      pre = poly.sigma((w, Fr(0)), dk)
      if pre is not None and pre[0] == j and lo < pre[1] < hi:
        cuts.add(pre[1])
    pts = [lo] + sorted(cuts) + [hi]
    for a, b in zip(pts, pts[1:]):
      kk = poly.sigma((j, (a + b) / 2), dk)[0]
      ta = _image_parameter(poly, j, a, dk, kk)
      tb = _image_parameter(poly, j, b, dk, kk)
      queue.append((e2, (kk, min(ta, tb), max(ta, tb))))
  return True, C, len(seen)


def orbit_period(poly, x, y, max_iter=10 ** 6):
  """Period of the orbit of the chord (x, y); None if a vertex is hit, -1 if not closed in max_iter."""
  x0, y0 = x, y
  for k in range(1, max_iter + 1):
    if poly.is_vertex(y):
      return None
    z = poly.step(x, y)
    if z is None:
      return None
    x, y = y, z
    if (x, y) == (x0, y0):
      return k
  return -1


def generic_periods(poly, C):
  """Periods of two off-centre rational points in every cell of the C-grid (illustration)."""
  breaks = {i: sorted({Fr(0), Fr(1)} | {t for (s, t) in C if s == i}) for i in range(poly.n)}
  out = {}
  for i in range(poly.n):
    for j in range(poly.n):
      if cross(poly.E[i], poly.E[j]) == 0:
        continue
      for a, b in zip(breaks[i], breaks[i][1:]):
        for c, d in zip(breaks[j], breaks[j][1:]):
          per = []
          for (r, s) in ((Fr(1, 3), Fr(2, 7)), (Fr(3, 11), Fr(5, 13))):
            k = orbit_period(poly, (i, a + r * (b - a)), (j, c + s * (d - c)))
            assert k is not None and k > 0
            per.append(k)
          out[max(per)] = out.get(max(per), 0) + 1
  return out


def special_octagon(W, H, c1, c2):
  """Rectangle [0,W]x[0,H] with top corners cut by 45-degree legs c1 and bottom corners by c2."""
  if not (c1 > 0 and c2 > 0 and 2 * c1 < W and 2 * c2 < W and c1 + c2 < H):
    raise ValueError('invalid octagon parameters')
  return [(c2, 0), (W - c2, 0), (W, c2), (W, H - c1), (W - c1, H), (c1, H), (0, H - c1), (0, c2)]


def hexhouse(s, h, p, q):
  """Square [0,s]^2 with the trapezoid (0,s),(s,s),(q,s+h),(p,s+h) on top, 0 < p < q < s."""
  if not (0 < p < q < s and h > 0):
    raise ValueError('invalid Hexhouse parameters')
  return [(0, 0), (s, 0), (s, s), (q, s + h), (p, s + h), (0, s)]


def penthouse(a, b):
  """Unit square with apex (b, 1 + a), a > 0, 0 < b < 1 (Albers et al., Section 4)."""
  return [(0, 0), (1, 0), (1, 1), (b, 1 + a), (0, 1)]
