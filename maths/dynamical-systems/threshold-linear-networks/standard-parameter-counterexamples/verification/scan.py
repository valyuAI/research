"""Run every scan stage with checked exits, complete counts and exact candidate rejection."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

here = Path(__file__).resolve().parent
os.chdir(here)
maxn = int(sys.argv[1]) if len(sys.argv) == 2 else 6
if maxn not in (6, 7):
  sys.exit('Usage: scan.py [6|7]')
expected = {2: 3, 3: 16, 4: 218, 5: 9608, 6: 1540944, 7: 882033440}
out = here / 'scan_results'
out.mkdir(exist_ok=True)
subprocess.run(['cc', '-O2', '-fsanitize=signed-integer-overflow', '-fno-sanitize-recover=all',
                '-o', str(out / 'fixedscan'), 'fixedscan.c', '-lm'], check=True)
for n, control in [(n, False) for n in range(2, maxn + 1)] + [(6, True)]:
  stem = f'n{n}_' + ('control' if control else 'std')
  print(f'START {stem}: expecting {expected[n]} digraphs', flush=True)
  base = subprocess.run(['geng', '-q', str(n)], capture_output=True, check=True)
  base_path = out / f'{stem}.g6'
  base_path.write_bytes(base.stdout)
  env = os.environ.copy()
  if n <= 6:
    env['CTLN_NO_PREFILTER'] = '1'
  params = ['21', '500', '10'] if control else ['3', '3', '1']
  with base_path.open('rb') as source, (out / f'{stem}.txt').open('w') as candidates, \
      (out / f'{stem}.err').open('w') as errors, (out / f'{stem}.directg.err').open('w') as gen_errors:
    generator = subprocess.Popen(['directg', '-q'], stdin=source, stdout=subprocess.PIPE, stderr=gen_errors)
    scanner = subprocess.Popen([str(out / 'fixedscan'), *params], stdin=generator.stdout,
                               stdout=candidates, stderr=errors, env=env)
    generator.stdout.close()
    start = time.monotonic()
    while scanner.poll() is None:
      try:
        scanner.wait(timeout=15)
      except subprocess.TimeoutExpired:
        print(f'  {stem}: scanning, elapsed {time.monotonic() - start:.0f}s', flush=True)
    generator_code = generator.wait()
    if scanner.returncode != 0 or generator_code != 0:
      sys.exit(f'FAIL: {stem}: directg={generator_code}, scanner={scanner.returncode}')
  summary = (out / f'{stem}.err').read_text().splitlines()[-1]
  values = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', summary)}
  if values.get('total') != expected[n] or values.get('nonzero') != expected[n] - 1:
    sys.exit(f'FAIL: incomplete enumeration: {summary}')
  count = sum(1 for _ in (out / f'{stem}.txt').open())
  if count != values.get('coefpos', -1) or values.get('undecided') != 0:
    sys.exit(f'FAIL: candidate accounting: {summary}')
  subprocess.run([sys.executable, '-u', '-B', 'recheck.py', *params, str(out / f'{stem}.txt'),
                  '--expect-candidates', str(count), '--expect-stable', '2' if control else '0',
                  '--output', str(out / f'{stem}.recheck.json')], check=True)
  values['prefilter_disabled'] = n <= 6
  (out / f'{stem}.summary.json').write_text(json.dumps(values, indent=2) + '\n')
  print(f'PASS {stem}: all {expected[n]} digraphs, {count} exact candidate checks', flush=True)
print('ALL SCAN STAGES PASS', flush=True)
