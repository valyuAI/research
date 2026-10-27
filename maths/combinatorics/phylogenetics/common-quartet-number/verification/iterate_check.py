#!/usr/bin/env python3
"""Executable form of the upper-bound proof (standard library only). For k random trees on
n = 2*3^(k-1)+1 leaves: take centroid edges of T1 and T2 (full leaf set), then for T3..Tk the centroid
edge of T_i restricted to X u Y, keeping the better diagonal each time. Asserts that the guaranteed size
bounds hold at every step and that the final quartet is common to all k trees.
Second part (Theorem 2.7): for the least n with n > 3*((1+sqrt(13))/2)^(k-1), the strategy that balances the cut on
the larger set (leaf weights 0 on the smaller set X, 1/|Y| on Y); asserts that the potential
Psi = min(|X||Y|, 2|X|^2, 2|Y|^2) retains at least (7-sqrt(13))/18 and that the final quartet is
common to all k trees."""

from fractions import Fraction as F
import random, sys, itertools
from collections import deque
from math import isqrt

if not __debug__:
    raise SystemExit("FAIL: verification requires Python assertions enabled")


def random_tree(n, rng):
    adj = {0: [n], 1: [n], 2: [n], n: [0, 1, 2]}
    nxt = n + 1
    labels = list(range(n))
    rng.shuffle(labels)
    order = labels  # insert leaves in random label order
    adj = {
        order[0]: [n],
        order[1]: [n],
        order[2]: [n],
        n: [order[0], order[1], order[2]],
    }
    for leaf in order[3:]:
        edges = [(u, v) for u in adj for v in adj[u] if u < v]
        u, v = rng.choice(edges)
        w = nxt
        nxt += 1
        adj[u] = [w if z == v else z for z in adj[u]]
        adj[v] = [w if z == u else z for z in adj[v]]
        adj[w] = [u, v, leaf]
        adj[leaf] = [w]
    return adj


def edge_splits(adj, n, S):
    """for each edge, the set of leaves of S on one side"""
    out = []
    for u in adj:
        for v in adj[u]:
            if u < v:
                seen = {u, v}
                st = [v]
                side = set()
                while st:
                    x = st.pop()
                    if x < n and x in S:
                        side.add(x)
                    for y in adj[x]:
                        if y not in seen:
                            seen.add(y)
                            st.append(y)
                out.append((frozenset(side), frozenset(S - side)))
    return out


def centroid(adj, n, S):
    """edge maximising the smaller side of S (equivalent to some edge of T|S meeting Lemma 2.1)"""
    return max(edge_splits(adj, n, S), key=lambda p: min(len(p[0]), len(p[1])))


def split4(adj, a, b, c, d):
    def dist(s):
        D = {s: 0}
        dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in D:
                    D[y] = D[x] + 1
                    dq.append(y)
        return D

    Da, Db, Dc = dist(a), dist(b), dist(c)
    s = (Da[b] + Dc[d], Da[c] + Db[d], Da[d] + Db[c])
    return s.index(min(s))


def phi(s):
    return ((2 * s + 2) // 3 + 1) // 2  # floor((ceil(2s/3)+1)/2)


def run(k, trials, seed):
    rng = random.Random(seed)
    n = 2 * 3 ** (k - 1) + 1
    for tr in range(trials):
        trees = [random_tree(n, rng) for _ in range(k)]
        L = frozenset(range(n))
        X, Y = centroid(trees[0], n, L)
        assert min(len(X), len(Y)) >= -(-n // 3)
        W, Z = centroid(trees[1], n, L)
        assert min(len(W), len(Z)) >= -(-n // 3)
        bound = ((-(-n // 3)) + 1) // 2
        X, Y = max(
            [(X & Z, Y & W), (X & W, Y & Z)], key=lambda p: min(len(p[0]), len(p[1]))
        )
        assert min(len(X), len(Y)) >= bound, (len(X), len(Y), bound)
        s = bound
        for T in trees[2:]:
            W, Z = centroid(T, n, X | Y)
            assert min(len(W), len(Z)) >= -(-(2 * s) // 3)
            X, Y = max(
                [(X & Z, Y & W), (X & W, Y & Z)],
                key=lambda p: min(len(p[0]), len(p[1])),
            )
            assert min(len(X), len(Y)) >= phi(s), (len(X), len(Y), phi(s))
            s = phi(s)
        assert s >= 2
        a, b = sorted(X)[:2]
        c, d = sorted(Y)[:2]
        q = sorted((a, b, c, d))
        tops = {split4(T, *q) for T in trees}
        assert len(tops) == 1, "not common!"
    print(
        f"k={k} n={n}: {trials} random families, all steps within bounds, common quartet found each time"
    )


def psi(a, d):
    return min(a * d, 2 * a * a, 2 * d * d)


def sharp_threshold(k):
    """Exact floor(3 beta^(k-1))+1, using integer arithmetic and beta=(1+sqrt(13))/2."""
    assert k >= 1
    a, b = 1, 0
    for _ in range(k - 1):
        a, b = a + 13 * b, a + b
    # beta^(k-1) = (a + b sqrt(13))/2^(k-1). Flooring the
    # nonnegative radical before integer division preserves the floor.
    return (3 * a + isqrt(117 * b * b)) // 2 ** (k - 1) + 1


def keeps_sharp_factor(new, old):
    """Compare new/old >= (7-sqrt(13))/18 without floating point."""
    assert old > 0
    gap = 7 * old - 18 * new
    return gap <= 0 or gap * gap <= 13 * old * old


def run_weighted(k, trials, seed):
    rng = random.Random(seed)
    n = sharp_threshold(k)
    print(f"weighted, k={k} n={n}: starting {trials} families", flush=True)
    for tr in range(trials):
        trees = [random_tree(n, rng) for _ in range(k)]
        L = frozenset(range(n))
        X, Y = centroid(trees[0], n, L)
        assert 9 * psi(len(X), len(Y)) >= 2 * n * n
        for step, T in enumerate(trees[1:], 1):
            if len(X) > len(Y):
                X, Y = Y, X
            a, d = len(X), len(Y)
            assert 2 <= a <= d
            cand = []
            for S, R in edge_splits(T, n, X | Y):
                w = F(len(S & Y), d)
                if F(1, 3) <= w <= F(2, 3):
                    cand.append((S, R))
            assert cand, "weighted balanced edge missing"
            Z, W = cand[0]
            X2, Y2 = max(
                [(X & Z, Y & W), (X & W, Y & Z)],
                key=lambda p: psi(len(p[0]), len(p[1])),
            )
            assert keeps_sharp_factor(psi(len(X2), len(Y2)), psi(a, d)), (
                a,
                d,
                len(X2),
                len(Y2),
            )
            X, Y = X2, Y2
            assert psi(len(X), len(Y)) > 2
            for earlier in trees[: step + 1]:
                assert any(
                    (X <= S and Y <= R) or (X <= R and Y <= S)
                    for S, R in edge_splits(earlier, n, X | Y)
                ), "separation lost"
        assert psi(len(X), len(Y)) > 2 and min(len(X), len(Y)) >= 2
        a, b = sorted(X)[:2]
        c, d = sorted(Y)[:2]
        tops = {split4(T, *sorted((a, b, c, d))) for T in trees}
        assert len(tops) == 1, "not common!"
        if (tr + 1) % max(1, trials // 5) == 0:
            print(f"weighted, k={k}: {tr + 1}/{trials} families passed", flush=True)
    print(
        f"weighted, k={k} n={n}: {trials} random families, sharp Psi factor and separation at every step, common quartet found each time",
        flush=True,
    )


def check_step_lemma(N=60):
    """Exact check of Lemma 2.6 on a rational grid (illustration; the lemma is proved in the paper): r = d/a in [1, 2], x, y multiples of 1/N, 1/3 <= y <= 2/3."""
    worst = None
    for ri in range(N + 1):
        r = 1 + F(ri, N)
        for i in range(N + 1):
            for j in range(N + 1):
                x, y = F(i, N), F(j, N)
                if not (F(1, 3) <= y <= F(2, 3)):
                    continue
                v = max(psi(x, (1 - y) * r), psi(1 - x, y * r)) / psi(F(1), r)
                assert keeps_sharp_factor(v, 1), (r, x, y, v)
                if worst is None or v < worst[0]:
                    worst = (v, r, x, y)
        if ri % 10 == 0:
            print(f"Lemma 2.6 grid: {ri + 1}/{N + 1} ratios checked", flush=True)
    print(
        f"Lemma 2.6 grid check (N={N}): minimum ratio {worst[0]} at r={worst[1]}, x={worst[2]}, y={worst[3]}"
    )


if __name__ == "__main__":
    assert [sharp_threshold(k) for k in range(1, 9)] == [
        4,
        7,
        16,
        37,
        85,
        195,
        448,
        1031,
    ]
    assert keeps_sharp_factor(17, 90)
    assert not keeps_sharp_factor(3, 16)
    for k, trials in ((2, 300), (3, 200), (4, 50), (5, 10)):
        run(k, trials, seed=k)
    check_step_lemma()
    for k, trials in ((1, 50), (2, 300), (3, 200), (4, 50), (5, 10), (6, 3)):
        run_weighted(k, trials, seed=100 + k)
