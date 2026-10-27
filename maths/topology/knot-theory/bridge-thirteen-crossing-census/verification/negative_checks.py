"""Confirm the certificate checker rejects damaged relations and coloring moves."""

import copy
import json
from pathlib import Path

import check
import check_matrices


ROOT = Path(__file__).resolve().parent


def rejected(action):
  try:
    action()
  except (AssertionError, KeyError, ValueError):
    return
  raise AssertionError("A damaged certificate was accepted")


def main():
  entries = json.loads((ROOT / "certificates.json").read_text())["certificates"]
  sources = {row["name"]: row for row in json.loads((ROOT / "source-snapshot.json").read_text())["rows"]}
  original = next(entry for entry in entries if entry["name"] == "13n_4645")
  source = sources[original["name"]]

  wrong_cycle = copy.deepcopy(original)
  wrong_cycle["meridian_cycles"][0][1] = 6
  rejected(lambda: check.verify_one(wrong_cycle, source))
  rejected(lambda: check_matrices.check(wrong_cycle))

  wrong_step = copy.deepcopy(original)
  wrong_step["coloring_steps"][0][1] = 12
  rejected(lambda: check.verify_one(wrong_step, source))

  wrong_crossing = copy.deepcopy(original)
  wrong_crossing["pd"][0][1] = 5
  rejected(lambda: check.verify_one(wrong_crossing, source))
  rejected(lambda: check_matrices.check(wrong_crossing))

  double = next(entry for entry in entries if entry["name"] == "13a_373")
  double_source = sources[double["name"]]
  wrong_matching = copy.deepcopy(double)
  wrong_matching["meridian_matchings"][0][0][1] = 7
  rejected(lambda: check.verify_one(wrong_matching, double_source))
  rejected(lambda: check_matrices.check(wrong_matching))
  print("Damaged cycles, matchings, coloring moves and PD crossings were rejected", flush=True)


if __name__ == "__main__":
  main()
