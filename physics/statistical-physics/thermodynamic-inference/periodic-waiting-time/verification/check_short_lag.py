"""Exact rational Fourier-polynomial check of the short-lag derivative."""

from fractions import Fraction as F


def add(*polynomials):
  result = {}
  for polynomial in polynomials:
    for key, (real, imag) in polynomial.items():
      x, y = result.get(key, (F(0), F(0)))
      result[key] = (x + real, y + imag)
  return {k: v for k, v in result.items() if v != (0, 0)}


def scale(p, factor):
  return {k: (factor * v[0], factor * v[1]) for k, v in p.items()}


def mul(p, q):
  terms = []
  for (k, d), (x, y) in p.items():
    for (l, e), (u, v) in q.items():
      terms.append({(k + l, d + e): (x * u - y * v, x * v + y * u)})
  return add(*terms)


def derivative(p):
  return {(k, d): (-k * y, k * x) for (k, d), (x, y) in p.items()}


def average(p):
  return {d: value for (k, d), value in add(p).items() if k == 0}


def require(actual, expected, label):
  if actual != expected:
    raise ValueError(f"{label}: {actual} != {expected}")
  print("PASS " + label, flush=True)


def main():
  # Keys encode exp(i*k*t) * epsilon**d.
  one = {(0, 0): (F(1), F(0))}
  cosine = {(1, 1): (F(1, 2), F(0)), (-1, 1): (F(1, 2), F(0))}
  sine = {(1, 1): (F(0), F(-1, 2)), (-1, 1): (F(0), F(1, 2))}
  a, b = add(one, cosine), add(one, sine)
  unit = {0: (F(1), F(0))}
  require(average(a), unit, "mean a = 1")
  require(average(b), unit, "mean b = 1")
  require(average(mul(a, b)), unit, "f(0) = g(0) = 1")
  hazard = mul(mul(a, b), add(a, b))
  f_prime = average(add(mul(a, derivative(b)), scale(hazard, -1)))
  g_prime = average(add(mul(b, derivative(a)), scale(hazard, -1)))
  require(f_prime, {0: (F(-2), F(0)), 2: (F(-1, 2), F(0))},
    "f'(0) = -2 - epsilon^2/2")
  require(g_prime, {0: (F(-2), F(0)), 2: (F(-3, 2), F(0))},
    "g'(0) = -2 - 3 epsilon^2/2")
  difference = average(add(mul(a, derivative(b)), scale(mul(b, derivative(a)), -1)))
  require(difference, {2: (F(1), F(0))}, "(f-g)'(0) = epsilon^2")


if __name__ == "__main__":
  main()
