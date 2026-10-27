"""Continuous flexes of the 45 flexible Johnson solids (standard library only, exact arithmetic).
  * 38 solids: Minkowski reorientation P_t = S1 + R_t S2 (minkflex.check; partition of the edges into the two
    summands from certificates/minkowski_partitions.json).
  * 7 augmented prisms J49, J52-J57: prism flex (prismflex.check).
Writes results/flex_finite.json."""
import json, sys
import minkflex, prismflex

MINK = [3, 4, 5, 7, 8, 9, 14, 15, 16, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 35, 36, 37, 38, 39, 40, 41, 42, 43, 67,
        72, 73, 74, 75, 76, 77, 78, 79, 80]
PRISM = [49, 52, 53, 54, 55, 56, 57]

if __name__ == '__main__':
  props = json.load(open('certificates/minkowski_partitions.json'))
  res = {}
  for k in MINK:
    E = props[str(k)]['edges']
    out = None
    for part in props[str(k)]['partitions']:
      s1 = [E[r] for r, bit in enumerate(part) if bit]
      out = minkflex.check('data/J%02d.json' % k, s1)
      if out['ok']:
        out['S1_edges'] = s1
        break
    out['type'] = 'minkowski'
    res[str(k)] = out
    print('J%d %s %s' % (k, 'FLEX' if out['ok'] else 'FAILED', {a: b for a, b in out.items() if a != 'S1_edges'}),
          flush=True)
  for k in PRISM:
    out = prismflex.check('data/J%02d.json' % k)
    out['type'] = 'prism'
    res[str(k)] = out
    print('J%d %s %s' % (k, 'FLEX' if out['ok'] else 'FAILED', out), flush=True)
  json.dump(res, open('results/flex_finite.json', 'w'), indent=1)
  bad = [k for k, r in res.items() if not r['ok']]
  print('ALL 45 FLEXES CERTIFIED' if not bad else 'FAILED: %s' % bad)
  sys.exit(1 if bad else 0)
