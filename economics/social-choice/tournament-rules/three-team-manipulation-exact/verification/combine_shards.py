"""Merge the result files of verify_rule.py --shard=i/m runs and confirm that all m shards are present."""
import sys, json
from fractions import Fraction
res = [json.load(open(f)) for f in sys.argv[2:]]
m = int(res[0]['shard'].split('/')[1])
shards = sorted(int(r['shard'].split('/')[0]) for r in res)
if shards != list(range(m)) or any(int(r['shard'].split('/')[1]) != m for r in res) or not all(r['ok'] for r in res):
  print('FAIL: shards missing or failed'); sys.exit(1)
if len(set(r.get('certificate_sha256') for r in res)) != 1 or res[0].get('certificate_sha256') is None:
  print('FAIL: shards were run on different certificates'); sys.exit(1)
keys = ('n', 'k', 'mode', 'alpha', 'classes', 'certificate_sha256')
if any(tuple(r[x] for x in keys) != tuple(res[0][x] for x in keys) for r in res):
  print('FAIL: shards refer to different certificates'); sys.exit(1)
out = {x: res[0][x] for x in keys}
out['manipulations'] = sum(r['manipulations'] for r in res)
out['max_gain'] = str(max(Fraction(r['max_gain']) for r in res))
out['tight_manipulations'] = sum(r['tight_manipulations'] for r in res)
out['tight_classes'] = sorted(set(c for r in res for c in r['tight_classes']))
out['properties'] = res[0]['properties']
out['shards'] = m
out['ok'] = Fraction(out['max_gain']) <= Fraction(out['alpha'])
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print(f"n={out['n']} k={out['k']} (sha256 {out['certificate_sha256'][:16]}...): {m} shards, {out['manipulations']} manipulations, max gain {out['max_gain']}, {out['tight_manipulations']} tight in {len(out['tight_classes'])} classes: {'OK' if out['ok'] else 'FAIL'}")
sys.exit(0 if out['ok'] else 1)
