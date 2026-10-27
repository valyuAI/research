#!/usr/bin/env python3
"""Replay exact compiled searches, requiring the expected answers and counts."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import time


def runCase(label, command, expected, logDir):
  log = logDir / (label + ".txt")
  print("START " + label, flush=True)
  start = time.monotonic()
  with log.open("w") as output:
    process = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT)
    while process.poll() is None:
      try:
        process.wait(timeout=20)
      except subprocess.TimeoutExpired:
        print(f"{label}: running, {time.monotonic() - start:.0f}s", flush=True)
  text = log.read_text()
  results = [line for line in text.splitlines() if line.startswith("RESULT ")]
  matches = results == [expected]
  if process.returncode != 0 or not matches:
    raise RuntimeError(f"{label}: exit={process.returncode}, results={results}; see {log}")
  print("PASS " + label + ": " + results[0], flush=True)
  return {"case": label, "command": command, "result": results[0], "seconds": round(time.monotonic() - start, 3)}


def main():
  os.chdir(Path(__file__).resolve().parent)
  buildDir = Path("build")
  buildDir.mkdir(exist_ok=True)
  stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
  logDir = Path("logs") / ("replay-" + stamp)
  logDir.mkdir(parents=True)
  for name in ("subsp", "bucket", "rankfq"):
    subprocess.run([os.environ.get("CC", "cc"), "-O3", "-Wall", "-Wextra", "-o", str(buildDir / name), name + ".c"], check=True)
  subprocess.run([os.environ.get("CXX", "c++"), "-std=c++17", "-O3", "-Wall", "-Wextra", "-o", str(buildDir / "check_local_rank7"), "check_local_rank7.cpp"], check=True)
  cases = [
    ("subsp_A2_rank8", "subsp", ["21", "4"], "RESULT f=21 n=4 rank<=8: NO (independent 4-subsets tested 103406616, hits 0)"),
    ("bucket_A2_rank8", "bucket", ["2", "1", "0", "1", "0", "1"], "RESULT q=2 f=1,0,1,0,1 rank<=8: NO (triples 74377, candidate buckets 464776, hits 0)"),
    ("rankfq_q2_rank8", "rankfq", ["2", "4", "1", "0", "1", "0", "1"], "RESULT q=2 f=1,0,1,0,1 rank<=8: NO (prefixes 74377, candidate buckets 464776)"),
    ("bucket_F16_rank8", "bucket", ["2", "1", "1", "0", "0", "1"], "RESULT q=2 f=1,1,0,0,1 rank<=8: NO (triples 24962, candidate buckets 7322, hits 0)"),
    ("rankfq_T4_rank8", "rankfq", ["2", "4", "0", "0", "0", "0", "1"], "RESULT q=2 f=0,0,0,0,1 rank<=8: YES (prefixes 24898, candidate buckets 400307)"),
    ("rankfq_q3_rank7", "rankfq", ["3", "3", "1", "0", "2", "0", "1"], "RESULT q=3 f=1,0,2,0,1 rank<=7: NO (prefixes 4794, candidate buckets 205980)"),
    ("rankfq_q4_rank7", "rankfq", ["4", "3", "3", "0", "1", "0", "1"], "RESULT q=4 f=3,0,1,0,1 rank<=7: NO (prefixes 21668, candidate buckets 1930239)"),
    ("rankfq_q5_rank7", "rankfq", ["5", "3", "4", "0", "4", "0", "1"], "RESULT q=5 f=4,0,4,0,1 rank<=7: NO (prefixes 73000, candidate buckets 17417506)"),
    ("local_q3_split", "check_local_rank7", ["3", "--split"], "RESULT rank<=7: YES prefixes=1 candidates=18"),
    ("local_q5_split", "check_local_rank7", ["5", "--split"], "RESULT rank<=7: YES prefixes=1 candidates=38"),
    ("local_q3", "check_local_rank7", ["3"], "RESULT rank<=7: NO prefixes=4794 candidates=205980"),
    ("local_q5", "check_local_rank7", ["5"], "RESULT rank<=7: NO prefixes=73000 candidates=17417506"),
  ]
  results = []
  for label, name, arguments, expected in cases:
    results.append(runCase(label, ["nice", "-n", "10", str(buildDir / name), *arguments], expected, logDir))
  (logDir / "results.json").write_text(json.dumps({"all_passed": True, "checks": results}, indent=2) + "\n")
  print(f"ALL {len(results)} COMPILED SEARCHES PASSED; logs in {logDir}", flush=True)


if __name__ == "__main__":
  main()
