#!/usr/bin/env python3
"""Exact check of the hyperbolic 6-periodic orbit in the asymmetric lattice octagon of Proposition 3.6.

Q has vertices (1,0),(3,0),(4,1),(4,4),(3,5),(2,5),(0,3),(0,1): opposite sides are parallel with
slopes 0, 1, infinity, -1, but Q has no axis of symmetry. The script is self-contained (standard
library only): it recomputes every chord from the side equations, checks that the six points
x0..x5 form a periodic trajectory with no vertex, and computes the return maps of the even and odd
points, which are affine with slopes -2 and -1/2 in the coordinate along each side.
"""
from fractions import Fraction as F

V = [(1, 0), (3, 0), (4, 1), (4, 4), (3, 5), (2, 5), (0, 3), (0, 1)]
V = [(F(a), F(b)) for a, b in V]
E = [(V[(i + 1) % 8][0] - V[i][0], V[(i + 1) % 8][1] - V[i][1]) for i in range(8)]


def cross(a, b):
  return a[0] * b[1] - a[1] * b[0]


def on_side(p):
  """Index of the side containing p in its relative interior (None for vertices or non-boundary)."""
  hits = []
  for i in range(8):
    w = (p[0] - V[i][0], p[1] - V[i][1])
    if cross(E[i], w) == 0:
      t = (w[0] * E[i][0] + w[1] * E[i][1]) / (E[i][0] ** 2 + E[i][1] ** 2)
      if 0 < t < 1:
        hits.append(i)
  return hits[0] if len(hits) == 1 else None


def inside(p):
  return all(cross(E[i], (p[0] - V[i][0], p[1] - V[i][1])) > 0 for i in range(8))


def chord(p, d):
  """Other endpoint of the interior chord through p parallel to d."""
  out = []
  for i in range(8):
    den = cross(E[i], d)
    if den == 0:
      continue
    w = (p[0] - V[i][0], p[1] - V[i][1])
    s = cross(w, E[i]) / den
    q = (p[0] + s * d[0], p[1] + s * d[1])
    if s != 0 and inside(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)) and on_side(q) is not None:
      out.append(q)
  out = sorted(set(out))
  assert len(out) == 1, (p, d, out)
  return out[0]


orbit = [(F(4), F(11, 3)), (F(5, 3), F(0)), (F(2, 3), F(11, 3)), (F(4), F(7, 3)), (F(2, 3), F(1, 3)), (F(5, 3), F(14, 3))]
n = len(orbit)
sides = [on_side(p) for p in orbit]
assert None not in sides, 'an orbit point is a vertex or off the boundary'
for k in range(n):
  prev, cur, nxt = orbit[k - 1], orbit[k], orbit[(k + 1) % n]
  assert chord(prev, E[sides[k]]) == nxt, k
print('6-periodic trajectory verified; sides', sides)


def slope(k):
  """Derivative of the projection x_{k-1} -> x_{k+1} along side(x_k), in edge parameters."""
  i, j, l = sides[k - 1], sides[k], sides[(k + 1) % n]
  return cross(E[i], E[j]) / cross(E[l], E[j])


lam_even = slope(1) * slope(3) * slope(5)   # x0 -> x2 -> x4 -> x0
lam_odd = slope(2) * slope(4) * slope(0)    # x1 -> x3 -> x5 -> x1
print('even return slope', lam_even, ' odd return slope', lam_odd)
assert lam_even == -2 and lam_odd == F(-1, 2)
# exact affine check: perturb x0 and x1 along their sides and apply the map six times
eps = F(1, 1000)
x = (orbit[0][0] + eps * E[sides[0]][0], orbit[0][1] + eps * E[sides[0]][1])
y = (orbit[1][0] + eps * E[sides[1]][0], orbit[1][1] + eps * E[sides[1]][1])
for k in range(n):
  x, y = y, chord(x, E[on_side(y)])
dx = (x[0] - orbit[0][0]) / E[sides[0]][0] if E[sides[0]][0] != 0 else (x[1] - orbit[0][1]) / E[sides[0]][1]
dy = (y[0] - orbit[1][0]) / E[sides[1]][0] if E[sides[1]][0] != 0 else (y[1] - orbit[1][1]) / E[sides[1]][1]
assert dx == lam_even * eps and dy == lam_odd * eps, (dx, dy)
print('perturbation by', eps, 'returns as', dx, 'and', dy)
print('PASS: hyperbolic periodic orbit, so Q is not fully periodic')
