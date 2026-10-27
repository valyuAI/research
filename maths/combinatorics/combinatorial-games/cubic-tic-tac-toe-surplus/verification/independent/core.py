"""Independent core for Maker-Breaker 7^3: lines, symmetries, pairing surplus.

Surplus sigma = min over nonempty slot sets S of |N(S)| - |S| in the slot graph
(2 slots per alive line, each adjacent to the free cells of its line).
Twin slots => an optimal S is a union of full line-slot-pairs, so
sigma = min over nonempty alive-line sets T of |free(U T)| - 2|T|.
For each line L, min_{T containing L} of that quantity equals (capped at K)
the number of extra units of flow that can be pushed through L when L's
source capacity is raised from 2 to 2+K, starting from a saturating matching
(augmenting s-t paths never re-enter s, so other lines stay saturated).
"""
import itertools

N = 7
C = (4, 4, 4)
CELLS = [(x, y, z) for x in range(1, N + 1) for y in range(1, N + 1) for z in range(1, N + 1)]
IDX = {c: i for i, c in enumerate(CELLS)}


def gen_lines():
  dirs = []
  for d in itertools.product((-1, 0, 1), repeat=3):
    if d == (0, 0, 0):
      continue
    if tuple(-v for v in d) in dirs:
      continue
    dirs.append(d)
  assert len(dirs) == 13
  lines = set()
  for s in CELLS:
    for d in dirs:
      pts = [tuple(s[i] + k * d[i] for i in range(3)) for k in range(N)]
      if all(1 <= v <= N for p in pts for v in p):
        lines.add(frozenset(IDX[p] for p in pts))
  return [tuple(sorted(l)) for l in sorted(lines, key=lambda l: sorted(l))]


LINES = gen_lines()
assert len(LINES) == 193, len(LINES)
CELL_LINES = [[] for _ in CELLS]
for li, l in enumerate(LINES):
  for c in l:
    CELL_LINES[c].append(li)

# space diagonals
SPACE_DIAGS = [li for li, l in enumerate(LINES) if all(
  CELLS[l[0]][i] != CELLS[l[1]][i] for i in range(3))]
assert len(SPACE_DIAGS) == 4
CI = IDX[C]
DIAG_CELLS = {li: [c for c in LINES[li] if c != CI] for li in SPACE_DIAGS}


def gen_syms():
  syms = []
  for perm in itertools.permutations(range(3)):
    for flips in itertools.product((False, True), repeat=3):
      def f(p, perm=perm, flips=flips):
        q = [p[perm[i]] for i in range(3)]
        return tuple((N + 1 - q[i]) if flips[i] else q[i] for i in range(3))
      syms.append([IDX[f(p)] for p in CELLS])
  assert len(syms) == 48
  return syms


SYMS = gen_syms()
LINESET = set(LINES)
for g in SYMS:  # sanity: symmetries preserve the line set
  for l in LINES:
    assert tuple(sorted(g[c] for c in l)) in LINESET


def surplus(maker, breaker, K=4):
  """Return sigma capped at K, or None if no saturating matching exists.
  Also returns the list of alive lines and number of lines met by breaker."""
  maker = set(maker)
  breaker = set(breaker)
  alive = [li for li, l in enumerate(LINES) if not any(c in breaker for c in l)]
  free = [True] * len(CELLS)
  for c in maker | breaker:
    free[c] = False
  adj = {li: [c for c in LINES[li] if free[c]] for li in alive}
  mc = [-1] * len(CELLS)  # cell -> line matched to

  def augment(src, mc):
    # BFS over lines; find a free unmatched cell reachable by alternating path
    par = {src: None}
    via = {}
    q = [src]
    qi = 0
    while qi < len(q):
      u = q[qi]
      qi += 1
      for c in adj[u]:
        w = mc[c]
        if w == -1:
          # flip path
          cell = c
          line = u
          while True:
            prev_cell = via.get(line)
            mc[cell] = line
            if line == src:
              return True
            cell = prev_cell
            line = par[line]
        if w not in par:
          par[w] = u
          via[w] = c
          q.append(w)
    return False

  # note: when flipping, cell `prev_cell` (via[line]) was matched to `line`
  # and is reassigned to par[line]; line keeps its other matched cells.
  for li in alive:
    for _ in range(2):
      if not augment(li, mc):
        return None, alive
  best = K
  for li in alive:
    m2 = mc[:]
    k = 0
    while k < best and augment(li, m2):
      k += 1
    best = min(best, k)
    if best == 0:
      break
  return best, alive


def lines_met(cells):
  s = set()
  for c in cells:
    s.update(CELL_LINES[c])
  return s


def canon(*groups):
  best = None
  for g in SYMS:
    key = tuple(tuple(sorted(g[c] for c in grp)) for grp in groups)
    if best is None or key < best:
      best = key
  return best
