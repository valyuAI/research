"""Exact standard-library checker: a CTLN with a stable fixed point whose support is not a clique.

Input JSON: {"n": n, "edges": [[j, i], ...] meaning j -> i, "eps": "1/4", "delta": "1/2", "support": [...] (optional)}.
CTLN (Curto-Morrison): dx_i/dt = -x_i + [sum_j W_ij x_j + theta]_+, W_ii = 0,
W_ij = -1 + eps if j -> i, W_ij = -1 - delta otherwise.  theta = 1.

Checks, all in exact rational / integer arithmetic:
  1. legal parameters: delta > 0, 0 < eps < delta / (1 + delta);
  2. the support sigma induces a subgraph that is not a clique;
  3. x* = (I - W_sigma)^{-1} theta 1 is entrywise positive on sigma, and the off-support conditions hold
     (for k outside sigma, sum_j W_kj x*_j + theta < 0); together: x* (zero off sigma) is a fixed point;
  4. A = (I - W)_sigma is positive stable (Jacobian -A on the active block, -1 on inactive coordinates):
     characteristic polynomial computed two independent ways (Berkowitz, integer and division free; and
     Hessenberg reduction over Q), then the Routh array and the Lienard-Chipart / Hurwitz-determinant
     criterion, each applied independently;
  5. nondegeneracy (CGM Definition 2.1): if eps = 1/4 and delta = 1/2 then (I - W)/eps is congruent to I
     mod 3, so every principal minor and every Cramer replacement determinant is congruent to 1 mod 3 and
     hence nonzero; this congruence is checked entrywise.  For n <= 12 all subsets are also checked directly.
"""
from fractions import Fraction as F
from itertools import combinations
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mm import charpoly_integer


def berkowitz(A):
  """Coefficients [1, c1, ..., cn] of det(xI - A) for an integer (or rational) matrix, division free."""
  n = len(A)
  # Standard Berkowitz: build Toeplitz products.
  C = [F(1), -A[0][0]]  # charpoly of leading 1x1 block
  for r in range(1, n):
    # partition leading (r+1)x(r+1) block: [[Ar, Sc],[R, a]]
    R = [A[r][j] for j in range(r)]
    Sc = [A[i][r] for i in range(r)]
    a = A[r][r]
    # column vector of Toeplitz first column: 1, -a, -R Sc, -R Ar Sc, ..., -R Ar^{r-1} Sc
    col = [F(1), -a]
    v = Sc[:]
    for k in range(r):
      col.append(-sum(R[j] * v[j] for j in range(r)))
      v = [sum(A[i][j] * v[j] for j in range(r)) for i in range(r)]
    # multiply lower-triangular Toeplitz (r+2) x (r+1) by C (length r+1)
    newC = []
    for i in range(r + 2):
      s = F(0)
      for j in range(min(i, r) + 1):
        if i - j < len(col): s += col[i - j] * C[j]
      newC.append(s)
    C = newC
  return C


def hessenberg_charpoly(A):
  """Coefficients [1, c1, ..., cn] of det(xI - A) via exact reduction to upper Hessenberg form."""
  n = len(A); H = [[F(x) for x in row] for row in A]
  for c in range(n - 2):
    p = next((r for r in range(c + 1, n) if H[r][c] != 0), None)
    if p is None: continue
    if p != c + 1:
      H[p], H[c + 1] = H[c + 1], H[p]
      for row in H: row[p], row[c + 1] = row[c + 1], row[p]
    piv = H[c + 1][c]
    for r in range(c + 2, n):
      f = H[r][c] / piv
      if f:
        for k in range(n): H[r][k] -= f * H[c + 1][k]
        for k in range(n): H[k][c + 1] += f * H[k][r]
  # recurrence for charpoly of Hessenberg matrix: p_0 = 1, p_k = (x - h_kk) p_{k-1} - sum ...
  P = [[F(1)]]
  for k in range(1, n + 1):
    pk = [F(0)] + P[k - 1]  # x * p_{k-1} (coeffs low -> high)
    pk = [pk[i] - (H[k - 1][k - 1] * P[k - 1][i] if i < len(P[k - 1]) else 0) for i in range(len(pk))]
    prod = F(1)
    for i in range(k - 1, 0, -1):
      prod *= H[i][i - 1]
      coef = prod * H[i - 1][k - 1]
      for j in range(len(P[i - 1])): pk[j] -= coef * P[i - 1][j]
    P.append(pk)
  return list(reversed(P[n]))


def routh_stable(a):
  """a = [a0 > 0, a1, ..., an]: True iff every root of sum a_k z^(n-k) has negative real part (Routh array)."""
  n = len(a) - 1
  r0 = a[0::2]; r1 = a[1::2] + [F(0)] * (len(a[0::2]) - len(a[1::2]))
  first = [r0[0], r1[0]]
  rows = [r0, r1]
  for _ in range(n - 1):
    p, q = rows[-2], rows[-1]
    if q[0] == 0: return False
    new = [(q[0] * (p[k + 1] if k + 1 < len(p) else 0) - p[0] * (q[k + 1] if k + 1 < len(q) else 0)) / q[0]
           for k in range(len(p) - 1)]
    new += [F(0)] * (len(q) - len(new))
    rows.append(new); first.append(new[0])
  return all(v > 0 for v in first[: n + 1])


def det(M):
  n = len(M); A = [[F(x) for x in row] for row in M]; d = F(1)
  for c in range(n):
    p = next((r for r in range(c, n) if A[r][c] != 0), None)
    if p is None: return F(0)
    if p != c: A[c], A[p] = A[p], A[c]; d = -d
    d *= A[c][c]
    for r in range(c + 1, n):
      f = A[r][c] / A[c][c]
      if f:
        for k in range(c, n): A[r][k] -= f * A[c][k]
  return d


def lienard_chipart_stable(a):
  """All a_k > 0 and Hurwitz determinants Delta_{n-1}, Delta_{n-3}, ... > 0 (Lienard-Chipart criterion)."""
  n = len(a) - 1
  if not all(v > 0 for v in a): return False
  coef = lambda k: a[k] if 0 <= k <= n else F(0)
  H = [[coef(2 * (j + 1) - (i + 1)) for j in range(n)] for i in range(n)]
  for k in range(n - 1, 0, -2):
    if det([row[:k] for row in H[:k]]) <= 0: return False
  return True


def solve(M, b):
  n = len(M); A = [[F(x) for x in M[i]] + [F(b[i])] for i in range(n)]
  for c in range(n):
    p = next(r for r in range(c, n) if A[r][c] != 0)
    A[c], A[p] = A[p], A[c]
    for r in range(n):
      if r != c and A[r][c] != 0:
        f = A[r][c] / A[c][c]
        for k in range(c, n + 1): A[r][k] -= f * A[c][k]
  return [A[i][n] / A[i][i] for i in range(n)]


def cluster_charpoly(cl, eps, delta, sigma):
  """det(xI - K) from the identical-row quotient: (x - 1)^(n - k) * det(xI - Q), Q = I + beta M + t 1 m^T.
  Valid when the vertex classes have identical nonedge rows (checked in main)."""
  m, M = cl['m'], cl['M']; k = len(m); n = len(sigma)
  t = (1 - eps) / eps; beta = 1 + delta / eps
  Q = [[(1 if a == b else 0) + beta * M[a][b] + t * m[b] for b in range(k)] for a in range(k)]
  cq = berkowitz(Q); poly = [F(1)]
  for _ in range(n - k): poly = [a - b for a, b in zip(poly + [F(0)], [F(0)] + poly)]
  prod = [F(0)] * (len(poly) + len(cq) - 1)
  for i, a in enumerate(poly):
    for j, c in enumerate(cq): prod[i + j] += a * c
  return prod


def main(path):
  t0 = time.time()
  d = json.load(open(path))
  n = d['n']; eps = F(d['eps']); delta = F(d['delta']); theta = F(1)
  E = {(j, i) for j, i in d['edges']}
  assert all(j != i and 0 <= i < n and 0 <= j < n for j, i in E), 'edges must be loopless, in range'
  W = [[F(0) if i == j else (-1 + eps if (j, i) in E else -1 - delta) for j in range(n)] for i in range(n)]
  sigma = d.get('support', list(range(n)))
  out = {'file': path, 'n': n, 'eps': str(eps), 'delta': str(delta), 'num_edges': len(E), 'support_size': len(sigma)}
  out['legal'] = delta > 0 and 0 < eps < delta / (1 + delta)
  missing = [(j, i) for i in sigma for j in sigma if i != j and (j, i) not in E]
  out['support_is_clique'] = not missing
  out['missing_edges_in_support'] = len(missing)
  A = [[(1 if i == j else 0) - W[i][j] for j in sigma] for i in sigma]
  x = solve(A, [theta] * len(sigma))
  out['fixed_point_positive_on_support'] = all(v > 0 for v in x)
  out['min_fixed_point_entry'] = str(min(x))
  xs = [F(0)] * n
  for s, v in zip(sigma, x): xs[s] = v
  off = [k for k in range(n) if k not in sigma]
  out['off_support_strict'] = all(sum(W[k][j] * xs[j] for j in range(n)) + theta < 0 for k in off)
  # residual check of the full nonlinear fixed point equation, exactly
  res = [-xs[i] + max(F(0), sum(W[i][j] * xs[j] for j in range(n)) + theta) for i in range(n)]
  out['fixed_point_residual_zero'] = all(r == 0 for r in res)
  # integer scaling: K = A / eps has integer entries at eps = 1/4, delta = 1/2
  K = [[v / eps for v in row] for row in A]
  m = len(K)
  methods = {}
  if all(v.denominator == 1 for row in K for v in row):
    ci, nprimes = charpoly_integer([[int(v) for v in row] for row in K])
    methods['multimodular_hessenberg_crt'] = [F(v) for v in ci]
    out['crt_primes'] = nprimes
  if m <= 60: methods['berkowitz'] = berkowitz(K)
  if m <= 40: methods['hessenberg_rational'] = hessenberg_charpoly(K)
  if 'cluster' in d:
    cl = d['cluster']; cls = cl['classes']
    assert sorted(v for c in cls for v in c) == sorted(sigma) and [len(c) for c in cls] == cl['m']
    Nrow = lambda i: tuple(0 if (i == j or (j, i) in E) else 1 for j in sigma)
    ok = all(Nrow(i) == Nrow(c[0]) for c in cls for i in c)
    ok = ok and all(sum(Nrow(c[0])[sigma.index(j)] for j in cls[b]) == cl['M'][a][b]
                    for a, c in enumerate(cls) for b in range(len(cls)))
    out['cluster_description_matches_graph'] = ok
    assert ok, 'cluster data does not describe the graph'
    methods['cluster_quotient_times_(x-1)^(n-k)'] = cluster_charpoly(d['cluster'], eps, delta, sigma)
  vals = list(methods.values())
  out['charpoly_methods'] = sorted(methods)
  out['charpoly_methods_agree'] = len(vals) >= 2 and all(v == vals[0] for v in vals)
  c1 = vals[0]
  # det(zI + K) = (-1)^m det(-zI - K): coefficients b_k = (-1)^k c_k
  b = [c1[k] * (-1) ** k for k in range(m + 1)]
  out['det_zI_plus_K_coeffs'] = [str(v) for v in b]
  out['routh_stable'] = routh_stable(b)
  out['lienard_chipart_stable'] = lienard_chipart_stable(b) if m <= 60 else 'skipped (n > 60)'
  out['positive_stable'] = out['routh_stable'] and out['lienard_chipart_stable'] in (True, 'skipped (n > 60)')
  # nondegeneracy
  Kfull = [[((1 if i == j else 0) - W[i][j]) / eps for j in range(n)] for i in range(n)]
  is_int = all(v.denominator == 1 for row in Kfull for v in row)
  out['K_integer'] = is_int
  out['K_congruent_I_mod_3'] = is_int and all((int(Kfull[i][j]) - (1 if i == j else 0)) % 3 == 0
                                              for i in range(n) for j in range(n))
  if n <= 12:
    ok = True
    for k in range(1, n + 1):
      for S in combinations(range(n), k):
        As = [[Kfull[i][j] for j in S] for i in S]
        if det(As) == 0: ok = False
        for col in range(k):
          B = [row[:] for row in As]
          for r in range(k): B[r][col] = F(1)
          if det(B) == 0: ok = False
    out['nondegenerate_bruteforce'] = ok
  out['nondegenerate'] = out['K_congruent_I_mod_3'] or out.get('nondegenerate_bruteforce', False)
  out['stable_nonclique_fixed_point'] = all(out[k] for k in (
    'legal', 'fixed_point_positive_on_support', 'off_support_strict', 'fixed_point_residual_zero',
    'charpoly_methods_agree', 'positive_stable', 'nondegenerate')) and not out['support_is_clique']
  out['seconds'] = round(time.time() - t0, 2)
  return out


if __name__ == '__main__':
  allok = True
  for p in sys.argv[1:]:
    r = main(p)
    short = {k: v for k, v in r.items() if k != 'det_zI_plus_K_coeffs'}
    print(json.dumps(short, indent=1), flush=True)
    allok &= r['stable_nonclique_fixed_point']
  print('ALL PASS' if allok else 'FAIL')
  sys.exit(0 if allok else 1)
