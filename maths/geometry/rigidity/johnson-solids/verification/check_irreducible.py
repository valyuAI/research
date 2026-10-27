"""Supplementary check for checker 1 (needs sympy): every minimal polynomial in data/ is irreducible over Q, so
Q[x]/(m) is a field and the modular rank in check1_rank.py is a lower bound for the real rank. (Checker 2 does
not need this.) Tower radicands are certified non-squares inside tower.py (norm or quadratic non-residue)."""
import glob, json
import sympy as sp
x = sp.Symbol('x')
bad = []
for f in sorted(glob.glob('data/J*.json')):
  d = json.load(open(f))
  P = sp.Poly(list(reversed([int(c) for c in d['minpoly']])), x)
  ok = P.is_irreducible
  print(f[5:8], 'degree', P.degree(), 'irreducible' if ok else 'REDUCIBLE', flush=True)
  if not ok:
    bad.append(f)
print('ALL IRREDUCIBLE' if not bad else 'REDUCIBLE: %s' % bad)
