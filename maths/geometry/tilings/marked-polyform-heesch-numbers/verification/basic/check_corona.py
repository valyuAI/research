#!/usr/bin/env python3
"""Independent checker for corona witnesses on the trihexagonal (3.6.3.6) grid whose
triangles may be split into drafters (30-60-90 triangles).

Standard library only.  Exact integer geometry.

Coordinates.  A point is an integer pair (X, Y) standing for the Euclidean point
(X / 8, sqrt(3) * Y / 8).  Squared distance = (dX^2 + 3 dY^2) / 64.
The trihexagonal tiling used here has hexagons of side sqrt(3)/2 centred at the points
(8x + 4y, 4y) with x - y = 0 (mod 3); every other point (8x + 4y, 4y) of that form is
the centre of a triangle.  (This is the grid of the heesch-sat program, rescaled.)

The refined complex K: every hexagon is a face; every triangle is split into its six
drafters (centre, vertex, midpoint of an incident edge); hexagon edges are split at
their midpoints so that K is edge-to-edge.

Witness format (JSON):
  tile:   {"hexagons": [[X, Y], ...] (centres),
           "drafters": [[[X,Y],[X,Y],[X,Y]], ...] (corners of each drafter)}
  placements: [{"L": [[p, q], [r, s]], "den": d, "T": [TX, TY], "level": j}, ...]
     the isometry maps P to (L P) / d + T.
Checks (Basic 2021, Definition 1, with C_0 = the identity placement):
  * every placement is a Euclidean isometry mapping faces of K onto faces of K;
  * placed tiles have pairwise disjoint interiors (no shared faces);
  * for each i >= 1 every tile of C_i shares a boundary point with a tile of C_{i-1};
  * U_i = union of C_0..C_i is a closed topological disk (edge-connected, manifold
    at every vertex, Euler characteristic 1);
  * U_{i-1} lies in the interior of U_i (every face of K touching U_{i-1} is in U_i).
"""
import json
import sys
from collections import defaultdict


def is_hex_centre(P):
  X, Y = P
  if Y % 4 or (X - Y) % 8:
    return False
  y = Y // 4
  x = (X - 4 * y) // 8
  return (x - y) % 3 == 0


def is_cell_centre(P):
  X, Y = P
  return Y % 4 == 0 and (X - Y) % 8 == 0


HEX_OFF = [(3, 1), (0, 2), (-3, 1), (-3, -1), (0, -2), (3, -1)]   # in units of 2 -> x2 below


def hex_corners(C):
  X, Y = C
  return [(X + 2 * a, Y + 2 * b) for a, b in HEX_OFF]


def tri_corners(C):
  """Corners of the triangle centred at C (C a cell centre that is not a hexagon)."""
  X, Y = C
  # the three neighbouring hexagon centres at distance sqrt(3)... instead use geometry:
  # triangle vertices are at distance (side/sqrt3) = 1/2 from the centre, i.e. 2-norm 1/2:
  # candidate offsets with (dX^2 + 3dY^2)/64 = 1/4 -> dX^2 + 3 dY^2 = 16
  cands = [(4, 0), (-4, 0), (2, 2), (-2, 2), (2, -2), (-2, -2)]
  pts = [(X + a, Y + b) for a, b in cands]
  hexes = set()
  # vertices of the triangle are those candidate points that are hexagon corners
  out = []
  for p in pts:
    for hc in nearby_hex_centres(p):
      if p in hex_corners(hc):
        out.append(p)
        break
  assert len(out) == 3, (C, out)
  return out


def nearby_hex_centres(p):
  X, Y = p
  res = []
  for dy in range(-4, 5):
    for dx in range(-7, 8):
      Q = (X + dx, Y + dy)
      if (dx * dx + 3 * dy * dy) <= 48 and is_hex_centre(Q):
        res.append(Q)
  return res


def mid(a, b):
  s = (a[0] + b[0], a[1] + b[1])
  assert s[0] % 2 == 0 and s[1] % 2 == 0
  return (s[0] // 2, s[1] // 2)


def drafters_of(C):
  v = tri_corners(C)
  out = []
  for i in range(3):
    for j in range(3):
      if i != j:
        out.append(frozenset([C, v[i], mid(v[i], v[j])]))
  return out


class Complex:
  """Lazily generated refined complex K."""

  def __init__(self):
    self.faces_at = {}   # point -> list of faces (frozensets of corner points) of K
    self.cell_cache = {}

  def faces_of_cell(self, C):
    if C not in self.cell_cache:
      self.cell_cache[C] = self._faces_of_cell(C)
    return self.cell_cache[C]

  def _faces_of_cell(self, C):
    if is_hex_centre(C):
      cs = hex_corners(C)
      pts = []
      for i in range(6):
        pts.append(cs[i])
        pts.append(mid(cs[i], cs[(i + 1) % 6]))
      return [('H', C, tuple(pts))]
    return [('D', C, tuple(sorted(d))) for d in drafters_of(C)]

  def star(self, p):
    """All faces of K having p as a corner."""
    if p in self.faces_at:
      return self.faces_at[p]
    X, Y = p
    found = []
    for dy in range(-4, 5):
      for dx in range(-7, 8):
        C = (X + dx, Y + dy)
        if dx * dx + 3 * dy * dy > 48 or not is_cell_centre(C):
          continue
        for f in self.faces_of_cell(C):
          if p in f[2]:
            found.append(face_key(f))
    self.faces_at[p] = found
    return found


def face_key(f):
  kind, C, pts = f
  return (kind, C, frozenset(pts))


def face_edges(fk):
  kind, C, pts = fk
  # order the corners cyclically around the face centroid using exact angle comparison
  ordered = cyclic(list(pts))
  return [frozenset((ordered[i], ordered[(i + 1) % len(ordered)])) for i in range(len(ordered))]


def cyclic(pts):
  cx = sum(p[0] for p in pts)
  cy = sum(p[1] for p in pts)
  n = len(pts)

  def half(v):
    x, y = v
    return 0 if (y > 0 or (y == 0 and x > 0)) else 1

  import functools

  def cmp(a, b):
    va = (a[0] * n - cx, (a[1] * n - cy))
    vb = (b[0] * n - cx, (b[1] * n - cy))
    ha, hb = half(va), half(vb)
    if ha != hb:
      return ha - hb
    # cross product in Euclidean metric: x = X, y = sqrt3 Y -> sign of X_a Y_b - Y_a X_b
    cr = va[0] * vb[1] - va[1] * vb[0]
    return -1 if cr > 0 else (1 if cr < 0 else 0)
  return sorted(pts, key=functools.cmp_to_key(cmp))


def apply(iso, p):
  (a, b), (c, d) = iso['L']
  den = iso['den']
  X = a * p[0] + b * p[1]
  Y = c * p[0] + d * p[1]
  assert X % den == 0 and Y % den == 0, 'non-integral image'
  return (X // den + iso['T'][0], Y // den + iso['T'][1])


def check_isometry(iso):
  (a, b), (c, d) = iso['L']
  den = iso['den']
  # columns images of e1=(1,0), e2=(0,1); metric G = diag(1,3)
  # need L^T G L = den^2 G
  g11 = a * a + 3 * c * c
  g12 = a * b + 3 * c * d
  g22 = b * b + 3 * d * d
  return g11 == den * den and g12 == 0 and g22 == 3 * den * den


def main(path):
  W = json.load(open(path))
  K = Complex()
  tile_faces = set()
  for C in W['tile']['hexagons']:
    C = tuple(C)
    assert is_hex_centre(C), C
    tile_faces.add(face_key(K.faces_of_cell(C)[0]))
  for d in W['tile']['drafters']:
    pts = frozenset(tuple(p) for p in d)
    # locate it as a face of K
    C = min(pts, key=lambda p: 0)  # placeholder
    ok = False
    for p in pts:
      for fk in K.star(p):
        if fk[0] == 'D' and fk[2] == pts:
          tile_faces.add(fk)
          ok = True
          break
      if ok:
        break
    assert ok, ('drafter not a face of K', d)
  nh = sum(1 for f in tile_faces if f[0] == 'H')
  nd = sum(1 for f in tile_faces if f[0] == 'D')
  print(f'tile: {nh} hexagons, {nd} drafters (= {nd/6:.4f} triangles); balance t - 2h = {nd/6 - 2*nh:+.4f}')
  # tile itself must be a disk
  placed = []
  levels = []
  for pl in W['placements']:
    assert check_isometry(pl), ('not an isometry', pl)
    img = set()
    for fk in tile_faces:
      kind, C, pts = fk
      C2 = apply(pl, C)
      pts2 = frozenset(apply(pl, p) for p in pts)
      # must be a face of K
      hit = None
      for fk2 in K.star(next(iter(pts2))):
        if fk2[0] == kind and fk2[2] == pts2:
          hit = fk2
          break
      assert hit is not None, ('image is not a face of K', pl)
      img.add(hit)
    placed.append(frozenset(img))
    levels.append(pl['level'])
  k = max(levels)
  # centre
  centre = [i for i, l in enumerate(levels) if l == 0]
  assert len(centre) == 1, 'exactly one tile at level 0'
  assert placed[centre[0]] == frozenset(tile_faces), 'level-0 tile must be the tile itself'
  # disjointness
  owner = {}
  for i, faces in enumerate(placed):
    for f in faces:
      assert f not in owner, ('overlap', i, owner[f])
      owner[f] = i
  print(f'{len(placed)} placements, levels 0..{k}, no overlaps')
  pts_of = [set(p for f in faces for p in f[2]) for faces in placed]
  # contact condition
  for i, l in enumerate(levels):
    if l == 0:
      continue
    if not any(levels[j] == l - 1 and (pts_of[i] & pts_of[j]) for j in range(len(placed))):
      raise AssertionError(f'tile {i} at level {l} touches no tile of level {l-1}')
  print('contact condition ok')
  # unions
  for j in range(k + 1):
    Uj = set(f for i, faces in enumerate(placed) if levels[i] <= j for f in faces)
    check_disk(K, Uj, j)
    if j > 0:
      prev = set(f for i, faces in enumerate(placed) if levels[i] <= j - 1 for f in faces)
      pts = set(p for f in prev for p in f[2])
      for p in pts:
        for fk in K.star(p):
          if fk not in Uj:
            raise AssertionError(f'U_{j-1} not in interior of U_{j}: face {fk} at point {p}')
    print(f'U_{j}: closed disk, {len(Uj)} faces' + ('' if j == 0 else f'; contains U_{j-1} in its interior'))
  print(f'VERIFIED: the tile is surrounded {k} times (Heesch number >= {k})')


def check_disk(K, faces, j):
  faces = set(faces)
  V = set()
  E = defaultdict(int)
  for f in faces:
    for e in face_edges(f):
      E[e] += 1
    V |= set(f[2])
  F = len(faces)
  chi = len(V) - len(E) + F
  assert chi == 1, f'U_{j}: Euler characteristic {chi} != 1'
  # edge-connectedness
  edge_faces = defaultdict(list)
  for f in faces:
    for e in face_edges(f):
      edge_faces[e].append(f)
  start = next(iter(faces))
  seen = {start}
  stack = [start]
  while stack:
    f = stack.pop()
    for e in face_edges(f):
      for g in edge_faces[e]:
        if g not in seen:
          seen.add(g)
          stack.append(g)
  assert len(seen) == F, f'U_{j} not edge-connected'
  # manifold condition at each vertex: faces of U around p form one contiguous fan
  for p in V:
    star = K.star(p)
    inU = [f for f in star if f in faces]
    if len(inU) == len(star):
      continue
    # adjacency among inU faces through edges incident to p
    adj = defaultdict(set)
    for f in inU:
      for e in face_edges(f):
        if p in e:
          for g in edge_faces[e]:
            if g != f:
              adj[f].add(g)
    s0 = inU[0]
    comp = {s0}
    st = [s0]
    while st:
      f = st.pop()
      for g in adj[f]:
        if g not in comp:
          comp.add(g)
          st.append(g)
    assert len(comp) == len(inU), f'U_{j} pinched at {p}'
  # a connected surface with boundary, manifold at every vertex, chi = 1, in the plane
  # is a closed disk.


if __name__ == '__main__':
  if not __debug__:
    raise SystemExit('FAIL: verification requires Python assertions enabled')
  main(sys.argv[1])
