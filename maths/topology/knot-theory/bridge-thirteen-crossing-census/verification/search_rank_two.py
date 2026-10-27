"""Reproduce the bounded rank-two permutation census with NumPy.

The proof uses the saved positive certificates, not search completeness.
"""

import argparse
import ast
import csv
import json
import time
from itertools import combinations, permutations
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent


def canonical_cycle(values):
  values = tuple(values)
  offset = values.index(min(values))
  return values[offset:] + values[:offset]


def pairings(points):
  points = tuple(points)
  if not points:
    yield ()
    return
  for i in range(1, len(points)):
    for tail in pairings(points[1:i] + points[i + 1:]):
      yield ((points[0], points[i]),) + tail


def labels_on_support(kind, support):
  if kind == "C":
    return sorted({canonical_cycle(order) for order in permutations(support)})
  return sorted({tuple(sorted(tuple(sorted(pair)) for pair in matching))
                 for matching in pairings(support)})


def map_label(kind, label, mapping):
  if kind == "C":
    return canonical_cycle(mapping[x] for x in label)
  return tuple(sorted(tuple(sorted((mapping[a], mapping[b]))) for a, b in label))


def permutation(kind, label, degree):
  result = list(range(degree))
  if kind == "C":
    for i in range(3):
      result[label[i]] = label[(i + 1) % 3]
  else:
    for a, b in label:
      result[a], result[b] = b, a
  return tuple(result)


def connected(kind, labels, degree, forest_only=False):
  parent = list(range(degree))

  def root(x):
    while parent[x] != x:
      parent[x] = parent[parent[x]]
      x = parent[x]
    return x

  for label in labels:
    edges = list(zip(label, label[1:])) if kind == "C" else label
    for a, b in edges:
      ra, rb = root(a), root(b)
      if forest_only and ra == rb:
        return False
      parent[ra] = rb
  return forest_only or len({root(x) for x in range(degree)}) == 1


def seed_configurations(kind, degree, lookup):
  support_size = 3 if kind == "C" else 4
  first = (0, 1, 2) if kind == "C" else ((0, 1), (2, 3))
  result = set()

  def visit(chosen, used):
    depth = len(chosen)
    if depth == 4:
      if used == degree and connected(kind, chosen, degree):
        result.add(tuple(lookup[label] for label in chosen))
      return
    for fresh in range(min(support_size, degree - used) + 1):
      if used + fresh + support_size * (3 - depth) < degree:
        continue
      new_points = tuple(range(used, used + fresh))
      for old_points in combinations(range(used), support_size - fresh):
        for label in labels_on_support(kind, old_points + new_points):
          if label in chosen:
            continue
          if fresh:
            variants = []
            for order in permutations(new_points):
              relabel = {i: i for i in range(used + fresh)}
              relabel.update(zip(new_points, order))
              variants.append(map_label(kind, label, relabel))
            if label != min(variants):
              continue
          extended = chosen + [label]
          if kind == "D" and degree == 9 and not connected(kind, extended, used + fresh, forest_only=True):
            continue
          visit(extended, used + fresh)

  visit([first], support_size)
  return np.array(sorted(result), dtype=np.int16)


def wirtinger(pd):
  n = len(pd)
  parent = list(range(2 * n + 1))

  def root(x):
    while parent[x] != x:
      parent[x] = parent[parent[x]]
      x = parent[x]
    return x

  for a, b, c, d in pd:
    assert c == a % (2 * n) + 1
    parent[root(b)] = root(d)
  roots = sorted({root(x) for x in range(1, 2 * n + 1)})
  number = {r: i for i, r in enumerate(roots)}
  arcs = {x: number[root(x)] for x in range(1, 2 * n + 1)}
  assert len(roots) == n
  crossings = []
  for a, b, c, d in pd:
    forward = d == b % (2 * n) + 1
    assert forward or b == d % (2 * n) + 1
    crossings.append((arcs[a], arcs[c], arcs[b], forward))
  return crossings


def coloring_plan(crossings):
  for seeds in combinations(range(13), 4):
    known = set(seeds)
    moves = []
    while True:
      old = len(known)
      for before, after, over, forward in crossings:
        if over not in known:
          continue
        if before in known and after not in known:
          known.add(after)
          moves.append((after, before, over, forward))
        elif after in known and before not in known:
          known.add(before)
          moves.append((before, after, over, not forward))
      if len(known) == 13:
        return seeds, moves
      if len(known) == old:
        break
  raise AssertionError("No four-seed coloring")


def conjugation_tables(kind, labels, degree, lookup):
  actions = [permutation(kind, label, degree) for label in labels]
  inverses = [tuple(action.index(i) for i in range(degree)) for action in actions]
  plus = np.array([[lookup[map_label(kind, label, over)] for over in inverses]
                   for label in labels], dtype=np.int16)
  minus = np.array([[lookup[map_label(kind, label, over)] for over in actions]
                    for label in labels], dtype=np.int16)
  return plus, minus


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("kind", choices=("C", "D"), help="C: 3-cycle; D: double transposition")
  parser.add_argument("degree", type=int, choices=(8, 9))
  parser.add_argument("csv", type=Path, help="database_knotinfo 2026.10.5 complete CSV")
  parser.add_argument("output", type=Path)
  args = parser.parse_args()
  start = time.monotonic()
  support_size = 3 if args.kind == "C" else 4
  labels = sorted({label for support in combinations(range(args.degree), support_size)
                   for label in labels_on_support(args.kind, support)})
  lookup = {label: i for i, label in enumerate(labels)}
  plus, minus = conjugation_tables(args.kind, labels, args.degree, lookup)
  configs = seed_configurations(args.kind, args.degree, lookup)
  print(f"{args.kind}{args.degree}: {len(labels)} labels, {len(configs)} normalized seed configurations", flush=True)
  open_names = set(json.loads((ROOT / "open-list-v1.3.0.json").read_text()))
  assert len(open_names) == 293
  rows = []
  with args.csv.open() as stream:
    for row in csv.DictReader(stream, delimiter="|"):
      if row.get("name") in open_names:
        rows.append((row["name"], ast.literal_eval(row["pd_notation"])))
  assert len(rows) == 293
  hits = []
  for i, (name, pd) in enumerate(rows):
    crossings = wirtinger(pd)
    seeds, moves = coloring_plan(crossings)
    for offset in range(0, len(configs), 100_000):
      chunk = configs[offset:offset + 100_000]
      colors = np.zeros((len(chunk), 13), dtype=np.int16)
      colors[:, seeds] = chunk
      for target, source, over, forward in moves:
        operation = plus if forward else minus
        colors[:, target] = operation[colors[:, source], colors[:, over]]
      valid = np.ones(len(chunk), dtype=bool)
      for before, after, over, forward in crossings:
        operation = plus if forward else minus
        valid &= colors[:, after] == operation[colors[:, before], colors[:, over]]
        if not valid.any():
          break
      matches = np.flatnonzero(valid)
      if len(matches):
        hits.append(name)
        print("HIT", name, flush=True)
        break
    if i % 10 == 0 or i + 1 == len(rows):
      print(f"{i + 1}/293 scanned, {len(hits)} hits, {time.monotonic() - start:.1f}s", flush=True)
  output = {"kind": args.kind, "degree": args.degree, "normalized_configurations": len(configs),
            "hit_names": hits}
  args.output.write_text(json.dumps(output, indent=2) + "\n")
  print("finished", len(hits), flush=True)


if __name__ == "__main__":
  main()
