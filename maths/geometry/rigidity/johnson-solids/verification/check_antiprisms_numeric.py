"""Floating-point cross-check (numpy): point-hyperplane rigidity matrix of the n-antiprism has corank 6
(first-order rigid) for 3 <= n < N. usage: python3 check_antiprisms_numeric.py N [height]"""
import numpy as np, sys
def antiprism(n):
  R = 1/(2*np.sin(np.pi/n)); h2 = 1 - 2*R*R*(1-np.cos(np.pi/n)); h = float(sys.argv[2]) if len(sys.argv) > 2 else np.sqrt(h2)
  top = [(R*np.cos(2*np.pi*k/n), R*np.sin(2*np.pi*k/n), h/2) for k in range(n)]
  bot = [(R*np.cos(2*np.pi*(k+.5)/n), R*np.sin(2*np.pi*(k+.5)/n), -h/2) for k in range(n)]
  X = np.array(top+bot)
  F = [list(range(n)), list(range(n, 2*n))]
  for k in range(n):
    F.append([k, (k+1)%n, n+k]); F.append([n+k, (k+1)%n, n+(k+1)%n])
  return X, F
def rig(X, F):
  A = []
  for f in F:
    a, *_ = np.linalg.lstsq(X[f], np.ones(len(f)), rcond=None); A.append(a)
  E = set()
  for f in F:
    for i in range(len(f)): E.add(tuple(sorted((f[i], f[(i+1)%len(f)]))))
  E = sorted(E); nV = len(X)
  rows = []
  for i,j in E:
    r = np.zeros(3*(nV+len(F))); d = X[i]-X[j]; r[3*i:3*i+3]=d; r[3*j:3*j+3]=-d; rows.append(r)
  for s,f in enumerate(F):
    for i in f:
      r = np.zeros(3*(nV+len(F))); r[3*i:3*i+3]=A[s]; r[3*nV+3*s:3*nV+3*s+3]=X[i]; rows.append(r)
  M = np.array(rows); sv = np.linalg.svd(M, compute_uv=False)
  return M.shape, sv
for n in range(3, int(sys.argv[1])):
  X, F = antiprism(n); sh, sv = rig(X, F)
  corank = sh[1] - int((sv > 1e-9).sum())
  print(n, sh, 'flex', corank-6, 'smallest sv %.2e' % sorted(sv)[0] if len(sv) else '', flush=True)
