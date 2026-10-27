"""Check that data/JNN.json is Johnson solid N (standard library only).

For a convex polyhedron with regular faces, every combinatorial automorphism is induced by an isometry (relabel
the vertices by the automorphism and apply Cauchy's rigidity theorem), so the order of the combinatorial
automorphism group equals the order of the full symmetry group. We compute it from the face lists (maps of
oriented darts, both orientations) and compare it with the known point group of each Johnson solid. For
pairs with equal symmetry order (ortho/gyro), we check that the faces' cyclic sequences of neighbour sizes
differ, and that the "ortho" member has like faces meeting across its equator (square-square and
triangle-triangle edges between the two caps)."""
import json, sys
from collections import Counter

ORDER = {  # |full symmetry group| from the point groups of the Johnson solids
  1: 8, 2: 10, 3: 6, 4: 8, 5: 10, 6: 10, 7: 6, 8: 8, 9: 10, 10: 8, 11: 10, 12: 12, 13: 20, 14: 12, 15: 16,
  16: 20, 17: 16, 18: 6, 19: 8, 20: 10, 21: 10, 22: 6, 23: 8, 24: 10, 25: 10, 26: 8, 27: 12, 28: 16, 29: 16,
  30: 20, 31: 20, 32: 10, 33: 10, 34: 20, 35: 12, 36: 12, 37: 16, 38: 20, 39: 20, 40: 10, 41: 10, 42: 20,
  43: 20, 44: 6, 45: 8, 46: 10, 47: 5, 48: 10, 49: 4, 50: 4, 51: 12, 52: 4, 53: 4, 54: 4, 55: 8, 56: 4,
  57: 12, 58: 10, 59: 20, 60: 4, 61: 6, 62: 4, 63: 6, 64: 6, 65: 6, 66: 8, 67: 16, 68: 10, 69: 20, 70: 4,
  71: 6, 72: 10, 73: 20, 74: 4, 75: 6, 76: 10, 77: 10, 78: 2, 79: 2, 80: 20, 81: 4, 82: 2, 83: 6, 84: 8,
  85: 16, 86: 4, 87: 2, 88: 4, 89: 4, 90: 8, 91: 8, 92: 6}


def oriented_faces(F):
  """Orient all faces coherently (each edge traversed once in each direction)."""
  F = [list(f) for f in F]
  out = [None] * len(F)
  out[0] = F[0]
  used = {(F[0][i], F[0][(i + 1) % len(F[0])]) for i in range(len(F[0]))}
  todo = True
  while todo:
    todo = False
    for i, f in enumerate(F):
      if out[i] is not None:
        continue
      ds = [(f[j], f[(j + 1) % len(f)]) for j in range(len(f))]
      if any((v, u) in used for u, v in ds):
        g = f
      elif any(d in used for d in ds):
        g = f[::-1]
      else:
        continue
      gd = [(g[j], g[(j + 1) % len(g)]) for j in range(len(g))]
      if any(d in used for d in gd):
        raise ValueError('face lists are not a coherently orientable surface')
      used.update(gd)
      out[i] = g
      todo = True
  if any(o is None for o in out):
    raise ValueError('face graph not connected')
  return out


def automorphism_count(F, nV):
  OF = oriented_faces(F)
  nxt = {}
  for f in OF:
    for i in range(len(f)):
      nxt[(f[i], f[(i + 1) % len(f)])] = (f[(i + 1) % len(f)], f[(i + 2) % len(f)])
  prv = {b: a for a, b in nxt.items()}
  darts = list(nxt)
  d0 = darts[0]
  count = 0
  for target in darts:
    for orient in (+1, -1):
      # orientation preserving: d -> t, next -> next ; reversing: d -> reverse(t), next(d) -> reverse(prev(t))
      start = target if orient > 0 else (target[1], target[0])
      mp, stack, ok = {d0: start}, [d0], True
      while stack and ok:
        d = stack.pop()
        t = mp[d]
        if orient > 0:
          pairs = ((nxt[d], nxt[t]), ((d[1], d[0]), (t[1], t[0])))
        else:
          # t is a reversed dart (u, v) of P read backwards: the face successor becomes the reversed predecessor
          tr = (t[1], t[0])
          p = prv[tr]
          pairs = (((nxt[d]), (p[1], p[0])), ((d[1], d[0]), tr))
        for a, b in pairs:
          if a in mp:
            if mp[a] != b:
              ok = False
              break
          else:
            mp[a] = b
            stack.append(a)
      if ok and len(mp) == len(darts):
        vm = {}
        for (u, v), (x, y) in mp.items():
          if vm.setdefault(u, x) != x:
            ok = False
            break
        if ok and len(set(vm.values())) == nV:
          count += 1
  return count


def neighbour_signature(F):
  e2f = {}
  for i, f in enumerate(F):
    for j in range(len(f)):
      e2f.setdefault(frozenset((f[j], f[(j + 1) % len(f)])), []).append(i)
  sig = Counter()
  for i, f in enumerate(F):
    nb = [len(F[[g for g in e2f[frozenset((f[j], f[(j + 1) % len(f)]))] if g != i][0]]) for j in range(len(f))]
    rots = [tuple(nb[s:] + nb[:s]) for s in range(len(nb))]
    sig[(len(f), min(rots + [r[::-1] for r in rots]))] += 1
  return sig


if __name__ == '__main__':
  bad = []
  sigs = {}
  for k in range(1, 93):
    d = json.load(open('data/J%02d.json' % k))
    F = d['faces']
    a = automorphism_count(F, len(d['vertices']))
    sigs[k] = (a, tuple(sorted(neighbour_signature(F).items())))
    ok = a == ORDER[k]
    print('J%-3d %-44s |Aut| = %-3d expected %-3d %s' % (k, d['name'][:44], a, ORDER[k], 'ok' if ok else 'MISMATCH'),
          flush=True)
    if not ok:
      bad.append(k)
  # ortho/gyro: like faces meet across the equator in the ortho member
  def like_edges(F):
    e2f = {}
    for i, f in enumerate(F):
      for j in range(len(f)):
        e2f.setdefault(frozenset((f[j], f[(j + 1) % len(f)])), []).append(len(f))
    return sum(1 for v in e2f.values() if v[0] == v[1] and v[0] in (3, 5)) + \
      sum(1 for v in e2f.values() if v == [4, 4])
  def aligned_belt(F):  # a belt square whose opposite neighbours have equal non-square sizes (3,4,3,4)/(5,4,5,4)
    return any(sz == 4 and seq[0] == seq[2] and seq[0] != 4 and seq[1] == seq[3] == 4
               for (sz, seq), c in neighbour_signature(F).items())
  for ortho, gyro, test in [(28, 29, like_edges), (30, 31, like_edges), (35, 36, aligned_belt),
                            (38, 39, aligned_belt), (42, 43, aligned_belt)]:
    Fo = json.load(open('data/J%02d.json' % ortho))['faces']
    Fg = json.load(open('data/J%02d.json' % gyro))['faces']
    vo, vg = test(Fo), test(Fg)
    ok = (vo > vg) if test is like_edges else (vo and not vg)
    print('ortho J%d vs gyro J%d (%s): %s vs %s -> %s' % (ortho, gyro, test.__name__, vo, vg, 'ok' if ok else 'SWAPPED?'))
    if not ok:
      bad.append((ortho, gyro))
  same = [(i, j) for i in sigs for j in sigs if i < j and sigs[i] == sigs[j]]
  print('pairs with identical invariants (automorphism order and neighbour signatures):', same)
  print('LABELS CONSISTENT' if not bad and not same else 'CHECK FAILED: %s %s' % (bad, same))
  sys.exit(1 if bad or same else 0)
