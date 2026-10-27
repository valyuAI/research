"""Derive display paths from retained exact witnesses; never invent a corona."""
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
VER=ROOT.parent/'verification'
NB=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]


def xy(p):
  return [p[0]+p[1]/2,p[1]*math.sqrt(3)/2]


def key(p):
  return tuple(round(v,7) for v in p)


def marked_outline(w):
  edges=[]
  for (cell,direction),mark in zip(w['edges'],w['labels']):
    centre=xy(cell);normal=xy(NB[direction]);tangent=[-normal[1],normal[0]]
    mid=[centre[i]+normal[i]/2 for i in range(2)]
    half=1/(2*math.sqrt(3));radius=.14
    start=[mid[i]-tangent[i]*half for i in range(2)]
    end=[mid[i]+tangent[i]*half for i in range(2)]
    points=[start]
    if mark!='f':
      sign=1 if mark=='b' else -1
      for j in range(17):
        theta=-math.pi/2+math.pi*j/16
        points.append([mid[i]+radius*(sign*normal[i]*math.cos(theta)+tangent[i]*math.sin(theta)) for i in range(2)])
    points.append(end)
    edges.append({'start':start,'end':end,'points':points,'mark':mark,'mid':mid,'normal':normal})
  lookup={key(e['start']):e for e in edges}
  ordered=[];edge=edges[0]
  for _ in edges:
    ordered.append(edge);edge=lookup[key(edge['end'])]
  assert len({key(e['start']) for e in ordered})==len(edges)
  assert key(ordered[-1]['end'])==key(ordered[0]['start'])
  points=[p for e in ordered for p in e['points']]
  return points,ordered


def transform_xy(p,pl):
  y=2*p[1]/math.sqrt(3);x=p[0]-y/2
  m,t=pl['M'],pl['t']
  return xy((m[0][0]*x+m[0][1]*y+t[0],m[1][0]*x+m[1][1]*y+t[1]))


def marked(name):
  path=VER/'witnesses'/name
  w=json.loads(path.read_text());points,edges=marked_outline(w)
  pieces=[];occupied=set();counts=[]
  for level in range(w['k']+1):
    for pl in [p for p in w['placements'] if p['level']==level]:
      cells={(pl['M'][0][0]*c[0]+pl['M'][0][1]*c[1]+pl['t'][0],pl['M'][1][0]*c[0]+pl['M'][1][1]*c[1]+pl['t'][1]) for c in w['cells']}
      assert not cells&occupied
      occupied|=cells
      pieces.append({'level':level,'points':[transform_xy(p,pl) for p in points]})
    counts.append(len(occupied))
  return {'source':str(path.relative_to(ROOT.parent)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'base_points':points,'base_edges':edges,'pieces':pieces,'cumulative_cells':counts,'labels':w['labels'],'cells':w['cells'],'radius':.14}


def basic():
  path=VER/'basic/basic_patch.json';data=json.loads(path.read_text())
  faces=[]
  offsets=[(6,2),(0,4),(-6,2),(-6,-2),(0,-4),(6,-2)]
  for x,y in data['tile']['hexagons']:
    corners=[(x+dx,y+dy) for dx,dy in offsets];face=[]
    for a,b in zip(corners,corners[1:]+corners[:1]):
      face.extend([a,((a[0]+b[0])//2,(a[1]+b[1])//2)])
    faces.append(face)
  for triangle in data['tile']['drafters']:
    cx=sum(p[0] for p in triangle)/3;cy=sum(p[1] for p in triangle)/3
    faces.append(sorted(map(tuple,triangle),key=lambda p:math.atan2(math.sqrt(3)*(p[1]-cy),p[0]-cx)))
  edges=Counter(tuple(sorted((a,b))) for face in faces for a,b in zip(face,face[1:]+face[:1]))
  graph=defaultdict(list)
  for (a,b),count in edges.items():
    assert count in [1,2]
    if count==1:graph[a].append(b);graph[b].append(a)
  assert len(graph)==75 and all(len(ns)==2 for ns in graph.values())
  first=min(graph);outline=[first];previous=None;current=first
  while True:
    nxt=next(p for p in graph[current] if p!=previous)
    if nxt==first:break
    outline.append(nxt);previous,current=current,nxt
  assert len(outline)==75
  pieces=[]
  for pl in data['placements']:
    points=[]
    for p in outline:
      nums=[sum(pl['L'][i][j]*p[j] for j in range(2)) for i in range(2)]
      assert all(v%pl['den']==0 for v in nums)
      q=[nums[i]//pl['den']+pl['T'][i] for i in range(2)]
      points.append([q[0]/8,math.sqrt(3)*q[1]/8])
    pieces.append({'level':pl['level'],'points':points})
  levels=[sum(p['level']==k for p in pieces) for k in range(7)]
  assert len(pieces)==169 and levels==[1,6,10,13,32,52,55]
  return {'source':str(path.relative_to(ROOT.parent)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pieces':pieces,'levels':levels,'base_boundary_edges':75}


def main():
  data={'mono':marked('hex1_k3.json'),'row4':marked('hex4_line_k5.json'),'basic':basic()}
  assert data['mono']['cumulative_cells']==[1,7,19,37]
  assert data['row4']['cumulative_cells']==[4,24,68,160,316,524]
  assert len(data['row4']['pieces'])==131
  ledger=json.loads((VER/'results.json').read_text())
  assert len(ledger['tiles'])==34 and all(t['upper_bound']['drat_verified'] for t in ledger['tiles'])
  data['table']=[{k:t[k] for k in ['grid','name','cells','h']} for t in ledger['tiles']]
  (ROOT/'geometry.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
  print('PASS: exact retained placements: mono 37, row4 131 / 524 cells, Basic 169; all 34 ledger entries.',flush=True)


if __name__=='__main__':
  main()
