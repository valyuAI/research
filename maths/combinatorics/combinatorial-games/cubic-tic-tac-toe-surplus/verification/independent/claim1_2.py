"""Claims 1 and 2 (centre case). Exhaustive over all 1296 raw Breaker sets
(no symmetry reduction), plus the Breaker rule against all Maker sequences."""
import itertools
import time
from collections import Counter
from core import CELLS, IDX, CI, LINES, SPACE_DIAGS, DIAG_CELLS, CELL_LINES, surplus, lines_met

t0 = time.time()
tab = Counter()
per_set = {}
for n, combo in enumerate(itertools.product(*[DIAG_CELLS[d] for d in SPACE_DIAGS])):
  B = list(combo)
  nl = len(lines_met(B))
  s, alive = surplus([CI], B, K=4)
  per_set[tuple(sorted(B))] = (nl, s)
  tab[(nl, s)] += 1
  if (n + 1) % 100 == 0:
    print(f"claim1 {n + 1}/1296 done, {time.time() - t0:.1f}s", flush=True)
print("CLAIM 1 table (lines met by B, sigma capped at 4; None = no saturating matching):")
for k in sorted(tab, key=lambda k: (-k[0], str(k[1]))):
  print(f"  lines={k[0]} sigma={k[1]} count={tab[k]}")
print(f"claim1 time {time.time() - t0:.1f}s", flush=True)

# Claim 2: Breaker rule
def rule_pick(maker_diag, breaker):
  used = set()
  for b in breaker:
    for d in SPACE_DIAGS:
      if b in LINES[d]:
        used.add(d)
  met = lines_met(breaker)
  best = None
  for d in SPACE_DIAGS:
    if d in used:
      continue
    for c in DIAG_CELLS[d]:
      if c in maker_diag or c in breaker:
        continue
      gain = len(set(CELL_LINES[c]) - met)
      key = (-gain, CELLS[c])
      if best is None or key < best[0]:
        best = (key, c)
  return None if best is None else best[1]

ALLDIAG = [c for d in SPACE_DIAGS for c in DIAG_CELLS[d]]
OFF = None
b1 = IDX[(5, 5, 5)]
results = Counter()
finals = Counter()
nseq = 0
for m2 in [OFF] + ALLDIAG:
  if m2 == b1:
    continue
  mk = set() if m2 is None else {m2}
  br = [b1]
  p2 = rule_pick(mk, br)
  br2 = br + [p2]
  for m3 in [OFF] + ALLDIAG:
    if m3 is not None and (m3 in mk or m3 in br2):
      continue
    mk3 = mk | ({m3} if m3 is not None else set())
    p3 = rule_pick(mk3, br2)
    br3 = br2 + [p3]
    for m4 in [OFF] + ALLDIAG:
      if m4 is not None and (m4 in mk3 or m4 in br3):
        continue
      mk4 = mk3 | ({m4} if m4 is not None else set())
      p4 = rule_pick(mk4, br3)
      assert p4 is not None
      br4 = br3 + [p4]
      assert len(set(br4)) == 4 and not (set(br4) & mk4)
      nl = len(lines_met(br4))
      results[nl] += 1
      finals[tuple(sorted(br4))] += 1
      nseq += 1
print("CLAIM 2: Maker diagonal-relevant sequences enumerated:", nseq)
print("  final lines-met distribution:", dict(results))
print("  distinct final Breaker sets:", len(finals))
fs = Counter(per_set[f] for f in finals)
print("  (lines, sigma) of distinct final sets (Maker={c} only):", dict(fs))
print("  final sets:", [[CELLS[c] for c in f] for f in sorted(finals)])
print(f"total time {time.time() - t0:.1f}s")
