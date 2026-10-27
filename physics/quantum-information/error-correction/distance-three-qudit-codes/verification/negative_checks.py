"""Corrupted inputs must be rejected by check_codes.check_dict (no assertions used)."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_codes import check_dict

HERE = os.path.dirname(os.path.abspath(__file__))


def load(rel):
  return json.load(open(os.path.join(HERE, rel)))


def main():
  cases = []
  base = load('certificates/table/q4_r5_n65.json')
  d = copy.deepcopy(base); d['stabilizer_X_part_A'][0][7] = d['stabilizer_X_part_A'][0][7] ^ 1
  cases.append(('flip one X entry of [[65,60]]_4', d))
  d = copy.deepcopy(base)
  for row in ('stabilizer_X_part_A', 'stabilizer_Z_part_B'):
    for i in range(len(d[row])):
      d[row][i][3] = d[row][i][2]
  cases.append(('duplicate a column pair (two equal lines)', d))
  d = copy.deepcopy(base)
  for row in ('stabilizer_X_part_A', 'stabilizer_Z_part_B'):
    for i in range(len(d[row])):
      d[row][i][5] = 0
  cases.append(('zero column pair (Pauli commuting with S)', d))
  d = copy.deepcopy(base); d['modulus_low_first'] = [1, 0, 1]
  cases.append(('reducible modulus X^2+1 over GF(2)', d))
  d = copy.deepcopy(base); d['stabilizer_Z_part_B'][1][0] = 7
  cases.append(('entry outside GF(4)', d))
  t = load('certificates/maximal/q3_r5_n28.json')
  d = copy.deepcopy(t)
  k = next(k for k in range(t['n']) if any(t['stabilizer_Z_part_B'][i][k] for i in range(5)))
  for i in range(5):
    d['stabilizer_Z_part_B'][i][k] = (2 * d['stabilizer_Z_part_B'][i][k]) % 3
  cases.append(('rescale one Z column of [[28,23]]_3 by 2 (breaks the Plucker relation)', d))
  d = copy.deepcopy(t)
  for row in ('stabilizer_X_part_A', 'stabilizer_Z_part_B'):
    for i in range(5):
      d[row][i] = d[row][i] + [d[row][i][0]]
  d['n'] = 29
  cases.append(('append a 29th qutrit equal to the first', d))
  results = []
  allrej = True
  for name, d in cases:
    r = check_dict(d, name)
    rejected = not r.get('valid', False)
    allrej = allrej and rejected
    results.append({'case': name, 'rejected': rejected, 'details': {k: v for k, v in r.items() if k not in ('file', 'sha256')}})
    print(('REJECTED ' if rejected else 'ACCEPTED!') + ' ' + name, flush=True)
  with open(os.path.join(HERE, 'negative_checks_results.json'), 'w') as f:
    json.dump({'all_rejected': allrej, 'cases': results}, f, indent=1)
  sys.exit(0 if allrej else 1)


if __name__ == '__main__':
  main()
