"""Assemble results/classification.json and the LaTeX table (results/table.tex) from the checker outputs.
Also recomputes, for each Minkowski flex, the number of distinct vertices and the dimension of both summands."""
import json
import nfsolid


def need(cond, msg='check failed'):
  """Explicit check that is not removed by python -O."""
  if not cond:
    raise ValueError(msg)

c1 = json.load(open('results/check1_rank.json'))
c2 = json.load(open('results/check2.json'))
fin = json.load(open('results/flex_finite.json'))
so = json.load(open('results/second_order.json'))
dims = json.load(open('results/exact_flex_dims.json'))


def summand_shape(k, s1_edges):
  name, K, V, F = nfsolid.load('data/J%02d.json' % k)
  P, A, E, rep = nfsolid.validate(K, V, F)
  S1 = set(tuple(sorted(e)) for e in s1_edges)
  zero3 = (K.zero, K.zero, K.zero)
  adj = {}
  for a, b in E:
    adj.setdefault(a, []).append(b)
    adj.setdefault(b, []).append(a)
  s1 = {0: zero3}
  stack = [0]
  while stack:
    a = stack.pop()
    for b in adj[a]:
      if b not in s1:
        d = K.vsub(P[b], P[a]) if tuple(sorted((a, b))) in S1 else zero3
        s1[b] = tuple(K.add(x, y) for x, y in zip(s1[a], d))
        stack.append(b)
  s2 = {v: K.vsub(P[v], s1[v]) for v in s1}
  def shape(pts):
    pts = list({tuple(tuple(c) if not hasattr(K, 'K') else c for c in p) for p in pts})
    base = pts[0]
    vecs = [K.vsub(p, base) for p in pts[1:]]
    from minkflex import rank_vectors
    return len(pts), rank_vectors(K, vecs)
  return shape(s1.values()), shape(s2.values())


def parallel_edges(k):
  name, K, V, F = nfsolid.load('data/J%02d.json' % k)
  P, A, E, rep = nfsolid.validate(K, V, F)
  vecs = [K.vsub(P[b], P[a]) for a, b in E]
  for i in range(len(vecs)):
    for j in range(i + 1, len(vecs)):
      if all(K.is0(x) for x in K.cross(vecs[i], vecs[j])):
        return True
  return False


rows = []
out = {}
for k in range(1, 93):
  r1, r2 = c1[str(k)], c2[str(k)]
  ub = r1['flex_dim_upper_bound']
  entry = {'name': r1['name'], 'V': r1['V'], 'E': r1['E'], 'F': r1['F'], 'field_degree': r1['field_degree'],
           'flex_dim_upper_bound_mod_p': ub, 'checker2': r2['verdict']}
  if ub == 0:
    need(r2['verdict'] == 'first-order rigid', "r2['verdict'] == 'first-order rigid'")
    entry['class'] = 'first-order rigid'
    entry['flex_dim'] = 0
  else:
    need(r2['verdict'] == 'first-order flexible', "r2['verdict'] == 'first-order flexible'")
    d = dims[str(k)]['flex_dim']
    need(d == ub, 'd == ub')
    entry['flex_dim'] = d
    if str(k) in so:
      need(so[str(k)]['second_order_rigid'] and so[str(k)]['flex_dim'] == d, "so[str(k)]['second_order_rigid'] and so[str(k)]['flex_dim'] ")
      entry['class'] = 'first-order flexible, second-order rigid'
      entry['prestress_certificate'] = so[str(k)]['prestress_certificate_found']
      entry['mechanism'] = so[str(k)]['method']
    else:
      f = fin[str(k)]
      need(f['ok'], "f['ok']")
      entry['class'] = 'flexible'
      if f['type'] == 'minkowski':
        (n1, d1), (n2, d2) = summand_shape(k, f['S1_edges'])
        entry['mechanism'] = 'Minkowski reorientation: S1 (%d vertices, dim %d) + R_t S2 (%d vertices, dim %d)' % (
          n1, d1, n2, d2)
        entry['summands'] = [[n1, d1], [n2, d2]]
      else:
        entry['mechanism'] = 'prism flex: ' + f['flex']
  entry['max_face'] = max(r1['face_sizes'])
  entry['parallel_edges'] = parallel_edges(k)
  out[k] = entry
  print('J%-3d %-44s %-42s d=%d %s' % (k, entry['name'][:44], entry['class'], entry['flex_dim'],
                                       entry.get('mechanism', '')), flush=True)
json.dump(out, open('results/classification.json', 'w'), indent=1)
cnt = {}
for e in out.values():
  cnt[e['class']] = cnt.get(e['class'], 0) + 1
print(cnt)
print('flexible without parallel edges:', [k for k, e in out.items() if e['class'] == 'flexible' and not e['parallel_edges']])
print('first-order flexible without parallel edges:',
      [k for k, e in out.items() if e['flex_dim'] > 0 and not e['parallel_edges']])
print('rigid without parallel edges:', [k for k, e in out.items() if e['class'] != 'flexible' and not e['parallel_edges']])
for cl in ('first-order rigid', 'flexible', 'first-order flexible, second-order rigid'):
  print('triangles+squares only, %s:' % cl, [k for k, e in out.items() if e['max_face'] <= 4 and e['class'] == cl])

# LaTeX table: J, name, V/E/F, degree, flex dim, class
abbrev = {'first-order rigid': 'R1', 'flexible': 'F', 'first-order flexible, second-order rigid': 'R2'}
lines = []
for k, e in out.items():
  mech = ''
  if e['class'] == 'flexible':
    mech = 'M' if e['mechanism'].startswith('Minkowski') else 'P'
  if e['class'].startswith('first-order flexible'):
    mech = 'S' + ('*' if e.get('prestress_certificate') else '')
  nm = e['name'].replace(' J12', '')
  lines.append('J%d & %s & %d/%d/%d & %d & %d & %s & %s \\\\' % (
    k, nm, e['V'], e['E'], e['F'], e['field_degree'], e['flex_dim'], abbrev[e['class']], mech))
open('results/table.tex', 'w').write('\n'.join(lines) + '\n')
