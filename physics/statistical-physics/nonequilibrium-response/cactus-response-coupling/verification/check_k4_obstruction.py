"""Exact replay of the K4 no-coupling certificate (standard library only).

For the complete directed graph on four states with the integer rates stored in
k4_no_coupling_certificate.json, there is no probability measure on uniquely
constructable tree families whose marginal at every root j is the arborescence
law P_j. Farkas' lemma: such a measure cannot exist if some y on (root, tree)
pairs satisfies sum_j y(j, T_j) >= 0 for every UC family and
sum_j sum_T y(j, T) P_j(T) < 0. This script

1. enumerates the 16 arborescences per root from scratch,
2. enumerates all 16^4 = 65536 tree families and their arc multisets,
3. marks the families whose multiset occurs once (uniquely constructable),
4. computes every P_j(T) exactly from the integer rates,
5. checks both Farkas conditions in exact rational arithmetic.

Run: python3 -B check_k4_obstruction.py
"""

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

N = 4


def label(arc):
  return f'{arc[0]}>{arc[1]}'


def arborescences(root):
  others = [v for v in range(N) if v != root]
  trees = []
  for targets in itertools.product(range(N), repeat=len(others)):
    nxt = dict(zip(others, targets))
    if any(v == t for v, t in nxt.items()):
      continue
    good = True
    for v in others:
      u, steps = v, 0
      while u != root and steps <= N:
        u, steps = nxt[u], steps + 1
      if u != root:
        good = False
        break
    if good:
      trees.append(tuple(sorted((v, nxt[v]) for v in others)))
  return trees


def main():
  cert = json.loads(Path(__file__).with_name('k4_no_coupling_certificate.json').read_text())
  rates = {}
  for key, val in cert['rates'].items():
    u, v = key.split('->')
    rates[(int(u), int(v))] = int(val)
  trees = {r: arborescences(r) for r in range(N)}
  assert all(len(trees[r]) == 16 for r in range(N))  # Cayley: 4^(4-2)

  y = {}
  for key, val in cert['y'].items():
    head, body = key.split(':')
    r = int(head.replace('root', ''))
    arcs = tuple(sorted((int(a.split('>')[0]), int(a.split('>')[1])) for a in body.split(',')))
    y[(r, arcs)] = Fraction(val)
  if set(y) != {(r, t) for r in range(N) for t in trees[r]}:
    raise SystemExit('certificate does not cover exactly the (root, tree) pairs')

  counts = Counter()
  families = list(itertools.product(*[trees[r] for r in range(N)]))
  for fam in families:
    counts[tuple(sorted(a for t in fam for a in t))] += 1
  uc = [fam for fam in families if counts[tuple(sorted(a for t in fam for a in t))] == 1]

  worst = min(sum(y[(r, fam[r])] for r in range(N)) for fam in uc)
  value = Fraction(0)
  for r in range(N):
    weights = {}
    for t in trees[r]:
      w = 1
      for arc in t:
        w *= rates[arc]
      weights[t] = w
    total = sum(weights.values())
    for t in trees[r]:
      value += y[(r, t)] * Fraction(weights[t], total)

  values = sorted(set(y.values()))
  result = {
    'families': len(families),
    'distinct_multisets': len(counts),
    'uniquely_constructable_families': len(uc),
    'certificate_values': [str(v) for v in values],
    'min_over_UC_families_of_sum_y': str(worst),
    'expected_value_under_root_laws': str(value),
    'expected_value_float': float(value),
    'matches_stored_value': str(value) == cert['b_dot_y'],
    'no_coupling_proved': worst >= 0 and value < 0,
  }
  Path(__file__).with_name('k4_obstruction_results.json').write_text(json.dumps(result, indent=2) + '\n')
  for k, v in result.items():
    print(k, v)
  if not result['no_coupling_proved'] or not result['matches_stored_value']:
    raise SystemExit('FAILED')


if __name__ == '__main__':
  main()
