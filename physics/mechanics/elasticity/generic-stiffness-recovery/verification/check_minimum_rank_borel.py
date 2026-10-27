"""Exact ingredients for a Borel fixed-point minimum-rank argument over C."""

import json
from pathlib import Path

import sympy as sp

from elasticity import build_coefficients

ROOT = Path(__file__).resolve().parent


def main():
  variables, gamma, p, _ = build_coefficients()
  trace_matrix = sp.Matrix(sp.Poly(sp.trace(gamma), *p).coeffs()).jacobian(variables)
  basis = sp.Matrix.hstack(*trace_matrix.nullspace())
  h = sp.symbols("h0:15")
  gamma_h = gamma.subs(dict(zip(variables, basis * sp.Matrix(h))), simultaneous=True)
  quartics = [p[0]**i * p[1]**j * p[2]**(4 - i - j)
              for i in range(4, -1, -1) for j in range(4 - i, -1, -1)]

  def coefficients(expression):
    poly = sp.Poly(sp.expand(expression), *p)
    return sp.Matrix([poly.coeff_monomial(monomial) for monomial in quartics])

  contraction = coefficients((sp.Matrix(p).T * gamma_h * sp.Matrix(p))[0]).jacobian(h)
  assert contraction.det() != 0
  incidence = coefficients(sp.trace(gamma * gamma_h)).jacobian(variables)
  a = p[0] + sp.I * p[1]
  s = sum(pi**2 for pi in p)
  highest = [a**4, s * a**2, s**2]
  records = []
  for name, quartic in zip(("harmonic_degree4", "harmonic_degree2_times_norm", "norm_squared"), highest):
    coordinates = contraction.inv() * coefficients(quartic)
    specialized = incidence.subs(dict(zip(h, coordinates)))
    rank = specialized.rank()
    print(f"{name}: rank={rank}", flush=True)
    records.append({"name": name, "H_coordinates": list(map(str, coordinates)), "incidence_rank": rank})
  raising = sp.Matrix.hstack(*[
    coefficients(a * sp.diff(q, p[2]) - p[2] * (sp.diff(q, p[0]) + sp.I * sp.diff(q, p[1])))
    for q in quartics
  ])
  highest_basis = sp.Matrix.hstack(*map(coefficients, highest))
  assert raising * highest_basis == sp.zeros(15, 3)
  assert highest_basis.rank() == 3
  assert raising.rank() == 12
  for weight, q in zip((4, 2, 0), highest):
    assert sp.expand(p[0] * sp.diff(q, p[1]) - p[1] * sp.diff(q, p[0]) - sp.I * weight * q) == 0
  result = {
    "field": "Q(i), embedded in C",
    "tracefree_contraction_determinant": str(contraction.det()),
    "raising_operator_rank": raising.rank(),
    "raising_operator_kernel_dimension": 3,
    "distinct_torus_weights": [4, 2, 0],
    "highest_weight_line_checks": records,
    "minimum_rank_lower_bound_using_Borel_fixed_point_theorem": min(r["incidence_rank"] for r in records),
    "scope": "Exact algebraic ingredients. Requires the stated SO3 equivariance and Borel fixed-point theorem; not a full injectivity proof.",
  }
  (ROOT / "minimum_rank_borel_checks.json").write_text(json.dumps(result, indent=2) + "\n")
  print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
  main()
