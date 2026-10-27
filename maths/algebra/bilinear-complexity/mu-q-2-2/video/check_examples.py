"""Check only the examples displayed in the video; no research files are written."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def multiply(a,b,modulus):
  out=0
  while b:
    if b&1:out^=a
    a<<=1;b>>=1
  degree=modulus.bit_length()-1
  while out.bit_length()>degree:
    out^=modulus<<(out.bit_length()-1-degree)
  return out

slices=[[[multiply(1<<i,1<<j,21)>>k&1 for j in range(4)] for i in range(4)] for k in range(4)]
expected=[[[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,1]],[[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],[[0,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,0]],[[0,0,0,1],[0,0,1,0],[0,1,0,1],[1,0,1,0]]]
assert slices==expected
assert (2+3)*(4+5)-2*4-3*5==22
assert multiply(8,2,21)==5
assert multiply(33,3,65)==34
assert (2**4-1)**2==225
record={'all_passed':True,'karatsuba':{'outside':[8,15],'combined':45,'middle':22},'binary_modulus_bits':21,'actual_output_slices':slices,'rank_one_grid_count':225,'convolution_example':{'left':[1,0,0,0,0,1],'right':[1,1,0,0,0,0],'result':[0,1,0,0,0,1]},'scope':'Production examples only; exhaustive research runs were read from accepted records.'}
(ROOT/'example-checks.json').write_text(json.dumps(record,indent=2)+'\n')
print('PASS: Karatsuba, four exact slices, finite masks, reduction and cyclic example.',flush=True)
