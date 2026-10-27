"""Sequential, fail-closed verification with durable logs and live heartbeats."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--quick', action='store_true', help='partial replay only')
  args = parser.parse_args()
  root = Path(__file__).resolve().parent.parent
  verification = root / 'verification'
  stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
  log_dir = verification / 'results' / 'replay' / stamp
  log_dir.mkdir(parents=True)
  manifest = {'started_utc': stamp, 'mode': 'partial' if args.quick else 'full', 'steps': []}
  inputs = [root / 'build.sh', root / 'paper.tex', root / 'references.bib']
  inputs += list(verification.glob('*.py'))
  for folder in ['data', 'data_extra', 'certificates']:
    inputs += sorted((verification / folder).glob('*'))
  manifest['input_sha256'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in inputs if p.is_file()}
  scripts = ['check_labels.py', 'check1_rank.py', 'check2_independent.py', 'check_flex_finite.py']
  if not args.quick:
    scripts += ['check_second_order.py', 'check_prestress.py', 'check_extra.py',
      'check_real_zeros_independent.py', 'exact_flex_dims.py', 'check2_independent.py --rank-only',
      'check_irreducible.py', 'check_antiprisms.py']
  scripts += ['summarize.py']
  commands = [(s, [sys.executable, '-B', '-u', *s.split()], verification) for s in scripts]
  tex = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'paper.tex']
  commands += [('latex-1', tex, root), ('bibtex', ['bibtex', 'paper'], root),
    ('latex-2', tex, root), ('latex-3', tex, root)]
  for index, (label, command, cwd) in enumerate(commands, 1):
    print(f'[{datetime.now(timezone.utc):%H:%M:%S UTC}] {index}/{len(commands)} START {label}', flush=True)
    path = log_dir / f'{index:02d}-{label.replace(" ", "_")}.log'
    start = time.monotonic()
    heartbeat = start
    with path.open('w') as output, path.open() as reader:
      child = subprocess.Popen(command, cwd=cwd, stdout=output, stderr=subprocess.STDOUT)
      while child.poll() is None:
        chunk = reader.read()
        if chunk:
          print(chunk, end='', flush=True)
        if time.monotonic() - heartbeat >= 25:
          print(f'{label}: active, {time.monotonic() - start:.0f}s elapsed', flush=True)
          heartbeat = time.monotonic()
        time.sleep(1)
      print(reader.read(), end='', flush=True)
    manifest['steps'].append({'command': command, 'cwd': str(cwd.relative_to(root)),
      'exit_code': child.returncode, 'elapsed_seconds': round(time.monotonic() - start, 2),
      'log': str(path.relative_to(root))})
    manifest['complete'] = False
    (log_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    if child.returncode:
      print(f'FAILED {label}; preserved log: {path}', flush=True)
      return child.returncode
  manifest['complete'] = True
  manifest['finished_utc'] = datetime.now(timezone.utc).isoformat()
  (log_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
  print('PARTIAL REPLAY ONLY' if args.quick else 'FULL REPLAY PASS', flush=True)
  print('Built', root / 'paper.pdf', flush=True)
  return 0


if __name__ == '__main__':
  sys.exit(main())
