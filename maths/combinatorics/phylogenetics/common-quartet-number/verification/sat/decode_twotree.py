"""Decode a kissat model of a twotree.py instance, rebuild T2, and brute-force check (sep_check) that the
pair (T1, T2) has no separated pair of sizes (s,t). Usage: decode_twotree.py n s t shape model"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from shapes import unrooted_shapes
from qlib import quartet_index
from recon import reconstruct
from export_sym import newick
from sep_check import best
n, s, t, si, model = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
qs, _ = quartet_index(n)
lits = set()
for line in open(model):
    if line.startswith('v '): lits.update(int(x) for x in line[2:].split() if int(x) > 0)
q2 = [[i for i in range(3) if 1 + 3 * q + i in lits][0] for q in range(len(qs))]
T2 = reconstruct(q2, n)
assert T2 is not None
T1 = unrooted_shapes(n)[si]
a, b = newick(T1, n), newick(T2, n)
print(a); print(b)
print('separated (%d,%d) pair found by brute force:' % (s, t), best(a, b, s, t))
