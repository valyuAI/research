"""Check that missing, duplicated or miscounted candidates cannot pass exact replay."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
cases = {}
with tempfile.TemporaryDirectory(prefix='recheck-check-') as directory:
  temp = Path(directory)
  candidates = temp / 'candidates.txt'
  original = (here / 'scan_results/n4_std.txt').read_text()
  candidates.write_text(original)
  def check(name, expected_count, expected_stable, should_pass):
    result = subprocess.run([sys.executable, str(here / 'recheck.py'), '3', '3', '1',
      str(candidates), '--expect-candidates', str(expected_count),
      '--expect-stable', str(expected_stable), '--output', str(temp / 'result.json')],
      capture_output=True, text=True)
    if (result.returncode == 0) != should_pass:
      raise RuntimeError(f'{name}: unexpected result {result.stdout} {result.stderr}')
    cases[name] = {'returncode': result.returncode, 'expected_pass': should_pass}
  check('complete_n4_candidates', 2, 0, True)
  check('wrong_candidate_count', 3, 0, False)
  check('wrong_stable_count', 2, 1, False)
  candidates.write_text(original + original)
  check('duplicate_candidates', 4, 0, False)
  candidates.write_text('')
  check('empty_candidates', 2, 0, False)
result = {'ok': True, 'cases': cases}
(here / 'scan_results/recheck_failure_tests.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
