#!/usr/bin/env python3
"""Recover Basic's published 6-corona patch from the Wikimedia SVG
(A_polygon_with_Heesch_number_6.svg) as exact grid placements."""
import re, sys, json, os
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
import thd, heesch_enc

svg = sys.argv[1]
out = sys.argv[2]
s = open(svg).read()
polys = re.findall(r'<polygon\s+class="(fil\d+)"\s+points="([^"]+)"', s)
left, right = defaultdict(list), defaultdict(list)
for cl, pts in polys:
  P = [tuple(map(float, p.split(','))) for p in pts.split()]
  cx = sum(p[0] for p in P) / len(P)
  (left if cx < 2860 else right)[cl].append(P)

def centre(P):
  return (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))

hexes = [centre(P) for lst in left.values() for P in lst if len(P) == 6]
o = min(hexes)
# basis: v1 horizontal neighbour (distance ~62), v2 at 60 degrees (y up => svg y negative)
d = sorted(((h[0] - o[0]) ** 2 + (h[1] - o[1]) ** 2, h) for h in hexes if h != o)
side = None
v1 = v2 = None
for dist2, h in d:
  v = (h[0] - o[0], h[1] - o[1])
  if v1 is None and abs(v[1]) < 5 and v[0] > 0:
    v1 = v
  if v2 is None and v[0] > 0 and v[1] < -5:
    v2 = v
  if v1 and v2:
    break
# refine: the horizontal lattice vector is a multiple of the true primitive one
m = round(v1[0] / (2 * v2[0]))
v1 = (v1[0] / m, 0.0)
print('basis', v1, v2)
# svg point -> thd lattice coordinates: p = o + a v1 + b v2 ; (a,b) -> a*(1,1) + b*(-1,2)
def fit(o, v1, v2, rad):
  import numpy as np
  det = v1[0] * v2[1] - v1[1] * v2[0]
  rows, rhs = [], []
  for h in hexes:
    x, y = h[0] - o[0], h[1] - o[1]
    a = (x * v2[1] - y * v2[0]) / det
    b = (v1[0] * y - v1[1] * x) / det
    if a * a + b * b > rad * rad:
      continue
    a, b = round(a), round(b)
    rows.append([1, 0, a, 0, b, 0]); rhs.append(h[0])
    rows.append([0, 1, 0, a, 0, b]); rhs.append(h[1])
  sol = np.linalg.lstsq(np.array(rows, float), np.array(rhs, float), rcond=None)[0]
  return (sol[0], sol[1]), (sol[2], sol[3]), (sol[4], sol[5])
for rad in (6, 15, 40, 1000):
  o, v1, v2 = fit(o, v1, v2, rad)
print('fitted basis', o, v1, v2)
det = v1[0] * v2[1] - v1[1] * v2[0]
def to_lat(p):
  x, y = p[0] - o[0], p[1] - o[1]
  a = (x * v2[1] - y * v2[0]) / det
  b = (v1[0] * y - v1[1] * x) / det
  return (a - b, a + 2 * b)

thd.register_region(120)
dkeys = list(thd.DRAFTER_CORNERS)
grid = defaultdict(list)
for k in dkeys:
  grid[(round(k[1] / 12), round(k[2] / 12))].append(k)

def snap_drafter(c):
  X, Y = 12 * c[0], 12 * c[1]
  best = None
  bx, by = round(c[0]), round(c[1])
  for gx in range(bx - 1, bx + 2):
    for gy in range(by - 1, by + 2):
      for k in grid[(gx, gy)]:
        dd = (k[1] - X) ** 2 + (k[1] - X) * (k[2] - Y) + (k[2] - Y) ** 2
        if best is None or dd < best[0]:
          best = (dd, k)
  return best

tiles = {}
maxerr = 0
for cl, lst in left.items():
  atoms = []
  for P in lst:
    c = to_lat(centre(P))
    if len(P) == 6:
      X, Y = round(4 * c[0]), round(4 * c[1])
      err = (4 * c[0] - X) ** 2 + (4 * c[1] - Y) ** 2
      assert (X % 4 == 0 and Y % 4 == 0 and ((X - Y) // 4) % 3 == 0), (cl, c)
      atoms.append(('H', X, Y))
    else:
      err, k = snap_drafter(c)
      err = err / 144.0
      atoms.append(k)
    maxerr = max(maxerr, err)
  tiles[cl] = atoms
print('tiles', len(tiles), 'max snap error (lattice units^2)', maxerr)

# identify each tile as an image of the base tile
base = heesch_enc.recentre([tuple(a) for a in json.load(open(sys.argv[3]))['atoms']])
bset = frozenset(base)
placements = {}
for cl, atoms in tiles.items():
  A = frozenset(atoms)
  hx = [a for a in atoms if a[0] == 'H']
  found = None
  for oi, orr in enumerate(thd.ORIENTS):
    img0 = [thd.transform_atom(a, orr, (0, 0)) for a in base]
    h0 = next(a for a in img0 if a[0] == 'H')
    for h in hx:
      t = ((h[1] - h0[1]) // 4, (h[2] - h0[2]) // 4)
      if frozenset(thd.transform_atom(a, orr, t) for a in base) == A:
        found = (oi, t)
        break
    if found:
      break
  assert found, ('tile not congruent to base', cl)
  placements[cl] = found
print('all 169 tiles are grid-aligned copies of the base tile')

# levels from the right figure: match by translated centroid
lc = {cl: centre([p for P in lst for p in P]) for cl, lst in left.items()}
rpolys = [(cl, centre(P)) for cl, lst in right.items() for P in lst]
# offset: right figure is the left one shifted; estimate by bounding boxes
lx = min(p[0] for lst in left.values() for P in lst for p in P); rx = min(p[0] for lst in right.values() for P in lst for p in P)
ly = min(p[1] for lst in left.values() for P in lst for p in P); ry = min(p[1] for lst in right.values() for P in lst for p in P)
off = (rx - lx, ry - ly)
print('offset', off)
# map each right polygon centre back, find which left tile contains a polygon with that centre
lcent = {}
for cl, lst in left.items():
  for P in lst:
    c = centre(P)
    lcent[(round(c[0]), round(c[1]))] = cl
rcls = sorted(right)
level_of = {}
votes = defaultdict(lambda: defaultdict(int))
for rcl, c in rpolys:
  key = (round(c[0] - off[0]), round(c[1] - off[1]))
  best = None
  for dx in range(-3, 4):
    for dy in range(-3, 4):
      if (key[0] + dx, key[1] + dy) in lcent:
        best = lcent[(key[0] + dx, key[1] + dy)]
        break
    if best:
      break
  if best:
    votes[best][rcl] += 1
# right classes ordered by size of the class (corona 0 smallest)
sizes = {rcl: sum(1 for c in rpolys if c[0] == rcl) for rcl in right}
order = sorted(right, key=lambda r: sizes[r])
lvl = {r: i for i, r in enumerate(order)}
for cl in tiles:
  if cl not in votes:
    raise SystemExit(f'no level for {cl}')
  r = max(votes[cl], key=votes[cl].get)
  level_of[cl] = lvl[r]
from collections import Counter
print('levels', sorted(Counter(level_of.values()).items()))
# re-express everything relative to the level-0 tile
c0 = next(cl for cl in tiles if level_of[cl] == 0)
oi0, t0 = placements[c0]
def matmul(o1, o2):
  a, b, d, e = o1; A, B, D, E = o2
  return (a * A + b * D, a * B + b * E, d * A + e * D, d * B + e * E)
inv = next(i for i, oo in enumerate(thd.ORIENTS) if matmul(oo, thd.ORIENTS[oi0]) == (1, 0, 0, 1))
for cl in tiles:
  A = [thd.transform_atom(thd.transform_atom(a, (1, 0, 0, 1), (-t0[0], -t0[1])), thd.ORIENTS[inv], (0, 0)) for a in tiles[cl]]
  tiles[cl] = A
  Aset = frozenset(A)
  found = None
  for oi, orr in enumerate(thd.ORIENTS):
    img0 = [thd.transform_atom(a, orr, (0, 0)) for a in base]
    h0 = next(a for a in img0 if a[0] == 'H')
    for h in [a for a in A if a[0] == 'H']:
      t = ((h[1] - h0[1]) // 4, (h[2] - h0[2]) // 4)
      if frozenset(thd.transform_atom(a, orr, t) for a in base) == Aset:
        found = (oi, t); break
    if found: break
  assert found
  placements[cl] = found
assert placements[c0] == (0, (0, 0)), placements[c0]
res = {'k': 6, 'result': 'SAT', 'source': 'Basic 2021 Fig. 2 (Wikimedia SVG)',
       'placements': [{'orient': placements[cl][0], 't': list(placements[cl][1]), 'level': level_of[cl]} for cl in tiles]}
json.dump(res, open(out, 'w'))
maxt = max((t[0] ** 2 + t[0] * t[1] + t[1] ** 2) ** 0.5 for (_, t) in placements.values())
print('max translation norm', maxt)
