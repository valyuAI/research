r"""Constructions for pure distance-three qudit stabilizer codes (generator side).

Everything is exact arithmetic over GF(q), q = p^m, using lookup tables.  A
"configuration" is a list of triples (u, v, lam): u, v in GF(q)^r span a line (the column
pair of the check matrix) and lam in GF(q)^* is its weight.  The check matrix has columns
A_i = u_i and B_i = lam_i v_i; it is isotropic iff sum_i lam_i u_i ^ v_i = 0.

Top layer (dimension r = mm + 2, K = GF(q^mm)):  L_a = <(1,0,a), (0,1,a w)>, a in K, where w
is the class of x in GF(q)[x]/(f) for the stored irreducible f.  Weighted zero-sum
("2-balanced") blocks of the top layer, the absorption step and the inductive recipe follow
Section 4 of the paper.
"""
import itertools, random


# ---------------------------------------------------------------- finite fields
def _poly_mulmod(a, b, mod, p):
  m = len(mod) - 1
  res = [0] * (len(a) + len(b) - 1)
  for i, x in enumerate(a):
    if x:
      for j, y in enumerate(b):
        res[i + j] = (res[i + j] + x * y) % p
  for d in range(len(res) - 1, m - 1, -1):
    c = res[d]
    if c:
      for k in range(m + 1):
        res[d - m + k] = (res[d - m + k] - c * mod[k]) % p
  out = res[:m]
  return out + [0] * (m - len(out))


def _irreducible_prime(p, deg):
  """smallest monic irreducible of degree deg over GF(p) (coefficient list, low first)."""
  for coeffs in itertools.product(range(p), repeat=deg):
    f = list(coeffs) + [1]
    if deg == 1:
      return f
    if f[0] == 0:
      continue
    ok = True
    for dd in range(1, deg // 2 + 1):
      for g in itertools.product(range(p), repeat=dd):
        g = list(g) + [1]
        r = f[:]
        for d in range(len(r) - 1, dd - 1, -1):
          c = r[d]
          if c:
            for k in range(dd + 1):
              r[d - dd + k] = (r[d - dd + k] - c * g[k]) % p
        if not any(r[:dd]):
          ok = False
          break
      if not ok:
        break
    if ok:
      return f


class GF:
  """GF(p^m); element x <-> polynomial sum c_i X^i with x = sum c_i p^i."""
  def __init__(self, p, m):
    self.p, self.m, self.q = p, m, p ** m
    self.mod = [0, 1] if m == 1 else _irreducible_prime(p, m)
    q = self.q
    vec = [[(x // p ** i) % p for i in range(m)] for x in range(q)]
    toint = lambda v: sum(c * p ** i for i, c in enumerate(v))
    self.add = [[toint([(a + b) % p for a, b in zip(vec[x], vec[y])]) for y in range(q)] for x in range(q)]
    self.neg = [toint([(-a) % p for a in vec[x]]) for x in range(q)]
    if m == 1:
      self.mul = [[(x * y) % p for y in range(q)] for x in range(q)]
    else:
      self.mul = [[toint(_poly_mulmod(vec[x], vec[y], self.mod, p)) for y in range(q)] for x in range(q)]
    self.inv = [None] + [next(y for y in range(1, q) if self.mul[x][y] == 1) for x in range(1, q)]
    self.sub = [[self.add[x][self.neg[y]] for y in range(q)] for x in range(q)]


class Ext:
  """GF(q^deg) as GF(q)[X]/(f), f monic irreducible over GF(q); elements are deg-tuples."""
  def __init__(self, F, deg):
    self.F, self.deg = F, deg
    self.f = self._irreducible()
  def _irreducible(self):
    F, deg, q = self.F, self.deg, self.F.q
    for coeffs in itertools.product(range(q), repeat=deg):
      if coeffs[0] == 0:
        continue
      f = list(coeffs) + [1]
      ok = True
      for dd in range(1, deg // 2 + 1):
        for g in itertools.product(range(q), repeat=dd):
          g = list(g) + [1]
          r = f[:]
          for d in range(len(r) - 1, dd - 1, -1):
            c = r[d]
            if c:
              for k in range(dd + 1):
                r[d - dd + k] = F.sub[r[d - dd + k]][F.mul[c][g[k]]]
          if not any(r[:dd]):
            ok = False
            break
        if not ok:
          break
      if ok:
        return f
  def mul(self, a, b):
    F, n = self.F, self.deg
    r = [0] * (2 * n - 1)
    for i in range(n):
      if a[i]:
        for j in range(n):
          r[i + j] = F.add[r[i + j]][F.mul[a[i]][b[j]]]
    for d in range(2 * n - 2, n - 1, -1):
      c = r[d]
      if c:
        for k in range(n + 1):
          r[d - n + k] = F.sub[r[d - n + k]][F.mul[c][self.f[k]]]
    return tuple(r[:n])
  def add(self, a, b):
    return tuple(self.F.add[x][y] for x, y in zip(a, b))
  def trace(self, a):
    """absolute trace K -> GF(q) (sum of Frobenius conjugates)."""
    q = self.F.q
    t = (0,) * self.deg
    x = a
    for _ in range(self.deg):
      t = self.add(t, x)
      y = (1,) + (0,) * (self.deg - 1)
      for _ in range(q):  # x^q by repeated multiplication
        y = self.mul(y, x)
      x = y
    return t


def mu(q, s):
  """maximum size of a partial line spread of PG(s-1,q)."""
  if s <= 1:
    return 0
  if s % 2 == 0:
    return (q ** s - 1) // (q * q - 1)
  return (q ** s - q ** 3) // (q * q - 1) + 1


# ---------------------------------------------------------------- geometry helpers
def plucker(F, u, v):
  r = len(u)
  return [F.sub[F.mul[u[i]][v[j]]][F.mul[v[i]][u[j]]] for i, j in itertools.combinations(range(r), 2)]


def plucker_sum(F, conf):
  tot = None
  for u, v, l in conf:
    pv = [F.mul[l][x] for x in plucker(F, u, v)]
    tot = pv if tot is None else [F.add[a][b] for a, b in zip(tot, pv)]
  return tot


class Ctx:
  def __init__(self, p, m, seed=7):
    self.F = GF(p, m)
    self.q, self.p = self.F.q, p
    self.ext = {}
    self.rng = random.Random(seed)
  def K(self, deg):
    if deg not in self.ext:
      self.ext[deg] = Ext(self.F, deg)
    return self.ext[deg]
  def top_line(self, r, a):
    K = self.K(r - 2)
    w = tuple([0, 1] + [0] * (r - 4))
    return [1, 0] + list(a), [0, 1] + list(K.mul(a, w))


# ---------------------------------------------------------------- 2-balanced blocks (Lemma 4.2)
def lagrange(F, S):
  """weights on 4 distinct points S of GF(q) killing 1, s, s^2 (third divided difference)."""
  v = {}
  for s in S:
    den = 1
    for s2 in S:
      if s2 != s:
        den = F.mul[den][F.sub[s][s2]]
    v[s] = F.inv[den]
  return v


def line_weights(C, T):
  """full-support weights on T (subset of GF(q), |T| >= 4) killing 1, s, s^2."""
  F, q = C.F, C.q
  T = list(T)
  if len(T) == q and q >= 4:
    return {s: 1 for s in T}
  if len(T) == 4:
    return lagrange(F, T)
  vecs = [lagrange(F, T[:3] + [x]) for x in T[3:]]
  for _ in range(100000):
    c = [C.rng.randrange(1, q) for _ in vecs]
    w = {s: 0 for s in T}
    for ci, v in zip(c, vecs):
      for s, val in v.items():
        w[s] = F.add[w[s]][F.mul[ci][val]]
    if all(w[s] for s in T):
      return w
  return None


def top_blocks(C, r, ntop):
  """zero-sum weighted subset of the top layer of size ntop (Lemma 4.2), or None."""
  F, q = C.F, C.q
  mm = r - 2
  if ntop == 0:
    return []
  out = []
  if q >= 4:
    sizes = list(range(4, q + 1)) if q >= 5 else [4]
    blocks, rem = [], ntop
    while rem > 0:
      if rem in sizes:
        blocks.append(rem)
        break
      cand = [s for s in sizes if rem - s >= 4]
      if not cand:
        return None
      blocks.append(max(cand))
      rem -= max(cand)
    offs = list(itertools.product(range(q), repeat=mm - 1))
    if len(blocks) > len(offs):
      return None
    for bi, size in enumerate(blocks):
      b = (0,) + offs[bi]
      T = list(range(size))
      lam = line_weights(C, T)
      if lam is None:
        return None
      for s in T:  # points b + s * 1 (direction 1 = first basis vector)
        a = (F.add[b[0]][s],) + b[1:]
        out.append((a, lam[s]))
    return out
  # q == 3: line pairs (weights 1, -1; size 6) and full planes (size 9) in planes <1, w> + b
  if mm < 2 or ntop % 3 or ntop < 6:
    return None
  nplanes = q ** (mm - 2)
  j = ntop // 3
  for nb in range(j // 3, -1, -1):
    if (j - 3 * nb) % 2 == 0 and (j - 3 * nb) // 2 + nb <= nplanes:
      na = (j - 3 * nb) // 2
      break
  else:
    return None
  offs = list(itertools.product(range(q), repeat=mm - 2))
  for pi in range(na + nb):
    off = (0, 0) + offs[pi]
    full = pi < nb
    for x in range(3):
      for y in range(3):
        if not full and x == 2:
          continue
        lam = 1 if full else (1 if x == 0 else F.neg[1])
        pt = list(off)
        pt[0] = F.add[pt[0]][x]
        pt[1] = F.add[pt[1]][y]
        out.append((tuple(pt), lam))
  return out


# ---------------------------------------------------------------- absorption (Lemma 4.3)
def absorbed_full(C, r):
  """mu_q(r) = q^(r-2) + 1 lines for r in {4,5}: all top lines with weights 1 + delta, plus one line in Pi."""
  F, q = C.F, C.q
  mm = r - 2
  K = C.K(mm)
  elems = list(itertools.product(range(q), repeat=mm))
  lam = {a: 1 for a in elems}
  one = tuple([1] + [0] * (mm - 1))
  w = tuple([0, 1] + [0] * (mm - 2))
  zero = tuple([0] * mm)
  if C.p % 2 == 1:
    d = one
    minus = tuple(F.neg[x] for x in d)
    lam[minus] = F.add[1][1]
    lam[zero] = F.neg[1]
    lam[d] = F.add[1][1]
    x, y = d, K.mul(d, w)          # defect 2 * (d ^ d w): line <d, d w>
    linf = ([0, 0] + list(x), [0, 0] + list(y))
  else:
    s = 2                          # an element of GF(q) \ {0,1} (q >= 4)
    if mm == 3:
      xx, yy = one, w              # defect s * (1 ^ w^2)
    else:
      xx = one
      yy = next(e for e in elems if K.trace(e)[0] != 0 and any(e[1:]))
    for a in [zero, xx, yy, K.add(xx, yy)]:
      lam[a] = F.add[1][s]
    linf = None
  conf = []
  for a in elems:
    u, v = C.top_line(r, a)
    conf.append((u, v, lam[a]))
  if linf is None:
    if mm == 2:
      linf = ([0, 0, 1, 0], [0, 0, 0, 1])
    else:
      linf = ([0, 0] + list(one), [0, 0] + list(K.mul(w, w)))
  tot = plucker_sum(F, conf)
  pl = plucker(F, linf[0], linf[1])
  i = next(k for k, t in enumerate(pl) if t)
  lamv = F.mul[F.neg[tot[i]]][F.inv[pl[i]]]
  conf.append((linf[0], linf[1], lamv))
  if lamv == 0 or any(plucker_sum(F, conf)):
    raise RuntimeError('absorption failed')
  return conf


# ---------------------------------------------------------------- base-case search (q in {3,4,5})
def full_support_weights(F, cols, rng, tries=3000):
  q = F.q
  r = len(cols[0][0])
  M = [[F.sub[F.mul[u[i]][v[j]]][F.mul[v[i]][u[j]]] for (u, v) in cols] for i, j in itertools.combinations(range(r), 2)]
  n = len(cols)
  piv, rk = [], 0
  for c in range(n):
    pr = next((i for i in range(rk, len(M)) if M[i][c]), None)
    if pr is None:
      continue
    M[rk], M[pr] = M[pr], M[rk]
    iv = F.inv[M[rk][c]]
    M[rk] = [F.mul[iv][x] for x in M[rk]]
    for i in range(len(M)):
      if i != rk and M[i][c]:
        f = M[i][c]
        M[i] = [F.sub[x][F.mul[f][y]] for x, y in zip(M[i], M[rk])]
    piv.append(c)
    rk += 1
  free = [c for c in range(n) if c not in piv]
  for _ in range(tries):
    lam = [0] * n
    for c in free:
      lam[c] = rng.randrange(1, q)
    for i, pc in enumerate(piv):
      s = 0
      for c in free:
        s = F.add[s][F.mul[M[i][c]][lam[c]]]
      lam[pc] = F.neg[s]
    if all(lam):
      return lam
  return None


def random_config(C, r, n, tries=600):
  F, q = C.F, C.q
  fam = [C.top_line(r, a) for a in itertools.product(range(q), repeat=r - 2)]
  fam.append(([0, 0, 1] + [0] * (r - 3), [0, 0, 0, 1] + [0] * (r - 4)))
  for _ in range(tries):
    sub = C.rng.sample(range(len(fam)), n)
    cols = [fam[i] for i in sub]
    lam = full_support_weights(F, cols, C.rng)
    if lam:
      return [(u, v, l) for (u, v), l in zip(cols, lam)]
  return None


# ---------------------------------------------------------------- inductive recipe (Theorem 4.4)
def recipe(C, r, n, memo, allow_random=True):
  """zero-sum configuration of n pairwise skew lines in GF(q)^r, or None; returns (conf, how)."""
  key = (r, n)
  if key in memo:
    return memo[key]
  q = C.q
  res = None
  if r in (4, 5) and n == mu(q, r):
    res = (absorbed_full(C, r), 'absorption')
  elif 4 <= n <= mu(q, r):
    lowmin = 5 if r - 2 == 4 else 6   # A(4) >= [5, mu], A(s) >= [6, mu] for s >= 5 (Theorem 4.4)
    lows = [0] + (list(range(mu(q, r - 2), lowmin - 1, -1)) if r - 2 >= 4 else [])
    for nlow in lows:
      ntop = n - nlow
      if ntop < 0 or ntop > q ** (r - 2):
        continue
      blk = top_blocks(C, r, ntop)
      if blk is None:
        continue
      low = []
      if nlow:
        sub = recipe(C, r - 2, nlow, memo, allow_random)
        if sub is None:
          continue
        low = sub[0]
      conf = [tuple(C.top_line(r, a)) + (l,) for a, l in blk] + [([0, 0] + list(u), [0, 0] + list(v), l) for u, v, l in low]
      res = (conf, 'blocks' if nlow == 0 else f'blocks+lower({nlow})')
      break
    if res is None and allow_random and r in (4, 5):
      conf = random_config(C, r, n)
      if conf is not None:
        res = (conf, 'search')
  memo[key] = res
  return res


def to_check_matrix(F, conf):
  r = len(conf[0][0])
  A = [[u[i] for u, v, l in conf] for i in range(r)]
  B = [[F.mul[l][v[i]] for u, v, l in conf] for i in range(r)]
  return A, B
