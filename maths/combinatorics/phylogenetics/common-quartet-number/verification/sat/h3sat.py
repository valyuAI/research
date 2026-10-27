"""SAT search: k unrooted binary trees on n leaves with no common quartet.
T1 fixed to each unrooted shape (labelled arbitrarily); T2..Tk free, encoded by full quartet systems
with 5-point consistency (a necessary condition for tree-likeness; sufficiency is checked on decoding)."""
import itertools, sys, time, json
from qlib import quartet_index, five_patterns, tree_quartets
from shapes import unrooted_shapes

def build_cnf(n, k, T1q, enc='aux'):
    qs, qid = quartet_index(n)
    nq = len(qs)
    nv = [0]
    def new():
        nv[0] += 1; return nv[0]
    X = [[[new() for _ in range(3)] for _ in range(nq)] for _ in range(k - 1)]  # trees 2..k
    cls = []
    for t in range(k - 1):
        for q in range(nq):
            a, b, c = X[t][q]
            cls += [[a, b, c], [-a, -b], [-a, -c], [-b, -c]]
    pats = five_patterns()
    for S in itertools.combinations(range(n), 5):
        sub = {}
        for qpos in itertools.combinations(range(5), 4):
            sub[qpos] = qid[tuple(S[i] for i in qpos)]
        for t in range(k - 1):
            if enc == 'aux':
                ys = []
                for p in pats:
                    y = new(); ys.append(y)
                    for qpos, topo in p.items():
                        cls.append([-y, X[t][sub[qpos]][topo]])
                cls.append(ys)
            else:
                allowed = {tuple(p[qpos] for qpos in sorted(p)) for p in pats}
                keys = sorted(pats[0])
                for combo in itertools.product(range(3), repeat=5):
                    if combo not in allowed:
                        cls.append([-X[t][sub[qpos]][combo[i]] for i, qpos in enumerate(keys)])
    # no common quartet: for each q, not all trees agree with T1
    for q in range(nq):
        cls.append([-X[t][q][T1q[q]] for t in range(k - 1)])
    return nv[0], cls, X, qs

def decode(model, X, nq):
    s = set(l for l in model if l > 0)
    return [[[i for i in range(3) if X[t][q][i] in s][0] for q in range(nq)] for t in range(len(X))]

if __name__ == '__main__':
    from pysat.solvers import Solver
    n = int(sys.argv[1]); k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    solver_name = sys.argv[3] if len(sys.argv) > 3 else 'cadical153'
    shapes = unrooted_shapes(n)
    print(f'n={n} k={k} shapes={len(shapes)}', flush=True)
    results = []
    for si, adj in enumerate(shapes):
        T1q = tree_quartets(adj, n)
        t0 = time.time()
        nvars, cls, X, qs = build_cnf(n, k, T1q)
        with Solver(name=solver_name, bootstrap_with=cls) as S:
            r = S.solve()
            dt = time.time() - t0
            print(f'  shape {si+1}/{len(shapes)} vars={nvars} clauses={len(cls)} -> {"SAT" if r else "UNSAT"} ({dt:.1f}s)', flush=True)
            if r:
                sol = decode(S.get_model(), X, len(qs))
                results.append({'shape': si, 'adj': {str(a): b for a, b in adj.items()}, 'T1q': T1q, 'others': sol})
                break
    print('RESULT', 'SAT' if results else 'UNSAT-all-shapes', flush=True)
    if results:
        json.dump(results[0], open(f'sol_n{n}_k{k}.json', 'w'))
