#!/usr/bin/env python3
"""Second, generic implementation: SAT synthesis of an edge marking of a base polyform
admitting k coronas, for grids given by vertex polygons (hexagonal, square, triangular).

Cells are tuples of lattice vertices; edges are unordered vertex pairs; two cells touch
iff they share a vertex; they are edge-adjacent iff they share an edge.  Placements are
x -> M x + t with M in the point group of the grid and t in its translation lattice.
Labels: slots in {b, n, f}; slot i of one side faces slot m-1-i of the other side;
reflections reverse the slot order.  #bump slots - #nick slots = imb (nonzero).

usage: marked_gen.py GRID CELLS_JSON --k K --imb B [--slots m] [--rfac f] [--out f]
GRID: tri (cells given as [a, b, s], s=0 up, s=1 down), hex, sq (cells [x, y]).
"""
import argparse, itertools, json, math, sys, time
from collections import deque


ATLEAST = False


def hexform(v):
  return v[0] * v[0] + v[0] * v[1] + v[1] * v[1]


class Grid:
  def __init__(self, kind):
    self.kind = kind
    if kind in ('tri', 'hex'):
      R = ((0, -1), (1, 1))        # 60 degree rotation: (x, y) -> (-y, x + y)
      F = ((1, 1), (0, -1))        # reflection: (x, y) -> (x + y, -y)
      self.form = hexform
      nrot = 6
    else:
      R = ((0, -1), (1, 0))
      F = ((1, 0), (0, -1))
      self.form = lambda v: v[0] * v[0] + v[1] * v[1]
      nrot = 4
    self.mats = []
    for s in range(2):
      for k in range(nrot):
        M = ((1, 0), (0, 1))
        if s:
          M = F
        for _ in range(k):
          M = mul(R, M)
        self.mats.append((M, s))

  def cell_vertices(self, c):
    if self.kind == 'tri':
      a, b, s = c
      if s == 0:
        return ((a, b), (a + 1, b), (a, b + 1))
      return ((a + 1, b), (a + 1, b + 1), (a, b + 1))
    if self.kind == 'sq':
      x, y = c
      return ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1))
    # hex: cell (q, r) -> corners in 3x coordinates (3c + n_i + n_{i+1})
    q, r = c
    NB = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    return tuple((3 * q + NB[i][0] + NB[(i + 1) % 6][0], 3 * r + NB[i][1] + NB[(i + 1) % 6][1]) for i in range(6))

  def vscale(self):
    return 3 if self.kind == 'hex' else 1


def mul(A, B):
  return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def ap(M, v):
  return (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])


def build(G, base_cells, k, imb, radius, slots, solver='cadical195'):
  from pysat.solvers import Solver
  from pysat.card import CardEnc, EncType
  LAB = [''.join(t) for t in itertools.product('bnf', repeat=slots)]
  cmap = {'b': 'n', 'n': 'b', 'f': 'f'}
  COMP = set((x, ''.join(cmap[x[slots - 1 - i]] for i in range(slots))) for x in LAB)
  sc = G.vscale()
  tile = [G.cell_vertices(c) for c in base_cells]          # polygons, cyclic CCW
  # boundary edges of the tile, with CCW orientation (u -> v)
  cnt = {}
  for poly in tile:
    for i in range(len(poly)):
      e = frozenset((poly[i], poly[(i + 1) % len(poly)]))
      cnt[e] = cnt.get(e, 0) + 1
  bedges = []
  for poly in tile:
    for i in range(len(poly)):
      u, v = poly[i], poly[(i + 1) % len(poly)]
      if cnt[frozenset((u, v))] == 1:
        bedges.append((u, v))
  NE = len(bedges)
  R = int(radius) + 2
  trans = [(x, y) for x in range(-2 * R, 2 * R + 1) for y in range(-2 * R, 2 * R + 1) if G.form((x, y)) <= radius * radius]
  P = []
  seen = set()
  for M, s in G.mats:
    for t in trans:
      T = (sc * t[0], sc * t[1])
      img = lambda v: (ap(M, v)[0] + T[0], ap(M, v)[1] + T[1])
      cells = frozenset(frozenset(img(v) for v in poly) for poly in tile)
      emap = {}
      for ei, (u, v) in enumerate(bedges):
        emap[frozenset((img(u), img(v)))] = (ei, s)
      key = (cells, frozenset((e, a) for e, a in emap.items()))
      if key in seen:
        continue
      seen.add(key)
      P.append((M, t, cells, emap))
  ident = next(i for i, p in enumerate(P) if p[0] == ((1, 0), (0, 1)) and p[1] == (0, 0))
  cid = {}
  for p in P:
    for c in p[2]:
      cid.setdefault(c, len(cid))
  NC = len(cid)
  cpl = [[] for _ in range(NC)]
  for i, p in enumerate(P):
    for c in p[2]:
      cpl[cid[c]].append(i)
  # touching via shared vertices, edge adjacency via shared edges
  vcells = {}
  ecells = {}
  for c, i in cid.items():
    vs = list(c)
    for v in vs:
      vcells.setdefault(v, []).append(i)
  cells_by_id = list(cid)
  for c, i in cid.items():
    poly = cyc(G, c)
    for j in range(len(poly)):
      ecells.setdefault(frozenset((poly[j], poly[(j + 1) % len(poly)])), []).append(i)
  # star sizes (number of cells around a vertex in the full grid)
  star = {'tri': 6, 'sq': 4, 'hex': 3}[G.kind]
  touch = [set() for _ in range(NC)]
  rim = [False] * NC
  for v, lst in vcells.items():
    full = len(lst) == star
    for i in lst:
      touch[i].update(lst)
      if not full:
        rim[i] = True
  for i in range(NC):
    touch[i].discard(i)
  enb = [set() for _ in range(NC)]
  for e, lst in ecells.items():
    for i in lst:
      enb[i].update(lst)
  for i in range(NC):
    enb[i].discard(i)
  S = Solver(name=solver)
  nv = [0]
  def new():
    nv[0] += 1
    return nv[0]
  ncl = [0]
  def addc(cl):
    S.add_clause(cl); ncl[0] += 1
  L = [[new() for _ in LAB] for _ in range(NE)]
  for e in range(NE):
    addc(L[e][:])
    for i in range(len(LAB)):
      for j in range(i + 1, len(LAB)):
        addc([-L[e][i], -L[e][j]])
  sb, sn = [], []
  for e in range(NE):
    for i in range(slots):
      vb, vn = new(), new()
      Lb = [L[e][j] for j, x in enumerate(LAB) if x[i] == 'b']
      Ln = [L[e][j] for j, x in enumerate(LAB) if x[i] == 'n']
      addc([-vb] + Lb); addc([-vn] + Ln)
      for l in Lb: addc([-l, vb])
      for l in Ln: addc([-l, vn])
      sb.append(vb); sn.append(vn)
  enc = CardEnc.atleast if ATLEAST else CardEnc.equals
  card = enc(lits=sb + [-v for v in sn], bound=imb + len(sn), top_id=nv[0], encoding=EncType.seqcounter)
  nv[0] = max(nv[0], card.nv)
  for cl in card.clauses: addc(cl)
  NP = len(P)
  u = [new() for _ in range(NP)]
  lev = [[new() for _ in range(k + 1)] for _ in range(NP)]
  cm = [[new() for _ in range(k + 1)] for _ in range(NP)]
  A = [[new() for _ in range(k + 1)] for _ in range(NC)]
  for p in range(NP):
    addc([-u[p]] + lev[p])
    for j in range(k + 1):
      addc([-lev[p][j], u[p]])
      for jj in range(j + 1, k + 1):
        addc([-lev[p][j], -lev[p][jj]])
      addc([-lev[p][j], cm[p][j]])
      if j:
        addc([-cm[p][j - 1], cm[p][j]]); addc([-cm[p][j], cm[p][j - 1], lev[p][j]])
      else:
        addc([-cm[p][j], lev[p][j]])
  addc([lev[ident][0]])
  for p in range(NP):
    if p != ident:
      addc([-lev[p][0]])
  for x in range(NC):
    ls = [u[p] for p in cpl[x]]
    if len(ls) > 1:
      card = CardEnc.atmost(lits=ls, bound=1, top_id=nv[0], encoding=EncType.seqcounter)
      nv[0] = max(nv[0], card.nv)
      for cl in card.clauses: addc(cl)
    for j in range(k + 1):
      ls = [cm[p][j] for p in cpl[x]]
      addc([-A[x][j]] + ls)
      for l in ls: addc([-l, A[x][j]])
  for x in range(NC):
    for j in range(k):
      if rim[x]:
        addc([-A[x][j]])
      else:
        for y in touch[x]:
          addc([-A[x][j], A[y][j + 1]])
  for p in range(NP):
    pc = set(cid[c] for c in P[p][2])
    halo = set()
    for x in pc:
      halo |= touch[x]
    halo -= pc
    for j in range(1, k + 1):
      addc([-lev[p][j]] + [A[y][j - 1] for y in sorted(halo)])
  # labels on placed edges: placed edge e (vertex pair) of placement p carries
  # effective label refl^s(L_ei); its slot order is relative to p's CCW direction.
  Y = {}
  def yv(e, side, x):
    key = (e, side, x)
    if key not in Y:
      Y[key] = new()
    return Y[key]
  # side of an edge = the cell (id) it belongs to
  for p, (M, t, cells, emap) in enumerate(P):
    cellof = {}
    for c in cells:
      poly = cyc(G, c)
      for j in range(len(poly)):
        cellof[frozenset((poly[j], poly[(j + 1) % len(poly)]))] = cid[c]
    for e, (ei, s) in emap.items():
      for i1, x in enumerate(LAB):
        addc([-u[p], -L[ei][i1], yv(e, cellof[e], x[::-1] if s else x)])
  bykey = {}
  for (e, side, x), var in Y.items():
    bykey.setdefault(e, {}).setdefault(side, {})[x] = var
  for e, sides in bykey.items():
    if len(sides) < 2:
      continue
    (s1, d1), (s2, d2) = list(sides.items())
    for x, v1 in d1.items():
      for y, v2 in d2.items():
        if (x, y) not in COMP:
          addc([-v1, -v2])
  return dict(S=S, P=P, cid=cid, cells_by_id=cells_by_id, rim=rim, enb=enb, touch=touch, u=u, lev=lev, cm=cm, A=A, L=L,
              LAB=LAB, k=k, NE=NE, nv=nv[0], ncl=ncl[0], bedges=bedges)


def cyc(G, c):
  """cyclic (CCW) order of a cell's vertices (cells are frozensets)."""
  vs = list(c)
  cx = sum(v[0] for v in vs) / len(vs)
  cy = sum(v[1] for v in vs) / len(vs)
  if G.kind in ('tri', 'hex'):
    key = lambda v: math.atan2((v[1] - cy) * math.sqrt(3) / 2, (v[0] - cx) + (v[1] - cy) / 2)
  else:
    key = lambda v: math.atan2(v[1] - cy, v[0] - cx)
  return sorted(vs, key=key)


def solve(F):
  S, P, k = F['S'], F['P'], F['k']
  while True:
    if not S.solve():
      return None
    m = set(l for l in S.get_model() if l > 0)
    lv = {p: next(j for j in range(k + 1) if F['lev'][p][j] in m) for p in range(len(P)) if F['u'][p] in m}
    blocked = 0
    for j in range(k + 1):
      used = set(F['cid'][c] for p, l in lv.items() if l <= j for c in P[p][2])
      for hole in holes(F, used):
        bound = set(p for p, l in lv.items() if l <= j and any(y in hole for c in P[p][2] for y in F['touch'][F['cid'][c]]))
        h = next(iter(hole))
        S.add_clause([-F['cm'][p][j] for p in sorted(bound)] + [F['A'][h][j]])
        blocked += 1
    if not blocked:
      labs = [next(x for i, x in enumerate(F['LAB']) if F['L'][e][i] in m) for e in range(F['NE'])]
      return labs, lv


def holes(F, used):
  cand = set()
  for x in used:
    cand |= F['enb'][x]
  cand -= used
  seen, out = set(), []
  for s in cand:
    if s in seen:
      continue
    comp, dq, esc = {s}, deque([s]), False
    while dq:
      x = dq.popleft()
      if F['rim'][x]:
        esc = True
        break
      for y in F['enb'][x]:
        if y not in used and y not in comp:
          comp.add(y); dq.append(y)
      if len(comp) > 5000:
        esc = True
        break
    seen |= comp
    if not esc:
      out.append(comp)
  return out


def main():
  ap_ = argparse.ArgumentParser()
  ap_.add_argument('grid'); ap_.add_argument('cells')
  ap_.add_argument('--k', type=int, required=True); ap_.add_argument('--imb', type=int, required=True)
  ap_.add_argument('--slots', type=int, default=1); ap_.add_argument('--rfac', type=float, default=1.0)
  ap_.add_argument('--out', default=None)
  ap_.add_argument('--atleast', action='store_true')
  ns = ap_.parse_args()
  global ATLEAST
  ATLEAST = ns.atleast
  G = Grid(ns.grid)
  cells = [tuple(c) for c in json.loads(ns.cells)]
  sc = G.vscale()
  # diameter in lattice units: max distance between cell centroids (+1 slack)
  cents = []
  for c in cells:
    vs = G.cell_vertices(c)
    cents.append((sum(v[0] for v in vs) / len(vs) / sc, sum(v[1] for v in vs) / len(vs) / sc))
  diam = max(math.sqrt(G.form((a[0] - b[0], a[1] - b[1]))) for a in cents for b in cents) + 1.0
  rmax = max(math.sqrt(G.form(c)) for c in cents) + 1.0
  rad = ns.rfac * ns.k * (diam + 1) + 2 * rmax + 2
  t0 = time.time()
  F = build(G, cells, ns.k, ns.imb, rad, ns.slots)
  print(f'{ns.grid} cells={json.dumps([list(c) for c in cells])} k={ns.k} imb={ns.imb} slots={ns.slots} radius={rad:.1f}: placements {len(F["P"])} clauses {F["ncl"]} ({time.time()-t0:.1f}s)', flush=True)
  r = solve(F)
  if r is None:
    print(f'UNSAT ({time.time()-t0:.1f}s)', flush=True)
    out = {'result': 'UNSAT'}
  else:
    labs, lv = r
    print(f'SAT labels={",".join(labs)} tiles={len(lv)} ({time.time()-t0:.1f}s)', flush=True)
    out = {'result': 'SAT', 'labels': labs,
           'placements': [{'M': [list(F['P'][p][0][0]), list(F['P'][p][0][1])], 't': list(F['P'][p][1]), 'level': l} for p, l in sorted(lv.items(), key=lambda r: r[1])]}
  out.update({'atleast': ns.atleast, 'grid': ns.grid, 'cells': [list(c) for c in cells], 'k': ns.k, 'imb': ns.imb, 'slots': ns.slots, 'radius': rad,
              'rigorous_radius': ns.rfac >= 1.0, 'bedges': [[list(u), list(v)] for u, v in F['bedges']]})
  if ns.out:
    json.dump(out, open(ns.out, 'w'))


if __name__ == '__main__':
  main()
