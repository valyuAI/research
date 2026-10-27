"""Compare direct finite permutations with both length-three recurrences."""

import itertools
import json
import math
import sys
from pathlib import Path

from check_length_three import appendCounts, prefixCounts


def main():
  rows = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines()]
  expected = {(h, a) for h in (8, 9, 10) for a in itertools.permutations((1, 2, 3))}
  actual = {(row['horizon'], tuple(row['pattern'])) for row in rows}
  if len(rows) != len(actual) or actual != expected:
    raise RuntimeError('Incomplete direct oracle coverage')
  for row in rows:
    a, horizon = tuple(row['pattern']), row['horizon']
    left = appendCounts(a, horizon)
    right = prefixCounts(a, horizon)
    if left != right:
      raise RuntimeError('Recurrence mismatch')
    first, wins, unresolved = left
    if wins != [row['winsA'], row['winsB']] or unresolved != row['unresolved']:
      raise RuntimeError(f'Direct horizon-count mismatch: {a}, H={horizon}')
    for label in range(2):
      expectedByEnd = [first[label][n] * (math.factorial(horizon) // math.factorial(n))
                       for n in range(horizon + 1)]
      if row['byEnd'][label] != expectedByEnd:
        raise RuntimeError(f'Direct first-hit-time mismatch: {a}, H={horizon}')
    print(f'Direct k=3 H={horizon}, pattern={a}: both recurrences MATCH', flush=True)
  print('All 18 direct horizon/race comparisons PASS', flush=True)


if __name__ == '__main__':
  main()
