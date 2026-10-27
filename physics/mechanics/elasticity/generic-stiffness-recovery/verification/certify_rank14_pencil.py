"""Certify a complex-projective pencil avoids rank <= 14 by a modular resultant.

The integer matrix is fixed before reduction. A nonzero modular resultant of
two maximal minors proves their integer resultant is nonzero. This is an
exact characteristic-zero certificate, unlike an uncertified sampled rank.
"""

import json
import random
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
PRIME = 32003


def determinant(matrix):
  rows = [[int(value) % PRIME for value in row] for row in matrix]
  result = 1
  for column in range(len(rows)):
    pivot = next((j for j in range(column, len(rows)) if rows[j][column]), None)
    if pivot is None:
      return 0
    if pivot != column:
      rows[pivot], rows[column] = rows[column], rows[pivot]
      result = -result
    value = rows[column][column]
    result = result * value % PRIME
    inverse = pow(value, -1, PRIME)
    for j in range(column + 1, len(rows)):
      factor = rows[j][column] * inverse % PRIME
      for k in range(column + 1, len(rows)):
        rows[j][k] = (rows[j][k] - factor * rows[column][k]) % PRIME
  return result % PRIME


def interpolate(values):
  """Newton forward-difference interpolation, returning ascending coefficients."""
  polynomial = [0] * len(values)
  basis = [1]
  differences = list(values)
  factorial = 1
  for degree in range(len(values)):
    if degree:
      factorial = factorial * degree % PRIME
    scale = differences[0] * pow(factorial, -1, PRIME) % PRIME
    for i, coefficient in enumerate(basis):
      polynomial[i] = (polynomial[i] + scale * coefficient) % PRIME
    differences = [(b - a) % PRIME for a, b in zip(differences, differences[1:])]
    product = [0] * (len(basis) + 1)
    for i, coefficient in enumerate(basis):
      product[i] = (product[i] - degree * coefficient) % PRIME
      product[i + 1] = (product[i + 1] + coefficient) % PRIME
    basis = product
  return polynomial


def main():
  source = (ROOT / "collision_incidence_matrix.sing").read_text()
  expression = source.split("matrix B[15][21]=", 1)[1].split(";", 1)[0]
  entries = [sp.sympify(value.replace("^", "**")) for value in expression.split(",")]
  matrix = sp.Matrix(15, 21, entries)
  parameters = sp.symbols("h0:15")
  report = json.loads((ROOT / "collision_incidence_checks.json").read_text())
  h0 = [int(value) for value in report["H0_coordinates"]]
  rng = random.Random(20261017)
  h1 = [rng.randrange(-7, 8) for _ in parameters]
  first = matrix.subs(dict(zip(parameters, h0))).tolist()
  second = matrix.subs(dict(zip(parameters, h1))).tolist()
  variable = sp.Symbol("t")
  records = []
  for attempt in range(100):
    columns = sorted(rng.sample(range(21), 15))
    coefficients = interpolate([
      determinant([[first[i][j] + t * second[i][j] for j in columns] for i in range(15)])
      for t in range(16)
    ])
    if coefficients[0] == 0 or coefficients[-1] == 0:
      continue
    polynomial = sp.Poly.from_list(list(reversed(coefficients)), variable, modulus=PRIME)
    record = {"columns_zero_based": columns, "coefficients_ascending": coefficients}
    print(f"candidate minor {attempt + 1}: degree={polynomial.degree()}", flush=True)
    for previous, previous_polynomial in records:
      left, right, gcd = sp.gcdex(previous_polynomial, polynomial)
      if gcd.degree() == 0:
        assert left * previous_polynomial + right * polynomial == sp.Poly(1, variable, modulus=PRIME)
        certificate = {
          "prime": PRIME,
          "H0_coordinates": h0,
          "H1_coordinates": h1,
          "B0": [[int(v) for v in row] for row in first],
          "B1": [[int(v) for v in row] for row in second],
          "minors": [previous, record],
          "bezout_coefficients_descending": [
            [int(v) % PRIME for v in left.all_coeffs()],
            [int(v) % PRIME for v in right.all_coeffs()],
          ],
          "bezout_identity": "u(t) f(t) + v(t) g(t) = 1 over F_32003",
          "both_minors_degree": 15,
          "no_common_projective_root": True,
          "characteristic_zero_implication": "Integer homogeneous minor resultant is nonzero modulo 32003, hence nonzero over Q.",
          "rank_at_every_complex_projective_pencil_point": 15,
          "affine_rank_le_14_locus_dimension_upper_bound": 13,
        }
        (ROOT / "rank14_pencil_certificate.json").write_text(json.dumps(certificate, indent=2) + "\n")
        print("CERTIFIED: pencil has rank 15 at every complex projective point; rank<=14 locus has affine dimension <=13.", flush=True)
        return
    records.append((record, polynomial))
  raise RuntimeError("No certificate found in bounded candidate search.")


if __name__ == "__main__":
  main()
