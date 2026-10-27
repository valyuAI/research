#!/usr/bin/env python3
"""Second, independent check of Lemma 3.3: generate each of the 135 CNFs with indep_twotree.py (standard
library, no shared code with ../twotree.py) and solve with Kissat. Usage: run_indep_twotree.py [workers]
Environment: KISSAT (path to kissat binary), WORKDIR (scratch directory)."""
import sys, os, subprocess, time, json, hashlib, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from indep_cnf import shapes_by_insertion
workers = int(sys.argv[1]) if len(sys.argv) > 1 else 2
KIS = os.environ.get('KISSAT', 'kissat')
W = os.environ.get('WORKDIR') or tempfile.mkdtemp(prefix='indep14_')
ns = len(shapes_by_insertion(14))
def job(si):
    pre = os.path.join(W, 'c')
    subprocess.run([sys.executable, os.path.join(HERE, 'indep_twotree.py'), '14', '3', '4', pre, str(si)], check=True, capture_output=True)
    cnf = f'{pre}_{si:03d}.cnf'
    h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
    t0 = time.time()
    r = subprocess.run([KIS, '-q', '-n', cnf], capture_output=True, text=True)
    st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, f'rc{r.returncode}')
    os.remove(cnf)
    res = {'shape': si, 'status': st, 'secs': round(time.time() - t0, 1), 'cnf_sha256': h}
    print(json.dumps(res), flush=True); return res
with ThreadPoolExecutor(max_workers=workers) as ex:
    results = list(ex.map(job, range(ns)))
print('UNSAT', sum(r['status'] == 'UNSAT' for r in results), 'of', ns)
sys.exit(0 if all(r['status'] == 'UNSAT' for r in results) else 1)
