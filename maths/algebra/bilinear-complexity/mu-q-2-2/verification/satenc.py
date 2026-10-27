#!/usr/bin/env python3
"""DIMACS encoding of 'tensor of F2[x]/(f) has F2-rank <= r'.

Usage: satenc.py f r out.cnf [--lex]
Variables: a[t][i], b[t][j], c[t][k] for t < r.  For every (i,j,k) the XOR over t
of a[t][i] b[t][j] c[t][k] must equal T[i][j][k].  Optional --lex adds a sound
symmetry-breaking constraint: the 3n-bit words (a_t,b_t,c_t) are non-decreasing in t
(terms of a decomposition can be permuted freely).
"""
import sys


def tensor(f):
  n = f.bit_length() - 1
  T = set()
  for i in range(n):
    for j in range(n):
      v = 1 << (i + j)
      for d in range(2 * n, n - 1, -1):
        if v >> d & 1:
          v ^= f << (d - n)
      for k in range(n):
        if v >> k & 1:
          T.add((i, j, k))
  return n, T


def encode(f, r, lex):
  n, T = tensor(f)
  nv = [0]
  cls = []

  def new():
    nv[0] += 1
    return nv[0]

  a = [[new() for _ in range(n)] for _ in range(r)]
  b = [[new() for _ in range(n)] for _ in range(r)]
  c = [[new() for _ in range(n)] for _ in range(r)]

  def and2(x, y):
    z = new()
    cls.extend([[-z, x], [-z, y], [z, -x, -y]])
    return z

  def xor2(x, y):
    z = new()
    cls.extend([[-z, x, y], [-z, -x, -y], [z, -x, y], [z, x, -y]])
    return z

  ab = {(t, i, j): and2(a[t][i], b[t][j]) for t in range(r) for i in range(n) for j in range(n)}
  for i in range(n):
    for j in range(n):
      for k in range(n):
        terms = [and2(ab[t, i, j], c[t][k]) for t in range(r)]
        acc = terms[0]
        for x in terms[1:]:
          acc = xor2(acc, x)
        cls.append([acc] if (i, j, k) in T else [-acc])
  if lex:
    for t in range(r - 1):
      u = a[t] + b[t] + c[t]
      v = a[t + 1] + b[t + 1] + c[t + 1]
      eq = None  # literal meaning 'prefixes equal so far'
      for q in range(len(u)):
        pre = [] if eq is None else [-eq]
        cls.append(pre + [-u[q], v[q]])  # equal prefix -> u_q <= v_q
        e = new()
        # e <-> (eq and u_q == v_q)
        if eq is not None:
          cls.append([-e, eq])
        cls.extend([[-e, -u[q], v[q]], [-e, u[q], -v[q]]])
        cls.append(pre + [e, u[q], v[q]])
        cls.append(pre + [e, -u[q], -v[q]])
        eq = e
  return nv[0], cls, (a, b, c), n, T


def main():
  f, r, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
  lex = '--lex' in sys.argv
  nv, cls, _, n, _ = encode(f, r, lex)
  with open(out, 'w') as fh:
    fh.write(f'p cnf {nv} {len(cls)}\n')
    for cl in cls:
      fh.write(' '.join(map(str, cl)) + ' 0\n')
  print(f'f={f} n={n} r={r} lex={lex}: {nv} vars, {len(cls)} clauses -> {out}')


if __name__ == '__main__':
  main()
