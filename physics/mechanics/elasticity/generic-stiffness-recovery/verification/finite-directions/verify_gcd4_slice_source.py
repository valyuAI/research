"""Independently reconstruct a saved cubic slice on full unisolvent grids.

Uses explicit Christoffel entries and the determinant odd-part identity,
not the symbolic assembly routine. No CAS is needed for these identities.
The original-generator ideal identities are checked by verify_direct_powers.py.
"""

import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
P=32003


def require(condition, message):
  if not condition:
    raise ValueError(message)


def rank(rows):
  a=[[v%P for v in row] for row in rows]
  r=0
  for c in range(len(a[0])):
    pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
    if pivot is None:continue
    a[r],a[pivot]=a[pivot],a[r]
    inverse=pow(a[r][c],-1,P)
    a[r]=[v*inverse%P for v in a[r]]
    for i in range(r+1,len(a)):
      scale=a[i][c]
      a[i]=[(v-scale*w)%P for v,w in zip(a[i],a[r])]
    r+=1
  return r


def christoffel(c,p):
  x,y,z=p
  g11=c['11']*x*x+c['66']*y*y+c['55']*z*z+2*c['16']*x*y+2*c['15']*x*z+2*c['56']*y*z
  g22=c['66']*x*x+c['22']*y*y+c['44']*z*z+2*c['26']*x*y+2*c['46']*x*z+2*c['24']*y*z
  g33=c['55']*x*x+c['44']*y*y+c['33']*z*z+2*c['45']*x*y+2*c['35']*x*z+2*c['34']*y*z
  g12=c['16']*x*x+c['26']*y*y+c['45']*z*z+(c['12']+c['66'])*x*y+(c['14']+c['56'])*x*z+(c['25']+c['46'])*y*z
  g13=c['15']*x*x+c['46']*y*y+c['35']*z*z+(c['14']+c['56'])*x*y+(c['13']+c['55'])*x*z+(c['36']+c['45'])*y*z
  g23=c['56']*x*x+c['24']*y*y+c['34']*z*z+(c['25']+c['46'])*x*y+(c['36']+c['45'])*x*z+(c['23']+c['44'])*y*z
  return [[g11,g12,g13],[g12,g22,g23],[g13,g23,g33]]


def determinant(a):
  return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
          -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
          +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))%P


def simplex(d,degree):
  if d==0:
    yield ()
    return
  for value in range(degree+1):
    for rest in simplex(d-1,degree-value):yield(value,)+rest


def main():
  parser=argparse.ArgumentParser();parser.add_argument('variables',type=int);n=parser.parse_args().variables
  slug=f'gcd4_slice_n{n}'
  data=json.loads((ROOT/(slug+'_input.json')).read_text())
  rows=data['integer_slice_matrix']
  require(data['source_dimension']==42 and data['slice_variables']==n and data['prime']==P,
          'Incorrect source dimension, slice dimension, or modulus')
  require(len(rows)==42 and all(len(row)==n and all(type(v) is int for v in row) for row in rows),
          'Expected a 42-by-n integer slice matrix')
  require(data['S_monomials']==[[a,b,2-a-b] for a in range(3) for b in range(3-a)],
          'Incorrect quadratic coefficient order')
  require(data['equation_powers']==[[a,b,6-a-b] for a in range(7) for b in range(7-a)],
          'Incorrect sextic coefficient order')
  require(all(P % d for d in range(2, int(P**0.5)+1)), 'The modulus must be prime')
  require(rank(rows)==n, 'The slice matrix does not have full column rank')
  source=(ROOT/(slug+'.sing')).read_text().split('ideal J=',1)[1].split(';',1)[0]
  coefficients=[]
  for expression in source.split(','):
    terms=[]
    for term in expression.strip().split('+'):
      pieces=term.split('*');indices=[int(v[1:]) for v in pieces[1:]]
      require(len(indices)==3 and all(0<=i<n for i in indices), 'Unexpected cubic source term')
      terms.append((int(pieces[0]),indices))
    coefficients.append(terms)
  require(len(coefficients)==28, 'Expected 28 sextic coefficients')
  ppoints=[(a,b,1) for a in range(7) for b in range(7-a)]
  tpoints=[v+(1,) for v in simplex(n-1,3)]
  for number,t in enumerate(tpoints,1):
    values=[sum(v*w for v,w in zip(row,t))%P for row in rows]
    c=dict(zip([f'{i}{j}' for i in range(1,7) for j in range(i,7)],values[:21]))
    h=dict(zip(['12','13','14','23','25','26','34','35','36','44','45','46','55','56','66'],values[21:36]))
    for name,a,b in [('11','55','66'),('22','44','66'),('33','44','55'),('16','26','45'),('15','35','46'),('24','34','56')]:h[name]=-h[a]-h[b]
    expected_coefficients=[sum(c*t[i]*t[j]*t[k] for c,(i,j,k) in terms)%P for terms in coefficients]
    for p in ppoints:
      gx,gh=christoffel(c,p),christoffel(h,p)
      require(sum(gh[i][i] for i in range(3))%P==0, 'H does not satisfy the trace identity')
      plus=[[gx[i][j]+gh[i][j] for j in range(3)] for i in range(3)]
      minus=[[gx[i][j]-gh[i][j] for j in range(3)] for i in range(3)]
      r=(determinant(plus)-determinant(minus))*pow(2,-1,P)%P
      q=sum(gx[i][j]*gh[j][i] for i,j in itertools.product(range(3),repeat=2))%P
      s=sum(v*pow(p[0],a)*pow(p[1],b)*pow(p[2],d) for v,(a,b,d) in zip(values[36:],data['S_monomials']))%P
      expected=sum(v*pow(p[0],a)*pow(p[1],b)*pow(p[2],d) for v,(a,b,d) in zip(expected_coefficients,data['equation_powers']))%P
      require((r-q*s)%P==expected, 'Tensor-to-cubic polynomial identity failed')
    if number%50==0 or number==len(tpoints):print(f'Unisolvent source grid {number}/{len(tpoints)} ×28 verified',flush=True)
  leading_path=ROOT/(slug+'_leading.txt')
  pure={}
  if leading_path.exists():
    for line in leading_path.read_text().splitlines():
      match=re.fullmatch(r't(\d+)(?:\^(\d+))?',line.strip())
      if match:
        variable,power=int(match[1]),int(match[2] or 1)
        pure[variable]=min(pure.get(variable,power),power)
    require(set(pure)==set(range(n)), 'The saved leading ideal lacks a pure power')
  result={'slice_rank_mod_p':n,'t_unisolvent_points':len(tpoints),'p_unisolvent_points':28,
          'all_coefficient_identities_verified':True,'pure_powers_in_saved_leading_ideal':pure,
          'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                    for name in [slug+'_input.json',slug+'.sing']},
          'scope':'Exact tensor-to-cubic assembly on complete unisolvent grids. Ideal membership is checked separately by verify_direct_powers.py.'}
  (ROOT/(slug+'_source_audit.json')).write_text(json.dumps(result,indent=2)+'\n')
  print('PASS exact tensor-to-cubic slice reconstruction',flush=True)


if __name__=='__main__':main()
