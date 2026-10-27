"""Independent encoding of the two-tree separation lemma (shares no code with ../twotree.py, ../qlib.py,
../shapes.py). Standard library only.

Statement checked for leaf number n and sizes (s, t): for every unrooted binary tree T1 on [n] (one labelled
representative per shape, shapes enumerated by leaf insertion) there is no tree T2 such that no pair X, Y
(|X| = s, |Y| = t or vice versa) separated by an edge of T1 is separated by an edge of T2.
T2 is encoded by one-hot quartet variables; every non-tree 5-leaf pattern (computed by brute force from the
15 labelled 5-leaf trees) is forbidden by a direct clause; separation in T2 is expressed through all cross
quartets xx'|yy'.
Usage: indep_twotree.py n s t out_prefix [shape_index]  -> writes out_prefix_<i>.cnf for every shape i
(or only the given one); prints the number of shapes."""
import sys, itertools
from indep_cnf import all_labelled_trees, quartet_vector, shapes_by_insertion, adjacency

def leaf_bipartitions(edges, n):
    adj = adjacency(edges)
    res = set()
    for (u, v) in edges:
        comp = {v}; stack = [v]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y != u and y not in comp and not (x == v and y == u):
                    comp.add(y); stack.append(y)
        side = frozenset(x for x in comp if isinstance(x, int) and x < n)
        other = frozenset(range(n)) - side
        res.add(frozenset([side, other]))
    return [tuple(p) for p in res]

def main():
    n, s, t, prefix = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    only = int(sys.argv[5]) if len(sys.argv) > 5 else None
    five = {tuple(quartet_vector(tr, 5)) for tr in all_labelled_trees(5)}
    assert len(five) == 15
    bad = [p for p in itertools.product(range(3), repeat=5) if p not in five]
    quarts = list(itertools.combinations(range(n), 4)); qpos = {q: i for i, q in enumerate(quarts)}
    var = lambda q, k: 1 + 3 * q + k
    nvars = 3 * len(quarts)
    base = []
    for q in range(len(quarts)):
        a, b, c = var(q, 0), var(q, 1), var(q, 2)
        base += [(a, b, c), (-a, -b), (-a, -c), (-b, -c)]
    for S in itertools.combinations(range(n), 5):
        qi = [qpos[tuple(S[j] for j in sub)] for sub in itertools.combinations(range(5), 4)]
        for p in bad:
            base.append(tuple(-var(qi[j], p[j]) for j in range(5)))
    def split_index(q, pair):
        # q sorted 4-tuple; index 0: q0q1|q2q3, 1: q0q2|q1q3, 2: q0q3|q1q2
        other = [x for x in q if x != q[0]]
        mate = pair[1] if pair[0] == q[0] else (pair[0] if pair[1] == q[0] else None)
        if mate is None:
            mate = [x for x in q if x not in pair]
            mate = mate[1] if mate[0] == q[0] else mate[0]
        return other.index(mate)
    shapes = shapes_by_insertion(n)
    for si, t1 in enumerate(shapes):
        if only is not None and si != only: continue
        cls = list(base)
        done = set()
        for side_a, side_b in leaf_bipartitions(t1, n):
            for A, B in ((side_a, side_b), (side_b, side_a)):
                for sx, sy in ((s, t), (t, s)):
                    if len(A) < sx or len(B) < sy: continue
                    for X in itertools.combinations(sorted(A), sx):
                        for Y in itertools.combinations(sorted(B), sy):
                            key = frozenset([frozenset(X), frozenset(Y)])
                            if key in done: continue
                            done.add(key)
                            c = []
                            for x1, x2 in itertools.combinations(X, 2):
                                for y1, y2 in itertools.combinations(Y, 2):
                                    q = tuple(sorted((x1, x2, y1, y2)))
                                    c.append(-var(qpos[q], split_index(q, (x1, x2))))
                            cls.append(tuple(c))
        with open(f'{prefix}_{si:03d}.cnf', 'w') as f:
            f.write(f'p cnf {nvars} {len(cls)}\n')
            for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    print(len(shapes))

if __name__ == '__main__':
    main()
