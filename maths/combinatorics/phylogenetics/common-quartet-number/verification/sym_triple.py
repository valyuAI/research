#!/usr/bin/env python3
"""Standard-library check of the 13-leaf construction: builds sigma T and sigma^2 T from T by relabelling,
prints the three Newick strings and the number of common quartets (expected 0)."""
import re
from check_family import check
T = "(1,(3,6),(((7,9),(4,(5,12))),((10,11),(2,(8,13)))));"
sigma = {1: 2, 2: 3, 3: 1, 4: 5, 5: 6, 6: 4, 7: 8, 8: 9, 9: 7, 10: 11, 11: 12, 12: 10, 13: 13}
relabel = lambda s: re.sub(r'\d+', lambda m: str(sigma[int(m.group())]), s)
trees = [T, relabel(T), relabel(relabel(T))]
assert relabel(trees[2]) == T  # sigma has order 3
for t in trees: print(t)
n, k, common = check(trees)
print(f'{k} trees on {n} leaves; common quartets: {len(common)}')
assert len(common) == 0
