"""Independent exact verifier (Python standard library only).

Certificate (JSON): {"n": n, "k": k, "mode": "eq"|"le", "alpha": "p/q",
  "classes": [{"T": upper-triangle 0/1 string (pair (i,j), i<j, '1' means i beats j), "r": [n fractions]}]}
Claims verified:
  1. the listed tournaments are pairwise non-isomorphic and there are exactly A000568(n) of them
     (so every tournament on n teams is isomorphic to exactly one listed T);
  2. each r is a probability vector, constant on automorphism orbits of T, and puts probability 1 on a
     Condorcet winner when T has one;
  3. the induced neutral rule (r transported along isomorphisms) satisfies
        r_S(T') - r_S(T) <= alpha
     for every listed T, every coalition S with |S| = k (mode eq) or 2 <= |S| <= k (mode le),
     and every T' obtained from T by re-orienting matches inside S.
  4. optional, if the certificate has "monotone": true: r_i(T') >= r_i(T) whenever T' is obtained from T by
     reversing one match that i lost (monotonicity in the sense of Schneider, Schvartzman and Weinberg);
  5. optional, if the certificate has "top_cycle": true: every team outside the top cycle of T has probability 0.
Neutrality makes checking one representative per class sufficient: the constraint set is permutation invariant.
Optional --shard=i/m checks the manipulations of every m-th class only (steps 1, 2, 4, 5 always run in full);
combine_shards.py merges the m result files.
"""
import sys, json, itertools, time
from fractions import Fraction

def fail(msg):
  print('FAIL:', msg)
  sys.exit(1)

def require(cond, msg):
  if not cond: fail(msg)

shard, nshards = 0, 1
args = [a for a in sys.argv[1:] if not a.startswith('--shard=')]
for a in sys.argv[1:]:
  if a.startswith('--shard='):
    shard, nshards = map(int, a[len('--shard='):].split('/'))
sys.argv = [sys.argv[0]] + args
A000568 = {1: 1, 2: 1, 3: 2, 4: 4, 5: 12, 6: 56, 7: 456, 8: 6880, 9: 191536}
import hashlib
raw = open(sys.argv[1], 'rb').read()
digest = hashlib.sha256(raw).hexdigest()
cert = json.loads(raw)
n, k, mode, alpha = cert['n'], cert['k'], cert['mode'], Fraction(cert['alpha'])
require(mode in ('eq', 'le') and isinstance(k, int) and 2 <= k <= n and 0 <= shard < nshards, 'bad header or shard')
require(n in A000568 and 0 <= alpha <= 1, 'unsupported order or invalid alpha')
require(all(type(cert.get(flag, False)) is bool for flag in ('monotone', 'top_cycle')), 'invalid property flag')
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
last_progress = time.monotonic()

def progress(message):
  global last_progress
  if time.monotonic() - last_progress >= 15:
    print(message, file=sys.stderr, flush=True)
    last_progress = time.monotonic()

def parse(s):
  require(isinstance(s, str) and len(s) == len(pairs), 'bad tournament length')
  out = [[False] * n for _ in range(n)]
  for t, (i, j) in enumerate(pairs):
    if s[t] == '1': out[i][j] = True
    elif s[t] == '0': out[j][i] = True
    else: fail('bad tournament string')
  return out

def refine(adj):
  """isomorphism-invariant colour classes by iterated out/in score refinement"""
  col = [sum(adj[v]) for v in range(n)]
  for _ in range(n):
    sig = [(col[v], tuple(sorted(col[w] for w in range(n) if adj[v][w])), tuple(sorted(col[w] for w in range(n) if adj[w][v]))) for v in range(n)]
    keys = sorted(set(sig))
    new = [keys.index(sig[v]) for v in range(n)]
    if len(set(new)) == len(set(col)):
      col = new; break
    col = new
  return col

def canon(adj):
  """returns (code, list of labelings achieving it); labeling lab[v] = new label of v"""
  col = refine(adj)
  order = sorted(set(col))
  groups = [[v for v in range(n) if col[v] == c] for c in order]
  best, labs = None, []
  for combo in itertools.product(*[itertools.permutations(g) for g in groups]):
    seq = [v for g in combo for v in g]          # seq[newlabel] = vertex
    code = 0
    for t, (a, b) in enumerate(pairs):
      if adj[seq[a]][seq[b]]: code |= 1 << t
    if best is None or code < best:
      best, labs = code, [seq]
    elif code == best:
      labs.append(seq)
  lab = []
  for seq in labs:
    l = [0] * n
    for newl, v in enumerate(seq): l[v] = newl
    lab.append(l)
  return best, lab

reps = {}
for C in cert['classes']:
  adj = parse(C['T'])
  r = [Fraction(x) for x in C['r']]
  require(len(r) == n, 'bad probability-vector length')
  code, labs = canon(adj)
  require(code not in reps, 'two listed tournaments are isomorphic')
  # value per canonical label (orbit-invariance check: all labelings must give the same values)
  vals = None
  for l in labs:
    v = [None] * n
    for vert in range(n): v[l[vert]] = r[vert]
    if vals is None: vals = v
    else: require(v == vals, 'values not constant on automorphism orbits')
  require(len(r) == n and all(x >= 0 for x in r) and sum(r) == 1, 'not a lottery')
  for v in range(n):
    if all(adj[v][w] for w in range(n) if w != v): require(r[v] == 1, 'Condorcet winner not chosen')
  reps[code] = (adj, r, vals)
  progress(f'  canonical representatives: {len(reps)}/{len(cert["classes"])}')
require(len(reps) == A000568[n], f'expected {A000568[n]} classes, got {len(reps)}')

def value(adj2, S):
  code, labs = canon(adj2)
  vals = reps[code][2]
  l = labs[0]
  return sum(vals[l[v]] for v in S)

def flipped(adj, a, b):
  adj2 = [row[:] for row in adj]
  adj2[a][b], adj2[b][a] = adj[b][a], adj[a][b]
  return adj2

def top_cycle(adj):
  top = set()
  for v in range(n):
    seen = {v}; st = [v]
    while st:
      u = st.pop()
      for w in range(n):
        if adj[u][w] and w not in seen: seen.add(w); st.append(w)
    if len(seen) == n: top.add(v)
  return top

extra = []
if cert.get('top_cycle'):
  for code, (adj, r, vals) in reps.items():
    top = top_cycle(adj)
    require(all(r[v] == 0 for v in range(n) if v not in top), 'positive probability outside the top cycle')
  extra.append('top-cycle consistent')
if cert.get('monotone'):
  nmono = 0
  for code, (adj, r, vals) in reps.items():
    for i in range(n):
      for j in range(n):
        if i != j and adj[j][i]:
          require(value(flipped(adj, i, j), [i]) >= r[i], 'not monotone')
          nmono += 1
          progress(f'  monotonicity: {nmono}/{len(reps) * len(pairs)} single-match reversals')
  extra.append(f'monotone ({nmono} single-match reversals checked)')

sizes = [k] if mode == 'eq' else list(range(2, k + 1))
worst = Fraction(-10)
checked = 0
tight = []
for done, (code, (adj, r, vals)) in enumerate(reps.items()):
  if done % nshards != shard: continue
  progress(f'  manipulations: {done}/{len(reps)} classes, {checked} checked, max gain {worst}')
  if done % 500 == 0 and done:
    print(f'  progress: {done}/{len(reps)} classes, {checked} manipulations, max gain so far {worst}', file=sys.stderr, flush=True)
  for sz in sizes:
    for S in itertools.combinations(range(n), sz):
      base = sum(r[v] for v in S)
      inner = list(itertools.combinations(S, 2))
      for bits in range(1 << len(inner)):
        adj2 = [row[:] for row in adj]
        changed = False
        for t, (a, b) in enumerate(inner):
          w = bool(bits >> t & 1)
          if adj2[a][b] != w: changed = True
          adj2[a][b] = w; adj2[b][a] = not w
        if not changed: continue
        gain = value(adj2, S) - base
        checked += 1
        if gain > worst: worst = gain
        if gain == alpha: tight.append((''.join('1' if adj[a][b] else '0' for a, b in pairs), S, bits))
        require(gain <= alpha, f'violation: gain {gain} > alpha')
tight_classes = sorted(set(t[0] for t in tight))
print((f'[shard {shard}/{nshards}] ' if nshards > 1 else '') + f'n={n} k={k} mode={mode}: {len(reps)} classes, {checked} manipulations checked, max gain {worst} <= alpha = {alpha}: OK' + ''.join('; ' + e for e in extra))
print(f'{len(tight)} manipulations attain gain alpha, in {len(tight_classes)} classes: ' + ', '.join(f"{c} (scores {sorted((sum(row) for row in parse(c)), reverse=True)})" for c in tight_classes))
if len(sys.argv) > 2:
  json.dump({'n': n, 'k': k, 'mode': mode, 'alpha': str(alpha), 'classes': len(reps), 'manipulations': checked, 'max_gain': str(worst), 'tight_manipulations': len(tight), 'tight_classes': tight_classes, 'properties': extra, 'shard': f'{shard}/{nshards}', 'certificate_sha256': digest, 'ok': True}, open(sys.argv[2], 'w'), indent=1)
