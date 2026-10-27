#!/usr/bin/env python3
"""Independent standard-library replay of every claim in the paper.

  1. Upper bounds: the explicit decompositions in certificates/ reproduce the
     multiplication tensors exactly (A2 = F2[x]/((x^2+x+1)^2) with 9 products,
     F2[x]/((x+1)^2) with 3, F2[x]/(x^6+1) with 12, F3[x]/((x^2+1)^2) with 8 symmetric
     products, F5[x]/((x^2+2)^2) with 8).
  2. Lower bound: exhaustive proof that R_{F2}(A2) > 8 (subspace criterion with unit-group
     reduction and bucketing; see the paper, Section 4), plus two controls run through the
     same code: F2[x]/(x^4) (rank 8, must be found) and F16 = F2[x]/(x^4+x+1) (rank 9).
  3. Optional (--full): exhaustive proof that R_{F3}(F3[x]/((x^2+1)^2)) > 7 (generic prime-field
     implementation of the same search, independent of the bit-vector code used for F2).

No assertions are used; every check is reported, and the exit status is non-zero if any
check fails.  Results are written to results.json next to this file.
Usage: python3 verify.py [--full]
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def record(name, ok, detail=''):
  CHECKS.append({'check': name, 'ok': bool(ok), 'detail': detail})
  print(('PASS ' if ok else 'FAIL ') + name + (f' ({detail})' if detail else ''), flush=True)


# ---------------------------------------------------------------- prime-field polynomials

def mono_product(i, j, mod, q):
  """Coefficient vector of x^i * x^j modulo the monic polynomial mod over F_q."""
  n = len(mod) - 1
  t = [0] * (2 * n - 1)
  t[i + j] = 1
  for d in range(2 * n - 2, n - 1, -1):
    c = t[d]
    if c:
      for k in range(n + 1):
        t[d - n + k] = (t[d - n + k] - c * mod[k]) % q
  return t[:n]


def check_decomposition(terms, mod, q):
  n = len(mod) - 1
  for i in range(n):
    for j in range(n):
      z = mono_product(i, j, mod, q)
      for k in range(n):
        s = sum(t['a'][i] * t['b'][j] * t['c'][k] for t in terms) % q
        if s != z[k]:
          return False
  return True


def part1():
  ub = json.load(open(os.path.join(HERE, 'certificates', 'upper_bounds.json')))
  expected = {'A2_F2_rank9': 9, 'A1_F2_rank3': 3, 'C6_F2_rank12': 12, 'B5_F5_rank8': 8}
  for name, rank in expected.items():
    d = ub[name]
    ok = d['rank'] == rank == len(d['terms']) and check_decomposition(d['terms'], d['modulus_low_to_high'], d['q'])
    record(f'decomposition {name}', ok, f"q={d['q']}, modulus {d['modulus_low_to_high']}, {len(d['terms'])} terms")
  d = json.load(open(os.path.join(HERE, 'certificates', 'q3_rank8.json')))
  ok = (d['q'] == 3 and d['modulus_low_to_high'] == [1, 0, 2, 0, 1] and len(d['terms']) == 8
        and check_decomposition(d['terms'], d['modulus_low_to_high'], 3))
  record('decomposition F3[x]/((x^2+1)^2) with 8 products', ok)
  sym = all(t['a'] == t['b'] for t in d['terms'])
  record('the F3 decomposition is symmetric (a_t = b_t)', sym)
  # negative controls: every single-coefficient corruption of the F3 certificate is rejected
  rejected = total = 0
  for ti, t in enumerate(d['terms']):
    for key in ('a', 'b', 'c'):
      for k in range(4):
        bad = json.loads(json.dumps(d['terms']))
        bad[ti][key][k] = (bad[ti][key][k] + 1) % 3
        total += 1
        rejected += not check_decomposition(bad, [1, 0, 2, 0, 1], 3)
  record('negative control: all single-entry corruptions of the F3 certificate are rejected',
         rejected == total, f'{rejected}/{total}')
  # moduli are the intended algebras
  record('x^4+x^2+1 = (x^2+x+1)^2 over F2', poly_mul([1, 1, 1], [1, 1, 1], 2) == [1, 0, 1, 0, 1])
  record('x^4+2x^2+1 = (x^2+1)^2 over F3', poly_mul([1, 0, 1], [1, 0, 1], 3) == [1, 0, 2, 0, 1])
  record('x^4+4x^2+4 = (x^2+2)^2 over F5', poly_mul([2, 0, 1], [2, 0, 1], 5) == [4, 0, 4, 0, 1])
  record('x^2+x+1 irreducible over F2', all((c * c + c + 1) % 2 for c in range(2)))
  record('x^2+1 irreducible over F3', all((c * c + 1) % 3 for c in range(3)))
  record('x^2+2 irreducible over F5', all((c * c + 2) % 5 for c in range(5)))
  record('x^6+1 = (x+1)^2 (x^2+x+1)^2 over F2',
         poly_mul([1, 0, 1], [1, 0, 1, 0, 1], 2) == [1, 0, 0, 0, 0, 0, 1])


def poly_mul(f, g, q):
  t = [0] * (len(f) + len(g) - 1)
  for i, a in enumerate(f):
    for j, b in enumerate(g):
      t[i + j] = (t[i + j] + a * b) % q
  return t


# ---------------------------------------------------------------- generic exhaustive search

def exhaustive(q, mod, m, stop_at_first=True):
  """Decide R_{F_q}(F_q[x]/(mod)) <= n + m, q prime.  Returns (possible, prefixes, info)."""
  n = len(mod) - 1
  nn = n * n
  inv = {a: pow(a, q - 2, q) for a in range(1, q)}

  def mul(x, y):
    t = [0] * (2 * n - 1)
    for i in range(n):
      if x[i]:
        for j in range(n):
          t[i + j] = (t[i + j] + x[i] * y[j]) % q
    for d in range(2 * n - 2, n - 1, -1):
      c = t[d]
      if c:
        for k in range(n + 1):
          t[d - n + k] = (t[d - n + k] - c * mod[k]) % q
    return t[:n]

  def unit(i):
    return [1 if k == i else 0 for k in range(n)]

  def echelon(vecs):
    basis = []
    for v in vecs:
      v = list(v)
      for p, b in basis:
        if v[p]:
          c = v[p]
          v = [(x - c * y) % q for x, y in zip(v, b)]
      piv = next((k for k, x in enumerate(v) if x), None)
      if piv is None:
        continue
      s = inv[v[piv]]
      v = [x * s % q for x in v]
      out = []
      for p, b in basis:
        if b[piv]:
          c = b[piv]
          b = [(x - c * y) % q for x, y in zip(b, v)]
        out.append((p, b))
      basis = out + [(piv, v)]
    return basis

  def reduce(v, basis):
    v = list(v)
    for p, b in basis:
      if v[p]:
        c = v[p]
        v = [(x - c * y) % q for x, y in zip(v, b)]
    return v

  def normalize(v):
    piv = next((k for k, x in enumerate(v) if x), None)
    if piv is None:
      return None
    s = inv[v[piv]]
    return tuple(x * s % q for x in v)

  slices = [[mul(unit(i), unit(j))[k] for i in range(n) for j in range(n)] for k in range(n)]
  S = echelon(slices)
  if len(S) != n:
    return None, 0, 'slices dependent'
  funcs = [tuple((code // q ** i) % q for i in range(n)) for code in range(1, q ** n)]
  funcs = [v for v in funcs if v[next(k for k, x in enumerate(v) if x)] == 1]
  ones = [(a, b, [a[i] * b[j] % q for i in range(n) for j in range(n)]) for a in funcs for b in funcs]
  img = [reduce(M, S) for _, _, M in ones]
  units = [u for u in (list((code // q ** i) % q for i in range(n)) for code in range(1, q ** n))
           if len(echelon([mul(u, unit(j)) for j in range(n)])) == n]
  cls = {}
  for a in funcs:
    if a in cls:
      continue
    c = len(set(cls.values()))
    cls[a] = c
    stack = [a]
    while stack:
      x = stack.pop()
      for u in units:
        cols = [mul(u, unit(j)) for j in range(n)]
        w = normalize([sum(x[i] * col[i] for i in range(n)) % q for col in cols])
        if w not in cls:
          cls[w] = c
          stack.append(w)
  reps = {}
  for idx, (a, b, _) in enumerate(ones):
    reps.setdefault(tuple(sorted((cls[a], cls[b]))), idx)
  N = len(ones)
  info = f'{len(units)} units, {len(set(cls.values()))} functional orbits, {len(reps)} F1 representatives, {N} rank-one forms'
  prefixes = 0

  def bucket_test(prefix):
    E = echelon([img[i] for i in prefix])
    if len(E) < len(prefix):
      return None
    common, buckets = [], {}
    for s in range(N):
      v = normalize(reduce(img[s], E))
      if v is None:
        common.append(ones[s][2])
      else:
        buckets.setdefault(v, []).append(ones[s][2])
    rc = len(echelon(common))
    for members in buckets.values():
      if len(members) >= n + m - rc and len(echelon(common + members)) == n + m:
        return True
    return False

  found = False
  for rep in reps.values():
    if m == 3:
      for i2 in range(N):
        if i2 == rep:
          continue
        r = bucket_test([rep, i2])
        if r is None:
          continue
        prefixes += 1
        if r:
          found = True
          break
    elif m == 4:
      for i2 in range(N):
        if i2 == rep:
          continue
        for i3 in range(i2 + 1, N):
          if i3 == rep:
            continue
          r = bucket_test([rep, i2, i3])
          if r is None:
            continue
          prefixes += 1
          if r:
            found = True
            break
        if found:
          break
    if found and stop_at_first:
      break
  return found, prefixes, info


def exhaustive_f2(f):
  """Bit-vector version of the same search over F_2 for n = 4, m = 4 (rank <= 8).
  Matrices are 16-bit integers, bit 4*i + j = entry (i, j); f is the modulus as a bit mask."""
  n = 4

  def mul(a, b):
    r = 0
    for i in range(n):
      if b >> i & 1:
        r ^= a << i
    for d in range(2 * n - 2, n - 1, -1):
      if r >> d & 1:
        r ^= f << (d - n)
    return r

  def rank(vecs):
    basis = {}
    for v in vecs:
      while v:
        h = v.bit_length() - 1
        if h in basis:
          v ^= basis[h]
        else:
          basis[h] = v
          break
    return len(basis)

  def reducer(vecs):
    piv = {}
    for v in vecs:
      for h, b in piv.items():
        if v >> h & 1:
          v ^= b
      if v:
        h = v.bit_length() - 1
        for k in list(piv):
          if piv[k] >> h & 1:
            piv[k] ^= v
        piv[h] = v

    def red(x):
      for h, b in piv.items():
        if x >> h & 1:
          x ^= b
      return x
    return piv, red

  slices = [0] * n
  for i in range(n):
    for j in range(n):
      z = mul(1 << i, 1 << j)
      for k in range(n):
        if z >> k & 1:
          slices[k] |= 1 << (n * i + j)
  pivS, redS = reducer(slices)
  if len(pivS) != n:
    return None, 0
  funcs = list(range(1, 1 << n))

  def r1(a, b):
    m = 0
    for i in range(n):
      if a >> i & 1:
        m |= b << (n * i)
    return m
  ones = [(a, b, r1(a, b)) for a in funcs for b in funcs]
  img = [redS(m) for (_, _, m) in ones]
  units = [u for u in range(1, 1 << n) if rank([mul(u, 1 << j) for j in range(n)]) == n]

  def act(a, u):
    w = 0
    for j in range(n):
      if bin(a & mul(u, 1 << j)).count('1') & 1:
        w |= 1 << j
    return w
  cls = {}
  for a in funcs:
    if a in cls:
      continue
    c = len(set(cls.values()))
    cls[a] = c
    stack = [a]
    while stack:
      x = stack.pop()
      for u in units:
        y = act(x, u)
        if y not in cls:
          cls[y] = c
          stack.append(y)
  reps = {}
  for idx, (a, b, _) in enumerate(ones):
    reps.setdefault(tuple(sorted((cls[a], cls[b]))), idx)
  N = len(ones)
  prefixes = 0
  for rep in reps.values():
    for i2 in range(N):
      if i2 == rep:
        continue
      piv2, red2 = reducer([img[rep], img[i2]])
      if len(piv2) < 2:
        continue
      r2 = [red2(v) for v in img]
      for i3 in range(i2 + 1, N):
        if i3 == rep or r2[i3] == 0:
          continue
        prefixes += 1
        w3 = r2[i3]
        h3 = w3.bit_length() - 1
        common, buckets = [], {}
        for t in range(N):
          v = r2[t]
          if v >> h3 & 1:
            v ^= w3
          if v == 0:
            common.append(ones[t][2])
          else:
            buckets.setdefault(v, []).append(ones[t][2])
        rc = rank(common)
        for members in buckets.values():
          if len(members) >= 8 - rc and rank(common + members) == 8:
            return True, prefixes
  return False, prefixes


def part2():
  t0 = time.time()
  found, prefixes = exhaustive_f2(0b10101)
  record('R_F2(F2[x]/((x^2+x+1)^2)) > 8 by exhaustive search', found is False,
         f'{prefixes} prefixes (F1, F2, F3), {time.time() - t0:.0f}s')
  found, prefixes = exhaustive_f2(0b10000)
  record('control: rank-8 subspace found for F2[x]/(x^4) (rank 8)', found is True, f'after {prefixes} prefixes')
  t0 = time.time()
  found, prefixes = exhaustive_f2(0b10011)
  record('control: no rank-8 subspace for F16 = F2[x]/(x^4+x+1) (rank 9)', found is False,
         f'{prefixes} prefixes, {time.time() - t0:.0f}s')


def part3():
  t0 = time.time()
  found, prefixes, info = exhaustive(3, [1, 0, 2, 0, 1], 3)
  record('R_F3(F3[x]/((x^2+1)^2)) > 7 by exhaustive search', found is False,
         f'{prefixes} prefixes (F1, F2), {info}, {time.time() - t0:.0f}s')


def main():
  part1()
  part2()
  if '--full' in sys.argv:
    part3()
  ok = all(c['ok'] for c in CHECKS)
  json.dump({'all_passed': ok, 'checks': CHECKS, 'python': sys.version.split()[0]},
            open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
  print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
  sys.exit(0 if ok else 1)


if __name__ == '__main__':
  main()
