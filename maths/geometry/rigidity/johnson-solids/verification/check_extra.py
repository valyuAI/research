"""Consistency check against arXiv:2607.09252 (AHWZ): our second-order pipeline on the regular dodecahedron and
the truncated icosahedron (exact data in data_extra/, built by make_extra.py and validated exactly). AHWZ report
both as first-order flexible (5 flexes), second-order rigid, and (numerically) not prestress stable."""
import json
from check_second_order import macaulay_full_rank, need
from check_prestress import forms_of, verify_certificate


def main():
  certs = json.load(open('certificates/prestress.json'))
  out = {}
  for path in ['data_extra/dodecahedron.json', 'data_extra/truncated_icosahedron.json']:
    print('Recomputing exact forms:', path, flush=True)
    name, K, forms = forms_of(path)
    d = len(forms[0])
    need(d == len(forms) == 5, 'expected five flexes and five stresses')
    print(name, 'checking degree-six Macaulay matrix', flush=True)
    rank, monomials = macaulay_full_rank(K, forms, d + 1)
    need(rank == monomials == 210, 'Macaulay matrix must have full rank 210')
    verify_certificate(K, forms, certs[path])
    out[path] = {'name': name, 'flex_dim': d, 'stress_dim': len(forms),
      'macaulay': {'degree': d + 1, 'rank': rank, 'monomials': monomials},
      'second_order_rigid': True, 'not_prestress_stable_certificate': True}
    print(name, ': rank 210/210, exact dual certificate PASS', flush=True)
  with open('results/extra_replay.json', 'w') as f:
    json.dump(out, f, indent=2)
  print('CONSISTENT WITH AHWZ; BOTH DUAL CERTIFICATES REPLAYED', flush=True)


if __name__ == '__main__':
  main()
