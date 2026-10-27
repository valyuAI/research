"""Exact checks of the combinatorial lemmas behind the cactus theorem.

Standard library only. Rates are random positive rationals from a fixed seed.

1. Cycle identity (Theorem 5): on a bidirected n-cycle the arborescences rooted
   at r are exactly the n cut trees, and w_r(k)/w_r(k-1) = a_k/b_k for every
   root r and cut index k in the window r+1..r+n-1.
2. Block factorisation (Lemma 3): for several cactus networks, the arborescences
   rooted at j are exactly the unions of block arborescences rooted at the block
   vertices nearest to j, with multiplicative weights, so P_j is a product law.
3. Dominant families are uniquely constructable (Lemma 2), sampled: for small
   cacti every dominant family of many random rate vectors is checked against an
   exhaustive enumeration of all tree families and their edge multisets.

Run: python3 -B check_cactus_lemmas.py  (prints a summary, writes JSON results)
"""

import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

RNG = random.Random(20261026)


def arborescences(n, arcs, root):
  """All in-arborescences rooted at root, as frozensets of arc indices."""
  out = {v: [k for k, (s, _) in enumerate(arcs) if s == v] for v in range(n)}
  others = [v for v in range(n) if v != root]
  found = []
  for choice in itertools.product(*[out[v] for v in others]):
    nxt = {v: arcs[k][1] for v, k in zip(others, choice)}
    ok = True
    for v in others:
      seen, u = set(), v
      while u != root:
        if u in seen:
          ok = False
          break
        seen.add(u)
        u = nxt[u]
      if not ok:
        break
    if ok:
      found.append(frozenset(choice))
  return found


def weight(tree, rates):
  w = Fraction(1)
  for k in tree:
    w *= rates[k]
  return w


def bidirected(pairs):
  arcs = []
  for u, v in pairs:
    arcs += [(u, v), (v, u)]
  return arcs


def random_rates(m):
  return [Fraction(RNG.randint(1, 60), RNG.randint(1, 60)) for _ in range(m)]


def check_cycle(n):
  pairs = [(i, (i + 1) % n) for i in range(n)]
  arcs = bidirected(pairs)
  idx = {a: k for k, a in enumerate(arcs)}
  rates = random_rates(len(arcs))
  b = [rates[idx[(v, (v + 1) % n)]] for v in range(n)]
  a = [rates[idx[(v, (v - 1) % n)]] for v in range(n)]
  for r in range(n):
    trees = set(arborescences(n, arcs, r))
    cut_trees = {}
    for k in range(r, r + n):
      tree = set()
      for v in range(r + 1, k + 1):
        tree.add(idx[(v % n, (v - 1) % n)])
      for v in range(k + 1, r + n):
        tree.add(idx[(v % n, (v + 1) % n)])
      cut_trees[k] = frozenset(tree)
    if set(cut_trees.values()) != trees or len(trees) != n:
      return False
    for k in range(r + 1, r + n):
      lhs = weight(cut_trees[k], rates) / weight(cut_trees[k - 1], rates)
      if lhs != a[k % n] / b[k % n]:
        return False
  return True


def blocks_of(n, pairs):
  """Blocks (as sets of undirected edges) of a simple undirected graph."""
  adj = {v: [] for v in range(n)}
  for i, (u, v) in enumerate(pairs):
    adj[u].append((v, i))
    adj[v].append((u, i))
  disc, low, stack, out = {}, {}, [], []
  counter = [0]

  def dfs(u, parent_edge):
    disc[u] = low[u] = counter[0]
    counter[0] += 1
    for v, i in adj[u]:
      if i == parent_edge:
        continue
      if v not in disc:
        stack.append(i)
        dfs(v, i)
        low[u] = min(low[u], low[v])
        if low[v] >= disc[u]:
          comp = set()
          while True:
            e = stack.pop()
            comp.add(e)
            if e == i:
              break
          out.append(comp)
      elif disc[v] < disc[u]:
        stack.append(i)
        low[u] = min(low[u], disc[v])

  dfs(0, None)
  return out


def nearest_block_vertex(n, pairs, block_vertices, j):
  adj = {v: set() for v in range(n)}
  for u, v in pairs:
    adj[u].add(v)
    adj[v].add(u)
  dist = {j: 0}
  frontier = [j]
  while frontier:
    nxt = []
    for u in frontier:
      for v in adj[u]:
        if v not in dist:
          dist[v] = dist[u] + 1
          nxt.append(v)
    frontier = nxt
  return min(block_vertices, key=lambda v: dist[v])


def check_factorisation(n, pairs):
  arcs = bidirected(pairs)
  rates = random_rates(len(arcs))
  arc_edge = [k // 2 for k in range(len(arcs))]
  blocks = blocks_of(n, pairs)
  for j in range(n):
    full = arborescences(n, arcs, j)
    total = sum(weight(t, rates) for t in full)
    factors = []
    for blk in blocks:
      verts = sorted({x for e in blk for x in pairs[e]})
      local = {v: i for i, v in enumerate(verts)}
      sub_arcs = [k for k in range(len(arcs)) if arc_edge[k] in blk]
      local_arcs = [(local[arcs[k][0]], local[arcs[k][1]]) for k in sub_arcs]
      r = nearest_block_vertex(n, pairs, verts, j)
      sub = arborescences(len(verts), local_arcs, local[r])
      factors.append([frozenset(sub_arcs[k] for k in t) for t in sub])
    product = set()
    for combo in itertools.product(*factors):
      product.add(frozenset().union(*combo))
    if product != set(full):
      return False
    # product law: P_j(T) equals the product of block probabilities
    for t in full:
      p = weight(t, rates) / total
      q = Fraction(1)
      for fac in factors:
        part = [s for s in fac if s <= t][0]
        q *= weight(part, rates) / sum(weight(s, rates) for s in fac)
      if p != q:
        return False
  return True


def check_dominant_uc(n, pairs, samples):
  arcs = bidirected(pairs)
  arbs = [arborescences(n, arcs, r) for r in range(n)]
  multiset_count = {}
  for fam in itertools.product(*arbs):
    key = tuple(sorted(k for t in fam for k in t))
    multiset_count[key] = multiset_count.get(key, 0) + 1
  for _ in range(samples):
    logw = [RNG.gauss(0.0, 3.0) for _ in arcs]
    fam = []
    for r in range(n):
      scores = [(sum(logw[k] for k in t), t) for t in arbs[r]]
      scores.sort(key=lambda s: s[0])
      if scores[-1][0] - scores[-2][0] < 1e-9:
        continue
      fam.append(scores[-1][1])
    if len(fam) < n:
      continue
    key = tuple(sorted(k for t in fam for k in t))
    if multiset_count[key] != 1:
      return False
  return True


def main():
  results = {}
  results['cycle_identity'] = {f'n={n}': check_cycle(n) for n in range(3, 9)}
  cacti = {
    'bowtie': (5, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]),
    'bowtie_plus_pendant': (6, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0), (4, 5)]),
    'square_with_two_triangles': (7, [(0, 1), (1, 2), (2, 3), (3, 0), (1, 4), (4, 5), (5, 1), (3, 6), (6, 2)]),
    'cycle_with_tails': (6, [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (4, 5)]),
    'triangle_chain': (7, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2), (4, 5), (5, 6), (6, 4)]),
  }
  results['block_factorisation'] = {name: check_factorisation(n, p) for name, (n, p) in cacti.items()}
  small = {
    'cycle5': (5, [(i, (i + 1) % 5) for i in range(5)]),
    'cycle6': (6, [(i, (i + 1) % 6) for i in range(6)]),
    'bowtie': cacti['bowtie'],
  }
  results['dominant_families_are_uc'] = {name: check_dominant_uc(n, p, 300) for name, (n, p) in small.items()}
  ok = all(v for group in results.values() for v in group.values())
  results['all_passed'] = ok
  Path(__file__).with_name('cactus_lemmas_results.json').write_text(json.dumps(results, indent=2) + '\n')
  for group, vals in results.items():
    print(group, vals)
  if not ok:
    raise SystemExit('FAILED')


if __name__ == '__main__':
  main()
