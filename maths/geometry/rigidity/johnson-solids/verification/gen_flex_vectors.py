"""Generate explicit exact first-order flexes (vertex velocities) for the 51 first-order flexible Johnson solids.
Writes certificates/flex_vectors.json, which check2_independent.py verifies independently.

  * Minkowski-reorientation solids (certificates/minkowski_partitions.json + results/flex_finite.json):
    v_i = l x s2_i, where s2 is the S2-summand vertex and l the rotation axis (derivative of S1 + R_t S2).
  * all others (augmented prisms, J58-J60, J81-J83): a kernel vector of the exact point-hyperplane rigidity
    matrix (exactlin) that is not a trivial motion; vertex part only.
Untrusted generator: correctness is established by check2_independent.py."""
import json, sys
import nfsolid, exactlin
from check_second_order import rigidity_rows, trivial_motions

FLEXIBLE = [3, 4, 5, 7, 8, 9, 14, 15, 16, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 35, 36, 37, 38, 39, 40, 41, 42, 43,
            49, 52, 53, 54, 55, 56, 57, 58, 59, 60, 67, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]


def ser(K, x):
  if hasattr(K, 'K'):
    return [[str(c) for c in x[0]], [str(c) for c in x[1]]]
  return [str(c) for c in x]


def minkowski_velocities(K, P, E, s1_edges, axis):
  S1 = set(tuple(sorted(e)) for e in s1_edges)
  zero3 = (K.zero, K.zero, K.zero)
  adj = {}
  for a, b in E:
    adj.setdefault(a, []).append(b)
    adj.setdefault(b, []).append(a)
  s1 = {0: zero3}
  stack = [0]
  while stack:
    a = stack.pop()
    for b in adj[a]:
      if b not in s1:
        d = K.vsub(P[b], P[a]) if tuple(sorted((a, b))) in S1 else zero3
        s1[b] = tuple(K.add(x, y) for x, y in zip(s1[a], d))
        stack.append(b)
  return [K.cross(axis, K.vsub(P[v], s1[v])) for v in range(len(P))]


def kernel_velocities(K, P, A, E, F):
  rows, inc, n = rigidity_rows(K, P, A, E, F)
  ker, rk = exactlin.nullspace(K, rows, n)
  T = trivial_motions(K, P, A)
  for v in ker:
    if exactlin.rank(K, T + [v], n) == 7:
      return [tuple(v.get(3 * i + k, K.zero) for k in range(3)) for i in range(len(P))], len(ker) - 6
  raise ValueError('no non-trivial kernel vector')


if __name__ == '__main__':
  parts = json.load(open('certificates/minkowski_partitions.json'))
  finite = json.load(open('results/flex_finite.json'))
  ks = [int(a) for a in sys.argv[1:]] or FLEXIBLE
  try:
    out = json.load(open('certificates/flex_vectors.json'))
  except FileNotFoundError:
    out = {}
  for k in ks:
    name, K, V, F = nfsolid.load('data/J%02d.json' % k)
    P, A, E, rep = nfsolid.validate(K, V, F)
    fin = finite.get(str(k), {})
    if fin.get('type') == 'minkowski':
      axis = tuple(nfsolid.conv_elem(c, K) for c in fin['axis'])
      vel = minkowski_velocities(K, P, E, fin['S1_edges'], axis)
      how = 'minkowski: l x s2'
    else:
      vel, dim = kernel_velocities(K, P, A, E, F)
      how = 'exact kernel vector (flex space dim %d)' % dim
    out[str(k)] = {'name': name, 'source': how, 'velocities': [[ser(K, c) for c in v] for v in vel]}
    print('J%d %s: %s' % (k, name, how), flush=True)
    json.dump(out, open('certificates/flex_vectors.json', 'w'))
