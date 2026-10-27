"""Exhaustive check behind Proposition prop:four of the paper (four reactant complexes, four species).

For every set of four distinct at-most-bimolecular complexes y1..y4 in four species
whose difference matrix M = [y1-y4; y2-y4; y3-y4] has rank 3, compute the kernel
vector b of M exactly. If some coordinate of b vanishes (a necessary condition for
ACR on the toric steady-state curve x* exp(t b)), record the number of distinct
values among the coordinates of b. The proposition needs: at most 3 distinct values.

Run: python3 four_reactant_exponents.py   (standard library only)
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations


def complexes(n):
    out = [tuple([0] * n)]
    for i in range(n):
        e = [0] * n
        e[i] = 1
        out.append(tuple(e))
    for i in range(n):
        for j in range(i, n):
            e = [0] * n
            e[i] += 1
            e[j] += 1
            out.append(tuple(e))
    return out


def nullspace(rows, ncols):
    """Reduced row echelon form over Q; return a basis of the right kernel."""
    m = [[Q(x) for x in r] for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        v = [Q(0)] * ncols
        v[fc] = Q(1)
        for i, pc in enumerate(pivots):
            v[pc] = -m[i][fc]
        basis.append(v)
    return basis


def main():
    n = 4
    C = complexes(n)
    assert len(C) == 15
    stats = Counter()
    worst = 0
    for ys in combinations(C, 4):
        M = [[a - b for a, b in zip(ys[j], ys[3])] for j in range(3)]
        ker = nullspace(M, n)
        if len(ker) != 1:
            stats["rank<3"] += 1
            continue
        b = ker[0]
        if all(x != 0 for x in b):
            stats["no zero coordinate"] += 1
            continue
        distinct = len(set(b))
        stats[f"zero coordinate, {distinct} distinct values"] += 1
        worst = max(worst, distinct)
    for k, v in sorted(stats.items()):
        print(f"{k}: {v}")
    assert worst <= 3, "found a kernel vector with four distinct values"
    print(f"maximum number of distinct kernel values with a zero coordinate: {worst}")
    print("FOUR-REACTANT CHECK PASSED")


if __name__ == "__main__":
    main()
