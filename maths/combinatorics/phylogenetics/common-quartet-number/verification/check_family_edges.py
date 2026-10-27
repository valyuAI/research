"""Count common quartets by edge bipartitions, independently of path distances.

Only Newick parsing is shared with check_family.py. Connectivity, tree structure
and every quartet split are checked again here without its distance algorithm.
"""
import argparse
from itertools import combinations
from pathlib import Path

from check_family import parse


def need(condition, message):
  if not condition:
    raise ValueError(message)


def quartet_table(line):
  adjacency, leaves = parse(line)
  n = len(leaves)
  need(sorted(leaves) == list(range(1, n + 1)), 'leaves must be 1..n')
  need(len(adjacency) == 2 * n - 2, 'binary-tree vertex count')
  for vertex, neighbours in adjacency.items():
    need(len(neighbours) == (1 if vertex[0] == 'l' else 3), 'binary degrees')
    need(len(set(neighbours)) == len(neighbours), 'duplicate adjacency')
    need(all(vertex in adjacency[other] for other in neighbours), 'reciprocal edges')
  edges = [(a, b) for a, neighbours in adjacency.items() for b in neighbours if a < b]
  need(len(edges) == len(adjacency) - 1, 'tree edge count')
  seen = {next(iter(adjacency))}
  stack = list(seen)
  while stack:
    for vertex in adjacency[stack.pop()]:
      if vertex not in seen:
        seen.add(vertex)
        stack.append(vertex)
  need(len(seen) == len(adjacency), 'connected tree')
  sides = []
  full = (1 << n) - 1
  for a, b in edges:
    seen, stack, mask = {a, b}, [b], 0
    while stack:
      vertex = stack.pop()
      if vertex[0] == 'l':
        mask |= 1 << (vertex[1] - 1)
      for other in adjacency[vertex]:
        if other not in seen:
          seen.add(other)
          stack.append(other)
    if 2 <= mask.bit_count() <= n - 2:
      sides.append(mask)
  table = {}
  for quartet in combinations(range(1, n + 1), 4):
    bits = [1 << (leaf - 1) for leaf in quartet]
    mask = sum(bits)
    splits = {min(side & mask, (full ^ side) & mask) for side in sides
      if (side & mask).bit_count() == 2}
    need(len(splits) == 1, 'exactly one displayed split per quartet')
    table[quartet] = splits.pop()
  return n, table


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('paths', nargs='+')
  args = parser.parse_args()
  for path in args.paths:
    trees = [quartet_table(line) for line in Path(path).read_text().splitlines() if line.strip()]
    n = trees[0][0]
    need(all(size == n for size, _ in trees), 'same leaf set')
    common = sum(len({table[q] for _, table in trees}) == 1 for q in trees[0][1])
    print(f'{path}: {len(trees)} trees, {n} leaves, {len(trees[0][1])} four-sets, {common} common (edge splits)', flush=True)
    need(common == 0, 'family must have no common quartet')


if __name__ == '__main__':
  main()
