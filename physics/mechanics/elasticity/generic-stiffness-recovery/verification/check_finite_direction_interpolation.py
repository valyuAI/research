"""Verify exact interpolation at the proposed finite measurement directions."""

import json
from pathlib import Path

import sympy as sp


def main():
  checks = {}
  for degree in [2, 4]:
    nodes = [
      (a, b)
      for a in range(degree + 1)
      for b in range(degree + 1 - a)
    ]
    powers = list(nodes)
    matrix = sp.Matrix([
      [sp.Integer(x)**a * sp.Integer(y)**b for a, b in powers]
      for x, y in nodes
    ])
    determinant = matrix.det()
    if determinant == 0:
      raise AssertionError(f"Degree-{degree} interpolation matrix is singular")
    checks[str(degree)] = {
      "nodes": nodes,
      "monomial_powers": powers,
      "determinant": str(determinant),
      "nonzero": True,
    }
    print(
      f"Degree {degree}: {len(nodes)} nodes, exact determinant {determinant}",
      flush=True,
    )
  output = Path(__file__).with_name("finite_direction_interpolation_checks.json")
  output.write_text(json.dumps(checks, indent=2) + "\n")


if __name__ == "__main__":
  main()
