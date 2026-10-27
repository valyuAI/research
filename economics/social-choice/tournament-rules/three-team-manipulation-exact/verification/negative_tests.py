"""Corrupt a valid certificate in several ways and confirm that verify_rule.py rejects each corruption."""
import sys, json, subprocess, tempfile, os, copy
from fractions import Fraction
here = os.path.dirname(os.path.abspath(__file__))
src = json.load(open(sys.argv[1]))
def run(cert):
  with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
    json.dump(cert, f); name = f.name
  p = subprocess.run([sys.executable, '-B', '-O', os.path.join(here, 'verify_rule.py'), name], capture_output=True, text=True)
  os.unlink(name)
  return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1]
cases = []
# 1. lower alpha slightly
c = copy.deepcopy(src); c['alpha'] = str(Fraction(src['alpha']) - Fraction(1, 10**6)); cases.append(('alpha decreased by 1e-6', c))
# 2. drop a class
c = copy.deepcopy(src); c['classes'] = c['classes'][1:]; cases.append(('one class removed', c))
# 3. duplicate a class (isomorphic copy)
c = copy.deepcopy(src); c['classes'] = c['classes'] + [c['classes'][0]]; cases.append(('duplicated class', c))
# 4. move probability within a class without a Condorcet winner
c = copy.deepcopy(src)
for C in c['classes']:
  r = [Fraction(x) for x in C['r']]
  if max(r) < 1:
    i = max(range(len(r)), key=lambda t: r[t]); j = min(range(len(r)), key=lambda t: r[t])
    eps = r[i] / 2; r[i] -= eps; r[j] += eps; C['r'] = [str(x) for x in r]; break
cases.append(('probability moved inside one class', c))
# 5. Condorcet winner not chosen
c = copy.deepcopy(src)
for C in c['classes']:
  r = [Fraction(x) for x in C['r']]
  if max(r) == 1:
    i = r.index(1); j = (i + 1) % len(r); r[i] = Fraction(1, 2); r[j] = Fraction(1, 2); C['r'] = [str(x) for x in r]; break
cases.append(('Condorcet winner given 1/2', c))
# 6. break automorphism invariance: perturb two teams in the same automorphism orbit
import itertools
def autos(T, n):
  pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
  beats = set()
  for t, (a, b) in enumerate(pairs):
    beats.add((a, b) if T[t] == '1' else (b, a))
  return [p for p in itertools.permutations(range(n)) if all((p[a], p[b]) in beats for a, b in beats)]
c = copy.deepcopy(src); n = src['n']; found = False
for C in c['classes']:
  r = [Fraction(x) for x in C['r']]
  for p in autos(C['T'], n):
    i = next((v for v in range(n) if p[v] != v and 0 < r[v] < 1), None)
    if i is not None:
      j = p[i]; eps = r[i] / 3; r[i] += eps; r[j] -= eps; C['r'] = [str(x) for x in r]; found = True; break
  if found: break
cases.append(('teams in one automorphism orbit given different probabilities', c))
# 7. a vector that does not sum to one
c = copy.deepcopy(src)
for C in c['classes']:
  r = [Fraction(x) for x in C['r']]
  if max(r) < 1:
    C['r'] = [str(x * Fraction(9, 10)) for x in r]; break
cases.append(('probabilities scaled by 9/10', c))
# 8. claim monotonicity and top-cycle consistency for a rule that lacks them (only for certificates without the flags)
if not src.get('monotone'):
  c = copy.deepcopy(src); c['monotone'] = True; c['top_cycle'] = True
  cases.append(('monotone and top-cycle flags added to a plain CC rule', c))
bad = 0
for name, cert in cases:
  code, last = run(cert)
  ok = code != 0
  bad += not ok
  print(f'{"rejected" if ok else "ACCEPTED (bad)"}: {name}: {last}')
sys.exit(1 if bad else 0)
