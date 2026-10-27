#!/usr/bin/env python3
"""Independent standard-library verifier for two theorems on Cartesian-tree squares.

Theorem A (binary, l = 4):  h2: a -> 00101, b -> 00111, c -> 01100   (letters 0 < 1).
Theorem B (ternary, l = 3): h3: a -> 000101, b -> 000221, c -> 022211 (letters 0 < 1 < 2).
For every infinite ternary word w with no factor of exponent > 7/4,
h(w) contains no Cartesian-tree square uv with |u| = |v| >= l.

Cartesian-tree equivalence is tested through the parent-distance encoding
PD(x)[i] = i - max{j < i : x[j] <= x[i]}, or 0 if no such j.

Checked steps (the written lemma is in the paper):
  (1) h is injective on letters and synchronizing;
  (3) local decoding with radius r: factors of length 2r+1 with equal PD encodings
      have equal middle letters (and radius r-1 does not suffice);
  (6) no CT-square with half-length in [l, M], M = 4(2r + 2q - 2), inside h(f) for
      every 7/4+-free ternary f of every length 1..K, K = ceil((2M-1)/q) + 1.
Checks (3) and (6) range over all source lengths up to the coverage bound. For the
theorem as stated (infinite base words, Proposition 3.1 of the paper) length K alone
suffices; the shorter lengths are the additional check that the same argument would
need for finite base words, which the paper does not claim.
The program does not use assert statements; any failed check exits with status 1.
Usage: python3 -B -O check_ct.py [A] [B] [A6]
"""
import os, sys, json, time, hashlib
from math import ceil

THEOREMS = {
    'A': {'tau': {'a': '00101', 'b': '00111', 'c': '01100'}, 'l': 4, 'r': 3},
    'B': {'tau': {'a': '000101', 'b': '000221', 'c': '022211'}, 'l': 3, 'r': 3},
    'A6': {'tau': {'a': '001000', 'b': '011001', 'c': '011101'}, 'l': 4, 'r': 3},
}

def fail(msg):
    print("CHECK FAILED:", msg)
    sys.exit(1)

def pd(x):
    """Parent-distance encoding, quadratic and transparent."""
    out = []
    for i in range(len(x)):
        d = 0
        for j in range(i - 1, -1, -1):
            if x[j] <= x[i]:
                d = i - j
                break
        out.append(d)
    return out

def free_words(K, upto=False):
    """All ternary words of length K (or of every length 1..K if upto) with no factor of
    exponent > 7/4."""
    layer = ['']
    collected = []
    for _ in range(K):
        nxt = []
        for w in layer:
            for c in 'abc':
                v = w + c
                n = len(v)
                ok = True
                for p in range(1, n):      # factors ending at the new letter, with period p
                    L = p
                    while L < n and v[n - 1 - L] == v[n - 1 - L + p]:
                        L += 1
                    if 4 * L > 7 * p:
                        ok = False
                        break
                if ok:
                    nxt.append(v)
        layer = nxt
        collected.extend(layer)
    return collected if upto else layer

def decoding_ok(tau, q, r):
    W = 2 * r + 1
    classes = {}
    for w in free_words(ceil((W - 1) / q) + 1, upto=True):
        x = ''.join(tau[c] for c in w)
        for p in range(len(x) - W + 1):
            f = x[p:p + W]
            classes.setdefault(tuple(pd(f)), set()).add(f[r])
    return all(len(v) == 1 for v in classes.values()), len(classes)

def first_ct_square(x, lo, hi):
    """First (p, m) with lo <= m <= hi such that x[p:p+m] and x[p+m:p+2m] are CT-equivalent."""
    n = len(x)
    span = min(n, 2 * hi)
    pdf = []                      # PD of every suffix, truncated, via a monotone stack
    for p in range(n):
        st, enc = [], []
        for t in range(min(n - p, span)):
            c = x[p + t]
            while st and x[p + st[-1]] > c:
                st.pop()
            enc.append(t - st[-1] if st else 0)
            st.append(t)
        pdf.append(enc)
    for m in range(lo, hi + 1):
        for p in range(0, n - 2 * m + 1):
            if pdf[p][:m] == pdf[p + m][:m]:
                return p, m
    return None

def check(name):
    spec = THEOREMS[name]
    tau, l, r = spec['tau'], spec['l'], spec['r']
    t0 = time.time()
    imgs = [tau[c] for c in 'abc']
    q = len(imgs[0])
    if any(len(s) != q for s in imgs):
        fail("morphism is not uniform")
    injective = len(set(imgs)) == 3
    sync = all((tau[a] + tau[b])[off:off + q] not in imgs
               for a in 'abc' for b in 'abc' for off in range(1, q))
    if not (injective and sync):
        fail(f"{name}: injective={injective} synchronizing={sync}")
    dec, nclasses = decoding_ok(tau, q, r)
    if not dec:
        fail(f"{name}: radius {r} does not decode")
    dec1, _ = decoding_ok(tau, q, r - 1)
    M = 4 * (2 * r + 2 * q - 2)
    K = ceil((2 * M - 1) / q) + 1
    exact = free_words(K)
    words = free_words(K, upto=True)
    for w in words:
        hit = first_ct_square(''.join(tau[c] for c in w), l, M)
        if hit is not None:
            fail(f"{name}: CT-square at {hit} in h({w})")
    res = {'theorem': name, 'tau': tau, 'l': l, 'q': q, 'r': r, 'M': M, 'K': K,
           'injective': injective, 'synchronizing': sync, 'pd_classes_radius_r': nclasses,
           'radius_r_minus_1_decodes': dec1, 'words_length_K': len(exact),
           'words_lengths_1_to_K': len(words),
           'words_sha256': hashlib.sha256('\n'.join(exact).encode()).hexdigest(),
           'ct_squares_found': 0, 'seconds': round(time.time() - t0, 1), 'status': 'verified'}
    print(json.dumps(res), flush=True)
    return res

if __name__ == '__main__':
    names = sys.argv[1:] or ['A', 'B']
    for n in names:
        if n not in THEOREMS:
            fail(f"unknown theorem {n}")
    out = [check(n) for n in names]
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_check_ct.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print("ALL CHECKS PASSED")
