"""Check saved finite-field ideal-membership identities using only Python.

The accepted grammar is integer-coefficient polynomials in t0,...,t(n-1).
No symbolic algebra system, numerical tolerance, or assertion is used.
"""

import re

PRIME = 32003
BITS = 5


def require(condition, message):
  if not condition:
    raise ValueError(message)


def exponents(key, variables):
  return tuple((key >> (BITS * i)) & 31 for i in range(variables))


def parse_polynomial(expression, variables):
  expression = re.sub(r"\s+", "", expression)
  require(bool(expression), "Empty polynomial")
  terms = re.findall(r"[+-]?[^+-]+", expression)
  require("".join(terms) == expression, "Unsupported polynomial grammar")
  result = {}
  for term in terms:
    coefficient = -1 if term.startswith("-") else 1
    term = term.lstrip("+-")
    powers = [0] * variables
    for factor in term.split("*"):
      if re.fullmatch(r"\d+", factor):
        coefficient *= int(factor)
      else:
        match = re.fullmatch(r"t(\d+)(?:\^(\d+))?", factor)
        require(match is not None, "Unsupported factor: " + factor)
        variable, power = int(match[1]), int(match[2] or 1)
        require(variable < variables and power < 16, "Invalid variable/power")
        powers[variable] += power
    require(max(powers) < 16, "Power exceeds safe multiplication encoding")
    key = sum(power << (BITS * i) for i, power in enumerate(powers))
    result[key] = (result.get(key, 0) + coefficient) % PRIME
  return {key: value for key, value in result.items() if value}


def multiply_add(total, left, right):
  for left_key, left_value in left.items():
    for right_key, right_value in right.items():
      key = left_key + right_key
      total[key] = (total.get(key, 0) + left_value * right_value) % PRIME


def leading_key(polynomial, variables):
  def order(key):
    powers = exponents(key, variables)
    return (sum(powers),) + tuple(-value for value in powers[::-1])
  require(bool(polynomial), "Zero target")
  return max(polynomial, key=order)
