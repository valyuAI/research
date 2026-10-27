"""Checker 1 (standard library only): exact validation of every Johnson solid in data/ and the rank of its
point-hyperplane rigidity matrix (arXiv:2607.09252, Section 3) modulo a prime.

Validation (nfsolid.validate, exact arithmetic in the coordinate field): Sturm-certified real embedding, unit
edges, planar faces, regular faces, strict convexity, Euler characteristic, each edge in exactly two faces.
Rank: entries are reduced by a ring map Z_(p)[theta] -> F_p (theta -> root of the minimal polynomial mod p;
for towers also sqrt(w) -> a square root of w mod p). Because the coordinate field is a field (minimal polynomial
irreducible: check_irreducible.py; tower radicand a non-square: tower.py), every minor that vanishes over the
reals vanishes mod p, so rank_p <= rank. Hence flex_dim <= cols - 6 - rank_p, and rank_p = cols - 6 proves
first-order rigidity (corank 6 = trivial motions only, Cor. 3.2 of arXiv:2607.09252)."""
import glob, json, sys, time
import nfsolid

if __name__ == '__main__':
  files = sorted(glob.glob('data/J*.json'))
  if len(sys.argv) > 1:
    files = [f for f in files if int(f[6:8]) in [int(a) for a in sys.argv[1:]]]
  res = {}
  for f in files:
    k = int(f[6:8])
    t0 = time.time()
    name, K, V, F = nfsolid.load(f)
    P, A, E, rep = nfsolid.validate(K, V, F)
    p, t = nfsolid.find_prime(K, P, A)
    rk, nrows, ncols = nfsolid.rigidity_rank_mod_p(K, P, A, E, F, p, t)
    res[k] = dict(name=name, field_degree=K.n, tower=hasattr(K, 'K'), prime=p, root=str(t), rank_mod_p=rk,
                  rows=nrows, cols=ncols, flex_dim_upper_bound=ncols - rk - 6, **rep)
    if hasattr(K, 'K'):
      res[k]['radicand_nonsquare_certificate'] = K.nonsquare_certificate
    print('J%-3d %-42s deg %2d p=%d rank_p=%d cols=%d -> flex <= %d  (%.1fs)'
          % (k, name[:42], K.n, p, rk, ncols, ncols - rk - 6, time.time() - t0), flush=True)
  out = 'results/check1_rank.json' if len(sys.argv) == 1 else 'results/check1_rank_partial.json'
  json.dump(res, open(out, 'w'), indent=1)
  rigid = sorted(k for k in res if res[k]['flex_dim_upper_bound'] == 0)
  print('%d solids, %d first-order rigid: %s' % (len(res), len(rigid), rigid))
