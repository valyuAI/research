"""Exact validation of a polyhedron with coordinates in a number field, and modular rigidity-matrix rank.
Standard library only."""
import json
from fractions import Fraction
from nf import NF


def load(path):
  d = json.load(open(path))
  K = NF(d['minpoly'], Fraction(d['interval'][0]), Fraction(d['interval'][1]))
  conv = lambda comp: tuple(Fraction(c) for c in comp)
  for w in d.get('tower', []):
    import tower
    w = conv_elem(w, K)
    K = tower.QuadExt(K, w)
  V = [tuple(conv_elem(comp, K) for comp in v) for v in d['vertices']]
  return d['name'], K, V, d['faces']


def conv_elem(x, K):
  """Nested lists of rational strings -> field element of K (NF: flat list; QuadExt: pair)."""
  if hasattr(K, 'K'):
    return (conv_elem(x[0], K.K), conv_elem(x[1], K.K))
  return tuple(Fraction(c) for c in x)


def edges_of(faces):
  E = set()
  for f in faces:
    for i in range(len(f)):
      E.add(tuple(sorted((f[i], f[(i + 1) % len(f)]))))
  return sorted(E)


def validate(K, V, faces, edge_len_sq=1):
  """Centre at the vertex centroid; exact checks: Sturm-isolated embedding, planarity, strict convexity,
  unit edges, regular faces, Euler characteristic, each vertex in >= 3 faces, edges = face boundary pairs."""
  out = {}
  if not K.check_simple_root():
    raise ValueError('isolating interval does not contain exactly one real root')
  n = len(V)
  c = tuple(K.scal(Fraction(1, n), sumK(K, (v[k] for v in V))) for k in range(3))
  P = [K.vsub(v, c) for v in V]
  A = []
  for f in faces:
    nrm = K.cross(K.vsub(P[f[1]], P[f[0]]), K.vsub(P[f[2]], P[f[0]]))
    h = K.dot(nrm, P[f[0]])
    A.append(tuple(K.div(x, h) for x in nrm))
  for fi, f in enumerate(faces):
    for v in f:
      if not K.is0(K.sub(K.dot(P[v], A[fi]), K.one)):
        raise ValueError(f'face {fi} not planar')
    fs = set(f)
    for v in range(n):
      if v not in fs and K.sign(K.sub(K.one, K.dot(P[v], A[fi]))) <= 0:
        raise ValueError(f'vertex {v} not strictly inside facet {fi}')
  E = edges_of(faces)
  for i, j in E:
    d = K.vsub(P[i], P[j])
    if not K.is0(K.sub(K.dot(d, d), K.const(edge_len_sq))):
      raise ValueError(f'edge {i}-{j} not of unit length')
  for f in faces:
    m = len(f)
    for s in range(1, m // 2 + 1):
      vals = set()
      for i in range(m):
        d = K.vsub(P[f[i]], P[f[(i + s) % m]])
        vals.add(K.dot(d, d))
      if len(vals) != 1:
        raise ValueError('face not regular')
  if n - len(E) + len(faces) != 2:
    raise ValueError('Euler characteristic')
  deg = [0] * n
  for f in faces:
    for v in f:
      deg[v] += 1
  if min(deg) < 3:
    raise ValueError('vertex in fewer than 3 faces')
  # every edge lies in exactly two faces
  cnt = {}
  for f in faces:
    for i in range(len(f)):
      e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
      cnt[e] = cnt.get(e, 0) + 1
  if set(cnt.values()) != {2}:
    raise ValueError('edge not in exactly two faces')
  out.update(V=n, E=len(E), F=len(faces), face_sizes=sorted(len(f) for f in faces))
  return P, A, E, out


def sumK(K, it):
  r = K.zero
  for x in it:
    r = K.add(r, x)
  return r


def find_prime(K, P, A, start=1000003, avoid=()):
  """Smallest prime >= start admitting a ring map to F_p under which all coordinates reduce."""
  p = start
  while True:
    if is_prime(p):
      for r in K.hom_roots(p):
        try:
          for X in list(P) + list(A):
            for c in X:
              K.reduce_mod(c, p, r)
        except ZeroDivisionError:
          continue
        if (p, r) not in avoid:
          return p, r
    p += 1


def find_prime_old(K, P, A, start=1000003, avoid=()):
  dens = 1
  for X in list(P) + list(A):
    for comp in X:
      for c in comp:
        dens = dens * c.denominator // gcd(dens, c.denominator)
  mp = K.m
  p = start
  while True:
    if is_prime(p) and dens % p and all(c.denominator % p == 0 or True for c in mp):
      for t in range(p) if p < 3000 else root_candidates(mp, p):
        if sum(int(c) * pow(t, i, p) for i, c in enumerate(mp)) % p == 0:
          if (p, t) not in avoid:
            return p, t
    p += 1


def root_candidates(mp, p):
  # roots of m mod p via gcd(x^p - x, m) is overkill here; brute force over a range is too slow for big p.
  # Use Cantor-Zassenhaus-free approach: since degrees are small, test all t in [0, p) only for p < 3000.
  # For larger p, find roots with the polynomial-gcd method.
  return poly_roots_mod_p([int(c) % p for c in mp], p)


def poly_roots_mod_p(f, p):
  """All roots of f (low-degree-first ints) in F_p using gcd with x^p - x and equal-degree splitting."""
  import random
  def trimz(a):
    a = [x % p for x in a]
    while len(a) > 1 and a[-1] == 0:
      a.pop()
    return a
  def pmod_(a, b):
    a = trimz(a); b = trimz(b)
    inv = pow(b[-1], -1, p)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
      c = a[-1] * inv % p
      k = len(a) - len(b)
      for i, y in enumerate(b):
        a[i + k] = (a[i + k] - c * y) % p
      a = trimz(a)
      if len(a) < len(b):
        break
    return a
  def pmul_(a, b, m):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
      for j, y in enumerate(b):
        r[i + j] = (r[i + j] + x * y) % p
    return pmod_(r, m)
  def ppow(base, e, m):
    r = [1]
    while e:
      if e & 1:
        r = pmul_(r, base, m)
      base = pmul_(base, base, m)
      e >>= 1
    return r
  def pgcd(a, b):
    a, b = trimz(a), trimz(b)
    while not (len(b) == 1 and b[0] == 0):
      a, b = b, pmod_(a, b)
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]
  f = trimz(f)
  xp = ppow([0, 1], p, f)
  g = pgcd(f, trimz([(xp[i] if i < len(xp) else 0) - (1 if i == 1 else 0) for i in range(max(len(xp), 2))]))
  roots = []
  stack = [g]
  rnd = random.Random(1)
  while stack:
    h = stack.pop()
    if len(h) == 1:
      continue
    if len(h) == 2:
      roots.append((-h[0]) * pow(h[1], -1, p) % p)
      continue
    while True:
      a = rnd.randrange(p)
      w = ppow([a, 1], (p - 1) // 2, h)
      d = pgcd(h, trimz([(w[i] if i < len(w) else 0) - (1 if i == 0 else 0) for i in range(max(len(w), 1))]))
      if 1 < len(d) < len(h):
        stack.append(d)
        q = h
        # h / d
        stack.append(pdiv_exact(h, d, p))
        break
  return sorted(set(roots))


def pdiv_exact(a, b, p):
  a = [x % p for x in a]
  inv = pow(b[-1], -1, p)
  q = [0] * (len(a) - len(b) + 1)
  for k in range(len(a) - len(b), -1, -1):
    c = a[k + len(b) - 1] * inv % p
    q[k] = c
    for i, y in enumerate(b):
      a[i + k] = (a[i + k] - c * y) % p
  return q


def gcd(a, b):
  while b:
    a, b = b, a % b
  return a


def is_prime(n):
  if n < 2:
    return False
  for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
    if n % q == 0:
      return n == q
  d, s = n - 1, 0
  while d % 2 == 0:
    d //= 2
    s += 1
  for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
    x = pow(a, d, n)
    if x in (1, n - 1):
      continue
    for _ in range(s - 1):
      x = x * x % n
      if x == n - 1:
        break
    else:
      return False
  return True


def rigidity_rows_mod(K, P, A, E, p, t):
  red = lambda x: K.reduce_mod(x, p, t)
  Pp = [tuple(red(c) for c in X) for X in P]
  Ap = [tuple(red(c) for c in X) for X in A]
  nV = len(P)
  inc = []
  return Pp, Ap


def rank_mod_p(rows, ncols, p):
  """Rank of a matrix given as list of dict rows over F_p (Gaussian elimination)."""
  piv = {}
  for r in rows:
    r = {c: v % p for c, v in r.items() if v % p}
    while r:
      c = min(r)
      if c in piv:
        f = r[c]
        for cc, val in piv[c].items():
          nv = (r.get(cc, 0) - f * val) % p
          if nv:
            r[cc] = nv
          else:
            r.pop(cc, None)
      else:
        inv = pow(r[c], -1, p)
        piv[c] = {cc: val * inv % p for cc, val in r.items()}
        break
  return len(piv)


def rigidity_rank_mod_p(K, P, A, E, faces, p, t):
  red = lambda x: K.reduce_mod(x, p, t)
  Pp = [tuple(red(c) for c in X) for X in P]
  Ap = [tuple(red(c) for c in X) for X in A]
  nV, nF = len(P), len(A)
  rows = []
  for i, j in E:
    r = {}
    for k in range(3):
      d = (Pp[i][k] - Pp[j][k]) % p
      if d:
        r[3 * i + k] = d
        r[3 * j + k] = (-d) % p
    rows.append(r)
  for fi, f in enumerate(faces):
    for i in f:
      r = {}
      for k in range(3):
        if Ap[fi][k]:
          r[3 * i + k] = Ap[fi][k]
        if Pp[i][k]:
          r[3 * nV + 3 * fi + k] = Pp[i][k]
      rows.append(r)
  return rank_mod_p(rows, 3 * (nV + nF), p), len(rows), 3 * (nV + nF)
