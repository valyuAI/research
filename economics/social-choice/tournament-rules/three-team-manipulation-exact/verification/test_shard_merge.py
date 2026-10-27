"""Exercise real shard merging and reject incomplete or inconsistent evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
cases = {}
with tempfile.TemporaryDirectory(prefix='merge-check-') as directory:
  temp = Path(directory)
  paths = [temp / f'shard{i}.json' for i in range(2)]
  for i, path in enumerate(paths):
    subprocess.run([sys.executable, str(here / 'verify_rule.py'),
      str(here / 'certificates/rule_n3_k3.json'), str(path), f'--shard={i}/2'], check=True)
  original = paths[1].read_text()
  def check(name, files, should_pass):
    result = subprocess.run([sys.executable, str(here / 'combine_shards.py'),
      str(temp / 'merged.json'), *map(str, files)], capture_output=True, text=True)
    if (result.returncode == 0) != should_pass:
      raise RuntimeError(f'{name}: unexpected result {result.stdout} {result.stderr}')
    cases[name] = {'returncode': result.returncode, 'expected_pass': should_pass}
  check('complete_real_shards', paths, True)
  check('missing_shard', paths[:1], False)
  for name, field, value in [('different_certificate', 'certificate_sha256', '0' * 64),
                              ('failed_shard', 'ok', False),
                              ('different_definition', 'mode', 'eq')]:
    data = json.loads(original)
    data[field] = value
    paths[1].write_text(json.dumps(data))
    check(name, paths, False)
    paths[1].write_text(original)
result = {'ok': True, 'cases': cases}
(here / 'results/shard_failure_tests.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
