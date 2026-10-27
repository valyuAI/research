#!/usr/bin/env python3
"""Trihexagonal (3.6.3.6) grid with triangles refined into drafters.

All arithmetic is exact (integers).  Coordinates follow heesch-sat's TriHexGrid:
a cell is an integer pair (x, y) in the basis e1, e2 of the hexagonal lattice with
page(e1) = (1, 0), page(e2) = (1/2, sqrt(3)/2).  Cell type (x - y) mod 3:
0 = hexagon, 1 / 2 = triangles.  The hexagon translation lattice is
{(x, y): x - y = 0 mod 3}.

Atomic cells:
  ('H', X, Y)  hexagon, (X, Y) = 4 * centre
  ('D', X, Y)  drafter (30-60-90 triangle), (X, Y) = sum of its three corners in
               4x coordinates (centre of triangle, a vertex, a midpoint of an edge)
Points (corners) are in 4x coordinates.
"""
from fractions import Fraction

HEX_VERTS = [(-1, -1), (-2, 1), (-1, 2), (1, 1), (2, -1), (1, -2)]  # doubled offsets
TRI_VERTS = {1: [(-1, 1), (1, 0), (0, -1)], 2: [(-1, 0), (0, 1), (1, -1)]}

# 12 orientations (a, b, d, e): x' = a x + b y, y' = d x + e y  (heesch-sat order)
ORIENTS = [
  (1, 0, 0, 1), (0, -1, 1, 1), (-1, -1, 1, 0), (-1, 0, 0, -1), (0, 1, -1, -1), (1, 1, -1, 0),
  (0, 1, 1, 0), (-1, 0, 1, 1), (-1, -1, 0, 1), (0, -1, -1, 0), (1, 0, -1, -1), (1, 1, 0, -1),
]


def ctype(x, y):
  return (x - y) % 3


def gram(u, v):
  """Euclidean inner product (times 1) of lattice vectors u, v, as a Fraction."""
  return Fraction(u[0] * v[0]) + Fraction(u[1] * v[1]) + Fraction(u[0] * v[1] + u[1] * v[0], 2)


def cell_corners4(x, y):
  """Corners of trihex cell (x, y) in 4x coordinates, in cyclic order."""
  t = ctype(x, y)
  offs = HEX_VERTS if t == 0 else TRI_VERTS[t]
  pts = [(4 * x + 2 * ox, 4 * y + 2 * oy) for ox, oy in offs]
  return cyclic_sort(pts, (4 * x, 4 * y))


def angle_key(v):
  """Exact angular order key for lattice vector v (page coordinates via e1, e2)."""
  # page coords: (x + y/2, y*sqrt3/2); use half-plane + cross-product comparisons via
  # an exact pseudo-angle on (2x + y, y) scaled (sqrt3 factor monotone in y-sign only).
  px, py = 2 * v[0] + v[1], v[1]  # page*(2) with y-component missing sqrt3 (sign kept)
  # true page vector is (px/2, py*sqrt3/2); angle order is preserved by the map
  # (px, py) -> (px, py*sqrt3) since it is a positive diagonal scaling.
  import math
  return math.atan2(py * 3 ** 0.5, px)


def cyclic_sort(pts, c):
  return sorted(pts, key=lambda p: angle_key((p[0] - c[0], p[1] - c[1])))


def atoms_of_cell(x, y):
  """Atomic cells of trihex cell (x, y): one hexagon or six drafters."""
  t = ctype(x, y)
  c = (4 * x, 4 * y)
  if t == 0:
    return [('H', c[0], c[1])]
  vs = cell_corners4(x, y)
  out = []
  for i in range(3):
    a = vs[i]
    for j in ((i + 1) % 3, (i + 2) % 3):
      b = vs[j]
      m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
      out.append(('D', c[0] + a[0] + m[0], c[1] + a[1] + m[1]))
  return out


def atom_corners(atom):
  """Boundary points of an atomic cell (4x coords); hexagon includes edge midpoints."""
  kind, X, Y = atom
  if kind == 'H':
    x, y = X // 4, Y // 4
    vs = cell_corners4(x, y)
    pts = []
    for i in range(6):
      a, b = vs[i], vs[(i + 1) % 6]
      pts.append(a)
      pts.append(((a[0] + b[0]) // 2, (a[1] + b[1]) // 2))
    return pts
  # drafter: recover its triangle cell from (X, Y) by search over nearby cells
  return DRAFTER_CORNERS[atom]


DRAFTER_CORNERS = {}
DRAFTER_CELL = {}


def register_region(R):
  """Build drafter tables for all trihex cells with |x|,|y| <= R."""
  for x in range(-R, R + 1):
    for y in range(-R, R + 1):
      t = ctype(x, y)
      if t == 0:
        continue
      c = (4 * x, 4 * y)
      vs = cell_corners4(x, y)
      for i in range(3):
        a = vs[i]
        for j in ((i + 1) % 3, (i + 2) % 3):
          b = vs[j]
          m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
          key = ('D', c[0] + a[0] + m[0], c[1] + a[1] + m[1])
          DRAFTER_CORNERS[key] = [c, a, m]
          DRAFTER_CELL[key] = (x, y)


def transform_atom(atom, o, t):
  """Apply orientation o = (a, b, d, e) and hex-lattice translation t = (tx, ty)."""
  a, b, d, e = o
  kind, X, Y = atom
  s = 4 if kind == 'H' else 12
  return (kind, a * X + b * Y + s * t[0], d * X + e * Y + s * t[1])


def transform_point(p, o, t):
  a, b, d, e = o
  return (a * p[0] + b * p[1] + 4 * t[0], d * p[0] + e * p[1] + 4 * t[1])


def is_grid_symmetry(o):
  a, b, d, e = o
  M = ((a, b), (d, e))
  # preserves the Euclidean metric
  for u in ((1, 0), (0, 1)):
    for v in ((1, 0), (0, 1)):
      Mu = (a * u[0] + b * u[1], d * u[0] + e * u[1])
      Mv = (a * v[0] + b * v[1], d * v[0] + e * v[1])
      if gram(Mu, Mv) != gram(u, v):
        return False
  # preserves the hexagon sublattice
  for u in ((1, 1), (-1, 2)):
    Mu = (a * u[0] + b * u[1], d * u[0] + e * u[1])
    if (Mu[0] - Mu[1]) % 3:
      return False
  return True
