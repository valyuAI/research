"""Exact certificate of a Minkowski reorientation flex P_theta = S1 + R_theta S2 (standard library only).

Input: exact solid data (number field) and a set of edges claimed to form summand S1 (the rest form S2).
Checks (exact):
  1. every face's S1-edge vectors sum to zero;
  2. s1 (integrating S1 edges) is well defined, s2 = p - s1;
  3. for each face F, affine dimensions k1 = dim s1(F), k2 = dim s2(F);
  4. critical faces (one part 2-dimensional, the other of positive dimension) have pairwise parallel normals; the
     rotation axis l is their common normal (or a coordinate axis if there are no critical faces);
  5. non-triviality: some vertex pair (u, w) has d/dtheta |p_u - p_w|^2 = 2 <p_u - p_w, l x (s2_u - s2_w)> != 0.
Then for small theta, P_theta has the same faces (planarity by 3-4, strict convexity by continuity from the validated
strict convexity at theta = 0), the same edge lengths, and is not congruent to P: a flex."""
import json, sys
from fractions import Fraction
import nfsolid


def need(cond, msg='check failed'):
  """Explicit check that is not removed by python -O."""
  if not cond:
    raise ValueError(msg)


def rank_vectors(K, vecs):
  rows = [list(v) for v in vecs if not all(K.is0(x) for x in v)]
  r = 0
  m = [list(v) for v in rows]
  cols = 3
  for c in range(cols):
    piv = next((i for i in range(r, len(m)) if not K.is0(m[i][c])), None)
    if piv is None:
      continue
    m[r], m[piv] = m[piv], m[r]
    inv = K.inv(m[r][c])
    for i in range(len(m)):
      if i != r and not K.is0(m[i][c]):
        f = K.mul(m[i][c], inv)
        m[i] = [K.sub(a, K.mul(f, b)) for a, b in zip(m[i], m[r])]
    r += 1
  return r


def check(path, s1_edges):
  name, K, V, F = nfsolid.load(path)
  P, A, E, rep = nfsolid.validate(K, V, F)
  S1 = set(tuple(sorted(e)) for e in s1_edges)
  need(S1 <= set(E) and 0 < len(S1) < len(E), 'S1 <= set(E) and 0 < len(S1) < len(E)')
  vec = lambda a, b: K.vsub(P[b], P[a])
  zero3 = (K.zero, K.zero, K.zero)
  # 1. face closure of S1 parts
  for f in F:
    s = zero3
    for i in range(len(f)):
      a, b = f[i], f[(i + 1) % len(f)]
      if tuple(sorted((a, b))) in S1:
        s = tuple(K.add(x, y) for x, y in zip(s, vec(a, b)))
    if not all(K.is0(x) for x in s):
      return {'ok': False, 'reason': 'S1 part of a face does not close'}
  # 2. integrate s1
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
        d = vec(a, b) if tuple(sorted((a, b))) in S1 else zero3
        s1[b] = tuple(K.add(x, y) for x, y in zip(s1[a], d))
        stack.append(b)
  for a, b in E:
    d = vec(a, b) if (a, b) in S1 else zero3
    if not all(K.is0(x) for x in K.vsub(K.vsub(s1[b], s1[a]), d)):
      return {'ok': False, 'reason': 's1 not well defined'}
  s2 = {v: K.vsub(P[v], s1[v]) for v in range(len(P))}
  # 3. face dimensions; 4. admissible rotation axes.
  # A face F = F1 + F2 stays planar under rotation of S2 about l iff: (k1,k2) has a zero entry, or k1 = k2 = 1,
  # or (2,2): l is normal to F; (2,1): l normal to F or l parallel to the S2-edge; (1,2): l normal to F or l
  # parallel to the S1-edge.
  kinds = {}
  constraints = []  # list of candidate-direction lists, one per critical face
  for fi, f in enumerate(F):
    d1 = [K.vsub(s1[v], s1[f[0]]) for v in f]
    d2 = [K.vsub(s2[v], s2[f[0]]) for v in f]
    k1, k2 = rank_vectors(K, d1), rank_vectors(K, d2)
    kinds[(k1, k2)] = kinds.get((k1, k2), 0) + 1
    if k1 == 2 and k2 == 2:
      constraints.append([A[fi]])
    elif k1 == 2 and k2 == 1:
      e2 = next(x for x in d2 if not all(K.is0(c) for c in x))
      constraints.append([A[fi], e2])
    elif k1 == 1 and k2 == 2:
      e1 = next(x for x in d1 if not all(K.is0(c) for c in x))
      constraints.append([A[fi], e1])
  par = lambda u, v: all(K.is0(x) for x in K.cross(u, v))
  if constraints:
    axes = [c for c in constraints[0] if all(any(par(c, o) for o in opts) for opts in constraints)]
    if not axes:
      return {'ok': False, 'reason': 'no rotation axis compatible with all critical faces',
              'kinds': str(kinds), 'critical': len(constraints)}
  else:
    axes = [tuple(K.const(1 if i == j else 0) for i in range(3)) for j in range(3)]
  crit_normals = constraints
  # 5. non-triviality
  for l in axes:
    for u in range(len(P)):
      for w in range(u + 1, len(P)):
        der = K.dot(K.vsub(P[u], P[w]), K.cross(l, K.vsub(s2[u], s2[w])))
        if not K.is0(der):
          return {'ok': True, 'name': name, 'kinds': {str(k): v for k, v in kinds.items()},
                  'critical_faces': len(crit_normals), 'axis': [[str(c) for c in x] for x in l],
                  'witness_pair': [u, w], 'S1_edges': len(S1), 'S2_edges': len(E) - len(S1)}
  return {'ok': False, 'reason': 'all distance derivatives vanish (trivial)'}


if __name__ == '__main__':
  props = {}
  for fn in sys.argv[1:]:
    props.update(json.load(open(fn)))
  results = {}
  for k in sorted(props, key=int):
    E = props[k]['edges']
    out = None
    for part in props[k]['partitions']:
      s1 = [E[r] for r, bit in enumerate(part) if bit]
      out = check(f'data/J{int(k):02d}.json', s1)
      if out['ok']:
        break
    results[k] = out
    print(f"J{k}: {'FLEX' if out and out['ok'] else 'no Minkowski flex'} {out}", flush=True)
  json.dump(results, open('minkflex_results.json', 'w'), indent=1)
