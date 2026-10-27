"""Independently check the rank-one certificate by rational linear algebra.

No Groebner calculation is used. All 34 displayed quadratic equations are
verified to be constant linear combinations of the original 2x2 minors.
"""

import itertools
import json
import re
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
FIELD = sp.QQ_I


def add_scaled(target, source, factor):
  for key, value in source.items():
    new = target.get(key, FIELD.zero) + factor * value
    if new:
      target[key] = new
    elif key in target:
      del target[key]


def main():
  data = json.loads((ROOT / "recursive_normal_borel_checks.json").read_text())
  w = sp.symbols("w0:8")
  entries = [[sp.sympify(value) for value in row] for row in data["next_normal_matrix"]]
  coefficients = [[[FIELD.from_sympy(sp.diff(value, variable)) for variable in w]
                   for value in row] for row in entries]
  monomials = list(itertools.combinations_with_replacement(range(8), 2))
  pivots = {}
  independent = []
  independent_vectors = []
  total = 0
  for rows in itertools.combinations(range(7), 2):
    for columns in itertools.combinations(range(13), 2):
      a, b = rows
      c, d = columns
      vector = {}
      for key, (i, j) in enumerate(monomials):
        value = coefficients[a][c][i] * coefficients[b][d][j] - coefficients[a][d][i] * coefficients[b][c][j]
        if i != j:
          value += coefficients[a][c][j] * coefficients[b][d][i] - coefficients[a][d][j] * coefficients[b][c][i]
        if value:
          vector[key] = value
      total += 1
      representation = {}
      original = dict(vector)
      while vector:
        first = min(vector)
        if first not in pivots:
          index = len(independent)
          independent.append({"rows_zero_based": rows, "columns_zero_based": columns})
          independent_vectors.append(original)
          representation[index] = FIELD.one
          scale = FIELD.one / vector[first]
          pivots[first] = (
            {key: value * scale for key, value in vector.items()},
            {key: value * scale for key, value in representation.items()},
          )
          break
        previous, combination = pivots[first]
        scale = -vector[first]
        add_scaled(vector, previous, scale)
        add_scaled(representation, combination, scale)
      if total % 250 == 0:
        print(f"{total}/1638 minors inspected; span rank={len(pivots)}", flush=True)
  text = (ROOT / "third_normal_rank1.log").read_text()
  equations = re.findall(r"^G\[\d+\]=(.*)$", text, re.MULTILINE)
  verified = []
  for expression in equations:
    expression = expression.replace("ii", "I").replace("^", "**")
    poly = sp.Poly(sp.sympify(expression), *w)
    vector = {
      key: FIELD.from_sympy(poly.coeff_monomial(w[i] * w[j]))
      for key, (i, j) in enumerate(monomials)
    }
    vector = {key: value for key, value in vector.items() if value}
    target = dict(vector)
    combination = {}
    while vector:
      first = min(vector)
      assert first in pivots
      previous, representation = pivots[first]
      scale = vector[first]
      add_scaled(vector, previous, -scale)
      add_scaled(combination, representation, scale)
    reconstructed = {}
    for index, coefficient in combination.items():
      add_scaled(reconstructed, independent_vectors[index], coefficient)
    assert reconstructed == target
    verified.append({
      "quadratic": str(poly.as_expr()),
      "independent_minor_combination": {str(key): str(FIELD.to_sympy(value)) for key, value in combination.items()},
    })
  assert len(equations) == 34
  polys = [sp.sympify(e.replace("ii", "I").replace("^", "**")) for e in equations]
  assert polys[0] == w[7]**2 and polys[8] == w[6]**2 and polys[15] == w[5]**2
  zeros = {w[7]: 0, w[6]: 0, w[5]: 0}
  assert sp.expand(polys[21].subs(zeros)) == w[4]**2
  zeros[w[4]] = 0
  assert sp.expand(polys[28].subs(zeros)) == 2*w[2]**2
  zeros[w[2]] = 0
  assert sp.expand(polys[27].subs(zeros)) == 2*w[0]*w[3]
  assert sp.expand((polys[32] + polys[27]).subs(zeros)) == 3*w[0]*w[1]
  assert sp.expand((polys[33] - polys[32]/3 + polys[27]/6).subs(zeros)) == w[0]**2
  zeros[w[0]] = 0
  assert sp.expand(polys[26].subs(zeros) - w[3]*(w[1]-w[3])) == 0
  assert sp.expand((polys[31]/3 - polys[26]).subs(zeros) - (w[1]-w[3])**2) == 0
  parameter = sp.Symbol("t")
  line = dict(zip(w, [0, parameter, 0, parameter, 0, 0, 0, 0]))
  line_matrix = sp.Matrix(entries).subs(line)
  assert line_matrix.rank() == 1
  report = {
    "field": "Q(i)",
    "all_2x2_minors_inspected": total,
    "quadratic_minor_span_rank": len(pivots),
    "verified_equations": len(verified),
    "independent_minors": independent,
    "equation_certificates": verified,
    "claimed_support_line": "w0=w2=w4=w5=w6=w7=0, w1=w3",
    "rank_on_nonzero_support_line": 1,
    "set_theoretic_elimination": [
      "G1,G9,G16 force w7=w6=w5=0.",
      "G22 then forces w4=0; G29 forces w2=0.",
      "G28 gives w0*w3=0; G33 then gives w0*w1=0; G34 gives w0^2=0, hence w0=0.",
      "G27 and G32 give w3*(w1-w3)=0 and w1*(w1-w3)=0; their difference gives (w1-w3)^2=0.",
      "The displayed line has matrix rank one. Thus the set of all rank<=1 points is exactly that affine line.",
    ],
    "affine_dimension_proved": 1,
  }
  (ROOT / "rank1_minor_independent_certificate.json").write_text(json.dumps(report, indent=2) + "\n")
  print("All34 equations independently verified in the original minor span; support line verified.", flush=True)


if __name__ == "__main__":
  main()
