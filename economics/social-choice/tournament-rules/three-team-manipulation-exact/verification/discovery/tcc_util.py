"""Top-cycle helper: variables (class, orbit) lying outside the top cycle of the class representative.
Orbit numbering follows gen_snm.c: orbits are numbered in order of their smallest vertex."""
NCLASSES = {4: 4, 12: 5, 56: 6, 456: 7, 6880: 8}

def _adj(code, n):
  pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
  a = [[0] * n for _ in range(n)]
  for t, (i, j) in enumerate(pairs):
    if code >> t & 1: a[i][j] = 1
    else: a[j][i] = 1
  return a

def _refine(adj, n):
  col = [sum(adj[v]) for v in range(n)]
  for _ in range(n):
    sig = [(col[v], tuple(sorted(col[w] for w in range(n) if adj[v][w])), tuple(sorted(col[w] for w in range(n) if adj[w][v]))) for v in range(n)]
    keys = sorted(set(sig)); new = [keys.index(sig[v]) for v in range(n)]
    if len(set(new)) == len(set(col)):
      col = new; break
    col = new
  return col

def orbits(adj, n):
  col = _refine(adj, n)
  groups = {}
  for v in range(n): groups.setdefault(col[v], []).append(v)
  par = list(range(n))
  def find(a):
    while par[a] != a: a = par[a]
    return a
  def rec(i, p, used):
    if i == n:
      for v in range(n):
        x, y = find(v), find(p[v])
        if x != y: par[max(x, y)] = min(x, y)
      return
    for w in groups[col[i]]:
      if w in used: continue
      if all(adj[i][j] == adj[w][p[j]] for j in range(i)):
        p.append(w); used.add(w); rec(i + 1, p, used); p.pop(); used.discard(w)
  rec(0, [], set())
  ids, out = {}, []
  for v in range(n):
    r = find(v)
    if r not in ids: ids[r] = len(ids)
    out.append(ids[r])
  return out

def top_cycle(adj, n):
  top = set()
  for v in range(n):
    seen = {v}; st = [v]
    while st:
      u = st.pop()
      for w in range(n):
        if adj[u][w] and w not in seen: seen.add(w); st.append(w)
    if len(seen) == n: top.add(v)
  return top

def tcc_zero_vars(pre, classes, n):
  out = []; v0 = 0
  for code, norb, cw, sizes in classes:
    adj = _adj(code, n); orb = orbits(adj, n); top = top_cycle(adj, n)
    assert max(orb) + 1 == norb and all(sum(1 for v in range(n) if orb[v] == o) == sizes[o] for o in range(norb))
    for o in range(norb):
      if not any(orb[v] == o for v in top): out.append(v0 + o)
    v0 += norb
  return out
