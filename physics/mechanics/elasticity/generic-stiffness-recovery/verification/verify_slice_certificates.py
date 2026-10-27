"""Verify the finite-field projective-slice certificates without Singular.

Checks every Bezout coefficient and reconstructs each saved minor on an
unisolvent simplex grid, using the known determinant degree bound.
"""

import itertools
import json
import re
from pathlib import Path

import sympy as sp

from certify_rank14_pencil import determinant

ROOT = Path(__file__).resolve().parent
PRIME = 32003


def polynomial(expression, variables):
  return {key: int(value) % PRIME for key, value in sp.Poly(
    sp.sympify(expression.replace("^", "**")), *variables, modulus=PRIME
  ).as_dict().items() if value}


def product_add(target, first, second):
  for left, a in first.items():
    for right, b in second.items():
      key = tuple(x + y for x, y in zip(left, right))
      target[key] = (target.get(key, 0) + a * b) % PRIME


def evaluate(terms, point, degree):
  powers = [[pow(value, exponent, PRIME) for exponent in range(degree + 1)] for value in point]
  total = 0
  for monomial, coefficient in terms.items():
    value = coefficient
    for i, exponent in enumerate(monomial):
      value = value * powers[i][exponent] % PRIME
    total = (total + value) % PRIME
  return total


def main():
  source = (ROOT / "collision_incidence_matrix.sing").read_text()
  expression = source.split("matrix B[15][21]=", 1)[1].split(";", 1)[0]
  matrix = sp.Matrix(15, 21, [sp.sympify(value.replace("^", "**")) for value in expression.split(",")])
  h = sp.symbols("h0:15")
  audit = []
  for rank in (13, 12):
    slug = f"rank_slice_r{rank}"
    record = json.loads((ROOT / (slug + "_input.json")).read_text())
    axes = record["nested_axes_in_H_basis"]
    assert sp.Matrix(axes).rank() == len(axes)
    dimension = len(axes) - 1
    variables = sp.symbols(f"x0:{dimension}")
    minors, coefficients = {}, {}
    for line in (ROOT / (slug + "_bezout_complete.txt")).read_text().splitlines():
      match = re.fullmatch(r"(minor|coefficient)\[(\d+)\]=(.*)", line)
      if match:
        kind, index, expression = match.groups()
        (minors if kind == "minor" else coefficients)[int(index) - 1] = polynomial(expression, variables)
    assert set(minors) == set(coefficients) == set(range(len(record["minors"])))
    identity = {}
    for index in sorted(minors):
      product_add(identity, minors[index], coefficients[index])
      print(f"r{rank}: Bezout product {index + 1}/{len(minors)}", flush=True)
    identity = {key: value for key, value in identity.items() if value}
    assert identity == {(0,) * dimension: 1}
    evaluated_axes = [
      [[int(value) for value in row] for row in matrix.subs(dict(zip(h, axis))).tolist()]
      for axis in axes
    ]
    degree = rank + 1
    assert all(sum(key) <= degree for terms in minors.values() for key in terms)
    grid = [point for point in itertools.product(range(degree + 1), repeat=dimension) if sum(point) <= degree]
    for count, point in enumerate(grid, 1):
      numeric = [[
        (evaluated_axes[-1][i][j] + sum(value * axis[i][j] for value, axis in zip(point, evaluated_axes[:-1]))) % PRIME
        for j in range(21)
      ] for i in range(15)]
      for index, selection in enumerate(record["minors"]):
        actual = determinant([[numeric[i][j] for j in selection["columns_zero_based"]]
                              for i in selection["rows_zero_based"]])
        assert actual == evaluate(minors[index], point, degree)
      if count % 100 == 0 or count == len(grid):
        print(f"r{rank}: determinant grid {count}/{len(grid)}", flush=True)
    audit.append({
      "rank_threshold": rank,
      "slice_vector_rank": len(axes),
      "prime": PRIME,
      "minors": len(minors),
      "bezout_identity_verified": True,
      "determinant_degree_bound": degree,
      "unisolvent_grid_points": len(grid),
      "all_saved_minors_identical_to_original_determinants": True,
      "software": "Python integer arithmetic and SymPy parsing; no Singular call",
    })
  (ROOT / "slice_certificates_independent_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
  print("Both complete projective-slice certificates independently verified.", flush=True)


if __name__ == "__main__":
  main()
