"""Exact checks of the full-rank part of the collision incidence.

This does not control the rank-drop strata and is not a proof of Conjecture E.
"""

import json
from pathlib import Path

import sympy as sp

from elasticity import build_coefficients

ROOT = Path(__file__).resolve().parent


def main():
  variables, gamma, p, _ = build_coefficients()
  trace_coefficients = sp.Poly(sp.trace(gamma), *p).coeffs()
  trace_matrix = sp.Matrix(trace_coefficients).jacobian(variables)
  nullspace = trace_matrix.nullspace()
  assert len(nullspace) == 15
  basis = sp.Matrix.hstack(*nullspace)
  h = sp.symbols("h0:15")
  substitution = dict(zip(variables, basis * sp.Matrix(h)))
  gamma_h = gamma.subs(substitution, simultaneous=True)
  expression = sp.expand(sp.trace(gamma * gamma_h))
  polynomial = sp.Poly(expression, *p)
  matrix = sp.Matrix(polynomial.coeffs()).jacobian(variables)
  assert matrix.shape == (15, 21)
  s = sum(pi**2 for pi in p)
  # The isotropic tensor lambda=4, mu=-1 has Gamma=3pp^T-|p|^2 I.
  h0 = {variable: 0 for variable in variables}
  for name in ("c11", "c22", "c33"):
    h0[sp.Symbol(name)] = 2
  for name in ("c12", "c13", "c23"):
    h0[sp.Symbol(name)] = 4
  for name in ("c44", "c55", "c66"):
    h0[sp.Symbol(name)] = -1
  gamma_h0 = gamma.subs(h0)
  assert gamma_h0 == 3 * sp.Matrix(p) * sp.Matrix(p).T - s * sp.eye(3)
  assert sp.trace(gamma_h0) == 0
  coordinates = basis.gauss_jordan_solve(sp.Matrix([h0[v] for v in variables]))[0]
  matrix_h0 = matrix.subs(dict(zip(h, coordinates)))
  rank_h0 = matrix_h0.rank()
  assert rank_h0 == 15
  # X=0 lies in every incidence fiber. Its determinant difference is 2 det Gamma_H.
  determinant_h0 = sp.factor(gamma_h0.det())
  assert sp.expand(determinant_h0 - 2 * s**3) == 0
  # Retain the exact symbolic matrix for bounded rank-stratum calculations.
  rows = [",".join(str(value).replace("**", "^") for value in row)
          for row in matrix.tolist()]
  singular = [
    "ring R=32003,(" + ",".join(map(str, h)) + "),dp;",
    "matrix B[15][21]=" + ",\n".join(rows) + ";",
    "// B is the quartic coefficient matrix of tr(Gamma_X Gamma_H).",
  ]
  (ROOT / "collision_incidence_matrix.sing").write_text("\n".join(singular) + "\n")
  report = {
    "trace_rank": trace_matrix.rank(),
    "trace_kernel_dimension": len(nullspace),
    "H_basis_columns": [[str(v) for v in column] for column in nullspace],
    "source_variables": list(map(str, variables)),
    "H0_coordinates": list(map(str, coordinates)),
    "H0_tensor": {str(k): v for k, v in h0.items()},
    "H0_incidence_rank": rank_h0,
    "H0_determinant": str(determinant_h0),
    "full_rank_incidence_dimension": 21,
    "full_rank_collision_dimension_upper_bound": 20,
    "scope": "This component verifies only the full-rank incidence. Separate rank-stratum certificates complete the paper argument.",
  }
  (ROOT / "collision_incidence_checks.json").write_text(json.dumps(report, indent=2) + "\n")
  print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
  main()
