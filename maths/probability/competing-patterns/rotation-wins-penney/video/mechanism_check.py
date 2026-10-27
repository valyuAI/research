"""Check the finite illustrations independently of the animation code."""
from fractions import Fraction
from itertools import permutations
import json
from math import factorial
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def rank(xs):
  ordered=sorted(xs)
  return tuple(ordered.index(x)+1 for x in xs)


A=(2,3,4,1)
B=(1,2,3,4)
assert rank([.2,.4,.6,.1])==A
stream=[.10,.20,.40,.60,.15]
assert rank(stream[:4])==B and rank(stream[1:])==A
counts={x+y:0 for x in 'AB' for y in 'AB'}
for p in permutations(range(5)):
  first,last=rank(p[:4]),rank(p[1:])
  if first in (A,B) and last in (A,B):
    counts[('A' if first==A else 'B')+('A' if last==A else 'B')]+=1
assert counts=={'AA':0,'AB':0,'BA':2,'BB':1}
seq=[-1]
for start in range(1,6):seq.append(-sum(seq[max(0,start-3):start]))
assert seq==[-1,1,0,0,-1,1]
words=set(permutations('BBTT'))
allowed={w for w in words if w[0]=='B'}
swapped={tuple('T' if x=='B' else 'B' for x in w) for w in allowed}
assert len(words)==6 and len(allowed)==3 and not allowed & swapped
margin=1-Fraction(256699,300300)-Fraction(144,2879)-Fraction(1,3360)
assert margin==Fraction(218738049,2305503200)>0
cases=json.loads((ROOT.parent/'verification/length-three.json').read_text())['cases']
bounds=[Fraction(c['winsA']+c['unresolved'],c['factorial']) for c in cases]
worst=cases[bounds.index(max(bounds))]
assert worst['pattern']==[1,3,2] and max(bounds)<Fraction(47,100)
out={'overlap_counts_over_120':counts,'recurrence_example':seq,'interleavings':6,'first_blue':3,'uniform_scaled_margin':str(margin),'uniform_margin_decimal':float(margin),'length_three_worst_original':worst['pattern'],'length_three_worst_bound':str(max(bounds)),'checks_passed':True,'scope':'Finite teaching examples only; not an independent proof of the universal theorem.'}
(ROOT/'mechanism-check.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2),flush=True)
