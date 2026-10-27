"""Solve the LP written by gen_snm (prefix.vars, prefix.ub) with HiGHS. Saves primal/dual."""
import sys, time, json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

pre = sys.argv[1]
t0 = time.time()
with open(pre + '.vars') as f:
  ncls, nvars = map(int, f.readline().split())
  classes = []
  for line in f:
    p = line.split()
    code, norb, cw = int(p[0]), int(p[1]), int(p[2])
    classes.append((code, norb, cw, list(map(int, p[3:3 + norb]))))
alpha = nvars
nv = nvars + 1
r, c, d = [], [], []
rows = 0
seen = set()
keep = []
with open(pre + '.ub') as f:
  for li, line in enumerate(f):
    p = line.split()
    entries = tuple(sorted((int(a), int(b)) for a, b in (x.split(':') for x in p[1:])))
    if entries in seen: continue
    seen.add(entries)
    keep.append(li)
    for a, b in entries:
      r.append(rows); c.append(a); d.append(b)
    rows += 1
import os
if len(sys.argv) > 2 and sys.argv[2] == 'mono':
  with open(pre + '.mono') as f:
    for line in f:
      p = line.split()
      for x in p[1:]:
        a, b = x.split(':'); r.append(rows); c.append(int(a)); d.append(int(b))
      rows += 1
Aub = coo_matrix((d, (r, c)), shape=(rows, nv)).tocsr()
er, ec, ed, beq = [], [], [], []
q = 0
var0 = 0
for code, norb, cw, sizes in classes:
  for o in range(norb):
    er.append(q); ec.append(var0 + o); ed.append(sizes[o])
  beq.append(1.0); q += 1
  if cw >= 0:
    er.append(q); ec.append(var0 + cw); ed.append(1); beq.append(1.0); q += 1
  var0 += norb
Aeq = coo_matrix((ed, (er, ec)), shape=(q, nv)).tocsr()
print(f'{pre}: {nv} vars, {rows} unique ub rows, {q} eq rows (load {time.time()-t0:.1f}s)', flush=True)
cvec = np.zeros(nv); cvec[alpha] = 1
res = linprog(cvec, A_ub=Aub, b_ub=np.zeros(rows), A_eq=Aeq, b_eq=np.array(beq), bounds=[(0, None)] * nv, method='highs')
print(res.status, res.message, flush=True)
from fractions import Fraction
print(f'{pre}: alpha* = {res.fun:.12f} ~ {Fraction(res.fun).limit_denominator(100000)} ({time.time()-t0:.1f}s)', flush=True)
np.save(pre + '_x.npy', res.x)
np.save(pre + '_keep.npy', np.array(keep))
np.save(pre + '_ineqdual.npy', res.ineqlin.marginals)
np.save(pre + '_eqdual.npy', res.eqlin.marginals)
