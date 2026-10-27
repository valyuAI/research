"""Exact replay of the ACR plus bistability examples with standard-library rational arithmetic.

For each network the script
  1. builds the mass-action vector field from the listed reactions,
  2. checks the factorisation that forces absolute concentration robustness (ACR),
  3. checks that the network is at most bimolecular and computes its dimension,
     complexes and reactant complexes,
  4. reduces the positive steady states to an explicit univariate polynomial and
     checks that its positive roots are exactly the listed points,
  5. evaluates the Jacobian exactly and applies the Routh-Hurwitz test.

Run: python3 verify_examples.py   (writes examples-certificate.json next to this file)
"""

import json
from fractions import Fraction as Q
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


# ---------------------------------------------------------------- polynomials
# A polynomial in the species concentrations is a dict {exponent tuple: Fraction}.


def padd(p, q, scale=Q(1)):
    out = dict(p)
    for mon, c in q.items():
        out[mon] = out.get(mon, Q(0)) + scale * c
        if out[mon] == 0:
            del out[mon]
    return out


def pmul(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            mon = tuple(a + b for a, b in zip(m1, m2))
            out[mon] = out.get(mon, Q(0)) + c1 * c2
            if out[mon] == 0:
                del out[mon]
    return out


def peval(p, x):
    total = Q(0)
    for mon, c in p.items():
        term = c
        for xi, e in zip(x, mon):
            term *= xi**e
        total += term
    return total


def pdiff(p, j):
    out = {}
    for mon, c in p.items():
        if mon[j] == 0:
            continue
        new = list(mon)
        new[j] -= 1
        out[tuple(new)] = out.get(tuple(new), Q(0)) + c * mon[j]
    return {m: c for m, c in out.items() if c != 0}


def var(n, j):
    mon = [0] * n
    mon[j] = 1
    return {tuple(mon): Q(1)}


def const(n, c):
    return {tuple([0] * n): Q(c)} if c != 0 else {}


# --------------------------------------------------------------- linear algebra


def rank(rows):
    rows = [[Q(x) for x in row] for row in rows]
    r = 0
    ncols = len(rows[0]) if rows else 0
    for col in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col] / rows[r][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def charpoly3(m):
    """Return (a1, a2, a3) with det(lambda I - m) = lambda^3 + a1 lambda^2 + a2 lambda + a3."""
    tr = m[0][0] + m[1][1] + m[2][2]
    minors = (
        (m[0][0] * m[1][1] - m[0][1] * m[1][0])
        + (m[0][0] * m[2][2] - m[0][2] * m[2][0])
        + (m[1][1] * m[2][2] - m[1][2] * m[2][1])
    )
    return -tr, minors, -det3(m)


def routh_hurwitz_stable(a1, a2, a3):
    return a1 > 0 and a3 > 0 and a1 * a2 > a3


# ---------------------------------------------------------------- networks


def mass_action(n, reactions):
    """reactions: list of (reactant tuple, product tuple, rate)."""
    f = [{} for _ in range(n)]
    for y, yp, k in reactions:
        mono = {tuple(y): Q(k)}
        for i in range(n):
            if yp[i] != y[i]:
                f[i] = padd(f[i], mono, Q(yp[i] - y[i]))
    return f


def network_data(n, reactions):
    complexes = set()
    reactants = set()
    for y, yp, _ in reactions:
        require(sum(y) <= 2 and sum(yp) <= 2, "network is not at most bimolecular")
        require(tuple(y) != tuple(yp), "trivial reaction")
        complexes.update([tuple(y), tuple(yp)])
        reactants.add(tuple(y))
    vectors = [[yp[i] - y[i] for i in range(n)] for y, yp, _ in reactions]
    dim = rank(vectors)
    return {
        "species": n,
        "reactions": len(reactions),
        "complexes": len(complexes),
        "reactant_complexes": len(reactants),
        "dimension": dim,
    }


def univariate(p, j, n):
    """Coefficient list (lowest degree first) of a polynomial that involves only x_j."""
    deg = max((mon[j] for mon in p), default=0)
    coeffs = [Q(0)] * (deg + 1)
    for mon, c in p.items():
        require(all(mon[i] == 0 for i in range(n) if i != j), "not univariate")
        coeffs[mon[j]] += c
    return coeffs


def poly_from_roots(roots, lead):
    coeffs = [Q(lead)]
    for r in roots:
        new = [Q(0)] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i + 1] += c
            new[i] -= r * c
        coeffs = new
    return coeffs


def jacobian(f, x):
    n = len(f)
    return [[peval(pdiff(f[i], j), x) for j in range(n)] for i in range(n)]


# ------------------------------------------------------------ the examples
# Species order (A, B, C). Exponent vectors of complexes.
A, B, C, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)


def add(*cs):
    return tuple(sum(t) for t in zip(*cs))


EXAMPLE_1 = {
    "name": "six-reaction example (paper, Example ex:six)",
    "reactions": [
        (add(A, B), add(B, B), 2),  # A + B -> 2B
        (B, Z, 2),  # B -> 0
        (Z, add(A, C), 60),  # 0 -> A + C
        (add(C, C), add(A, C), 1),  # 2C -> A + C
        (add(A, C), add(C, C), 13),  # A + C -> 2C
        (add(B, C), B, 2),  # B + C -> B
    ],
    "acr_species": 0,
    "acr_value": 1,
    # f_B = 2 b (a - 1): checked symbolically below
    "acr_factor": {"species": 1, "cofactor": {(0, 1, 0): Q(2)}, "linear": {(1, 0, 0): Q(1), (0, 0, 0): Q(-1)}},
    "steady_states": [(1, 15, 3), (1, 12, 4), (1, 10, 5)],
    "stable": [True, False, True],
}


def check_example_1(ex):
    n = 3
    f = mass_action(n, ex["reactions"])
    data = network_data(n, ex["reactions"])
    # ACR factorisation: f_B == 2 b (a - 1)
    fac = ex["acr_factor"]
    require(
        f[fac["species"]] == pmul(fac["cofactor"], fac["linear"]),
        "ACR factorisation fails",
    )
    # every positive steady state has a = 1 (since b > 0 there).
    # Reduction at a = 1: f_A(1,b,c) = -2 b + 60 + c^2 - 13 c, linear in b with
    # coefficient -2, so b = (c^2 - 13 c + 60)/2 is forced.
    a = Q(1)
    fA = {}
    for mon, c in f[0].items():
        fA = padd(fA, {(0, mon[1], mon[2]): c * a ** mon[0]})
    require(fA.get((0, 1, 0)) == Q(-2), "f_A not of the expected form")
    require(all(m[1] == 0 for m in fA if m != (0, 1, 0)), "f_A not linear in b")
    b_of_c = {(0, 0, m[2]): -c / Q(-2) for m, c in fA.items() if m != (0, 1, 0)}
    # substitute b = b_of_c(c) into f_C(1, b, c)
    fC = {}
    for mon, c in f[2].items():
        term = {(0, 0, mon[2]): c * a ** mon[0]}
        for _ in range(mon[1]):
            term = pmul(term, b_of_c)
        fC = padd(fC, term)
    g = univariate(fC, 2, n)
    target = poly_from_roots([Q(3), Q(4), Q(5)], -1)
    require(g == target, "reduced polynomial is not -(c-3)(c-4)(c-5)")
    results = []
    for point, expect in zip(ex["steady_states"], ex["stable"]):
        x = [Q(v) for v in point]
        require(all(peval(fi, x) == 0 for fi in f), f"{point} is not a steady state")
        require(peval(b_of_c, x) == x[1], "b does not match the reduction")
        J = jacobian(f, x)
        a1, a2, a3 = charpoly3(J)
        stable = routh_hurwitz_stable(a1, a2, a3)
        require(stable == expect, f"stability mismatch at {point}")
        require(det3(J) != 0, "degenerate steady state")
        results.append(
            {
                "point": list(point),
                "charpoly": [1, str(a1), str(a2), str(a3)],
                "routh_hurwitz_stable": stable,
                "det_J": str(det3(J)),
            }
        )
    return {"network": data, "reduced_polynomial_in_c": [str(v) for v in g], "steady_states": results}


EXAMPLE_2 = {
    "name": "six-complex example (paper, Example ex:cpx)",
    "reactions": [
        (C, add(A, C), 1),  # C -> A + C
        (add(A, C), C, 1),  # A + C -> C
        (A, add(A, C), 6),  # A -> A + C
        (B, add(B, B), 11),  # B -> 2B
        (add(B, B), B, 1),  # 2B -> B
        (add(B, C), B, 1),  # B + C -> B
        (add(B, C), C, 6),  # B + C -> C
        (C, add(B, C), 6),  # C -> B + C
    ],
    "steady_states": [(1, 2, 3), (1, 3, 2), (1, 6, 1)],
    "stable": [True, False, True],
}


def check_example_2(ex):
    n = 3
    f = mass_action(n, ex["reactions"])
    data = network_data(n, ex["reactions"])
    # ACR factorisation: f_A == c (1 - a)
    require(f[0] == {(0, 0, 1): Q(1), (1, 0, 1): Q(-1)}, "ACR factorisation fails")
    # at a = 1: f_C(1, b, c) = 6 - b c, so c = 6 / b on positive steady states
    fC = {}
    for mon, c in f[2].items():
        fC = padd(fC, {(0, mon[1], mon[2]): c})
    require(fC == {(0, 0, 0): Q(6), (0, 1, 1): Q(-1)}, "f_C not of the expected form")
    # b * f_B(1, b, 6/b) as a polynomial in b
    g = {}
    for mon, c in f[1].items():
        eb, ec = mon[1], mon[2]
        # b * c_coef * b^eb * (6/b)^ec = c_coef * 6^ec * b^(1 + eb - ec)
        e = 1 + eb - ec
        require(e >= 0, "negative power")
        g = padd(g, {(0, e, 0): c * Q(6) ** ec})
    gu = univariate(g, 1, n)
    target = poly_from_roots([Q(2), Q(3), Q(6)], -1)
    require(gu == target, "reduced polynomial is not -(b-2)(b-3)(b-6)")
    results = []
    for point, expect in zip(ex["steady_states"], ex["stable"]):
        x = [Q(v) for v in point]
        require(all(peval(fi, x) == 0 for fi in f), f"{point} is not a steady state")
        J = jacobian(f, x)
        a1, a2, a3 = charpoly3(J)
        stable = routh_hurwitz_stable(a1, a2, a3)
        require(stable == expect, f"stability mismatch at {point}")
        require(det3(J) != 0, "degenerate steady state")
        results.append(
            {
                "point": list(point),
                "charpoly": [1, str(a1), str(a2), str(a3)],
                "routh_hurwitz_stable": stable,
                "det_J": str(det3(J)),
            }
        )
    return {"network": data, "reduced_polynomial_in_b_times_b": [str(v) for v in gu], "steady_states": results}


# Remark rem:union: decoupled union of a bistable two-species competition network with
# 0 <-> Z. Species order (X, Y, Z).
EPS = Q(6, 49)
X_, Y_, Z_ = (1, 0, 0), (0, 1, 0), (0, 0, 1)
REMARK = {
    "name": "decoupled three-species example (paper, Remark rem:union)",
    "reactions": [
        (Z, X_, EPS),  # 0 -> X
        (Z, Y_, EPS),  # 0 -> Y
        (X_, add(X_, X_), 1),  # X -> 2X
        (add(X_, X_), X_, 1),  # 2X -> X
        (Y_, add(Y_, Y_), 1),  # Y -> 2Y
        (add(Y_, Y_), Y_, 1),  # 2Y -> Y
        (add(X_, Y_), X_, 2),  # X + Y -> X
        (add(X_, Y_), Y_, 2),  # X + Y -> Y
        (Z, Z_, 1),  # 0 -> Z
        (Z_, Z, 1),  # Z -> 0
    ],
    "steady_states": [(Q(6, 7), Q(1, 7), Q(1)), (Q(1, 7), Q(6, 7), Q(1)), (Q(3, 7), Q(3, 7), Q(1))],
    "stable": [True, True, False],
}


def check_remark(ex):
    n = 3
    f = mass_action(n, ex["reactions"])
    data = network_data(n, ex["reactions"])
    x, y, z = var(n, 0), var(n, 1), var(n, 2)
    one = const(n, 1)
    # f_Z = 1 - z: ACR in Z with value 1
    require(f[2] == padd(one, z, Q(-1)), "f_Z is not 1 - z")
    # f_X - f_Y = (x - y)(1 - x - y): positive steady states have x = y or x + y = 1
    diff = padd(f[0], f[1], Q(-1))
    require(diff == pmul(padd(x, y, Q(-1)), padd(padd(one, x, Q(-1)), y, Q(-1))), "difference does not factor")
    # branch x = y: f_X(x, x, z) = eps + x - 3 x^2 = -3 (x - 3/7)(x + 2/21)
    br1 = {}
    for mon, c in f[0].items():
        br1 = padd(br1, {(mon[0] + mon[1], 0, 0): c})
    require(univariate(br1, 0, n) == poly_from_roots([Q(3, 7), Q(-2, 21)], -3), "branch x = y")
    # branch y = 1 - x: f_X(x, 1 - x, z) = eps - x + x^2 = (x - 6/7)(x - 1/7)
    one_minus_x = padd(one, x, Q(-1))
    br2 = {}
    for mon, c in f[0].items():
        term = {(mon[0], 0, 0): c}
        for _ in range(mon[1]):
            term = pmul(term, one_minus_x)
        br2 = padd(br2, term)
    require(univariate(br2, 0, n) == poly_from_roots([Q(6, 7), Q(1, 7)], 1), "branch x + y = 1")
    results = []
    for point, expect in zip(ex["steady_states"], ex["stable"]):
        require(all(peval(fi, point) == 0 for fi in f), f"{point} is not a steady state")
        J = jacobian(f, point)
        a1, a2, a3 = charpoly3(J)
        stable = routh_hurwitz_stable(a1, a2, a3)
        require(stable == expect, f"stability mismatch at {point}")
        require(det3(J) != 0, "degenerate steady state")
        results.append(
            {
                "point": [str(v) for v in point],
                "charpoly": [1, str(a1), str(a2), str(a3)],
                "routh_hurwitz_stable": stable,
                "det_J": str(det3(J)),
            }
        )
    return {"network": data, "steady_states": results}


def main():
    cert = {
        "example_1": check_example_1(EXAMPLE_1),
        "example_2": check_example_2(EXAMPLE_2),
        "remark_decoupled": check_remark(REMARK),
    }
    out = Path(__file__).with_name("examples-certificate.json")
    out.write_text(json.dumps(cert, indent=2) + "\n")
    print(json.dumps(cert, indent=2))
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
