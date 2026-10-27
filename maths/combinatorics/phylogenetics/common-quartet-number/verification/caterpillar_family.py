#!/usr/bin/env python3
"""Proposition 4.1 (standard library): the caterpillars C_0..C_{k-1} on 2^k+1 leaves have no common quartet.
Layer j (1 <= j <= L = 2^(k-1)) is {j, m+1-j}, m = 2L+1, centre L+1. C_t puts m+1-j (instead of j) at
position j iff t >= 1 and binary digit t-1 of j-1 is 1. A caterpillar splits a 4-set into its first two and
last two leaves. Usage: caterpillar_family.py KMAX (default 6; k = 6 has 677040 four-sets)."""
import itertools, sys

def family(k):
    L = 2 ** (k - 1); m = 2 * L + 1
    orders = []
    for t in range(k):
        left, right = [], []
        for j in range(1, L + 1):
            a, b = j, m + 1 - j
            if t >= 1 and ((j - 1) >> (t - 1)) & 1:
                a, b = b, a
            left.append(a); right.append(b)
        orders.append(left + [L + 1] + right[::-1])
    return m, orders

def common_quartets(m, orders):
    pos = [{e: i for i, e in enumerate(o)} for o in orders]
    count = 0
    for Q in itertools.combinations(range(1, m + 1), 4):
        first = None; same = True
        for p in pos:
            s = sorted(Q, key=p.get)
            split = frozenset((frozenset(s[:2]), frozenset(s[2:])))
            if first is None: first = split
            elif split != first: same = False; break
        count += same
    return count

if __name__ == '__main__':
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for k in range(1, kmax + 1):
        m, orders = family(k)
        c = common_quartets(m, orders)
        assert c == 0
        print(f'k={k}: {k} caterpillars on {m} leaves, common quartets: {c}' + (f'  orders {orders}' if k <= 3 else ''), flush=True)
    print('OK')
