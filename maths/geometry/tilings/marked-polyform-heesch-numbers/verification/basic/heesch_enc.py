#!/usr/bin/env python3
"""SAT search for k-coronas of a tile on the trihex grid with drafter-refined triangles.

Placements are trihex grid symmetries (12 orientations x hexagon-lattice translations).
Encoding (k = number of coronas):
  u_p           placement p used
  e_{p,j}       p used at level j (exactly one level if used)
  c_{p,j}       p used at level <= j   (cumulative)
  a_{x,j}       atom x covered by a placement of level <= j
Constraints:
  centre placement at level 0, no other at level 0
  at most one used placement per atom (no overlaps)
  a_{x,j} <-> OR_{p ni x} c_{p,j}
  interior:  a_{x,j} -> a_{y,j+1} for every atom y touching x   (j < k)
  contact:   e_{p,j} -> OR_{y in halo(p)} a_{y,j-1}               (j >= 1)
Holes in any U_j are removed lazily (blocking clauses) after each model.
"""
import argparse, json, sys, time
from collections import defaultdict, deque

sys.path.insert(0, __import__('os').path.dirname(__file__))
import thd


def recentre(atoms):
  """Translate the tile by a hexagon-lattice vector so its centroid is near the origin."""
  sx = sy = 0
  for kind, X, Y in atoms:
    f = 3 if kind == 'H' else 1   # bring to 12x coordinates
    sx += X * f; sy += Y * f
  cx, cy = sx / (12 * len(atoms)), sy / (12 * len(atoms))
  best = None
  for x in range(int(cx) - 3, int(cx) + 4):
    for y in range(int(cy) - 3, int(cy) + 4):
      if (x - y) % 3 == 0:
        d = (x - cx) ** 2 + (x - cx) * (y - cy) + (y - cy) ** 2
        if best is None or d < best[0]:
          best = (d, (x, y))
  t = (-best[1][0], -best[1][1])
  return [thd.transform_atom(a, (1, 0, 0, 1), t) for a in atoms]


def norm2(v):
  return v[0] * v[0] + v[0] * v[1] + v[1] * v[1]


class Universe:
  def __init__(self, tile_atoms, radius2, reg=None):
    if reg is None:
      reg = int((radius2 ** 0.5) * 1.3) + 30
    thd.register_region(reg)
    self.tile = recentre(list(tile_atoms))
    plac = {}
    tr = []
    R = int(radius2 ** 0.5) + 2
    for x in range(-2 * R, 2 * R + 1):
      for y in range(-2 * R, 2 * R + 1):
        if (x - y) % 3 == 0 and norm2((x, y)) <= radius2:
          tr.append((x, y))
    tr.sort(key=norm2)
    for oi, o in enumerate(thd.ORIENTS):
      for t in tr:
        img = frozenset(thd.transform_atom(a, o, t) for a in self.tile)
        if img not in plac:
          plac[img] = (oi, t)
    self.atom_id = {}
    self.atoms = []
    self.placements = []   # list of tuple(atom ids)
    self.pinfo = []        # (orientation index, translation)
    for img, info in plac.items():
      ids = []
      for a in img:
        if a not in self.atom_id:
          self.atom_id[a] = len(self.atoms)
          self.atoms.append(a)
        ids.append(self.atom_id[a])
      self.placements.append(tuple(sorted(ids)))
      self.pinfo.append(info)
    ident = frozenset(self.tile)
    self.centre = list(plac.keys()).index(ident)
    # points and touching
    pt_atoms = defaultdict(list)
    self.corners = []
    for i, a in enumerate(self.atoms):
      cs = thd.atom_corners(a)
      self.corners.append(cs)
      for p in cs:
        pt_atoms[p].append(i)
    self.pt_atoms = pt_atoms
    self.touch = [set() for _ in self.atoms]
    for p, lst in pt_atoms.items():
      for i in lst:
        self.touch[i].update(lst)
    for i in range(len(self.atoms)):
      self.touch[i].discard(i)
    self.atom_plac = [[] for _ in self.atoms]
    for pi, ids in enumerate(self.placements):
      for i in ids:
        self.atom_plac[i].append(pi)
    # halo: atoms touching p (in universe) but not in p. Atoms touching p outside the
    # universe are added as phantom atoms that can never be covered.
    self.halo = []
    self.phantom = 0
    for pi, ids in enumerate(self.placements):
      s = set(ids)
      h = set()
      for i in ids:
        h |= self.touch[i]
      h -= s
      self.halo.append(tuple(sorted(h)))

  def edge_adjacent(self, i, j):
    ci, cj = self.corners[i], self.corners[j]
    common = set(ci) & set(cj)
    return len(common) >= 2


def all_touching_points_complete(U, ids):
  pass


class Encoder:
  def __init__(self, U, k, solver_name='cadical195'):
    from pysat.solvers import Solver
    self.U, self.k = U, k
    self.nv = 0
    self.S = Solver(name=solver_name)
    self.nclauses = 0
    P, A = len(U.placements), len(U.atoms)
    self.u = [self.new() for _ in range(P)]
    self.e = [[self.new() for _ in range(k + 1)] for _ in range(P)]
    self.c = [[self.new() for _ in range(k + 1)] for _ in range(P)]
    self.a = [[self.new() for _ in range(k + 1)] for _ in range(A)]
    add = self.add
    for p in range(P):
      # u <-> OR e ; at most one level
      add([-self.u[p]] + self.e[p])
      for j in range(k + 1):
        add([-self.e[p][j], self.u[p]])
      for j in range(k + 1):
        for jj in range(j + 1, k + 1):
          add([-self.e[p][j], -self.e[p][jj]])
      # cumulative
      for j in range(k + 1):
        add([-self.e[p][j], self.c[p][j]])
        prev = self.c[p][j - 1] if j > 0 else None
        if prev is not None:
          add([-prev, self.c[p][j]])
          add([-self.c[p][j], prev, self.e[p][j]])
        else:
          add([-self.c[p][j], self.e[p][j]])
    # centre
    add([self.e[U.centre][0]])
    for p in range(P):
      if p != U.centre:
        add([-self.e[p][0]])
    # at most one placement per atom (sequential counter)
    for x in range(A):
      self.amo([self.u[p] for p in U.atom_plac[x]])
    # atom coverage by level
    for x in range(A):
      for j in range(k + 1):
        lits = [self.c[p][j] for p in U.atom_plac[x]]
        add([-self.a[x][j]] + lits)
        for l in lits:
          add([-l, self.a[x][j]])
    # interior condition
    for x in range(A):
      for j in range(k):
        for y in U.touch[x]:
          if y < A:
            add([-self.a[x][j], self.a[y][j + 1]])
    # atoms touching the universe boundary: if a placement's atom touches a point whose
    # surrounding atoms are not all in the universe, it cannot be at level < k.
    full = self.boundary_safe()
    for x in range(A):
      if not full[x]:
        for j in range(k):
          add([-self.a[x][j]])
    # contact
    for p in range(P):
      for j in range(1, k + 1):
        add([-self.e[p][j]] + [self.a[y][j - 1] for y in U.halo[p]])

  def boundary_safe(self):
    """atom x is safe if every point of x has its full star inside the universe."""
    U = self.U
    out = []
    for x, cs in enumerate(U.corners):
      ok = True
      for p in cs:
        if len(U.pt_atoms[p]) < star_size(p, U):
          ok = False
          break
      out.append(ok)
    return out

  def new(self):
    self.nv += 1
    return self.nv

  def add(self, cl):
    self.S.add_clause(cl)
    self.nclauses += 1

  def amo(self, lits):
    n = len(lits)
    if n <= 1:
      return
    if n <= 6:
      for i in range(n):
        for j in range(i + 1, n):
          self.add([-lits[i], -lits[j]])
      return
    s = [self.new() for _ in range(n - 1)]
    self.add([-lits[0], s[0]])
    for i in range(1, n - 1):
      self.add([-lits[i], s[i]])
      self.add([-s[i - 1], s[i]])
      self.add([-lits[i], -s[i - 1]])
    self.add([-lits[n - 1], -s[n - 2]])

  def model_levels(self, m):
    ms = set(l for l in m if l > 0)
    lv = {}
    for p in range(len(self.U.placements)):
      if self.u[p] in ms:
        for j in range(self.k + 1):
          if self.e[p][j] in ms:
            lv[p] = j
    return lv


_STAR = {}


def star_size(p, U):
  """number of atoms around point p in the full (infinite) refined grid."""
  if p in _STAR:
    return _STAR[p]
  # compute from a local reconstruction: atoms of nearby trihex cells
  X, Y = p
  cx, cy = X // 4, Y // 4
  cnt = 0
  for x in range(cx - 2, cx + 3):
    for y in range(cy - 2, cy + 3):
      for a in thd.atoms_of_cell(x, y):
        if p in thd.atom_corners(a):
          cnt += 1
  _STAR[p] = cnt
  return cnt


def find_holes(U, used_atoms, rim):
  """Hole components (sets of atom ids) of the union of used atoms.  The complement is
  explored through edge-adjacency; a component reaching a rim atom (an atom whose
  neighbourhood is incomplete in the universe) or an atom farther out than every used
  atom is the outside."""
  used = set(used_atoms)
  rmax = max(norm4(U.atoms[x]) for x in used)
  cand = set()
  for x in used:
    for y in U.touch[x]:
      if y not in used:
        cand.add(y)
  seen = set()
  holes = []
  for s in cand:
    if s in seen:
      continue
    comp = {s}
    dq = deque([s])
    escaped = False
    while dq and not escaped:
      x = dq.popleft()
      if rim[x] or norm4(U.atoms[x]) > rmax:
        escaped = True
        break
      for y in U.touch[x]:
        if y in used or y in comp:
          continue
        if not U.edge_adjacent(x, y):
          continue
        comp.add(y)
        dq.append(y)
    seen |= comp
    if not escaped:
      holes.append(comp)
  return holes


def norm4(a):
  kind, X, Y = a
  s = 4 if kind == 'H' else 12
  # compare squared norms on a common scale (12x coordinates)
  f = 12 // s
  return norm2((X * f, Y * f))


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('tile_json')
  ap.add_argument('--k', type=int, required=True)
  ap.add_argument('--radius', type=float, required=True, help='translation radius (lattice norm)')
  ap.add_argument('--out', default=None)
  ns = ap.parse_args()
  tile = [tuple(a) for a in json.load(open(ns.tile_json))['atoms']]
  t0 = time.time()
  U = Universe(tile, ns.radius ** 2)
  print(f'placements {len(U.placements)} atoms {len(U.atoms)} ({time.time()-t0:.1f}s)', flush=True)
  E = Encoder(U, ns.k)
  print(f'vars {E.nv} clauses {E.nclauses} ({time.time()-t0:.1f}s)', flush=True)
  rim = [not ok for ok in E.boundary_safe()]
  it = 0
  while True:
    it += 1
    ok = E.S.solve()
    print(f'solve #{it}: {"SAT" if ok else "UNSAT"} ({time.time()-t0:.1f}s)', flush=True)
    if not ok:
      if ns.out:
        json.dump({'k': ns.k, 'result': 'UNSAT', 'radius': ns.radius}, open(ns.out, 'w'))
      return
    lv = E.model_levels(E.S.get_model())
    blocked = 0
    for j in range(ns.k + 1):
      atoms_j = [x for p, l in lv.items() if l <= j for x in U.placements[p]]
      for hole in find_holes(U, atoms_j, rim):
        bound = set()
        for x in hole:
          for y in U.touch[x]:
            for p in U.atom_plac[y]:
              if p in lv and lv[p] <= j and y in U.placements[p]:
                bound.add(p)
        h = next(iter(hole))
        E.add([-E.c[p][j] for p in sorted(bound)] + [E.a[h][j]])
        blocked += 1
    if blocked == 0:
      res = {'k': ns.k, 'result': 'SAT', 'radius': ns.radius,
             'placements': [{'orient': U.pinfo[p][0], 't': list(U.pinfo[p][1]), 'level': l}
                            for p, l in sorted(lv.items(), key=lambda r: r[1])]}
      print(f'found {ns.k}-corona with {len(lv)} tiles', flush=True)
      if ns.out:
        json.dump(res, open(ns.out, 'w'))
      return
    print(f'  blocked {blocked} holes', flush=True)


if __name__ == '__main__':
  main()
