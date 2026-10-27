"""Replay of the inductive construction (Theorem 4.4) for small parameters.

For each (q, r) below, builds with construct.recipe a zero-sum configuration of n pairwise
skew lines in GF(q)^r for every r+1 <= n <= min(mu_q(r), cap) and verifies it with the
independent checker (check_codes.check_dict).  For q in {3,4,5} the base cases r in {4,5}
are taken from the stored certificates; for q >= 7 no search is allowed (blocks and
absorption only), as in the proof.  There is no search over line configurations, but
construct.line_weights picks the weights of line blocks with a size other than 4 or q by
seeded random trials of the coefficients in Lemma 4.2(5).  Prints progress; writes
replay_recipe_results.json.
Usage: python3 -B -O replay_recipe.py [quick]
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construct import Ctx, mu, recipe, to_check_matrix
from check_codes import check_dict

HERE = os.path.dirname(os.path.abspath(__file__))
PLAN_FULL = [((3, 1), 8, 900), ((2, 2), 7, 1100), ((5, 1), 6, 700), ((7, 1), 6, 700),
             ((2, 3), 6, 700), ((3, 2), 5, 800), ((11, 1), 5, 400), ((13, 1), 4, 200)]
PLAN_QUICK = [((3, 1), 7, 300), ((2, 2), 6, 300), ((5, 1), 6, 200), ((7, 1), 5, 200)]


def load_base(C, memo):
  q = C.q
  for r in (4, 5):
    for n in range(4, mu(q, r) + 1):
      path = os.path.join(HERE, 'certificates', 'base', f'q{q}_r{r}_n{n}.json')
      if os.path.exists(path):
        d = json.load(open(path))
        A, B = d['stabilizer_X_part_A'], d['stabilizer_Z_part_B']
        conf = [([A[i][k] for i in range(r)], [B[i][k] for i in range(r)], 1) for k in range(d['n'])]
        memo[(r, n)] = (conf, 'stored certificate')


def main():
  plan = PLAN_QUICK if 'quick' in sys.argv[1:] else PLAN_FULL
  report = []
  t0 = time.time()
  allok = True
  for (p, m), rmax, cap in plan:
    C = Ctx(p, m, seed=11)
    q = C.q
    memo = {}
    if q in (3, 4, 5):
      load_base(C, memo)
    for r in range(4, rmax + 1):
      lo, hi = r + 1, min(mu(q, r), cap)
      missing, invalid, hows = [], [], {}
      for n in range(lo, hi + 1):
        res = recipe(C, r, n, memo, allow_random=False)
        if res is None:
          missing.append(n)
          continue
        conf, how = res
        key = how.split('(')[0]
        hows[key] = hows.get(key, 0) + 1
        A, B = to_check_matrix(C.F, conf)
        d = {'p': p, 'm': m, 'q': q, 'n': n, 'modulus_low_first': C.F.mod,
             'stabilizer_X_part_A': A, 'stabilizer_Z_part_B': B}
        rr = check_dict(d, f'q{q}_r{r}_n{n}')
        if not rr['valid'] or rr['rank'] > r or len(conf) != n:
          invalid.append(n)
      ok = not missing and not invalid
      allok = allok and ok
      report.append({'q': q, 'r': r, 'mu': mu(q, r), 'n_range': [lo, hi], 'missing': missing,
                     'invalid': invalid, 'methods': hows})
      print(f'q={q} r={r} mu={mu(q,r)} n={lo}..{hi}: missing {missing} invalid {invalid} {hows} ({time.time()-t0:.0f}s)', flush=True)
  with open(os.path.join(HERE, 'replay_recipe_results.json' if plan is PLAN_FULL else 'replay_recipe_quick.json'), 'w') as f:
    json.dump({'all_ok': allok, 'report': report}, f, indent=1)
  sys.exit(0 if allok else 1)


if __name__ == '__main__':
  main()
