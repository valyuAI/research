"""Quadratic extensions L = K(sqrt w) of a number field K with a fixed real embedding (sqrt w > 0).
Same interface as nf.NF. Standard library only."""
from fractions import Fraction
import nf


class QuadExt:
  def __init__(self, base, w):
    self.K = base
    self.w = w
    if self.K.sign(w) <= 0:
      raise ValueError('radicand not positive in the real embedding')
    nrm = norm_to_Q(base, w)
    self.nonsquare_certificate = ('norm', str(nrm))
    if is_rational_square(nrm):
      cert = nonresidue_certificate(base, w)
      if cert is None:
        raise ValueError('cannot certify sqrt(w) is not in K')
      self.nonsquare_certificate = ('nonresidue', cert)
    self.n = 2 * base.n
    self.zero = (base.zero, base.zero)
    self.one = (base.one, base.zero)

  def check_simple_root(self):
    return self.K.check_simple_root()

  def const(self, q): return (self.K.const(q), self.K.zero)
  def add(self, a, b): return (self.K.add(a[0], b[0]), self.K.add(a[1], b[1]))
  def sub(self, a, b): return (self.K.sub(a[0], b[0]), self.K.sub(a[1], b[1]))
  def neg(self, a): return (self.K.neg(a[0]), self.K.neg(a[1]))
  def scal(self, q, a): return (self.K.scal(q, a[0]), self.K.scal(q, a[1]))
  def is0(self, a): return self.K.is0(a[0]) and self.K.is0(a[1])

  def mul(self, a, b):
    K = self.K
    return (K.add(K.mul(a[0], b[0]), K.mul(self.w, K.mul(a[1], b[1]))),
            K.add(K.mul(a[0], b[1]), K.mul(a[1], b[0])))

  def inv(self, a):
    K = self.K
    d = K.sub(K.mul(a[0], a[0]), K.mul(self.w, K.mul(a[1], a[1])))
    di = K.inv(d)
    return (K.mul(a[0], di), K.neg(K.mul(a[1], di)))

  def div(self, a, b): return self.mul(a, self.inv(b))

  def sign(self, a):
    K = self.K
    if self.is0(a):
      return 0
    sa, sb = K.sign(a[0]), K.sign(a[1])
    if sb == 0:
      return sa
    if sa == 0:
      return sb
    if sa == sb:
      return sa
    d = K.sub(K.mul(a[0], a[0]), K.mul(self.w, K.mul(a[1], a[1])))
    sd = K.sign(d)
    if sd == 0:
      raise ValueError('nonzero element with zero norm: sqrt(w) in K?')
    return sa if sd > 0 else sb

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
    out = []
    for r in self.K.hom_roots(p):
      try:
        wv = self.K.reduce_mod(self.w, p, r)
      except ZeroDivisionError:
        continue
      s = sqrt_mod(wv, p)
      if s is not None and wv % p:
        out.append((r, s))
    return out

  def reduce_mod(self, a, p, r):
    br, s = r
    return (self.K.reduce_mod(a[0], p, br) + s * self.K.reduce_mod(a[1], p, br)) % p

  def to_float(self, a):
    return self.K.to_float(a[0]) + self.K.to_float(a[1]) * self.K.to_float(self.w) ** 0.5


def norm_to_Q(K, w):
  """Norm N_{K/Q}(w) as the determinant of multiplication by w (K = nf.NF or QuadExt)."""
  basis = basis_of(K)
  M = []
  for b in basis:
    M.append(flatten(K, K.mul(w, b)))
  return det_frac(M)


def basis_of(K):
  if isinstance(K, nf.NF):
    out = []
    for i in range(K.n):
      e = [Fraction(0)] * K.n
      e[i] = Fraction(1)
      out.append(tuple(e))
    return out
  bb = basis_of(K.K)
  return [(b, K.K.zero) for b in bb] + [(K.K.zero, b) for b in bb]


def flatten(K, a):
  if isinstance(K, nf.NF):
    return list(a)
  return flatten(K.K, a[0]) + flatten(K.K, a[1])


def det_frac(M):
  M = [list(r) for r in M]
  n = len(M)
  d = Fraction(1)
  for c in range(n):
    p = next((i for i in range(c, n) if M[i][c] != 0), None)
    if p is None:
      return Fraction(0)
    if p != c:
      M[c], M[p] = M[p], M[c]
      d = -d
    d *= M[c][c]
    for i in range(c + 1, n):
      f = M[i][c] / M[c][c]
      if f:
        for j in range(c, n):
          M[i][j] -= f * M[c][j]
  return d


def is_rational_square(q):
  q = Fraction(q)
  if q < 0:
    return False
  return isqrt_exact(q.numerator) and isqrt_exact(q.denominator)


def isqrt_exact(n):
  from math import isqrt
  r = isqrt(n)
  return r * r == n


def sqrt_mod(a, p):
  a %= p
  if a == 0:
    return 0
  if pow(a, (p - 1) // 2, p) != 1:
    return None
  if p % 4 == 3:
    return pow(a, (p + 1) // 4, p)
  # Tonelli-Shanks
  q, s = p - 1, 0
  while q % 2 == 0:
    q //= 2
    s += 1
  z = 2
  while pow(z, (p - 1) // 2, p) != p - 1:
    z += 1
  m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
  while t != 1:
    i, t2 = 0, t
    while t2 != 1:
      t2 = t2 * t2 % p
      i += 1
    b = pow(c, 1 << (m - i - 1), p)
    m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
  return r


def nonresidue_certificate(K, w, start=10007, tries=4000):
  """Certificate that w is not a square in K = Q[x]/(m) (m monic integral): a prime p with m squarefree mod p
  (so Z_(p)[theta] is integrally closed at p and every s in K with s^2 = w lies in it) and a root r of m mod p
  with w(r) a quadratic non-residue.  Then w = s^2 would give w(r) = s(r)^2, a contradiction."""
  import nfsolid
  base = K
  if not isinstance(base, nf.NF) or any(c.denominator != 1 for c in base.m):
    return None
  p = start
  while tries:
    p += 1
    if not nfsolid.is_prime(p):
      continue
    tries -= 1
    f = [int(c) % p for c in base.m]
    if not squarefree_mod_p(f, p):
      continue
    for r in nfsolid.poly_roots_mod_p(f, p):
      try:
        wv = base.reduce_mod(w, p, r)
      except ZeroDivisionError:
        continue
      if wv and pow(wv, (p - 1) // 2, p) == p - 1:
        return {'p': p, 'r': r, 'w_mod_p': wv}
  return None


def squarefree_mod_p(f, p):
  """gcd(f, f') == 1 over F_p (f low-degree-first, monic mod p)."""
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
    return a
  a, b = trimz(f), trimz([i * c for i, c in enumerate(f)][1:])
  if len(a) - 1 != len(f) - 1 or (len(b) == 1 and b[0] == 0):
    return False
  while not (len(b) == 1 and b[0] == 0):
    a, b = b, pmod_(a, b)
  return len(a) == 1
