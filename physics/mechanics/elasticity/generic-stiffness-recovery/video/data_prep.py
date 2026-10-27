"""Rebuild every number the video shows or says, and write data.json.

Sources:
  - running material: the reference tensor of
    ../verification/numerical-illustration/reconstruct_from_directions.py (seed 20261017)
  - noise example: ../verification/numerical-illustration/reconstruction_results.json
  - isotropic witness H0 (Lame 4, -1) and all counts: ../paper.tex
The twin pair is a teaching example built here (a sign flip valid for box-symmetric,
'orthorhombic' tables, the class where de Hoop et al. report four-to-one ambiguity); it is
checked numerically below and labelled as an illustration in the video.

Run with the video venv python:  $V data_prep.py
"""

import itertools
import json
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NUM = HERE.parent / 'verification' / 'numerical-illustration'

PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]  # Voigt order 11,22,33,23,13,12
PI = {p: k for k, p in enumerate(PAIRS)}
PI.update({(b, a): k for (a, b), k in list(PI.items())})


def tensor(V):
  V = np.asarray(V, dtype=float)
  return np.array([V[PI[i, j], PI[k, l]] for i in range(3) for j in range(3) for k in range(3)
                   for l in range(3)]).reshape(3, 3, 3, 3)


def christoffel(V, n):
  return np.einsum('ijkl,j,k->il', tensor(V), n, n)


def speeds(V, n):
  return np.sqrt(np.clip(np.linalg.eigvalsh(christoffel(V, n)), 0, None))


def summaries(eig):
  a, b, c = eig
  return a + b + c, a * b + a * c + b * c, a * b * c


def unit(v):
  v = np.asarray(v, dtype=float)
  return v / np.linalg.norm(v)


def main():
  out = {}

  # 1. Running material: the paper's synthetic reference tensor (no symmetry at all).
  rng = np.random.default_rng(20261017)
  M = rng.integers(-3, 4, size=(6, 6))
  A = (M @ M.T + 20 * np.eye(6)) / 20
  res = json.loads((NUM / 'reconstruction_results.json').read_text())
  assert np.allclose(A, np.array(res['true_stiffness'])), 'reference tensor mismatch'
  assert np.linalg.eigvalsh(A).min() > 0
  out['A'] = A.round(4).tolist()
  free = [A[i, j] for i in range(6) for j in range(i, 6)]
  assert len(free) == 21 == 6 + 5 + 4 + 3 + 2 + 1
  assert len(set(np.round(free, 4))) >= 15  # many different values; no hidden pattern

  up = np.array([0.0, 0.0, 1.0])
  e = np.linalg.eigvalsh(christoffel(A, up))
  s, p2, p3 = summaries(e)
  out['up'] = {'speeds': np.sqrt(e).round(4).tolist(), 'squares': e.round(4).tolist(), 'sum': round(s, 4),
               'pairs': round(p2, 4), 'product': round(p3, 4)}
  assert abs(s - 6.1) < 1e-9 and abs(p2 - 11.765) < 1e-9 and abs(p3 - 7.1205) < 1e-9
  saved = res['phase_speeds'][0]
  assert np.allclose(np.sqrt(e), saved), 'straight-up speeds must match the saved file'

  # Trace formula: sum of squared speeds = a x^2 + b y^2 + c z^2 + d xy + e xz + f yz.
  mons = [(2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
  dirs = [unit(v) for v in rng.normal(size=(40, 3))]
  Xm = np.array([[n[0] ** a * n[1] ** b * n[2] ** c for a, b, c in mons] for n in dirs])
  y = np.array([np.trace(christoffel(A, n)) for n in dirs])
  coef = np.linalg.lstsq(Xm, y, rcond=None)[0]
  assert np.allclose(Xm @ coef, y, atol=1e-12)
  expect = [7.1, 6.3, 6.1, -2.4, -1.1, 0.7]
  assert np.allclose(coef, expect, atol=1e-9), coef
  out['trace_coefficients'] = expect

  # Coefficient counts of the three summaries (degree 2, 4, 6 forms in three variables).
  counts = [comb(d + 2, 2) for d in (2, 4, 6)]
  assert counts == [6, 15, 28] and sum(counts) == 49
  out['counts'] = counts

  # 3D surface of the fastest wave, and a slice with all three.
  th = np.linspace(0, np.pi, 25)
  ph = np.linspace(0, 2 * np.pi, 49)
  grid = [[float(speeds(A, np.array([np.sin(t) * np.cos(f), np.sin(t) * np.sin(f), np.cos(t)]))[2]) for f in ph]
          for t in th]
  out['surface'] = {'theta': th.tolist(), 'phi': ph.tolist(), 'fast': grid}
  allv = np.array([speeds(A, unit(v)) for v in rng.normal(size=(4000, 3))])
  out['fast_range'] = [float(allv[:, 2].min()), float(allv[:, 2].max())]

  # Choose a slice plane with clearly separated curves and visible anisotropy.
  best = None
  cand = rng.normal(size=(300, 3))
  for nrm in [np.array([0, 0, 1.0]), np.array([0, 1.0, 0]), np.array([1.0, 0, 0])] + list(cand):
    nrm = unit(nrm)
    u = unit(np.cross(nrm, [0.3, 0.5, 0.7]))
    w = np.cross(nrm, u)
    ang = np.linspace(0, np.pi, 91)
    sv = np.array([speeds(A, np.cos(a) * u + np.sin(a) * w) for a in ang])
    gap = min((sv[:, 1] - sv[:, 0]).min(), (sv[:, 2] - sv[:, 1]).min())
    aniso = sv[:, 2].max() / sv[:, 2].min()
    score = aniso if gap > 0.06 else 0
    if best is None or score > best[0]:
      best = (score, nrm, u, w, gap)
  _, nrm, u, w, gap = best
  ang = np.linspace(0, 2 * np.pi, 241)
  curves = np.array([speeds(A, np.cos(a) * u + np.sin(a) * w) for a in ang])
  out['slice'] = {'normal': nrm.tolist(), 'u': u.tolist(), 'w': w.tolist(), 'angles': ang.tolist(),
                  'speeds': curves.T.round(5).tolist(), 'min_gap': float(gap)}

  # 2. Twin pair (illustration): box-symmetric table; flip the signs of c12+c66 and c13+c55.
  c = dict(c11=9, c22=7, c33=8, c44=1.5, c55=2, c66=1, c12=1, c13=2, c23=3)

  def ortho(c12, c13):
    V = np.zeros((6, 6))
    V[0, 0], V[1, 1], V[2, 2] = c['c11'], c['c22'], c['c33']
    V[3, 3], V[4, 4], V[5, 5] = c['c44'], c['c55'], c['c66']
    V[0, 1] = V[1, 0] = c12
    V[0, 2] = V[2, 0] = c13
    V[1, 2] = V[2, 1] = c['c23']
    return V

  T1 = ortho(c['c12'], c['c13'])
  T2 = ortho(-c['c12'] - 2 * c['c66'], -c['c13'] - 2 * c['c55'])
  assert T2[0, 1] == -3 and T2[0, 2] == -6
  assert np.linalg.eigvalsh(T1).min() > 0 and np.linalg.eigvalsh(T2).min() > 0, 'both must be physical'
  worst = 0.0
  for v in rng.normal(size=(20000, 3)):
    n = unit(v)
    worst = max(worst, np.abs(np.linalg.eigvalsh(christoffel(T1, n)) - np.linalg.eigvalsh(christoffel(T2, n))).max())
  assert worst < 1e-12, worst
  # A slice that is not a mirror plane, so the flipped entries matter.
  nrm2 = unit([1, 2, 3])
  u2 = unit(np.cross(nrm2, [0, 0, 1]))
  w2 = np.cross(nrm2, u2)
  tw = np.array([speeds(T1, np.cos(a) * u2 + np.sin(a) * w2) for a in ang])
  # Check the flipped entries really matter in this slice: a single flip changes the speeds.
  T3 = ortho(-c['c12'] - 2 * c['c66'], c['c13'])
  t3 = np.array([speeds(T3, np.cos(a) * u2 + np.sin(a) * w2) for a in ang])
  assert np.abs(t3 - tw).max() > 0.05
  out['twins'] = {'T1': T1.tolist(), 'T2': T2.tolist(), 'max_speed_difference': worst,
                  'slice_speeds': tw.T.round(5).tolist(), 'single_flip_difference': float(np.abs(t3 - tw).max())}

  # 3. The paper's witness: isotropic H0 with Lame parameters 4 and -1, midpoint M = 0.
  lam, mu = 4, -1
  d = np.eye(3)
  H0 = lam * np.einsum('ij,kl->ijkl', d, d) + mu * (np.einsum('ik,jl->ijkl', d, d) + np.einsum('il,jk->ijkl', d, d))
  G = np.einsum('ijkl,j,k->il', H0, up, up)
  assert np.allclose(G, np.diag([-1, -1, 2]))
  eD = np.diag(G)
  eN = -eD
  sD, sN = summaries(eD), summaries(eN)
  assert sD[0] == sN[0] == 0 and sD[1] == sN[1] == -3 and sD[2] == 2 and sN[2] == -2
  for v in rng.normal(size=(50, 3)):  # matches in every direction for sum and pairs, never for product
    n = unit(v)
    ev = np.linalg.eigvalsh(np.einsum('ijkl,j,k->il', H0, n, n))
    a1, b1 = summaries(ev), summaries(-ev)
    assert abs(a1[0] - b1[0]) < 1e-12 and abs(a1[1] - b1[1]) < 1e-12 and abs(a1[2] - 2) < 1e-12
  out['witness'] = {'D': eD.tolist(), 'minusD': eN.tolist(), 'D_summaries': list(sD), 'minusD_summaries': list(sN)}

  # 4. The dimension count of the main proof (paper, Section 2).
  rows = []
  for r in range(6, 16):
    dD = 15 if r == 15 else r - 1
    rows.append({'r': r, 'D': dD, 'M': 21 - r, 'total': dD + 21 - r, 'after_test3': dD + 21 - r - (1 if r == 15 else 0)})
  assert all(x['after_test3'] == 20 for x in rows)
  out['strata'] = rows

  # 5. Direction counts (paper, Section 7).
  out['lower_bound'] = {m: min(m, 6) + 2 * m for m in range(1, 12)}
  assert out['lower_bound'][7] == 20 and out['lower_bound'][8] == 22
  assert 21 + 2 * 11 == 43
  nodes = [(a, b) for a in range(5) for b in range(5 - a)]
  assert len(nodes) == 15 and len([1 for a, b in nodes if a + b <= 2]) == 6
  out['nodes'] = nodes
  assert (32000 + 10) % 32003 == 7

  # 6. Noise example: compressed fit with the smallest residual at 0.1% speed noise.
  ex = [x for x in res['experiments'] if x['relative_phase_speed_noise_std'] == 1e-3]
  comp = min((x for x in ex if x['data_mode'] == 'compressed-22'), key=lambda x: x['scaled_residual_norm'])
  full = [x for x in ex if x['data_mode'] == 'all-45-speeds' and x['initialization'] == 'best-compressed-fit'][0]
  out['noise'] = {'noise': 1e-3, 'compressed_error': comp['relative_frobenius_error'],
                  'full_error': full['relative_frobenius_error']}
  assert abs(comp['relative_frobenius_error'] - 0.452) < 0.001 and abs(full['relative_frobenius_error'] - 0.00577) < 1e-4

  (HERE / 'data.json').write_text(json.dumps(out, indent=1))
  print('up', out['up'])
  print('fast range', out['fast_range'], 'slice gap', gap, 'normal', nrm)
  print('twin max difference', worst, 'single flip', out['twins']['single_flip_difference'])
  print('noise', out['noise'])
  print('wrote data.json')


if __name__ == '__main__':
  main()
