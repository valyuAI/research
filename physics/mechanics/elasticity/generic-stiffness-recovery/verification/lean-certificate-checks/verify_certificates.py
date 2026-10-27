"""Verify minor-ideal dimension certificates using only Python's standard library.

Arithmetic is exact in Q(i), represented by pairs of fractions. Determinants
are recomputed from the original linear matrix. No CAS or Groebner engine is
imported, and no rank or ideal-membership solver is trusted by this checker.
"""

import ast
import itertools
import json
import time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
MONOMIAL_ONE = (0,)*8


def cadd(a, b):
  return (a[0]+b[0], a[1]+b[1])


def cmul(a, b):
  return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def cinv(a):
  norm = a[0]*a[0]+a[1]*a[1]
  assert norm
  return (a[0]/norm, -a[1]/norm)


def add(a, b, scalar=ONE):
  result = dict(a)
  for monomial, coefficient in b.items():
    value = cadd(result.get(monomial, ZERO), cmul(scalar, coefficient))
    if value != ZERO:
      result[monomial] = value
    elif monomial in result:
      del result[monomial]
  return result


def multiply(a, b):
  result = {}
  for x, c in a.items():
    for y, d in b.items():
      monomial = tuple(i+j for i, j in zip(x, y))
      value = cadd(result.get(monomial, ZERO), cmul(c, d))
      if value != ZERO:
        result[monomial] = value
      elif monomial in result:
        del result[monomial]
  return result


def constant(coefficient):
  return {} if coefficient == ZERO else {MONOMIAL_ONE: coefficient}


def variable(index):
  return {tuple(int(j == index) for j in range(8)): ONE}


def parse(expression):
  def walk(node):
    if isinstance(node, ast.Constant) and type(node.value) is int:
      return constant((Fraction(node.value), Fraction(0)))
    if isinstance(node, ast.Name):
      if node.id == "I":
        return constant((Fraction(0), Fraction(1)))
      if node.id in {f"w{i}" for i in range(8)}:
        return variable(int(node.id[1:]))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
      return add({}, walk(node.operand), (Fraction(-1), Fraction(0)))
    if isinstance(node, ast.BinOp):
      a = walk(node.left)
      if isinstance(node.op, ast.Pow):
        assert isinstance(node.right, ast.Constant) and type(node.right.value) is int
        assert 0 <= node.right.value <= 8
        result = constant(ONE)
        for _ in range(node.right.value):
          result = multiply(result, a)
        return result
      b = walk(node.right)
      if isinstance(node.op, ast.Add):
        return add(a, b)
      if isinstance(node.op, ast.Sub):
        return add(a, b, (Fraction(-1), Fraction(0)))
      if isinstance(node.op, ast.Mult):
        return multiply(a, b)
      if isinstance(node.op, ast.Div):
        assert set(b) == {MONOMIAL_ONE}
        return add({}, a, cinv(b[MONOMIAL_ONE]))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")
  return walk(ast.parse(expression, mode="eval").body)


def coefficient(expression):
  polynomial = parse(expression)
  assert not polynomial or set(polynomial) == {MONOMIAL_ONE}
  return polynomial.get(MONOMIAL_ONE, ZERO)


def grevlex(monomial):
  return (sum(monomial), tuple(-x for x in reversed(monomial)))


def main():
  if not __debug__:
    raise RuntimeError("Run this verifier without Python's -O option.")
  started = time.monotonic()
  data = json.loads((ROOT / "minor_dimension_certificates.json").read_text())
  assert set(data["bounds"]) == {"2", "3"}
  matrix = [[parse(x) for x in row] for row in data["matrix"]]
  assert len(matrix) == 7 and all(len(row) == 13 for row in matrix)
  assert all(all(sum(m) == 1 for m in entry) for row in matrix for entry in row)

  @lru_cache(None)
  def minor(rows, columns):
    assert len(rows) == len(columns)
    if len(rows) == 1:
      return matrix[rows[0]][columns[0]]
    result = {}
    for index, col in enumerate(columns):
      product = multiply(matrix[rows[0]][col], minor(rows[1:], columns[:index]+columns[index+1:]))
      result = add(result, product, (Fraction((-1)**index), Fraction(0)))
    return result

  records = []
  for rank, claim in data["bounds"].items():
    size = int(rank)+1
    assert claim["minor_size"] == size
    supports, leading = [], []
    for cert in claim["certificates"]:
      powers = [tuple(t["powers"]) for t in cert["polynomial"]]
      assert len(set(powers)) == len(powers)
      assert all(len(m) == 8 and all(type(e) is int and e >= 0 for e in m) for m in powers)
      target = {tuple(t["powers"]): coefficient(t["coefficient"]) for t in cert["polynomial"]}
      assert target and all(c != ZERO for c in target.values())
      reconstructed = {}
      for term in cert["minor_combination"]:
        descriptor = claim["independent_minors"][term["minor"]]
        rows, columns = tuple(descriptor["rows"]), tuple(descriptor["columns"])
        assert rows == tuple(sorted(set(rows))) and columns == tuple(sorted(set(columns)))
        assert len(rows) == len(columns) == size
        assert all(0 <= j < 7 for j in rows) and all(0 <= j < 13 for j in columns)
        polynomial = minor(rows, columns)
        if term["multiplier_variable"] is not None:
          index = term["multiplier_variable"]
          assert type(index) is int and 0 <= index < 8
          polynomial = multiply(variable(index), polynomial)
        reconstructed = add(reconstructed, polynomial, coefficient(term["coefficient"]))
      assert reconstructed == target, f"Failed rank-{rank} identity {cert['target_id']}"
      lm = max(target, key=grevlex)
      supports.append({j for j, exponent in enumerate(lm) if exponent})
      leading.append(list(lm))
      print(f"Rank<={rank}, identity {cert['target_id']}: exact original-minor reconstruction passed", flush=True)
    minimum = None
    covers = None
    for cover_size in range(9):
      found = [list(c) for c in itertools.combinations(range(8), cover_size)
               if all(set(c) & support for support in supports)]
      if found:
        minimum, covers = cover_size, found
        break
    assert minimum == claim["minimum_variable_cover_size"]
    assert covers == claim["minimum_variable_covers"]
    assert 8-minimum == claim["dimension_upper_bound"]
    assert claim["dimension_upper_bound"] == int(rank)
    records.append({"rank_bound": int(rank), "identities_verified": len(leading),
      "leading_monomials": leading, "minimum_variable_cover_size": minimum,
      "minimum_variable_covers": covers, "dimension_upper_bound": 8-minimum})
    print(f"Rank<={rank}: independently verified dimension upper bound {8-minimum}", flush=True)
  result = {"verification": "PASS", "arithmetic": "Python standard-library Fraction pairs for Q(i)",
    "uses_CAS": False, "uses_Groebner_basis": False, "bounds": records,
    "elapsed_seconds": time.monotonic()-started}
  (ROOT / "independent_verification.json").write_text(json.dumps(result, indent=2)+"\n")
  print(f"All identities and dimension bounds passed in {result['elapsed_seconds']:.2f}s", flush=True)


if __name__ == "__main__":
  main()
