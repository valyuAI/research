"""Exact local tangent computation at the rank-six highest-weight point."""

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
  source = (ROOT / "collision_incidence_matrix.sing").read_text()
  expression = source.split("matrix B[15][21]=", 1)[1].split(";", 1)[0]
  matrix = sp.Matrix(15, 21, [sp.sympify(value.replace("^", "**")) for value in expression.split(",")])
  parameters = sp.symbols("h0:15")
  borel = json.loads((ROOT / "minimum_rank_borel_checks.json").read_text())
  point = [sp.sympify(v) for v in borel["highest_weight_line_checks"][0]["H_coordinates"]]
  base = matrix.subs(dict(zip(parameters, point)))
  assert base.rank() == 6
  left = sp.Matrix.hstack(*base.T.nullspace())
  right = sp.Matrix.hstack(*base.nullspace())
  print(f"Normal block dimensions: {left.cols} x {right.cols}", flush=True)
  normal = (left.T * matrix * right).applyfunc(sp.expand)
  linear_map = sp.Matrix(list(normal)).jacobian(parameters)
  normal_rank = linear_map.rank()
  kernel = linear_map.nullspace()
  print(f"Normal linear-map rank={normal_rank}, affine tangent dimension={len(kernel)}", flush=True)
  result = {
    "field": "Q(i)",
    "basepoint_rank": 6,
    "left_nullspace_dimension": left.cols,
    "right_nullspace_dimension": right.cols,
    "normal_linear_map_rank": normal_rank,
    "affine_rank6_locus_tangent_dimension_at_highest_weight_point": len(kernel),
    "normal_linear_map_kernel_basis": [list(map(str, v)) for v in kernel],
    "normal_block_entries": [[str(v) for v in row] for row in normal.tolist()],
    "left_nullspace_basis": [[str(v) for v in row] for row in left.tolist()],
    "right_nullspace_basis": [[str(v) for v in row] for row in right.tolist()],
    "implication": "Every projective rank<=6 component contains this unique eligible B-fixed point; hence its affine dimension is at most the displayed tangent dimension.",
  }
  (ROOT / "rank6_tangent_checks.json").write_text(json.dumps(result, indent=2) + "\n")
  print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}, indent=2), flush=True)


if __name__ == "__main__":
  main()
