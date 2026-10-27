"""Independent checker for the stored stabilizer-code certificates (standard library only;
shares no code with construct.py; does not rely on Python assertions).

For each certificate (q = p^m, modulus, r x n matrices A, B over GF(q)) it checks:
  F. the modulus is monic of degree m and irreducible over GF(p) (no factor of degree <= m/2);
  G. the symplectic Gram matrix A B^T - B A^T vanishes (rows of [A|B] commute);
  S. the n(q^2-1) syndromes of the nonzero single-qudit Paulis X^x Z^z (syndrome
     (A_k z - B_k x)) are pairwise distinct and nonzero.  This holds iff no nonzero Pauli of
     weight <= 2 commutes with the stabilizer, i.e. the code is pure with distance >= 3;
  R. the rank r' of [A|B].  The certificate then gives a pure [[n, n-r', >=3]]_q code, and
     (adding logical operators to the stabilizer) pure [[n, n-r, >=3]]_q codes for r' <= r <= n-1.
Usage: python3 -B -O check_codes.py [certificate.json ...]   (default: all under certificates/)
Default mode (no arguments) checks every stored certificate, writes check_codes_results.json
next to this file, and exits with status 1 if any certificate is invalid or if the base-case
coverage required by Theorem 4.4 is incomplete.  Explicit-file mode checks only the named files,
reports coverage for information, and fails only on invalid certificates.
"""
import hashlib, json, os, sys, itertools

HERE = os.path.dirname(os.path.abspath(__file__))


class Field:
  def __init__(self, p, m, mod):
    self.p, self.m, self.q, self.mod = p, m, p ** m, mod
    q = self.q
    self.vec = [[(x // p ** i) % p for i in range(m)] for x in range(q)]
    self.add = [[self._enc([(a + b) % p for a, b in zip(self.vec[x], self.vec[y])]) for y in range(q)] for x in range(q)]
    self.neg = [self._enc([(-a) % p for a in self.vec[x]]) for x in range(q)]
    self.mul = [[self._mul(x, y) for y in range(q)] for x in range(q)]
  def _enc(self, c):
    return sum(ci * self.p ** i for i, ci in enumerate(c))
  def _mul(self, x, y):
    p, m = self.p, self.m
    if m == 1:
      return (x * y) % p
    a, b = self.vec[x], self.vec[y]
    prod = [0] * (2 * m - 1)
    for i in range(m):
      for j in range(m):
        prod[i + j] = (prod[i + j] + a[i] * b[j]) % p
    for d in range(2 * m - 2, m - 1, -1):
      c = prod[d]
      if c:
        for k in range(m + 1):
          prod[d - m + k] = (prod[d - m + k] - c * self.mod[k]) % p
    return self._enc(prod[:m])


def irreducible(p, m, mod):
  if len(mod) != m + 1 or mod[-1] != 1 or any(not (0 <= c < p) for c in mod):
    return False
  if m == 1:
    return True
  for dd in range(1, m // 2 + 1):
    for g in itertools.product(range(p), repeat=dd):
      g = list(g) + [1]
      r = list(mod)
      for d in range(len(r) - 1, dd - 1, -1):
        c = r[d]
        if c:
          for k in range(dd + 1):
            r[d - dd + k] = (r[d - dd + k] - c * g[k]) % p
      if not any(r[:dd]):
        return False
  return True


def check(path):
  raw = open(path, 'rb').read()
  return check_dict(json.loads(raw), os.path.relpath(path, HERE), hashlib.sha256(raw).hexdigest())


def check_dict(d, label='<memory>', digest=None):
  res = {'file': label, 'sha256': digest}
  p, m, q, n = d['p'], d['m'], d['q'], d['n']
  A, B = d['stabilizer_X_part_A'], d['stabilizer_Z_part_B']
  r = len(A)
  ok_shape = (p ** m == q and len(B) == r and all(len(row) == n for row in A + B)
              and all(0 <= x < q for row in A + B for x in row))
  ok_field = ok_shape and irreducible(p, m, d['modulus_low_first'] if m > 1 else [0, 1])
  res.update({'q': q, 'n': n, 'r_ambient': r, 'field_ok': ok_field})
  if not ok_field:
    res['valid'] = False
    return res
  F = Field(p, m, d['modulus_low_first'])
  ad, mu_, ng = F.add, F.mul, F.neg
  gram_ok = True
  for i in range(r):
    for j in range(i + 1, r):
      s = 0
      for k in range(n):
        s = ad[s][ad[mu_[A[i][k]][B[j][k]]][ng[mu_[B[i][k]][A[j][k]]]]]
      if s:
        gram_ok = False
  seen = set()
  synd_ok = True
  zero = (0,) * r
  for k in range(n):
    for x in range(q):
      for z in range(q):
        if x == 0 and z == 0:
          continue
        s = tuple(ad[mu_[A[i][k]][z]][ng[mu_[B[i][k]][x]]] for i in range(r))
        if s == zero or s in seen:
          synd_ok = False
        seen.add(s)
  # rank of [A|B] over GF(q) (inverse by search)
  inv = [None] + [next(y for y in range(1, q) if mu_[x][y] == 1) for x in range(1, q)]
  M = [A[i] + B[i] for i in range(r)]
  rk = 0
  for c in range(2 * n):
    pr = next((i for i in range(rk, r) if M[i][c]), None)
    if pr is None:
      continue
    M[rk], M[pr] = M[pr], M[rk]
    iv = inv[M[rk][c]]
    M[rk] = [mu_[iv][x] for x in M[rk]]
    for i in range(r):
      if i != rk and M[i][c]:
        f = M[i][c]
        M[i] = [ad[x][ng[mu_[f][y]]] for x, y in zip(M[i], M[rk])]
    rk += 1
  res.update({'gram_zero': gram_ok, 'single_qudit_syndromes_distinct_nonzero': synd_ok, 'rank': rk,
              'valid': gram_ok and synd_ok,
              'conclusion': f'pure [[{n},{n - rk},>=3]]_{q}' if gram_ok and synd_ok else 'INVALID'})
  return res


def main():
  paths = sys.argv[1:]
  if not paths:
    for root, _, files in os.walk(os.path.join(HERE, 'certificates')):
      for fn in sorted(files):
        if fn.endswith('.json') and fn != 'generation_log.json':
          paths.append(os.path.join(root, fn))
  results = [check(pth) for pth in sorted(paths)]
  bad = [r_['file'] for r_ in results if not r_['valid']]
  summary = {'checked': len(results), 'valid': len(results) - len(bad), 'invalid': bad}
  # base-case coverage required by Theorem 4.4
  cover = {}
  for r_ in results:
    if r_['valid'] and r_['file'].startswith('certificates/base/'):
      cover.setdefault((r_['q'], r_['r_ambient']), set()).add(r_['n'])
  need = {}
  for q in (3, 4, 5):
    need[(q, 4)] = set(range(5, q * q + 2))
    need[(q, 5)] = set(range(6, q ** 3 + 2))
  missing = {f'q{q}_r{r}': sorted(need[(q, r)] - cover.get((q, r), set())) for (q, r) in need}
  summary['base_case_missing'] = missing
  summary['base_cases_complete'] = all(not v for v in missing.values())
  out = {'summary': summary, 'results': results}
  if paths and not sys.argv[1:]:
    with open(os.path.join(HERE, 'check_codes_results.json'), 'w') as f:
      json.dump(out, f, indent=1)
  print(json.dumps(summary, indent=1))
  for r_ in results:
    if not r_['file'].startswith('certificates/base/'):
      print(r_['file'], r_.get('conclusion'))
  default_mode = not sys.argv[1:]
  if default_mode and not summary['base_cases_complete']:
    print('BASE CASE COVERAGE INCOMPLETE:', {k: v for k, v in missing.items() if v}, file=sys.stderr)
  if bad:
    print('INVALID CERTIFICATES:', bad, file=sys.stderr)
  sys.exit(1 if bad or (default_mode and not summary['base_cases_complete']) else 0)


if __name__ == '__main__':
  main()
