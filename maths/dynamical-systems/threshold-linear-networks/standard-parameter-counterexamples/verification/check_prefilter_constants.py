"""Check the platform's recovered prefilter constants by exact rational inequalities."""
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

here = Path(__file__).resolve().parent
binary = here / 'scan_results/prefilter_constants'
subprocess.run(['cc', '-O2', '-o', str(binary), str(here / 'prefilter_constants.c'), '-lm'], check=True)
result = subprocess.run([str(binary)], capture_output=True, text=True, check=True)
rows = []
for line in result.stdout.splitlines():
  order, hexadecimal = line.split()
  n = int(order)
  c = Fraction(float.fromhex(hexadecimal))
  bound2 = n * n * (1 + 9 * (n - 1)) ** (n - 1)
  rows.append({'n': n, 'constant_hex': hexadecimal, 'squared_hadamard_bound': bound2,
               'greater_than_1_001_times_bound': c * c > Fraction(1001, 1000) ** 2 * bound2})
ok = [r['n'] for r in rows] == list(range(2, 8)) and all(r['greater_than_1_001_times_bound'] for r in rows)
out = {'constants': rows, 'ok': ok}
(here / 'scan_results/prefilter_constants.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
sys.exit(0 if ok else 1)
