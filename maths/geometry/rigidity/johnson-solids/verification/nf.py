"""Exact arithmetic in a number field Q(theta) = Q[x]/(m), m monic with integer coefficients,
with a fixed real embedding given by a rational isolating interval for theta. Standard library only."""
from fractions import Fraction


class NF:
  def __init__(self, minpoly, lo, hi):
    """minpoly: integer coefficients [c0, c1, ..., c_{n-1}, 1] (monic, low degree first)."""
    if not minpoly or minpoly[-1] != 1:
      raise ValueError('minimal polynomial must be monic')
    self.m = [Fraction(c) for c in minpoly]
    self.n = len(minpoly) - 1
    self.lo, self.hi = Fraction(lo), Fraction(hi)
    if self._msign(self.lo) * self._msign(self.hi) >= 0:
      raise ValueError("isolating interval does not bracket a sign change")
    self.zero = tuple([Fraction(0)] * self.n)
    self.one = tuple([Fraction(1)] + [Fraction(0)] * (self.n - 1))

  def _meval(self, x):
    r = Fraction(0)
    for c in reversed(self.m):
      r = r * x + c
    return r

  def _msign(self, x):
    v = self._meval(x)
    return (v > 0) - (v < 0)

  def check_simple_root(self):
    """Verify via Sturm sequence that m has exactly one real root in [lo, hi]."""
    return sturm_count(self.m, self.lo, self.hi) == 1

  def const(self, q):
    return tuple([Fraction(q)] + [Fraction(0)] * (self.n - 1))

  def add(self, a, b): return tuple(x + y for x, y in zip(a, b))
  def sub(self, a, b): return tuple(x - y for x, y in zip(a, b))
  def neg(self, a): return tuple(-x for x in a)
  def scal(self, q, a): return tuple(q * x for x in a)
  def is0(self, a): return all(x == 0 for x in a)

  def mul(self, a, b):
    n = self.n
    prod = [Fraction(0)] * (2 * n - 1)
    for i, x in enumerate(a):
      if x:
        for j, y in enumerate(b):
          if y:
            prod[i + j] += x * y
    for k in range(2 * n - 2, n - 1, -1):
      c = prod[k]
      if c:
        prod[k] = Fraction(0)
        for j in range(n):
          prod[k - n + j] -= c * self.m[j]
    return tuple(prod[:n])

  def inv(self, a):
    # extended Euclid in Q[x] between a(x) and m(x)
    if self.is0(a):
      raise ZeroDivisionError
    r0, r1 = trim(list(self.m)), trim(list(a))
    s0, s1 = [Fraction(0)], [Fraction(1)]
    while not (len(r1) == 1 and r1[0] == 0):
      q, r = pdivmod(r0, r1)
      r0, r1 = r1, r
      s0, s1 = s1, psub(s0, pmul(q, s1))
    # r0 is the gcd (a constant since m irreducible); s0 * a = r0 mod m
    if len(r0) != 1:
      raise ValueError("minimal polynomial not irreducible?")
    c = r0[0]
    s = [x / c for x in s0]
    s = pmod(s, self.m)
    s = s + [Fraction(0)] * (self.n - len(s))
    return tuple(s[:self.n])

  def div(self, a, b): return self.mul(a, self.inv(b))

  def sign(self, a):
    if self.is0(a):
      return 0
    lo, hi = self.lo, self.hi
    for _ in range(400):
      l, h = interval_eval(a, lo, hi)
      if l > 0:
        return 1
      if h < 0:
        return -1
      mid = (lo + hi) / 2
      if self._msign(mid) == 0:
        v = sum(c * mid ** i for i, c in enumerate(a))
        return (v > 0) - (v < 0)
      if self._msign(lo) * self._msign(mid) < 0:
        hi = mid
      else:
        lo = mid
      self.lo, self.hi = lo, hi
    raise ValueError("sign not resolved")

  def to_float(self, a):
    t = float((self.lo + self.hi) / 2)
    return sum(float(c) * t ** i for i, c in enumerate(a))

  def dot(self, u, v):
    r = self.zero
    for x, y in zip(u, v):
      r = self.add(r, self.mul(x, y))
    return r

  def vsub(self, u, v): return tuple(self.sub(x, y) for x, y in zip(u, v))

  def cross(self, u, v):
    return (self.sub(self.mul(u[1], v[2]), self.mul(u[2], v[1])),
            self.sub(self.mul(u[2], v[0]), self.mul(u[0], v[2])),
            self.sub(self.mul(u[0], v[1]), self.mul(u[1], v[0])))

  def hom_roots(self, p):
    """Roots of the minimal polynomial modulo p (each defines a ring map Z_(p)[theta] -> F_p)."""
    import nfsolid
    if any(c.denominator % p == 0 for c in self.m):
      return []
    return nfsolid.poly_roots_mod_p([int(c) % p for c in self.m], p)

  def reduce_mod(self, a, p, t):
    """Image of a under theta -> t in F_p (requires p-integral coefficients)."""
    r = 0
    for c in reversed(a):
      if c.denominator % p == 0:
        raise ZeroDivisionError("coefficient not p-integral")
      r = (r * t + c.numerator * pow(c.denominator, -1, p)) % p
    return r


def interval_eval(a, lo, hi):
  """Enclosure of sum a_i x^i for x in [lo, hi] (Horner with interval arithmetic)."""
  L = H = Fraction(0)
  for c in reversed(a):
    cands = [L * lo, L * hi, H * lo, H * hi]
    L, H = min(cands) + c, max(cands) + c
  return L, H


def trim(p):
  while len(p) > 1 and p[-1] == 0:
    p.pop()
  return p


def pmul(a, b):
  r = [Fraction(0)] * (len(a) + len(b) - 1)
  for i, x in enumerate(a):
    for j, y in enumerate(b):
      r[i + j] += x * y
  return trim(r)


def psub(a, b):
  n = max(len(a), len(b))
  r = [(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(n)]
  return trim([Fraction(x) for x in r])


def pdivmod(a, b):
  a = trim(list(a)); b = trim(list(b))
  if len(a) < len(b):
    return [Fraction(0)], a
  q = [Fraction(0)] * (len(a) - len(b) + 1)
  r = list(a)
  while len(r) >= len(b) and not (len(r) == 1 and r[0] == 0):
    c = r[-1] / b[-1]
    k = len(r) - len(b)
    q[k] = c
    for i, y in enumerate(b):
      r[i + k] -= c * y
    r.pop()
    trim(r)
    if len(r) < len(b):
      break
  return trim(q), trim(r) if r else [Fraction(0)]


def pmod(a, m):
  return pdivmod(a, m)[1]


def pderiv(p):
  return trim([i * c for i, c in enumerate(p)][1:] or [Fraction(0)])


def sturm_count(m, lo, hi):
  seq = [trim(list(m)), pderiv(list(m))]
  while not (len(seq[-1]) == 1 and seq[-1][0] == 0):
    r = pmod(seq[-2], seq[-1])
    r = [-x for x in r]
    if len(r) == 1 and r[0] == 0:
      break
    seq.append(trim(r))
  def var(x):
    vals = [sum(c * x ** i for i, c in enumerate(p)) for p in seq]
    vals = [v for v in vals if v != 0]
    return sum(1 for u, v in zip(vals, vals[1:]) if (u > 0) != (v > 0))
  return var(lo) - var(hi)
