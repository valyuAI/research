#!/usr/bin/env python3
"""Negative control for the doubling lemma (standard library only).
A distinct covering with minimum modulus 4 and moduli dividing 360 exists (control_m4_L360_covering.json).
Its classes with moduli dividing 180 form a level-2 state that is completed to a covering at level 3, so by the
lemma it must have Q_2 < R for every price vector.  This script checks that, and also evaluates the level-2 part
of the infinite covering of arXiv:2605.18644, Theorem 1.10 (Q_2 = R for some vectors)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_p2 import phi
here = os.path.dirname(os.path.abspath(__file__))
fam = [list(map(int, l.split())) for l in open(os.path.join(here, 'prices.txt')) if l.strip()]
def columns(system, L0):
    L = 2**L0 * 45
    cols = [0] * 2**L0
    for b in range(L):
        if not any(L % m == 0 and b % m == r for m, r in system):
            cols[b % 2**L0] |= 1 << (b % 45)
    return cols
cov = [tuple(p) for p in json.load(open(os.path.join(here, 'control_m4_L360_covering.json')))]
mods = [m for m, r in cov]
assert len(set(mods)) == len(mods) and all(360 % m == 0 and m >= 4 for m in mods)
assert all(any(b % m == r for m, r in cov) for b in range(360)), 'not a covering'
print('control covering: distinct moduli', sorted(mods), 'covers Z (checked mod 360)')
cols = columns(cov, 2)
ok = True
for rho in fam:
    q = sum(phi(c, rho) for c in cols)
    print('  rho', rho, 'Q2', q, 'R', sum(rho), 'alive' if q < sum(rho) else 'DEAD (lemma violated!)')
    ok &= q < sum(rho)
print('control 1:', 'PASS (alive under every price vector)' if ok else 'FAIL')
if not ok:
    raise SystemExit('FAIL: finite covering contradicts the asserted potential test')
# level-2 part of the infinite covering of Theorem 1.10 (moduli 6,12,9,18,36,10,20,15,30,45,90,60,180)
# (from the paper's coordinate description: (0|2),(10|2); (*|02),(0|01),(10|01); (0|4),(01|3); (*|1|2),(0|1|1);
#  (*|00|2),(0|00|1); first members of the chains 2^2 up 15 and 2^2 up 45, which start at moduli 60 and 180)
inf2 = [(6, 2), (9, 6), (10, 4), (12, 5), (15, 7), (18, 12), (20, 18), (30, 16), (36, 21), (45, 27), (60, 10), (90, 36), (180, 90)]
cols = columns(inf2, 2)
print('Theorem 1.10 truncation: column sizes', [bin(c).count('1') for c in cols])
equalities = []
for i, rho in enumerate(fam, 1):
    q = sum(phi(c, rho) for c in cols)
    print('  rho', rho, 'Q2', q, 'R', sum(rho), '(Q2 = R)' if q == sum(rho) else '')
    if q == sum(rho):
        equalities.append(i)
if equalities != [3, 9, 10]:
    raise SystemExit(f'FAIL: unexpected tightness vectors {equalities}')
print('control 2: PASS (equality exactly at vectors 3, 9, 10)')
