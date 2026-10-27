"""Compare the saved knot labels and diagrams with KnotInfo's CSV release."""

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIELDS = (
  "name",
  "dt_name",
  "crossing_number",
  "bridge_index",
  "geometric_type",
  "alternating",
  "montesinos_notation",
  "pretzel_notation",
  "pd_notation",
)
TYPE_FIELDS = (
  "conway_notation",
  "montesinos_notation",
  "pretzel_notation",
)


def main():
  if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 check_source.py /path/to/knotinfo_data_complete.csv")
  path = Path(sys.argv[1])
  snapshot = json.loads((ROOT / "source-snapshot.json").read_text())
  expected = {row["name"]: row for row in snapshot["rows"]}
  open_names = set(json.loads((ROOT / "open-list-v1.3.0.json").read_text()))
  assert len(expected) == 27
  assert len(open_names) == 293
  digest = hashlib.sha256()
  with path.open("rb") as stream:
    while block := stream.read(1024 * 1024):
      digest.update(block)
  assert digest.hexdigest() == snapshot["csv_sha256"], "KnotInfo CSV hash differs"
  rows = {}
  open_intervals = {}
  type_field_audit = {"thirteen_crossing_rows": 0, "nonblank": {field: 0 for field in TYPE_FIELDS}}
  with path.open(newline="") as stream:
    for row in csv.DictReader(stream, delimiter="|"):
      if row["crossing_number"] == "13":
        type_field_audit["thirteen_crossing_rows"] += 1
        for field in TYPE_FIELDS:
          type_field_audit["nonblank"][field] += bool(row[field])
      if row["name"] in expected:
        rows[row["name"]] = row
      if row["name"] in open_names:
        open_intervals[row["name"]] = row["bridge_index"]
  assert set(rows) == set(expected)
  assert set(open_intervals) == open_names
  assert set(open_intervals.values()) == {"[3,4]"}
  assert type_field_audit == snapshot["type_field_audit"]
  for name, saved in expected.items():
    for field in FIELDS:
      assert rows[name][field] == saved[field], f"{name}: {field} differs"
    print(f"{name}: KnotInfo 2026.10.5 source row matches", flush=True)
  print("Type-field coverage audit matches all thirteen-crossing rows", flush=True)
  print("All 293 pinned names retain bridge interval [3,4] in KnotInfo 2026.10.5", flush=True)


if __name__ == "__main__":
  main()
