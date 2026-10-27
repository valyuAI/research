#!/usr/bin/env python3
"""Counting facts behind the 6x6x6 discussion and the round-optimality remark for 7x7x7.
Standard library only: python3 -I obstruction6.py"""
import json
from itertools import product


def build(n):
    cells = list(product(range(1, n + 1), repeat=3))
    dirs = [d for d in product((-1, 0, 1), repeat=3) if d != (0, 0, 0) and next(v for v in d if v) > 0]
    lines = []
    for d in dirs:
        for s in product(range(1, n + 1), repeat=3):
            if any((d[i] == 1 and s[i] != 1) or (d[i] == -1 and s[i] != n) for i in range(3)):
                continue
            lines.append(tuple((s[0] + t * d[0], s[1] + t * d[1], s[2] + t * d[2]) for t in range(n)))
    return cells, lines


out = {}
# ---- 6^3 ----
cells, lines = build(6)
space = [l for l in lines if all(len({c[k] for c in l}) == 6 for k in range(3))]
assert len(lines) == 148 and len(space) == 4
deg = {c: sum(1 for l in lines if c in l) for c in cells}
nonspace = {c: sum(1 for l in lines if c in l and l not in space) for c in cells}
out["6^3"] = {"cells": len(cells), "lines": len(lines), "degree_histogram": {}, "max_non_space_lines_per_cell": max(nonspace.values())}
for v in deg.values():
    out["6^3"]["degree_histogram"][v] = out["6^3"]["degree_histogram"].get(v, 0) + 1
# After k full rounds (Maker to move) a pairing needs 2*(148-E) <= 216-2k, i.e. E >= 40+k,
# while k Breaker cells meet at most 6k + min(k,4) lines.
rows = []
for k in range(1, 13):
    need = 40 + k
    bound = 6 * k + min(k, 4)
    rows.append({"k": k, "lines_needed": need, "upper_bound_lines_met": bound, "pairing_possible_by_counting": bound >= need})
out["6^3"]["rounds"] = rows
out["6^3"]["first_round_not_excluded"] = min(r["k"] for r in rows if r["pairing_possible_by_counting"])
# single-line surplus ceiling: an alive line with j Maker cells has 6-j free cells, 2 slots
out["6^3"]["single_line_surplus_ceiling"] = {j: 6 - j - 2 for j in range(0, 5)}
# ---- 7^3 round optimality ----
cells7, lines7 = build(7)
deg7 = {c: sum(1 for l in lines7 if c in l) for c in cells7}
assert len(lines7) == 193 and deg7[(4, 4, 4)] == 13 and sorted(deg7.values())[-2] == 7
# centre opening (Maker holds the centre): after k rounds need 2*(193-E) <= 343-2k, E >= 21.5+k;
# k Breaker cells meet at most 7k lines.
out["7^3"] = {
    "centre_opening": [{"k": k, "need": 22 + k, "max_met": 7 * k, "possible": 7 * k >= 22 + k} for k in (2, 3, 4)],
    # non-centre opening: best two Breaker cells meet <= 13 + 6 = 19 lines (centre + any cell;
    # every other cell shares a line with the centre only if ... we bound by 13+7=20 anyway).
    "noncentre_opening": [{"k": 2, "need": 24, "max_met_upper_bound": 13 + 7, "possible": 13 + 7 >= 24},
                          {"k": 3, "need": 25, "achieved": 25}],
}
print(json.dumps(out, indent=1))
assert out["6^3"]["max_non_space_lines_per_cell"] == 6
assert out["6^3"]["first_round_not_excluded"] == 8
assert not out["7^3"]["centre_opening"][1]["possible"] and out["7^3"]["centre_opening"][2]["possible"]
assert not out["7^3"]["noncentre_opening"][0]["possible"]
json.dump(out, open("results/obstruction6.json", "w"), indent=1)
print("OBSTRUCTION_FACTS_OK")
