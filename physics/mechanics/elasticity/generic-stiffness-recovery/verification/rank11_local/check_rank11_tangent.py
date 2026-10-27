"""Exact tangent certificate at the harmonic-degree-two rank-eleven point.

This checks a local determinantal tangent space over Q(i), not generic
injectivity of the elasticity coefficient map.
"""

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent


def strings(matrix):
  return [[str(x) for x in row] for row in matrix.tolist()]


def main():
  text = (SOURCE / "collision_incidence_matrix.sing").read_text()
  raw = text.split("matrix B[15][21]=", 1)[1].split(";", 1)[0]
  variables = sp.symbols("h0:15")
  matrix = sp.Matrix(15, 21, [sp.sympify(x.replace("^", "**")) for x in raw.split(",")])
  records = json.loads((SOURCE / "minimum_rank_borel_checks.json").read_text())
  record = next(x for x in records["highest_weight_line_checks"] if x["name"] == "harmonic_degree2_times_norm")
  point = sp.Matrix([sp.sympify(x) for x in record["H_coordinates"]])
  base = matrix.subs(dict(zip(variables, point)))
  print("Parsed 15-by-21 matrix and exact harmonic-degree-two point", flush=True)
  base_rank = base.rank()
  assert base_rank == 11
  left = sp.Matrix.hstack(*base.T.nullspace())
  right = sp.Matrix.hstack(*base.nullspace())
  assert left.shape == (15, 4) and right.shape == (21, 10)
  assert left.T * base == sp.zeros(4, 21)
  assert base * right == sp.zeros(15, 10)
  print("Exact base rank 11; left/right nullspace dimensions 4/10", flush=True)
  normal = (left.T * matrix * right).applyfunc(sp.expand)
  tangent_map = sp.Matrix(list(normal)).jacobian(variables)
  assert tangent_map.shape == (40, 15)
  rref, pivot_columns = tangent_map.rref()
  rank = len(pivot_columns)
  kernel = sp.Matrix.hstack(*tangent_map.nullspace())
  assert tangent_map * kernel == sp.zeros(40, kernel.cols)
  assert kernel.rank() == kernel.cols == 15-rank
  free_rows = [j for j in range(15) if j not in pivot_columns]
  kernel_independence_minor = kernel[free_rows, :]
  assert kernel_independence_minor == sp.eye(kernel.cols)
  assert tangent_map * point == sp.zeros(40, 1)
  print(f"Normal-map rank {rank}; affine tangent dimension {kernel.cols}", flush=True)
  pivot_rows = tangent_map[:, list(pivot_columns)].T.rref()[1]
  minor = tangent_map.extract(pivot_rows, pivot_columns)
  determinant = sp.factor(minor.det())
  assert determinant != 0
  # The highest-weight point has h9=1. Its radial direction is in the
  # cone tangent kernel but is excluded by the normalized projective chart.
  chart_index = 9
  assert point[chart_index] == 1
  chart_row = sp.zeros(1, 15)
  chart_row[0, chart_index] = 1
  chart_tangent_map = tangent_map.col_join(chart_row)
  chart_rank = chart_tangent_map.rank()
  assert chart_rank == rank+1
  chart_kernel = sp.Matrix.hstack(*chart_tangent_map.nullspace())
  assert chart_kernel.cols == 14-rank
  assert chart_tangent_map*chart_kernel == sp.zeros(41, chart_kernel.cols)
  print(f"Projective chart h9=1: tangent dimension {chart_kernel.cols}", flush=True)
  result = {
    "field": "Q(i), characteristic zero",
    "source_matrix_sha256": hashlib.sha256((SOURCE / "collision_incidence_matrix.sing").read_bytes()).hexdigest(),
    "point_source_sha256": hashlib.sha256((SOURCE / "minimum_rank_borel_checks.json").read_bytes()).hexdigest(),
    "point_name": record["name"],
    "point_coordinates": list(map(str, point)),
    "basepoint_rank": base_rank,
    "left_nullspace_basis": strings(left),
    "right_nullspace_basis": strings(right),
    "normal_block_entries": strings(normal),
    "normal_tangent_map": strings(tangent_map),
    "normal_map_rank": rank,
    "nonzero_minor_rows_zero_indexed": list(pivot_rows),
    "nonzero_minor_columns_zero_indexed": list(pivot_columns),
    "nonzero_minor_determinant": str(determinant),
    "affine_tangent_dimension": kernel.cols,
    "affine_tangent_kernel_columns": strings(kernel),
    "kernel_independence_minor_rows_zero_indexed": free_rows,
    "kernel_independence_minor_determinant": "1",
    "projective_chart": "h9=1",
    "projective_tangent_dimension": chart_kernel.cols,
    "projective_tangent_kernel_columns": strings(chart_kernel),
    "rank11_incidence_fiber_dimension": 10,
    "local_affine_incidence_dimension_bound_for_components_through_this_point": kernel.cols+10,
    "scope": "Local dimension bound for rank<=11 components through this harmonic-degree-two point. Components whose Borel-fixed limit is only the rank-six point require separate analysis. No generic-injectivity conclusion.",
  }
  (ROOT / "rank11_tangent_certificate.json").write_text(json.dumps(result, indent=2)+"\n")
  print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}, indent=2), flush=True)


if __name__ == "__main__":
  main()
