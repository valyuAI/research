"""Floating-point sanity check (not part of the proof): integrate the CTLN from a random perturbation of the
exact fixed point and report the distance to it over time.  Usage: python3 simulate.py G.json [T]"""
import json, sys
import numpy as np
d = json.load(open(sys.argv[1])); n = d['n']; E = set(map(tuple, d['edges']))
eps, delta, theta = 0.25, 0.5, 1.0
W = np.array([[0.0 if i == j else (-1 + eps if (j, i) in E else -1 - delta) for j in range(n)] for i in range(n)])
xs = np.linalg.solve(np.eye(n) - W, theta * np.ones(n))
f = lambda x: -x + np.maximum(W @ x + theta, 0)
rng = np.random.default_rng(0)
amp = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-4
x = xs * (1 + amp * rng.standard_normal(n))
T = float(sys.argv[2]) if len(sys.argv) > 2 else 4000; dt = 0.05; steps = int(T / dt)
print(f'n={n}  min x*={xs.min():.5f}  initial distance {np.linalg.norm(x - xs):.3e}')
for s in range(1, steps + 1):
  k1 = f(x); k2 = f(x + dt / 2 * k1); k3 = f(x + dt / 2 * k2); k4 = f(x + dt * k3)
  x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
  if s % (steps // 8) == 0:
    print(f't={s * dt:8.1f}  |x - x*| = {np.linalg.norm(x - xs):.3e}  min x = {x.min():.5f}', flush=True)
