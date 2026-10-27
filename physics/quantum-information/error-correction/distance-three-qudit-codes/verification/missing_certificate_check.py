"""Negative test for base-case coverage (standard library only; no assertions used).

Copies check_codes.py and certificates/ to a temporary directory, deletes one required base
certificate (certificates/base/q3_r4_n5.json) and runs check_codes.py there in default mode.
The run must exit nonzero and report base_cases_complete = false.  As a control, explicit-file
mode on a single remaining certificate must still exit 0.  The package itself is not modified.
Exits with status 1 if either expectation fails.
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REMOVED = os.path.join('certificates', 'base', 'q3_r4_n5.json')
CONTROL = os.path.join('certificates', 'table', 'q4_r5_n65.json')


def main():
  ok = True
  with tempfile.TemporaryDirectory() as tmp:
    shutil.copy(os.path.join(HERE, 'check_codes.py'), tmp)
    shutil.copytree(os.path.join(HERE, 'certificates'), os.path.join(tmp, 'certificates'))
    os.remove(os.path.join(tmp, REMOVED))
    run = subprocess.run([sys.executable, '-B', '-O', os.path.join(tmp, 'check_codes.py')],
                         capture_output=True, text=True)
    summary = json.load(open(os.path.join(tmp, 'check_codes_results.json')))['summary']
    default_ok = run.returncode != 0 and summary['base_cases_complete'] is False \
        and summary['base_case_missing'].get('q3_r4') == [5]
    print(json.dumps({'test': 'default mode with ' + REMOVED + ' removed', 'exit_code': run.returncode,
                      'base_case_missing': {k: v for k, v in summary['base_case_missing'].items() if v},
                      'base_cases_complete': summary['base_cases_complete'],
                      'rejected': default_ok}))
    ok = ok and default_ok
    ctl = subprocess.run([sys.executable, '-B', '-O', os.path.join(tmp, 'check_codes.py'),
                          os.path.join(tmp, CONTROL)], capture_output=True, text=True)
    print(json.dumps({'test': 'explicit-file mode on ' + CONTROL, 'exit_code': ctl.returncode,
                      'accepted': ctl.returncode == 0}))
    ok = ok and ctl.returncode == 0
  print('MISSING-CERTIFICATE CHECK PASSED' if ok else 'MISSING-CERTIFICATE CHECK FAILED')
  sys.exit(0 if ok else 1)


if __name__ == '__main__':
  main()
