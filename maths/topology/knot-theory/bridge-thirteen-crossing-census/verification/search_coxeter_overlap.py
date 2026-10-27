"""Screen census diagrams for maximal-rank A4, D4 and H4 reflection actions."""

import ast
import csv
import hashlib
import json
import sys
import time
from itertools import combinations, permutations
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
ENTRIES = json.loads((ROOT / "certificates.json").read_text())["certificates"]
ZERO = (0, 0)
ONE = (1, 0)
PHI = (0, 1)


def add(a, b):
  return (a[0] + b[0], a[1] + b[1])


def neg(a):
  return (-a[0], -a[1])


def mul(a, b):
  return (a[0] * b[0] + a[1] * b[1],
          a[0] * b[1] + a[1] * b[0] + a[1] * b[1])


def unit(j):
  return tuple(ONE if i == j else ZERO for i in range(4))


def canonical(root):
  opposite = tuple(neg(x) for x in root)
  return min(root, opposite)


def gram(kind):
  matrix = [[(2, 0) if i == j else ZERO for j in range(4)] for i in range(4)]
  edges = [(0, 1, PHI if kind == "H4" else ONE), (1, 2, ONE), (2, 3, ONE)]
  if kind == "D4":
    edges = [(0, 1, ONE), (1, 2, ONE), (1, 3, ONE)]
  for i, j, value in edges:
    matrix[i][j] = neg(value)
    matrix[j][i] = neg(value)
  return matrix


def inner(x, y, matrix):
  result = ZERO
  for i in range(4):
    for j in range(4):
      result = add(result, mul(mul(x[i], matrix[i][j]), y[j]))
  return result


def reflect(x, root, matrix):
  coefficient = inner(x, root, matrix)
  return tuple(add(x[i], neg(mul(coefficient, root[i]))) for i in range(4))


def root_quandle(kind):
  matrix = gram(kind)
  simple = [unit(i) for i in range(4)]
  roots = {unit(0)}
  frontier = [unit(0)]
  while frontier:
    current = frontier.pop()
    for simple_root in simple:
      image = reflect(current, simple_root, matrix)
      if image not in roots:
        roots.add(image)
        frontier.append(image)
  expected = {"A4": 20, "D4": 24, "H4": 120}[kind]
  assert len(roots) == expected, (kind, len(roots))
  lines = sorted({canonical(root) for root in roots})
  lookup = {root: i for i, root in enumerate(lines)}
  assert len(lines) * 2 == expected
  assert all(inner(root, root, matrix) == (2, 0) for root in lines)
  table = np.array([[lookup[canonical(reflect(under, over, matrix))]
                     for under in lines] for over in lines], dtype=np.int16)
  for i in range(len(lines)):
    assert table[i, i] == i
    assert all(table[i, table[i, j]] == j for j in range(len(lines)))
  first = lookup[canonical(unit(0))]
  return lines, table, first


def determinant(rows):
  result = ZERO
  for order in permutations(range(4)):
    inversions = sum(order[i] > order[j] for i in range(4) for j in range(i + 1, 4))
    term = ONE
    for i in range(4):
      term = mul(term, rows[i][order[i]])
    result = add(result, neg(term) if inversions % 2 else term)
  return result


def arc_indices(pd):
  parent = list(range(27))

  def root(x):
    while parent[x] != x:
      parent[x] = parent[parent[x]]
      x = parent[x]
    return x

  for _, b, _, d in pd:
    parent[root(b)] = root(d)
  incoming = {root(a): i for i, (a, _, _, _) in enumerate(pd)}
  assert len(incoming) == 13
  return {edge: incoming[root(edge)] for edge in range(1, 27)}


def coloring(pd):
  arcs = arc_indices(pd)
  for seeds in combinations(range(13), 4):
    known = set(seeds)
    steps = []
    while True:
      old = len(known)
      for index, (a, b, c, _) in enumerate(pd):
        before, over, after = arcs[a], arcs[b], arcs[c]
        if over not in known:
          continue
        if before in known and after not in known:
          known.add(after)
          steps.append([index, after])
        elif after in known and before not in known:
          known.add(before)
          steps.append([index, before])
      if len(known) == 13:
        return list(seeds), steps
      if len(known) == old:
        break
  raise ValueError("Diagram has no four-seed coloring")


def find(entry, lines, table, first):
  pd = entry["pd"]
  arcs = arc_indices(pd)
  seeds = entry["seed_arcs"]
  q = len(lines)
  all_configs = np.indices((q, q, q), dtype=np.int16).reshape(3, -1).T
  colors = np.zeros((len(all_configs), 13), dtype=np.int16)
  colors[:, seeds[0]] = first
  colors[:, seeds[1:]] = all_configs
  for crossing_index, new_arc in entry["coloring_steps"]:
    a, b, c, _ = pd[crossing_index]
    before, after, over = arcs[a], arcs[c], arcs[b]
    other = before if new_arc == after else after
    assert new_arc in (before, after)
    colors[:, new_arc] = table[colors[:, over], colors[:, other]]
  valid = np.ones(len(colors), dtype=bool)
  for a, b, c, d in pd:
    before, after, over = arcs[a], arcs[c], arcs[b]
    assert over == arcs[d]
    valid &= colors[:, after] == table[colors[:, over], colors[:, before]]
    if not valid.any():
      return None, 0
  indices = np.flatnonzero(valid)
  for index in indices:
    labels = colors[index]
    if determinant([lines[int(labels[seed])] for seed in seeds]) != ZERO:
      return labels.tolist(), len(indices)
  return None, len(indices)


def main():
  if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 search_coxeter_overlap.py knotinfo_data_complete.csv")
  source = Path(sys.argv[1])
  expected_hash = json.loads((ROOT / "source-snapshot.json").read_text())["csv_sha256"]
  digest = hashlib.sha256()
  with source.open("rb") as stream:
    while block := stream.read(1024 * 1024):
      digest.update(block)
  assert digest.hexdigest() == expected_hash
  with source.open(newline="") as stream:
    row = next(row for row in csv.DictReader(stream, delimiter="|") if row["name"] == "13a_112")
  assert row["bridge_index"] == "4"
  pd = ast.literal_eval(row["pd_notation"])
  seeds, steps = coloring(pd)
  control = {"name": "13a_112", "pd": pd, "seed_arcs": seeds, "coloring_steps": steps}
  start = time.monotonic()
  output = {"scope": "Twenty-five new certificates; all four seed images up to conjugating the first reflection",
            "positive_control": "13a_112", "targets": {}}
  for kind in ("A4", "D4", "H4"):
    lines, table, first = root_quandle(kind)
    print(f"{kind}: {len(lines)} root lines, {len(lines) ** 3} seed triples", flush=True)
    witness, control_count = find(control, lines, table, first)
    assert witness is not None
    print(f"{kind}: positive control 13a_112 has a rank-four witness among {control_count} valid assignments", flush=True)
    hits = []
    for index, entry in enumerate(ENTRIES):
      if entry["status"] != "new":
        continue
      labels, count = find(entry, lines, table, first)
      if labels is not None:
        hits.append(entry["name"])
        print(f"HIT {kind} {entry['name']} assignments {count}", flush=True)
      print(f"{kind} {index + 1}/{len(ENTRIES)} {entry['name']} valid {count} elapsed {time.monotonic() - start:.1f}s", flush=True)
    output["targets"][kind] = {"root_lines": len(lines),
                                "seed_triples": len(lines) ** 3,
                                "positive_control_valid_assignments": control_count,
                                "hit_names": hits}
    print(f"{kind}: {len(hits)} rank-four reflection hits", flush=True)
  (ROOT / "coxeter-overlap-summary.json").write_text(json.dumps(output, indent=2) + "\n")
  print("finished", time.monotonic() - start, flush=True)


if __name__ == "__main__":
  main()
