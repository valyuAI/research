"""Require arithmetic rejection of deliberately corrupted certificate inputs."""

import contextlib
import copy
import io
import json
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

import independent_verification as checker


def main():
  root = checker.ROOT
  data = json.loads((root / "modular-obstruction.json").read_text())
  with contextlib.redirect_stdout(io.StringIO()):
    vertices, normals, facets, edges, _ = checker.verify_geometry(data)
  results = []

  def reject(label, function, expected):
    try:
      with contextlib.redirect_stdout(io.StringIO()):
        function()
    except ValueError as error:
      checker.require(expected in str(error), "Unexpected rejection path: " + str(error))
      results.append({"mutation": label, "rejection": str(error)})
      print(f"PASS rejected {label}: {error}", flush=True)
    else:
      raise ValueError("Corrupted input accepted: " + label)

  bad = copy.deepcopy(data)
  bad["normals"][0][0][0] = str(Fraction(bad["normals"][0][0][0]) + 1)
  reject("facet normal", lambda: checker.verify_geometry(bad), "Supporting-facet")
  for key, expected in [
    ("kernel", "J*K"), ("range_dual", "left inverse"),
    ("left_nullspace", "Left-nullspace"), ("second_order_correction", "Second-order"),
    ("cubic_obstruction", "Cubic obstruction"),
  ]:
    bad = copy.deepcopy(data)
    bad[key][0][0] = (bad[key][0][0] + 1) % checker.P
    reject(key, lambda: checker.verify_modular(bad, vertices, normals, facets, edges), expected)

  certificate = json.loads((root / "pure-power-certificate.json").read_text())
  certificate["coefficients"][0][0][0] = (certificate["coefficients"][0][0][0] + 1) % checker.P
  original_read = Path.read_text

  def read_mutated(path, *args, **kwargs):
    if path == root / "pure-power-certificate.json":
      return json.dumps(certificate)
    return original_read(path, *args, **kwargs)

  with patch.object(Path, "read_text", read_mutated):
    reject("pure-power coefficient", lambda: checker.verify_identities(
      data["cubic_obstruction"], [tuple(m) for m in data["degree3_monomials"]]), "Pure-power identity")
  (root / "negative_verification_results.json").write_text(json.dumps(results, indent=2) + "\n")
  print("ALL SEVEN CORRUPTION CHECKS REJECTED", flush=True)


if __name__ == "__main__":
  main()
