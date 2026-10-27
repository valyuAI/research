#!/usr/bin/env python3
"""Regenerate every base CNF of the ledger with the encoder and compare its SHA-256 hash.

  python3 regenerate_cnfs.py                          hashes only (needs python-sat for the encoder)
  python3 regenerate_cnfs.py --drat-max-clauses N     also solve formulas with <= N clauses using
                                                      `cadical` and check the DRAT proof with
                                                      `drat-trim` (path in $DRAT_TRIM, default drat-trim)
  PYTHON=/path/to/python-with-pysat python3 regenerate_cnfs.py
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ENC = os.path.join(HERE, 'encoder', 'marked_syn.py')


def execute(command, expected_exit=0):
  print('RUN ' + ' '.join(command), flush=True)
  with tempfile.TemporaryFile(mode='w+') as log:
    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
    start = time.monotonic()
    while True:
      try:
        code = process.wait(timeout=20)
        break
      except subprocess.TimeoutExpired:
        print(f'  running {time.monotonic() - start:.0f}s', flush=True)
    log.seek(0)
    output = log.read()
  if code != expected_exit:
    raise RuntimeError(f'expected exit {expected_exit}, got {code}: {output[-2000:]}')
  return output


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('--drat-max-clauses', type=int, default=0)
  ns = ap.parse_args()
  py = os.environ.get('PYTHON', sys.executable)
  drat_trim = os.environ.get('DRAT_TRIM', 'drat-trim')
  T = json.load(open(os.path.join(HERE, 'results.json')))
  recs = [t['upper_bound'] for t in T['tiles']]
  with tempfile.TemporaryDirectory() as tmp:
    for u in recs:
      cnf = os.path.join(tmp, u['name'] + '.cnf')
      execute([py, ENC, u['grid'], json.dumps(u['cells']), '--k', str(u['k']), '--imb', '1', '--atleast',
               '--dimacs', cnf, '--cnf-only'])
      h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
      assert h == u['cnf_sha256'], (u['name'], 'CNF hash mismatch', h)
      msg = f"{u['name']}: CNF hash matches ({u['nvars']} vars, {u['nclauses']} clauses)"
      if u['nclauses'] <= ns.drat_max_clauses:
        proof = cnf[:-4] + '.drat'
        output = execute(['cadical', '-q', cnf, proof], expected_exit=20)
        assert re.search(r'^s UNSATISFIABLE$', output, re.M), (u['name'], 'no UNSAT conclusion')
        out = execute([drat_trim, cnf, proof])
        assert re.search(r'^s VERIFIED$', out.replace('\r', '\n'), re.M), (u['name'], 'drat-trim did not verify')
        os.remove(proof)
        msg += '; UNSAT, DRAT proof VERIFIED'
      os.remove(cnf)
      print(msg, flush=True)


if __name__ == '__main__':
  if not __debug__:
    raise SystemExit('FAIL: verification requires Python assertions enabled')
  main()
