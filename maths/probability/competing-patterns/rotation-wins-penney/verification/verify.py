"""Check exact rotation certificates and optionally reconstructed coefficients."""

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def require(condition, message):
  if not condition:
    raise RuntimeError(message)


def complement(pattern):
  return tuple(len(pattern) + 1 - x for x in pattern)


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('--generated', type=Path)
  args = ap.parse_args()
  base = Path(__file__).resolve().parent
  data = json.loads((base / 'certificates.json').read_text())
  require(data['schema'] == 1, 'Unexpected certificate schema')
  expected = {4: (15, Fraction(3, 4)), 5: (12, Fraction(9, 10)),
              6: (5, Fraction(49, 50)), 7: (6, Fraction(99, 100))}
  results = {}
  for k, (cutoff, advertisedLower) in expected.items():
    rows = data['cases'][str(k)]
    patterns = {tuple(row['pattern']) for row in rows}
    wanted = {p for p in itertools.permutations(range(1, k + 1)) if p < complement(p)}
    require(len(rows) == len(patterns) and patterns == wanted, f'Incomplete coverage for k={k}')
    if args.generated:
      rebuiltRows = [json.loads(line) for line in (args.generated / f'k{k}.jsonl').read_text().splitlines()]
      rebuilt = {tuple(row['pattern']): row for row in rebuiltRows}
      require(len(rebuiltRows) == len(rebuilt) and rebuilt.keys() == patterns, f'Incomplete reconstruction for k={k}')
    r = Fraction(2 * (k - 1), math.factorial(k))
    q = (cutoff - k + 1) // (2 * k - 2)
    tail = Fraction(4, math.factorial(k)) * r ** (q + 1) / (1 - r)
    minimum = None
    minimizers = []
    for row in rows:
      p = tuple(row['pattern'])
      require(row['cutoff'] == cutoff, f'Unexpected cutoff for {p}')
      cs = row['coefficients']
      require(len(cs) == 2 and all(len(c) == cutoff + 1 for c in cs), f'Invalid dimensions for {p}')
      require(all(type(v) is int for c in cs for v in c), f'Noninteger coefficient for {p}')
      require(cs[0][0] == cs[1][0] == -1, f'Invalid root counts for {p}')
      if args.generated:
        require(rebuilt[p] == row, f'Independent coefficient mismatch for {p}')
      delta = sum((Fraction(cs[0][s] - cs[1][s], math.factorial(k + s))
                   for s in range(cutoff + 1)), Fraction(0))
      scaled = delta * math.factorial(k + 1)
      require(delta > tail, f'Uncertified sign for {p}')
      require(scaled > advertisedLower, f'Failed table lower bound for {p}')
      if minimum is None or scaled < minimum:
        minimum, minimizers = scaled, [p]
      elif scaled == minimum:
        minimizers.append(p)
    results[str(k)] = {'representatives': len(rows), 'cutoff': cutoff,
                       'minimumScaledDelta': str(minimum), 'minimizers': [list(p) for p in minimizers],
                       'scaledTail': str(tail * math.factorial(k + 1))}
    print(f'k={k}: {len(rows)} representatives, min={minimum}, tail={results[str(k)]["scaledTail"]}, PASS', flush=True)

  def term(k, s):
    return Fraction(math.comb(2 * s, s) * math.factorial(k + 1), math.factorial(k + s))

  local = sum((term(8, s) for s in range(2, 7)), Fraction(0)) + Fraction(3, 2) * term(8, 7)
  far = Fraction(4 * 8 * 7 * 9, math.factorial(8) - 14)
  margin = 1 - local - far - Fraction(4, 3) * term(8, 8)
  require(local == Fraction(256699, 300300), 'Uniform local bound mismatch')
  require(far == Fraction(144, 2879), 'Uniform tail mismatch')
  require(margin == Fraction(218738049, 2305503200) and margin > 0, 'Uniform sign failed')
  print(f'k>=8: exact uniform scaled margin >= {margin}, PASS', flush=True)
  results['uniform'] = {'scaledMargin': str(margin)}
  expectedResults = json.loads((base / 'results.json').read_text())
  require(results == expectedResults, 'Saved result summary differs from recomputation')
  print('Certificate arithmetic and coverage PASS' + ('; independent coefficients MATCH' if args.generated else ''), flush=True)
  if not args.generated:
    print('Counts were read from the certificate. Use build.sh to reconstruct them independently.', flush=True)


if __name__ == '__main__':
  main()
