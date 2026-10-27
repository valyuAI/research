"""Exact certificates that J58, J59, J81 (and J83) are NOT prestress stable (standard library only, except that
an optional numerical search proposes the certificate; see below).

Prestress stability means that some combination sum_j mu_j Q_j of the second-order forms (k x k symmetric
matrices Q_j, see check_second_order.py) is definite. Theorem of alternatives: the open cone of positive definite
matrices misses the subspace span(Q_j) iff there is a non-zero positive semidefinite X with <Q_j, X> = tr(Q_j X) = 0
for all j. (If sum mu_j Q_j were positive or negative definite, tr((sum mu_j Q_j) X) would be non-zero for every
non-zero X >= 0.) We exhibit a positive definite X with exact entries in Q(sqrt5), orthogonal to every Q_j, and
check positive definiteness exactly by Sylvester's criterion.

The coefficients of X in a basis of the orthogonal complement are proposed by maximising the smallest eigenvalue
numerically (numpy) and rounding to rationals; the proposal is untrusted and everything is re-checked exactly.
usage: python3 check_prestress.py [J numbers]   (default 58 59 81 83)"""
import json, sys
from fractions import Fraction
import nfsolid, exactlin
from check_second_order import rigidity_rows, trivial_motions, bform, definite, need


def forms_of(k):
  name, K, V, F = nfsolid.load(k if str(k).endswith('.json') else 'data/J%02d.json' % k)
  P, A, E, rep = nfsolid.validate(K, V, F)
  rows, inc, n = rigidity_rows(K, P, A, E, F)
  ker, rk = exactlin.nullspace(K, rows, n)
  cols_T, m = exactlin.transpose(rows, n)
  stresses, _ = exactlin.nullspace(K, cols_T, m)
  T = trivial_motions(K, P, A)
  need(exactlin.rank(K, T, n) == 6, 'trivial-motion rank')
  need(all(all(K.is0(x) for x in exactlin.apply(K, rows, t)) for t in T), 'trivial motions in kernel')
  flex, r = [], 6
  for v in ker:
    if exactlin.rank(K, T + flex + [v], n) > r:
      flex.append(v)
      r += 1
  d = len(flex)
  need(d == len(ker) - 6 == len(stresses), 'flex/stress dimensions')
  forms = [[[bform(K, E, inc, len(P), xi, flex[a], flex[b]) for b in range(d)] for a in range(d)] for xi in stresses]
  return name, K, forms


def sym_basis(K, d):
  B = []
  for a in range(d):
    for b in range(a, d):
      M = [[K.zero] * d for _ in range(d)]
      M[a][b] = K.one
      M[b][a] = K.one
      B.append(M)
  return B


def inner(K, M, N):
  tot = K.zero
  for a in range(len(M)):
    for b in range(len(M)):
      tot = K.add(tot, K.mul(M[a][b], N[a][b]))
  return tot


def orthogonal_basis(K, forms):
  d = len(forms[0])
  B = sym_basis(K, d)
  # orthogonal complement of span(Q_j) inside Sym(d): solve <Q_j, sum c_i B_i> = 0 exactly
  rows = [{i: inner(K, Q, Bi) for i, Bi in enumerate(B) if not K.is0(inner(K, Q, Bi))} for Q in forms]
  comp, rk = exactlin.nullspace(K, rows, len(B))
  C = [[[nfsolid.sumK(K, (K.mul(v.get(i, K.zero), B[i][a][b]) for i in range(len(B)))) for b in range(d)]
        for a in range(d)] for v in comp]
  return C


def verify_certificate(K, forms, cert):
  """Replay an untrusted stored matrix; success is entirely exact."""
  d = len(forms[0])
  need(all(len(x) == K.n for row in cert['X'] for x in row), 'field element dimensions')
  X = [[nfsolid.conv_elem(x, K) for x in row] for row in cert['X']]
  need(len(X) == d and all(len(row) == d for row in X), 'certificate dimensions')
  need(all(K.is0(K.sub(X[a][b], X[b][a])) for a in range(d) for b in range(d)), 'certificate symmetry')
  need(all(K.is0(inner(K, Q, X)) for Q in forms), 'certificate orthogonality')
  need(K.sign(X[0][0]) > 0 and definite(K, X), 'certificate positive definiteness')
  return True


def certificate(K, forms):
  """Optional numerical proposal; normal replay uses only verify_certificate."""
  C = orthogonal_basis(K, forms)
  d = len(forms[0])
  # numerical proposal: maximise the smallest eigenvalue of sum t_i C_i over |t| = 1
  import numpy as np
  from scipy.optimize import minimize
  Cf = [np.array([[K.to_float(x) for x in r] for r in M]) for M in C]
  def negmin(t):
    t = t / np.linalg.norm(t)
    return -np.linalg.eigvalsh(sum(ti * Ci for ti, Ci in zip(t, Cf)))[0]
  best = None
  rng = np.random.default_rng(1)
  for _ in range(200):
    res = minimize(negmin, rng.normal(size=len(Cf)), method='Nelder-Mead', options={'maxiter': 4000})
    if best is None or res.fun < best.fun:
      best = res
  t = best.x / np.linalg.norm(best.x)
  lam = -best.fun
  if lam <= 0:
    return {'ok': False, 'reason': 'no positive definite element found numerically', 'lambda_min': float(lam)}
  coeffs = [Fraction(float(x)).limit_denominator(10 ** 6) for x in t]
  X = [[nfsolid.sumK(K, (K.scal(c, M[a][b]) for c, M in zip(coeffs, C))) for b in range(d)] for a in range(d)]
  orth = all(K.is0(inner(K, Q, X)) for Q in forms)
  pd = definite(K, X)
  return {'ok': orth and pd, 'orthogonal_exact': orth, 'definite_exact': pd, 'lambda_min_float': float(lam),
          'complement_dim': len(C), 'coefficients': [str(c) for c in coeffs],
          'X': [[[str(c) for c in x] for x in r] for r in X]}


if __name__ == '__main__':
  ks = [int(a) for a in sys.argv[1:]] or [58, 59, 81, 83]
  certs = json.load(open('certificates/prestress.json'))
  out = {}
  for k in ks:
    print('Recomputing J%s stress forms' % k, flush=True)
    name, K, forms = forms_of(k)
    cert = certs[str(k)]
    verify_certificate(K, forms, cert)
    out[str(k)] = dict(name=name, k=len(forms[0]), ok=True, orthogonal_exact=True, positive_definite_exact=True)
    print('J%s: exact non-prestress certificate PASS' % k, flush=True)
  with open('results/prestress_replay.json', 'w') as f:
    json.dump(out, f, indent=2)
  print('ALL REQUESTED CERTIFICATES REPLAYED', flush=True)
