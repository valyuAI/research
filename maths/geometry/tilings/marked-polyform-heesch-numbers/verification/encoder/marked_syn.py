#!/usr/bin/env python3
"""Synthesize an edge-marking of a fixed base polyform that admits k coronas, by SAT.

The base polyform's boundary edges receive labels from {B, N, F} (bump, nick, flat);
copies may meet along an edge only with complementary labels (B-N, N-B, F-F).
The marking is a SAT variable; a cardinality constraint fixes the imbalance
#B - #N = b0 != 0, which (by counting) rules out every tiling of the plane by
grid-aligned copies.  The solver looks for a marking together with k coronas
(Basic 2021, Definition 1, hole-free outermost union; holes are removed lazily).

usage: marked_syn.py GRID CELLS_JSON --k K --imb B0 [--out f.json] [--fix LABELS]
GRID: hex | sq
"""
import argparse, json, sys, time
from collections import deque


class HexGrid:
  name = 'hex'
  DIRS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
  ndir = 6

  def __init__(self):
    self.orients = []
    for s in range(2):
      for k in range(6):
        self.orients.append((s, k))

  def apply(self, o, c):
    s, k = o
    if s:
      c = (c[0] + c[1], -c[1])
    for _ in range(k):
      c = (-c[1], c[0] + c[1])
    return c

  def dmap(self, o):
    return [self.DIRS.index(self.apply(o, d)) for d in self.DIRS]

  def opp(self, d):
    return (d + 3) % 6

  def norm2(self, v):
    return v[0] * v[0] + v[0] * v[1] + v[1] * v[1]

  def touching(self, c):          # cells sharing a boundary point
    return [(c[0] + d[0], c[1] + d[1]) for d in self.DIRS]

  def edge_nbrs(self, c):
    return self.touching(c)


class SqGrid:
  name = 'sq'
  DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  ndir = 4

  def __init__(self):
    self.orients = [(s, k) for s in range(2) for k in range(4)]

  def apply(self, o, c):
    s, k = o
    if s:
      c = (c[0], -c[1])
    for _ in range(k):
      c = (-c[1], c[0])
    return c

  def dmap(self, o):
    return [self.DIRS.index(self.apply(o, d)) for d in self.DIRS]

  def opp(self, d):
    return (d + 2) % 4

  def norm2(self, v):
    return v[0] * v[0] + v[1] * v[1]

  def touching(self, c):
    return [(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]

  def edge_nbrs(self, c):
    return [(c[0] + d[0], c[1] + d[1]) for d in self.DIRS]


def add(a, b):
  return (a[0] + b[0], a[1] + b[1])


import itertools as _it
SLOTS = 1
def set_slots(m):
  global SLOTS, LAB, COMPSET, REFL, VAL
  SLOTS = m
  LAB = [''.join(t) for t in _it.product('bnf', repeat=m)]
  c = {'b': 'n', 'n': 'b', 'f': 'f'}
  # A's slot i faces B's slot m-1-i
  COMPSET = set()
  for x in LAB:
    y = ''.join(c[x[m - 1 - i]] for i in range(m))
    COMPSET.add((x, y))
  REFL = {x: x[::-1] for x in LAB}
  VAL = {x: x.count('b') - x.count('n') for x in LAB}
set_slots(1)
IMB_ATLEAST = False
UNMARKED = False
DIMACS = None


def build(G, cells, k, imb, radius, fix=None, solver='cadical195'):
  from pysat.solvers import Solver
  from pysat.card import CardEnc, EncType
  cells = [tuple(c) for c in cells]
  cs = set(cells)
  edges = [(c, d) for c in cells for d in range(G.ndir) if add(c, G.DIRS[d]) not in cs]
  eidx = {e: i for i, e in enumerate(edges)}
  R = int(radius) + 1
  trans = [(x, y) for x in range(-2 * R, 2 * R + 1) for y in range(-2 * R, 2 * R + 1) if G.norm2((x, y)) <= radius * radius]
  # placements: (orientation, translation) -> placed cells, and map placed edge -> prototile edge index
  P = []
  seenimg = {}
  for o in G.orients:
    dm = G.dmap(o)
    for t in trans:
      pc = tuple(sorted(add(G.apply(o, c), t) for c in cells))
      emap = {(add(G.apply(o, c), t), dm[d]): eidx[(c, d)] for (c, d) in edges}
      key = (pc, tuple(sorted(emap.items())))
      if key in seenimg:
        continue
      seenimg[key] = len(P)
      P.append((o, t, pc, emap))
  ident = [i for i, p in enumerate(P) if p[0] == G.orients[0] and p[1] == (0, 0)][0]
  cell_id = {}
  for p in P:
    for c in p[2]:
      cell_id.setdefault(c, len(cell_id))
  NC = len(cell_id)
  cell_pl = [[] for _ in range(NC)]
  for i, p in enumerate(P):
    for c in p[2]:
      cell_pl[cell_id[c]].append(i)
  rim = [any(n not in cell_id for n in G.touching(c)) for c in cell_id]
  S = Solver(name=solver)
  nv = [0]
  def new():
    nv[0] += 1
    return nv[0]
  ncl = [0]
  dfile = open(DIMACS + '.body', 'w') if DIMACS else None
  def addc(cl):
    S.add_clause(cl); ncl[0] += 1
    if dfile is not None:
      dfile.write(' '.join(map(str, cl)) + ' 0\n')
  NP = len(P)
  # label variables
  NL = len(LAB)
  L = [[new() for _ in LAB] for _ in edges]
  for e in range(len(edges)):
    addc(L[e][:])
    card = CardEnc.atmost(lits=L[e][:], bound=1, top_id=nv[0], encoding=EncType.pairwise)
    for cl in card.clauses:
      addc(cl)
  if fix:
    for e, l in enumerate(fix.split(',')):
      addc([L[e][LAB.index(l)]])
  # imbalance: sum over slots of [bump] - [nick] = imb, via slot indicator variables
  slotb, slotn = [], []
  for e in range(len(edges)):
    for i in range(SLOTS):
      vb, vn = new(), new()
      Lb = [L[e][j] for j, x in enumerate(LAB) if x[i] == 'b']
      Ln = [L[e][j] for j, x in enumerate(LAB) if x[i] == 'n']
      addc([-vb] + Lb)
      for l in Lb:
        addc([-l, vb])
      addc([-vn] + Ln)
      for l in Ln:
        addc([-l, vn])
      slotb.append(vb); slotn.append(vn)
  lits = slotb + [-v for v in slotn]
  if UNMARKED:
    for e in range(len(edges)):
      addc([L[e][LAB.index('f' * SLOTS)]])
  elif IMB_ATLEAST:
    card = CardEnc.atleast(lits=lits, bound=imb + len(slotn), top_id=nv[0], encoding=EncType.seqcounter)
  else:
    card = CardEnc.equals(lits=lits, bound=imb + len(slotn), top_id=nv[0], encoding=EncType.seqcounter)
  if not UNMARKED:
    nv[0] = max(nv[0], card.nv)
    for cl in card.clauses:
      addc(cl)
  u = [new() for _ in range(NP)]
  e = [[new() for _ in range(k + 1)] for _ in range(NP)]
  cm = [[new() for _ in range(k + 1)] for _ in range(NP)]
  a = [[new() for _ in range(k + 1)] for _ in range(NC)]
  for p in range(NP):
    addc([-u[p]] + e[p])
    for j in range(k + 1):
      addc([-e[p][j], u[p]])
      for jj in range(j + 1, k + 1):
        addc([-e[p][j], -e[p][jj]])
      addc([-e[p][j], cm[p][j]])
      if j > 0:
        addc([-cm[p][j - 1], cm[p][j]])
        addc([-cm[p][j], cm[p][j - 1], e[p][j]])
      else:
        addc([-cm[p][j], e[p][j]])
  addc([e[ident][0]])
  for p in range(NP):
    if p != ident:
      addc([-e[p][0]])
  for x in range(NC):
    ls = [u[p] for p in cell_pl[x]]
    if len(ls) > 1:
      card = CardEnc.atmost(lits=ls, bound=1, top_id=nv[0], encoding=EncType.seqcounter)
      nv[0] = max(nv[0], card.nv)
      for cl in card.clauses:
        addc(cl)
  for x in range(NC):
    for j in range(k + 1):
      ls = [cm[p][j] for p in cell_pl[x]]
      addc([-a[x][j]] + ls)
      for l in ls:
        addc([-l, a[x][j]])
  cells_list = list(cell_id)
  for c, x in cell_id.items():
    for j in range(k):
      if rim[x]:
        addc([-a[x][j]])
        continue
      for n in G.touching(c):
        addc([-a[x][j], a[cell_id[n]][j + 1]])
  for p in range(NP):
    pcs = set(P[p][2])
    halo = set()
    for c in pcs:
      for n in G.touching(c):
        if n not in pcs and n in cell_id:
          halo.add(cell_id[n])
    for j in range(1, k + 1):
      addc([-e[p][j]] + [a[y][j - 1] for y in sorted(halo)])
  # compatibility
  owner = {}
  for p, (o, t, pc, emap) in enumerate(P):
    for ed, ei in emap.items():
      owner.setdefault(ed, []).append((p, ei))
  def eff(o, x):
    return REFL[x] if o[0] else x
  # effective label variables per directed edge position
  Y = {}
  def yv(pos, x):
    key = (pos, x)
    if key not in Y:
      Y[key] = new()
    return Y[key]
  for p, (o, t, pc, emap) in enumerate(P):
    for pos, ei in emap.items():
      for i1, x in enumerate(LAB):
        addc([-u[p], -L[ei][i1], yv(pos, eff(o, x))])
  done = set()
  for (pos, x) in list(Y):
    c, d = pos
    opp = (add(c, G.DIRS[d]), G.opp(d))
    if (opp, pos) in done:
      continue
    done.add((pos, opp))
    for y in LAB:
      if (opp, y) in Y and (x, y) not in COMPSET:
        addc([-Y[(pos, x)], -Y[(opp, y)]])
  return dict(dfile=dfile, S=S, P=P, cell_id=cell_id, rim=rim, u=u, e=e, cm=cm, a=a, L=L, edges=edges, k=k,
              ident=ident, nv=nv[0], ncl=ncl[0], G=G)


def holes(G, used, cell_id, rim):
  rmax = max(G.norm2(c) for c in used)
  cand = set()
  for c in used:
    for n in G.edge_nbrs(c):
      if n not in used:
        cand.add(n)
  seen, out = set(), []
  for s in cand:
    if s in seen:
      continue
    comp = {s}
    dq = deque([s])
    esc = False
    while dq:
      x = dq.popleft()
      if x not in cell_id or rim[cell_id[x]] or G.norm2(x) > rmax:
        esc = True
        break
      for y in G.edge_nbrs(x):
        if y not in used and y not in comp:
          comp.add(y)
          dq.append(y)
    seen |= comp
    if not esc:
      out.append(comp)
  return out


def solve(F, log=print):
  S, P, k = F['S'], F['P'], F['k']
  G = F['G']
  it = 0
  t0 = time.time()
  while True:
    it += 1
    ok = S.solve()
    if not ok:
      return None
    m = set(l for l in S.get_model() if l > 0)
    lv = {}
    for p in range(len(P)):
      if F['u'][p] in m:
        lv[p] = next(j for j in range(k + 1) if F['e'][p][j] in m)
    blocked = 0
    for j in range(k + 1):
      used = set(c for p, l in lv.items() if l <= j for c in P[p][2])
      for hole in holes(G, used, F['cell_id'], F['rim']):
        bound = set(p for p, l in lv.items() if l <= j and any(n in hole for c in P[p][2] for n in G.touching(c)))
        h = next(iter(hole))
        cl = [-F['cm'][p][j] for p in sorted(bound)] + [F['a'][F['cell_id'][h]][j]]
        F['S'].add_clause(cl)
        F['nblock'] = F.get('nblock', 0) + 1
        if F.get('dfile') is not None:
          F['dfile'].write(' '.join(map(str, cl)) + ' 0\n')
        blocked += 1
    if not blocked:
      labels = ','.join(next(LAB[i] for i in range(len(LAB)) if F['L'][ei][i] in m) for ei in range(len(F['edges'])))
      return {'labels': labels, 'placements': [{'o': list(P[p][0]), 't': list(P[p][1]), 'level': l} for p, l in sorted(lv.items(), key=lambda r: r[1])]}


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('grid')
  ap.add_argument('cells')
  ap.add_argument('--k', type=int, required=True)
  ap.add_argument('--imb', type=int, required=True)
  ap.add_argument('--radius', type=float, default=None)
  ap.add_argument('--fix', default=None)
  ap.add_argument('--rfac', type=float, default=1.0)
  ap.add_argument('--slots', type=int, default=1)
  ap.add_argument('--atleast', action='store_true', help='imbalance >= imb instead of == imb')
  ap.add_argument('--dimacs', default=None, help='write the final CNF (with blocking clauses) here')
  ap.add_argument('--out', default=None)
  ap.add_argument('--unmarked', action='store_true', help='validation mode: all edges flat, no imbalance constraint')
  ap.add_argument('--cnf-only', action='store_true', help='write the base CNF to --dimacs and exit without solving')
  ns = ap.parse_args()
  set_slots(ns.slots)
  global IMB_ATLEAST, DIMACS, UNMARKED
  IMB_ATLEAST = ns.atleast
  UNMARKED = ns.unmarked
  DIMACS = ns.dimacs
  G = HexGrid() if ns.grid == 'hex' else SqGrid()
  cells = json.loads(ns.cells)
  diam = max(G.norm2((a[0] - b[0], a[1] - b[1])) for a in cells for b in cells) ** 0.5
  step = diam + (1.0 if ns.grid == "hex" else 2 ** 0.5)  # max distance between touching cells
  rad = ns.radius if ns.radius else ns.rfac * ns.k * step + 2 * diam + 2
  t0 = time.time()
  F = build(G, cells, ns.k, ns.imb, rad, fix=ns.fix)
  print(f'{ns.grid} cells={cells} k={ns.k} imb={ns.imb} radius={rad:.1f}: placements {len(F["P"])} vars {F["nv"]} clauses {F["ncl"]} ({time.time()-t0:.1f}s)', flush=True)
  if ns.cnf_only:
    F['dfile'].close()
    with open(ns.dimacs, 'w') as fo:
      fo.write(f'p cnf {F["nv"]} {F["ncl"]}\n')
      with open(ns.dimacs + '.body') as fi:
        for ln in fi:
          fo.write(ln)
    __import__('os').remove(ns.dimacs + '.body')
    meta = {'grid': ns.grid, 'cells': cells, 'k': ns.k, 'imb': ns.imb, 'atleast': ns.atleast, 'slots': ns.slots, 'radius': rad,
            'nvars': F['nv'], 'nclauses': F['ncl'], 'edges': [[list(c), d] for c, d in F['edges']],
            'L': F['L'], 'u_count': len(F['P'])}
    json.dump(meta, open(ns.dimacs + '.meta.json', 'w'))
    print(f'wrote {ns.dimacs}', flush=True)
    return
  res = solve(F)
  dt = time.time() - t0
  if F.get('dfile') is not None:
    F['dfile'].close()
    nvars = F['S'].nof_vars()
    ncls = F['ncl'] + F.get('nblock', 0)
    with open(ns.dimacs, 'w') as fo:
      fo.write(f'p cnf {nvars} {ncls}\n')
      with open(ns.dimacs + '.body') as fi:
        for ln in fi:
          fo.write(ln)
    __import__('os').remove(ns.dimacs + '.body')
  if res is None:
    print(f'UNSAT ({dt:.1f}s)', flush=True)
    out = {'result': 'UNSAT'}
  else:
    print(f'SAT labels={res["labels"]} tiles={len(res["placements"])} ({dt:.1f}s)', flush=True)
    out = {'result': 'SAT', **res}
  out.update({'atleast': ns.atleast, 'slots': ns.slots, 'rigorous_radius': ns.rfac >= 1.0 and not ns.radius, 'grid': ns.grid, 'cells': cells, 'k': ns.k, 'imb': ns.imb, 'radius': rad,
              'edges': [[list(c), d] for c, d in F['edges']]})
  if ns.out:
    json.dump(out, open(ns.out, 'w'))


if __name__ == '__main__':
  main()
