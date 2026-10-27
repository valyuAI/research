#!/usr/bin/env python3
"""Standard-library verification for Conjecture 6.3 of arXiv:2610.29291v1.

lambda_k = (k, k-1, ..., 4, 3, 3).  A Latin tableau of shape lambda and type lambda' fills row i
with 1..lambda_i (each once) so that no column repeats an entry.

Checks:
  A. LT(lambda_k) = 9 * 4^(k-3) for k = 5, ..., KMAX by exhaustive enumeration
     (two different enumeration orders: bottom-up rows, and top-down rows).
  B. Every tableau of lambda_6 satisfies the invariants I1-I5 of the paper (base case).
  D. The six shapes listed after Conjecture 6.3 are wide and the supplied fillings are Latin
     tableaux of them.
  C. Sanity: every tableau of lambda_k satisfies I1-I5 and has exactly 4 one-row extensions,
     for k = 6, ..., KINV.
No assertions; exit status 1 on any failure.  Usage: check_latin.py [KMAX] [KINV]
"""
import itertools
import json
import os
import sys
import time

KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
KINV = int(sys.argv[2]) if len(sys.argv) > 2 else 8
RESULTS = []


def record(name, ok, detail=''):
  RESULTS.append({'check': name, 'ok': bool(ok), 'detail': detail})
  print(('PASS ' if ok else 'FAIL ') + name + (f' ({detail})' if detail else ''), flush=True)


def shape(k):
  return list(range(k, 3, -1)) + [3, 3]


def tableaux_bottom_up(lam):
  """All tableaux, rows filled from the bottom (shortest) row upwards."""
  rows = len(lam)
  cols = [set() for _ in range(lam[0])]
  filled = [None] * rows
  out = []

  def place(r):
    if r < 0:
      out.append(tuple(filled))
      return
    L = lam[r]
    for perm in itertools.permutations(range(1, L + 1)):
      if all(perm[j] not in cols[j] for j in range(L)):
        filled[r] = perm
        for j in range(L):
          cols[j].add(perm[j])
        place(r - 1)
        for j in range(L):
          cols[j].discard(perm[j])
  place(rows - 1)
  return out


def count_top_down(lam):
  """Count by filling rows from the top (longest) row downwards, cell by cell."""
  rows = len(lam)
  cols = [set() for _ in range(lam[0])]
  total = 0

  def row_fill(r, j, used):
    nonlocal total
    if r == rows:
      total += 1
      return
    L = lam[r]
    if j == L:
      row_fill(r + 1, 0, set())
      return
    for v in range(1, L + 1):
      if v not in used and v not in cols[j]:
        used.add(v)
        cols[j].add(v)
        row_fill(r, j + 1, used)
        cols[j].discard(v)
        used.discard(v)
  row_fill(0, 0, set())
  return total


def dominates(a, b):
  sa = sb = 0
  for i in range(len(a)):
    sa += a[i]
    sb += b[i] if i < len(b) else 0
    if sa < sb:
      return False
  return True


def conjugate(lam):
  return [sum(1 for x in lam if x >= c) for c in range(1, lam[0] + 1)]


def wide(lam):
  """Definition 2.2 of the source: every subpartition (any subset of the rows) dominates its conjugate."""
  n = len(lam)
  for mask in range(1, 1 << n):
    mu = [lam[i] for i in range(n) if mask >> i & 1]
    if not dominates(mu, conjugate(mu)):
      return False
  return True


def invariants(T, k):
  """I1-I5 for a tableau T (tuple of rows, top row first) of lambda_k; 1-indexed columns."""
  def col(c):
    return [row[c - 1] for row in T if len(row) >= c]
  r1 = T[0]
  i1 = (sorted(r1[0:3]) == [k - 2, k - 1, k]
        and all(r1[c - 1] == k + 1 - c for c in range(4, k - 2))
        and sorted(r1[k - 3:k]) == [1, 2, 3])
  i2 = (all(sorted(col(c)) == list(range(1, k - c + 2)) for c in range(4, k - 1))
        and len(col(k - 1)) == 2 and set(col(k - 1)) <= {1, 2, 3}
        and len(col(k)) == 1 and set(col(k)) <= {1, 2, 3})
  first3 = [set(col(c)) for c in (1, 2, 3)]
  i3 = (all(all(v in s for s in first3) for v in range(1, k - 1))
        and sum((k - 1) in s for s in first3) == 2
        and sum(k in s for s in first3) == 1)
  i4 = r1.index(k) != T[1].index(k - 1)
  i5 = r1[k - 1] != T[1][k - 2]
  return i1 and i2 and i3 and i4 and i5


def extensions(Tp, k):
  """Number of top rows of length k extending a tableau Tp of lambda_{k-1}."""
  colsets = [set() for _ in range(k)]
  for row in Tp:
    for j, v in enumerate(row):
      colsets[j].add(v)
  n = 0

  def rec(j, used):
    nonlocal n
    if j == k:
      n += 1
      return
    for v in range(1, k + 1):
      if v not in used and v not in colsets[j]:
        used.add(v)
        rec(j + 1, used)
        used.discard(v)
  rec(0, set())
  return n


def main():
  t0 = time.time()
  cache = {}
  for k in range(5, KMAX + 1):
    lam = shape(k)
    if k <= max(KINV, 6):
      cache[k] = tableaux_bottom_up(lam)
      n1 = len(cache[k])
    else:
      n1 = None
    n2 = count_top_down(lam)
    target = 9 * 4 ** (k - 3)
    ok = n2 == target and (n1 is None or n1 == target)
    record(f'LT{tuple(lam)} = 9*4^{k - 3} = {target}', ok,
           f'top-down count {n2}' + (f', bottom-up enumeration {n1}' if n1 is not None else '') + f', {time.time() - t0:.0f}s')
  wk = [k for k in range(5, 16) if wide(shape(k))]
  record('lambda_k is wide (all row subsets) for 5 <= k <= 15', wk == list(range(5, 16)), f'wide for k in {wk}')
  six = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'six_shapes.json')))['tableaux']
  for key, T in six.items():
    lam = [int(x) for x in key.split(',')]
    ok = (len(T) == len(lam)
          and all(sorted(row) == list(range(1, L + 1)) for row, L in zip(T, lam))
          and all(len({row[c] for row in T if len(row) > c}) == sum(1 for row in T if len(row) > c)
                  for c in range(lam[0]))
          and wide(lam))
    record(f'explicit Latin tableau of the wide shape {tuple(lam)}', ok)
  base = cache[6]
  bad = sum(not invariants(T, 6) for T in base)
  record('base case: all tableaux of lambda_6 satisfy I1-I5', bad == 0, f'{len(base)} tableaux, {bad} violations')
  for k in range(6, KINV + 1):
    bad = sum(not invariants(T, k) for T in cache[k])
    record(f'sanity: all tableaux of lambda_{k} satisfy I1-I5', bad == 0, f'{len(cache[k])} tableaux')
    if k + 1 <= KINV + 1 and k >= 6:
      ext = {extensions(T, k + 1) for T in cache[k]}
      record(f'sanity: every tableau of lambda_{k} has exactly 4 extensions to lambda_{k + 1}', ext == {4}, f'values {sorted(ext)}')
  ok = all(r['ok'] for r in RESULTS)
  out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.json')
  json.dump({'all_passed': ok, 'checks': RESULTS}, open(out, 'w'), indent=1)
  print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
  sys.exit(0 if ok else 1)


if __name__ == '__main__':
  main()
