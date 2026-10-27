"""Signed cluster enumeration with predecessor sets and minimal elements."""

import functools
import math


def linearExtensions(a, b, d):
  k = len(a)
  shared = sorted(range(k - d), key=lambda i: a[d + i])
  if [b[i] for i in shared] != sorted(b[:k - d]):
    return 0
  ar = [0] + [a[d + i] for i in shared] + [k + 1]
  br = [0] + [b[i] for i in shared] + [k + 1]
  result = 1
  for i in range(len(ar) - 1):
    x = ar[i + 1] - ar[i] - 1
    y = br[i + 1] - br[i] - 1
    result *= math.comb(x + y, x)
  return result



def addChain(pred, pattern, start):
  n = start + len(pattern)
  out = list(pred) + [0] * (n - len(pred))
  order = sorted(range(len(pattern)), key=pattern.__getitem__)
  for i, j in zip(order, order[1:]):
    u, v = start + i, start + j
    if out[u] & (1 << v):
      return None
    added = out[u] | (1 << u)
    for w in range(n):
      if w == v or out[w] & (1 << v):
        out[w] |= added
  return tuple(out)


def countExtensions(pred):
  full = (1 << len(pred)) - 1

  @functools.lru_cache(maxsize=None)
  def rec(placed):
    if placed == full:
      return 1
    remaining = full ^ placed
    total = 0
    while remaining:
      bit = remaining & -remaining
      i = bit.bit_length() - 1
      if pred[i] & ~placed == 0:
        total += rec(placed | bit)
      remaining ^= bit
    return total

  return rec(0)


def compute(a, cutoff, verbose=False):
  k = len(a)
  b = (a[-1],) + a[:-1]
  patterns = (a, b)
  compatible = {(i, j, d): linearExtensions(patterns[i], patterns[j], d) > 0
                for i in range(2) for j in range(2) for d in range(1, k)}
  states = [dict() for _ in range(cutoff + 1)]
  for i, p in enumerate(patterns):
    states[0][(addChain((), p, 0), i)] = -1
  coeffs = [[0] * (cutoff + 1) for _ in range(2)]
  nStates = 0
  for s in range(cutoff + 1):
    current = states[s]
    nStates += len(current)
    if verbose:
      print(f'pattern={a}, span={s}/{cutoff}, states={len(current)}, total={nStates}', flush=True)
    for (pred, last), weight in current.items():
      if not weight:
        continue
      coeffs[last][s] += weight * countExtensions(pred)
      for d in range(1, min(k, cutoff - s + 1)):
        for j, p in enumerate(patterns):
          if not compatible[last, j, d]:
            continue
          newPred = addChain(pred, p, s + d)
          if newPred is None:
            continue
          key = newPred, j
          dest = states[s + d]
          dest[key] = dest.get(key, 0) - weight
    states[s] = {}
  return coeffs, nStates

