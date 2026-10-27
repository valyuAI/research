"""Claim 3 (non-centre case). Usage:
  python3 claim3.py classes            -> all symmetry classes (weighted counts)
  python3 claim3.py raw <part> <nparts> -> raw configurations, slice part/nparts
  python3 claim3.py sample <n> <seed>  -> random raw sample
"""
import sys
import time
import random
import itertools
from collections import Counter, defaultdict
from core import CELLS, CI, LINES, SPACE_DIAGS, DIAG_CELLS, CELL_LINES, surplus, canon

diag_of = {c: d for d in SPACE_DIAGS for c in DIAG_CELLS[d]}
ALLDIAG = sorted(diag_of)
pairs = []
for a, b in itertools.combinations(ALLDIAG, 2):
  if diag_of[a] == diag_of[b]:
    continue
  if set(CELL_LINES[a]) & set(CELL_LINES[b]):
    continue
  pairs.append((a, b))
partners = Counter()
for a, b in pairs:
  partners[a] += 1
  partners[b] += 1
NONCENTRE = [i for i in range(len(CELLS)) if i != CI]
configs = [(m, a, b) for (a, b) in pairs for m in NONCENTRE if m not in (a, b)]


def header():
  print("pairs:", len(pairs), "partner counts:", dict(Counter(partners.values())),
        "cells with partners:", len(partners), "configs:", len(configs), flush=True)


def run(cfgs, weights=None, label=""):
  t0 = time.time()
  dist = Counter()
  worst = []
  for n, (m, a, b) in enumerate(cfgs):
    s, _ = surplus([m], [CI, a, b], K=4)
    w = 1 if weights is None else weights[n]
    dist[s] += w
    if s is None or s < 2:
      worst.append((CELLS[m], CELLS[a], CELLS[b], s))
    if (n + 1) % 200 == 0:
      print(f"{label} {n + 1}/{len(cfgs)} {time.time() - t0:.0f}s", flush=True)
  print(f"{label} sigma distribution (capped 4):", dict(dist))
  print(f"{label} configs with sigma<2:", worst[:50], "count", len(worst))
  print(f"{label} time {time.time() - t0:.1f}s", flush=True)


mode = sys.argv[1]
header()
if mode == "classes":
  cls = defaultdict(int)
  rep = {}
  for (m, a, b) in configs:
    k = canon([m], [CI, a, b])
    cls[k] += 1
    rep.setdefault(k, (m, a, b))
  keys = sorted(cls)
  print("classes:", len(keys), "total weight:", sum(cls.values()), flush=True)
  run([rep[k] for k in keys], [cls[k] for k in keys], "classes(weighted by orbit size)")
elif mode == "raw":
  part, nparts = int(sys.argv[2]), int(sys.argv[3])
  run(configs[part::nparts], None, f"raw[{part}/{nparts}]")
elif mode == "sample":
  n, seed = int(sys.argv[2]), int(sys.argv[3])
  rng = random.Random(seed)
  run(rng.sample(configs, n), None, f"sample{n}")
