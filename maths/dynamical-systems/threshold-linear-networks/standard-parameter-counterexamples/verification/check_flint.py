"""Independent second implementation (python-flint, FLINT exact arithmetic), sharing no code with check_ctln.py.

For each input JSON (same format as check_ctln.py) it rebuilds W from the edge list, forms the integer
matrix K = (I - W)/eps (eps = 1/4, delta = 1/2), solves K y = 1 over Q, computes the exact characteristic
polynomial with FLINT, and applies the Hurwitz criterion to det(zI + K): every coefficient and every
Hurwitz determinant Delta_1, ..., Delta_n is computed exactly (FLINT integer determinants) and must be positive.
"""
import json, sys
import flint

def run(path):
  d = json.load(open(path)); n = d['n']
  frac = lambda s: flint.fmpq(*map(int, (s + '/1').split('/')[:2]))
  assert frac(d['eps']) == flint.fmpq(1, 4) and frac(d['delta']) == flint.fmpq(1, 2)
  E = set(map(tuple, d['edges']))
  # (I - W)/eps: diagonal 1/eps = 4; edge j->i: (1 - eps)/eps = 3; nonedge: (1 + delta)/eps = 6
  K = flint.fmpz_mat([[4 if i == j else (3 if (j, i) in E else 6) for j in range(n)] for i in range(n)])
  y = flint.fmpq_mat(K).solve(flint.fmpq_mat([[1]] * n))
  pos = all(y[i, 0] > 0 for i in range(n))
  cp = K.charpoly()                       # det(xI - K)
  a = [cp[n - i] * (-1) ** i for i in range(n + 1)]   # det(zI + K) coefficients, high to low
  coef = lambda k: a[k] if 0 <= k <= n else 0
  H = [[coef(2 * (j + 1) - (i + 1)) for j in range(n)] for i in range(n)]
  hur = []
  for r in range(1, n + 1):
    hur.append(flint.fmpz_mat([row[:r] for row in H[:r]]).det())
  stable = all(c > 0 for c in a) and all(h > 0 for h in hur)
  nonclique = any((j, i) not in E for i in range(n) for j in range(n) if i != j)
  print(json.dumps({'file': path, 'n': n, 'permitted': pos, 'min_y': str(min(y[i, 0] for i in range(n))),
                    'all_hurwitz_determinants_positive': stable, 'nonclique': nonclique}), flush=True)
  return pos and stable and nonclique

if __name__ == '__main__':
  ok = all([run(p) for p in sys.argv[1:]])
  print('ALL PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
