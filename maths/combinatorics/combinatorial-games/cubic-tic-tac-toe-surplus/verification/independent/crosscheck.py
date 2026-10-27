"""Independent second sigma method: for k = 0..K and each alive line L, build the
slot graph with 2 slots per line plus k extra copies of L's slot, and run plain
Kuhn (DFS) bipartite matching from scratch. sigma >= k iff all succeed
(for k=0: the base graph has a saturating matching).
Compared with core.surplus on random configurations of claims 1 and 3."""
import sys
import random
import itertools
from core import CELLS, CI, LINES, SPACE_DIAGS, DIAG_CELLS, CELL_LINES, surplus

sys.setrecursionlimit(10000)


def saturates(slots_adj):
  match = {}

  def try_(s, seen):
    for c in slots_adj[s]:
      if c in seen:
        continue
      seen.add(c)
      if c not in match or try_(match[c], seen):
        match[c] = s
        return True
    return False

  for s in range(len(slots_adj)):
    if not try_(s, set()):
      return False
  return True


def sigma2(maker, breaker, K=4):
  occ = set(maker) | set(breaker)
  alive = [l for l in LINES if not (set(l) & set(breaker))]
  base = []
  for l in alive:
    fr = [c for c in l if c not in occ]
    base += [fr, fr]
  if not saturates(base):
    return None
  for k in range(1, K + 1):
    for l in alive:
      fr = [c for c in l if c not in occ]
      if not saturates(base + [fr] * k):
        return k - 1
  return K


rng = random.Random(7)
diag_of = {c: d for d in SPACE_DIAGS for c in DIAG_CELLS[d]}
ALLDIAG = sorted(diag_of)
mism = 0
n = 0
# claim-1 style: one representative per lines-met value plus randoms
combos = list(itertools.product(*[DIAG_CELLS[d] for d in SPACE_DIAGS]))
for B in rng.sample(combos, 12):
  a, b = surplus([CI], B), sigma2([CI], B)
  n += 1
  mism += a[0] != b
  print("c1", [CELLS[c] for c in B], a[0], b, flush=True)
for _ in range(12):
  a, b = rng.sample(ALLDIAG, 2)
  m = rng.choice([i for i in range(len(CELLS)) if i not in (CI, a, b)])
  x, y = surplus([m], [CI, a, b])[0], sigma2([m], [CI, a, b])
  n += 1
  mism += x != y
  print("c3", CELLS[m], CELLS[a], CELLS[b], x, y, flush=True)
print("checked", n, "mismatches", mism)
