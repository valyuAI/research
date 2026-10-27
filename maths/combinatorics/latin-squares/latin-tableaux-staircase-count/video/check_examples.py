"""Check displayed tableau data without importing or modifying research checkers."""
import ast
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
base5=[[4,5,2,1,3],[3,1,4,2],[2,3,1],[1,2,3]]
base6=[[5,4,6,3,1,2],*base5]

def valid(rows):
  return all(sorted(row)==list(range(1,len(row)+1)) for row in rows) and all(len(v)==len(set(v)) for v in [[r[j] for r in rows if j<len(r)] for j in range(len(rows[0]))])

assert valid(base5) and valid(base6)
clash=[base5[0],[4,1,3,2],*base5[2:]]
assert all(sorted(row)==list(range(1,len(row)+1)) for row in clash)
assert not valid(clash) and clash[0][0]==clash[1][0]==4
# All 7! possibilities, rather than assuming the invariant's restricted form.
tops=[list(row) for row in itertools.permutations(range(1,8)) if valid([row,*base6])]
assert tops==[[6,7,5,4,2,1,3],[6,7,5,4,2,3,1],[7,6,5,4,2,1,3],[7,6,5,4,2,3,1]]
rows=[tops[0],*base6]
for k in range(8,11):
  allowed=[]
  for left in itertools.permutations([k-2,k-1,k]):
    for right in itertools.permutations([1,2,3]):
      row=[*left,*range(k-3,3,-1),*right]
      if valid([row,*rows]):allowed.append(row)
  assert len(allowed)==4
  rows=[allowed[0],*rows]
assert rows[0][3:7]==[7,6,5,4]
assert all(576*4**(k-6)==9*4**(k-3) for k in range(6,20))
(ROOT/'example-checks.json').write_text(json.dumps({'all_passed':True,'base5':base5,'base6':base6,'all_seven_cell_extensions':tops,'k10_rows':rows,'scope':'All 5040 candidate top rows checked for the displayed k6 base; this does not rerun the scientific enumeration of all bases.'},indent=2)+'\n')
print('PASS: displayed fillings, all four extensions from exhaustive 7! candidates, k10 middle and count identity.',flush=True)
