"""Classify B-fixed lines in the rank-six normal quotient."""

import json
from pathlib import Path

import sympy as sp

from elasticity import build_coefficients

ROOT = Path(__file__).resolve().parent


def main():
  data = json.loads((ROOT / "rank6_tangent_checks.json").read_text())
  h = sp.symbols("h0:15")
  normal = sp.Matrix([[sp.sympify(v) for v in row] for row in data["normal_block_entries"]])
  normal_map = sp.Matrix(list(normal)).jacobian(h)
  pivots = normal_map.rref()[1]
  complement = sp.eye(15)[:, list(pivots)]
  kernel = sp.Matrix.hstack(*normal_map.nullspace())
  change = complement.row_join(kernel)
  change_inverse = change.inv()
  variables, gamma, p, _ = build_coefficients()
  trace_matrix = sp.Matrix(sp.Poly(sp.trace(gamma), *p).coeffs()).jacobian(variables)
  basis = sp.Matrix.hstack(*trace_matrix.nullspace())
  gamma_h = gamma.subs(dict(zip(variables, basis * sp.Matrix(h))), simultaneous=True)
  quartics = [p[0]**i * p[1]**j * p[2]**(4 - i - j)
              for i in range(4, -1, -1) for j in range(4 - i, -1, -1)]

  def coefficients(expression):
    polynomial = sp.Poly(sp.expand(expression), *p)
    return sp.Matrix([polynomial.coeff_monomial(q) for q in quartics])

  contraction = coefficients((sp.Matrix(p).T * gamma_h * sp.Matrix(p))[0]).jacobian(h)
  a = p[0] + sp.I * p[1]
  raising = sp.Matrix.hstack(*[
    coefficients(a * sp.diff(q, p[2]) - p[2] * (sp.diff(q, p[0]) + sp.I * sp.diff(q, p[1])))
    for q in quartics
  ])
  torus = sp.Matrix.hstack(*[
    coefficients(p[0] * sp.diff(q, p[1]) - p[1] * sp.diff(q, p[0]))
    for q in quartics
  ]) / sp.I
  raising = contraction.inv() * raising * contraction
  torus = contraction.inv() * torus * contraction
  assert (normal_map * raising * kernel).applyfunc(sp.simplify) == sp.zeros(135, 5)
  assert (normal_map * torus * kernel).applyfunc(sp.simplify) == sp.zeros(135, 5)
  raising_quotient = (change_inverse * raising * complement)[:10, :].applyfunc(sp.simplify)
  torus_quotient = (change_inverse * torus * complement)[:10, :].applyfunc(sp.simplify)
  records = []
  for weight in sorted(torus_quotient.eigenvals()):
    fixed = raising_quotient.col_join(torus_quotient - weight * sp.eye(10)).nullspace()
    if not fixed:
      continue
    entry = {"weight": str(weight), "eigenspace_dimension": len(fixed), "basis": [list(map(str, v)) for v in fixed]}
    if len(fixed) == 1:
      source = complement * fixed[0]
      rank = normal.subs(dict(zip(h, source))).rank()
      entry["normal_matrix_rank"] = rank
    else:
      entry["normal_matrix_rank"] = "family requires analysis"
    print(entry, flush=True)
    records.append(entry)
  quotient_variables = sp.symbols("z0:10")
  quotient_normal = normal.subs(dict(zip(h, complement * sp.Matrix(quotient_variables))), simultaneous=True)
  result = {
    "quotient_dimension": 10,
    "normal_kernel_dimension": 5,
    "quotient_basis_source_columns": list(pivots),
    "B_fixed_line_families": records,
    "quotient_normal_matrix": [[str(v) for v in row] for row in quotient_normal.tolist()],
    "raising_quotient": [[str(v) for v in row] for row in raising_quotient.tolist()],
    "torus_quotient": [[str(v) for v in row] for row in torus_quotient.tolist()],
  }
  (ROOT / "normal_borel_checks.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
  main()
