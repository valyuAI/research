"""Second, independent check of the two examples using SymPy.

This implementation does not use the reduction formulas of verify_examples.py. It
  * rebuilds the mass-action equations from a plain-text reaction list,
  * computes a lexicographic Groebner basis of the steady-state ideal, saturated by
    the product of the concentrations (so boundary components are removed),
  * solves it to list every complex steady state off the coordinate hyperplanes,
  * keeps the positive real ones and checks that all share the same x_A (ACR),
  * certifies stability with exact cubic Routh-Hurwitz inequalities and
    instability with a negative constant coefficient (a positive real root).

Run: python3 independent_check.py   (needs sympy)
"""

import sympy as sp

if not __debug__:
    raise SystemExit("FAIL: verification requires Python assertions enabled")

a, b, c, t = sp.symbols("a b c t")
X = (a, b, c)

NETWORKS = {
    "example_1": """
        A+B -> 2B : 2
        B -> 0 : 2
        0 -> A+C : 60
        2C -> A+C : 1
        A+C -> 2C : 13
        B+C -> B : 2
    """,
    "example_2": """
        C -> A+C : 1
        A+C -> C : 1
        A -> A+C : 6
        B -> 2B : 11
        2B -> B : 1
        B+C -> B : 1
        B+C -> C : 6
        C -> B+C : 6
    """,
}


def parse_complex(text):
    vec = [0, 0, 0]
    text = text.strip()
    if text == "0":
        return vec
    for term in text.split("+"):
        term = term.strip()
        coef = int(term[:-1]) if len(term) > 1 else 1
        vec["ABC".index(term[-1])] += coef
    return vec


def equations(spec):
    f = [sp.Integer(0)] * 3
    reactions = []
    for line in spec.strip().splitlines():
        lhs, rest = line.split("->")
        rhs, k = rest.split(":")
        y, yp, k = parse_complex(lhs), parse_complex(rhs), sp.Rational(k.strip())
        assert k > 0, "rate constants must be positive"
        assert sum(y) <= 2 and sum(yp) <= 2
        reactions.append((y, yp))
        mono = k * a ** y[0] * b ** y[1] * c ** y[2]
        for i in range(3):
            f[i] += (yp[i] - y[i]) * mono
    return [sp.expand(fi) for fi in f], reactions


def positive_steady_states(f):
    # saturate by a*b*c: add 1 - t*a*b*c and eliminate t
    G = sp.groebner(list(f) + [1 - t * a * b * c], t, c, b, a, order="lex")
    gens = [g for g in G.exprs if not g.has(t)]
    sols = sp.solve(gens, [c, b, a], dict=True)
    pos = []
    for s in sols:
        vals = [sp.simplify(s[v]) for v in (a, b, c)]
        assert all(v.is_real is not None for v in vals), "undecided reality"
        assert all(
            v.is_positive is not None for v in vals if v.is_real
        ), "undecided sign"
        if all(v.is_real and v.is_positive for v in vals):
            pos.append(tuple(vals))
    return sorted(pos), len(sols)


def exact_stability(cp):
    """Certify the two cases needed here; refuse an undecided polynomial."""
    coeffs = cp.all_coeffs()
    assert len(coeffs) == 4 and coeffs[0] == 1
    c1, c2, c3 = coeffs[1:]
    if c1 > 0 and c2 > 0 and c3 > 0 and c1 * c2 > c3:
        return True
    assert (
        c3 < 0
    ), "neither a strict Hurwitz certificate nor a positive-root certificate"
    return False


def main():
    for name, spec in NETWORKS.items():
        f, reactions = equations(spec)
        M = sp.Matrix([[yp[i] - y[i] for i in range(3)] for y, yp in reactions])
        complexes = {tuple(v) for pair in reactions for v in pair}
        reactants = {tuple(y) for y, _ in reactions}
        print(
            f"{name}: dimension {M.rank()}, {len(reactions)} reactions, "
            f"{len(complexes)} complexes, {len(reactants)} reactant complexes"
        )
        pos, nsol = positive_steady_states(f)
        print(
            f"  {nsol} steady states off the coordinate hyperplanes, {len(pos)} positive: {pos}"
        )
        expected = {
            "example_1": (6, 7, 6, [(1, 10, 5), (1, 12, 4), (1, 15, 3)]),
            "example_2": (8, 6, 6, [(1, 2, 3), (1, 3, 2), (1, 6, 1)]),
        }[name]
        assert (M.rank(), len(reactions), len(complexes), len(reactants)) == (
            3,
            *expected[:3],
        )
        assert nsol == 3 and pos == expected[3], "steady-state list or ACR fails"
        J = sp.Matrix(f).jacobian(X)
        stable = []
        for p in pos:
            Jp = J.subs(dict(zip(X, p)))
            lam = sp.symbols("lam")
            cp = sp.Poly((lam * sp.eye(3) - Jp).det(), lam)
            st = exact_stability(cp)
            stable.append(st)
            print(
                f"  {p}: charpoly {cp.all_coeffs()}, exact certificate = {'Hurwitz stable' if st else 'positive real eigenvalue'}"
            )
        assert stable == [True, False, True], "stability pattern fails"
    remark_two_species()
    four_reactant_cross_check()
    print("INDEPENDENT CHECK PASSED")


def remark_two_species():
    """Remark rem:union: competition network plus a decoupled 0 <-> Z; all positive steady states."""
    x, y, z, u = sp.symbols("x y z u")
    eps = sp.Rational(6, 49)
    # 0 -> X, 0 -> Y (eps); X <-> 2X, Y <-> 2Y (1, 1); X+Y -> X, X+Y -> Y (2, 2); 0 <-> Z (1, 1)
    fx = eps + x - x**2 - 2 * x * y
    fy = eps + y - y**2 - 2 * x * y
    fz = 1 - z
    G = sp.groebner([fx, fy, fz, 1 - u * x * y * z], u, z, y, x, order="lex")
    sols = sp.solve([g for g in G.exprs if not g.has(u)], [x, y, z], dict=True)
    pos = sorted(
        (
            tuple(s[v] for v in (x, y, z))
            for s in sols
            if all(s[v].is_real and s[v] > 0 for v in (x, y, z))
        ),
    )
    J = sp.Matrix([fx, fy, fz]).jacobian([x, y, z])
    pattern = []
    for pnt in pos:
        Jp = J.subs(dict(zip((x, y, z), pnt)))
        stable = exact_stability(Jp.charpoly().as_poly())
        pattern.append(stable)
        print(
            f"  decoupled example: steady state {pnt}, exact certificate = {'Hurwitz stable' if stable else 'positive real eigenvalue'}"
        )
    assert pos == [
        (sp.Rational(1, 7), sp.Rational(6, 7), 1),
        (sp.Rational(3, 7), sp.Rational(3, 7), 1),
        (sp.Rational(6, 7), sp.Rational(1, 7), 1),
    ], "decoupled steady-state list fails"
    assert [p[2] for p in pos] == [1, 1, 1], "ACR in Z fails"
    assert pattern == [True, False, True], pattern


def four_reactant_cross_check():
    """Proposition prop:four: redo the exponent enumeration with SymPy nullspaces."""
    from itertools import combinations, combinations_with_replacement

    n = 4
    cpx = [tuple([0] * n)]
    for k in (1, 2):
        for idx in combinations_with_replacement(range(n), k):
            v = [0] * n
            for i in idx:
                v[i] += 1
            cpx.append(tuple(v))
    assert len(cpx) == 15
    worst, sets = 0, 0
    for ys in combinations(cpx, 4):
        M = sp.Matrix([[ys[j][i] - ys[3][i] for i in range(n)] for j in range(3)])
        ns = M.nullspace()
        if len(ns) != 1:
            continue
        b = list(ns[0])
        if 0 in b:
            sets += 1
            worst = max(worst, len(set(b)))
    print(
        f"  four-reactant cross-check: {sets} rank-3 sets with a zero exponent, max distinct exponents {worst}"
    )
    assert (sets, worst) == (922, 3)


if __name__ == "__main__":
    main()
