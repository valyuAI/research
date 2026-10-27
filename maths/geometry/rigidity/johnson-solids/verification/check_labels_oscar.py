"""Optional (needs networkx and the dataset files): cross-check J-number labels: our face lists vs the OSCAR 'Exact Johnson Solids' dataset (Zenodo 10729583)
by isomorphism of vertex-facet incidence graphs.
usage: python3 check_labels_oscar.py <directory with the files j1 ... j92 of Zenodo record 10729583>"""
import json, sys, glob
import networkx as nx
from networkx.algorithms import isomorphism as iso
DATA = 'data'
EXT = sys.argv[1]

def graph(faces):
  G = nx.Graph()
  for i, f in enumerate(faces):
    G.add_node(('f', i), kind='f')
    for v in f:
      G.add_node(('v', v), kind='v')
      G.add_edge(('f', i), ('v', v))
  return G

def ext_faces(k):
  d = json.load(open('%s/j%d' % (EXT, k)))
  inc = d['data']['float']['VERTICES_IN_FACETS']
  return [r for r in inc if isinstance(r, list)]

nm = iso.categorical_node_match('kind', None)
ours = {}
bad = []
for k in range(1, 93):
  F = json.load(open('%s/J%02d.json' % (DATA, k)))['faces']
  ours[k] = graph(F)
  import os
  if not os.path.exists("%s/j%d" % (EXT, k)):
    print("J%d: not in external dataset" % k); continue
  E = graph(ext_faces(k))
  ok = nx.is_isomorphic(ours[k], E, node_match=nm)
  name = json.load(open('%s/J%02d.json' % (DATA, k)))['name']
  desc = json.load(open('%s/j%d' % (EXT, k)))['data']['float'].get('_info', {}).get('description', '').strip()
  print('J%d %-45s | ext: %-55s | isomorphic: %s' % (k, name, desc, ok), flush=True)
  if not ok:
    bad.append(k)
print('MISMATCHES:', bad)
