#!/usr/bin/env python3
"""Turn a list of rank-one bilinear forms (a, b) spanning a subspace W >= S into an explicit
decomposition of the multiplication tensor of F_q[x]/(f), q prime.
Usage: extract.py q W.txt out.json c0 c1 ... cn
W.txt: one line per rank-one form, 'a_0..a_{n-1} b_0..b_{n-1}' (form (x, y) -> a(x) b(y)).
"""
import json
import sys


def main():
  q = int(sys.argv[1])
  wfile, out = sys.argv[2], sys.argv[3]
  f = [int(c) % q for c in sys.argv[4:]]
  n = len(f) - 1
  inv = {a: pow(a, q - 2, q) for a in range(1, q)}

  def mulmono(i, j):
    t = [0] * (2 * n - 1)
    t[i + j] = 1
    for d in range(2 * n - 2, n - 1, -1):
      c = t[d]
      if c:
        for k in range(n + 1):
          t[d - n + k] = (t[d - n + k] - c * f[k]) % q
    return t[:n]

  forms = []
  for line in open(wfile):
    v = [int(x) for x in line.split()]
    if v:
      forms.append((v[:n], v[n:]))
  mats = [[a[i] * b[j] % q for i in range(n) for j in range(n)] for a, b in forms]
  slices = [[mulmono(i, j)[k] for i in range(n) for j in range(n)] for k in range(n)]
  # greedy basis selection, then solve slices in that basis
  def rank(rows):
    rows = [list(r) for r in rows]
    r = 0
    for c in range(n * n):
      p = next((i for i in range(r, len(rows)) if rows[i][c]), None)
      if p is None:
        continue
      rows[r], rows[p] = rows[p], rows[r]
      s = inv[rows[r][c]]
      rows[r] = [x * s % q for x in rows[r]]
      for i in range(len(rows)):
        if i != r and rows[i][c]:
          cc = rows[i][c]
          rows[i] = [(x - cc * y) % q for x, y in zip(rows[i], rows[r])]
      r += 1
    return r
  chosen = []
  for t in range(len(mats)):
    if rank([mats[s] for s in chosen + [t]]) > len(chosen):
      chosen.append(t)
  R = len(chosen)
  coeff = [[0] * n for _ in range(R)]
  for k in range(n):
    A = [[mats[t][r] for t in chosen] + [slices[k][r]] for r in range(n * n)]
    row, pivs = 0, []
    for c in range(R):
      p = next((r for r in range(row, n * n) if A[r][c]), None)
      if p is None:
        continue
      A[row], A[p] = A[p], A[row]
      s = inv[A[row][c]]
      A[row] = [x * s % q for x in A[row]]
      for r in range(n * n):
        if r != row and A[r][c]:
          cc = A[r][c]
          A[r] = [(x - cc * y) % q for x, y in zip(A[r], A[row])]
      pivs.append(c)
      row += 1
    assert all(A[r][R] == 0 for r in range(row, n * n)), 'slice not in span of W'
    for r, c in enumerate(pivs):
      coeff[c][k] = A[r][R]
  terms = [{'a': forms[t][0], 'b': forms[t][1], 'c': coeff[i]} for i, t in enumerate(chosen)]
  terms = [t for t in terms if any(t['c'])]
  for i in range(n):
    for j in range(n):
      z = mulmono(i, j)
      for k in range(n):
        assert sum(t['a'][i] * t['b'][j] * t['c'][k] for t in terms) % q == z[k]
  json.dump({'q': q, 'modulus_low_to_high': f, 'rank': len(terms), 'terms': terms,
             'convention': 'x^i * x^j mod f = sum_t a_t[i] * b_t[j] * (sum_k c_t[k] x^k), arithmetic mod q'},
            open(out, 'w'), indent=1)
  print(f'verified decomposition of rank {len(terms)} written to {out}')
  for t in terms:
    print(' ', t)


if __name__ == '__main__':
  main()
