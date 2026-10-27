#!/usr/bin/env python3
"""Calibration of the price-potential method on cases with known answers.
Moduli 2^i d with d | D (D odd), 2^i d >= m, i <= L0 at the test level; prices on the divisors of D.
Loop: exhaustive DFS for systems surviving the price family -> LP (column generation) finds prices killing a
survivor, or reports that the survivor is ALIVE for every price vector (then the method cannot certify).
Usage: calib.py D m L0 [max_rounds]"""
import sys, time
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
from math import gcd
D, m, L0 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
MAXR = int(sys.argv[4]) if len(sys.argv) > 4 else 60
DIV = [d for d in range(1, D + 1) if D % d == 0]
CL = {d: [sum(1 << y for y in range(D) if (y - r) % d == 0) for r in range(d)] for d in DIV}
CLASSES = [(d, CL[d][r]) for d in DIV for r in range(d)]
FULL = (1 << D) - 1
P = 1 << L0
def phi_cover(S, rho):
    """exact min-cost cover by branching on the lowest uncovered residue; returns (cost, counts by divisor)."""
    if not S: return 0, [0] * len(DIV)
    best = [rho[0], [1] + [0] * (len(DIV) - 1)]
    def rec(T, cost, cnt):
        if cost >= best[0]: return
        if not T: best[0] = cost; best[1] = cnt[:]; return
        y = (T & -T).bit_length() - 1
        for k, d in enumerate(DIV):
            cnt[k] += 1; rec(T & ~CL[d][y % d], cost + rho[k], cnt); cnt[k] -= 1
    rec(S, 0, [0] * len(DIV))
    return best[0], best[1]
memo = {}
def phi(S, rho):
    key = (S, tuple(rho))
    v = memo.get(key)
    if v is None: v = phi_cover(S, rho)[0]; memo[key] = v
    return v
items = [(i, d) for i in range(L0 + 1) for d in DIV if (d << i) >= m]
items.sort(key=lambda t: (t[0] > 0, -(D // t[1]) * (P >> t[0])))  # level 0 first, then by area acted on
def search(fam, maxsurv=1):
    R = [sum(r) for r in fam]
    imp = [[(P >> i) * fam[f][DIV.index(d)] for f in range(len(fam))] for (i, d) in items]
    cols = [FULL] * P; out = []; nodes = [0]
    def dead(rem):
        return any(sum(phi(c, fam[f]) for c in cols) - rem[f] >= R[f] for f in range(len(fam)))
    def dfs(t, rem, fixed):
        nodes[0] += 1
        if fam and dead(rem): return
        if t == len(items):
            out.append(list(cols)); return
        if len(out) >= maxsurv: return
        i, d = items[t]
        rem2 = [rem[f] - imp[t][f] for f in range(len(fam))]
        dfs(t + 1, rem2, fixed)
        nn = 1 << i
        for n in range(nn):
            for r in range(d):
                if i == 0 and not fixed and r != 0: continue   # translation: first level-0 class is 0 mod d
                msk = CL[d][r]; xs = range(n, P, nn)
                if not any(cols[x] & msk for x in xs): continue
                save = [cols[x] for x in xs]
                for x in xs: cols[x] &= ~msk
                dfs(t + 1, rem2, fixed or i == 0)
                for x, s in zip(xs, save): cols[x] = s
                if len(out) >= maxsurv: return
    rem0 = [sum(imp[t][f] for t in range(len(items))) for f in range(len(fam))]
    dfs(0, rem0, False)
    return out, nodes[0]
def lp_kill(state):
    k = len(DIV); state = [S for S in state if S]
    if not state: return -1.0, None
    covers = [[[1] + [0] * (k - 1)] for _ in state]
    for it in range(500):
        n = len(state); nv = k + n
        c = np.zeros(nv); c[k:] = -1; c[:k] = 1
        A = []; b = []
        for i in range(n):
            for cnt in covers[i]:
                row = np.zeros(nv); row[k + i] = 1; row[:k] = -np.array(cnt); A.append(row); b.append(0)
        r = linprog(c, A_ub=np.array(A), b_ub=b, A_eq=[np.r_[np.ones(k), np.zeros(n)]], b_eq=[1],
                    bounds=[(0, None)] * k + [(None, None)] * n, method='highs')
        rho = r.x[:k]; z = r.x[k:]; val = -r.fun; added = 0
        for i in range(n):
            cost, cnt = phi_cover(state[i], list(rho))
            if cost < z[i] - 1e-9: covers[i].append(cnt); added += 1
        if not added: return val, rho
    return val, rho
def integerise(rho, state):
    for den in (10, 20, 50, 100, 200, 500, 1000, 5000):
        iv = [int(round(x * den)) for x in rho]; g = 0
        for v in iv: g = gcd(g, v)
        if g == 0: continue
        iv = [v // g for v in iv]
        if sum(phi(S, iv) for S in state) >= sum(iv): return iv
    return None
t0 = time.time(); fam = []
print(f'D={D} m={m} L0={L0} divisors={DIV} items={items}', flush=True)
for rnd in range(MAXR):
    surv, nodes = search(fam)
    if not surv:
        print(f'[{time.time()-t0:.0f}s] round {rnd}: NO SURVIVORS ({nodes} nodes) with {len(fam)} price vectors: '
              f'no covering with moduli 2^i d, d|{D}, >= {m}, for any a', flush=True)
        print('family', fam); break
    st = surv[0]
    val, rho = lp_kill(st)
    if val < -1e-9:
        print(f'[{time.time()-t0:.0f}s] round {rnd}: ALIVE survivor (LP value {val:.4f}); method cannot certify. '
              f'columns sizes {[bin(c).count("1") for c in st]}', flush=True); break
    iv = integerise(rho, st)
    print(f'[{time.time()-t0:.0f}s] round {rnd}: survivor killed, LP {val:.4f}, add {iv} ({nodes} nodes)', flush=True)
    if iv is None: print('integerisation failed'); break
    fam.append(iv)
