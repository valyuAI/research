"""Exact check of the subdivision step on K4 (standard library only).

Subdivide the edge {0, 1} of the complete four-state digraph by a new state 4,
with rates W(4->0) = W(4->1) = 1, W(0->4) = 2 W(0->1), W(1->4) = 2 W(1->0) and all
other rates as in k4_no_coupling_certificate.json. Contracting state 4 maps every
arborescence of the subdivided graph rooted at j in {0,1,2,3} to an arborescence
of K4 rooted at j. This script checks, in exact arithmetic, that

1. the push-forward of each root law of the subdivided graph is the K4 root law;
2. contraction maps every uniquely constructable family of the subdivided graph
   (roots 0..3) to a uniquely constructable family of K4, as Lemma 5.2(c) states;
3. the lifted certificate y'(j, T) = y(j, contraction of T) for j <= 3 and
   y'(4, T) = 0 is nonnegative on every uniquely constructable family of the
   subdivided graph (24^5 families are enumerated);
4. its expectation under the root laws is the negative K4 value.

So no coherent coupling exists on the subdivided K4 either, as the suppression
lemma of the paper predicts.

Run: python3 -B check_k4_subdivision.py   (about a minute)
"""

import itertools
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

X = 4
VERTS = range(5)


def load_k4():
  cert = json.loads(Path(__file__).with_name('k4_no_coupling_certificate.json').read_text())
  rates = {}
  for key, val in cert['rates'].items():
    u, v = key.split('->')
    rates[(int(u), int(v))] = int(val)
  y = {}
  for key, val in cert['y'].items():
    head, body = key.split(':')
    r = int(head.replace('root', ''))
    arcs = tuple(sorted((int(a.split('>')[0]), int(a.split('>')[1])) for a in body.split(',')))
    y[(r, arcs)] = int(val)
  return rates, y, Fraction(cert['b_dot_y'])


def arborescences(arcs, root):
  out = {v: [b for (a, b) in arcs if a == v] for v in VERTS}
  others = [v for v in VERTS if v != root]
  trees = []
  for targets in itertools.product(*[out[v] for v in others]):
    nxt = dict(zip(others, targets))
    ok = True
    for v in others:
      u, steps = v, 0
      while u != root and steps <= len(others):
        u, steps = nxt[u], steps + 1
      if u != root:
        ok = False
        break
    if ok:
      trees.append(tuple(sorted(nxt.items())))
  return trees


def contract(tree):
  """Map an arborescence of the subdivided graph (root != X) to one of K4."""
  nxt = dict(tree)
  ins = [u for u, v in tree if v == X]
  out = {}
  for u, v in tree:
    if u == X:
      continue
    if v == X:
      out[u] = nxt[X]  # u -> X -> w becomes u -> w
    else:
      out[u] = v
  assert len(ins) <= 1
  return tuple(sorted(out.items()))


def main():
  start = time.time()
  k4_rates, y, stored = load_k4()
  rates = {a: w for a, w in k4_rates.items() if set(a) != {0, 1}}
  rates[(X, 0)] = 1
  rates[(X, 1)] = 1
  rates[(0, X)] = 2 * k4_rates[(0, 1)]
  rates[(1, X)] = 2 * k4_rates[(1, 0)]
  arcs = sorted(rates)
  index = {a: i for i, a in enumerate(arcs)}
  k4_arcs = sorted(k4_rates)

  def weight(tree, rate_map):
    w = 1
    for arc in tree:
      w *= rate_map[arc]
    return w

  trees = {r: arborescences(arcs, r) for r in VERTS}

  # 1. push-forward of the root laws
  pushforward_ok = True
  for r in range(4):
    total = sum(weight(t, rates) for t in trees[r])
    image = Counter()
    for t in trees[r]:
      image[contract(t)] += weight(t, rates)
    k4_total = 0
    for t, w in image.items():
      k4_w = weight(t, k4_rates)
      k4_total += k4_w
      if w != 2 * k4_w:
        pushforward_ok = False
    if total != 2 * k4_total or len(image) != 16:
      pushforward_ok = False
  print('pushforward of root laws equals K4 laws:', pushforward_ok, flush=True)

  # 2. enumerate all families; arc counts are <= 5 so base 6 codes add without carries
  code = {r: [sum(6 ** index[a] for a in t) for t in trees[r]] for r in VERTS}
  yval = {r: [y[(r, contract(t))] if r != X else 0 for t in trees[r]] for r in VERTS}
  sizes = [len(trees[r]) for r in VERTS]
  print('arborescences per root:', sizes, 'families:',
        sizes[0] * sizes[1] * sizes[2] * sizes[3] * sizes[4], flush=True)
  counts = Counter()
  c0, c1, c2, c3, c4 = (code[r] for r in VERTS)
  for i, a in enumerate(c0):
    for b in c1:
      ab = a + b
      for c in c2:
        abc = ab + c
        for d in c3:
          abcd = abc + d
          for e in c4:
            counts[abcd + e] += 1
    print(f'  pass 1: {i + 1}/{len(c0)} ({time.time() - start:.0f}s)', flush=True)
  # K4 multisets of contracted families (base 5 codes; counts <= 4)
  k4_index = {a: i for i, a in enumerate(k4_arcs)}
  k4_trees = {r: sorted({contract(t) for t in trees[r]}) for r in range(4)}
  k4_counts = Counter()
  for fam in itertools.product(*[k4_trees[r] for r in range(4)]):
    k4_counts[sum(5 ** k4_index[a] for t in fam for a in t)] += 1
  k4_code = {r: [sum(5 ** k4_index[a] for a in contract(t)) for t in trees[r]] for r in range(4)}
  k0, k1, k2, k3 = (k4_code[r] for r in range(4))
  contraction_preserves_uc = True
  y0, y1, y2, y3, y4 = (yval[r] for r in VERTS)
  worst = None
  uc = 0
  for i, a in enumerate(c0):
    for j, b in enumerate(c1):
      ab = a + b
      yab = y0[i] + y1[j]
      kab = k0[i] + k1[j]
      for k, c in enumerate(c2):
        abc = ab + c
        yabc = yab + y2[k]
        kabc = kab + k2[k]
        for m, d in enumerate(c3):
          abcd = abc + d
          yabcd = yabc + y3[m]
          kabcd = kabc + k3[m]
          for n_, e in enumerate(c4):
            if counts[abcd + e] == 1:
              uc += 1
              if k4_counts[kabcd] != 1:
                contraction_preserves_uc = False
              val = yabcd + y4[n_]
              if worst is None or val < worst:
                worst = val
    print(f'  pass 2: {i + 1}/{len(c0)} ({time.time() - start:.0f}s)', flush=True)

  # 3. expectation of the lifted certificate
  value = Fraction(0)
  for r in range(4):
    total = sum(weight(t, rates) for t in trees[r])
    for t in trees[r]:
      value += y[(r, contract(t))] * Fraction(weight(t, rates), total)

  result = {
    'subdivided_edge': [0, 1],
    'arborescences_per_root': sizes,
    'families': sizes[0] * sizes[1] * sizes[2] * sizes[3] * sizes[4],
    'distinct_multisets': len(counts),
    'uniquely_constructable_families': uc,
    'pushforward_equals_k4_laws': pushforward_ok,
    'k4_distinct_multisets': len(k4_counts),
    'contraction_maps_UC_to_UC': contraction_preserves_uc,
    'min_over_UC_families_of_sum_lifted_y': worst,
    'expected_value_under_root_laws': str(value),
    'equals_k4_value': value == stored,
    'no_coupling_proved': pushforward_ok and contraction_preserves_uc and worst >= 0 and value < 0,
    'seconds': round(time.time() - start, 1),
  }
  Path(__file__).with_name('k4_subdivision_results.json').write_text(json.dumps(result, indent=2) + '\n')
  for key, val in result.items():
    print(key, val)
  if not result['no_coupling_proved'] or not result['equals_k4_value']:
    raise SystemExit('FAILED')


if __name__ == '__main__':
  main()
