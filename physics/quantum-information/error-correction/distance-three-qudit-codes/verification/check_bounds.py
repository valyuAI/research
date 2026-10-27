"""Arithmetic of the upper bounds (standard library only, no assertions).

1. mu_q(s): maximum size of a partial line spread of PG(s-1,q) (Lemma 3.2), and the
   inequality 2t + mu_q(r-t) <= mu_q(r) for 1 <= t <= r (Lemma 3.3), checked for all prime
   powers 3 <= q <= 32 and 4 <= r <= 40.
2. Theorem 3.4 / Corollary 5.2: for every open codetables.de entry [[n,k]]_q in the snapshot
   (the twelve compared entries, q = 3,4,5,7; 25 Oct 2026), the largest d allowed by
      n <= max_{0<=t<=r} ((d-1) t + m_q(d, r-t)),  r = n-k,
   where m_q(3,s) = mu_q(s), m_q(d,s) <= 1 + m_q(d-1,s-2) (projection from a line),
   m_q(4,6) <= q^2+1 for odd q (Thas), m_q(d,s) <= floor(s/2) if s < 2(d-1).
   Entries whose upper bound drops are listed, together with the new lower bounds from the
   stored certificates ([[59,54]]_4, [[61,56]]_4, [[62,57]]_4, [[65,60]]_4: d >= 3).
Writes check_bounds_results.json.
"""
import json, os, sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))


def mu(q, s):
  if s <= 1:
    return 0
  if s % 2 == 0:
    return (q ** s - 1) // (q * q - 1)
  return (q ** s - q ** 3) // (q * q - 1) + 1


@lru_cache(None)
def mbound(q, d, s):
  if s < 2:
    return 0
  if d <= 2:
    return 10 ** 9   # no constraint beyond dimension two for each plane
  if d == 3:
    return mu(q, s)
  if s < 2 * (d - 1):
    return s // 2
  b = min(mbound(q, d - 1, s), 1 + mbound(q, d - 1, s - 2))
  if d == 4 and s == 6 and q % 2 == 1:
    b = min(b, q * q + 1)
  return b


def nmax(q, d, r):
  return max((d - 1) * t + mbound(q, d, r - t) for t in range(0, r + 1))


def main():
  out = {}
  # 1. Lemma 3.3
  pp = [q for q in range(3, 33) if any(q == p ** e for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31) for e in range(1, 6))]
  viol = [(q, r, t) for q in pp for r in range(4, 41) for t in range(1, r + 1) if 2 * t + mu(q, r - t) > mu(q, r)]
  out['lemma_3_3_checked'] = {'prime_powers': pp, 'r_range': [4, 40], 'violations': viol}
  # check also that nmax(q,3,r) == mu(q,r) for q >= 3
  out['theorem_3_4_nmax_equals_mu'] = all(nmax(q, 3, r) == mu(q, r) for q in pp for r in range(4, 41))
  # 2. table comparison
  snap = json.load(open(os.path.join(HERE, 'codetables_snapshot_2026-10-25.json')))
  improved = []
  for qs, tab in snap['tables'].items():
    q = int(qs)
    for key, (lo, hi) in tab.items():
      n, k = map(int, key.split(','))
      if k == 0 or lo == hi:
        continue
      r = n - k
      d = hi
      while d > lo and n > nmax(q, d, r):
        d -= 1
      if d < hi:
        improved.append({'q': q, 'n': n, 'k': k, 'table_lower': lo, 'table_upper': hi, 'new_upper': d,
                         'exact_now': d == lo})
  new_lower = []
  for n in (59, 61, 62, 65):
    lo, hi = snap['tables']['4'][f'{n},{n-5}']
    new_lower.append({'q': 4, 'n': n, 'k': n - 5, 'table_lower': lo, 'table_upper': hi, 'new_lower': 3,
                      'exact_now': hi == 3, 'certificate': f'certificates/table/q4_r5_n{n}.json'})
  out['upper_bound_improvements'] = sorted(improved, key=lambda e: (e['q'], e['n']))
  out['lower_bound_improvements'] = new_lower
  out['entries_improved'] = len(improved) + len(new_lower)
  out['entries_now_exact'] = sum(e['exact_now'] for e in improved + new_lower)
  # 3. Proposition 5.3: F_2-additive ququart stabilizers (rho = 2r, 4-dim subspaces of F_2^s)
  def a(s):  # upper bound on pairwise trivially intersecting 4-dim subspaces of F_2^s
    if s < 4: return 0
    if s <= 7: return 1
    if s == 10: return 65          # Nastase-Sissokho, JCTA 152 (2017), Theorem 5
    return (2 ** s - 1) // 15      # point count (s = 8, 9)
  def m_add(d, s):  # any <= d-1 of the 4-dim subspaces independent
    if d == 3: return a(s)
    if d == 4: return min(a(s), 1 + a(s - 4)) if s >= 4 else 0
  add = {}
  for (n, r, d) in [(66, 5, 3), (67, 7, 4)]:
    rho = 2 * r
    terms = [(d - 1) * tau + m_add(d, rho - tau) for tau in range(rho + 1)]
    add[f'[[{n},{n-r},{d}]]_4'] = {'max_bound': max(terms), 'excluded': n > max(terms), 'terms': terms}
  out['additive_ququart_prop_5_4'] = add
  with open(os.path.join(HERE, 'check_bounds_results.json'), 'w') as f:
    json.dump(out, f, indent=1)
  print('Lemma 3.3 violations:', viol)
  print('nmax(q,3,r) == mu_q(r) for all checked q>=3, r>=4:', out['theorem_3_4_nmax_equals_mu'])
  for e in out['upper_bound_improvements']:
    print('upper  q=%(q)d [[%(n)d,%(k)d]] table %(table_lower)d-%(table_upper)d -> d <= %(new_upper)d exact=%(exact_now)s' % e)
  for e in new_lower:
    print('lower  q=%(q)d [[%(n)d,%(k)d]] table %(table_lower)d-%(table_upper)d -> d >= %(new_lower)d exact=%(exact_now)s' % e)
  print('entries improved:', out['entries_improved'], 'now exact:', out['entries_now_exact'])
  for k_, v in add.items():
    print('additive ququart', k_, 'max bound', v['max_bound'], 'excluded', v['excluded'])
  ok = not viol and out['theorem_3_4_nmax_equals_mu'] and all(v['excluded'] for v in add.values())
  sys.exit(0 if ok else 1)


if __name__ == '__main__':
  main()
