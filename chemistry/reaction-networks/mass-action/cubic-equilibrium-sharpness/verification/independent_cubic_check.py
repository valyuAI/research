"""Replay actual mass-action equilibria using only rational standard-library arithmetic."""

import copy
from fractions import Fraction as Q
import json
from math import prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def determinant(matrix):
    matrix = [[Q(x) for x in row] for row in matrix]
    size = len(matrix)
    result = Q(1)
    for column in range(size):
        pivot = next((i for i in range(column, size) if matrix[i][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        value = matrix[column][column]
        result *= value
        for i in range(column + 1, size):
            factor = matrix[i][column] / value
            for j in range(column + 1, size):
                matrix[i][j] -= factor * matrix[column][j]
            matrix[i][column] = 0
    return result


def validate_case(case):
    n = case["n"]
    source = [[int(x) for x in row] for row in case["source_rows"]]
    product = [[int(x) for x in row] for row in case["product_rows"]]
    require(len(source) == len(product) == n, "Wrong reaction count")
    require(all(len(row) == n for row in source + product), "Wrong species count")
    require(
        all(x >= 0 for row in source + product for x in row), "Negative complex entry"
    )
    require(max(map(sum, source)) == 3, "Sources are not cubic")
    require(max(map(sum, product)) <= 2 * n, "Product degree exceeds the stated bound")
    gamma = [[product[i][j] - source[i][j] for i in range(n)] for j in range(n)]
    recorded_columns = [[int(x) for x in row] for row in case["stoichiometric_columns"]]
    require(list(map(list, zip(*gamma))) == recorded_columns, "Stoichiometry mismatch")
    rates = list(map(Q, case["rate_constants"]))
    z = list(map(Q, case["conservation_vector"]))
    level = Q(case["class_level"])
    require(
        len(rates) == len(z) == n and all(k > 0 for k in rates),
        "Invalid rates or conservation vector",
    )
    require(
        any(v > 0 for v in z) and any(v < 0 for v in z),
        "Expected mixed-sign conservation",
    )
    require(
        all(sum(z[j] * gamma[j][i] for j in range(n)) == 0 for i in range(n)),
        "Conservation fails",
    )
    require(all(sum(row) == 0 for row in gamma), "Positive flux kernel fails")
    require(
        determinant([row[: n - 1] for row in gamma[: n - 1]]) != 0,
        "Stoichiometric rank is too small",
    )
    seen = set()
    equilibria = case["equilibria"]
    require(len(equilibria) == n, "Wrong number of equilibria")
    for equilibrium in equilibria:
        x = tuple(map(Q, equilibrium["concentrations"]))
        require(
            len(x) == n and all(value > 0 for value in x), "Equilibrium is not positive"
        )
        require(x not in seen, "Duplicate equilibrium")
        seen.add(x)
        require(
            sum(a * b for a, b in zip(z, x)) == level, "Equilibrium is on another class"
        )
        flux = [
            rates[i] * prod(x[j] ** source[i][j] for j in range(n)) for i in range(n)
        ]
        require(
            all(sum(gamma[j][i] * flux[i] for i in range(n)) == 0 for j in range(n)),
            "Vector field is nonzero",
        )
        # Differentiate the supplied monomials directly, independently of the
        # generator's matrix/Jacobian and equilibrium-curve calculations.
        jacobian = [
            [
                sum(
                    gamma[row][i]
                    * rates[i]
                    * source[i][column]
                    * prod(x[j] ** (source[i][j] - (j == column)) for j in range(n))
                    for i in range(n)
                )
                for column in range(n)
            ]
            for row in range(n)
        ]
        # The first n-1 field components are independent coordinates on im Gamma;
        # adding the conservation equation tests transversality to the class.
        require(
            determinant(jacobian[: n - 1] + [z]) != 0,
            "Degenerate constrained equilibrium",
        )
    return n


if __name__ == "__main__":
    path = Path(__file__).with_name("cubic-sharpness-certificate.json")
    certificate = json.loads(path.read_text())
    require(
        [case["n"] for case in certificate["cases"]] == list(range(2, 9)),
        "Unexpected case inventory",
    )
    total = 0
    for case in certificate["cases"]:
        total += validate_case(case)
        print(f"PASS independent direct-equation replay n={case['n']}", flush=True)
    for kind in ("product", "point", "rate"):
        changed = copy.deepcopy(certificate["cases"][1])
        if kind == "product":
            changed["product_rows"][0][0] = str(int(changed["product_rows"][0][0]) + 1)
        elif kind == "point":
            changed["equilibria"][0]["concentrations"][0] = str(
                Q(changed["equilibria"][0]["concentrations"][0]) + 1
            )
        else:
            changed["rate_constants"][0] = str(2 * Q(changed["rate_constants"][0]))
        try:
            validate_case(changed)
        except ValueError:
            print(f"PASS rejected corrupted {kind}", flush=True)
        else:
            raise ValueError(f"Corrupted {kind} was accepted")
    print(
        f"PASS {total} positive nondegenerate equilibria; finite checks only",
        flush=True,
    )
