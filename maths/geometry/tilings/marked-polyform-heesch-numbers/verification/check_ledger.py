#!/usr/bin/env python3
"""Consistency of the results ledger (results.json).  Standard library only.

Checks that
  * the ledger lists every free polyhex with <= 4 cells and every free polyomino with <= 5 cells
    exactly once (enumerated here from scratch), plus the straight row of 5 hexagons;
  * for every tile the witness file passes check_marked.py with exactly h coronas and is a
    marking of that tile;
  * the retained upper-bound log records an unsatisfiable base formula for k = h + 1
    (same tile up to symmetry, imbalance threshold 1) and a successful drat-trim check.

This checks retained execution records; it does not regenerate formulas or replay DRAT proofs.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_marked import check  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NB = {'hex': [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)], 'sq': [(1, 0), (0, 1), (-1, 0), (0, -1)]}


def syms(grid):
  out = []
  for s in (0, 1):
    for k in range(6 if grid == 'hex' else 4):
      def f(c, s=s, k=k):
        if s:
          c = (c[0] + c[1], -c[1]) if grid == 'hex' else (c[0], -c[1])
        for _ in range(k):
          c = (-c[1], c[0] + c[1]) if grid == 'hex' else (-c[1], c[0])
        return c
      out.append(f)
  return out


def canon(grid, cells):
  best = None
  for f in syms(grid):
    img = [f(tuple(c)) for c in cells]
    mx, my = min(c[0] for c in img), min(c[1] for c in img)
    key = tuple(sorted((c[0] - mx, c[1] - my) for c in img))
    if best is None or key < best:
      best = key
  return best


def enumerate_free(grid, n):
  level = {canon(grid, [(0, 0)])}
  allf = set(level)
  for _ in range(n - 1):
    nxt = set()
    for P in level:
      ps = set(P)
      for c in P:
        for d in NB[grid]:
          e = (c[0] + d[0], c[1] + d[1])
          if e not in ps:
            nxt.add(canon(grid, list(ps | {e})))
    level = nxt
    allf |= level
  return allf


def main(ledger=None):
  T = json.load(open(ledger or os.path.join(HERE, 'results.json')))
  want = {('hex', P) for P in enumerate_free('hex', 4)} | {('sq', P) for P in enumerate_free('sq', 5)}
  want.add(('hex', canon('hex', [(0, i) for i in range(5)])))
  have = [(t['grid'], canon(t['grid'], t['cells'])) for t in T['tiles']]
  assert len(have) == len(set(have)), 'duplicate tile in ledger'
  assert set(have) == want, ('ledger does not match the enumeration', set(have) ^ want)
  counts = {g: sum(1 for x in want if x[0] == g) for g in ('hex', 'sq')}
  for t in T['tiles']:
    r = check(os.path.join(HERE, t['witness']))
    W = json.load(open(os.path.join(HERE, t['witness'])))
    assert r['grid'] == t['grid'] and r['slots'] == 1, (t['name'], 'wrong grid or slot scope')
    assert r['coronas'] == t['h'], (t['name'], 'witness has', r['coronas'], 'coronas')
    assert canon(t['grid'], W['cells']) == canon(t['grid'], t['cells']), (t['name'], 'witness is for another tile')
    u = t['upper_bound']
    assert u is not None and u['drat_verified'], (t['name'], 'no verified upper bound')
    assert u['k'] == t['h'] + 1 and u['grid'] == t['grid'], (t['name'], 'upper bound is not at k = h + 1')
    assert canon(t['grid'], u['cells']) == canon(t['grid'], t['cells']), (t['name'], 'upper bound is for another tile')
    assert u['solver_unsat'] and u.get('cadical_rc', 20) == 20
    # These are retained execution records, not a fresh DRAT replay.
    log = open(os.path.join(HERE, u['evidence_log'])).read()
    # Count scope lines before parsing so a malformed second scope cannot be skipped.
    scopes = [line for line in log.splitlines() if 'cells=' in line]
    assert len(scopes) == 1, ('missing or ambiguous formula scope', t['name'])
    scope = re.fullmatch(
      r'(hex|sq) cells=(\[.*\]) k=([0-9]+) imb=([0-9]+) radius=[0-9]+\.[0-9]: '
      r'placements ([0-9]+) vars ([0-9]+) clauses ([0-9]+) \([0-9]+\.[0-9]s\)', scopes[0])
    assert scope, ('invalid formula scope', t['name'])
    grid, cells, k, imbalance, placements, nvars, nclauses = scope.groups()
    try:
      cells = json.loads(cells)
    except json.JSONDecodeError as exc:
      raise AssertionError(('invalid formula cells', t['name'])) from exc
    assert cells and all(isinstance(c, list) and len(c) == 2 and
                         all(type(v) is int for v in c) for c in cells), ('invalid formula cells', t['name'])
    assert grid == u['grid'] and canon(grid, cells) == canon(grid, u['cells']), \
      ('formula log is for another tile', t['name'])
    assert int(k) == u['k'] and int(imbalance) == 1, ('formula log has wrong bound or imbalance', t['name'])
    assert (int(placements), int(nvars), int(nclauses)) == (u['placements'], u['nvars'], u['nclauses']), \
      ('formula log has wrong dimensions', t['name'])
    for field, suffix in [('cnf_sha256', '.cnf'), ('proof_sha256', '.drat')]:
      assert re.fullmatch(r'[0-9a-f]{64}', u[field]), ('invalid hash', t['name'], field)
      assert f"{u[field]}  {u['name']}{suffix}" in log, ('hash not in log', t['name'], field)
    assert re.search(r'^s UNSATISFIABLE$', log, re.M), ('no solver conclusion', t['name'])
    assert re.search(r'^s VERIFIED$', log, re.M), ('no DRAT verification', t['name'])
    assert re.search(r'^DRAT_VERIFIED ' + re.escape(u['name']) + '$', log, re.M)
    assert 'END' in log, ('incomplete log', t['name'])
  hexmax = max(t['h'] for t in T['tiles'] if t['grid'] == 'hex' and len(t['cells']) <= 4)
  sqmax = max(t['h'] for t in T['tiles'] if t['grid'] == 'sq')
  print(f"ledger: {counts['hex'] - 1} polyhexes (<= 4 cells) + straight 5-row, {counts['sq']} polyominoes (<= 5 cells); "
        f"every value has a freshly checked witness and a retained DRAT verification record; "
        f"max h: polyhex {hexmax}, polyomino {sqmax}")


if __name__ == '__main__':
  if not __debug__:
    raise SystemExit('FAIL: verification requires Python assertions enabled')
  main()
