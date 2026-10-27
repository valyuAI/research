"""Export exact rule (from exact_rule.py pickle + .vars) to the JSON certificate format of verify_rule.py."""
import sys, json, pickle
pre, n, k, mode, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
import os
d = pickle.load(open(os.environ.get('PKL', pre + '_exactrule.pkl'), 'rb'))
x, alpha = d['x'], d['alpha']
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
classes = []
with open(pre + '.vars') as f:
  ncls, nvars = map(int, f.readline().split())
  v0 = 0
  for line in f:
    p = line.split(); code, norb = int(p[0]), int(p[1])
    adj = [[0] * n for _ in range(n)]
    for t, (a, b) in enumerate(pairs):
      if code >> t & 1: adj[a][b] = 1
      else: adj[b][a] = 1
    classes.append((code, norb, v0)); v0 += norb
# orbit of each vertex: recompute via brute force automorphisms (independent of C ordering is not needed:
# we need the C program's orbit numbering to expand values). Re-derive orbits exactly as gen_snm does.
import itertools
def refine(adj):
  col = [sum(adj[v]) for v in range(n)]
  for _ in range(n):
    sig = [(col[v], tuple(sorted(col[w] for w in range(n) if adj[v][w])), tuple(sorted(col[w] for w in range(n) if adj[w][v]))) for v in range(n)]
    keys = sorted(set(sig)); new = [keys.index(sig[v]) for v in range(n)]
    if len(set(new)) == len(set(col)): col = new; break
    col = new
  return col
def orbits(adj):
  col = refine(adj)
  groups = {}
  for v in range(n): groups.setdefault(col[v], []).append(v)
  perms = []
  # automorphisms preserve colours: search maps colour class -> itself
  verts = list(range(n))
  def rec(i, p, used):
    if i == n:
      perms.append(tuple(p)); return
    v = verts[i]
    for w in groups[col[v]]:
      if w in used: continue
      if all(adj[v][verts[j]] == adj[w][p[j]] for j in range(i)) and all(adj[verts[j]][v] == adj[p[j]][w] for j in range(i)):
        p.append(w); used.add(w); rec(i + 1, p, used); p.pop(); used.discard(w)
  rec(0, [], set())
  par = list(range(n))
  def find(a):
    while par[a] != a: a = par[a]
    return a
  for p in perms:
    for v in range(n):
      a, b = find(v), find(p[v])
      if a != b: par[max(a, b)] = min(a, b)
  roots = []
  for v in range(n):
    if find(v) not in roots: roots.append(find(v))
  return [roots.index(find(v)) for v in range(n)]
out_classes = []
for code, norb, v0 in classes:
  adj = [[0] * n for _ in range(n)]
  for t, (a, b) in enumerate(pairs):
    if code >> t & 1: adj[a][b] = 1
    else: adj[b][a] = 1
  orb = orbits(adj)
  assert max(orb) + 1 == norb
  r = [str(x[v0 + orb[v]]) for v in range(n)]
  s = ''.join('1' if adj[a][b] else '0' for a, b in pairs)
  out_classes.append({'T': s, 'r': r})
obj = {'n': n, 'k': k, 'mode': mode, 'alpha': str(alpha if alpha is not None else sys.argv[6] if len(sys.argv) > 6 else '1')}
for flag in filter(None, os.environ.get('FLAGS', '').split(',')): obj[flag] = True
obj['classes'] = out_classes
json.dump(obj, open(out, 'w'))
print('wrote', out, len(out_classes), 'classes')
