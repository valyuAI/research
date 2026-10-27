"""A clean package works without generated files; incomplete evidence must fail."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
cases = {}
with tempfile.TemporaryDirectory(prefix='census-audit-') as directory:
  temp = Path(directory)
  for name in ('audit_recorded.py', 'census_counts.json', 'census_nonsingular_nneg_le4.txt.gz',
               'enumerate_nonsingular.log', 'enumerate_check.log', 'max_reduced_order.log',
               'max_reduced_order_check.log', 'check_census_result.json', 'extremal_result.json',
               'order30_check.json', 'extremal_doubling_check.log'):
    shutil.copy2(here / name, temp / name)
  def check(name, should_pass, args=()):
    result = subprocess.run([sys.executable, str(temp / 'audit_recorded.py'), *args],
      capture_output=True, text=True)
    if (result.returncode == 0) != should_pass:
      raise RuntimeError(f'{name}: unexpected result {result.stdout} {result.stderr}')
    cases[name] = {'returncode': result.returncode, 'expected_pass': should_pass}
  check('clean_package_without_generated_output', True)
  check('required_generated_output_missing', False, ('--require-generated',))
  path = temp / 'enumerate_check.log'
  original = path.read_text()
  lines = original.splitlines()
  retained = [line for line in lines if 'order=17:' not in line]
  if len(retained) != len(lines) - 1:
    raise RuntimeError('test fixture must remove exactly one termination level')
  path.write_text('\n'.join(retained) + '\n')
  check('missing_termination_level', False)
  path.write_text(original)
  generated = temp / 'output/ns_k4'
  generated.mkdir(parents=True)
  (generated / 'order1.txt').write_text('')
  check('partial_generated_output', False)
result = {'ok': True, 'cases': cases}
(here / 'audit_failure_tests.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
