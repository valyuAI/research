#!/usr/bin/env python3
"""Negative tests: corrupted witnesses must be rejected by check_marked.py.  Standard library only."""
import copy
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_marked import check  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def rejected(W):
  path = os.path.join(HERE, '_negative_tmp.json')
  json.dump(W, open(path, 'w'))
  try:
    check(path)
    return False
  except AssertionError:
    return True
  finally:
    os.remove(path)


def mutations(W):
  flip = {'b': 'n', 'n': 'b', 'f': 'b'}
  # 1. change the label of the first edge
  X = copy.deepcopy(W)
  X['labels'][0] = ''.join(flip[c] for c in X['labels'][0])
  yield 'relabel first edge', X
  # 2. drop one copy of level 1
  X = copy.deepcopy(W)
  i = next(i for i, p in enumerate(X['placements']) if p['level'] == 1)
  del X['placements'][i]
  yield 'drop a level-1 copy', X
  # 3. shift one copy of level 1 by one cell
  X = copy.deepcopy(W)
  X['placements'][i]['t'][0] += 1
  yield 'shift a level-1 copy', X
  # 4. promote the outermost corona to a fake extra corona
  X = copy.deepcopy(W)
  k = max(p['level'] for p in X['placements'])
  for p in X['placements']:
    if p['level'] == k:
      p['level'] = k + 1
  yield 'relabel last corona as k+1', X
  # 5. balance the marking: turn every bump into a flat edge and every nick into a flat edge
  X = copy.deepcopy(W)
  X['labels'] = ['f' * len(l) for l in X['labels']]
  yield 'all-flat marking', X


def main():
  n = 0
  for f in sorted(glob.glob(os.path.join(HERE, 'witnesses', '*.json'))):
    W = json.load(open(f))
    for name, X in mutations(W):
      assert rejected(X), f'{os.path.basename(f)}: mutation "{name}" was not rejected'
      n += 1
  print(f'negative tests: all {n} corrupted witnesses rejected')


if __name__ == '__main__':
  main()
