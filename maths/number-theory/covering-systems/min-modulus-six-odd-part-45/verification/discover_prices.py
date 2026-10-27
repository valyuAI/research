# Price discovery (not needed for verification; uses numpy and scipy).
# Iterate: exhaustive C DFS finds level-2 survivors of the price family; an LP (column generation with an exact
# structured cover oracle) finds prices killing each survivor; integerised prices are added; repeat until the
# DFS finds no survivor in any level-0 orbit.
import subprocess, sys, time, json
import numpy as np
from fractions import Fraction
from math import gcd
from scipy.optimize import linprog
DS = [1, 3, 5, 9, 15, 45]
def bits(m): return [i for i in range(45) if m >> i & 1]
def phi_cover(S, rho):
    """exact min-cost cover of set S (int mask) under prices rho; returns (cost, count vector)."""
    if not S: return 0, [0]*6
    best = (rho[0], [1, 0, 0, 0, 0, 0])
    pts = [(i // 5, i % 5) for i in bits(S)]
    for V in range(32):
        cost = rho[2] * bin(V).count('1'); cnt = [0, 0, bin(V).count('1'), 0, 0, 0]
        for b in range(3):
            cb = rho[1]; cbv = [0, 1, 0, 0, 0, 0]
            for U in range(8):
                us = [b + 3 * j for j in range(3) if U >> j & 1]
                c = rho[3] * len(us); cv = [0, 0, 0, len(us), 0, 0]
                for v in range(5):
                    if V >> v & 1: continue
                    k = sum(1 for (u, vv) in pts if vv == v and u % 3 == b and u not in us)
                    if k:
                        if rho[4] <= rho[5] * k: c += rho[4]; cv[4] += 1
                        else: c += rho[5] * k; cv[5] += k
                if c < cb: cb = c; cbv = cv
            cost += cb; cnt = [cnt[i] + cbv[i] for i in range(6)]
        if cost < best[0]: best = (cost, cnt)
    return best
def lp_kill(state):
    covers = [[[1, 0, 0, 0, 0, 0]] for _ in state]
    for it in range(300):
        n = len(state); nv = 6 + n
        c = np.zeros(nv); c[6:] = -1; c[:6] = 1
        A = []; b = []
        for i in range(n):
            for cnt in covers[i]:
                row = np.zeros(nv); row[6 + i] = 1; row[:6] = -np.array(cnt); A.append(row); b.append(0)
        r = linprog(c, A_ub=np.array(A), b_ub=b, A_eq=[np.r_[np.ones(6), np.zeros(n)]], b_eq=[1],
                    bounds=[(0, None)] * 6 + [(None, None)] * n, method='highs')
        rho = r.x[:6]; z = r.x[6:]; val = -r.fun
        added = 0
        for i in range(n):
            cost, cnt = phi_cover(state[i], list(rho))
            if cost < z[i] - 1e-9: covers[i].append(cnt); added += 1
        if not added: return val, rho
    return val, rho
def integerise(rho, state):
    for den in (10, 20, 30, 50, 100, 200, 500, 1000):
        iv = [int(round(x * den)) for x in rho]
        g = 0
        for v in iv: g = gcd(g, v)
        if g == 0: continue
        iv = [v // g for v in iv]
        if sum(phi_cover(S, iv)[0] for S in state) >= sum(iv): return iv
    return None
famfile = sys.argv[1];  # requires ./dfs2 (compiled from c/dfs2.c) in the working directory
maxsurv = int(sys.argv[2]) if len(sys.argv) > 2 else 20
fam = [list(map(int, l.split())) for l in open(famfile) if l.strip()]
t0 = time.time(); rnd = 0
while True:
    rnd += 1
    open(famfile, 'w').write('\n'.join(' '.join(map(str, r)) for r in fam) + '\n')
    p = subprocess.run(['./dfs2', famfile, str(maxsurv), '-1', 'surv_round.txt'], capture_output=True, text=True)
    tail = [l for l in p.stderr.splitlines() if 'TOTAL' in l or 'max surv' in l]
    survs = [list(map(int, l.split())) for l in open('surv_round.txt') if l.strip()]
    print(f'[{time.time()-t0:.0f}s] round {rnd} fam {len(fam)} survivors {len(survs)} {tail}', flush=True)
    if not survs:
        print('NO SURVIVORS: every level-2 state is dead under the family', flush=True); break
    added = 0
    for s in survs:
        state = [m for m in s if m]
        if any(sum(phi_cover(S, r)[0] for S in state) >= sum(r) for r in fam): continue
        val, rho = lp_kill(state)
        if val < -1e-9:
            print('  ALIVE survivor (LP value %.5f):' % val, s, flush=True)
            json.dump({'state': s, 'lp': val}, open(f'alive_{rnd}.json', 'w'))
            sys.exit(0)
        iv = integerise(rho, state)
        if iv is None:
            print('  integerisation failed', s, rho, flush=True); sys.exit(1)
        fam.append(iv); added += 1
        print(f'  killed {[len(bits(m)) for m in state]} LP {val:.4f} -> {iv}', flush=True)
    if not added:
        print('  no new prices added?!', flush=True); sys.exit(1)
