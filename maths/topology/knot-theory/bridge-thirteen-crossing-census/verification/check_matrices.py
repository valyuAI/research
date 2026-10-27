"""Independent binary-matrix audit of every bridge census certificate."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UNIT = [1 << i for i in range(8)]


def product(left, right):
  return [_row_product(row, right) for row in left]


def _row_product(row, matrix):
  value = 0
  for j in range(8):
    if (row >> j) & 1:
      value ^= matrix[j]
  return value


def rank(rows):
  pivots = {}
  for initial in rows:
    row = initial
    while row:
      pivot = row.bit_length() - 1
      if pivot not in pivots:
        pivots[pivot] = row
        break
      row ^= pivots[pivot]
  return len(pivots)


def matrix(entry, label):
  action = list(range(8))
  if entry["permutation_type"] == "three_cycle":
    for j in range(3):
      action[label[j]] = label[(j + 1) % 3]
  else:
    assert entry["permutation_type"] == "double_transposition"
    for a, b in label:
      action[a], action[b] = b, a
  rows = [0] * 8
  for col, image in enumerate(action):
    rows[image] = 1 << col
  return rows


def arc_indices(pd):
  parent = list(range(27))

  def root(x):
    while parent[x] != x:
      parent[x] = parent[parent[x]]
      x = parent[x]
    return x

  for _, b, _, d in pd:
    parent[root(b)] = root(d)
  incoming_roots = {root(crossing[0]): i for i, crossing in enumerate(pd)}
  assert len(incoming_roots) == 13
  result = {edge: incoming_roots[root(edge)] for edge in range(1, 27)}
  assert set(result.values()) == set(range(13))
  return result


def check(entry):
  pd = entry["pd"]
  arcs = arc_indices(pd)
  if entry["permutation_type"] == "three_cycle":
    labels = entry["meridian_cycles"]
  else:
    assert entry["permutation_type"] == "double_transposition"
    labels = entry["meridian_matchings"]
  matrices = [matrix(entry, label) for label in labels]
  assert len(matrices) == 13
  for action in matrices:
    assert rank([action[i] ^ UNIT[i] for i in range(8)]) == 2
    if entry["permutation_type"] == "three_cycle":
      assert product(action, product(action, action)) == UNIT
    else:
      assert product(action, action) == UNIT
  for a, b, c, d in pd:
    before = matrices[arcs[a]]
    after = matrices[arcs[c]]
    over = matrices[arcs[b]]
    assert over == matrices[arcs[d]]
    if d == b % 26 + 1:
      assert product(over, after) == product(before, over)
    else:
      assert b == d % 26 + 1
      assert product(after, over) == product(over, before)
  stack = [action[i] ^ UNIT[i] for action in matrices for i in range(8)]
  assert rank(stack) == 7
  colored = set(entry["seed_arcs"])
  assert len(colored) == 4
  assert len(entry["coloring_steps"]) == 9
  for crossing_index, new_arc in entry["coloring_steps"]:
    a, b, c, _ = pd[crossing_index]
    under = {arcs[a], arcs[c]}
    assert len(under) == 2
    assert new_arc in under - colored
    assert arcs[b] in colored
    assert (under - {new_arc}) <= colored
    colored.add(new_arc)
  assert colored == set(range(13))
  print(f"{entry['name']}: matrix ranks 2 and 7; 13 relations; 4 coloring seeds", flush=True)


def main():
  entries = json.loads((ROOT / "certificates.json").read_text())["certificates"]
  assert len(entries) == 27
  for entry in entries:
    check(entry)
  print("All 27 independent matrix checks passed", flush=True)


if __name__ == "__main__":
  main()
