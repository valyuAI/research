"""Prepare exact Q(i) dimension calculations for the recursive normal map."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
  data = json.loads((ROOT / "recursive_normal_borel_checks.json").read_text())
  entries = ",\n".join(
    ",".join(value.replace("I", "i").replace("**", "^") for value in row)
    for row in data["next_normal_matrix"]
  )
  for bound in [2, 3]:
    slug = f"recursive_normal_rank{bound}"
    output = ROOT / f"{slug}.sing"
    output.write_text(
      "ring R=(0,i),(w0,w1,w2,w3,w4,w5,w6,w7),dp;\n"
      "minpoly=i^2+1;\n"
      f"matrix N[7][13]={entries};\n"
      f'print("Generating all {bound+1}x{bound+1} minors over Q(i)");\n'
      f"ideal J=minor(N,{bound+1});\n"
      'print("NONZERO_MINORS"); size(J);\n'
      'print("Computing exact standard basis");\n'
      "ideal G=std(J);\n"
      'print("AFFINE_DIMENSION"); dim(G);\n'
      'print("STANDARD_BASIS_SIZE"); size(G);\n'
      f'link output="ASCII:w {slug + "_basis.txt"}";\n'
      'for(int k=1;k<=size(G);k++){write(output,"generator="+string(k));write(output,G[k]);}\n'
      "close(output);\nquit;\n"
    )
    print(f"Prepared {output.name}", flush=True)


if __name__ == "__main__":
  main()
