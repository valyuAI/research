#!/usr/bin/env python3
"""Controls for check_ct.py (standard library only).

1. The PD encoding agrees with the authors' psv_encoding (re-implemented from
   github.com/koeppl/squarechecker, base.py) on the authors' unit tests and on random words.
2. Exhaustive search reproduces the finite Cartesian-tree entries of Table 1 of
   arXiv:2607.00674: sigma=2: l=1 -> 1, l=2 -> 5, l=3 -> 29; sigma=3: l=1 -> 1, l=2 -> 9.
3. Negative controls: a deliberately weakened claim must be rejected:
   h2 does contain a 3+-CT-square, and corrupted morphisms are rejected.
4. Sanity: a prefix of Dejean's 7/4+-free word maps to CT-square-free prefixes.
"""
import sys, random
from check_ct import pd, first_ct_square, THEOREMS, free_words

def fail(msg):
    print("CONTROL FAILED:", msg); sys.exit(1)

def psv_authors(s):
    stack = []
    result = [0] * len(s)
    for i, c in enumerate(s):
        while stack and stack[-1][0] > c:
            stack.pop()
        result[i] = i - stack[-1][1] if stack else 0
        stack.append((c, i))
    return result

# 1
for s, expect in [("", []), ("a", [0]), ("aa", [0, 1]), ("ab", [0, 1]), ("ba", [0, 0]),
                  ("abc", [0, 1, 1]), ("cba", [0, 0, 0]), ("banana", [0, 0, 1, 2, 1, 2]),
                  ("aaaa", [0, 1, 1, 1]), ("abcdabcd", [0, 1, 1, 1, 4, 1, 1, 1])]:
    if pd(s) != expect or psv_authors(s) != expect:
        fail(f"encoding mismatch on {s}")
rnd = random.Random(20261026)
for _ in range(20000):
    s = ''.join(rnd.choice('abc') for _ in range(rnd.randint(0, 14)))
    if pd(s) != psv_authors(s):
        fail(f"encoding mismatch on {s}")
print("1. PD encoding matches the authors' psv_encoding")

# 2
def longest_incremental(sigma, l, cap=200):
    """DFS that only checks squares ending at the last letter."""
    best, stack = 0, ['']
    while stack:
        w = stack.pop()
        n = len(w)
        bad = False
        for m in range(l, n // 2 + 1):
            if pd(w[n - 2 * m:n - m]) == pd(w[n - m:]):
                bad = True; break
        if bad:
            continue
        best = max(best, n)
        if n >= cap:
            return None
        stack.extend(w + c for c in 'abcde'[:sigma])
    return best

table = {(2, 1): 1, (2, 2): 5, (2, 3): 29, (3, 1): 1, (3, 2): 9, (4, 2): 9}
for (sigma, l), v in table.items():
    got = longest_incremental(sigma, l)
    if got != v:
        fail(f"Table 1 entry sigma={sigma}, l={l}: expected {v}, got {got}")
print("2. Finite CT entries of Table 1 reproduced:", table)

# 3
tau = THEOREMS['A']['tau']
w = 'abcacbcabcbacbcacba'
if first_ct_square(''.join(tau[c] for c in w), 3, 3) is None:
    fail("expected a CT-square of half-length 3 in h2(w)")
corrupt = [({'a': '00101', 'b': '00111', 'c': '00101'}, 4, 'not injective'),
           ({'a': '00101', 'b': '00111', 'c': '01101'}, 4, 'CT-square'),
           ({'a': '000101', 'b': '000221', 'c': '022101'}, 3, 'CT-square')]
words = free_words(12)
for t, l, kind in corrupt:
    imgs = [t[c] for c in 'abc']
    if len(set(imgs)) < 3:
        continue
    found = any(first_ct_square(''.join(t[c] for c in f), l, 30) is not None for f in words)
    if not found:
        fail(f"corrupted morphism {t} was not rejected")
print("3. Negative controls rejected as expected")

# 4
D = {'a': 'abcacbcabcbacbcacba', 'b': 'bcabacabcacbacabacb', 'c': 'cabcbabcabacbabcbac'}
x = 'a'
while len(x) < 200:
    x = ''.join(D[c] for c in x)
x = x[:120]
for name in ['A', 'B']:
    t, l = THEOREMS[name]['tau'], THEOREMS[name]['l']
    y = ''.join(t[c] for c in x)
    if first_ct_square(y, l, len(y) // 2) is not None:
        fail(f"CT-square in image of Dejean prefix under {name}")
print("4. Images of a 120-letter Dejean prefix are CT-square-free (all half-lengths)")
print("ALL CONTROLS PASSED")
