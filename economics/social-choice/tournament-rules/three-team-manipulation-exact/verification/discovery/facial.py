"""Step 1 of facial-reduction exactification: interior point (no crossover) of the optimal face
{x : neutral CC rule, all rows r_S(T')-r_S(T) <= alpha}. Saves x and prints slack histogram.
usage: facial.py prefix alpha_num alpha_den [mono] [tcc]
  mono: also impose monotonicity rows from prefix.mono (x_i(T) <= x_i(T') when i wins one more match)
  tcc:  also impose top-cycle consistency (orbits outside the top cycle get probability 0)"""
import sys, time
import numpy as np
from fractions import Fraction
import highspy
from scipy.sparse import coo_matrix

pre = sys.argv[1]; alpha = Fraction(int(sys.argv[2]), int(sys.argv[3])); opts = set(sys.argv[4:])
from tcc_util import tcc_zero_vars, NCLASSES
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
rhs = np.array([float(alpha)] * nsnm + [0.0] * (len(rows) - nsnm))
zero_ub = tcc_zero_vars(pre, classes, NCLASSES[ncls]) if 'tcc' in opts else []
print(f'{nsnm} unique SNM rows, {len(rows) - nsnm} monotonicity rows, {len(zero_ub)} TCC zero vars, {nvars} vars ({time.time()-t0:.0f}s)', flush=True)
r, c, d = [], [], []
for i, ent in enumerate(rows):
  for a, b in ent: r.append(i); c.append(a); d.append(float(b))
eqr, eqc, eqd, eqb = [], [], [], []
q = 0; v0 = 0
for code, norb, cw, sizes in classes:
  for o in range(norb): eqr.append(q); eqc.append(v0 + o); eqd.append(float(sizes[o]))
  eqb.append(1.0); q += 1
  if cw >= 0: eqr.append(q); eqc.append(v0 + cw); eqd.append(1.0); eqb.append(1.0); q += 1
  v0 += norb
m = len(rows)
R = np.concatenate([np.array(r), m + np.array(eqr)])
C = np.concatenate([np.array(c), np.array(eqc)])
D = np.concatenate([np.array(d), np.array(eqd)])
A = coo_matrix((D, (R, C)), shape=(m + q, nvars)).tocsr()
lp = highspy.HighsLp()
lp.num_col_ = nvars; lp.num_row_ = m + q
lp.col_cost_ = np.zeros(nvars)
lp.col_lower_ = np.zeros(nvars); cu = np.ones(nvars); cu[zero_ub] = 0.0; lp.col_upper_ = cu
inf = highspy.kHighsInf
lp.row_lower_ = np.concatenate([np.full(m, -inf), np.array(eqb)])
lp.row_upper_ = np.concatenate([rhs, np.array(eqb)])
lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
lp.a_matrix_.start_ = A.indptr.astype(np.int32)
lp.a_matrix_.index_ = A.indices.astype(np.int32)
lp.a_matrix_.value_ = A.data
h = highspy.Highs()
h.setOptionValue('threads', 1)
h.setOptionValue('solver', 'ipm'); h.setOptionValue('run_crossover', 'off')
h.setOptionValue('presolve', 'off')
h.setOptionValue('log_to_console', True)
h.passModel(lp)
h.run()
print(h.modelStatusToString(h.getModelStatus()), f'({time.time()-t0:.0f}s)', flush=True)
if h.getModelStatus() != highspy.HighsModelStatus.kOptimal:
  sys.exit('FAIL: interior-point feasibility solve was not optimal')
x = np.array(h.getSolution().col_value)
tag = ''.join('_' + o for o in sorted(opts))
np.save(pre + tag + '_relint_x.npy', x)
s = rhs - A[:m] @ x
for name, vals in (('row slack', s), ('x', x)):
  lv = np.log10(np.maximum(np.abs(vals), 1e-30))
  hist = np.histogram(lv, bins=np.arange(-30, 2))[0]
  print(name, 'min', vals.min(), 'log10 histogram from -30:', list(hist), flush=True)
