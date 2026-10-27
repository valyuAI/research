#!/usr/bin/env python3
"""Replay the certificate run for Lemma 3.3 (two trees on [14] always have separated sets of sizes 3 and 4).

For every one of the 135 unrooted shapes: regenerate the CNF with twotree.py (standard library), compare
its SHA-256 with ../results/twotree_n14_cadical_drat.json, and, unless --hash-only is given, solve it with
CaDiCaL writing a DRAT proof and verify the proof with DRAT-trim.

Usage: run_twotree_certificates.py [--hash-only] [--workers N] [--shapes i,j,...]
Environment: CADICAL (path to cadical binary), DRAT_TRIM (path to drat-trim), WORKDIR (scratch dir)."""
import argparse, hashlib, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from twotree import build
from shapes import unrooted_shapes

def write_cnf(si, path):
    adj = unrooted_shapes(14)[si]
    nv, cls = build(14, 3, 4, adj)
    with open(path, 'w') as f:
        f.write(f'c twotree n=14 s=3 t=4 shape={si}\np cnf {nv} {len(cls)}\n')
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hash-only', action='store_true')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--shapes', default=None)
    a = ap.parse_args()
    rec = {r['shape']: r for r in json.load(open(os.path.join(HERE, '..', 'results', 'twotree_n14_cadical_drat.json')))}
    shapes = list(range(135)) if a.shapes is None else [int(x) for x in a.shapes.split(',')]
    work = os.environ.get('WORKDIR') or tempfile.mkdtemp(prefix='twotree14_')
    cad = os.environ.get('CADICAL', 'cadical'); dt = os.environ.get('DRAT_TRIM', 'drat-trim')
    def job(si):
        cnf = os.path.join(work, f's{si:03d}.cnf'); prf = cnf[:-4] + '.drat'
        write_cnf(si, cnf)
        h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
        out = {'shape': si, 'hash_matches_record': h == rec[si]['cnf_sha256']}
        if not a.hash_only:
            t0 = time.time()
            r = subprocess.run([cad, '-q', cnf, prf], capture_output=True, text=True)
            out['status'] = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, f'rc{r.returncode}')
            out['solve_s'] = round(time.time() - t0, 1)
            if out['status'] == 'UNSAT':
                v = subprocess.run([dt, cnf, prf, '-t', '200000'], capture_output=True, text=True)
                out['drat'] = 'VERIFIED' if 's VERIFIED' in v.stdout else 'FAILED'
            if os.path.exists(prf): os.remove(prf)
        os.remove(cnf)
        print(json.dumps(out), flush=True)
        return out
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(job, shapes))
    ok = all(r['hash_matches_record'] and (a.hash_only or (r['status'] == 'UNSAT' and r['drat'] == 'VERIFIED')) for r in res)
    print('ALL OK' if ok else 'FAILURES', len(res), 'shapes')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
