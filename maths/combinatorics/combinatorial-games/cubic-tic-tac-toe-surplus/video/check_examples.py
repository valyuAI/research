"""Exact checks of displayed board examples, independent of expensive matchers."""
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PAIRS=[[2,6,8,5,8],[11,10,3,1,10],[11,4,0,4,12],[9,1,9,5,12],[7,6,3,7,2]]
flat=sum(PAIRS,[])
assert all(flat.count(k)==2 for k in range(1,13)) and flat.count(0)==1
lines5=[*PAIRS,*map(list,zip(*PAIRS)),[PAIRS[i][i] for i in range(5)],[PAIRS[i][4-i] for i in range(5)]]
assert all(any(row.count(k)==2 for k in range(1,13)) for row in lines5)

def lines(n):
  out=[]
  for d in itertools.product([-1,0,1],repeat=3):
    if not any(d) or next(x for x in d if x)!=1:continue
    for p in itertools.product(range(1,n+1),repeat=3):
      q=tuple(p[i]+(n-1)*d[i] for i in range(3))
      if all(1<=x<=n for x in q):out.append(tuple(tuple(p[i]+k*d[i] for i in range(3)) for k in range(n)))
  return out

ls=lines(7);ls6=lines(6)
assert len(ls)==193 and len(ls6)==148
diags=[l for l in ls if all(l[0][i]!=l[-1][i] for i in range(3))]
assert len(diags)==4 and sum((4,4,4) in l for l in ls)==13
chosen=[(5,5,5)];used={next(i for i,l in enumerate(diags) if chosen[0] in l)}
while len(chosen)<4:
  old={i for i,l in enumerate(ls) if any(b in l for b in chosen)}
  candidates=[(sum(p in l and i not in old for i,l in enumerate(ls)),p,j) for j,line in enumerate(diags) if j not in used for p in line if p!=(4,4,4)]
  _,p,j=min(candidates,key=lambda v:(-v[0],v[1]));chosen.append(p);used.add(j)
assert sum(any(p in l for p in chosen) for l in ls)==27
partner_counts=[]
for a in {p for l in diags for p in l if p!=(4,4,4)}:
  partner_counts.append(sum(p!=(4,4,4) and not any(a in l and p in l for l in ls) for line in diags if a not in line for p in line))
assert set(partner_counts)=={12}
p=(1,7,1);q=(6,2,6)
for perm in itertools.permutations(range(3)):
  for signs in itertools.product([-1,1],repeat=3):
    a=tuple(4+signs[i]*(p[perm[i]]-4) for i in range(3))
    b=tuple(4+signs[i]*(q[perm[i]]-4) for i in range(3))
    assert not(a[0]<=4 and b[0]<=4)
assert 216*27==5832 and 5832//2==2916
assert 7*6+4==46<47==148-(216-14)//2
assert 576+288+384+48==1296 and 24480*2==48960
(ROOT/'example-checks.json').write_text(json.dumps({'all_passed':True,'pairing_board':PAIRS,'line_counts':{'7':len(ls),'6':len(ls6)},'central_displayed_breaker_cells':chosen,'central_lines_met':27,'all_diagonal_partner_counts':partner_counts,'opposite_pair_checked_under_48_symmetries':[p,q],'six_round7_bound':[46,47],'scope':'Exact display data checks only. Surplus values and full opening universality come from the accepted independent research records.'},indent=2)+'\n')
print('PASS: 5x5 pairing, cube lines, greedy sample, partner counts, all 48 symmetries, and six-cube arithmetic.',flush=True)
