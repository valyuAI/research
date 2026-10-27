"""Second-order rigidity certificates for the first-order flexible Johnson solids that are rigid
(J58, J59, J60, J81, J82, J83). Standard library only; all arithmetic exact over the coordinate field K.

Model (Adrian-Himmelmann, Winter, Zhang, arXiv:2607.09252, Sections 3-4): unknowns are the vertices p_i and the
facet normals a_s (with <p_i, a_s> = 1); constraints |p_i - p_j|^2 (edges) and <p_i, a_s> (incidences).
For each solid we compute exactly
  * the first-order motion space ker R (and check it contains the 6 trivial motions),
  * a flex basis F_1..F_k completing the trivial motions, the stress space coker R (dimension k, Prop. 3.6),
  * the quadratic forms Q_xi(u) = xi^T R(u) u restricted to span(F) (Theorem 4.2, stress test),
and certify that the forms have no common real zero except 0:
  k = 1: the single form is non-zero;
  k >= 2: Macaulay matrix in degree k+1 has full rank (then every degree-(k+1) monomial lies in the ideal, so the
          only common complex zero is 0), or, for k = 3, a resultant/gcd/Sturm argument excluding real zeros.
Q_xi is invariant under adding trivial motions (constraints are invariant under the Euclidean group), so this is
exactly the stress test; by Theorem 4.1 of arXiv:2607.09252 second-order rigidity implies rigidity.
Also: exact prestress-stability check (a stress whose form is definite) where one is found."""
import itertools, json, sys
from fractions import Fraction
import nfsolid, exactlin


def need(cond, msg='check failed'):
  """Explicit check that is not removed by python -O."""
  if not cond:
    raise ValueError(msg)


def rigidity_rows(K, P, A, E, F):
  nV = len(P)
  inc = [(i, s) for s, f in enumerate(F) for i in f]
  rows = []
  for i, j in E:
    d = K.vsub(P[i], P[j])
    r = {}
    for k in range(3):
      if not K.is0(d[k]):
        r[3 * i + k] = d[k]
        r[3 * j + k] = K.neg(d[k])
    rows.append(r)
  for i, s in inc:
    r = {}
    for k in range(3):
      if not K.is0(A[s][k]):
        r[3 * i + k] = A[s][k]
      if not K.is0(P[i][k]):
        r[3 * nV + 3 * s + k] = P[i][k]
    rows.append(r)
  return rows, inc, 3 * (nV + len(A))


def trivial_motions(K, P, A):
  nV = len(P)
  T = []
  for k in range(3):  # translations: p -> p + e_k, a -> a - <a, e_k> a (first order)
    v = {3 * i + k: K.one for i in range(nV)}
    for s, a in enumerate(A):
      for j in range(3):
        x = K.neg(K.mul(a[k], a[j]))
        if not K.is0(x):
          v[3 * nV + 3 * s + j] = x
    T.append(v)
  for i0, j0 in [(1, 2), (2, 0), (0, 1)]:  # rotations
    v = {}
    for idx, X in enumerate(list(P) + list(A)):
      if not K.is0(X[j0]):
        v[3 * idx + i0] = X[j0]
      if not K.is0(X[i0]):
        v[3 * idx + j0] = K.neg(X[i0])
    T.append(v)
  return T


def bform(K, E, inc, nV, xi, u, w):
  g = lambda v, c: v.get(c, K.zero)
  tot = K.zero
  for r, (i, j) in enumerate(E):
    x = xi.get(r)
    if x is None:
      continue
    s = K.zero
    for k in range(3):
      du = K.sub(g(u, 3 * i + k), g(u, 3 * j + k))
      dw = K.sub(g(w, 3 * i + k), g(w, 3 * j + k))
      s = K.add(s, K.mul(du, dw))
    tot = K.add(tot, K.mul(x, s))
  for r, (i, f) in enumerate(inc):
    x = xi.get(len(E) + r)
    if x is None:
      continue
    s = K.zero
    for k in range(3):
      s = K.add(s, K.mul(g(u, 3 * i + k), g(w, 3 * nV + 3 * f + k)))
      s = K.add(s, K.mul(g(w, 3 * i + k), g(u, 3 * nV + 3 * f + k)))
    tot = K.add(tot, K.mul(x, s))
  return tot


def monomials(n, d):
  return [m for m in itertools.product(range(d + 1), repeat=n) if sum(m) == d]


def macaulay_full_rank(K, forms, N):
  k = len(forms[0])
  cols = monomials(k, N)
  cidx = {m: i for i, m in enumerate(cols)}
  rows = []
  for M in forms:
    poly = {}
    for a in range(k):
      for b in range(k):
        e = [0] * k
        e[a] += 1
        e[b] += 1
        poly[tuple(e)] = K.add(poly.get(tuple(e), K.zero), M[a][b])
    for mono in monomials(k, N - 2):
      r = {}
      for e, c in poly.items():
        if K.is0(c):
          continue
        t = cidx[tuple(x + y for x, y in zip(e, mono))]
        r[t] = K.add(r.get(t, K.zero), c)
      rows.append({i: c for i, c in r.items() if not K.is0(c)})
  rk = exactlin.rank(K, rows, len(cols))
  return rk, len(cols)


# ---- univariate polynomials over K (low degree first) ----
def ptrim(K, p):
  p = list(p)
  while len(p) > 1 and K.is0(p[-1]):
    p.pop()
  return p


def pmod(K, a, b):
  a, b = ptrim(K, a), ptrim(K, b)
  inv = K.inv(b[-1])
  while len(a) >= len(b) and not (len(a) == 1 and K.is0(a[0])):
    c = K.mul(a[-1], inv)
    k = len(a) - len(b)
    for i, y in enumerate(b):
      a[i + k] = K.sub(a[i + k], K.mul(c, y))
    a = ptrim(K, a[:-1] if len(a) > 1 else a)
  return a


def pgcd(K, a, b):
  a, b = ptrim(K, a), ptrim(K, b)
  while not (len(b) == 1 and K.is0(b[0])):
    a, b = b, pmod(K, a, b)
  return a


def real_root_count(K, f):
  """Number of distinct real roots of f (Sturm sequence, signs at -inf and +inf)."""
  f = ptrim(K, f)
  if len(f) == 1:
    return 0
  df = ptrim(K, [K.scal(i, c) for i, c in enumerate(f)][1:])
  seq = [f, df]
  while len(seq[-1]) > 1 or not K.is0(seq[-1][0]):
    r = pmod(K, seq[-2], seq[-1])
    if len(r) == 1 and K.is0(r[0]):
      break
    seq.append([K.neg(c) for c in r])
  def var(sgns):
    s = [x for x in sgns if x]
    return sum(1 for u, v in zip(s, s[1:]) if u != v)
  plus = [K.sign(p[-1]) for p in seq]
  minus = [K.sign(p[-1]) * (-1) ** (len(p) - 1) for p in seq]
  return var(minus) - var(plus)


# ---- homogeneous polynomials in (x, y) over K: dict (i, j) -> elem ----
def hadd(K, p, q):
  r = dict(p)
  for e, c in q.items():
    r[e] = K.add(r.get(e, K.zero), c)
  return {e: c for e, c in r.items() if not K.is0(c)}


def hmul(K, p, q):
  r = {}
  for e1, c1 in p.items():
    for e2, c2 in q.items():
      e = (e1[0] + e2[0], e1[1] + e2[1])
      r[e] = K.add(r.get(e, K.zero), K.mul(c1, c2))
  return {e: c for e, c in r.items() if not K.is0(c)}


def hneg(K, p):
  return {e: K.neg(c) for e, c in p.items()}


def ternary_no_real_zero(K, forms):
  """Three ternary quadratic forms (3x3 symmetric matrices over K): certify that they have no common real zero
  other than 0, via a rational change of coordinates, resultants in z, a gcd over K and a Sturm count."""
  T = [[1, 0, 2], [0, 1, -3], [1, -1, 1]]  # v -> T v ; invertible (det = 1 - 2 + ... checked below)
  detT = (T[0][0] * (T[1][1] * T[2][2] - T[1][2] * T[2][1]) - T[0][1] * (T[1][0] * T[2][2] - T[1][2] * T[2][0])
          + T[0][2] * (T[1][0] * T[2][1] - T[1][1] * T[2][0]))
  need(detT != 0, 'detT != 0')
  def transform(M):
    return [[nfsolid.sumK(K, (K.scal(T[i][a] * T[j][b], M[i][j]) for i in range(3) for j in range(3)
                              if T[i][a] * T[j][b])) for b in range(3)] for a in range(3)]
  Ms = [transform(M) for M in forms]
  # Q = a z^2 + b z + c with a in K, b linear in (x,y), c quadratic in (x,y)
  def split(M):
    a = M[2][2]
    b = {(1, 0): K.scal(2, M[0][2]), (0, 1): K.scal(2, M[1][2])}
    c = {(2, 0): M[0][0], (1, 1): K.scal(2, M[0][1]), (0, 2): M[1][1]}
    return a, {e: x for e, x in b.items() if not K.is0(x)}, {e: x for e, x in c.items() if not K.is0(x)}
  parts = [split(M) for M in Ms]
  if any(K.is0(p[0]) for p in parts):
    return {'ok': False, 'reason': 'a z^2 coefficient vanishes'}
  def res(p, q):
    (a1, b1, c1), (a2, b2, c2) = p, q
    k1, k2 = {(0, 0): a1}, {(0, 0): a2}
    A = hadd(K, hmul(K, k1, c2), hneg(K, hmul(K, k2, c1)))
    B = hadd(K, hmul(K, k1, b2), hneg(K, hmul(K, k2, b1)))
    C = hadd(K, hmul(K, b1, c2), hneg(K, hmul(K, b2, c1)))
    return hadd(K, hmul(K, A, A), hneg(K, hmul(K, B, C)))  # quartic binary form
  R12, R13 = res(parts[0], parts[1]), res(parts[0], parts[2])
  # y = 0 branch: (x : 0 : z) with x != 0 needs R12(1,0) = R13(1,0) = 0
  y0 = K.is0(R12.get((4, 0), K.zero)) and K.is0(R13.get((4, 0), K.zero))
  uni = lambda R: ptrim(K, [R.get((i, 4 - i), K.zero) for i in range(5)])
  g = pgcd(K, uni(R12), uni(R13))
  nreal = real_root_count(K, g)
  ok = (not y0) and nreal == 0
  return {'ok': ok, 'gcd_degree': len(g) - 1, 'gcd_real_roots': nreal, 'y0_branch_possible': y0,
          'a_coeffs_nonzero': True}


def definite(K, M):
  """Sylvester: M positive definite iff all leading principal minors > 0; negative definite iff -M is."""
  def minors(M):
    out = []
    for k in range(1, len(M) + 1):
      rows = [list(r[:k]) for r in M[:k]]
      out.append(det(K, rows))
    return out
  def det(K, rows):
    rows = [list(r) for r in rows]
    n = len(rows)
    d = K.one
    for c in range(n):
      p = next((i for i in range(c, n) if not K.is0(rows[i][c])), None)
      if p is None:
        return K.zero
      if p != c:
        rows[c], rows[p] = rows[p], rows[c]
        d = K.neg(d)
      d = K.mul(d, rows[c][c])
      inv = K.inv(rows[c][c])
      for i in range(c + 1, n):
        f = K.mul(rows[i][c], inv)
        if not K.is0(f):
          rows[i] = [K.sub(x, K.mul(f, y)) for x, y in zip(rows[i], rows[c])]
    return d
  pos = all(K.sign(m) > 0 for m in minors(M))
  neg = all(K.sign(m) > 0 for m in minors([[K.neg(x) for x in r] for r in M]))
  return pos or neg


def analyse(path):
  name, K, V, F = nfsolid.load(path)
  P, A, E, rep = nfsolid.validate(K, V, F)
  rows, inc, n = rigidity_rows(K, P, A, E, F)
  ker, rk = exactlin.nullspace(K, rows, n)
  cols_T, m = exactlin.transpose(rows, n)
  stresses, rk2 = exactlin.nullspace(K, cols_T, m)
  need(rk == rk2, 'rk == rk2')
  T = trivial_motions(K, P, A)
  for t in T:
    need(all(K.is0(x) for x in exactlin.apply(K, rows, t)), 'trivial motion not in kernel')
  need(exactlin.rank(K, T, n) == 6, 'exactlin.rank(K, T, n) == 6')
  flex, r = [], 6
  for v in ker:
    if exactlin.rank(K, T + flex + [v], n) > r:
      flex.append(v)
      r += 1
  k = len(flex)
  need(k == len(ker) - 6 == len(stresses), (k, len(ker), len(stresses)))
  for v in flex:
    need(all(K.is0(x) for x in exactlin.apply(K, rows, v)), 'all(K.is0(x) for x in exactlin.apply(K, rows, v))')
  forms = [[[bform(K, E, inc, len(P), xi, flex[a], flex[b]) for b in range(k)] for a in range(k)]
           for xi in stresses]
  out = {'name': name, 'field_degree': K.n, 'cols': n, 'rank': rk, 'flex_dim': k, 'stress_dim': len(stresses)}
  if k == 1:
    nz = [not K.is0(M[0][0]) for M in forms]
    out['second_order_rigid'] = any(nz)
    out['method'] = 'single flex: some stress form Q_xi(F1) != 0'
    out['prestress_certificate_found'] = any(nz)
  else:
    mr, mc = macaulay_full_rank(K, forms, k + 1)
    out['macaulay'] = {'degree': k + 1, 'rank': mr, 'monomials': mc}
    if mr == mc:
      out['second_order_rigid'] = True
      out['method'] = 'Macaulay matrix full rank: no common complex zero'
    elif k == 3:
      tz = ternary_no_real_zero(K, forms)
      out['ternary'] = tz
      out['second_order_rigid'] = tz['ok']
      out['method'] = 'resultants + gcd over K + Sturm: no common real zero'
    else:
      out['second_order_rigid'] = False
      out['method'] = 'inconclusive'
    # prestress: look for a small integer combination of stresses with a definite form
    ps = False
    for mu in itertools.product(range(-3, 4), repeat=len(forms)):
      if not any(mu):
        continue
      M = [[nfsolid.sumK(K, (K.scal(c, f[a][b]) for c, f in zip(mu, forms) if c)) for b in range(k)]
           for a in range(k)]
      if definite(K, M):
        ps = list(mu)
        break
    out['prestress_certificate_found'] = bool(ps)
    if ps:
      out['prestress_combination'] = ps
    if k == 2 and len(forms) == 2:
      # exact decision: a 2x2 symmetric matrix is definite iff its determinant is > 0, and
      # D(mu) = det(mu1 M1 + mu2 M2) = A mu1^2 + B mu1 mu2 + C mu2^2; prestress stable iff D(mu) > 0 for some mu
      M1, M2 = forms
      det2 = lambda a, b, c: K.sub(K.mul(a, c), K.mul(b, b))  # [[a, b], [b, c]]
      A = det2(M1[0][0], M1[0][1], M1[1][1])
      C = det2(M2[0][0], M2[0][1], M2[1][1])
      Bx = K.sub(K.add(K.mul(M1[0][0], M2[1][1]), K.mul(M2[0][0], M1[1][1])), K.scal(2, K.mul(M1[0][1], M2[0][1])))
      disc = K.sub(K.mul(Bx, Bx), K.scal(4, K.mul(A, C)))
      never_positive = K.sign(A) <= 0 and K.sign(C) <= 0 and K.sign(disc) <= 0
      out['prestress_stable_exact'] = not never_positive
      out['pencil_det'] = {'sign_A': K.sign(A), 'sign_C': K.sign(C), 'sign_disc': K.sign(disc)}
  return out, (K, P, flex)


if __name__ == '__main__':
  ks = [int(a) for a in sys.argv[1:]] or [58, 59, 60, 81, 82, 83]
  res = {}
  for kk in ks:
    out, _ = analyse('data/J%02d.json' % kk)
    res[kk] = out
    print('J%d' % kk, json.dumps(out), flush=True)
  json.dump(res, open('results/second_order.json' if len(sys.argv) == 1 else 'results/second_order_partial.json',
                      'w'), indent=1)
  bad = [k for k, r in res.items() if not r['second_order_rigid']]
  print('ALL SECOND-ORDER RIGID' if not bad else 'NOT CERTIFIED: %s' % bad)
  sys.exit(1 if bad else 0)
