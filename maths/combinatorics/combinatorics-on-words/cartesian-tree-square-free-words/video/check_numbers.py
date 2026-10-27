"""Reproduce every number and example shown in the explainer video.

Run: python3 check_numbers.py   (pure Python, a few seconds)

1. Binary words: every word of length 4 over {a, b} contains a square; aba and bab are the longest.
2. The Dejean word (iterate the 19-uniform substitution from a): first 30 letters, square-free,
   and its most repetitive short blocks have exponent exactly 7/4.
3. Shape codes (parent distances) for the on-screen examples.
4. The binary substitution h2 applied to the Dejean prefix.
5. Windows: radius 2 (5 letters) is ambiguous, radius 3 (7 letters) decodes; 23 classes.
6. A short shape-square of half-length 3 inside h2(w) (allowed; the theorem starts at 4).
7. The bound 2 - 14/m and 2 - 16/m against 7/4.
8. Table entries 29 and 9 (exhaustive search, as in ../verification/controls.py).
"""

import itertools
from fractions import Fraction

H2 = {'a': '00101', 'b': '00111', 'c': '01100'}
H3 = {'a': '000101', 'b': '000221', 'c': '022211'}
DEJEAN = {'a': 'abcacbcabcbacbcacba', 'b': 'bcabacabcacbacabacb', 'c': 'cabcbabcabacbabcbac'}


def pd(x):
  out = []
  for i in range(len(x)):
    js = [j for j in range(i) if x[j] <= x[i]]
    out.append(i - max(js) if js else 0)
  return out


def has_square(w):
  n = len(w)
  return any(w[i:i + m] == w[i + m:i + 2 * m] for m in range(1, n // 2 + 1) for i in range(n - 2 * m + 1))


def max_exponent(w):
  best = (Fraction(1), '')
  for i in range(len(w)):
    for j in range(i + 2, len(w) + 1):
      z = w[i:j]
      for p in range(1, len(z)):
        if all(z[k] == z[k + p] for k in range(len(z) - p)):
          e = Fraction(len(z), p)
          if e > best[0]:
            best = (e, z)
          break
  return best


print('1. binary words')
for n in range(1, 6):
  free = [''.join(t) for t in itertools.product('ab', repeat=n) if not has_square(''.join(t))]
  print(f'   length {n}: square-free = {free}')

w = 'a'
while len(w) < 400:
  w = ''.join(DEJEAN[c] for c in w)
print('2. Dejean prefix (30):', w[:30])
print('   square-free:', not has_square(w[:120]))
e, z = max_exponent(w[:60])
print(f'   max exponent in first 60 letters: {e} (block {z})')
print('   abcab exponent:', Fraction(5, 3))

print('3. shape codes')
for s in [[3, 1, 4, 1, 5], [2, 0, 7, 0, 9], [1, 3, 2, 4, 3]]:
  print('  ', s, pd(s))
for s in ['00', '01', '11', '10', '0110', '0111', '0011', 'banana']:
  print('  ', s, pd(s))

x = ''.join(H2[c] for c in w)
print('4. h2(w) first 50:', ' '.join(x[i:i + 5] for i in range(0, 50, 5)))
print('   h2(w[:10]) letters:', w[:10])


def windows(x, r):
  cls = {}
  for i in range(r, len(x) - r):
    y = x[i - r:i + r + 1]
    cls.setdefault(tuple(pd(y)), {}).setdefault(y[r], (i, y))
  return cls


for r in (2, 3):
  cls = windows(x[:2000], r)
  amb = {k: v for k, v in cls.items() if len(v) > 1}
  print(f'5. radius {r}: {len(cls)} codes seen, ambiguous codes: {len(amb)}')
  for k, v in list(amb.items())[:3]:
    print('    code', k, {m: y for m, (i, y) in v.items()})

print('6. first shape-square of half-length 3 in h2(w):')
for i in range(len(x) - 6):
  u, v = x[i:i + 3], x[i + 3:i + 6]
  if pd(u) == pd(v):
    print(f'   position {i}: {u} {v}  codes {pd(u)} {pd(v)}  exact square: {u == v}')
    break
for i in range(len(x) - 6):
  u, v = x[i:i + 3], x[i + 3:i + 6]
  if pd(u) == pd(v) and u != v:
    print(f'   first non-exact: position {i}: {u} {v}  codes {pd(u)} {pd(v)}')
    break
# Half-length >= 4 in a long prefix: none expected.
y = x[:600]
bad = [(i, m) for m in range(4, 80) for i in range(len(y) - 2 * m + 1) if pd(y[i:i + m]) == pd(y[i + m:i + 2 * m])]
print('   shape-squares of half-length 4..79 in first 600 letters of h2(w):', len(bad))

print('7. bound')
for m in (56, 57, 100):
  print(f'   m={m}: 2 - 14/m = {Fraction(2) - Fraction(14, m)}  > 7/4? {Fraction(2) - Fraction(14, m) > Fraction(7, 4)}')
for m in (64, 65):
  print(f'   m={m}: 2 - 16/m = {Fraction(2) - Fraction(16, m)}  > 7/4? {Fraction(2) - Fraction(16, m) > Fraction(7, 4)}')


def longest(sigma, l, cap=200):
  best, stack = 0, ['']
  while stack:
    s = stack.pop()
    n = len(s)
    if any(pd(s[n - 2 * m:n - m]) == pd(s[n - m:]) for m in range(l, n // 2 + 1)):
      continue
    best = max(best, n)
    if n >= cap:
      return None
    stack.extend(s + c for c in 'abc'[:sigma])
  return best


print('8. table: (2,3) ->', longest(2, 3), ' (3,2) ->', longest(3, 2), ' (2,2) ->', longest(2, 2))
