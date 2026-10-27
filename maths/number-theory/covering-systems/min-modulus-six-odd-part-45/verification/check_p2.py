#!/usr/bin/env python3
"""Independent checker (standard library only) for the claim:

  For every a >= 0 there is no finite system of congruences with distinct moduli, every modulus >= 6 and
  dividing 2^a * 45, that covers the integers.

Method (see README): for a price vector rho = (rho_1, rho_3, rho_5, rho_9, rho_15, rho_45) let phi_rho(S) be the
minimum total price of residue classes mod divisors of 45 covering a set S of residues mod 45.  For a system with
moduli dividing 2^k * 45 let the 'columns' be S_x = {b mod 45 : b uncovered mod 2^k*45, b = x mod 2^k} and
Q_rho = sum_x phi_rho(S_x).  Lemma: if k >= 2 and Q_rho >= R_rho = sum(rho), the system cannot be completed to a
covering with larger moduli 2^i d (i > k).  This script enumerates (up to translation and tree symmetry) every
system with moduli in {9,15,45, 6,10,18,30,90, 12,20,36,60,180} and checks that each one has Q_rho >= R_rho for
some rho in the family.  Run:  python3 check_p2.py family.txt [root_index_start root_index_stop]
"""
import sys, time
from itertools import combinations

N = 45
DIVS = [1, 3, 5, 9, 15, 45]

def cls(d, r):
    """residues y mod 45 with y = r (mod d), as a bitmask"""
    m = 0
    for y in range(N):
        if (y - r) % d == 0:
            m |= 1 << y
    return m

CLASSES = {d: [cls(d, r) for r in range(d)] for d in DIVS}
FULL = (1 << N) - 1

def phi_brute(S, rho):
    """exact min-cost cover by exhaustive branching on the lowest uncovered residue (small sets only)"""
    best = [rho[0] if S else 0]
    def rec(T, cost):
        if cost >= best[0]:
            return
        if not T:
            best[0] = cost
            return
        y = (T & -T).bit_length() - 1
        for k, d in enumerate(DIVS):
            rec(T & ~CLASSES[d][y % d], cost + rho[k])
    rec(S, 0)
    return best[0]

def phi(S, rho):
    """exact min-cost cover using the product structure Z/45 = Z/9 x Z/5:
    choose the set V of classes mod 5 used; then, independently for each class beta mod 3, either one class
    mod 3 or a set U of classes mod 9 inside beta plus, for each v not in V, either one class mod 15
    (beta, v) or single residues mod 45."""
    if not S:
        return 0
    r1, r3, r5, r9, r15, r45 = rho
    ys = [y for y in range(N) if S >> y & 1]
    best = r1
    for nv in range(6):
        for V in combinations(range(5), nv):
            cost = r5 * nv
            if cost >= best:
                continue
            for beta in range(3):
                us = [u for u in range(9) if u % 3 == beta]
                cb = r3
                for nu in range(4):
                    for U in combinations(us, nu):
                        c = r9 * nu
                        for v in range(5):
                            if v in V:
                                continue
                            k = sum(1 for y in ys if y % 5 == v and y % 3 == beta and (y % 9) not in U)
                            if k:
                                c += min(r15, r45 * k)
                        cb = min(cb, c)
                cost += cb
            best = min(best, cost)
    return best

def selftest():
    import random
    rng = random.Random(1)
    for t in range(300):
        rho = [rng.randint(1, 30) for _ in range(6)]
        S = 0
        p = rng.random() * 0.5
        for y in range(N):
            if rng.random() < p:
                S |= 1 << y
        a, b = phi(S, rho), phi_brute(S, rho)
        assert a == b, (S, rho, a, b)
    print('selftest: structured cover == exhaustive cover on 300 random instances', flush=True)

def main():
    fam = [list(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 135
    selftest()
    R = [sum(r) for r in fam]
    memo = [dict() for _ in fam]
    def ph(f, S):
        m = memo[f]
        v = m.get(S)
        if v is None:
            v = phi(S, fam[f]); m[S] = v
        return v
    # level-1 and level-2 moduli 2^i d (d | 45, 2^i d >= 6), processed in this order
    items = [(1, 3), (1, 5), (2, 3), (1, 9), (1, 15), (2, 5), (2, 9), (1, 45), (2, 15), (2, 45)]
    impact = [[(2 if i == 1 else 1) * fam[f][DIVS.index(d)] for f in range(len(fam))] for (i, d) in items]
    stats = {'nodes': 0, 'surv': 0}
    t0 = time.time()
    cols = [0, 0, 0, 0]  # column x = b mod 4
    def dead(rem):
        for f in range(len(fam)):
            if sum(ph(f, c) for c in cols) - rem[f] >= R[f]:
                return True
        return False
    def dfs(t, rem):
        stats['nodes'] += 1
        if dead(rem):
            return
        if t == len(items):
            stats['surv'] += 1
            print('SURVIVOR', cols, flush=True)
            return
        i, d = items[t]
        rem2 = [rem[f] - impact[t][f] for f in range(len(fam))]
        dfs(t + 1, rem2)  # modulus unused (or its class meets no uncovered residue)
        # tree symmetry: the subtrees x = 0,2 (b = 0 mod 2) and x = 1,3 (b = 1 mod 2) are interchangeable
        # when they carry the same pair of columns; within a subtree x and x+2 are interchangeable if equal.
        sym_odd = sorted((cols[0], cols[2])) == sorted((cols[1], cols[3]))
        if i == 1:
            for x2 in (0, 1):
                if x2 == 1 and sym_odd:
                    break
                for r in range(d):
                    m = CLASSES[d][r]
                    a, b = cols[x2], cols[x2 + 2]
                    if not ((a | b) & m):
                        continue
                    cols[x2], cols[x2 + 2] = a & ~m, b & ~m
                    dfs(t + 1, rem2)
                    cols[x2], cols[x2 + 2] = a, b
        else:
            for x in range(4):
                if x % 2 == 1 and sym_odd:
                    continue
                if x >= 2 and cols[x] == cols[x - 2]:
                    continue
                a = cols[x]
                for r in range(d):
                    m = CLASSES[d][r]
                    if not (a & m):
                        continue
                    cols[x] = a & ~m
                    dfs(t + 1, rem2)
                    cols[x] = a
    roots = [(0, r15, r45) for r15 in (0, 5, 10) for r45 in range(45)]
    for idx in range(lo, hi):
        r9, r15, r45 = roots[idx]
        S0 = FULL & ~CLASSES[9][r9] & ~CLASSES[15][r15] & ~CLASSES[45][r45]
        for x in range(4):
            cols[x] = S0
        rem = [sum(impact[t][f] for t in range(len(items))) for f in range(len(fam))]
        n0 = stats['nodes']
        dfs(0, rem)
        print(f'[{time.time()-t0:.0f}s] root {idx} (9:{r9} 15:{r15} 45:{r45}) nodes {stats["nodes"]-n0} '
              f'total {stats["nodes"]} survivors {stats["surv"]}', flush=True)
    print(f'DONE roots {lo}..{hi-1}: nodes {stats["nodes"]} survivors {stats["surv"]}', flush=True)

if __name__ == '__main__':
    main()
