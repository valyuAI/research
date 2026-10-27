"""Step 2 of facial-reduction exactification.
From a relative-interior point x (facial.py) of the face {rule : all rows <= alpha}:
  Z = variables with x < ztol (forced zero), E = rows with slack < stol (implicit equalities).
  x0 = rational rounding (denominator D) of x off Z, CW classes exact.
  Correct exactly: on the classes touched by E, solve the least-norm correction so that every row in E
  equals alpha and every touched class is normalised; untouched classes are rescaled exactly.
  Then check every row, nonnegativity, normalisation and CW exactly.
usage: exactify.py prefix alpha_num alpha_den [D=1000] [ztol=1e-9] [stol=1e-9] [mono] [tcc]
  mono: monotonicity rows (prefix.mono, right-hand side 0) are included, as in facial.py
  tcc:  read the interior point computed with top-cycle consistency (zeros are then in Z)"""
import sys, time, pickle
import numpy as np
from fractions import Fraction
import flint
from tcc_util import tcc_zero_vars, NCLASSES

pre = sys.argv[1]; alpha = Fraction(int(sys.argv[2]), int(sys.argv[3]))
D = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
ztol = float(sys.argv[5]) if len(sys.argv) > 5 else 1e-9
stol = float(sys.argv[6]) if len(sys.argv) > 6 else 1e-9
opts = set(sys.argv[7:]); tag = ''.join('_' + o for o in sorted(opts))
t0 = time.time()
with open(pre + '.vars') as f:
  ncls, nvars = map(int, f.readline().split())
  classes = [(int(p[0]), int(p[1]), int(p[2]), list(map(int, p[3:3 + int(p[1])]))) for p in (l.split() for l in f)]
rows = []; seen = set()
with open(pre + '.ub') as f:
  for line_no, line in enumerate(f, 1):
    if line_no % 250000 == 0: print(f'read {line_no} LP rows', flush=True)
    p = line.split()
    ent = tuple(sorted((int(a), int(b)) for a, b in (x.split(':') for x in p[1:]) if int(a) != nvars))
    if ent in seen: continue
    seen.add(ent); rows.append(ent)
nsnm = len(rows)
if 'mono' in opts:
  with open(pre + '.mono') as f:
    for line in f:
      p = line.split()
      rows.append(tuple(sorted((int(a), int(b)) for a, b in (x.split(':') for x in p[1:]))))
rhsv = [alpha] * nsnm + [Fraction(0)] * (len(rows) - nsnm)
xf = np.load(pre + tag + '_relint_x.npy')
print(f'{len(rows)} rows, {nvars} vars ({time.time()-t0:.0f}s)', flush=True)
clsof = [0] * nvars; v0s = []
v0 = 0
for ci, (code, norb, cw, sizes) in enumerate(classes):
  v0s.append(v0)
  for o in range(norb): clsof[v0 + o] = ci
  v0 += norb
Z = set(j for j in range(nvars) if xf[j] < ztol)
slack = np.array([float(rhsv[i]) - sum(b * xf[a] for a, b in ent) for i, ent in enumerate(rows)])
E = [i for i in range(len(rows)) if slack[i] < stol and not all(a in Z for a, b in rows[i])]
gap = np.sort(slack[slack >= stol])[:3]
print(f'|Z|={len(Z)}  |E|={len(E)}  next slacks {gap}', flush=True)
x = [Fraction(0) if j in Z else Fraction(round(xf[j] * D), D) for j in range(nvars)]
for ci, (code, norb, cw, sizes) in enumerate(classes):
  if cw >= 0:
    for o in range(norb): x[v0s[ci] + o] = Fraction(int(o == cw))
touched = sorted(set(clsof[a] for i in E for a, b in rows[i]))
touched = [ci for ci in touched if classes[ci][2] < 0]
U = [v0s[ci] + o for ci in touched for o in range(classes[ci][1]) if v0s[ci] + o not in Z]
pos = {j: t for t, j in enumerate(U)}
# equations over U: rows in E (= alpha) and class normalisation (= 1); other variables fixed at x
eqs = []
for i in E:
  d = {}; rhs = rhsv[i]
  for a, b in rows[i]:
    if a in pos: d[a] = d.get(a, 0) + b
    else: rhs -= b * x[a]
  eqs.append((d, rhs))
for ci in touched:
  code, norb, cw, sizes = classes[ci]
  eqs.append(({v0s[ci] + o: sizes[o] for o in range(norb) if v0s[ci] + o in pos}, Fraction(1)))
print(f'{len(touched)} touched classes, {len(U)} unknowns, {len(eqs)} equations', flush=True)
if U:
  M = flint.fmpq_mat(len(eqs), len(U)); bvec = flint.fmpq_mat(len(eqs), 1)
  for r_, (d, rhs) in enumerate(eqs):
    s = Fraction(0)
    for j, v in d.items():
      M[r_, pos[j]] = v; s += v * x[j]
    res = rhs - s
    bvec[r_, 0] = flint.fmpq(res.numerator, res.denominator)
  # least-norm correction delta = M^T y with (M M^T) y = res, after removing dependent equations
  rank = M.rank()
  # choose independent rows greedily
  ind = []
  for r_ in range(len(eqs)):
    trial = ind + [r_]
    sub = flint.fmpq_mat([[M[t, c] for c in range(len(U))] for t in trial])
    if sub.rank() == len(trial): ind.append(r_)
  Mi = flint.fmpq_mat([[M[t, c] for c in range(len(U))] for t in ind])
  bi = flint.fmpq_mat([[bvec[t, 0]] for t in ind])
  y = (Mi * Mi.transpose()).solve(bi)
  delta = Mi.transpose() * y
  for j in U:
    dv = delta[pos[j], 0]; x[j] += Fraction(int(dv.p), int(dv.q))
  chk = M * flint.fmpq_mat([[flint.fmpq(x[j].numerator, x[j].denominator)] for j in U])
  consistent = all(chk[r_, 0] == flint.fmpq(eqs[r_][1].numerator, eqs[r_][1].denominator) for r_ in range(len(eqs)))
  print(f'rank {rank}, independent {len(ind)}; all equations satisfied: {consistent}; max |delta| {max(abs(float(delta[t,0])) for t in range(len(U))):.3g}', flush=True)
tset = set(touched)
for ci, (code, norb, cw, sizes) in enumerate(classes):
  if ci in tset or cw >= 0: continue
  tot = sum(sizes[o] * x[v0s[ci] + o] for o in range(norb))
  for o in range(norb): x[v0s[ci] + o] /= tot
ok = all(v >= 0 for v in x)
for ci, (code, norb, cw, sizes) in enumerate(classes):
  if sum(sizes[o] * x[v0s[ci] + o] for o in range(norb)) != 1: ok = False
  if cw >= 0 and x[v0s[ci] + cw] != 1: ok = False
worst = Fraction(-1)
mono_ok = True
for row_no, ent in enumerate(rows):
  value = sum(b * x[a] for a, b in ent)
  if row_no < nsnm: worst = max(worst, value)
  elif value > 0: mono_ok = False
  if row_no % 100000 == 0: print(f'exact rows checked: {row_no}/{len(rows)}', flush=True)
if 'tcc' in opts:
  ok = ok and all(x[j] == 0 for j in tcc_zero_vars(pre, classes, NCLASSES[ncls]))
print(f'lotteries/CC ok={ok}; exact max row value {worst} (target {alpha}); monotone rows ok={mono_ok}; feasible={ok and mono_ok and worst <= alpha}; max denominator {max(v.denominator for v in x)} ({time.time()-t0:.0f}s)', flush=True)
if ok and mono_ok and worst <= alpha:
  pickle.dump({'x': x, 'alpha': alpha}, open(pre + tag + '_frrule.pkl', 'wb'))
  print('saved', pre + tag + '_frrule.pkl', flush=True)
else:
  sys.exit('FAIL: exact rule is infeasible; no certificate written')
