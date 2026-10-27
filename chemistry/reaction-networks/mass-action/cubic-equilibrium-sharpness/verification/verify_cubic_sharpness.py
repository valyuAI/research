"""Exact finite checks of the cubic-source family, independent of the old family."""

import hashlib
import json
from pathlib import Path
import time

import sympy as sp

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows(matrix):
    return [[str(value) for value in row] for row in matrix.tolist()]


def check(n):
    identity = sp.eye(n)
    source = 2 * identity
    for i in range(n - 1):
        source[i, i + 1] = 1
    degree = 2**n
    powers = sp.Matrix(
        [
            sp.Rational(degree + (-1) ** (n - i) * 2 ** (i - 1), 3)
            for i in range(1, n + 1)
        ]
    )
    require(all(p.is_Integer and p > 0 for p in powers), "Invalid exponent")
    require(len(set(powers)) == n, "Repeated exponent")
    require(source * powers == degree * sp.ones(n, 1), "Weighted degrees differ")
    require(source.det() == degree, "Singular source matrix")
    interpolation = sp.Matrix(
        [
            [1] + [sp.Integer(root) ** power for power in powers]
            for root in range(1, n + 1)
        ]
    )
    kernel = interpolation.nullspace()
    require(len(kernel) == 1, "Wrong interpolation rank")
    coefficients = kernel[0]
    denominator = sp.ilcm(*[value.q for value in coefficients])
    coefficients *= denominator
    divisor = sp.igcd(*[int(value) for value in coefficients])
    coefficients /= divisor
    require(all(value != 0 for value in coefficients), "Missing coefficient")
    ordered = sorted(zip([0] + list(powers), list(coefficients)))
    require(
        all(a[1] * b[1] < 0 for a, b in zip(ordered, ordered[1:])),
        "Coefficients do not alternate in exponent order",
    )
    c = sp.Matrix([abs(value) for value in coefficients[1:]])
    z = sp.Matrix([sp.sign(value) for value in coefficients[1:]])
    require(set(z) == {-1, 1}, "Conservation law is not mixed-sign")
    columns = [
        -identity[:, i] + z[i] * z[i + 1] * identity[:, i + 1] for i in range(n - 1)
    ]
    columns.append(-sum(columns, sp.zeros(n, 1)))
    gamma = sp.Matrix.hstack(*columns)
    product = source + gamma.T
    require(all(value >= 0 for value in source), "Invalid source complex")
    require(all(value >= 0 for value in product), "Invalid product complex")
    require(max(map(sum, source.tolist())) == 3, "Sources are not cubic")
    require(max(map(sum, product.tolist())) <= 2 * n, "Product bound fails")
    require(gamma.rank() == n - 1, "Wrong stoichiometric rank")
    require(gamma * sp.ones(n, 1) == sp.zeros(n, 1), "Flux kernel mismatch")
    require(z.T * gamma == sp.zeros(1, n), "Conservation law fails")
    rates = [sp.prod(c[j] ** (-source[i, j]) for j in range(n)) for i in range(n)]
    require(all(rate.is_Rational and rate > 0 for rate in rates), "Invalid rates")
    basis = gamma[:, : n - 1]
    pivot_rows = list(basis.T.rref()[1])
    basis_inverse = basis[pivot_rows, :].inv()
    level = -coefficients[0]
    equilibria = []
    for root in range(1, n + 1):
        t = sp.Integer(root)
        x = sp.Matrix([c[i] * t ** powers[i] for i in range(n)])
        flux = sp.Matrix(
            [
                rates[i] * sp.prod(x[j] ** source[i, j] for j in range(n))
                for i in range(n)
            ]
        )
        require(flux == t**degree * sp.ones(n, 1), "Unequal positive fluxes")
        require(gamma * flux == sp.zeros(n, 1), "Not an equilibrium")
        require((z.T * x)[0] == level, "Wrong stoichiometric class")
        tangent = sp.Matrix([c[i] * powers[i] * t ** (powers[i] - 1) for i in range(n)])
        derivative = (z.T * tangent)[0]
        require(derivative != 0, "Multiple prescribed root")
        jacobian = (
            gamma * sp.diag(*flux) * source * sp.diag(*[1 / value for value in x])
        )
        require(jacobian * tangent == sp.zeros(n, 1), "Wrong kernel tangent")
        restricted = basis_inverse * jacobian[pivot_rows, :] * basis
        require(basis * restricted == jacobian * basis, "Wrong Jacobian restriction")
        determinant = restricted.det(method="domain-ge")
        require(determinant != 0, "Degenerate equilibrium")
        equilibria.append(
            {
                "parameter": root,
                "concentrations": [str(value) for value in x],
                "polynomial_derivative": str(derivative),
                "restricted_jacobian_determinant": str(determinant),
            }
        )
    return {
        "n": n,
        "powers": list(map(int, powers)),
        "polynomial_coefficients_constant_then_species_order": list(
            map(str, coefficients)
        ),
        "source_rows": rows(source),
        "product_rows": rows(product),
        "stoichiometric_columns": rows(gamma.T),
        "conservation_vector": list(map(int, z)),
        "class_level": str(level),
        "rate_constants": list(map(str, rates)),
        "maximum_source_molecularity": 3,
        "maximum_product_molecularity": int(max(map(sum, product.tolist()))),
        "equilibria": equilibria,
    }


def main():
    started = time.monotonic()
    cases = []
    for n in range(2, 9):
        print(f"Checking cubic-source family n={n}", flush=True)
        case = check(n)
        cases.append(case)
        print(
            f"PASS n={n}: {n} exact nondegenerate equilibria, powers={case['powers']}",
            flush=True,
        )
    result = {
        "status": "PASS",
        "scope": "Exact finite validation, not a substitute for the all-n proof",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version": sp.__version__,
        "elapsed_seconds": time.monotonic() - started,
        "cases": cases,
    }
    (ROOT / "cubic-sharpness-certificate.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(f"All 35 equilibria PASS in {result['elapsed_seconds']:.2f}s", flush=True)


if __name__ == "__main__":
    main()
