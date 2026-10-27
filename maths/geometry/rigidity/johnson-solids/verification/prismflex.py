"""Exact structural certificate for the augmented prisms J49, J52-J57 (standard library only).

Checks that P is a right n-prism (two parallel regular n-gon faces B and T = B + h, |h| = 1, h orthogonal to them,
n lateral unit squares) together with square pyramids erected on some lateral squares (each apex adjacent exactly to
the 4 square vertices, 4 triangles, the square itself not a face).  Flex lemma (see paper):
  n >= 4: deform B within its plane through convex equilateral n-gons (an (n-3)-parameter family); every lateral face
          stays a unit square, so each pyramid can follow its square rigidly.
  n == 3: rotate h about the common direction of the horizontal edges of the augmented squares (requires all
          augmented squares to have parallel horizontal edges); those squares stay unit squares.
"""
import sys, json
import nfsolid


def check(path):
  name, K, V, F = nfsolid.load(path)
  P, A, E, rep = nfsolid.validate(K, V, F)
  m = max(len(f) for f in F)
  apex_like = [v for v in range(len(P)) if all(len(f) == 3 for f in F if v in f)]
  if m >= 5:
    capf = [f for f in F if len(f) == m]
  else:
    capf = [f for f in F if len(f) == 3 and not any(v in apex_like for v in f)]
  if len(capf) != 2:
    return {'ok': False, 'reason': 'could not identify the two caps', 'caps': len(capf)}
  Bf, Tf = capf
  n = len(Bf)
  Bs, Ts = set(Bf), set(Tf)
  # lateral edges: edges between B and T
  lat = [(a, b) if a in Bs else (b, a) for a, b in E if (a in Bs and b in Ts) or (a in Ts and b in Bs)]
  if len(lat) != n:
    return {'ok': False, 'reason': 'lateral edges'}
  h = K.vsub(P[lat[0][1]], P[lat[0][0]])
  for a, b in lat:
    if not all(K.is0(x) for x in K.vsub(K.vsub(P[b], P[a]), h)):
      return {'ok': False, 'reason': 'lateral edges not translates'}
  # h orthogonal to the cap plane
  for i in range(n):
    e = K.vsub(P[Bf[(i + 1) % n]], P[Bf[i]])
    if not K.is0(K.dot(e, h)):
      return {'ok': False, 'reason': 'not a right prism'}
  apices = [v for v in range(len(P)) if v not in Bs and v not in Ts]
  aug_edges = []
  for apx in apices:
    nb = sorted({b for a, b in E if a == apx} | {a for a, b in E if b == apx})
    if len(nb) != 4:
      return {'ok': False, 'reason': 'apex degree'}
    nbB = [v for v in nb if v in Bs]
    if len(nbB) != 2:
      return {'ok': False, 'reason': 'apex not over a lateral square'}
    # the two B-neighbours are consecutive on B, and the other two neighbours are their translates by h
    i0, i1 = Bf.index(nbB[0]), Bf.index(nbB[1])
    if (i1 - i0) % n not in (1, n - 1):
      return {'ok': False, 'reason': 'apex B-neighbours not adjacent'}
    nbT = [v for v in nb if v in Ts]
    trans = sorted(v for v in nbT if any(all(K.is0(x) for x in K.vsub(K.vsub(P[v], P[u]), h)) for u in nbB))
    if len(nbT) != 2 or len(trans) != 2:
      return {'ok': False, 'reason': 'apex T-neighbours are not the translates of its B-neighbours'}
    aug_edges.append(K.vsub(P[nbB[1]], P[nbB[0]]))
    # the square itself must not be a face, the 4 triangles must be faces
    tris = [f for f in F if apx in f]
    if len(tris) != 4 or any(len(f) != 3 for f in tris):
      return {'ok': False, 'reason': 'apex faces'}
  out = {'ok': True, 'name': name, 'n': n, 'augmented': len(apices)}
  if n >= 4:
    out['flex'] = 'polygon flex of the regular %d-gon (dimension %d), all lateral squares preserved' % (n, n - 3)
    return out
  # n == 3: need common direction of augmented horizontal edges
  for e in aug_edges[1:]:
    if not all(K.is0(x) for x in K.cross(aug_edges[0], e)):
      return {'ok': False, 'reason': 'augmented squares not parallel; tilt flex unavailable', 'n': n}
  out['flex'] = 'tilt of h about the augmented squares horizontal edge direction'
  return out


if __name__ == '__main__':
  res = {}
  for k in [int(a) for a in sys.argv[1:]]:
    res[k] = check(f'data/J{k:02d}.json')
    print(f'J{k}: {res[k]}', flush=True)
  json.dump(res, open('prismflex_results.json', 'w'), indent=1)
