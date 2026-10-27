#!/usr/bin/env python3
"""F2/F3/F5 controls. Retained-log fixtures are not fresh enumerations.

Usage: python3 -B test_review_regressions.py --output /new/evidence/directory
Add --q5 to replay the larger C q=5 search. Never repeats subsp 21 4.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import run_searches

HERE = Path(__file__).resolve().parent
RETAINED = HERE / "logs/replay-20261026T134435172402Z"


def require(condition, message):
  if not condition:
    raise RuntimeError(message)


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("--output", type=Path, required=True)
  parser.add_argument("--q5", action="store_true")
  args = parser.parse_args()
  output = args.output.resolve()
  output.mkdir(parents=True, exist_ok=False)
  for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                   "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[variable] = "1"
  records = []

  def run(label, command, expectedExit=0, expectedResult=None):
    command = ["nice", "-n", "10", *map(str, command)]
    print("START " + label, flush=True)
    start = time.monotonic()
    log = output / (label + ".txt")
    with log.open("w") as stream:
      process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
      while True:
        try:
          code = process.wait(timeout=10)
          break
        except subprocess.TimeoutExpired:
          print(f"{label}: running {time.monotonic() - start:.0f}s", flush=True)
          if time.monotonic() - start > 1800:
            process.kill()
            process.wait()
            raise RuntimeError(f"{label}: timeout; see {log}")
    text = log.read_text()
    require(code == expectedExit, f"{label}: exit {code}; see {log}")
    require("runtime error:" not in text and "Sanitizer" not in text,
            f"{label}: sanitizer diagnostic; see {log}")
    lines = [line for line in text.splitlines() if line.startswith("RESULT ")]
    if expectedExit:
      require(not lines, f"{label}: rejected input printed a RESULT")
    elif expectedResult is not None:
      require(lines == [expectedResult], f"{label}: result mismatch {lines}")
    records.append({"case": label, "command": command, "exit": code,
                    "seconds": round(time.monotonic() - start, 3), "results": lines})
    (output / "progress.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS " + label + (": " + lines[0] if lines else ""), flush=True)
    return lines

  for name in ("subsp", "rankfq"):
    run("compile-" + name, [os.environ.get("CC", "cc"), "-O1", "-g", "-Wall", "-Wextra",
        "-fsanitize=address,undefined", "-fno-sanitize-recover=all",
        HERE / (name + ".c"), "-o", output / name])

  subspInvalid = [[], ["21"], ["21", "4", "extra"], ["0", "4"], ["1", "0"],
                 ["32", "4"], ["21", "9"], ["-1", "0"], ["21", "-1"],
                 ["abc", "4"], ["21", "4x"], ["", "0"], ["21", ""],
                 ["999999999999999999999999", "4"], ["21", "999999999999999999999999"],
                 ["3", "1"], ["7", "3"], ["15", "7"]]
  rankfqInvalid = [[], ["2", "1", "1"], ["2", "1", "1", "0", "0", "0", "0", "1"],
                  ["0", "1", "1", "1", "1"], ["6", "1", "1", "1", "1"],
                  ["8", "1", "1", "1", "1"], ["2x", "1", "1", "1", "1"],
                  ["999999999999999999999999", "1", "1", "1", "1"],
                  ["2", "0", "1", "1", "1"], ["2", "5", "1", "1", "1"],
                  ["2", "1x", "1", "1", "1"], ["2", "", "1", "1", "1"],
                  ["2", "1", "bad", "1", "1"], ["2", "1", "-1", "1", "1"],
                  ["2", "1", "2", "1", "1"], ["2", "1", "1x", "1", "1"],
                  ["2", "1", "999999999999999999999999", "1", "1"],
                  ["2", "1", "1", "1", "0"], ["2", "1", "1", "1"],
                  ["2", "3", "1", "1", "1"], ["5", "3", "0", "4", "1", "4", "1"],
                  ["7", "3", "0", "1", "4", "1", "1"]]
  for name, cases in (("subsp", subspInvalid), ("rankfq", rankfqInvalid)):
    for index, arguments in enumerate(cases, 1):
      run(f"{name}-invalid-{index}", [output / name, *arguments], 2)

  # All supported binary polynomials at increments 0..2; compare two real searches.
  agreements = 0
  for f in range(2, 32):
    n = f.bit_length() - 1
    for m in range(min(2, n * n - n) + 1):
      subspLines = run(f"subsp-f{f}-m{m}", [output / "subsp", f, m])
      require(len(subspLines) == 1, "missing subsp result")
      if m:
        coefficients = [(f >> bit) & 1 for bit in range(n + 1)]
        rankfqLines = run(f"rankfq-f{f}-m{m}", [output / "rankfq", 2, m, *coefficients])
        require(len(rankfqLines) == 1, "missing rankfq result")
        require(subspLines[0].split(": ")[1].split()[0] ==
                rankfqLines[0].split(": ")[1].split()[0], f"binary disagreement f={f} m={m}")
        agreements += 1

  run("rankfq-q7-max-forms", [output / "rankfq", 7, 1, 1, 0, 0, 1, 1],
      expectedResult="RESULT q=7 f=1,0,0,1,1 rank<=5: NO (prefixes 1, candidate buckets 0)")
  tree = ast.parse((HERE / "run_searches.py").read_text())
  cases = next(ast.literal_eval(node.value) for node in ast.walk(tree)
               if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "cases" for t in node.targets))
  expected = {row[0]: row[3] for row in cases}
  retained = json.loads((RETAINED / "results.json").read_text())["checks"]
  require(len(cases) == len(retained) == 12, "unexpected retained case count")
  for record in retained:
    label = record["case"]
    require(record["result"] == expected[label], f"retained expectation mismatch: {label}")
    run_searches.runCase("fixture-" + label,
                        [sys.executable, "-B", "-c", "from pathlib import Path; "
                         f"print(Path({str(RETAINED / (label + '.txt'))!r}).read_text(), end='')"],
                        expected[label], output)

  cLine = expected["rankfq_q5_rank7"]
  cppLine = expected["local_q5"]
  mutants = [
    ("c-buckets", cLine, cLine.replace("17417506", "0"), 0),
    ("cpp-buckets", cppLine, cppLine.replace("17417506", "0"), 0),
    ("q-scope", cLine, cLine.replace("q=5", "q=3"), 0),
    ("polynomial-scope", cLine, cLine.replace("4,0,4,0,1", "0,0,0,0,1"), 0),
    ("missing-scope", cLine, cLine.replace("q=5 f=4,0,4,0,1 ", ""), 0),
    ("prefix-digit", cppLine, cppLine.replace("73000", "730000"), 0),
    ("wrong-answer", cLine, cLine.replace("NO", "YES"), 0),
    ("wrong-rank", cLine, cLine.replace("<=7", "<=8"), 0),
    ("truncated-result", cLine, cLine.split(", candidate")[0], 0),
    ("extra-suffix", cLine, cLine + " unverified", 0),
    ("nonzero-exit", cLine, cLine, 37),
    ("missing-result", cLine, "incomplete", 0),
    ("duplicate-result", cLine, cLine + "\n" + cLine, 0),
  ]
  for label, wanted, text, code in mutants:
    try:
      run_searches.runCase("mutant-" + label,
                          [sys.executable, "-B", "-c", f"print({text!r}); raise SystemExit({code})"],
                          wanted, output)
    except RuntimeError:
      print("PASS rejected " + label, flush=True)
    else:
      raise RuntimeError("accepted mutant " + label)

  for label, name, arguments, wanted in cases:
    if label in ("rankfq_q2_rank8", "rankfq_T4_rank8", "rankfq_q3_rank7", "rankfq_q4_rank7"):
      run("fresh-" + label, [output / name, *arguments], expectedResult=wanted)
  if args.q5:
    run("compile-rankfq-fast", [os.environ.get("CC", "cc"), "-O3", "-Wall", "-Wextra",
        HERE / "rankfq.c", "-o", output / "rankfq-fast"])
    run("fresh-rankfq_q5_rank7", [output / "rankfq-fast", 5, 3, 4, 0, 4, 0, 1],
        expectedResult=cLine)
  summary = {"all_passed": True, "fresh_process_checks": records,
             "binary_answer_agreements": agreements, "retained_log_fixtures": 12,
             "rejected_runner_mutants": len(mutants), "subsp_21_4_replayed": False,
             "q5_c_fresh": args.q5,
             "source_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                               for name in ("rankfq.c", "subsp.c", "run_searches.py", Path(__file__).name)}}
  (output / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
  print("ALL REVIEW REGRESSIONS PASSED", flush=True)


if __name__ == "__main__":
  main()
