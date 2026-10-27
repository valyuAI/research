"""Two-tree separation lemma at size n with parameters (s, t, z): for T1 = shape representative and T2 free,
the CNF says T2 is a tree (quartet system with 5-point consistency) and NO pair (X, Y) with |X| = s, |Y| = t
or |X| = t, |Y| = s, X on one side and Y on the other side of an edge of T1, is separated by an edge of T2
(i.e. for every such (X, Y) some cross quartet xx'|yy' fails in T2).
UNSAT for every shape  <=>  every two trees on n leaves have such a separated pair.
Usage: twotree.py n s t shape_idx out.cnf"""
import sys, itertools, collections
from qlib import quartet_index, five_patterns, tree_quartets, topo_of_split
from shapes import unrooted_shapes

def splits(adj, n):
    """leaf bipartitions induced by the edges of adj"""
    out = []
    for u in adj:
        for v in adj[u]:
            if u < v:
                # leaves on v's side when edge u-v removed
                seen = {u, v}; st = [v]; side = set()
                while st:
                    x = st.pop()
                    if x < n: side.add(x)
                    for y in adj[x]:
                        if y not in seen: seen.add(y); st.append(y)
                out.append((frozenset(side), frozenset(set(range(n)) - side)))
    return out

def build(n, s, t, adj):
    qs, qid = quartet_index(n)
    nq = len(qs)
    X = [[1 + 3 * q + i for i in range(3)] for q in range(nq)]
    nv = 3 * nq; cls = []
    for q in range(nq):
        a, b, c = X[q]; cls += [[a, b, c], [-a, -b], [-a, -c], [-b, -c]]
    for S in itertools.combinations(range(n), 5):
        ys = []
        for p in five_patterns():
            nv += 1; ys.append(nv)
            for qpos, topo in p.items():
                cls.append([-nv, X[qid[tuple(S[i] for i in qpos)]][topo]])
        cls.append(ys)
    seen = set()
    for P, Q in splits(adj, n):
        for (A, B) in ((P, Q), (Q, P)):
            for sx, sy in ((s, t), (t, s)):
                for Xs in itertools.combinations(sorted(A), sx):
                    for Ys in itertools.combinations(sorted(B), sy):
                        key = (frozenset(Xs), frozenset(Ys))
                        rkey = (key[1], key[0])
                        if key in seen or rkey in seen: continue
                        seen.add(key)
                        lits = []
                        for x1, x2 in itertools.combinations(Xs, 2):
                            for y1, y2 in itertools.combinations(Ys, 2):
                                q = tuple(sorted((x1, x2, y1, y2)))
                                lits.append(-X[qid[q]][topo_of_split(q, (x1, x2))])
                        cls.append(lits)
    return nv, cls

if __name__ == '__main__':
    n, s, t, si, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    adj = unrooted_shapes(n)[si]
    nv, cls = build(n, s, t, adj)
    with open(out, 'w') as f:
        f.write(f'c twotree n={n} s={s} t={t} shape={si}\np cnf {nv} {len(cls)}\n')
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    print(nv, len(cls))
