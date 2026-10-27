"""Generate the stored certificates (deterministic seeds).

  certificates/base/      zero-sum line configurations for the base cases of Theorem 4.4:
                          q in {3,4,5}; r = 4, 5 <= n <= mu_q(4); r = 5, 6 <= n <= mu_q(5).
  certificates/table/     the four new ququart codes [[59,54,3]]_4, [[61,56,3]]_4,
                          [[62,57,3]]_4, [[65,60,3]]_4 (codetables.de lower bounds 2 -> 3).
  certificates/maximal/   [[q^3+1, q^3-4, 3]]_q for q = 3,4,5,7,8,9 (absorption, Lemma 4.3).
Run:  python3 -B generate_certificates.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construct import Ctx, mu, recipe, absorbed_full, to_check_matrix

HERE = os.path.dirname(os.path.abspath(__file__))


def write(path, C, conf, note):
  A, B = to_check_matrix(C.F, conf)
  d = {'q': C.q, 'p': C.p, 'm': C.F.m, 'modulus_low_first': C.F.mod,
       'element_encoding': 'integer x = sum c_i p^i encodes sum c_i X^i in GF(p)[X]/(modulus)',
       'n': len(conf), 'r_ambient': len(A), 'note': note,
       'stabilizer_X_part_A': A, 'stabilizer_Z_part_B': B}
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, 'w') as f:
    json.dump(d, f)


def main():
  out = os.path.join(HERE, 'certificates')
  log = {}
  for p, m in [(3, 1), (2, 2), (5, 1)]:
    C = Ctx(p, m, seed=2026)
    q = C.q
    memo = {}
    for r, nmin in [(4, 5), (5, 6)]:
      for n in range(nmin, mu(q, r) + 1):
        res = recipe(C, r, n, memo)
        if res is None:
          print(f'q={q} r={r} n={n}: NONE', flush=True)
          continue
        conf, how = res
        write(os.path.join(out, 'base', f'q{q}_r{r}_n{n}.json'), C, conf, f'base case, method: {how}')
        log[f'q{q}_r{r}_n{n}'] = how
    print(f'q={q}: base certificates written', flush=True)
  # new ququart table codes: subsets of the 65-line configuration need full-support weights;
  # use the recipe in GF(4)^5 (it returns blocks / absorption / search as appropriate)
  C = Ctx(2, 2, seed=2026)
  memo = {}
  for n in (59, 61, 62, 65):
    conf, how = recipe(C, 5, n, memo)
    write(os.path.join(out, 'table', f'q4_r5_n{n}.json'), C, conf, f'new codetables.de entry [[{n},{n-5},3]]_4; method: {how}')
    log[f'table_q4_n{n}'] = how
  for p, m in [(3, 1), (2, 2), (5, 1), (7, 1), (2, 3), (3, 2)]:
    C = Ctx(p, m, seed=2026)
    conf = absorbed_full(C, 5)
    write(os.path.join(out, 'maximal', f'q{C.q}_r5_n{len(conf)}.json'), C, conf, 'maximal length q^3+1 (Lemma 4.3)')
    log[f'maximal_q{C.q}'] = 'absorption'
  with open(os.path.join(out, 'generation_log.json'), 'w') as f:
    json.dump(log, f, indent=1, sort_keys=True)
  print('done', flush=True)


if __name__ == '__main__':
  main()
