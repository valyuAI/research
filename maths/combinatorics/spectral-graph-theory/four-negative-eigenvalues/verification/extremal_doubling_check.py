"""For k = 1..4: the reduced graphs with exactly k negative eigenvalues and 2^{k+1} - 2 vertices, compared
with the doubling words kappa^{k-1-j} kappa'^j (K2) (kappa = Kotlov-Lovasz step, kappa' = variant with the
pendant vertex also joined to V; see order30_check.py and Section 6 of the paper).

For each k, enumerates all maximum compatible cliques over all nonsingular bases of rank 2k with n^- = k
(classify_max_order.graphs_for_basis), merges isomorphic graphs (nauty), and matches each class to the
words of length k-1. Expected: exactly k classes, matched one-to-one by the words with all kappa' first.

Usage: python extremal_doubling_check.py
"""
import itertools, os, sys, time
import numpy as np
from classify_max_order import graphs_for_basis
from max_reduced_order import load
from enumerate_nonsingular import cert, OUT
from order30_check import step


def main():
  ok = True
  for k in (1, 2, 3, 4):
    rank, target = 2 * k, 2 ** (k + 1) - 2
    bases = [A for (A, p, q) in load(os.path.join(OUT, 'ns_k4', f'order{rank}.txt'), rank) if q == k]
    classes = {}
    last_progress = time.monotonic()
    for done, A in enumerate(bases, 1):
      if time.monotonic() - last_progress >= 15:
        print(f'k={k}: {done}/{len(bases)} bases checked', flush=True)
        last_progress = time.monotonic()
      if target == rank:  # k = 1: the basis itself, with no further compatible vectors
        if not graphs_for_basis(A, target + 1):
          classes.setdefault(cert(A), A)
      for G in graphs_for_basis(A, target):
        classes.setdefault(cert(G), G)
    words = {}
    for seq in itertools.product((True, False), repeat=k - 1):
      M = [[0, 1], [1, 0]]
      for s in seq:
        M = step(M, s, True)
      words.setdefault(cert(np.array(M, dtype=np.int8)), []).append(''.join("k'" if s else 'k' for s in seq) or 'K2')
    match = [words.get(c, []) for c in classes]
    good = len(classes) == k and all(len(m) == 1 for m in match)
    ok = ok and good
    print(f'k={k}: order {target}, {len(bases)} bases of rank {rank}, {len(classes)} classes; '
          f'words (applied left to right) {match}; {"OK" if good else "MISMATCH"}', flush=True)
  print('ALL OK' if ok else 'FAILED', flush=True)
  sys.exit(0 if ok else 1)


if __name__ == '__main__':
  main()
