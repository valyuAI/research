"""Recompute every number shown on screen in the explainer video, and write numbers.json for scenes.py.

Run: python3 check_numbers.py   (standard library only, about 10 seconds)

Running example: the driven triangle. States 0, 1, 2; clockwise hops v -> v+1 have rate 2, anticlockwise
hops v -> v-1 have rate 1. Edge k is the undirected edge {k, k+1} (indices mod 3).

 1. Trees rooted at each state, their weights (4, 2, 1), totals 7, 7, 7 and the steady state 1/3 each.
 2. A simulated trajectory (seeded) and its time fractions; the net clockwise current.
 3. The 1 percent nudge of the rate 0 -> 1: totals 7, 7.06, 7.04 and relative changes; the exact response
    (-10/21, 8/21, 2/21) and the fractions of tree weight using 0 -> 1 (0, 6/7, 4/7).
 4. Tree families: 27 families, 18 bags (multisets of arrows), 11 uniquely constructable (UC); chance that
    independent lotteries give a non-UC family; centred scores (building blocks) of every family.
 5. The staircase lambda_k = 2^-k, root windows, one turn round the ring multiplies by 1/8.
 6. The edge-token (Gumbel) coupling: exact probability of every family (7 families, 1/7 each), all UC;
    their building blocks average to the response; a seeded simulation of 400,000 draws.
 7. K4: 16 trees per root, 65,536 families, 5,955 bags, 346 UC; replay of the +1/-1 certificate on the
    64 (root, tree) pairs: every UC family scores >= 0, expectation -0.0566 under the root lotteries.
 8. Numbers quoted from ../verification/*.json (subdivided K4, numerical evidence).
"""

import itertools
import json
import math
import random
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
VER = HERE.parent / 'verification'
OUT = {}


def arborescences(n, rates, root):
  """All spanning trees pointing at root: one out-arc per non-root state, every state drains to root."""
  others = [v for v in range(n) if v != root]
  choices = [[(v, u) for (x, u) in rates if x == v] for v in others]
  trees = []
  for pick in itertools.product(*choices):
    nxt = dict(pick)
    ok = True
    for v in others:
      seen, x = set(), v
      while x != root:
        if x in seen:
          ok = False
          break
        seen.add(x)
        x = nxt[x]
      if not ok:
        break
    if ok:
      trees.append(tuple(sorted(pick)))
  return trees


def weight(tree, rates):
  w = Fr(1)
  for a in tree:
    w *= rates[a]
  return w


# 1. Triangle trees -----------------------------------------------------------------------------------
N = 3
RATES = {}
for v in range(N):
  RATES[(v, (v + 1) % N)] = Fr(2)
  RATES[(v, (v - 1) % N)] = Fr(1)


def deleted_edge(tree):
  """On a ring, a tree misses exactly one undirected edge {k, k+1}; return k."""
  used = {frozenset(a) for a in tree}
  miss = [k for k in range(N) if frozenset((k, (k + 1) % N)) not in used]
  assert len(miss) == 1
  return miss[0]


TREES = {r: arborescences(N, RATES, r) for r in range(N)}
TOTAL = {r: sum(weight(t, RATES) for t in TREES[r]) for r in range(N)}
P = {r: {t: weight(t, RATES) / TOTAL[r] for t in TREES[r]} for r in range(N)}
PI = {r: TOTAL[r] / sum(TOTAL.values()) for r in range(N)}
print('1. trees per root')
for r in range(N):
  for t in sorted(TREES[r], key=lambda t: -weight(t, RATES)):
    print(f'   root {r}: deletes edge {deleted_edge(t)}  arrows {t}  weight {weight(t, RATES)}  prob {P[r][t]}')
print('   totals', [str(TOTAL[r]) for r in range(N)], ' pi', [str(PI[r]) for r in range(N)])
assert [TOTAL[r] for r in range(N)] == [7, 7, 7] and all(PI[r] == Fr(1, 3) for r in range(N))
root0 = {deleted_edge(t): (str(weight(t, RATES)), str(P[0][t]), [list(a) for a in t]) for t in TREES[0]}
assert {k: v[:2] for k, v in root0.items()} == {0: ('4', '4/7'), 1: ('2', '2/7'), 2: ('1', '1/7')}
OUT['root0_trees'] = root0
# Every root: the edge just after the root (clockwise) is deleted with prob 4/7, then 2/7, then 1/7.
for r in range(N):
  for t in TREES[r]:
    assert P[r][t] == {0: Fr(4, 7), 1: Fr(2, 7), 2: Fr(1, 7)}[(deleted_edge(t) - r) % N]

# 2. Simulation -----------------------------------------------------------------------------------------
rng = random.Random(20261026)
state, t, hops, occ = 0, 0.0, [], [0.0, 0.0, 0.0]
checkpoints, marks = [], [2, 5, 10, 20, 40, 80, 150, 300, 600, 1200, 2500]
net = 0
while t < marks[-1]:
  hold = rng.expovariate(3.0)
  nxt = (state + 1) % N if rng.random() < 2 / 3 else (state - 1) % N
  for m in marks:
    if t < m <= t + hold:
      o = occ[:]
      o[state] += m - t
      checkpoints.append([m, [x / m for x in o]])
  occ[state] += hold
  t += hold
  net += 1 if nxt == (state + 1) % N else -1
  if len(hops) < 40:
    hops.append([state, hold, nxt])
  state = nxt
final = checkpoints[-1][1]
print('2. simulation: time fractions at t =', marks[-1], [round(x, 3) for x in final],
      ' net clockwise hops per unit time', round(net / t, 3), '(expected 1)')
assert all(abs(x - 1 / 3) < 0.02 for x in final)
OUT['sim_hops'] = hops
OUT['sim_checkpoints'] = checkpoints
# Net current: each state sends 2 * pi clockwise and 1 * pi back, so 1/3 per second per edge, i.e. 1 net
# clockwise hop per unit time in total over the three edges.

# 3. The nudge ----------------------------------------------------------------------------------------
KNOB = (0, 1)
nudged = dict(RATES)
nudged[KNOB] = RATES[KNOB] * Fr(101, 100)
TOT1 = {r: sum(weight(t, nudged) for t in TREES[r]) for r in range(N)}
PI1 = {r: TOT1[r] / sum(TOT1.values()) for r in range(N)}
rel = {r: PI1[r] / PI[r] - 1 for r in range(N)}
print('3. 1% nudge of 0->1: totals', [float(TOT1[r]) for r in range(N)], ' new pi',
      [round(float(PI1[r]), 5) for r in range(N)], ' relative change (%)', [round(100 * float(rel[r]), 3) for r in range(N)])
assert [TOT1[r] for r in range(N)] == [Fr(7), Fr(706, 100), Fr(704, 100)]
use = {r: sum(P[r][t] for t in TREES[r] if KNOB in t) for r in range(N)}
avg_use = sum(PI[r] * use[r] for r in range(N))
resp = {r: use[r] - avg_use for r in range(N)}
print('   share of tree weight using 0->1', [str(use[r]) for r in range(N)], ' average', avg_use,
      ' response', [str(resp[r]) for r in range(N)])
assert [use[r] for r in range(N)] == [0, Fr(6, 7), Fr(4, 7)] and avg_use == Fr(10, 21)
assert [resp[r] for r in range(N)] == [Fr(-10, 21), Fr(8, 21), Fr(2, 21)]
# The exact derivative agrees with a tiny finite difference.
h = Fr(1, 10 ** 9)
nud = dict(RATES)
nud[KNOB] = RATES[KNOB] * (1 + h)
T2 = {r: sum(weight(t, nud) for t in TREES[r]) for r in range(N)}
for r in range(N):
  fd = (math.log(T2[r] / sum(T2.values())) - math.log(PI[r])) / float(h)
  assert abs(fd - float(resp[r])) < 1e-6
OUT['nudge'] = {'totals': [str(float(TOT1[r])) for r in range(N)], 'rel_pct': [100 * float(rel[r]) for r in range(N)],
                'use': [str(use[r]) for r in range(N)], 'response': [str(resp[r]) for r in range(N)]}

# 4. Families, bags, UC -----------------------------------------------------------------------------------
FAMS = list(itertools.product(*[TREES[r] for r in range(N)]))


def bag(fam):
  out = {}
  for tr in fam:
    for a in tr:
      out[a] = out.get(a, 0) + 1
  return tuple(sorted(out.items()))


bags = {}
for f in FAMS:
  bags.setdefault(bag(f), []).append(f)
UC = [f for f in FAMS if len(bags[bag(f)]) == 1]
label = lambda f: tuple(deleted_edge(t) for t in f)  # noqa: E731
print(f'4. families {len(FAMS)}, bags {len(bags)}, UC {len(UC)}')
assert (len(FAMS), len(bags), len(UC)) == (27, 18, 11)
print('   UC families (deleted edge at roots 0,1,2):', sorted(label(f) for f in UC))
lookalike = [sorted(label(f) for f in fs) for fs in bags.values() if len(fs) > 1]
print('   look-alike groups:', lookalike)
p_indep_nonuc = sum(P[0][f[0]] * P[1][f[1]] * P[2][f[2]] for f in FAMS if len(bags[bag(f)]) > 1)
print('   independent lotteries land on a look-alike family with probability', p_indep_nonuc, '=',
      round(float(p_indep_nonuc), 3))


def score(f):
  g = [1 if KNOB in f[r] else 0 for r in range(N)]
  m = sum(PI[r] * g[r] for r in range(N))
  return tuple(Fr(g[r]) - m for r in range(N))


blocks = {label(f): score(f) for f in FAMS}
uc_points = sorted({(blocks[label(f)][0], blocks[label(f)][1]) for f in UC})
all_points = sorted({(b[0], b[1]) for b in blocks.values()})
print('   building blocks (centred scores, states 0 and 1) of UC families:', [(str(a), str(b)) for a, b in uc_points])
print('   ... of all families:', [(str(a), str(b)) for a, b in all_points])
# Eq. (5): independent-lottery average of the building blocks equals the response.
avg5 = [sum(P[0][f[0]] * P[1][f[1]] * P[2][f[2]] * score(f)[r] for f in FAMS) for r in range(N)]
assert avg5 == [resp[r] for r in range(N)]
ex = next(f for f in FAMS if label(f) == (0, 1, 2))
print('   example family (0,1,2): uses 0->1 at roots', [int(KNOB in ex[r]) for r in range(N)], ' block',
      [str(x) for x in score(ex)], ' independent prob', P[0][ex[0]] * P[1][ex[1]] * P[2][ex[2]])
OUT['uc_labels'] = sorted(label(f) for f in UC)
OUT['lookalike'] = lookalike
OUT['p_indep_nonuc'] = str(p_indep_nonuc)
OUT['family_trees'] = {','.join(map(str, label(f))): [[list(a) for a in tr] for tr in f] for f in FAMS}

# 5. Staircase -------------------------------------------------------------------------------------------
a = {v: RATES[(v, (v - 1) % N)] for v in range(N)}
b = {v: RATES[(v, (v + 1) % N)] for v in range(N)}
lam = [Fr(1)]
for k in range(1, 6):
  lam.append(lam[-1] * a[k % N] / b[k % N])
print('5. staircase lambda_0..5', [str(x) for x in lam], ' one turn:', lam[3] / lam[0])
assert lam[:5] == [1, Fr(1, 2), Fr(1, 4), Fr(1, 8), Fr(1, 16)] and lam[3] / lam[0] == Fr(1, 8)
for r in range(N):
  for t in TREES[r]:
    k = deleted_edge(t)
    kk = next(x for x in range(r, r + N) if x % N == k)  # position of the cut inside root r's window
    ratio = weight(t, RATES) / lam[kk]
    assert ratio == weight(TREES[r][0], RATES) / lam[next(x for x in range(r, r + N) if x % N == deleted_edge(TREES[r][0]))]


# 6. Edge tokens: exact family law via the exponential-race form of the Gumbel-max trick -----------------
# Root r picks the edge e minimising E_e / w_r(e) with E_e = exp(-gamma_e) independent Exp(1).
def wr(r):
  return {k % N: lam[k] for k in range(r, r + N)}


def clip(poly, c):
  """Keep the part of a polygon (points (x0, x1), x2 = 1 - x0 - x1) where c . (x0, x1, x2) <= 0."""
  val = lambda p: c[0] * p[0] + c[1] * p[1] + c[2] * (1 - p[0] - p[1])  # noqa: E731
  out = []
  for i in range(len(poly)):
    p, q = poly[i], poly[(i + 1) % len(poly)]
    vp, vq = val(p), val(q)
    if vp <= 0:
      out.append(p)
    if (vp < 0 < vq) or (vq < 0 < vp):
      s = vp / (vp - vq)
      out.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
  return out


def cone_prob(poly):
  """P(E in cone) for i.i.d. Exp(1): sum over fan triangles of |det| of the vertices on x0 + x1 + x2 = 1."""
  tot = Fr(0)
  pts = [(p[0], p[1], 1 - p[0] - p[1]) for p in poly]
  for i in range(1, len(pts) - 1):
    u, v, w = pts[0], pts[i], pts[i + 1]
    det = (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))
    tot += abs(det)
  return tot


exact = {}
for fam in itertools.product(range(N), repeat=N):
  poly = [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(0), Fr(0))]
  for r, e in enumerate(fam):
    w = wr(r)
    for f in range(N):
      if f != e:
        c = [Fr(0)] * 3
        c[e] += w[f]
        c[f] -= w[e]
        poly = clip(poly, c)
        if len(poly) < 3:
          break
    if len(poly) < 3:
      break
  pr = cone_prob(poly) if len(poly) >= 3 else Fr(0)
  if pr:
    exact[fam] = pr
print('6. edge-token family law:', {k: str(v) for k, v in sorted(exact.items())})
assert sum(exact.values()) == 1
assert sorted(exact) == sorted([(0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 0), (1, 1, 2), (0, 2, 2), (0, 1, 2)])
assert all(v == Fr(1, 7) for v in exact.values())
assert all(k in OUT['uc_labels'] for k in exact)
for r in range(N):  # marginals are the root lotteries
  for e in range(N):
    m = sum(v for k, v in exact.items() if k[r] == e)
    assert m == {0: Fr(4, 7), 1: Fr(2, 7), 2: Fr(1, 7)}[(e - r) % N]
avg6 = [sum(v * blocks[k][r] for k, v in exact.items()) for r in range(N)]
assert avg6 == [resp[r] for r in range(N)]
groups = {}
for k in exact:
  groups.setdefault((blocks[k][0], blocks[k][1]), []).append(k)
print('   blocks of the 7 families (state 0, state 1):', {(str(x), str(y)): v for (x, y), v in groups.items()})
print('   average of their blocks:', [str(x) for x in avg6])
OUT['coupling_groups'] = [[[str(x), str(y)], v] for (x, y), v in sorted(groups.items())]

# Monte Carlo of the same construction, and demo draws for the bar animation.
rng = random.Random(7)
LN2 = math.log(2)


def draw(rng):
  g = [-math.log(-math.log(rng.random())) for _ in range(N)]
  fam = tuple(max(range(r, r + N), key=lambda k: math.log(lam[k]) + g[k % N]) % N for r in range(N))
  return g, fam


counts = {k: 0 for k in exact}
root0 = [0, 0, 0]
tally_marks = [7, 35, 70, 140, 350, 700, 1400, 3500, 7000, 20000, 70000, 400000]
tally = []
demo = []
for i in range(1, 400001):
  g, fam = draw(rng)
  counts[fam] += 1
  root0[fam[0]] += 1
  if len(demo) < 3 and min(g) > -0.9 and max(g) < 2.2 and fam not in [d[1] for d in demo]:
    demo.append((g, fam))
  if i in tally_marks:
    tally.append([i, [counts[k] for k in sorted(exact)], root0[:]])
freqs = {k: v / 400000 for k, v in counts.items()}
print('   400,000 draws: family frequencies', {k: round(v, 4) for k, v in sorted(freqs.items())},
      ' min', round(min(freqs.values()), 4), ' max', round(max(freqs.values()), 4))
print('   root 0 frequencies', [round(x / 400000, 4) for x in root0], ' exact 4/7, 2/7, 1/7 =',
      [round(4 / 7, 4), round(2 / 7, 4), round(1 / 7, 4)])
assert all(abs(v - 1 / 7) < 0.002 for v in freqs.values())
print('   demo draws (gamma per edge -> family):', [([round(x, 2) for x in g], f) for g, f in demo])
OUT['families_sorted'] = sorted(exact)
OUT['tally'] = tally
OUT['mc_range'] = [round(min(freqs.values()), 3), round(max(freqs.values()), 3)]
OUT['demo_draws'] = [[g, list(f)] for g, f in demo]

# 7. K4 obstruction replay -------------------------------------------------------------------------------
cert = json.loads((VER / 'k4_no_coupling_certificate.json').read_text())
K4R = {tuple(map(int, k.split('->'))): Fr(v) for k, v in cert['rates'].items()}
K4T = {r: arborescences(4, K4R, r) for r in range(4)}
assert all(len(K4T[r]) == 16 for r in range(4))
k4bags = {}
for f in itertools.product(*[K4T[r] for r in range(4)]):
  k4bags.setdefault(bag(f), []).append(f)
k4uc = [fs[0] for fs in k4bags.values() if len(fs) == 1]


def key(r, tr):
  return f'root{r}:' + ','.join(f'{u}>{v}' for u, v in sorted(tr))


y = {k: int(v) for k, v in cert['y'].items()}
assert len(y) == 64
min_uc = min(sum(y[key(r, f[r])] for r in range(4)) for f in k4uc)
K4tot = {r: sum(weight(t, K4R) for t in K4T[r]) for r in range(4)}
expv = sum(y[key(r, t)] * weight(t, K4R) / K4tot[r] for r in range(4) for t in K4T[r])
print(f'7. K4: trees per root 16, families {16 ** 4}, bags {len(k4bags)}, UC {len(k4uc)}, '
      f'min UC score {min_uc}, expectation {expv} = {float(expv):.4f}')
assert (len(k4bags), len(k4uc), min_uc) == (5955, 346, 0) and expv == Fr(cert['b_dot_y'])
rows = {r: sorted(K4T[r], key=lambda t: key(r, t)) for r in range(4)}
row_avg = [sum(y[key(r, t)] * weight(t, K4R) / K4tot[r] for t in rows[r]) for r in range(4)]
assert sum(row_avg) == expv
uc_scores = sorted({sum(y[key(r, f[r])] for r in range(4)) for f in k4uc})
sample = next(f for f in sorted(k4uc, key=lambda f: [key(r, f[r]) for r in range(4)])
              if sum(y[key(r, f[r])] for r in range(4)) == 0)
print('   row averages', [round(float(x), 4) for x in row_avg], ' UC family scores take values', uc_scores,
      ' sample UC family cells', [rows[r].index(sample[r]) for r in range(4)])
assert min(uc_scores) == 0
OUT['k4'] = {'uc': len(k4uc), 'bags': len(k4bags), 'expect': round(float(expv), 4),
             'grid': [[y[key(r, t)] for t in rows[r]] for r in range(4)],
             'row_avg': [round(float(x), 4) for x in row_avg], 'uc_scores': uc_scores,
             'sample': [rows[r].index(sample[r]) for r in range(4)]}

# 8. Quoted from verification outputs --------------------------------------------------------------------
sub = json.loads((VER / 'k4_subdivision_results.json').read_text())
num = json.loads((VER / 'numerical_evidence_results.json').read_text())
lem = json.loads((VER / 'cactus_lemmas_results.json').read_text())
assert sub['uniquely_constructable_families'] == 984 and sub['equals_k4_value'] and sub['no_coupling_proved']
assert lem['all_passed'] and len(lem['block_factorisation']) == 5 and max(int(k[2:]) for k in lem['cycle_identity']) == 8
diam = num['A_gumbel_monte_carlo']['diamond']['max_abs_frequency_error']
k4s = num['C_conjecture_search']['K4_all_roots']
k5s = num['C_conjecture_search']['K5_roots_0_1']
lpd = num['B_coupling_lp']['diamond']
print(f'8. subdivided K4: {sub["uniquely_constructable_families"]} UC families, same negative value: {sub["equals_k4_value"]}')
print(f'   diamond: edge-token error {diam:.3f}; LP found couplings in {lpd["trials"] - lpd["infeasible_trials"]}'
      f'/{lpd["trials"]} trials')
print(f'   conjecture searches: K4 {k4s["trials"]} runs, max gap {k4s["max_gap_soft_minus_bound"]:.1e}; '
      f'K5 {k5s["trials"]} runs, max gap {k5s["max_gap_soft_minus_bound"]:.1e} (negative = no violation)')
assert round(diam, 2) == 0.06 and k4s['trials'] == 150 and k4s['max_gap_soft_minus_bound'] < 0
assert k5s['trials'] == 150 and k5s['max_gap_soft_minus_bound'] < 0

(HERE / 'numbers.json').write_text(json.dumps(OUT, indent=1, default=list))
print('all checks passed; wrote numbers.json')
