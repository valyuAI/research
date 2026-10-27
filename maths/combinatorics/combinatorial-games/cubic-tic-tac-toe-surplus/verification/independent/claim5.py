"""Claim 5: which pairs of cells cannot be mapped by any of the 48 cube
symmetries into the half-cube {x <= 4}? Brute force vs characterization
'p - c and q - c have strictly opposite signs in every coordinate'."""
import itertools
from core import CELLS, CI, SYMS, CELL_LINES, LINES

def mappable(p, q):
  return any(CELLS[g[p]][0] <= 4 and CELLS[g[q]][0] <= 4 for g in SYMS)

def opposite(p, q):
  P, Q = CELLS[p], CELLS[q]
  return all((P[i] - 4) * (Q[i] - 4) < 0 for i in range(3))

bad = []
for p, q in itertools.combinations(range(len(CELLS)), 2):
  m = mappable(p, q)
  assert m == (not opposite(p, q)), (CELLS[p], CELLS[q])
  if not m:
    bad.append((p, q))
print("unmappable unordered pairs:", len(bad), "(expected 216*27/2 =", 216 * 27 // 2, ")")
p0, q0 = CELLS.index((1, 7, 1)), CELLS.index((6, 2, 6))
print("(1,7,1),(6,2,6) mappable?", mappable(p0, q0))
# relevance: first Maker move non-centre, second Maker move arbitrary non-centre
share = sum(1 for p, q in bad if set(CELL_LINES[p]) & set(CELL_LINES[q]))
print("of these, pairs sharing a line:", share)
# also: with the weaker target {x<=4} OR via 'some coordinate' -- any pair can be put in a closed half-space through c?
# check: can every pair be mapped into {x <= 4} or {x >= 4}? (same thing by reflection)
# and: can every pair be mapped so both lie in a closed octant-free 'half' {x+y+z <= 12}?
def mappable_sum(p, q):
  return any(sum(CELLS[g[p]]) <= 12 and sum(CELLS[g[q]]) <= 12 for g in SYMS)
print("all pairs mappable into {x+y+z<=12}?", all(mappable_sum(p, q) for p, q in bad))
