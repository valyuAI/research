"""Symmetric search: T_{i+1} = sigma^i(T_1), i=0..k-1, for a permutation sigma of [n]. One free tree T1.
Usage: symsat.py n k "cycle-type" [solver]   e.g. symsat.py 13 3 3,3,3,3,1"""
import sys, itertools, time, json
from pysat.solvers import Solver
from qlib import quartet_index, five_patterns, tree_quartets, topo_of_split
from recon import reconstruct
n, k = int(sys.argv[1]), int(sys.argv[2])
ctype = [int(x) for x in sys.argv[3].split(',')]
assert sum(ctype) == n
solver_name = sys.argv[4] if len(sys.argv) > 4 else 'cadical153'
# build sigma
sigma = {}; start = 0
for c in ctype:
    for i in range(c): sigma[start + i] = start + (i + 1) % c
    start += c
qs, qid = quartet_index(n)
nq = len(qs)
X = [[1 + 3 * q + t for t in range(3)] for q in range(nq)]
nv = 3 * nq
cls = []
for q in range(nq):
    a, b, c = X[q]; cls += [[a, b, c], [-a, -b], [-a, -c], [-b, -c]]
pats = five_patterns()
for S in itertools.combinations(range(n), 5):
    ys = []
    for p in pats:
        nv += 1; y = nv; ys.append(y)
        for qpos, topo in p.items():
            cls.append([-y, X[qid[tuple(S[i] for i in qpos)]][topo]])
    cls.append(ys)
def pair_of(q, t):
    a, b, c, d = q
    return [(a, b), (a, c), (a, d)][t]
def image(q, t, perm):
    """split t on q mapped by perm -> (q', t')"""
    x, y = pair_of(q, t)
    q2 = tuple(sorted(perm[v] for v in q))
    return qid[q2], topo_of_split(q2, (perm[x], perm[y]))
powers = [{v: v for v in range(n)}]
for i in range(1, k):
    prev = powers[-1]; powers.append({v: sigma[prev[v]] for v in range(n)})
inv = [{p[v]: v for v in range(n)} for p in powers]
# T_{i}(Q) = sigma^i (T1(sigma^{-i} Q)). Common split t on Q in all trees: T1 has split inv_i(t) on inv_i(Q) for all i.
for q in range(nq):
    for t in range(3):
        lits = set()
        for i in range(k):
            q2, t2 = image(qs[q], t, inv[i])
            lits.add(-X[q2][t2])
        cls.append(sorted(lits))
t0 = time.time()
with Solver(name=solver_name, bootstrap_with=cls) as S:
    r = S.solve()
    print(f'sym n={n} k={k} type={ctype}: {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s, vars {nv}, clauses {len(cls)})', flush=True)
    if r:
        m = set(l for l in S.get_model() if l > 0)
        T1q = [[t for t in range(3) if X[q][t] in m][0] for q in range(nq)]
        T1 = reconstruct(T1q, n)
        assert T1 is not None
        trees = []
        for i in range(k):
            P = powers[i]
            # relabel leaves of T1 by P; internal nodes shifted to avoid clashes
            A = {}
            for v, nb in T1.items():
                f = lambda u: P[u] if u < n else u
                A[f(v)] = [f(u) for u in nb]
            trees.append(A)
        Q = [tree_quartets(t, n) for t in trees]
        common = sum(1 for qq in range(nq) if len({Q[i][qq] for i in range(k)}) == 1)
        print('verified common quartets:', common, flush=True)
        json.dump([{str(a): b for a, b in t.items()} for t in trees], open(f'symsol_n{n}_k{k}.json', 'w'))
