"""Direct permutation controls for the cluster sign conventions."""

import itertools
import json
import math
from pathlib import Path


def main():
  base = Path(__file__).resolve().parent
  data = json.loads((base / 'certificates.json').read_text())
  a, b = (2, 3, 4, 1), (1, 2, 3, 4)
  row = next(row for row in data['cases']['4'] if tuple(row['pattern']) == a)
  cs = [[0] * 4 + c for c in row['coefficients']]
  first = [[0] * 10 for _ in range(2)]
  for n in range(1, 10):
    for i in range(2):
      first[i][n] = (-cs[i][n] + n * first[i][n - 1]
                     + sum(math.comb(n, j) * (cs[0][j] + cs[1][j]) * first[i][n - j]
                           for j in range(1, n + 1)))
  for n in range(4, 10):
    actual = [0, 0]
    for index, p in enumerate(itertools.permutations(range(n))):
      if n == 9 and index % 50000 == 0:
        print(f'Direct permutations n=9: {index}/362880 examined', flush=True)
      for start in range(n - 3):
        block = p[start:start + 4]
        pattern = tuple(1 + sum(y < x for y in block) for x in block)
        if pattern == a or pattern == b:
          if start == n - 4:
            actual[0 if pattern == a else 1] += 1
          break
    expected = [first[i][n] for i in range(2)]
    if actual != expected:
      raise RuntimeError(f'First-hit mismatch at n={n}: {actual} != {expected}')
    print(f'Direct permutations n={n}: {actual}, MATCH', flush=True)

  for k in range(3, 9):
    for mask in range(1 << 13):
      starts = [0] + [i + 1 for i in range(13) if mask & (1 << i)]
      values = [-1]
      previous = {-1: 0}
      lastSign = -1
      for j in range(1, len(starts)):
        value = -sum(values[i] for i in range(j) if starts[j] - starts[i] < k)
        if value not in (-1, 0, 1):
          raise RuntimeError('Pointwise bound failed')
        values.append(value)
        if value:
          if value == lastSign or (value in previous and starts[j] - previous[value] < k):
            raise RuntimeError('Nonzero separation failed')
          previous[value] = starts[j]
          lastSign = value
    print(f'Pointwise recurrence k={k}: all 8192 start sets through span 13, PASS', flush=True)


if __name__ == '__main__':
  main()
