"""Prepare nested projective rank-stratum slices with an affine last chart.

Run r=13 before r=12, etc. The prior slice certifies the hyperplane at infinity.
This generator itself makes no emptiness claim.
"""

import argparse
import json
import random
from pathlib import Path

import sympy as sp

from certify_rank14_pencil import determinant

ROOT = Path(__file__).resolve().parent
PRIME = 32003


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("rank", type=int)
  parser.add_argument("--minors", type=int, default=6)
  args = parser.parse_args()
  assert 1 <= args.rank <= 13
  source = (ROOT / "collision_incidence_matrix.sing").read_text()
  expression = source.split("matrix B[15][21]=", 1)[1].split(";", 1)[0]
  matrix = sp.Matrix(15, 21, [sp.sympify(value.replace("^", "**")) for value in expression.split(",")])
  parameters = sp.symbols("h0:15")
  pencil = json.loads((ROOT / "rank14_pencil_certificate.json").read_text())
  axes = [pencil["H0_coordinates"], pencil["H1_coordinates"]]
  rng = random.Random(2026101701)
  while len(axes) < 16 - args.rank:
    axes.append([rng.randrange(-7, 8) for _ in parameters])
  matrices = [matrix.subs(dict(zip(parameters, axis))) for axis in axes]
  variables = sp.symbols(f"x0:{len(axes) - 1}")
  sliced = matrices[-1] + sum((v * m for v, m in zip(variables, matrices[:-1])), sp.zeros(15, 21))
  size = args.rank + 1
  selections = []
  for _ in range(10000):
    rows = sorted(rng.sample(range(15), size))
    columns = sorted(rng.sample(range(21), size))
    if determinant([[matrices[0][i, j] for j in columns] for i in rows]):
      selections.append({"rows_zero_based": rows, "columns_zero_based": columns})
      if len(selections) == args.minors:
        break
  assert len(selections) == args.minors
  slug = f"rank_slice_r{args.rank}"
  inputs = [
    'LIB "matrix.lib";',
    f"ring R={PRIME},({','.join(map(str, variables))}),dp;",
    "matrix B[15][21]=" + ",\n".join(
      ",".join(str(value).replace("**", "^") for value in row) for row in sliced.tolist()
    ) + ";",
    "ideal J;",
  ]
  for number, selection in enumerate(selections, 1):
    inputs.extend([
      f'print("Computing minor {number}/{len(selections)} of size {size}");',
      f"intvec rows{number}=" + ",".join(str(i + 1) for i in selection["rows_zero_based"]) + ";",
      f"intvec cols{number}=" + ",".join(str(i + 1) for i in selection["columns_zero_based"]) + ";",
      f"J[{number}]=det(submat(B,rows{number},cols{number}));",
    ])
  inputs.extend([
    'print("Computing standard basis of selected minors");',
    "ideal G=std(J);",
    'print("AFFINE_SLICE_STANDARD_BASIS"); G;',
    "if(size(G)==1 && G[1]==1){",
    '  print("UNIT_IDEAL_CERTIFIED");',
    "  matrix certificate=lift(J,ideal(1));",
    "  matrix generators[1][size(J)]=J; matrix verification=generators*certificate;",
    '  if(verification[1,1]==1){print("BEZOUT_IDENTITY_VERIFIED");}',
    f'  link certfile="ASCII:w {ROOT / (slug + "_bezout_complete.txt")}";',
    f'  write(certfile,"prime={PRIME}");',
    '  write(certfile,"rows="+string(nrows(certificate)));',
    '  int ci; for(ci=1;ci<=size(J);ci++){',
    '    write(certfile,"minor["+string(ci)+"]="+string(J[ci]));',
    '    write(certfile,"coefficient["+string(ci)+"]="+string(certificate[ci,1]));',
    '  }',
    '  close(certfile);',
    "}",
    "quit;",
  ])
  (ROOT / (slug + ".sing")).write_text("\n".join(inputs) + "\n")
  (ROOT / (slug + "_input.json")).write_text(json.dumps({
    "prime": PRIME,
    "excluded_rank_at_most": args.rank,
    "projective_slice_dimension": len(axes) - 1,
    "affine_chart": "last coordinate equals one",
    "nested_axes_in_H_basis": axes,
    "minors": selections,
    "required_infinity_certificate": f"rank_slice_r{args.rank + 1}" if args.rank < 13 else "rank14_pencil_certificate",
    "status": "Input only. Emptiness and certificate not yet established.",
  }, indent=2) + "\n")
  print(ROOT / (slug + ".sing"), flush=True)


if __name__ == "__main__":
  main()
