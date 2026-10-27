"""Independent second checker (standard library only; shares no code with nf.py / tower.py / nfsolid.py).

Differences from checker 1 (check1_rank.py):
  * formulation: vertex-only. Unknown velocities v_i of the vertices only; constraints: edge lengths and, for
    every face with k >= 4 vertices, the k - 3 determinant conditions det(b - a, c - a, d - a) = 0 (a, b, c the
    first three vertices of the face, d any further vertex).  When every face has three non-collinear vertices,
    the first-order motions of this system are exactly the vertex parts of the first-order motions of the
    point-hyperplane system of arXiv:2607.09252, and the projection is injective; so rigidity <=> rank 3V - 6.
  * arithmetic: equalities are checked formally in Q[x]/(m) (or its quadratic extension by y^2 = w), which is
    sound for any real root theta of m in the given interval (evaluation is a ring homomorphism; no
    irreducibility needed); inequalities and ranks are certified with rigorous fixed-point interval arithmetic
    at that root (outward rounding), not by modular reduction.
  * flexibility: an explicit exact first-order flex (certificates/flex_vectors.json) is checked to satisfy all
    linearised constraints formally and to be non-trivial (some pairwise distance has a non-zero derivative,
    certified by interval arithmetic).
usage: python3 check2_independent.py [J numbers]"""
import json, sys, time
from fractions import Fraction
from math import isqrt

PREC = 640  # bits of fixed-point precision


def need(cond, msg='check failed'):
  """Explicit check that is not removed by python -O."""
  if not cond:
    raise ValueError(msg)


# ---------------- formal arithmetic in Q[x]/(m) and Q[x]/(m)[y]/(y^2 - w) ----------------
class Ring:
  def __init__(self, m, w=None):
    self.m = [Fraction(c) for c in m]
    need(self.m[-1] == 1, 'self.m[-1] == 1')
    self.n = len(m) - 1
    self.w = w  # None or base element

  def bmul(self, a, b):
    n = self.n
    r = [Fraction(0)] * (2 * n - 1)
    for i in range(n):
      if a[i]:
        for j in range(n):
          if b[j]:
            r[i + j] += a[i] * b[j]
    for k in range(2 * n - 2, n - 1, -1):
      c = r[k]
      if c:
        for j in range(n + 1):
          r[k - n + j] -= c * self.m[j]
    return tuple(r[:n])

  def zero(self):
    z = tuple([Fraction(0)] * self.n)
    return (z, z) if self.w is not None else z

  def cst(self, q):
    b = tuple([Fraction(q)] + [Fraction(0)] * (self.n - 1))
    return (b, tuple([Fraction(0)] * self.n)) if self.w is not None else b

  def add(self, a, b):
    if self.w is None:
      return tuple(x + y for x, y in zip(a, b))
    return (tuple(x + y for x, y in zip(a[0], b[0])), tuple(x + y for x, y in zip(a[1], b[1])))

  def neg(self, a):
    if self.w is None:
      return tuple(-x for x in a)
    return (tuple(-x for x in a[0]), tuple(-x for x in a[1]))

  def sub(self, a, b):
    return self.add(a, self.neg(b))

  def mul(self, a, b):
    if self.w is None:
      return self.bmul(a, b)
    add = lambda u, v: tuple(x + y for x, y in zip(u, v))
    return (add(self.bmul(a[0], b[0]), self.bmul(self.w, self.bmul(a[1], b[1]))),
            add(self.bmul(a[0], b[1]), self.bmul(a[1], b[0])))

  def iszero(self, a):
    if self.w is None:
      return all(x == 0 for x in a)
    return all(x == 0 for x in a[0]) and all(x == 0 for x in a[1])


# ---------------- rigorous fixed-point intervals: (lo, hi) integers, value in [lo, hi] * 2^-PREC ----------------
ONE = 1 << PREC


def iv_frac(q):
  q = Fraction(q)
  return ((q.numerator << PREC) // q.denominator, -((-q.numerator << PREC) // q.denominator))


def iv_add(a, b):
  return (a[0] + b[0], a[1] + b[1])


def iv_sub(a, b):
  return (a[0] - b[1], a[1] - b[0])


def iv_mul(a, b):
  c = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
  return (min(c) >> PREC, -((-max(c)) >> PREC))


def iv_div(a, b):
  need(b[0] > 0 or b[1] < 0, 'division by interval containing 0')
  c = [Fraction(x * ONE, y) for x in a for y in b]
  lo, hi = min(c), max(c)
  return (lo.numerator // lo.denominator, -((-hi.numerator) // hi.denominator))


def iv_sqrt(a):
  need(a[0] >= 0, 'a[0] >= 0')
  return (isqrt(a[0] << PREC), isqrt(a[1] << PREC) + 1)


def iv_sign(a):
  return 1 if a[0] > 0 else (-1 if a[1] < 0 else 0)


class Embedding:
  """A real root theta of m in [lo, hi] (sign change certified exactly), narrowed by bisection; sqrt(w(theta))."""

  def __init__(self, R, lo, hi):
    self.R = R
    f = lambda x: sum(c * x ** i for i, c in enumerate(R.m))
    lo, hi = Fraction(lo), Fraction(hi)
    flo, fhi = f(lo), f(hi)
    need(flo * fhi < 0, 'no sign change of the minimal polynomial on the interval')
    while hi - lo > Fraction(1, 1 << (PREC + 8)):
      mid = (lo + hi) / 2
      fm = f(mid)
      if fm == 0:
        lo = hi = mid
        break
      if (fm < 0) == (flo < 0):
        lo, flo = mid, fm
      else:
        hi = mid
    self.theta = (iv_frac(lo)[0], iv_frac(hi)[1])
    self.lo, self.hi = lo, hi
    if R.w is not None:
      wv = self.base(R.w)
      need(wv[0] > 0, 'radicand not certified positive')
      self.s = iv_sqrt(wv)

  def base(self, a):
    r = (0, 0)
    for c in reversed(a):
      r = iv_add(iv_mul(r, self.theta), iv_frac(c))
    return r

  def __call__(self, a):
    if self.R.w is None:
      return self.base(a)
    return iv_add(self.base(a[0]), iv_mul(self.base(a[1]), self.s))


# ---------------- solid loading and exact validation ----------------
def load(path):
  d = json.load(open(path))
  m = [int(c) for c in d['minpoly']]
  R = Ring(m)
  if d.get('tower'):
    need(len(d['tower']) == 1, "len(d['tower']) == 1")
    R = Ring(m, tuple(Fraction(c) for c in d['tower'][0]))
    el = lambda x: (tuple(Fraction(c) for c in x[0]), tuple(Fraction(c) for c in x[1]))
  else:
    el = lambda x: tuple(Fraction(c) for c in x)
  V = [tuple(el(c) for c in v) for v in d['vertices']]
  emb = Embedding(R, d['interval'][0], d['interval'][1])
  return d['name'], R, emb, V, d['faces']


def vsub(R, u, v):
  return tuple(R.sub(x, y) for x, y in zip(u, v))


def dot(R, u, v):
  r = R.zero()
  for x, y in zip(u, v):
    r = R.add(r, R.mul(x, y))
  return r


def cross(R, u, v):
  return (R.sub(R.mul(u[1], v[2]), R.mul(u[2], v[1])), R.sub(R.mul(u[2], v[0]), R.mul(u[0], v[2])),
          R.sub(R.mul(u[0], v[1]), R.mul(u[1], v[0])))


def validate(R, emb, V, F):
  n = len(V)
  E = {}
  for f in F:
    for i in range(len(f)):
      e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
      E[e] = E.get(e, 0) + 1
  need(set(E.values()) == {2}, 'every edge must lie in exactly two faces')
  need(n - len(E) + len(F) == 2, 'Euler characteristic')
  one = R.cst(1)
  for (i, j) in E:
    d = vsub(R, V[i], V[j])
    need(R.iszero(R.sub(dot(R, d, d), one)), 'edge length not 1')
  for f in F:
    a, b, c = (V[f[0]], V[f[1]], V[f[2]])
    nrm = cross(R, vsub(R, b, a), vsub(R, c, a))
    for d in f[3:]:
      need(R.iszero(dot(R, nrm, vsub(R, V[d], a))), 'face not planar')
    k = len(f)
    for s in range(2, k // 2 + 1):  # equal chords of every step: with unit sides, a regular k-gon
      ref = None
      for i in range(k):
        dd = vsub(R, V[f[i]], V[f[(i + s) % k]])
        q = dot(R, dd, dd)
        if ref is None:
          ref = q
        need(R.iszero(R.sub(q, ref)), 'face not regular')
    # strict convexity: all other vertices strictly on one side of the face plane
    nrm_iv = [emb(x) for x in nrm]
    sg = set()
    fs = set(f)
    for v in range(n):
      if v not in fs:
        w = [emb(x) for x in vsub(R, V[v], a)]
        t = iv_add(iv_add(iv_mul(nrm_iv[0], w[0]), iv_mul(nrm_iv[1], w[1])), iv_mul(nrm_iv[2], w[2]))
        sg.add(iv_sign(t))
    need(len(sg) == 1 and 0 not in sg, 'not strictly convex')
    # face polygon convex in the given cyclic order: every face vertex weakly... strictly left of every side
    Pf = [[emb(x) for x in V[u]] for u in f]
    sg2 = set()
    for i in range(k):
      e = [iv_sub(Pf[(i + 1) % k][t], Pf[i][t]) for t in range(3)]
      for j in range(k):
        if j in (i, (i + 1) % k):
          continue
        u = [iv_sub(Pf[j][t], Pf[i][t]) for t in range(3)]
        cr = [iv_sub(iv_mul(e[1], u[2]), iv_mul(e[2], u[1])), iv_sub(iv_mul(e[2], u[0]), iv_mul(e[0], u[2])),
              iv_sub(iv_mul(e[0], u[1]), iv_mul(e[1], u[0]))]
        t = iv_add(iv_add(iv_mul(cr[0], nrm_iv[0]), iv_mul(cr[1], nrm_iv[1])), iv_mul(cr[2], nrm_iv[2]))
        sg2.add(iv_sign(t))
    need(k == 3 or (len(sg2) == 1 and 0 not in sg2), 'face polygon not convex in the given order')
  return sorted(E)


# ---------------- vertex-only rigidity matrix ----------------
def jacobian(R, V, F, E):
  """Rows as dicts column -> exact element."""
  rows = []
  for i, j in E:
    d = vsub(R, V[i], V[j])
    r = {}
    for k in range(3):
      r[3 * i + k] = d[k]
      r[3 * j + k] = R.neg(d[k])
    rows.append(r)
  for f in F:
    a, b, c = V[f[0]], V[f[1]], V[f[2]]
    u, v = vsub(R, b, a), vsub(R, c, a)
    for d in f[3:]:
      w = vsub(R, V[d], a)
      gb, gc, gd = cross(R, v, w), cross(R, w, u), cross(R, u, v)
      ga = tuple(R.neg(R.add(R.add(gb[k], gc[k]), gd[k])) for k in range(3))
      r = {}
      for vert, g in ((f[0], ga), (f[1], gb), (f[2], gc), (d, gd)):
        for k in range(3):
          r[3 * vert + k] = R.add(r.get(3 * vert + k, R.zero()), g[k])
      rows.append(r)
  return rows


def interval_rank(emb, rows, ncols):
  """Lower bound for the rank of the real matrix at the embedded root (interval Gaussian elimination with
  partial pivoting chosen by midpoint magnitude; a pivot is accepted only if its interval excludes 0)."""
  M = [{c: emb(x) for c, x in r.items()} for r in rows]
  M = [{c: x for c, x in r.items() if x != (0, 0)} for r in M]
  remaining = list(range(len(M)))
  rank = 0
  for col in range(ncols):
    best, bv = None, -1
    for i in remaining:
      x = M[i].get(col)
      if x is not None:
        mag = min(abs(x[0]), abs(x[1])) if iv_sign(x) else 0
        if mag > bv:
          best, bv = i, mag
    if best is None or bv <= 0:
      continue
    piv = M[best][col]
    remaining.remove(best)
    rank += 1
    prow = M[best]
    for i in remaining:
      x = M[i].get(col)
      if x is None:
        continue
      f = iv_div(x, piv)
      r = M[i]
      for c, y in prow.items():
        if c == col:
          continue
        r[c] = iv_sub(r.get(c, (0, 0)), iv_mul(f, y))
      del r[col]
  return rank


def check_flex(R, emb, V, E, rows, vec):
  """vec: list of 3-tuples of exact elements (vertex velocities)."""
  flat = {}
  for i, v in enumerate(vec):
    for k in range(3):
      flat[3 * i + k] = v[k]
  for r in rows:
    s = R.zero()
    for c, x in r.items():
      s = R.add(s, R.mul(x, flat[c]))
    if not R.iszero(s):
      return {'ok': False, 'reason': 'not a first-order motion'}
  n = len(V)
  for i in range(n):
    for j in range(i + 1, n):
      q = dot(R, vsub(R, V[i], V[j]), vsub(R, vec[i], vec[j]))
      if iv_sign(emb(q)) != 0:
        return {'ok': True, 'witness_pair': [i, j]}
  return {'ok': False, 'reason': 'could not certify non-triviality'}


def main(ks):
  try:
    flexcert = json.load(open('certificates/flex_vectors.json'))
  except FileNotFoundError:
    flexcert = {}
  out = {}
  for k in ks:
    t0 = time.time()
    name, R, emb, V, F = load('data/J%02d.json' % k)
    E = validate(R, emb, V, F)
    rows = jacobian(R, V, F, E)
    ncols = 3 * len(V)
    res = {'name': name, 'V': len(V), 'E': len(E), 'F': len(F), 'rows': len(rows), 'cols': ncols}
    if RANK_ONLY:
      rk = interval_rank(emb, rows, ncols)
      res['rank_lower_bound'] = rk
      res['verdict'] = 'rank >= %d = 3V - 6 - %d' % (rk, ncols - 6 - rk)
    elif str(k) in flexcert:
      el = (lambda x: (tuple(Fraction(c) for c in x[0]), tuple(Fraction(c) for c in x[1]))) if R.w is not None \
        else (lambda x: tuple(Fraction(c) for c in x))
      vec = [tuple(el(c) for c in v) for v in flexcert[str(k)]['velocities']]
      res['flex'] = check_flex(R, emb, V, E, rows, vec)
      res['verdict'] = 'first-order flexible' if res['flex']['ok'] else 'FAILED'
    else:
      rk = interval_rank(emb, rows, ncols)
      res['rank_lower_bound'] = rk
      res['verdict'] = 'first-order rigid' if rk == ncols - 6 else 'UNDECIDED'
    res['seconds'] = round(time.time() - t0, 1)
    out[k] = res
    print('J%-3d %-42s %s  (%s)' % (k, name[:42], res['verdict'], res['seconds']), flush=True)
  return out


RANK_ONLY = '--rank-only' in sys.argv  # negative control: interval rank lower bound for every solid

if __name__ == '__main__':
  if RANK_ONLY:
    sys.argv.remove('--rank-only')
  ks = [int(a) for a in sys.argv[1:]] or list(range(1, 93))
  out = main(ks)
  fn = 'results/check2_rank_only.json' if RANK_ONLY else (
    'results/check2.json' if len(sys.argv) == 1 else 'results/check2_partial.json')
  json.dump(out, open(fn, 'w'), indent=1)
  if RANK_ONLY:
    sys.exit(0)
  bad = [k for k, r in out.items() if r['verdict'] not in ('first-order rigid', 'first-order flexible')]
  print('ALL CERTIFIED' if not bad else 'NOT CERTIFIED: %s' % bad)
  sys.exit(1 if bad else 0)
