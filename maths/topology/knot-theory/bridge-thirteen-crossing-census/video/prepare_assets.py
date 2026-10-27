"""Freeze the actual 13n_1005 certificate and a checked planar drawing.

The drawing comes from the PD rotation system. Auxiliary face vertices spread
the geometry but are never drawn. No new knot or research data are invented.
"""
import hashlib
import json
import sys
from pathlib import Path

import networkx as nx
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent
VERIFY=ROOT.parent/'verification'
sys.path.insert(0,str(VERIFY))
import check
import check_matrices


def need(v,message):
  if not v: raise ValueError(message)


def cross(a,b):
  return a[0]*b[1]-a[1]*b[0]


def point_segment(p,a,b):
  t=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1)
  return np.linalg.norm(p-a-t*(b-a))


def drawing(entry):
  pd=entry['pd']
  rotations={i:[13+x for x in row] for i,row in enumerate(pd)}
  for edge in range(1,27): rotations[13+edge]=[i for i,row in enumerate(pd) if edge in row]
  emb=nx.PlanarEmbedding(); emb.set_data(rotations); emb.check_structure()
  marked=set(); faces=[]
  for a,b in emb.edges():
    if (a,b) not in marked: faces.append(emb.traverse_face(a,b,marked))
  outer=max(faces,key=len); graph=nx.Graph(emb); triangles=[]
  for i,face in enumerate(faces):
    if face!=outer:
      node=100+i; graph.add_edges_from((node,v) for v in face)
      triangles.extend((node,face[j],face[(j+1)%len(face)]) for j in range(len(face)))
  fixed={v:np.array([np.cos(2*np.pi*i/len(outer)),np.sin(2*np.pi*i/len(outer))]) for i,v in enumerate(outer)}
  inside=[v for v in graph if v not in fixed]; idx={v:i for i,v in enumerate(inside)}
  matrix=np.zeros((len(inside),len(inside))); rhs=np.zeros((len(inside),2))
  for v in inside:
    row=idx[v]; matrix[row,row]=graph.degree(v)
    for w in graph[v]:
      if w in fixed: rhs[row]+=fixed[w]
      else: matrix[row,idx[w]]-=1
  solution=np.linalg.solve(matrix,rhs)
  position=fixed|{v:solution[idx[v]] for v in inside}
  nodes=list(graph); index={v:i for i,v in enumerate(nodes)}
  xy=np.array([position[v] for v in nodes]); variable=np.array([index[v] for v in inside])
  tri=np.array([[index[v] for v in t] for t in triangles])
  for i,(a,b,c) in enumerate(tri):
    if cross(xy[b]-xy[a],xy[c]-xy[a])<0: tri[i]=[a,c,b]
  def energy_grad(points):
    a,b,c=[points[tri[:,i]] for i in range(3)]
    area=.5*((b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0]))
    if np.min(area)<=1e-10: return -float('inf'),None
    grad=np.zeros_like(points)
    for col,u,v in [(0,b,c),(1,c,a),(2,a,b)]:
      derivative=np.column_stack([u[:,1]-v[:,1],v[:,0]-u[:,0]])*.5/area[:,None]
      np.add.at(grad,tri[:,col],derivative)
    return float(np.log(area).sum()),grad
  for it in range(1200):
    score,grad=energy_grad(xy)
    step=.025/max(np.linalg.norm(grad[variable],axis=1))
    for _ in range(25):
      proposed=xy.copy(); proposed[variable]+=step*grad[variable]
      value,_=energy_grad(proposed)
      if value>score: xy=proposed; break
      step*=.5
    if it%300==0: print(f'Planar display spacing {it}/1200',flush=True)
  # PD lists are counterclockwise in the paper's convention. The harmonic
  # construction above reverses that global orientation; reflect it back.
  position={v:xy[index[v]]*np.array([1.,-1.]) for v in rotations}
  edges=list(nx.Graph(emb).edges())
  intersections=[]
  for i,(a,b) in enumerate(edges):
    for c,d in edges[i+1:]:
      if {a,b}&{c,d}: continue
      p,q,r,s=[position[v] for v in [a,b,c,d]]
      if cross(q-p,r-p)*cross(q-p,s-p)<-1e-13 and cross(s-r,p-r)*cross(s-r,q-r)<-1e-13: intersections.append([a,b,c,d])
  need(not intersections,'Extra crossings introduced by planar layout')
  gaps={}
  orientation=[]
  for i,row in enumerate(pd):
    p=position[i]
    clearance=min(point_segment(p,position[a],position[b]) for a,b in edges if i not in [a,b])
    radius=min(np.linalg.norm(position[13+e]-p) for e in row)
    gaps[i]=float(.18*min(clearance,radius))
    directions=[position[13+e]-p for e in row]
    angles=np.array([np.arctan2(v[1],v[0]) for v in directions])
    # Boundary vertices can have a gap greater than pi, so nearest-angle
    # unwrapping is not a cyclic-order test. Sum directed modular gaps.
    total=float(np.sum((np.roll(angles,-1)-angles)%(2*np.pi)))
    if abs(total-2*np.pi)<1e-8: orientation.append(2*np.pi)
    elif abs(total-6*np.pi)<1e-8: orientation.append(-2*np.pi)
    else: raise ValueError(f'Crossing {i} has a non-cyclic port order')
  need(all(abs(abs(t)-2*np.pi)<1e-8 for t in orientation),'Crossing cyclic order changed')
  need(all(t*orientation[0]>0 for t in orientation),'Inconsistent crossing orientation')
  return {str(v):position[v].tolist() for v in position},gaps,{'extra_segment_intersections':intersections,'crossing_rotation_system_consistent':True,'global_orientation_radians':orientation[0],'minimum_gap_radius':min(gaps.values())}


def main():
  all_entries=json.loads((VERIFY/'certificates.json').read_text())['certificates']
  entry=next(e for e in all_entries if e['name']=='13n_1005')
  source=next(r for r in json.loads((VERIFY/'source-snapshot.json').read_text())['rows'] if r['name']==entry['name'])
  check.verify_one(entry,source); check_matrices.check(entry)
  arcs=check.edge_arcs(entry['pd']); need(arcs==check_matrices.arc_indices(entry['pd']),'Arc reconstructions differ')
  a,b,c,d=entry['pd'][0]
  incoming,over,outgoing=[entry['meridian_matchings'][arcs[e]] for e in [a,b,c]]
  need((incoming,over,outgoing)==([[0,1],[2,3]],[[0,1],[3,4]],[[0,1],[2,4]]),'Wrong illustrated crossing')
  seed_actions=[entry['meridian_matchings'][i] for i in entry['seed_arcs']]
  graph=nx.Graph();graph.add_nodes_from(range(8));components=[]
  for matching in seed_actions:
    graph.add_edges_from(matching); components.append(nx.number_connected_components(graph))
  need(components==[6,5,3,1],'Illustrated equalities incorrect')
  known={v:i for i,v in enumerate(entry['seed_arcs'])};moves=[]
  for crossing,new in entry['coloring_steps']:
    a,b,c,d=entry['pd'][crossing]; before,after,above=[arcs[e] for e in [a,c,b]]
    other=before if after==new else after
    need(above in known and other in known and new not in known,'Invalid animation coloring move')
    known[new]=known[other]
    moves.append({'crossing':crossing,'new_arc':new,'over_arc':above,'known_under_arc':other,'seed_colour':known[new]})
  positions,gaps,layout_report=drawing(entry)
  asset={'entry':entry,'edge_arcs':arcs,'positions':positions,'crossing_gaps':gaps,'moves':moves,'seed_actions':seed_actions,'components_after_seeds':components,'new_names':[e['name'] for e in all_entries if e['status']=='new']}
  (ROOT/'example.json').write_text(json.dumps(asset,indent=2))
  files=['README.md','paper.tex','video-brief.md','verification/certificates.json','verification/source-snapshot.json','verification/open-list-v1.3.0.json','verification/remaining-v1.3.0.json','verification/coxeter-overlap-summary.json']
  report={'illustrated_certificate_replayed':True,'first_crossing':[incoming,over,outgoing],'components_after_seed_actions':components,'coloring_moves':moves,'diagram_check':layout_report,'input_sha256':{f:hashlib.sha256((ROOT.parent/f).read_bytes()).hexdigest() for f in files},'scope':'Two source checkers replayed; diagram embedding and exact displayed operations additionally checked. Not an independent new theorem or priority audit.'}
  (ROOT/'qa/example-check.json').write_text(json.dumps(report,indent=2))
  im=Image.new('RGB',(1200,1200),'#0d0f12');draw=ImageDraw.Draw(im)
  pos={int(k):np.array(v)*np.array([500.,-500.])+600 for k,v in positions.items()}
  for edge in range(1,27):
    endpoints=[i for i,row in enumerate(entry['pd']) if edge in row]
    draw.line([tuple(pos[endpoints[0]]),tuple(pos[13+edge]),tuple(pos[endpoints[1]])],fill='#58c4dd',width=5)
  for i,row in enumerate(entry['pd']):
    p=pos[i];rad=gaps[i]*500
    draw.ellipse((p[0]-rad,p[1]-rad,p[0]+rad,p[1]+rad),fill='#0d0f12')
    for edge in [row[1],row[3]]:
      direction=pos[13+edge]-p;end=p+direction/np.linalg.norm(direction)*(rad+3)
      draw.line([tuple(p),tuple(end)],fill='#58c4dd',width=5)
    draw.text(tuple(p+np.array([8,8])),str(i),fill='white')
  im.save(ROOT/'qa/diagram-preview.png')
  print('Actual PD diagram, first crossing, four seed actions and all nine coloring moves checked',flush=True)


if __name__=='__main__': main()
