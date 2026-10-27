"""Freeze exact checked graph examples for the animation, without research writes."""
import hashlib
import importlib.util
import json
from pathlib import Path
import networkx as nx

ROOT=Path(__file__).resolve().parent
V=ROOT.parent/'verification'
spec=importlib.util.spec_from_file_location('extremal',V/'verify_extremal.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


def doubling(A,variant=False):
  n=len(A);B=[[0]*(2*n+2) for _ in range(2*n+2)]
  for i in range(2*n):
    for j in range(2*n):B[i][j]=A[i%n][j%n]
  for i in range(n):
    B[n+i][2*n]=B[2*n][n+i]=1
    if variant:B[i][2*n+1]=B[2*n+1][i]=1
  B[2*n][2*n+1]=B[2*n+1][2*n]=1
  return B


def record(A):
  return {'matrix':A,'edges':[[i,j] for i in range(len(A)) for j in range(i+1,len(A)) if A[i][j]],'inertia':list(checker.ldl_inertia(A)),'reduced':checker.reduced(A)}


out={'W5':record(checker.w5()),'X':record(checker.affine_x()),'doublings':{},'ordinary_steps':[]}
for key in ['W5','X']:assert out[key]['inertia']==[11,0,4] and out[key]['reduced']
known=[nx.from_graph6_bytes(line.strip()) for line in (V/'order30_graphs.g6').read_bytes().splitlines() if line.strip()]
for count in range(4):
  word='V'*count+'O'*(3-count);A=[[0,1],[1,0]]
  for char in word:A=doubling(A,char=='V')
  rec=record(A)
  assert rec['inertia']==[4,22,4] and rec['reduced']
  G=nx.Graph();G.add_nodes_from(range(30));G.add_edges_from(rec['edges'])
  matches=[i for i,g in enumerate(known) if nx.is_isomorphic(g,G)]
  assert len(matches)==1
  rec['certificate_index']=matches[0];out['doublings'][word]=rec
  print(f'{word}: 30 vertices, {len(rec["edges"])} edges, exact inertia (4,22,4), certificate match {matches[0]}',flush=True)
A=[[0,1],[1,0]]
for _ in range(4):out['ordinary_steps'].append(record(A));A=doubling(A)
out['maxima']=[5,10,18,30,26,22,20,17,15,15,15]
out['census_exactly_four']=[1,17,295,3648,10384,14422,10810,4473,993,110,2,0,0]
out['source_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [V/'verify_extremal.py',V/'order30_graphs.g6',V/'census_counts.json',V/'final_census_result.json']}
(ROOT/'assets.json').write_text(json.dumps(out,indent=2))
print('W5 and X exact inertia verified; four doubling examples matched to certificates.',flush=True)
