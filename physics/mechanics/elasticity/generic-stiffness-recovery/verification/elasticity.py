"""Construct the 21-parameter elasticity and its Christoffel coefficients."""

import itertools
import sympy as sp

def build_coefficients():
  pairs = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
  index = {tuple(sorted(pair)): i for i, pair in enumerate(pairs)}
  positions = list(itertools.combinations_with_replacement(range(6), 2))
  variables = sp.symbols(" ".join(f"c{i + 1}{j + 1}" for i, j in positions))
  voigt = sp.zeros(6)
  for variable, (i, j) in zip(variables, positions):
    voigt[i, j] = voigt[j, i] = variable
  p = sp.symbols("p1:4")

  def tensor(i, j, k, l):
    return voigt[index[tuple(sorted((i, j)))], index[tuple(sorted((k, l)))]]

  gamma = sp.Matrix(3, 3, lambda i, l: sum(
    tensor(i, j, k, l) * p[j] * p[k] for j in range(3) for k in range(3)
  ))
  assert gamma == gamma.T
  trace = sp.trace(gamma)
  second = (trace**2 - sp.trace(gamma * gamma)) / 2
  determinant = gamma.det(method="domain-ge")
  groups = []
  for power, expression in [(0, determinant), (1, second), (2, trace)]:
    coefficients = sp.Poly(sp.expand(expression), *p).terms()
    for monomial, coefficient in coefficients:
      terms = {tuple(exponent): int(value) for exponent, value in sp.Poly(coefficient, *variables).terms()}
      groups.append({"r_power": power, "p_monomial": monomial, "terms": terms})
    print(f"Built degree {6 - 2 * power} slowness coefficients: {len(coefficients)}", flush=True)
  assert len(groups) == 49
  return variables, gamma, p, groups
