#!/usr/bin/env python3
"""Independent checker for corona witnesses of edge-marked polyhexes and polyominoes.

Standard library only, exact integer arithmetic.  Usage:
  python3 check_marked.py WITNESS.json [WITNESS.json ...]

Grids (cells are integer pairs):
  hex  axial coordinates; cell (q, r) has centre q*(1, 0) + r*(1/2, sqrt(3)/2);
       neighbour vectors NB = (1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1).
  sq   cell (x, y) is the unit square centred at (x, y);
       neighbour vectors NB = (1,0), (0,1), (-1,0), (0,-1).
An edge of a tile is a pair (cell, d) with cell + NB[d] outside the tile.  Each edge
carries a label: a string over {b, n, f} (one character per slot, listed in the
counter-clockwise direction of the owning tile).  Slot i on one side of a shared edge
faces slot m-1-i on the other side; facing slots must be b-n, n-b or f-f.  A reflected
copy lists its slots in reverse order.

Witness JSON: {"grid", "cells", "edges": [[cell, d], ...], "labels": [...],
               "placements": [{"M": [[a, b], [c, d]], "t": [x, y], "level": j}, ...]}
A placement maps a cell c to M c + t (M must be a symmetry of the lattice).

Checks (strict Heesch coronas, as in Kaplan 2022 and Basic 2021 Definition 1):
  1. every M is a lattice symmetry; the level-0 copy is the tile itself;
  2. copies have pairwise disjoint interiors (no shared cell);
  3. on every edge shared by two copies the labels are complementary;
  4. every copy of level i >= 1 shares a boundary point with a copy of level i - 1;
  5. U_i = union of copies of level <= i is a closed topological disk (edge-connected and
     Euler characteristic 1; for unions of closed cells this excludes holes and pinch
     points), and U_{i-1} lies in the interior of U_i (every cell sharing a point with
     U_{i-1} belongs to U_i);
  6. the marking is unbalanced (#bump slots != #nick slots), so by counting the
     realized tile cannot tile the plane.
"""
import json
import sys
from boundary import boundary_cycle

GRIDS = {
  'hex': [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)],
  'sq': [(1, 0), (0, 1), (-1, 0), (0, -1)],
}
CMP = {'b': 'n', 'n': 'b', 'f': 'f'}


def add(a, b):
  return (a[0] + b[0], a[1] + b[1])


def mat(M, v):
  return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def det(M):
  return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def bilinear(grid, u, v):
  if grid == 'hex':   # 2 <u, v> for the hexagonal metric q^2 + q r + r^2
    return 2 * u[0] * v[0] + u[0] * v[1] + u[1] * v[0] + 2 * u[1] * v[1]
  return u[0] * v[0] + u[1] * v[1]


def is_symmetry(grid, M):
  basis = [(1, 0), (0, 1)]
  return all(bilinear(grid, mat(M, u), mat(M, v)) == bilinear(grid, u, v) for u in basis for v in basis)


def corners(grid, c):
  """Corners of cell c as exact integer points (hex: scaled by 3, sq: scaled by 2), in cyclic order."""
  NB = GRIDS[grid]
  if grid == 'hex':
    return [(3 * c[0] + NB[i][0] + NB[(i + 1) % 6][0], 3 * c[1] + NB[i][1] + NB[(i + 1) % 6][1]) for i in range(6)]
  x, y = c
  return [(2 * x + 1, 2 * y + 1), (2 * x - 1, 2 * y + 1), (2 * x - 1, 2 * y - 1), (2 * x + 1, 2 * y - 1)]


def touching(grid, c):
  """Cells sharing at least one point with c."""
  if grid == 'hex':
    return [add(c, n) for n in GRIDS['hex']]
  return [(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


def euler(grid, cells):
  V, E = set(), set()
  for c in cells:
    vs = corners(grid, c)
    for i in range(len(vs)):
      V.add(vs[i])
      E.add(frozenset((vs[i], vs[(i + 1) % len(vs)])))
  return len(V) - len(E) + len(cells)


def edge_connected(grid, cells):
  cells = set(cells)
  start = next(iter(cells))
  seen, stack = {start}, [start]
  while stack:
    c = stack.pop()
    for n in GRIDS[grid]:
      d = add(c, n)
      if d in cells and d not in seen:
        seen.add(d)
        stack.append(d)
  return len(seen) == len(cells)


def compatible(x, y):
  m = len(x)
  return len(y) == m and all(y[m - 1 - i] == CMP[x[i]] for i in range(m))


def check(path):
  W = json.load(open(path))
  grid = W['grid']
  NB = GRIDS[grid]
  cells = [tuple(c) for c in W['cells']]
  cs = set(cells)
  assert len(cs) == len(cells) and all(type(x) is int for c in cells for x in c), 'bad or duplicate cells'
  assert len(W['edges']) == len(W['labels']), 'wrong label count'
  labels = {}
  for (c, d), l in zip(W['edges'], W['labels']):
    labels[(tuple(c), NB[d])] = l.lower()
  nedges = sum(1 for c in cells for n in NB if add(c, n) not in cs)
  assert len(labels) == nedges == len(W['edges']), 'every boundary edge must carry exactly one label'
  for (c, n) in labels:
    assert c in cs and add(c, n) not in cs, 'label on a non-boundary edge'
  assert edge_connected(grid, cells) and euler(grid, cells) == 1, 'tile must be a closed disk'
  boundary_cycle([corners(grid, c) for c in cells])
  slots = {len(l) for l in labels.values()}
  assert len(slots) == 1 and 0 not in slots and set(''.join(labels.values())) <= set('bnf'), 'bad labels'
  nb = sum(l.count('b') for l in labels.values())
  nn = sum(l.count('n') for l in labels.values())
  assert nb != nn, 'balanced marking: the counting argument does not apply'
  placed, levels = [], []
  for pl in W['placements']:
    M, t = pl['M'], tuple(pl['t'])
    assert all(type(x) is int for row in M for x in row) and all(type(x) is int for x in t), 'noninteger placement'
    assert type(pl['level']) is int and pl['level'] >= 0, 'invalid level'
    assert is_symmetry(grid, M), ('not a lattice symmetry', M)
    pc = {add(mat(M, c), t) for c in cells}
    pe = {}
    for (c, n), l in labels.items():
      pe[(add(mat(M, c), t), mat(M, n))] = l[::-1] if det(M) < 0 else l
    placed.append((pc, pe))
    levels.append(int(pl['level']))
  k = max(levels)
  zero = [i for i, l in enumerate(levels) if l == 0]
  assert len(zero) == 1 and placed[zero[0]][0] == cs and placed[zero[0]][1] == labels, 'level 0 must be the tile itself'
  owner = {}
  for i, (pc, _) in enumerate(placed):
    for c in pc:
      assert c not in owner, ('overlap at', c)
      owner[c] = i
  shared = 0
  for i, (pc, pe) in enumerate(placed):
    for (c, n), l in pe.items():
      d = add(c, n)
      if d in owner:
        l2 = placed[owner[d]][1][(d, (-n[0], -n[1]))]
        assert compatible(l, l2), ('incompatible labels', c, n, l, l2)
        shared += 1
  for i, l in enumerate(levels):
    if l > 0:
      assert any(d in owner and levels[owner[d]] == l - 1 for c in placed[i][0] for d in touching(grid, c)), \
        f'copy {i} (level {l}) does not touch level {l - 1}'
  sizes = []
  for j in range(k + 1):
    U = {c for c, i in owner.items() if levels[i] <= j}
    assert edge_connected(grid, U) and euler(grid, U) == 1, f'U_{j} is not a closed disk'
    boundary_cycle([corners(grid, c) for c in U])
    if j:
      for c in (c for c, i in owner.items() if levels[i] <= j - 1):
        for d in touching(grid, c):
          assert d in U, f'U_{j - 1} is not in the interior of U_{j}'
    sizes.append(len(U))
  return dict(grid=grid, cells=len(cells), edges=nedges, slots=slots.pop(), bumps=nb, nicks=nn,
              copies=len(placed), shared_edges=shared // 2, coronas=k, union_sizes=sizes)


def main(paths):
  for p in paths:
    r = check(p)
    print(f"VERIFIED {p}: {r['grid']} tile with {r['cells']} cells, imbalance {r['bumps'] - r['nicks']:+d}, "
          f"{r['copies']} copies, {r['coronas']} coronas (|U_j| = {r['union_sizes']})")


if __name__ == '__main__':
  if not __debug__:
    raise SystemExit('FAIL: verification requires Python assertions enabled')
  if not sys.argv[1:]:
    raise SystemExit('FAIL: at least one witness is required')
  main(sys.argv[1:])
