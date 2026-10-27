"""Read finalized certificates; freeze checked animation data inside video/."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parent
V=ROOT.parent/'verification/examples'
g=json.loads((V/'G11.json').read_text())
cert=json.loads((V/'G11_certificate.json').read_text())
n=g['n']
K=[[4 if i==j else 6 for j in range(n)] for i in range(n)]
for j,i in g['edges']:K[i][j]=3
x=[Fraction(v) for v in cert['fixed_point_theta_1']]
assert all(sum(K[i][j]*x[j] for j in range(n))==4 for i in range(n))
assert all(v>0 for v in x) and len(g['deleted_arcs'])==21
assert all(int(v)>0 for v in cert['hurwitz_determinants_Delta1_to_Deltan'])
matrix=np.array(K,dtype=float);rates=np.array([float(v) for v in x]);W=np.eye(n)-matrix/4
initial=rates*(1+.001*np.sin(np.arange(n)+.5))
times=np.linspace(0,800,1001)
sol=solve_ivp(lambda t,y:-y+np.maximum(W@y+1,0),(0,800),initial,t_eval=times,rtol=1e-9,atol=1e-12)
assert sol.success and np.max(abs(sol.y[:,-1]-rates))<1e-5
data={'K':K,'deleted_arcs':g['deleted_arcs'],'edges':g['edges'],'numerators':[int(v*292) for v in x], 'rates':[str(v) for v in x], 'hurwitz':cert['hurwitz_determinants_Delta1_to_Deltan'], 'coefficients':cert['det_zI_plus_K_coefficients_high_to_low'],'eigenvalues':[[float(v.real),float(v.imag)] for v in np.linalg.eigvals(matrix)],'simulation':{'times':times.tolist(),'values':sol.y.T.tolist(),'initial':initial.tolist(),'description':'One 0.1% sinusoidal relative perturbation; numerical illustration, not a basin theorem.'},'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [V/'G11.json',V/'G11_certificate.json']}}
(ROOT/'assets.json').write_text(json.dumps(data,indent=2))
print('Exact Kx=4 verified in all 11 rows; 21 missing arcs; all Hurwitz determinants positive; numerical illustration saved.',flush=True)
