"""Floating-point map of the legal (eps, delta) region where the full support of a given graph is a stable
fixed point (permitted and positive stable).  Illustration only; the theorem uses exact checks."""
import json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = json.load(open(sys.argv[1])); n = d['n']; E = set(map(tuple, d['edges']))
N = np.array([[0 if (i == j or (j, i) in E) else 1 for j in range(n)] for i in range(n)], float)

def ok(eps, delta):
  if not (0 < eps < delta / (1 + delta)): return np.nan
  t = (1 - eps) / eps; beta = 1 + delta / eps
  C = np.eye(n) + beta * N
  y = np.linalg.solve(C, np.ones(n))
  if y.min() <= 0: return 0
  return 1 if np.linalg.eigvals(C + t).real.min() > 0 else 0

lo_e, hi_e, lo_d, hi_d = (float(v) for v in sys.argv[3:7]) if len(sys.argv) > 6 else (0.005, 0.6, 0.02, 2.0)
G = int(sys.argv[7]) if len(sys.argv) > 7 else 240
E1 = np.linspace(lo_e, hi_e, G); D1 = np.linspace(lo_d, hi_d, G)
Z = np.array([[ok(e, dl) for e in E1] for dl in D1])
pass
fig, ax = plt.subplots(figsize=(5.2, 4.2))
ax.contourf(E1, D1, np.nan_to_num(Z, nan=-1), levels=[-1.5, -0.5, 0.5, 1.5], colors=['#eeeeee', 'white', '#1f5fa8'])
ax.plot(E1, 2 * E1, color='#999999', lw=0.8, ls=':', label=r'$\delta=2\varepsilon$ ($\beta=3$)')
ax.plot([0.25], [0.5], marker='*', color='#c0392b', ms=12, ls='none', label=r'standard $(\varepsilon,\delta)=(1/4,1/2)$')
ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'$\delta$')
ax.set_title('Full support stable (blue); illegal parameters (grey)', fontsize=9)
ax.set_xlim(lo_e, hi_e); ax.set_ylim(lo_d, hi_d); ax.legend(fontsize=7, loc='upper left'); fig.tight_layout(); fig.savefig(sys.argv[2] + '.pdf')
inside = np.nansum(Z); print('stable grid points', int(inside), 'of legal', int(np.sum(~np.isnan(Z))))
