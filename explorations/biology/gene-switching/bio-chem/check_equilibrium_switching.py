"""Exact audit of a reversible concentration-dependent switching model.

Run with Python 3 and SymPy 1.14.0. This is exploratory verification, not a
claim of priority or a fit to experimental data. No external data are needed.
"""

import json
import math
from pathlib import Path

import sympy as sp


def inverse_dwell_affine_witness(concentrations, mean_intervals):
    """Exact feasibility of nonnegative affine inverse means in given boxes.

    Feasibility is necessary, not sufficient, for a singleton macrostate.
    Inputs are exact positive concentrations and positive dwell intervals.
    """
    if not concentrations or len(concentrations) != len(mean_intervals):
        raise ValueError("Require matching nonempty concentrations and intervals")
    data = []
    for concentration, (lower, upper) in zip(concentrations, mean_intervals):
        concentration, lower, upper = map(sp.Rational, (concentration, lower, upper))
        if not (concentration > 0 and 0 < lower <= upper):
            raise ValueError(
                "Require positive concentrations and ordered positive intervals"
            )
        data.append((concentration, 1 / upper, 1 / lower))

    # Eliminate the intercept: every lower bound must be below every upper.
    slope_lower = sp.Integer(0)
    slope_upper = min(upper / concentration for concentration, _, upper in data)
    for ci, lower, _ in data:
        for cj, _, upper in data:
            coefficient = cj - ci
            rhs = upper - lower
            if coefficient > 0:
                slope_upper = min(slope_upper, rhs / coefficient)
            elif coefficient < 0:
                slope_lower = max(slope_lower, rhs / coefficient)
            elif rhs < 0:
                return None
    if slope_lower > slope_upper:
        return None
    slope = slope_lower
    intercept = max([sp.Integer(0)] + [lower - slope * c for c, lower, _ in data])
    if any(not lower <= intercept + slope * c <= upper for c, lower, upper in data):
        raise ArithmeticError("Internal affine-feasibility inconsistency")
    return intercept, slope


def main():
    b, k, c, s = sp.symbols("b k c s", positive=True)
    q = sp.Matrix(
        [
            [-b * c, b * c, 0, 0],
            [b, -b - k, k, 0],
            [0, k, -k - b * c, b * c],
            [0, 0, b, -b],
        ]
    )
    pi = sp.Matrix([[1, c, c, c**2]]) / (1 + c) ** 2
    checks = []

    def equal(name, actual, expected):
        residual = sp.simplify(actual - expected)
        if isinstance(residual, sp.MatrixBase):
            passed = residual == sp.zeros(*residual.shape)
        else:
            passed = residual == 0
        if not passed:
            raise AssertionError((name, residual))
        checks.append(name)
        print(f"PASS {name}", flush=True)

    equal("generator row sums", q * sp.ones(4, 1), sp.zeros(4, 1))
    equal("stationary normalization", sum(pi), 1)
    equal("stationarity", pi * q, sp.zeros(1, 4))
    equal("detailed balance", sp.diag(*pi) * q, q.T * sp.diag(*pi))

    f = sp.Matrix([0, 0, 1, 1])
    p = (pi * f)[0]
    equal("ON probability", p, c / (1 + c))
    flux = pi[1] * q[1, 2]
    equal("OFF to ON flux", flux, k * c / (1 + c) ** 2)
    equal("switching timescale from mean dwells", p * (1 - p) / flux, 1 / k)

    dwell_results = {}
    for label, sub, entry, mean, cv in [
        (
            "OFF",
            q[:2, :2],
            1,
            (1 + c) / (k * c),
            1 + 2 * k / (b * (1 + c) ** 2),
        ),
        (
            "ON",
            q[2:, 2:],
            0,
            (1 + c) / k,
            1 + 2 * k * c / (b * (1 + c) ** 2),
        ),
    ]:
        first = -sub.inv() * sp.ones(2, 1)
        second = 2 * sub.inv() ** 2 * sp.ones(2, 1)
        equal(f"{label} dwell mean", first[entry], mean)
        equal(f"{label} dwell squared CV", second[entry] / mean**2 - 1, cv)
        dwell_results[label] = {"mean": str(mean), "cv_squared": str(cv)}

    g = f - p * sp.ones(4, 1)
    variance = p * (1 - p)
    a = b * (1 + c)
    equal("centered observable generator image", q * g, sp.Matrix([0, k, -k, 0]))
    equal(
        "two-dimensional invariant subspace",
        (q**2 + (a + 2 * k) * q + a * k * sp.eye(4)) * g,
        sp.zeros(4, 1),
    )
    equal(
        "initial normalized covariance derivative",
        (g.T * sp.diag(*pi) * q * g)[0] / variance,
        -k,
    )
    resolvent = (s * sp.eye(4) - q).inv()
    transform = sp.factor((g.T * sp.diag(*pi) * resolvent * g)[0] / variance)
    expected_transform = (s + a + k) / (s**2 + (a + 2 * k) * s + a * k)
    equal("normalized covariance Laplace transform", transform, expected_transform)
    equal("integrated covariance time", transform.subs(s, 0), 1 / k + 1 / a)

    discriminant = sp.sqrt(a**2 + 4 * k**2)
    slow = (a + 2 * k - discriminant) / 2
    fast = (a + 2 * k + discriminant) / 2
    slow_weight = (1 + a / discriminant) / 2
    mixture = slow_weight / (s + slow) + (1 - slow_weight) / (s + fast)
    equal("two positive exponential covariance components", mixture, transform)

    occupancy = (pi * sp.Matrix([0, 1, 1, 2]))[0]
    association_flux = pi[0] * q[0, 1] + pi[2] * q[2, 3]
    equal("mean bound ligand count", occupancy, 2 * c / (1 + c))
    equal("association-event flux", association_flux, b * c / (1 + c))
    equal(
        "mean residence by occupancy over arrival flux",
        occupancy / association_flux,
        2 / b,
    )

    # Sharpness of the four-concentration, exact-data state-count certificate.
    three_q = sp.Matrix([[-13 * c, 13 * c, 0], [13, -13 - c, c], [0, 1, -1]])
    three_pi = sp.Matrix([[1, c, c**2]]) / (1 + c + c**2)
    equal("three-state witness stationarity", three_pi * three_q, sp.zeros(1, 3))
    equal(
        "three-state witness detailed balance",
        sp.diag(*three_pi) * three_q,
        three_q.T * sp.diag(*three_pi),
    )
    three_p = three_pi[1]
    three_td = sp.factor((1 - three_p) / (13 + c))
    equal(
        "three-state equal-time factorization",
        three_td - sp.Rational(1, 21),
        -(c - 1) * (c - 2) * (c - 4) / (21 * (c + 13) * (c**2 + c + 1)),
    )
    equal(
        "three-state equal times at distinct concentrations",
        sp.Matrix([three_td.subs(c, value) for value in [1, 2, 4]]),
        sp.ones(3, 1) / 21,
    )
    equal(
        "three-state distinct activities at equal-time points",
        sp.Matrix([three_p.subs(c, value) for value in [1, 2, 4]]),
        sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 7), sp.Rational(4, 21)]),
    )

    epsilon = sp.symbols("epsilon", nonnegative=True)
    off_rates = [sp.Rational(1, 2), sp.Rational(2, 3), sp.Rational(4, 5)]
    contrast_upper = (2 * off_rates[0] + off_rates[2]) / (1 - epsilon)
    contrast_upper -= 3 * off_rates[1] / (1 + epsilon)
    equal(
        "OFF inverse-mean affine contrast interval margin",
        contrast_upper,
        (-1 + 19 * epsilon) / (5 * (1 - epsilon**2)),
    )
    on_endpoint_gap = sp.Rational(1, 2) / (1 + epsilon)
    on_endpoint_gap -= sp.Rational(1, 5) / (1 - epsilon)
    equal(
        "ON inverse-mean monotonicity interval margin",
        on_endpoint_gap,
        (3 - 7 * epsilon) / (10 * (1 - epsilon**2)),
    )
    concentrations = [1, 2, 4]
    mean_targets = {
        "ON": [sp.Integer(2), sp.Integer(3), sp.Integer(5)],
        "OFF": [sp.Integer(2), sp.Rational(3, 2), sp.Rational(5, 4)],
    }
    for label, means in mean_targets.items():
        intervals = [
            (mean * sp.Rational(19, 20), mean * sp.Rational(21, 20)) for mean in means
        ]
        equal(
            f"{label} singleton infeasible for five-percent dwell intervals",
            int(inverse_dwell_affine_witness(concentrations, intervals) is None),
            1,
        )
    off_threshold_intervals = [
        (mean * sp.Rational(18, 19), mean * sp.Rational(20, 19))
        for mean in mean_targets["OFF"]
    ]
    off_witness = inverse_dwell_affine_witness(concentrations, off_threshold_intervals)
    equal(
        "OFF affine-line feasibility at sharp interval threshold",
        sp.Matrix(off_witness),
        sp.Matrix([sp.Rational(19, 45), sp.Rational(19, 180)]),
    )
    on_threshold_intervals = [
        (mean * sp.Rational(4, 7), mean * sp.Rational(10, 7))
        for mean in mean_targets["ON"]
    ]
    on_witness = inverse_dwell_affine_witness(concentrations, on_threshold_intervals)
    equal(
        "ON affine-line feasibility at monotonicity threshold",
        sp.Matrix(on_witness),
        sp.Matrix([sp.Rational(7, 20), 0]),
    )

    # Check the derived time-uniform bound against the exact spectral formula.
    # This finite check supplements the analytic inequalities in the note.
    max_ratio = 0.0
    sample_count = 0
    for epsilon in [0.5, 0.1, 0.01, 0.001]:
        bound = epsilon / (math.e * (1 - epsilon))
        for concentration in [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]:
            rate = (1 + concentration) / epsilon
            root = math.sqrt(rate**2 + 4)
            # Rationalized expressions avoid cancellation when rate is large.
            slow_rate = 1 - 2 / (root + rate)
            fast_rate = (rate + 2 + root) / 2
            fast_weight = 2 / (root * (root + rate))
            for time in [0.0] + [10 ** (i / 10) for i in range(-60, 31)]:
                covariance = (1 - fast_weight) * math.exp(-slow_rate * time)
                covariance += fast_weight * math.exp(-fast_rate * time)
                error = abs(covariance - math.exp(-time))
                if error > bound + 1e-13:
                    raise AssertionError((epsilon, concentration, time, error, bound))
                max_ratio = max(max_ratio, error / bound)
                sample_count += 1
    print(f"PASS covariance bound grid: {sample_count} samples", flush=True)

    result = {
        "sympy_version": sp.__version__,
        "symbolic_checks": checks,
        "symbolic_check_count": len(checks),
        "dwell_results": dwell_results,
        "dwell_interval_screen": {
            "concentrations": concentrations,
            "mean_targets_k_equals_one": {
                label: list(map(str, means)) for label, means in mean_targets.items()
            },
            "relative_halfwidth_excluding_both_singletons": "epsilon < 1/19",
            "OFF_boundary_affine_witness_intercept_slope": list(map(str, off_witness)),
            "scope": "Deterministic intervals centered on target means; known concentrations. This is a necessary singleton screen, not a statistical confidence procedure or a complete three-state feasibility test.",
        },
        "covariance_laplace_transform": str(transform),
        "uniform_bound_grid_samples": sample_count,
        "largest_error_to_bound_ratio_on_grid": max_ratio,
        "scope": "Mathematical witness checked; source supplement and novelty audit incomplete.",
    }
    output = Path(__file__).with_name("equilibrium_switching_checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {output.name}", flush=True)


if __name__ == "__main__":
    main()
