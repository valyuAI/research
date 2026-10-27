"""Exact dimension of the first-order flex space (corank of the point-hyperplane rigidity matrix minus 6) for the
51 first-order flexible Johnson solids, by exact Gaussian elimination over the coordinate field (exactlin).
Standard library only. Writes results/exact_flex_dims.json."""
import json, sys, time
import nfsolid, exactlin
from check_second_order import rigidity_rows
from gen_flex_vectors import FLEXIBLE

if __name__ == '__main__':
  ks = [int(a) for a in sys.argv[1:]] or FLEXIBLE
  fn = 'results/exact_flex_dims.json'
  try:
    res = json.load(open(fn))
  except FileNotFoundError:
    res = {}
  for k in ks:
    t0 = time.time()
    name, K, V, F = nfsolid.load('data/J%02d.json' % k)
    P, A, E, rep = nfsolid.validate(K, V, F)
    rows, inc, n = rigidity_rows(K, P, A, E, F)
    rk = exactlin.rank(K, rows, n)
    res[str(k)] = {'name': name, 'cols': n, 'exact_rank': rk, 'flex_dim': n - 6 - rk}
    print('J%d %s: exact rank %d of %d -> flex dim %d (%.0fs)' % (k, name, rk, n, n - 6 - rk, time.time() - t0),
          flush=True)
    json.dump(res, open(fn, 'w'), indent=1)
