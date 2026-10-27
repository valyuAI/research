# Verification

`check_colless.py` (standard library only):

1. For f(n) = n+1, 2^n, n!+1, n^3+1 and the (n+1)-th prime, finds two different level-outdegree words w, w' with equal f-size of the fully symmetric trees FS_w, FS_w', computing the f-size both by the closed formula and by building the trees and summing f over all vertices. It then forms the tree whose root has children FS_w and FS_w', checks that it is not fully symmetric, and evaluates the Colless-like index for D = variance (exact rationals), standard deviation and mean deviation from the median: all three are 0.
2. For random integer weights in 0..50 at outdegrees 0, 2, 3, 4, prints the least m for which the counting inequality (3m)!/(m!)^3 > M 24^m + 1 of the proof holds (M = max of f(2), f(3), f(4); f(0) plays no role).

Run: `python3 check_colless.py` (a few seconds). Expected last line: `OK`.

The theorem itself is proved in `paper.tex`; the script only illustrates it and tests the f-size formula.
