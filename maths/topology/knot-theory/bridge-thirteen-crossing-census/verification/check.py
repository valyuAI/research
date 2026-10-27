"""Replay every bridge census certificate using only the standard library."""

import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent
IDENTITY = tuple(range(8))


def compose(left, right):
  return tuple(left[right[i]] for i in range(8))


def inverse(perm):
  return tuple(perm.index(i) for i in range(8))


def from_cycle(cycle):
  assert len(cycle) == 3 and len(set(cycle)) == 3
  assert all(isinstance(x, int) and 0 <= x < 8 for x in cycle)
  perm = list(range(8))
  for i in range(3):
    perm[cycle[i]] = cycle[(i + 1) % 3]
  return tuple(perm)


def from_matching(matching):
  assert len(matching) == 2 and all(len(pair) == 2 for pair in matching)
  points = [point for pair in matching for point in pair]
  assert len(set(points)) == 4
  assert all(type(x) is int and 0 <= x < 8 for x in points)
  perm = list(range(8))
  for a, b in matching:
    perm[a], perm[b] = b, a
  return tuple(perm)


def edge_arcs(pd):
  """Arc i ends at the incoming underedge of PD crossing i."""
  n = len(pd)
  incoming = {crossing[0]: i for i, crossing in enumerate(pd)}
  assert len(incoming) == n
  arcs = {}
  for edge in range(1, 2 * n + 1):
    cursor = edge
    for _ in range(2 * n):
      if cursor in incoming:
        arcs[edge] = incoming[cursor]
        break
      cursor = cursor % (2 * n) + 1
    else:
      raise AssertionError("No undercrossing terminates edge")
  assert set(arcs.values()) == set(range(n))
  return arcs


def verify_one(entry, source):
  name = entry["name"]
  assert source["name"] == source["dt_name"] == name
  assert source["crossing_number"] == "13"
  assert source["bridge_index"] == "[3,4]"
  if entry["status"] == "prior_cable":
    assert name in {"13n_4587", "13n_4639"}
    assert "T(2,3)" in source["geometric_type"]
  else:
    assert entry["status"] == "new"
    assert source["geometric_type"] == "hyperbolic"
    assert source["montesinos_notation"] == ""
    assert source["pretzel_notation"] == ""
  pd = entry["pd"]
  assert len(pd) == 13
  assert all(len(crossing) == 4 for crossing in pd)
  assert Counter(edge for crossing in pd for edge in crossing) == Counter(
    {edge: 2 for edge in range(1, 27)}
  )
  assert json.loads(source["pd_notation"]) == pd
  arcs = edge_arcs(pd)
  if entry["permutation_type"] == "three_cycle":
    perms = [from_cycle(cycle) for cycle in entry["meridian_cycles"]]
    assert all(compose(perm, compose(perm, perm)) == IDENTITY for perm in perms)
  else:
    assert entry["permutation_type"] == "double_transposition"
    perms = [from_matching(matching) for matching in entry["meridian_matchings"]]
    assert all(compose(perm, perm) == IDENTITY for perm in perms)
  assert len(perms) == 13

  for a, b, c, d in pd:
    assert c == a % 26 + 1
    assert arcs[b] == arcs[d]
    over = perms[arcs[b]]
    before = perms[arcs[a]]
    after = perms[arcs[c]]
    if d == b % 26 + 1:
      expected = compose(inverse(over), compose(before, over))
    else:
      assert b == d % 26 + 1
      expected = compose(over, compose(before, inverse(over)))
    assert after == expected

  orbit = {0}
  while True:
    expanded = orbit | {perm[point] for perm in perms for point in orbit}
    if expanded == orbit:
      break
    orbit = expanded
  assert orbit == set(range(8))

  image = {IDENTITY}
  queue = deque([IDENTITY])
  while queue:
    element = queue.popleft()
    for generator in (perms[arc] for arc in entry["seed_arcs"]):
      product = compose(element, generator)
      if product not in image:
        image.add(product)
        queue.append(product)
  assert len(image) == 20160

  seeds = entry["seed_arcs"]
  assert len(seeds) == len(set(seeds)) == 4
  assert all(0 <= arc < 13 for arc in seeds)
  known = set(seeds)
  steps = entry["coloring_steps"]
  assert len(steps) == 9
  for crossing_index, new_arc in steps:
    assert 0 <= crossing_index < 13
    a, b, c, d = pd[crossing_index]
    assert arcs[b] in known
    before, after = arcs[a], arcs[c]
    assert before != after and new_arc in {before, after}
    assert new_arc not in known
    assert (before in known) != (after in known)
    known.add(new_arc)
  assert known == set(range(13))
  return name


def main():
  entries = json.loads((ROOT / "certificates.json").read_text())
  sources = json.loads((ROOT / "source-snapshot.json").read_text())
  open_names = json.loads((ROOT / "open-list-v1.3.0.json").read_text())
  remaining = json.loads((ROOT / "remaining-v1.3.0.json").read_text())
  search = json.loads((ROOT / "search-summary.json").read_text())
  assert entries["schema_version"] == 2
  assert entries["point_count"] == 8
  assert sources["database"] == "database_knotinfo"
  assert sources["version"] == "2026.10.5"
  assert len(entries["certificates"]) == len(sources["rows"]) == 27
  assert len(open_names) == len(set(open_names)) == 293
  assert len(remaining) == 268
  names = {entry["name"] for entry in entries["certificates"]}
  assert len(names) == 27 and names <= set(open_names)
  new_names = {entry["name"] for entry in entries["certificates"] if entry["status"] == "new"}
  assert len(new_names) == 25
  assert set(remaining) == set(open_names) - new_names
  assert {row["name"] for row in sources["rows"]} == names
  runs = {(run["kind"], run["degree"]): run for run in search["runs"]}
  assert set(runs) == {("C", 8), ("C", 9), ("D", 8), ("D", 9)}
  assert set(runs[("C", 8)]["hit_names"]) == {
    entry["name"] for entry in entries["certificates"] if entry["permutation_type"] == "three_cycle"
  }
  assert set(runs[("D", 8)]["hit_names"]) == {
    entry["name"] for entry in entries["certificates"] if entry["permutation_type"] == "double_transposition"
  }
  assert not runs[("C", 9)]["hit_names"] and not runs[("D", 9)]["hit_names"]
  by_name = {row["name"]: row for row in sources["rows"]}
  for entry in entries["certificates"]:
    name = verify_one(entry, by_name[entry["name"]])
    print(f"{name}: 13 relations, image A8, 4 coloring seeds", flush=True)
  print("All 27 bridge certificates passed; 25 entries removed from the pinned open list", flush=True)


if __name__ == "__main__":
  main()
