"""Write DIMACS CNF for (n, k, shape index). Usage: write_cnf.py n k shape_idx out.cnf [enc]"""
import sys
from qlib import tree_quartets
from shapes import unrooted_shapes
from h3sat import build_cnf
n, k, si, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
enc = sys.argv[5] if len(sys.argv) > 5 else 'aux'
adj = unrooted_shapes(n)[si]
T1q = tree_quartets(adj, n)
nv, cls, X, qs = build_cnf(n, k, T1q, enc)
with open(out, 'w') as f:
    f.write(f'c n={n} k={k} shape={si} enc={enc}\n')
    f.write(f'p cnf {nv} {len(cls)}\n')
    for c in cls:
        f.write(' '.join(map(str, c)) + ' 0\n')
