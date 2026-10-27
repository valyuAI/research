#!/usr/bin/env python3
"""Explicit upper-bound decompositions, each verified coefficient by coefficient.

  A2 = F_2[x]/((x^2+x+1)^2)     rank 9   (p-adic Karatsuba; works over any F_q with p irreducible)
  A1 = F_2[x]/((x+1)^2)         rank 3
  C6 = F_2[x]/(x^6+1)           rank 12  (CRT: C6 = A1 x A2)
  B5 = F_5[x]/((x^2+2)^2)       rank 8   (evaluation at 0,1,2,3, one quadratic place, infinity)

A decomposition is a list of terms (a, b, c) of coefficient vectors in the monomial basis
1, x, ..., x^{n-1}: for all f, g in A,
  f g = sum_t (a_t . f) (b_t . g) c_t   in A (coordinates mod q).
"""
import json
import sys


def polymulmod(f, g, mod, q):
  """f, g coefficient lists (low to high); returns f*g reduced modulo monic mod, over F_q."""
  t = [0] * (len(f) + len(g) - 1)
  for i, a in enumerate(f):
    for j, b in enumerate(g):
      t[i + j] = (t[i + j] + a * b) % q
  n = len(mod) - 1
  for d in range(len(t) - 1, n - 1, -1):
    c = t[d]
    if c:
      for k in range(n + 1):
        t[d - n + k] = (t[d - n + k] - c * mod[k]) % q
  t = t[:n] + [0] * max(0, n - len(t))
  return t


def verify(terms, mod, q):
  n = len(mod) - 1
  for i in range(n):
    for j in range(n):
      e_i = [1 if k == i else 0 for k in range(n)]
      e_j = [1 if k == j else 0 for k in range(n)]
      z = polymulmod(e_i, e_j, mod, q)
      for k in range(n):
        s = sum(a[i] * b[j] * c[k] for a, b, c in terms) % q
        if s != z[k]:
          return False
  return True


def linmap(func, n, q):
  """Matrix (list of output vectors per input basis vector) of a linear map F_q^n -> F_q^m."""
  return [func([1 if k == i else 0 for k in range(n)]) for i in range(n)]


def compose_form(form, M):
  """form: linear form on F_q^m (vector); M: images of basis e_i of F_q^n. Returns form o M."""
  return [sum(fk * mk for fk, mk in zip(form, col)) for col in M]


def padic_karatsuba(p, q):
  """Rank-9 decomposition of F_q[x]/(p^2), p monic irreducible of degree 2."""
  # p^2 as a polynomial
  sq = [0] * 5
  for i in range(3):
    for j in range(3):
      sq[i + j] = (sq[i + j] + p[i] * p[j]) % q
  n = 4

  def split(fv):
    # f = f0 + f1 p with deg f0, f1 <= 1: long division by p
    r = list(fv)
    quo = [0, 0]
    for d in (3, 2):
      c = r[d]
      if c:
        quo[d - 2] = c
        for k in range(3):
          r[d - 2 + k] = (r[d - 2 + k] - c * p[k]) % q
    return r[:2], quo
  F0 = linmap(lambda v: split(v)[0], n, q)
  F1 = linmap(lambda v: split(v)[1], n, q)
  # linear forms (on F_q^2) of Karatsuba for a full product of two linear polynomials
  kar = [([1, 0], [1, 0], [1, q - 1, 0]),   # a0 b0 contributes to x^0 and -x^1
         ([0, 1], [0, 1], [0, q - 1, 1]),   # a1 b1 contributes to x^2 and -x^1
         ([1, 1], [1, 1], [0, 1, 0])]       # (a0+a1)(b0+b1) contributes to x^1
  # fg = F + (G - F - H) p (mod p^2), F = f0 g0, G = (f0+f1)(g0+g1), H = f1 g1
  def times_p(poly):
    out = [0] * 6
    for i, a in enumerate(poly):
      for j, b in enumerate(p):
        out[i + j] = (out[i + j] + a * b) % q
    return polymulmod(out, [1], sq, q)
  terms = []
  # (left map, right map, kind): F contributes poly*(1 - p), G contributes poly*p, H contributes -poly*p
  groups = [
      (F0, F0, 'F'),
      ([[(x + y) % q for x, y in zip(c0, c1)] for c0, c1 in zip(F0, F1)],
       [[(x + y) % q for x, y in zip(c0, c1)] for c0, c1 in zip(F0, F1)], 'G'),
      (F1, F1, 'H')]
  for L, R, kind in groups:
    for la, lb, out in kar:
      a = [x % q for x in compose_form(la, L)]
      b = [x % q for x in compose_form(lb, R)]
      outp = out + [0]  # degree <= 2 polynomial padded to 4
      outp = outp[:4]
      pp = times_p(out)
      if kind == 'F':
        c = [(o - t) % q for o, t in zip(outp, pp)]
      elif kind == 'G':
        c = pp
      else:
        c = [(-t) % q for t in pp]
      terms.append((a, b, c))
  return terms, sq


def crt_c6(termsA1, termsA2):
  """Rank-12 decomposition of F_2[x]/(x^6+1) from decompositions of A1 x A2."""
  q = 2
  m6 = [1, 0, 0, 0, 0, 0, 1]
  m1 = [1, 0, 1]            # (x+1)^2
  m2 = [1, 0, 1, 0, 1]      # (x^2+x+1)^2
  n = 6
  P1 = linmap(lambda v: polymulmod(v, [1], m1, q), n, q)
  P2 = linmap(lambda v: polymulmod(v, [1], m2, q), n, q)
  # CRT idempotents in F_2[x]/(x^6+1): e1 = 1 mod m1, 0 mod m2; e2 = 1 - e1
  e1 = None
  for code in range(64):
    v = [(code >> i) & 1 for i in range(6)]
    if polymulmod(v, [1], m1, q) == [1, 0] and polymulmod(v, [1], m2, q) == [0, 0, 0, 0]:
      e1 = v
  assert e1 is not None
  e2 = [(1 + e1[0]) % 2] + e1[1:]
  def lift(w, e):
    w6 = (list(w) + [0] * 6)[:6]
    return polymulmod(w6, e, m6, q)
  terms = []
  for (a, b, c) in termsA1:
    terms.append((compose_form(a, P1), compose_form(b, P1), lift(c, e1)))
  for (a, b, c) in termsA2:
    terms.append((compose_form(a, P2), compose_form(b, P2), lift(c, e2)))
  terms = [([x % 2 for x in a], [x % 2 for x in b], [x % 2 for x in c]) for a, b, c in terms]
  return terms, m6


def toom_b5():
  """Rank-8 decomposition of F_5[x]/((x^2+2)^2): evaluate the full product of two cubics at
  0,1,2,3, modulo r = x^2+2 (Karatsuba over F_25), and at infinity; reconstruct by CRT."""
  q = 5
  p = [2, 0, 1]
  mod = [4, 0, 4, 0, 1]     # (x^2+2)^2 = x^4 + 4x^2 + 4
  r = [3, 0, 1]             # x^2 + 3 = x^2 - 2, irreducible since 2 is a non-square mod 5
  pts = [0, 1, 2, 3]
  M = [1]
  for c in pts:
    M = [(x - c * y) % q for x, y in zip([0] + M, M + [0])]
  Mfull = [0] * 7
  for i, a in enumerate(M):
    for j, b in enumerate(r):
      Mfull[i + j] = (Mfull[i + j] + a * b) % q   # M * r, monic degree 6
  # Lagrange-type CRT basis for residues modulo the factors of Mfull = prod(x - c) * r
  def polymod(f, m):
    return polymulmod(f, [1], m, q)
  # idempotent-like basis: E_c = 1 mod (x-c), 0 mod other factors; E_r0, E_r1 = 1, x mod r and 0 mod points
  def solve_crt(target_mod_r, point_vals):
    # brute force over polynomials of degree < 6 is 5^6 = 15625, fine
    for code in range(q ** 6):
      v = [(code // q ** i) % q for i in range(6)]
      if all(sum(v[k] * pow(c, k, q) for k in range(6)) % q == pv for c, pv in zip(pts, point_vals)) \
         and polymod(v, r) == target_mod_r:
        return v
    raise ValueError
  basis = {}
  for idx, c in enumerate(pts):
    vals = [1 if j == idx else 0 for j in range(4)]
    basis[('pt', c)] = solve_crt([0, 0], vals)
  basis[('r', 0)] = solve_crt([1, 0], [0, 0, 0, 0])
  basis[('r', 1)] = solve_crt([0, 1], [0, 0, 0, 0])
  terms = []
  def red(poly):
    return polymulmod((list(poly) + [0] * 7)[:7], [1], mod, q)
  # point evaluations: (f(c)) (g(c)) * E_c
  for c in pts:
    ev = [pow(c, k, q) for k in range(4)]
    terms.append((ev, ev, red(basis[('pt', c)])))
  # modulo r: f mod r = u0 + u1 x with x^2 = -3 = 2; product (u0+u1x)(v0+v1x) = u0v0 + 2u1v1 + (u0v1+u1v0)x
  Rm = linmap(lambda v: polymod(v, r), 4, q)
  u0 = compose_form([1, 0], Rm)
  u1 = compose_form([0, 1], Rm)
  s = [(x + y) % q for x, y in zip(u0, u1)]
  E0, E1 = basis[('r', 0)], basis[('r', 1)]
  # u0v0 -> coefficient 1 on E0 and -1 on E1 ; u1v1 -> 2 on E0 and -1 on E1 ; (u0+u1)(v0+v1) -> E1
  def comb(a0, a1):
    return red([(a0 * x + a1 * y) % q for x, y in zip(E0, E1)])
  terms.append((u0, u0, comb(1, q - 1)))
  terms.append((u1, u1, comb(2, q - 1)))
  terms.append((s, s, comb(0, 1)))
  # infinity: f3 g3 * Mfull (the leading coefficient term)
  e3 = [0, 0, 0, 1]
  terms.append((e3, e3, red(Mfull)))
  return terms, mod


def main():
  out = {}
  A2, mod2 = padic_karatsuba([1, 1, 1], 2)
  assert verify(A2, mod2, 2) and len(A2) == 9
  A1 = [([1, 0], [1, 0], [1, 1]), ([0, 1], [0, 1], [1, 1]), ([1, 1], [1, 1], [0, 1])]
  assert verify(A1, [1, 0, 1], 2)
  C6, m6 = crt_c6(A1, A2)
  assert verify(C6, m6, 2) and len(C6) == 12
  B5, mod5 = toom_b5()
  assert verify(B5, mod5, 5) and len(B5) == 8
  # the p-adic Karatsuba construction gives 9 over every small field
  for q, p in [(3, [1, 0, 1]), (5, [2, 0, 1]), (7, [1, 0, 1])]:
    T, m = padic_karatsuba(p, q)
    assert verify(T, m, q) and len(T) == 9
  for name, (terms, mod, q) in {'A2_F2_rank9': (A2, mod2, 2), 'A1_F2_rank3': (A1, [1, 0, 1], 2),
                                'C6_F2_rank12': (C6, m6, 2), 'B5_F5_rank8': (B5, mod5, 5)}.items():
    out[name] = {'q': q, 'modulus_low_to_high': mod, 'rank': len(terms),
                 'terms': [{'a': a, 'b': b, 'c': c} for a, b, c in terms]}
    print(f'{name}: verified, {len(terms)} terms')
  if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], 'w'), indent=1)


if __name__ == '__main__':
  main()
