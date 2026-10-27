"""Independent finite-horizon integer certificates for the known length-three case."""

import itertools
import json
import math
from pathlib import Path


def appendCounts(a, horizon):
  b = (a[-1],) + a[:-1]
  targetOrders = [tuple(sorted(range(3), key=p.__getitem__)) for p in (a, b)]
  states = {(1, 2): 1, (2, 1): 1}
  first = [[0] * (horizon + 1) for _ in range(2)]
  totals = [0, 0]
  for n in range(2, horizon):
    nextStates = {}
    newHits = [0, 0]
    for (x, y), weight in states.items():
      for r in range(1, n + 2):
        values = (x + (x >= r), y + (y >= r), r)
        order = tuple(sorted(range(3), key=values.__getitem__))
        if order in targetOrders:
          newHits[targetOrders.index(order)] += weight
        else:
          key = values[1], r
          nextStates[key] = nextStates.get(key, 0) + weight
    for i in range(2):
      first[i][n + 1] = newHits[i]
      totals[i] = (n + 1) * totals[i] + newHits[i]
    states = nextStates
    if sum(totals) + sum(states.values()) != math.factorial(n + 1):
      raise RuntimeError('Prefix-permutation mass is not conserved')
  return first, totals, sum(states.values())


def prefixCounts(a, horizon):
  b = (a[-1],) + a[:-1]
  first = [[0] * (horizon + 1) for _ in range(2)]
  for label, target in enumerate((a, b)):
    states = {(target[0], target[1]): 1}
    first[label][3] = 1
    for n in range(4, horizon + 1):
      nextStates = {}
      for i in range(1, n + 1):
        for j in range(1, n + 1):
          if i == j:
            continue
          suffixFirst = j - (j > i)
          count = 0
          for ell in range(1, n):
            if ell == suffixFirst:
              continue
            z = ell + (ell >= i)
            pattern = (1 + (i > j) + (i > z),
                       1 + (j > i) + (j > z),
                       1 + (z > i) + (z > j))
            if pattern != a and pattern != b:
              count += states.get((suffixFirst, ell), 0)
          if count:
            nextStates[i, j] = count
      states = nextStates
      first[label][n] = sum(states.values())
  factorial = math.factorial(horizon)
  totals = [sum(first[i][n] * (factorial // math.factorial(n))
                for n in range(3, horizon + 1)) for i in range(2)]
  return first, totals, factorial - sum(totals)


def main():
  horizon = 18
  result = {'horizon': horizon, 'cases': []}
  for a in itertools.permutations((1, 2, 3)):
    if a > tuple(4 - x for x in a):
      continue
    left = appendCounts(a, horizon)
    right = prefixCounts(a, horizon)
    if left != right:
      raise RuntimeError(f'Independent recurrence mismatch: {a}')
    _, wins, unresolved = left
    factorial = math.factorial(horizon)
    if 2 * (wins[0] + unresolved) >= factorial:
      raise RuntimeError(f'Length-three interval does not certify: {a}')
    if 100 * (wins[0] + unresolved) >= 47 * factorial:
      raise RuntimeError(f'Length-three displayed bound fails: {a}')
    result['cases'].append({'pattern': list(a), 'winsA': wins[0], 'winsB': wins[1],
                            'unresolved': unresolved, 'factorial': factorial})
    print(f'k=3, pattern={a}: A={wins[0]}, B={wins[1]}, R={unresolved}, denominator={factorial}, PASS', flush=True)
  path = Path(__file__).with_name('length-three.json')
  if json.loads(path.read_text()) != result:
    raise RuntimeError('Saved length-three certificate differs')
  print('Length three: both independent integer recurrences MATCH; all three complement representatives PASS', flush=True)


if __name__ == '__main__':
  main()
