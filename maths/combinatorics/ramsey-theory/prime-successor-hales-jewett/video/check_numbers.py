"""Reproduce every number quoted in the narration and on screen.

Run: python3 check_numbers.py   (pure Python, under a second)

1. The 3 by 3 board (p = 2): its 7 lines, the failed checkerboard, the repaired colouring.
2. The 3 by 3 by 3 cube: exhaustive search shows no draw exists (so HJ(3,2;2) = 3).
3. The 4 by 4 by 4 cube (p = 3): the rule gives 19 blue cells and a draw.
4. The 8^7 cube (p = 7): blue sums, number of blue cells, sum histogram, line count.
5. The example lines drawn on the number line.
"""

import itertools
import sys
from math import comb


def blue_rule(p, s):
  return s == 0 or (s % p == 1 and s > 1)


def lines(k, n):
  """Every variable word over {0..k-1, *} with at least one star, as a list of k points."""
  out = []
  for w in itertools.product(list(range(k)) + ['*'], repeat=n):
    if '*' in w:
      out.append([tuple(a if c == '*' else c for c in w) for a in range(k)])
  return out


def check(k, n, blue):
  red_lines = sum(1 for L in lines(k, n) if not any(x in blue for x in L))
  blue_pairs = sum(1 for L in lines(k, n) for a in range(k - 1) if L[a] in blue and L[a + 1] in blue)
  return red_lines, blue_pairs


# 1. Tic-tac-toe board, p = 2.
L32 = lines(3, 2)
print('3x3 board: number of lines =', len(L32))
pts = list(itertools.product(range(3), repeat=2))
checker = {x for x in pts if sum(x) % 2 == 1}
print('  checkerboard (odd sums) blue =', sorted(checker), '-> (red lines, blue pairs) =', check(3, 2, checker))
repaired = {x for x in pts if blue_rule(2, sum(x))}
print('  repaired rule blue =', sorted(repaired), '->', check(3, 2, repaired))
assert check(3, 2, repaired) == (0, 0)
anti = [(0, 2), (1, 1), (2, 0)]
assert anti not in L32, 'anti-diagonal must not be a combinatorial line'

# 2. 3x3x3: no draw (backtracking over cells; prune on a red line or a blue pair).
cells = list(itertools.product(range(3), repeat=3))
idx = {c: i for i, c in enumerate(cells)}
L333 = [[idx[x] for x in L] for L in lines(3, 3)]
pairs = [(L[a], L[a + 1]) for L in L333 for a in range(2)]
print('3x3x3 cube: lines =', len(L333), 'neighbour pairs =', len(pairs))
lines_by_cell = [[] for _ in cells]
for L in L333:
  for c in L:
    lines_by_cell[c].append(L)
pairs_by_cell = [[] for _ in cells]
for a, b in pairs:
  pairs_by_cell[a].append(b)
  pairs_by_cell[b].append(a)
col = [None] * len(cells)
found = []


def solve(i):
  if i == len(cells):
    found.append(list(col))
    return True
  for c in ('B', 'R'):
    col[i] = c
    ok = True
    if c == 'B':
      ok = all(col[j] != 'B' for j in pairs_by_cell[i])
    else:
      for L in lines_by_cell[i]:
        if all(col[j] == 'R' for j in L):
          ok = False
          break
    if ok and solve(i + 1):
      return True
  col[i] = None
  return False


print('  draw on 3x3x3 exists?', solve(0))
assert not found

# 3. 4x4x4, p = 3.
pts444 = list(itertools.product(range(4), repeat=3))
b444 = {x for x in pts444 if blue_rule(3, sum(x))}
by_sum = {s: sum(1 for x in b444 if sum(x) == s) for s in (0, 4, 7)}
print('4x4x4 cube (p=3): blue sums 0,4,7 counts', by_sum, 'total', len(b444), '->', check(4, 3, b444))
assert check(4, 3, b444) == (0, 0)

# 4. 8^7, p = 7.
p, k, n = 7, 8, 7
hist = [0] * (n * (k - 1) + 1)
for x in itertools.product(range(k), repeat=n - 1):
  s0 = sum(x)
  for last in range(k):
    hist[s0 + last] += 1
blue_sums = [s for s in range(len(hist)) if blue_rule(p, s)]
print('8^7 cube: points =', k ** n, 'lines =', (k + 1) ** n - k ** n)
print('  blue sums =', blue_sums)
print('  blue counts by sum =', {s: hist[s] for s in blue_sums}, 'total =', sum(hist[s] for s in blue_sums))
print('  sum-one points =', hist[1], ' 8x8 boards needed =', k ** n // 64)
print('  full histogram =', hist)
assert sum(hist[s] for s in blue_sums) == 299587

# 5. Number-line examples: (d, S) -> sums S + d a for a = 0..7, and which are blue.
for d, S in [(3, 5), (7, 0), (1, 1), (1, 0), (2, 3)]:
  sums = [S + d * a for a in range(k)]
  print(f'  line d={d} S={S}: sums {sums} blue at', [s for s in sums if blue_rule(p, s)])

# Clock: stepping by d on a p-hour clock.
for m, d in [(7, 3), (6, 2), (6, 3)]:
  print(f'  {m}-hour clock, step {d}:', [(d * a) % m for a in range(m)])
print('all checks passed')
sys.stdout.flush()
