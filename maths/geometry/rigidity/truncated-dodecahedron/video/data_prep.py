"""Prepare the numbers the explainer animates, straight from the finding's certificate.

Writes data.json next to this file:
  vertices      60 float vertex positions (exact Q(phi) coordinates evaluated)
  faces         32 faces, each a cyclically ordered vertex list
  flex          one real first-order flex (vertex arrows), orthogonal to rigid motions
  real_corank   numerical dimension of the real first-order flex space mod rigid motions
  cubic         the four certified cubic obstructions over F_1009 with their monomials
  cancel        for v0^9: coefficients of the running sum A_10 C_1 + ... + A_k0 C_k
                over all 220 degree-nine monomials, k = 1..4

Run with any Python that has numpy:  python data_prep.py
"""

import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
VER = HERE.parent / 'verification'
PHI = (1 + 5 ** 0.5) / 2
P = 1009


def qphi(pair):
  a, b = (float(Fraction(x)) for x in pair)
  return a + b * PHI


def main():
  data = json.loads((VER / 'modular-obstruction.json').read_text())
  verts = np.array([[qphi(c) for c in v] for v in data['vertices']])
  normals = np.array([[qphi(c) for c in n] for n in data['normals']])
  edges = data['edges']
  facets = data['facets']
  assert len(verts) == 60 and len(edges) == 90 and len(facets) == 32

  # Exact-ish sanity: every incidence p.a = 1 and every edge has squared length 8 - 4 phi.
  for f, fac in enumerate(facets):
    for i in fac:
      assert abs(verts[i] @ normals[f] - 1) < 1e-9
  for i, j in edges:
    assert abs(np.sum((verts[i] - verts[j]) ** 2) - (8 - 4 * PHI)) < 1e-9

  # Cyclic order of each face for drawing.
  faces = []
  for f, fac in enumerate(facets):
    c = verts[fac].mean(axis=0)
    n = normals[f] / np.linalg.norm(normals[f])
    e1 = verts[fac[0]] - c
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    ang = [np.arctan2((verts[i] - c) @ e2, (verts[i] - c) @ e1) for i in fac]
    faces.append([fac[k] for k in np.argsort(ang)])

  # Real first-order (Jacobian) analysis in the 276 variables, without gauges.
  nv = 60
  rows = []
  for i, j in edges:
    r = np.zeros(276)
    d = verts[i] - verts[j]
    r[3 * i:3 * i + 3] = 2 * d
    r[3 * j:3 * j + 3] = -2 * d
    rows.append(r)
  for f, fac in enumerate(facets):
    for i in fac:
      r = np.zeros(276)
      r[3 * i:3 * i + 3] = normals[f]
      r[3 * (nv + f):3 * (nv + f) + 3] = verts[i]
      rows.append(r)
  jac = np.array(rows)
  assert jac.shape == (270, 276)
  sv = np.linalg.svd(jac, compute_uv=False)
  # Rigid motions: translations and rotations acting on points; normals follow the normalization.
  triv = []
  for t in np.eye(3):
    u = np.zeros(276)
    for i in range(nv):
      u[3 * i:3 * i + 3] = t
    for f in range(32):
      a = normals[f]
      u[3 * (nv + f):3 * (nv + f) + 3] = -a * (a @ t)  # d/ds of a/(1 + a.(s t))
    triv.append(u)
  for w in np.eye(3):
    u = np.zeros(276)
    for i in range(nv):
      u[3 * i:3 * i + 3] = np.cross(w, verts[i])
    for f in range(32):
      u[3 * (nv + f):3 * (nv + f) + 3] = np.cross(w, normals[f])
    triv.append(u)
  triv = np.array(triv)
  assert np.max(np.abs(jac @ triv.T)) < 1e-9
  _, s, vt = np.linalg.svd(jac)
  null = vt[np.concatenate([s, np.zeros(276 - len(s))]) < 1e-8]
  tq, _ = np.linalg.qr(triv.T)
  proj = null.T - tq @ (tq.T @ null.T)
  uu, ss, _ = np.linalg.svd(proj, full_matrices=False)
  real_corank = int(np.sum(ss > 1e-6))
  # Pick the nontrivial flex whose vertex arrows are as even in size as possible (pleasant to draw).
  basis = uu[:, :real_corank]
  best, best_score = None, None
  rng = np.random.default_rng(7)
  for _ in range(4000):
    c = rng.normal(size=real_corank)
    u = basis @ c
    vel = u[:180].reshape(60, 3)
    vel = vel - vel.mean(axis=0)
    m = np.linalg.norm(vel, axis=1)
    score = m.std() / m.mean()
    if best_score is None or score < best_score:
      best, best_score = u, score
  vel = best[:180].reshape(60, 3)
  scale = 1 / np.max(np.linalg.norm(vel, axis=1))
  flex = (best * scale)
  # An orthonormal basis of the four nontrivial flexes whose first element is the drawn flex.
  bq, _ = np.linalg.qr(np.column_stack([flex, basis]))
  flex_basis = []
  for k in range(4):
    b = bq[:, k] * (1 if k else np.sign(bq[:, 0] @ flex))
    bv = b[:180].reshape(60, 3)
    flex_basis.append((bv / np.max(np.linalg.norm(bv, axis=1))).round(6).tolist())
    assert np.max(np.abs(jac @ b)) < 1e-8
  assert np.max(np.abs(jac @ flex)) < 1e-8
  # Second-order growth of edge lengths when following the arrows exactly: |u_i-u_j|^2 per edge.
  fv = flex[:180].reshape(60, 3)
  edge_growth = [float(np.sum((fv[i] - fv[j]) ** 2)) for i, j in edges]

  # The full equations F(x) = J x + q(x) and a real second-order correction w with J w + q(u) = 0.
  def equations(x):
    u = x[:180].reshape(60, 3)
    a = x[180:].reshape(32, 3)
    out = [np.sum((verts[i] + u[i] - verts[j] - u[j]) ** 2) - np.sum((verts[i] - verts[j]) ** 2) for i, j in edges]
    out += [(verts[i] + u[i]) @ (normals[f] + a[f]) - 1 for f, fac in enumerate(facets) for i in fac]
    return np.array(out)

  q_u = equations(flex) - jac @ flex
  w, *_ = np.linalg.lstsq(jac, -q_u, rcond=None)
  second_residual = float(np.max(np.abs(jac @ w + q_u)))
  assert second_residual < 1e-10

  def worst_stick_error(x):
    u = x[:180].reshape(60, 3)
    return max(abs(np.linalg.norm(verts[i] + u[i] - verts[j] - u[j]) - np.linalg.norm(verts[i] - verts[j]))
               for i, j in edges)

  ts = np.linspace(0, 0.5, 51)
  straight = [worst_stick_error(t * flex) for t in ts]
  bent = [worst_stick_error(t * flex + t * t * w) for t in ts]

  # Cubic obstructions and the cancellation for v0^9.
  mon3 = data['degree3_monomials']
  exps3 = [tuple(m.count(i) for i in range(4)) for m in mon3]
  cubics = data['cubic_obstruction']
  cert = json.loads((VER / 'pure-power-certificate.json').read_text())
  mult = [tuple(m) for m in cert['multiplier_monomials']]
  coeffs = cert['coefficients']
  mon9 = sorted({e for e in itertools.product(range(10), repeat=4) if sum(e) == 9}, reverse=True)
  assert len(mon9) == 220
  cancel = {}
  for target in range(4):
    running = {e: 0 for e in mon9}
    stages = []
    for gen in range(4):
      for m, row in zip(mult, coeffs[gen]):
        for e3, val in zip(exps3, cubics[gen]):
          e = tuple(a + b for a, b in zip(e3, m))
          running[e] = (running[e] + row[target] * val) % P
      stages.append([running[e] for e in mon9])
    final = {e: v for e, v in running.items() if v}
    assert final == {tuple(9 if i == target else 0 for i in range(4)): 1}, final
    cancel[f'v{target}'] = {'stages': stages, 'nonzero': [sum(1 for v in st if v) for st in stages]}
  # Size of the multipliers used in the v0 identity.
  mult_terms = [[sum(1 for row in coeffs[g] if row[t]) for g in range(4)] for t in range(4)]

  out = {
    'vertices': verts.round(6).tolist(),
    'faces': faces,
    'edges': edges,
    'flex': {'vertex_arrows': fv.round(6).tolist(), 'edge_growth': edge_growth,
             'second_order_vertices': w[:180].reshape(60, 3).round(6).tolist(),
             'second_order_residual': second_residual, 'basis_vertex_arrows': flex_basis},
    'error_curves': {'t': ts.round(4).tolist(), 'straight': straight, 'bent': bent},
    'real_singular_values_smallest': sorted(float(x) for x in sv)[:12],
    'real_corank_mod_rigid': real_corank,
    'cubic': {'monomials': exps3, 'coefficients': cubics},
    'mon9': mon9,
    'cancel': cancel,
    'multiplier_nonzero_terms': mult_terms,
    'phi_check': [627, 627 * 627, (627 * 627) % P],
  }
  (HERE / 'data.json').write_text(json.dumps(out))
  print('real corank mod rigid motions:', real_corank)
  print('smallest singular values:', np.round(sorted(sv)[:12], 6))
  print('nonzero coefficient counts per stage (v0..v3):', {k: v['nonzero'] for k, v in cancel.items()})
  print('multiplier nonzero terms [target][generator]:', mult_terms)
  print('627^2 =', 627 * 627, '-> mod 1009 =', (627 * 627) % P)
  print('edge growth range:', min(edge_growth), max(edge_growth))
  print('second-order residual:', second_residual)
  for k in (5, 10, 20, 30, 50):
    print(f't={ts[k]:.2f} worst stick error straight={straight[k]:.5f} bent={bent[k]:.5f}')


if __name__ == '__main__':
  main()
