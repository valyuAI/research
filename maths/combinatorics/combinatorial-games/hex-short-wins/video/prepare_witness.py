"""Prepare and audit the exact retained 23-move illustration, not a strategy proof."""
from collections import deque
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MOVES=[(3,3),(1,1),(2,4),(5,2),(5,1),(4,2),(5,3),(4,3),(4,1),(3,2),(3,1),(1,4),(1,5),(1,2),(1,3),(2,2),(3,5),(2,5),(3,4),(4,4),(4,5),(2,1),(5,4)]
PATH=[(1,5),(2,4),(3,4),(3,5),(4,5),(5,4)]


def neighbours(cell,n=5):
  r,c=cell
  return [(r+dr,c+dc) for dr,dc in [(0,1),(0,-1),(1,0),(-1,0),(1,-1),(-1,1)] if 1<=r+dr<=n and 1<=c+dc<=n]


def distance(stones,blue=True):
  starts=[p for p in stones if p[0 if blue else 1]==1]
  queue=deque((p,1) for p in starts)
  seen=set(starts)
  while queue:
    p,d=queue.popleft()
    if p[0 if blue else 1]==5:
      return d
    for q in neighbours(p):
      if q in stones and q not in seen:
        seen.add(q);queue.append((q,d+1))
  return None


def main():
  blue,red=set(),set()
  audit=[]
  for i,p in enumerate(MOVES,1):
    assert p not in blue|red
    (blue if i%2 else red).add(p)
    b,r=distance(blue),distance(red,False)
    assert r is None and (b is None if i<23 else b==6)
    audit.append({'move':i,'cell':p,'blueShortest':b,'redShortest':r})
  assert len(blue)==12 and set(PATH)<=blue
  assert all(b in neighbours(a) for a,b in zip(PATH,PATH[1:]))
  paths=set()
  def walk(seq):
    p=seq[-1]
    if p[0]==5:
      paths.add(frozenset(seq));return
    if len(seq)==6:
      return
    for q in neighbours(p):
      if q not in seq:
        walk(seq+[q])
  for c in range(1,6):
    walk([(1,c)])
  minimal=[s for s in paths if not any(t<s for t in paths)]
  assert len(minimal)==106
  data={'source':'../video-brief.md, checked 23-move retained branch; not the universal strategy proof','moves':MOVES,'path':PATH,'blue_stones':12,'first_connection':23,'shortest_path':6,'minimal_targets':sorted([sorted(s) for s in minimal]),'audit':audit}
  (ROOT/'witness-data.json').write_text(json.dumps(data,indent=2)+'\n')
  print('PASS: legal 23-move branch, first connection at 23, 12 Blue stones, shortest path 6; 106 exact minimal target sets.',flush=True)


if __name__=='__main__':
  main()
