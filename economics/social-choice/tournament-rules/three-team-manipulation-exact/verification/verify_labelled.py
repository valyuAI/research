"""Second, brute-force checker for small n (standard library only).

Unlike verify_rule.py it uses no canonical forms and no neutrality argument. It expands the
certificate to a rule on all 2^(n(n-1)/2) labelled tournaments, by trying every permutation
to find an isomorphism to a listed representative and requiring all isomorphisms to give the
same vector, and then checks every coalition of size 2..k on every labelled tournament.
Practical for n <= 6.
usage: verify_labelled.py certificate.json"""
import sys, json, itertools, time
from fractions import Fraction

cert = json.load(open(sys.argv[1]))
n, k, alpha = cert['n'], cert['k'], Fraction(cert['alpha'])
if cert.get('mode') != 'le' or not 2 <= k <= n <= 6:
  sys.exit('FAIL: labelled checker requires le mode and 2 <= k <= n <= 6')
last_progress = time.monotonic()
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
m = len(pairs)
pid = {p: t for t, p in enumerate(pairs)}
perms = list(itertools.permutations(range(n)))

def beats(code, a, b):
  """True if a beats b in the labelled tournament with bit code."""
  if a < b: return bool(code >> pid[(a, b)] & 1)
  return not (code >> pid[(b, a)] & 1)

def relabel(code, p):
  """code of the tournament in which p[a] beats p[b] whenever a beats b"""
  out = 0
  for t, (a, b) in enumerate(pairs):
    x, y = p[a], p[b]
    w = beats(code, a, b)
    if x < y:
      if w: out |= 1 << pid[(x, y)]
    else:
      if not w: out |= 1 << pid[(y, x)]
  return out

reps = []
for C in cert['classes']:
  code = sum(1 << t for t in range(m) if C['T'][t] == '1')
  reps.append((code, [Fraction(x) for x in C['r']]))
rule = {}
for code, r in reps:
  for p in perms:
    c2 = relabel(code, p)
    v = [None] * n
    for a in range(n): v[p[a]] = r[a]
    if c2 in rule and rule[c2] != v:
      print('FAIL: two listed tournaments are isomorphic or a vector is not automorphism invariant'); sys.exit(1)
    rule[c2] = v
if len(rule) != 1 << m:
  print(f'FAIL: certificate covers {len(rule)} of {1 << m} labelled tournaments'); sys.exit(1)
for code, v in rule.items():
  if any(x < 0 for x in v) or sum(v) != 1:
    print('FAIL: not a lottery'); sys.exit(1)
  for a in range(n):
    if all(beats(code, a, b) for b in range(n) if b != a) and v[a] != 1:
      print('FAIL: Condorcet winner not chosen'); sys.exit(1)
extra = []
if cert.get('monotone'):
  for code, v in rule.items():
    for a in range(n):
      for b in range(n):
        if a != b and beats(code, b, a):
          code2 = code ^ (1 << pid[(min(a, b), max(a, b))])
          if rule[code2][a] < v[a]:
            print('FAIL: not monotone'); sys.exit(1)
  extra.append('monotone')
if cert.get('top_cycle'):
  for code, v in rule.items():
    for a in range(n):
      seen = {a}; st = [a]
      while st:
        u = st.pop()
        for w in range(n):
          if w != u and beats(code, u, w) and w not in seen: seen.add(w); st.append(w)
      if len(seen) < n and v[a] != 0:
        print('FAIL: positive probability outside the top cycle'); sys.exit(1)
  extra.append('top-cycle consistent')
worst = Fraction(-1); checked = 0
for sz in range(2, k + 1):
  for S in itertools.combinations(range(n), sz):
    if time.monotonic() - last_progress >= 15:
      print(f'  labelled n={n}: size {sz}, coalition {S}, {checked} manipulations checked', flush=True)
      last_progress = time.monotonic()
    mask = sum(1 << pid[(a, b)] for a, b in itertools.combinations(S, 2))
    sub = [s for s in range(1 << m) if s & ~mask == 0]
    for code, v in rule.items():
      base = sum(v[a] for a in S)
      for s in sub:
        if s == 0: continue
        v2 = rule[code ^ s]
        gain = sum(v2[a] for a in S) - base
        checked += 1
        if gain > worst: worst = gain
        if gain > alpha:
          print(f'FAIL: violation: gain {gain} > alpha'); sys.exit(1)
print(f'n={n} k={k}: {len(rule)} labelled tournaments, {checked} (T, S, T\') checked, max gain {worst} <= alpha = {alpha}: OK' + ''.join('; ' + e for e in extra))
