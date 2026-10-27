"""Reconstruct the polytope and verify its modular obstruction certificate.

Standard library only. No probe, certificate generator, or CAS is imported.
Geometry is checked in Q(sqrt(5)), independently of the saved Q(phi) encoding.
The geometric deduction from this certificate is a separate written proof.
"""

import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
P = 1009
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
PHI = (Fraction(1, 2), Fraction(1, 2))
SQRT5 = (Fraction(0), Fraction(1))


def require(condition, message):
  if not condition:
    raise ValueError(message)


def add(x, y):
  return x[0] + y[0], x[1] + y[1]


def neg(x):
  return -x[0], -x[1]


def sub(x, y):
  return add(x, neg(y))


def mul(x, y):
  return x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def div(x, y):
  denominator = y[0] ** 2 - 5 * y[1] ** 2
  require(denominator != 0, "Division by zero in Q(sqrt(5))")
  return mul(x, (y[0] / denominator, -y[1] / denominator))


def integer(n):
  return Fraction(n), Fraction(0)


def sign(x):
  if x == ZERO:
    return 0
  low, high = Fraction(2), Fraction(3)
  for _ in range(128):
    endpoints = [x[0] + x[1] * low, x[0] + x[1] * high]
    if min(endpoints) > 0:
      return 1
    if max(endpoints) < 0:
      return -1
    middle = (low + high) / 2
    if middle * middle > 5:
      high = middle
    else:
      low = middle
  raise ValueError("Exact real-embedding comparison did not separate")


def dot(x, y):
  answer = ZERO
  for a, b in zip(x, y):
    answer = add(answer, mul(a, b))
  return answer


def difference(x, y):
  return tuple(sub(a, b) for a, b in zip(x, y))


def cross(x, y):
  return tuple(sub(mul(x[(i + 1) % 3], y[(i + 2) % 3]),
                   mul(x[(i + 2) % 3], y[(i + 1) % 3])) for i in range(3))


def determinant(matrix):
  a = [row[:] for row in matrix]
  result = ONE
  for j in range(len(a)):
    pivot = next((i for i in range(j, len(a)) if a[i][j] != ZERO), None)
    if pivot is None:
      return ZERO
    if pivot != j:
      a[j], a[pivot] = a[pivot], a[j]
      result = neg(result)
    value = a[j][j]
    result = mul(result, value)
    for i in range(j + 1, len(a)):
      scale = div(a[i][j], value)
      for k in range(j + 1, len(a)):
        a[i][k] = sub(a[i][k], mul(scale, a[j][k]))
      a[i][j] = ZERO
  return result


def parse_point(row):
  require(len(row) == 3, "Expected three coordinates")
  result = []
  for a, b in row:
    a, b = Fraction(a), Fraction(b)
    result.append((a + b / 2, b / 2))
  return tuple(result)


def field_mod(x, phi):
  def rational(value):
    require(value.denominator % P != 0, "Nonintegral coordinate at selected prime")
    return value.numerator * pow(value.denominator, -1, P) % P
  return (rational(x[0]) + (2 * phi - 1) * rational(x[1])) % P


def regular_face(points, face, edges):
  n = len(face)
  require(n in (3, 5, 10), "Unexpected polygon size")
  center = tuple(div(sum_field(points[i][k] for i in face), integer(n)) for k in range(3))
  radius = dot(difference(points[face[0]], center), difference(points[face[0]], center))
  require(sign(radius) > 0, "Degenerate face radius")
  cosine = {3: (Fraction(-1, 2), Fraction(0)),
            5: div(sub(PHI, ONE), integer(2)), 10: div(PHI, integer(2))}[n]
  local_edges = [(i, j) for i, j in edges if i in face and j in face]
  require(len(local_edges) == n, "Polygon has wrong edge count")
  for i in face:
    require(sum(i in edge for edge in local_edges) == 2, "Polygon degree is not two")
    delta = difference(points[i], center)
    require(dot(delta, delta) == radius, "Face vertices are not concyclic")
  seen = {face[0]}
  while True:
    enlarged = seen | {j for edge in local_edges for j in edge if any(i in seen for i in edge)}
    if enlarged == seen:
      break
    seen = enlarged
  require(seen == set(face), "Disconnected face boundary")
  for i, j in local_edges:
    require(dot(difference(points[i], center), difference(points[j], center)) == mul(cosine, radius),
            "Incorrect regular-polygon central angle")


def sum_field(values):
  result = ZERO
  for value in values:
    result = add(result, value)
  return result


def verify_geometry(data):
  vertices = [parse_point(row) for row in data["vertices"]]
  normals = [parse_point(row) for row in data["normals"]]
  facets = [tuple(face) for face in data["facets"]]
  edges = [tuple(edge) for edge in data["edges"]]
  require(len(vertices) == len(set(vertices)) == 60 and len(normals) == len(facets) == 32,
          "Wrong vertex/facet census")
  require(sorted(map(len, facets)) == [3] * 20 + [10] * 12, "Wrong facet types")
  require(all(tuple(sorted(set(f))) == f and all(0 <= i < 60 for i in f) for f in facets),
          "Malformed facet")
  length_squared = sub(integer(8), mul(integer(4), PHI))
  actual_edges = [edge for edge in itertools.combinations(range(60), 2)
                  if dot(difference(vertices[edge[0]], vertices[edge[1]]),
                         difference(vertices[edge[0]], vertices[edge[1]])) == length_squared]
  require(edges == actual_edges and len(edges) == 90, "Saved edges differ from exact length pairs")
  strict_inequalities = 0
  for face, normal in zip(facets, normals):
    for i, vertex in enumerate(vertices):
      value = sub(dot(vertex, normal), ONE)
      require(value == ZERO if i in face else sign(value) < 0, "Supporting-facet test failed")
      strict_inequalities += i not in face
    reconstructed = None
    for i, j, k in itertools.combinations(face, 3):
      perpendicular = cross(difference(vertices[j], vertices[i]), difference(vertices[k], vertices[i]))
      offset = dot(perpendicular, vertices[i])
      if offset != ZERO:
        reconstructed = tuple(div(value, offset) for value in perpendicular)
        break
    require(reconstructed == normal, "Independent facet-normal reconstruction failed")
    regular_face(vertices, face, edges)
  for i in range(60):
    incident = [j for j, f in enumerate(facets) if i in f]
    require(len(incident) == 3 and sum(i in e for e in edges) == 3, "Vertex is not simple")
    require(determinant([list(normals[j]) for j in incident]) != ZERO, "Facet normals are dependent")
    require({tuple(j for j in incident if other in facets[j])
             for e in edges if i in e for other in e if other != i} == set(itertools.combinations(incident, 2)),
            "Incident edges do not realize all three trihedral rays")
  require(all(sum(i in f and j in f for f in facets) == 2 for i, j in edges), "Wrong edge-facet incidence")

  original = set(itertools.product((neg(ONE), ONE), repeat=3))
  for signs in itertools.product((-1, 1), repeat=2):
    point = (ZERO, mul(integer(signs[0]), sub(PHI, ONE)), mul(integer(signs[1]), PHI))
    for shift in range(3):
      original.add(point[shift:] + point[:shift])
  original = sorted(original)
  require(len(original) == 20 and all(dot(v, v) == integer(3) for v in original), "Original dodecahedron coordinates failed")
  original_edges = [e for e in itertools.combinations(range(20), 2)
                    if dot(difference(original[e[0]], original[e[1]]), difference(original[e[0]], original[e[1]])) == length_squared]
  require(len(original_edges) == 30 and all(sum(i in e for e in original_edges) == 3 for i in range(20)),
          "Original dodecahedron edge census failed")
  directed = {}
  for i, j in original_edges:
    for a, b in [(i, j), (j, i)]:
      directed[a, b] = tuple(add(mul(PHI, x), mul(sub(PHI, ONE), y)) for x, y in zip(original[a], original[b]))
  require(set(directed.values()) == set(vertices), "Saved polytope is not the stated exact truncation")
  index = {v: i for i, v in enumerate(vertices)}
  triangles = {tuple(sorted(index[v] for (a, _), v in directed.items() if a == i)) for i in range(20)}
  require(triangles == {f for f in facets if len(f) == 3}, "Truncation triangles mismatch")
  original_facets, original_normals = [], []
  for face, normal in zip(facets, normals):
    if len(face) != 10:
      continue
    original_normal = tuple(mul(SQRT5, x) for x in normal)
    original_face = tuple(i for i, v in enumerate(original) if dot(v, original_normal) == ONE)
    require(len(original_face) == 5, "Retained facet does not come from a pentagon")
    require(all(sign(sub(dot(v, original_normal), ONE)) <= 0 for v in original), "Original pentagon is not supporting")
    regular_face(original, original_face, original_edges)
    truncated_face = tuple(sorted(index[v] for (a, b), v in directed.items() if a in original_face and b in original_face))
    require(truncated_face == face, "Truncation decagon mismatch")
    original_facets.append(original_face)
    original_normals.append(original_normal)
  require(len(set(original_facets)) == 12 and all(sum(i in f for f in original_facets) == 3 for i in range(20)),
          "Original regular-dodecahedron facet census failed")
  require(all(sum(i in f and j in f for f in original_facets) == 2 for i, j in original_edges),
          "Original dodecahedron edge-facet incidence failed")
  for i in range(20):
    incident = [j for j, f in enumerate(original_facets) if i in f]
    require(determinant([list(original_normals[j]) for j in incident]) != ZERO,
            "Original dodecahedron facet normals are dependent")
  truncation = div(sub(PHI, ONE), SQRT5)
  require(truncation == div(ONE, add(PHI, integer(2))), "Truncation fraction mismatch")
  require(mul(PHI, truncation) == sub(ONE, mul(integer(2), truncation)), "Uniform edge-length relation failed")
  print("PASS exact Q(sqrt5) geometry, all supports, regular polygons, and uniform dodecahedral truncation", flush=True)
  return vertices, normals, facets, edges, {
    "vertices": 60, "edges": 90, "facets": 32,
    "strict_supporting_inequalities": strict_inequalities,
    "exact_regular_faces": {"triangles": 20, "decagons": 12},
    "original_regular_pentagons": 12,
    "identification": "phi*a+(phi-1)*b for each directed edge a->b of the standard dodecahedron; normalized truncation fraction1/(phi+2)",
  }


def shape(matrix, rows, columns, label):
  require(len(matrix) == rows and all(len(row) == columns for row in matrix), label + " shape mismatch")
  require(all(type(value) is int and 0 <= value < P for row in matrix for value in row), label + " noncanonical entry")


def small_rank(matrix):
  a = [[v % P for v in row] for row in matrix]
  rank = 0
  for column in range(len(a[0])):
    pivot = next((r for r in range(rank, len(a)) if a[r][column]), None)
    if pivot is None:
      continue
    a[rank], a[pivot] = a[pivot], a[rank]
    scale = pow(a[rank][column], -1, P)
    a[rank] = [v * scale % P for v in a[rank]]
    for r in range(rank + 1, len(a)):
      scale = a[r][column]
      a[r] = [(u - scale * v) % P for u, v in zip(a[r], a[rank])]
    rank += 1
    if rank == len(a):
      break
  return rank


def verify_modular(data, vertices, normals, facets, edges):
  phi = data["phi_mod_p"]
  require(data["prime"] == P and all(P % i for i in range(2, 32)), "Incorrect/nonprime modulus")
  require(type(phi) is int and 0 <= phi < P and (phi * phi - phi - 1) % P == 0, "Invalid golden-ratio residue")
  points = [[field_mod(x, phi) for x in point] for point in vertices + normals]
  jacobian, quadratic = [], []
  for i, j in edges:
    row = {}
    for k in range(3):
      delta = (points[i][k] - points[j][k]) % P
      row[3 * i + k], row[3 * j + k] = 2 * delta % P, -2 * delta % P
    jacobian.append(row)
    quadratic.append([(3 * i + k, 3 * i + k, 1) for k in range(3)]
                     + [(3 * j + k, 3 * j + k, 1) for k in range(3)]
                     + [(3 * i + k, 3 * j + k, -2) for k in range(3)])
  for f, face in enumerate(facets):
    normal = 60 + f
    for i in face:
      jacobian.append({**{3 * i + k: points[normal][k] for k in range(3)},
                       **{3 * normal + k: points[i][k] for k in range(3)}})
      quadratic.append([(3 * i + k, 3 * normal + k, 1) for k in range(3)])
  require(len(jacobian) == 270, "Incorrect ungauged equation count")
  motions = []
  for point in vertices:
    x, y, z = point
    motions.extend([[ONE, ZERO, ZERO, ZERO, neg(z), y],
                    [ZERO, ONE, ZERO, z, ZERO, neg(x)],
                    [ZERO, ZERO, ONE, neg(y), x, ZERO]])
  for normal in normals:
    x, y, z = normal
    translations = [[neg(mul(a, b)) for b in normal] for a in normal]
    rotations = [[ZERO, neg(z), y], [z, ZERO, neg(x)], [neg(y), x, ZERO]]
    motions.extend([a + b for a, b in zip(translations, rotations)])
  motions_mod = [[field_mod(x, phi) for x in row] for row in motions]
  require(all(sum(c * motions_mod[j][a] for j, c in row.items()) % P == 0
              for row in jacobian for a in range(6)), "Euclidean infinitesimal motions do not preserve source constraints")
  gauges = data["gauges"]
  require(len(gauges) == len(set(gauges)) == 6 and all(type(i) is int and 0 <= i < 180 for i in gauges), "Invalid vertex-coordinate gauge")
  gauge_determinant = determinant([motions[i][:] for i in gauges])
  require(gauge_determinant != ZERO and field_mod(gauge_determinant, phi) != 0, "Gauge is not transverse")
  for i in gauges:
    jacobian.append({i: 1})
    quadratic.append([])
  kernel, dual, left, correction = (data[k] for k in ["kernel", "range_dual", "left_nullspace", "second_order_correction"])
  for matrix, rows, columns, label in [(kernel, 276, 4, "K"), (dual, 272, 276, "range dual"),
                                      (left, 4, 276, "left nullspace"), (correction, 276, 10, "W2")]:
    shape(matrix, rows, columns, label)
  pivots, free = data["pivot_columns"], data["free_columns"]
  require(len(pivots) == 272 and len(free) == 4 and sorted(pivots + free) == list(range(276)), "Invalid pivot/free partition")
  require([kernel[i] for i in free] == [[int(a == b) for b in range(4)] for a in range(4)], "K free block is not identity")
  require(all(sum(c * kernel[j][a] for j, c in row.items()) % P == 0
              for row in jacobian for a in range(4)), "J*K is nonzero")
  for i, coefficients in enumerate(dual):
    product = [0] * 276
    for scale, row in zip(coefficients, jacobian):
      for j, c in row.items():
        product[j] += scale * c
    require([product[j] % P for j in pivots] == [int(i == j) for j in range(272)], "Range dual is not a left inverse on pivot columns")
  require(small_rank(left) == 4, "Left nullspace lacks full row rank")
  for coefficients in left:
    product = [0] * 276
    for scale, row in zip(coefficients, jacobian):
      for j, c in row.items():
        product[j] += scale * c
    require(all(v % P == 0 for v in product), "Left-nullspace equation failed")
  require(data["rank"] == 272, "Saved rank claim differs from independently certified rank")
  print("PASS reconstructed Jacobian, exact transverse gauge, rank272, four-dimensional kernel and cokernel", flush=True)

  degree2 = list(itertools.combinations_with_replacement(range(4), 2))
  degree3 = list(itertools.combinations_with_replacement(range(4), 3))
  require(data["degree2_monomials"] == [list(x) for x in degree2] and
          data["degree3_monomials"] == [list(x) for x in degree3], "Incorrect monomial order")
  quadratic_coefficients = []
  for terms in quadratic:
    coefficients = []
    for a, b in degree2:
      value = sum(c * (kernel[i][a] * kernel[j][b] + (kernel[i][b] * kernel[j][a] if a != b else 0))
                  for i, j, c in terms)
      coefficients.append(value % P)
    quadratic_coefficients.append(coefficients)
  require(all(v == 0 for i in free for v in correction[i]), "W2 free coordinates are not zero")
  require(all((sum(c * correction[j][a] for j, c in row.items()) + quadratic_coefficients[r][a]) % P == 0
              for r, row in enumerate(jacobian) for a in range(10)), "Second-order equation J*W2+q(K) failed")
  require(all(sum(c * quadratic_coefficients[r][a] for r, c in enumerate(row)) % P == 0
              for row in left for a in range(10)), "Nonzero quadratic obstruction")
  index3 = {monomial: i for i, monomial in enumerate(degree3)}
  cubic = []
  for terms in quadratic:
    coefficients = [0] * 20
    for i, j, c in terms:
      for a in range(4):
        for b, pair in enumerate(degree2):
          coefficients[index3[tuple(sorted((a, *pair)))]] += c * (kernel[i][a] * correction[j][b] + correction[i][b] * kernel[j][a])
    cubic.append([c % P for c in coefficients])
  obstruction = [[sum(c * cubic[r][a] for r, c in enumerate(row)) % P for a in range(20)] for row in left]
  shape(data["cubic_obstruction"], 4, 20, "cubic obstruction")
  require(obstruction == data["cubic_obstruction"], "Cubic obstruction differs from independent source reconstruction")
  print("PASS all40 quadratic obstruction coefficients, W2 equations, and all80 cubic coefficients", flush=True)
  return obstruction, degree3, {"gauge_coordinate_indices": gauges,
    "gauge_determinant_Qphi": [str(gauge_determinant[0] - gauge_determinant[1]), str(2 * gauge_determinant[1])],
    "gauge_determinant_mod_p": field_mod(gauge_determinant, phi), "jacobian_rank": 272,
    "kernel_dimension": 4, "left_nullspace_dimension": 4, "quadratic_obstruction_coefficients_zero": 40,
    "cubic_coefficients_reconstructed": 80}


def verify_identities(cubics, monomials):
  data = json.loads((ROOT / "pure-power-certificate.json").read_text())
  require(data["prime"] == P and data["target_power"] == 9, "Incorrect identity field/degree")
  multipliers = [tuple(m) for m in data["multiplier_monomials"]]
  expected = {(a, b, c, 6 - a - b - c) for a in range(7) for b in range(7 - a) for c in range(7 - a - b)}
  require(len(multipliers) == 84 and set(multipliers) == expected, "Incomplete degree-six multipliers")
  coefficients = data["coefficients"]
  require(len(coefficients) == 4, "Expected four generator coefficient blocks")
  for block in coefficients:
    shape(block, 84, 4, "identity coefficient")
  exponents = [tuple(m.count(i) for i in range(4)) for m in monomials]
  for target in range(4):
    result = {}
    for generator in range(4):
      for multiplier, row in zip(multipliers, coefficients[generator]):
        for power, value in zip(exponents, cubics[generator]):
          exponent = tuple(a + b for a, b in zip(power, multiplier))
          result[exponent] = (result.get(exponent, 0) + row[target] * value) % P
    result = {k: v for k, v in result.items() if v}
    require(result == {tuple(9 if i == target else 0 for i in range(4)): 1}, "Pure-power identity failed")
    print(f"PASS direct original-cubic identity t{target}^9", flush=True)
  source = (ROOT / "cubic-obstruction.sing").read_text().split("ideal I=", 1)[1].split(";", 1)[0]
  forms = source.split(",")
  require(len(forms) == 4, "Expected four displayed cubic forms")
  for form, saved in zip(forms, cubics):
    parsed = {}
    for term in form.strip().split("+"):
      coefficient, *variables = term.split("*")
      require(len(variables) == 3 and all(v in ("t0", "t1", "t2", "t3") for v in variables), "Invalid cubic term")
      key = tuple(variables.count(f"t{i}") for i in range(4))
      parsed[key] = (parsed.get(key, 0) + int(coefficient)) % P
    require({k: v for k, v in parsed.items() if v} == {k: v for k, v in zip(exponents, saved) if v}, "Displayed Singular source does not match reconstructed cubics")


def main():
  started = time.monotonic()
  data = json.loads((ROOT / "modular-obstruction.json").read_text())
  vertices, normals, facets, edges, geometry = verify_geometry(data)
  cubics, monomials, linear = verify_modular(data, vertices, normals, facets, edges)
  verify_identities(cubics, monomials)
  names = ["modular-obstruction.json", "pure-power-certificate.json", "cubic-obstruction.sing", "independent_verification.py"]
  result = {"verification": "PASS", "arithmetic": "Exact Q(sqrt5) geometry and F1009 arithmetic; standard library only",
    "geometry": geometry, "linear_and_obstruction": linear, "direct_power_identities": 4,
    "source_hashes": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names},
    "elapsed_seconds": round(time.monotonic() - started, 3),
    "scope": "Source reconstruction and certificate arithmetic. Local-rigidity and characteristic-zero transfer are separate written deductions, not formalized here."}
  (ROOT / "independent_verification.json").write_text(json.dumps(result, indent=2) + "\n")
  print(f"ALL INDEPENDENT CHECKS PASSED in {result['elapsed_seconds']}s", flush=True)


if __name__ == "__main__":
  main()
