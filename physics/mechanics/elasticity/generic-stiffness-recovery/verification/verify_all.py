"""Reconstruct and check the exact arithmetic used in the accompanying paper.

This is an arithmetic checker, not a formalization of the geometric argument.
Run from any working directory. No network requests are made.
"""

import argparse
import itertools
import json
import re
import select
import shutil
import subprocess
import sys
import time
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def run(command, label, seconds=240):
  print(f"\nSTART {label}", flush=True)
  start = last = time.monotonic()
  process = subprocess.Popen(
    command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    text=True, bufsize=1,
  )
  lines = []
  while process.poll() is None:
    now = time.monotonic()
    if now - start > seconds:
      process.kill()
      process.communicate()
      raise RuntimeError(f"Timeout in {label} after {seconds} seconds")
    readable, _, _ = select.select([process.stdout], [], [], 1)
    if readable:
      line = process.stdout.readline()
      if line:
        lines.append(line)
        print(line, end="", flush=True)
    if now - last > 10:
      print(f"{label}: elapsed {now-start:.1f}s", flush=True)
      last = now
  remainder = process.communicate()[0]
  lines.append(remainder)
  print(remainder, end="", flush=True)
  output = "".join(lines)
  (ROOT / f"{label}.log").write_text(output)
  if process.returncode or re.search(r"^\s*\?", output, re.MULTILINE):
    raise RuntimeError(f"Failed {label}; inspect {label}.log")
  print(f"PASS {label} ({time.monotonic()-start:.1f}s)", flush=True)
  return output


def record(name):
  return json.loads((ROOT / name).read_text())


def check_linear_gates():
  collision = record("collision_incidence_checks.json")
  assert collision["trace_rank"] == 6
  assert collision["trace_kernel_dimension"] == 15
  assert collision["H0_incidence_rank"] == 15
  p = sp.symbols("p1:4")
  assert sp.expand(sp.sympify(collision["H0_determinant"]) - 2*sum(x*x for x in p)**3) == 0
  borel = record("minimum_rank_borel_checks.json")
  assert int(borel["tracefree_contraction_determinant"]) == 4194304
  assert borel["raising_operator_kernel_dimension"] == 3
  assert borel["distinct_torus_weights"] == [4, 2, 0]
  assert [r["incidence_rank"] for r in borel["highest_weight_line_checks"]] == [6, 11, 15]
  first = record("normal_borel_checks.json")
  assert first["normal_kernel_dimension"] == 5
  assert [(r["weight"], r["eigenspace_dimension"], r["normal_matrix_rank"])
          for r in first["B_fixed_line_families"]] == [("0", 1, 6), ("2", 1, 2)]
  second = record("recursive_normal_borel_checks.json")
  assert second["base_rank"] == 2
  assert second["affine_tangent_kernel_dimension"] == 2
  assert second["next_quotient_dimension"] == 8
  rank11 = record("rank11_local/rank11_tangent_certificate.json")
  assert rank11["basepoint_rank"] == 11
  assert rank11["normal_map_rank"] == 7
  assert rank11["affine_tangent_dimension"] == 8
  print("PASS all representation and normal-space arithmetic gates", flush=True)


def independent_dimension(bound):
  data = record("recursive_normal_borel_checks.json")
  entries = ",\n".join(
    ",".join(value.replace("I", "j").replace("**", "^") for value in row)
    for row in data["next_normal_matrix"]
  )
  slug = f"recursive_normal_rank{bound}_independent"
  script = ROOT / (slug + ".sing")
  script.write_text(
    "ring Audit=(0,j),(w7,w6,w5,w4,w3,w2,w1,w0),Dp;\n"
    "minpoly=j^2+1;\noption(redSB);\n"
    f"matrix M[7][13]={entries};\nideal J=minor(M,{bound+1});\n"
    'print("Computing reverse-variable degree-lex standard basis");\n'
    'ideal G=std(J);\nprint("INDEPENDENT_AFFINE_DIMENSION"); dim(G);\n'
    'print("BASIS_SIZE"); size(G);\n'
    f'link output="ASCII:w {slug}_leading.txt";\n'
    'for(int k=1;k<=size(G);k++){write(output,string(lead(G[k])));}\n'
    'close(output);\nquit;\n'
  )
  output = run(["Singular", "-q", script.name], slug)
  match = re.search(r"INDEPENDENT_AFFINE_DIMENSION\s+(\d+)", output)
  assert match and int(match[1]) == bound
  variables = sp.symbols("w0:8")
  supports = []
  for line in (ROOT / f"{slug}_leading.txt").read_text().splitlines():
    poly = sp.Poly(sp.sympify(line.replace("^", "**")), *variables)
    assert len(poly.monoms()) == 1
    supports.append({i for i, power in enumerate(poly.monoms()[0]) if power})
  covers = []
  for size in range(9):
    covers = [list(c) for c in itertools.combinations(range(8), size)
              if all(set(c) & support for support in supports)]
    if covers:
      break
  assert 8 - size == bound
  return {"rank_bound": bound, "affine_dimension": 8-size,
          "minimum_variable_cover_size": size, "minimal_covers": covers}


def main():
  if not __debug__:
    raise RuntimeError("Run this verifier without Python's -O option.")
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--with-groebner", action="store_true",
                      help="also regenerate optional Singular corroboration in two orders")
  args = parser.parse_args()
  if args.with_groebner and shutil.which("Singular") is None:
    raise RuntimeError("Singular is required only for --with-groebner; see README.md")
  print(f"Python {sys.version.split()[0]}; SymPy {sp.__version__}", flush=True)
  scripts = [
    "check_collision_incidence.py", "check_minimum_rank_borel.py",
    "check_rank6_tangent.py", "check_normal_borel.py",
    "check_recursive_normal_borel.py", "rank11_local/check_rank11_tangent.py",
    "certify_rank14_pencil.py", "verify_slice_certificates.py",
    "verify_rank1_minor_certificate.py", "check_finite_direction_interpolation.py",
  ]
  for script in scripts:
    run([sys.executable, "-u", script], Path(script).stem)
  check_linear_gates()
  certificates = record("linear-certificates/minor_dimension_certificates.json")
  reconstructed = record("recursive_normal_borel_checks.json")["next_normal_matrix"]
  assert certificates["matrix"] == reconstructed, "Minor-certificate source matrix mismatch"
  print("PASS embedded N2 matrix equals the reconstructed normal quotient", flush=True)
  run([sys.executable, "-u", "linear-certificates/verify_certificates.py"],
      "verify_minor_dimension_certificates")
  bounds = record("linear-certificates/independent_verification.json")
  assert bounds["verification"] == "PASS"
  assert [(r["rank_bound"], r["identities_verified"], r["dimension_upper_bound"])
          for r in bounds["bounds"]] == [(2, 6, 2), (3, 5, 3)]
  run([sys.executable, "-O", "-u", "finite-directions/verify_gcd4_slice_source.py", "11"],
      "verify_finite_direction_source")
  run([sys.executable, "-O", "-u", "finite-directions/verify_direct_powers.py"],
      "verify_finite_direction_identities")
  finite_source = record("finite-directions/gcd4_slice_n11_source_audit.json")
  finite_identity = record("finite-directions/direct_power_audit.json")
  assert finite_source["all_coefficient_identities_verified"]
  assert (finite_source["slice_rank_mod_p"], finite_source["t_unisolvent_points"],
          finite_source["p_unisolvent_points"]) == (11, 286, 28)
  assert finite_identity["dimension_zero_certified"]
  assert finite_identity["identities_verified"] == 11
  assert finite_source["sha256"]["gcd4_slice_n11.sing"] == finite_identity["sha256"]["gcd4_slice_n11.sing"]
  dimensions = []
  if args.with_groebner:
    run([sys.executable, "-u", "prepare_recursive_normal_ideals.py"],
        "prepare_recursive_normal_ideals")
    for bound, count in [(2, 102), (3, 215)]:
      slug = f"recursive_normal_rank{bound}"
      output = run(["Singular", "-q", slug + ".sing"], slug)
      match = re.search(r"AFFINE_DIMENSION\s+(\d+)", output)
      assert match and int(match[1]) == bound
      match = re.search(r"STANDARD_BASIS_SIZE\s+(\d+)", output)
      assert match and int(match[1]) == count
      dimensions.append(independent_dimension(bound))
    (ROOT / "recursive_normal_independent_dimension_audit.json").write_text(
      json.dumps(dimensions, indent=2) + "\n"
    )
  report = {
    "all_arithmetic_checks_passed": True,
    "normal_rank_dimension_upper_bounds": bounds["bounds"],
    "certificate_matrix_matches_reconstructed_N2": True,
    "finite_direction_slice_source_verified": True,
    "finite_direction_slice_dimension_zero_certified": True,
    "finite_direction_certificate_hashes": {
      "source": finite_source["sha256"], "identities": finite_identity["sha256"],
    },
    "groebner_corroboration_run": args.with_groebner,
    "optional_groebner_dimensions": dimensions,
    "geometric_argument": "Written proof; not established by this script alone",
    "formal_coverage": (
      "Separate Lean proofs cover seven matrix/collision lemmas and eleven N2 "
      "determinant identities; not the finite-direction cubic slice or geometric theorem"
    ),
  }
  (ROOT / "verification_summary.json").write_text(json.dumps(report, indent=2)+"\n")
  print("\nALL ARITHMETIC GATES PASSED. Read the paper for the geometric deductions.", flush=True)


if __name__ == "__main__":
  main()
