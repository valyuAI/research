def is_prime(p):
  if p < 2: return False
  for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
    if p % q == 0: return p == q
  d, s = p - 1, 0
  while d % 2 == 0: d //= 2; s += 1
  for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
    x = pow(a, d, p)
    if x in (1, p - 1): continue
    for _ in range(s - 1):
      x = x * x % p
      if x == p - 1: break
    else: return False
  return True

def charpoly_mod(A, p):
  """det(xI - A) mod p (coefficients high -> low) via Hessenberg reduction over GF(p)."""
  n = len(A); H = [[a % p for a in row] for row in A]
  for c in range(n - 2):
    piv = next((r for r in range(c + 1, n) if H[r][c]), None)
    if piv is None: continue
    if piv != c + 1:
      H[piv], H[c + 1] = H[c + 1], H[piv]
      for row in H: row[piv], row[c + 1] = row[c + 1], row[piv]
    inv = pow(H[c + 1][c], p - 2, p)
    for r in range(c + 2, n):
      f = H[r][c] * inv % p
      if f:
        Rr = H[r]; Rc = H[c + 1]
        for k in range(n): Rr[k] = (Rr[k] - f * Rc[k]) % p
        for row in H: row[c + 1] = (row[c + 1] + f * row[r]) % p
  P = [[1]]
  for k in range(1, n + 1):
    pk = [0] + P[k - 1]
    hk = H[k - 1][k - 1]
    for i in range(len(P[k - 1])): pk[i] = (pk[i] - hk * P[k - 1][i]) % p
    prod = 1
    for i in range(k - 1, 0, -1):
      prod = prod * H[i][i - 1] % p
      coef = prod * H[i - 1][k - 1] % p
      if coef:
        for j in range(len(P[i - 1])): pk[j] = (pk[j] - coef * P[i - 1][j]) % p
    P.append(pk)
  return list(reversed(P[n]))

def charpoly_integer(A):
  """Exact integer characteristic polynomial det(xI - A) of an integer matrix by multimodular Hessenberg + CRT.
  Uses the bound |c_k| <= C(n,k) * prod of the k largest row 2-norms (Hadamard), and enough 61-bit primes."""
  from math import comb, isqrt
  n = len(A)
  norms = sorted((isqrt(sum(a * a for a in row)) + 1 for row in A), reverse=True)
  bound = 1
  for k in range(n + 1):
    pr = 1
    for v in norms[:k]: pr *= v
    bound = max(bound, comb(n, k) * pr)
  target = 2 * bound + 1
  primes = []; p = (1 << 61) - 1; M = 1
  while M <= target:
    if is_prime(p): primes.append(p); M *= p
    p -= 2
  res = None; mod = 1
  for p in primes:
    c = charpoly_mod(A, p)
    if res is None: res, mod = c, p; continue
    inv = pow(mod, -1, p)
    res = [r + mod * (((ci - r) * inv) % p) for r, ci in zip(res, c)]
    mod *= p
  return [r - mod if r > mod // 2 else r for r in res], len(primes)
