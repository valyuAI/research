"""Verify compact leading-power certificates against the original cubics.

This checker uses only Python's standard library. Certificate generation may
use computer algebra or linear algebra; no generator assertion is trusted.
"""

import argparse
import hashlib
import json
import re
import time
from pathlib import Path

from verify_membership import exponents, leading_key, multiply_add, parse_polynomial, require

ROOT = Path(__file__).resolve().parent
GROUPS = {3: [1, 2, 3, 4], 4: [5, 6], 5: [7, 8], 6: [9, 10], 7: [11]}


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--through-degree", type=int, choices=range(3, 8), default=7)
  args = parser.parse_args()
  started = time.monotonic()
  source_path = ROOT / "gcd4_slice_n11.sing"
  target_path = ROOT / "gcd4_slice_n11_targets.txt"
  source = source_path.read_text().split("ideal J=", 1)[1].split(";", 1)[0]
  generators = [parse_polynomial(item, 11) for item in source.split(",")]
  require(len(generators) == 28, "Expected 28 original cubics")
  targets = {}
  for line in target_path.read_text().splitlines():
    match = re.fullmatch(r"target\[(\d+)\]=(.*)", line)
    require(match is not None, "Malformed target line")
    index = int(match[1])
    require(index not in targets, "Duplicate target")
    targets[index] = parse_polynomial(match[2], 11)
  require(set(targets) == set(range(1, 12)), "Expected all eleven candidate targets")
  verified = []
  files = [source_path, target_path]
  for degree, indices in GROUPS.items():
    if degree > args.through_degree:
      break
    path = ROOT / f"macaulay_degree{degree}_membership.txt"
    files.append(path)
    coefficients = {}
    for line in path.read_text().splitlines():
      match = re.fullmatch(r"coefficient\[(\d+),(\d+)\]=(.*)", line)
      require(match is not None, "Malformed coefficient line")
      row, column = int(match[1]), int(match[2])
      require(1 <= row <= 28 and 1 <= column <= len(indices), "Coefficient index out of range")
      require((row, column) not in coefficients, "Duplicate coefficient")
      coefficient = parse_polynomial(match[3], 11)
      require(all(sum(exponents(key, 11)) == degree - 3 for key in coefficient), "Incorrect coefficient degree")
      coefficients[row, column] = coefficient
    for column, index in enumerate(indices, 1):
      actual = {}
      for row, generator in enumerate(generators, 1):
        multiply_add(actual, generator, coefficients.get((row, column), {}))
      actual = {key: value for key, value in actual.items() if value}
      require(actual == targets[index], f"Identity {index} failed")
      leading = exponents(leading_key(targets[index], 11), 11)
      require(leading[index - 1] == degree and sum(leading) == degree, "Wrong pure leading power")
      verified.append({"variable": index - 1, "power": degree})
      print(f"Direct identity {index}/11 and leading power t{index-1}^{degree}: PASS", flush=True)
  complete = args.through_degree == 7
  require(not complete or len(verified) == 11, "Incomplete dimension certificate")
  result = {
    "prime": 32003,
    "original_generators": 28,
    "identities_verified": len(verified),
    "pure_leading_powers": verified,
    "dimension_zero_certified": complete,
    "seconds": round(time.monotonic() - started, 4),
    "method": "Exact standard-library modular polynomial products; no CAS, numeric tolerance, or basis assertion",
    "sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
  }
  suffix = "" if complete else f"_through_{args.through_degree}"
  (ROOT / f"direct_power_audit{suffix}.json").write_text(json.dumps(result, indent=2) + "\n")
  print("PASS: zero-dimensionality certificate" if complete else "PASS: partial identities only; no dimension conclusion yet", flush=True)


if __name__ == "__main__":
  main()
