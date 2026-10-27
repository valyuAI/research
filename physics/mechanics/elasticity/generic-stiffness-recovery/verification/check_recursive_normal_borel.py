"""One further exact normal-space reduction at the unique low-rank B-fixed line."""

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
  data = json.loads((ROOT / "normal_borel_checks.json").read_text())
  z = sp.symbols("z0:10")
  matrix = sp.Matrix([[sp.sympify(v) for v in row] for row in data["quotient_normal_matrix"]])
  raising = sp.Matrix([[sp.sympify(v) for v in row] for row in data["raising_quotient"]])
  torus = sp.Matrix([[sp.sympify(v) for v in row] for row in data["torus_quotient"]])
  fixed = next(item for item in data["B_fixed_line_families"] if item["weight"] == "2")
  point = sp.Matrix([sp.sympify(v) for v in fixed["basis"][0]])
  base = matrix.subs(dict(zip(z, point)))
  assert base.rank() == 2
  left = sp.Matrix.hstack(*base.T.nullspace())
  right = sp.Matrix.hstack(*base.nullspace())
  normal = (left.T * matrix * right).applyfunc(sp.expand)
  linear_map = sp.Matrix(list(normal)).jacobian(z)
  kernel = sp.Matrix.hstack(*linear_map.nullspace())
  pivots = linear_map.rref()[1]
  dimension = len(pivots)
  complement = sp.eye(10)[:, list(pivots)]
  change_inverse = complement.row_join(kernel).inv()
  assert (linear_map * raising * kernel).applyfunc(sp.simplify) == sp.zeros(left.cols * right.cols, kernel.cols)
  assert (linear_map * torus * kernel).applyfunc(sp.simplify) == sp.zeros(left.cols * right.cols, kernel.cols)
  next_raising = (change_inverse * raising * complement)[:dimension, :].applyfunc(sp.simplify)
  next_torus = (change_inverse * torus * complement)[:dimension, :].applyfunc(sp.simplify)
  print(f"Recursive normal dimensions={normal.shape}; kernel={kernel.cols}; quotient={dimension}", flush=True)
  w = sp.symbols(f"w0:{dimension}")
  next_normal = normal.subs(dict(zip(z, complement * sp.Matrix(w))), simultaneous=True)
  records = []
  for weight in sorted(next_torus.eigenvals()):
    vectors = next_raising.col_join(next_torus - weight * sp.eye(dimension)).nullspace()
    if not vectors:
      continue
    entry = {"weight": str(weight), "eigenspace_dimension": len(vectors), "basis": [list(map(str, v)) for v in vectors]}
    if len(vectors) == 1:
      entry["normal_matrix_rank"] = next_normal.subs(dict(zip(w, vectors[0]))).rank()
    print(entry, flush=True)
    records.append(entry)
  result = {
    "original_normal_quotient_dimension": 10,
    "base_rank": 2,
    "affine_tangent_kernel_dimension": kernel.cols,
    "next_quotient_dimension": dimension,
    "next_quotient_basis_indices": list(pivots),
    "B_fixed_line_families": records,
    "next_normal_matrix": [[str(v) for v in row] for row in next_normal.tolist()],
    "next_raising": [[str(v) for v in row] for row in next_raising.tolist()],
    "next_torus": [[str(v) for v in row] for row in next_torus.tolist()],
    "kernel_basis": [[str(v) for v in row] for row in kernel.tolist()],
  }
  (ROOT / "recursive_normal_borel_checks.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
  main()
