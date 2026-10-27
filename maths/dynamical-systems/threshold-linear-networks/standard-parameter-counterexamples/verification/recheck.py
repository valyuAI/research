"""Exact recheck of every coefficient-positive candidate emitted by fixedscan2 (lines 'TAG d6').
For each: rebuild N from digraph6, K = DEN*I + BETA*N + T*J, exact charpoly (Berkowitz over Q),
Lienard-Chipart (exact Hurwitz determinants) and Routh array; reports any graph that is positive stable."""
import sys, os, argparse, hashlib, json, time
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_ctln import berkowitz, routh_stable, lienard_chipart_stable, solve
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('beta', type=int)
parser.add_argument('t', type=int)
parser.add_argument('den', type=int)
parser.add_argument('paths', nargs='+')
parser.add_argument('--expect-candidates', type=int, required=True)
parser.add_argument('--expect-stable', type=int, required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
beta, t, den = args.beta, args.t, args.den
def d6(s):
  if not s.startswith('&'): raise ValueError('invalid digraph6 prefix')
  s = s[1:]; n = ord(s[0]) - 63; bits = []
  if not 2 <= n <= 7 or len(s) != 1 + (n * n + 5) // 6: raise ValueError('invalid digraph6 order/length')
  for ch in s[1:]: v = ord(ch) - 63; bits += [(v >> k) & 1 for k in range(5, -1, -1)]
  if any(bits[i * n + i] for i in range(n)): raise ValueError('loop in digraph6')
  return [bits[i * n:(i + 1) * n] for i in range(n)]
tot = stable = disagree = 0; tags = {}
seen = set(); last_progress = time.monotonic(); stable_graphs = []
for path in args.paths:
  for line in open(path):
    tag, s = line.split()
    if tag not in ('HIT', 'REJ', 'UNDECIDED', 'SINGULAR_C'): raise ValueError('invalid candidate tag')
    if s in seen: raise ValueError('duplicate candidate across scan files')
    seen.add(s)
    N = d6(s); n = len(N); tot += 1; tags[tag] = tags.get(tag, 0) + 1
    C = [[den * (i == j) + beta * N[i][j] for j in range(n)] for i in range(n)]
    y = solve(C, [1] * n)
    if not all(v > 0 for v in y): raise ValueError(f'candidate is not permitted: {s}')
    K = [[C[i][j] + t for j in range(n)] for i in range(n)]
    c = berkowitz(K); b = [c[k] * (-1) ** k for k in range(n + 1)]
    lc = lienard_chipart_stable(b); r = routh_stable(b)
    if lc != r: raise ValueError(f'exact stability criteria disagree: {s}')
    if lc:
      stable += 1; print('STABLE', tag, s, flush=True)
      stable_graphs.append(s)
      if tag != 'HIT': disagree += 1
    elif tag == 'HIT': disagree += 1; print('FLOAT_HIT_NOT_STABLE', s)
    if time.monotonic() - last_progress >= 15:
      print(f'exactly rechecked {tot}/{args.expect_candidates} candidates; stable {stable}', flush=True)
      last_progress = time.monotonic()
print(f'rechecked {tot} candidates {tags}: exactly positive stable {stable}; float/exact disagreements {disagree}')
ok = tot == args.expect_candidates and stable == args.expect_stable
result = {'parameters': [beta, t, den], 'candidates': tot, 'stable': stable,
          'tags': tags, 'stable_graphs': stable_graphs, 'float_exact_disagreements': disagree,
          'inputs_sha256': {os.path.basename(p): hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in args.paths},
          'ok': ok}
with open(args.output, 'w') as f: json.dump(result, f, indent=2)
sys.exit(0 if ok else 'FAIL: candidate count or exact stable count differs from expectation')
