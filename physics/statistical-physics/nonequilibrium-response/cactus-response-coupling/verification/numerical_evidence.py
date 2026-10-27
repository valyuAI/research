"""Floating-point evidence accompanying the cactus theorem (numpy and scipy).

Nothing proved in the paper depends on this script. It reproduces three groups of
observations with fixed seeds and writes numerical_evidence_results.json.

A. Monte Carlo of the undirected-edge Gumbel perturbation: exact (within sampling
   error) on cactus networks, visibly wrong on the diamond graph; independent noise
   on each arc is wrong even on a five-cycle.
B. Coherent-coupling linear programs: feasibility of a measure on uniquely
   constructable families with prescribed root laws, for series-parallel graphs
   and for graphs with a K4 minor.
C. Searches for violations of the Fancher-Horowitz conjecture itself on K4 and the
   two-root reduction on K5 (gradient ascent of random linear functionals).

Run: python3 -B numerical_evidence.py   (about ten minutes on a laptop)
"""

import collections
import itertools
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize


def arborescences(n, arcs, root):
  out = collections.defaultdict(list)
  for k, (s, _) in enumerate(arcs):
    out[s].append(k)
  others = [v for v in range(n) if v != root]
  res = []
  for choice in itertools.product(*[out[v] for v in others]):
    nxt = {v: arcs[k][1] for v, k in zip(others, choice)}
    ok = True
    for v in others:
      seen, u = set(), v
      while u != root:
        if u in seen:
          ok = False
          break
        seen.add(u)
        u = nxt[u]
      if not ok:
        break
    if ok:
      res.append(tuple(sorted(choice)))
  return res


class Net:
  def __init__(self, n, arcs):
    self.n, self.arcs, self.m = n, arcs, len(arcs)
    self.arbs = [arborescences(n, arcs, r) for r in range(n)]
    self.inc = []
    for a in self.arbs:
      mat = np.zeros((len(a), self.m))
      for i, t in enumerate(a):
        mat[i, list(t)] = 1
      self.inc.append(mat)
    base = self.n
    pw = np.array([base ** e for e in range(self.m)], dtype=np.int64)
    codes = [(mat.astype(np.int64) @ pw) for mat in self.inc]
    tot = codes[0].copy()
    for r in range(1, self.n):
      tot = tot[..., None] + codes[r].reshape((1,) * r + (-1,))
    flat = tot.ravel()
    _, inv, cnt = np.unique(flat, return_inverse=True, return_counts=True)
    once = np.where(cnt[inv] == 1)[0]
    self.uc = np.array(np.unravel_index(once, tot.shape)).T

  def laws(self, theta):
    out = []
    for mat in self.inc:
      lw = mat @ theta
      w = np.exp(lw - lw.max())
      out.append(w / w.sum())
    return out


def bidir(pairs):
  arcs = []
  for u, v in pairs:
    arcs += [(u, v), (v, u)]
  return arcs


GRAPHS = {
  'C5': (5, bidir([(i, (i + 1) % 5) for i in range(5)])),
  'C6': (6, bidir([(i, (i + 1) % 6) for i in range(6)])),
  'bowtie_plus_pendant': (6, bidir([(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0), (4, 5)])),
  'diamond': (4, bidir([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])),
  'K23': (5, bidir([(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)])),
  'C5_plus_chord': (5, bidir([(i, (i + 1) % 5) for i in range(5)] + [(0, 2)])),
  'K4': (4, [(i, j) for i in range(4) for j in range(4) if i != j]),
  'K4_subdivided': (5, bidir([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 4), (4, 3)])),
}


def gumbel_monte_carlo(name, samples, rng, per_arc=False):
  n, arcs = GRAPHS[name]
  net = Net(n, arcs)
  ucset = {tuple(int(x) for x in f) for f in net.uc}
  theta = rng.normal(size=net.m) * 1.5
  exact = net.laws(theta)
  uid = {}
  arc_edge = np.array([uid.setdefault(frozenset(a), len(uid)) for a in arcs])
  counts = [np.zeros(len(a)) for a in net.arbs]
  non_uc = 0
  gam = rng.gumbel(size=(samples, len(arcs) if per_arc else len(uid)))
  for s in range(samples):
    pert = theta - (gam[s] if per_arc else gam[s][arc_edge])
    fam = tuple(int(np.argmax(mat @ pert)) for mat in net.inc)
    for r in range(n):
      counts[r][fam[r]] += 1
    non_uc += fam not in ucset
  dev = max(float(np.abs(c / samples - p).max()) for c, p in zip(counts, exact))
  return {'samples': samples, 'non_uc_families': non_uc, 'max_abs_frequency_error': dev,
          'binomial_sd_bound': 0.5 / np.sqrt(samples)}


def coupling_lp(name, trials, rng):
  n, arcs = GRAPHS[name]
  net = Net(n, arcs)
  k = len(net.uc)
  sizes = [len(a) for a in net.arbs]
  off = np.cumsum([0] + sizes)
  rows = off[-1]
  aeq = np.zeros((rows, k))
  for a, f in enumerate(net.uc):
    for r in range(n):
      aeq[off[r] + f[r], a] = 1
  cost = np.concatenate([np.zeros(k), np.ones(2 * rows)])
  big = np.hstack([aeq, np.eye(rows), -np.eye(rows)])
  slacks = []
  for _ in range(trials):
    theta = rng.normal(size=net.m) * rng.choice([0.3, 1, 3])
    b = np.concatenate(net.laws(theta))
    res = linprog(cost, A_eq=big, b_eq=b, bounds=[(0, None)] * (k + 2 * rows), method='highs')
    slacks.append(float(res.fun))
  slacks = np.array(slacks)
  return {'uc_families': k, 'trials': trials, 'infeasible_trials': int((slacks > 1e-7).sum()),
          'max_l1_slack': float(slacks.max())}


def conjecture_search(name, trials, rng, roots=None):
  n, arcs = GRAPHS[name] if name in GRAPHS else (5, [(i, j) for i in range(5) for j in range(5) if i != j])
  roots = list(range(n)) if roots is None else roots
  net = Net(n, arcs) if roots == list(range(n)) else None
  if net is None:
    arbs = [arborescences(n, arcs, r) for r in roots]
    inc = []
    for a in arbs:
      mat = np.zeros((len(a), len(arcs)))
      for i, t in enumerate(a):
        mat[i, list(t)] = 1
      inc.append(mat)
    sets = [set(a) for a in arbs]
    uc = []
    for i, t in enumerate(arbs[0]):
      for j, tp in enumerate(arbs[1]):
        common = set(t) & set(tp)
        diff = sorted(set(t) ^ set(tp))
        need = len(t) - len(common)
        unique = True
        for x in itertools.combinations(diff, need):
          s = tuple(sorted(common | set(x)))
          sp = tuple(sorted(common | (set(diff) - set(x))))
          if s != t and s in sets[0] and sp in sets[1]:
            unique = False
            break
        if unique:
          uc.append((i, j))
    uc = np.array(uc)
  else:
    inc, uc = net.inc, net.uc
  m = len(arcs)
  best = -np.inf
  for t in range(trials):
    d = rng.normal(size=m)
    y = rng.normal(size=len(roots))
    y -= y.mean()
    c = np.outer(y, d)
    bound = sum(inc[r][uc[:, r]] @ c[r] for r in range(len(roots))).max()

    def neg(theta):
      v, g = 0.0, np.zeros(m)
      for r, mat in enumerate(inc):
        lw = mat @ theta
        w = np.exp(lw - lw.max())
        w /= w.sum()
        s = mat @ c[r]
        es = w @ s
        v += es
        g += (w * s) @ mat - es * (w @ mat)
      return -v, -g

    for _ in range(3):
      res = minimize(neg, rng.normal(size=m) * rng.choice([0.5, 2, 5]), jac=True, method='L-BFGS-B')
      best = max(best, -res.fun - bound)
  return {'trials': trials, 'max_gap_soft_minus_bound': float(best)}


def main():
  t0 = time.time()
  rng = np.random.default_rng(20261026)
  out = {'A_gumbel_monte_carlo': {}, 'B_coupling_lp': {}, 'C_conjecture_search': {}}
  for name in ['C6', 'bowtie_plus_pendant', 'diamond']:
    out['A_gumbel_monte_carlo'][name] = gumbel_monte_carlo(name, 50000, rng)
    print(name, out['A_gumbel_monte_carlo'][name], flush=True)
  out['A_gumbel_monte_carlo']['C5_independent_noise_per_arc'] = gumbel_monte_carlo('C5', 50000, rng, per_arc=True)
  print('C5 per-arc', out['A_gumbel_monte_carlo']['C5_independent_noise_per_arc'], flush=True)
  for name, trials in [('diamond', 100), ('K23', 60), ('C5_plus_chord', 60), ('K4', 100), ('K4_subdivided', 40)]:
    out['B_coupling_lp'][name] = coupling_lp(name, trials, rng)
    print(name, out['B_coupling_lp'][name], flush=True)
  out['C_conjecture_search']['K4_all_roots'] = conjecture_search('K4', 150, rng)
  print('K4', out['C_conjecture_search']['K4_all_roots'], flush=True)
  out['C_conjecture_search']['K5_roots_0_1'] = conjecture_search('K5', 150, rng, roots=[0, 1])
  print('K5 two roots', out['C_conjecture_search']['K5_roots_0_1'], flush=True)
  out['seconds'] = round(time.time() - t0, 1)
  Path(__file__).with_name('numerical_evidence_results.json').write_text(json.dumps(out, indent=2) + '\n')


if __name__ == '__main__':
  main()
