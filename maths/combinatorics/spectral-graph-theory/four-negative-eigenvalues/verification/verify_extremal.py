"""Standard-library check of the two extremal graphs with inertia (11, 0, 4).

Builds W5 and the affine-plane graph X from their definitions, computes their characteristic
polynomials exactly (Faddeev-LeVerrier over the rationals), their inertia by Descartes' rule
(exact for real-rooted polynomials) and independently by an LDL^T congruence over the rationals
(Sylvester's law of inertia), checks that both are reduced and connected, and that they are not
isomorphic (different degree sequences). Prints a JSON summary.
"""
import itertools, json, sys
from fractions import Fraction


def w5():
  pts = list(range(5))
  pairs = list(itertools.combinations(pts, 2))
  V = [('p', i) for i in pts] + [('s', S) for S in pairs]
  def adj(x, y):
    if x == y:
      return 0
    if x[0] == 'p' and y[0] == 'p':
      return 1
    if x[0] == 's' and y[0] == 's':
      return int(not set(x[1]) & set(y[1]))
    a, b = (x, y) if x[0] == 'p' else (y, x)
    return int(a[1] in b[1])
  return [[adj(x, y) for y in V] for x in V]


def affine_x():
  # AG(2,3): points (x,y) in Z_3^2; parallel classes: y=c (rows), x=c (cols), y-x=c, y+x=c
  pts = [(x, y) for x in range(3) for y in range(3)]
  cls = {
    'row': lambda p: p[1], 'col': lambda p: p[0],
    'd1': lambda p: (p[1] - p[0]) % 3, 'd2': lambda p: (p[1] + p[0]) % 3,
  }
  lines = [(c, v) for c in ('d1', 'd2') for v in range(3)]
  V = [('p', p) for p in pts] + [('l', L) for L in lines]
  def adj(x, y):
    if x == y:
      return 0
    if x[0] == 'p' and y[0] == 'p':
      p, q = x[1], y[1]
      return int(cls['row'](p) == cls['row'](q) or cls['col'](p) == cls['col'](q))
    if x[0] == 'l' and y[0] == 'l':
      return int(x[1][0] == y[1][0])  # parallel lines (same class) are adjacent
    a, b = (x, y) if x[0] == 'p' else (y, x)
    c, v = b[1]
    return int(cls[c](a[1]) == v)
  return [[adj(x, y) for y in V] for x in V]


def charpoly(A):
  """Faddeev-LeVerrier: coefficients c_0..c_n of det(xI - A), exact rationals."""
  n = len(A)
  M = [[Fraction(0)] * n for _ in range(n)]
  c = [Fraction(0)] * (n + 1)
  c[n] = Fraction(1)
  I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
  for k in range(1, n + 1):
    # M_k = A M_{k-1} + c_{n-k+1} I
    AM = [[sum(A[i][t] * M[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    M = [[AM[i][j] + c[n - k + 1] * I[i][j] for j in range(n)] for i in range(n)]
    AMk = [[sum(A[i][t] * M[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    c[n - k] = -sum(AMk[i][i] for i in range(n)) / k
  assert all(x.denominator == 1 for x in c)
  return [int(x) for x in c]


def descartes_inertia(c):
  z = 0
  while c[z] == 0:
    z += 1
  nz = c[z:]
  def sc(seq):
    s = [x for x in seq if x != 0]
    return sum(1 for a, b in zip(s, s[1:]) if (a > 0) != (b > 0))
  return sc(nz), z, sc([x * (-1) ** i for i, x in enumerate(nz)])


def ldl_inertia(A):
  M = [[Fraction(x) for x in r] for r in A]
  n = len(M)
  pos = neg = 0
  idx = list(range(n))
  while idx:
    piv = next((i for i in idx if M[i][i] != 0), None)
    if piv is not None:
      d = M[piv][piv]
      pos += d > 0
      neg += d < 0
      rest = [i for i in idx if i != piv]
      for i in rest:
        if M[i][piv] != 0:
          f = M[i][piv] / d
          for j in rest:
            M[i][j] -= f * M[piv][j]
      idx = rest
      continue
    pair = next(((i, j) for i in idx for j in idx if i < j and M[i][j] != 0), None)
    if pair is None:
      break
    i, j = pair
    for t in range(n):
      M[i][t] += M[j][t]
    for t in range(n):
      M[t][i] += M[t][j]
  return pos, n - pos - neg, neg


def reduced(A):
  rows = [tuple(r) for r in A]
  return len(set(rows)) == len(rows) and all(sum(r) > 0 for r in A)


def connected(A):
  n = len(A); seen = {0}; stack = [0]
  while stack:
    u = stack.pop()
    for v in range(n):
      if A[u][v] and v not in seen:
        seen.add(v); stack.append(v)
  return len(seen) == n


def g6(A):
  n = len(A)
  bits = [A[i][j] for j in range(1, n) for i in range(j)]
  while len(bits) % 6:
    bits.append(0)
  s = chr(n + 63)
  for t in range(0, len(bits), 6):
    v = 0
    for b in bits[t:t + 6]:
      v = 2 * v + b
    s += chr(v + 63)
  return s


def main():
  out = {}
  ok = True
  for name, A in (('W5', w5()), ('X_AG23', affine_x())):
    c = charpoly(A)
    d_in = descartes_inertia(c)
    l_in = ldl_inertia(A)
    rec = {
      'order': len(A), 'edges': sum(map(sum, A)) // 2,
      'degrees': sorted(sum(r) for r in A),
      'charpoly_coeffs_low_to_high': c,
      'inertia_descartes': d_in, 'inertia_ldl': l_in,
      'reduced': reduced(A), 'connected': connected(A), 'graph6': g6(A),
    }
    ok &= d_in == (11, 0, 4) and l_in == (11, 0, 4) and rec['reduced'] and rec['connected']
    out[name] = rec
  ok &= out['W5']['degrees'] != out['X_AG23']['degrees']
  out['all_checks_passed'] = bool(ok)
  print(json.dumps(out, indent=1))
  sys.exit(0 if ok else 1)


if __name__ == '__main__':
  main()
