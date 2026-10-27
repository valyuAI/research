"""Independent symbolic elimination for the J58/J59 real-zero obstruction.

The exact stress forms are shared with the first checker. Sympy's Groebner
algorithm and algebraic-number arithmetic independently check the elimination,
without the first checker's resultant, polynomial gcd, or Sturm routines.
"""
import json
import sympy as sp

from check_prestress import forms_of
from check_second_order import need


def main():
  x, y, z = sp.symbols('x y z')
  theta = 1 + sp.sqrt(5)
  out = {}
  for k in [58, 59]:
    print('J%s: recomputing exact forms' % k, flush=True)
    _, K, forms = forms_of(k)
    need(K.m == [-4, -2, 1], 'expected theta = 1 + sqrt(5)')
    variables = [x + 2*z, y - 3*z, x - y + z]
    polys = [sp.expand(sum(sum(sp.Rational(c.numerator, c.denominator) * theta**i
      for i, c in enumerate(M[a][b])) * variables[a] * variables[b]
      for a in range(3) for b in range(3))) for M in forms]
    # Projective chart y=1: lexicographic elimination removes z.
    basis = sp.groebner([p.subs(y, 1) for p in polys], z, x, extension=sp.sqrt(5))
    univariate = [sp.Poly(p.as_expr(), x, extension=sp.sqrt(5))
      for p in basis.polys if not p.as_expr().has(z)]
    need(len(univariate) == 1 and univariate[0].degree() == 2, 'quadratic elimination polynomial')
    disc = sp.simplify(sp.discriminant(univariate[0].as_expr(), x))
    need(disc.is_negative is True, 'exact negative discriminant')
    # The remaining projective chart y=0, x=1 has no complex solution.
    infinity = sp.groebner([p.subs({y: 0, x: 1}) for p in polys], z, extension=sp.sqrt(5))
    need(list(infinity) == [1], 'no common zero at infinity with x nonzero')
    need(any(sp.simplify(p.subs({x: 0, y: 0, z: 1})) != 0 for p in polys), 'exclude (0:0:1)')
    # The proper chart ideal with this irreducible quadratic also proves complex zeros exist.
    need(not basis.contains(sp.Integer(1)), 'chart ideal is proper')
    out[str(k)] = {'groebner_basis': [str(p) for p in basis],
      'elimination_discriminant': str(disc), 'discriminant_negative_exact': True,
      'infinity_excluded': True, 'no_nonzero_real_zero': True,
      'complex_projective_zero_exists': True}
    print('J%s: independent Groebner elimination PASS, negative discriminant %s' % (k, disc), flush=True)
  with open('results/real_zeros_independent.json', 'w') as f:
    json.dump(out, f, indent=2)


if __name__ == '__main__':
  main()
