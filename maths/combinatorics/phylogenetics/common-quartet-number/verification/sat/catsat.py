"""Sanity check against Snir-Yuster's h*(k) = 2^k + 2 (all trees caterpillars). Adds snowflake-free clauses."""
import sys, itertools, time
from pysat.solvers import Solver
from qlib import quartet_index, tree_quartets, topo_of_split
from shapes import unrooted_shapes, canon_unrooted
from h3sat import build_cnf
n, k = int(sys.argv[1]), int(sys.argv[2])
qs, qid = quartet_index(n)
# caterpillar representative: find the shape whose canonical form is the caterpillar (max diameter)
shapes = unrooted_shapes(n)
def diam(adj):
    import collections
    def far(s):
        d = {s: 0}; dq = collections.deque([s])
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in d: d[y] = d[x] + 1; dq.append(y)
        m = max(d, key=d.get); return m, d[m]
    a, _ = far(0); b, L = far(a); return L
cat = max(shapes, key=diam)
T1q = tree_quartets(cat, n)
nv, cls, X, _ = build_cnf(n, k, T1q)
def pairings(S):
    if not S: yield []; return
    a = S[0]
    for i in range(1, len(S)):
        for rest in pairings(S[1:i] + S[i+1:]):
            yield [(a, S[i])] + rest
for S in itertools.combinations(range(n), 6):
    for P in pairings(list(S)):
        clause_lits = []
        for q in itertools.combinations(S, 4):
            full = [p for p in P if p[0] in q and p[1] in q]
            pair = full[0]
            t = topo_of_split(q, pair)
            clause_lits.append((qid[q], t))
        for t in range(k - 1):
            cls.append([-X[t][qi][tt] for qi, tt in clause_lits])
t0 = time.time()
with Solver(name='cadical153', bootstrap_with=cls) as s:
    r = s.solve()
print(f'caterpillars only: n={n} k={k} -> {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)')
