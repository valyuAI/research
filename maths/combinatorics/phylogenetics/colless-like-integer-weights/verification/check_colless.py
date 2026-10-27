#!/usr/bin/env python3
"""Standard-library checks for the note on Colless-like indices with commensurable weights.

1. For several integer weight functions f, list two different outdegree sequences w, w' (fully symmetric
   trees FS_w, FS_w') with equal f-size, computed twice: by the closed formula and by building the trees
   and summing f(outdegree) over all vertices. Then build the tree whose root has children FS_w and FS_w'
   and evaluate C_{D,f} for D = variance, standard deviation and mean deviation from the median: all zero,
   although the tree is not fully symmetric.
2. For random integer weights (values 0..50 at outdegrees 2,3,4; f(0) is irrelevant), find the least m with
   (3m)!/(m!)^3 > M 24^m + 1, the inequality used in the proof.
"""
import itertools, math, random, statistics
from fractions import Fraction

def fsize_formula(w, f):
    p, s = 1, 0
    for k in w:
        s += p * f(k); p *= k
    return s + p * f(0)

def build_fs(w):
    """fully symmetric tree as nested tuples: leaves are ()"""
    t = ()
    for k in reversed(w):
        t = tuple([t] * k)
    return t

def fsize_tree(t, f):
    return f(len(t)) + sum(fsize_tree(c, f) for c in t)

def canon(t):
    return '(' + ''.join(sorted(canon(c) for c in t)) + ')'

def fully_symmetric(t):
    return all(len({canon(c) for c in t}) <= 1 and fully_symmetric(c) for c in t)

def colless_like(t, f, D):
    if not t: return 0
    vals = [fsize_tree(c, f) for c in t]
    return D(vals) + sum(colless_like(c, f, D) for c in t)

def var(v): m = Fraction(sum(v), len(v)); return sum((Fraction(x) - m) ** 2 for x in v) / len(v)
def mdm(v): med = statistics.median(v); return sum(abs(x - med) for x in v) / len(v)
def sd(v): return math.sqrt(var(v))

def words(maxprod):
    out = []
    def rec(w, p):
        out.append(tuple(w))
        k = 2
        while p * k <= maxprod:
            w.append(k); rec(w, p * k); w.pop(); k += 1
    rec([], 1)
    return out

def first_collision(f, maxprod=2000):
    seen = {}
    for w in sorted(words(maxprod), key=lambda w: (math.prod(w), w)):
        d = fsize_formula(w, f)
        if d in seen: return seen[d], w, d
        seen[d] = w
    return None

def main():
    examples = {
        'f(n) = n + 1': lambda n: n + 1,
        'f(n) = 2^n': lambda n: 2 ** n,
        'f(n) = n! + 1': lambda n: math.factorial(n) + 1,
        'f(n) = n^3 + 1': lambda n: n ** 3 + 1,
        'f(n) = (n + 1)-th prime': lambda n: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97][n] if n < 25 else 10 ** 6 + n,
    }
    for name, f in examples.items():
        w1, w2, d = first_collision(f)
        t1, t2 = build_fs(w1), build_fs(w2)
        assert fsize_tree(t1, f) == fsize_tree(t2, f) == d and canon(t1) != canon(t2)
        T = (t1, t2)
        assert not fully_symmetric(T)
        vals = [colless_like(T, f, D) for D in (var, sd, mdm)]
        assert all(v == 0 for v in vals)
        print(f'{name}: FS{w1} and FS{w2} both have f-size {d}; the tree with these two root subtrees '
              f'is not fully symmetric and has C_(D,f) = 0 for D = var, sd, MDM')
    rng = random.Random(2026)
    for trial in range(5):
        a = {j: rng.randint(0, 50) for j in (2, 3, 4)}; a[0] = rng.randint(0, 50)
        M = max(a[j] for j in (2, 3, 4))
        m = 1
        while math.factorial(3 * m) // math.factorial(m) ** 3 <= M * 24 ** m + 1:
            m += 1
        found = None
        if m <= 6:
            seen = {}
            for w in set(itertools.permutations([2] * m + [3] * m + [4] * m)):
                d = fsize_formula(w, lambda k: a[k])
                if d in seen: found = (seen[d], w); break
                seen[d] = w
        print(f'weights {a}: counting guarantees a collision at m = {m} (trees with 24^{m} leaves)'
              + (f'; direct search finds {found[0]} ~ {found[1]}' if found else ''))
        if m <= 6: assert found
    print('OK')

if __name__ == '__main__':
    main()
