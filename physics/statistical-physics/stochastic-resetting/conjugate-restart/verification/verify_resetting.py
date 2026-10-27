"""Exact finite-chain certificates and independent Brownian integral checks."""

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import erf, erfc, logsumexp

ROOT = Path(__file__).resolve().parent


def expLaw(q, rate):
    identity = sp.eye(q.rows)
    ones = sp.ones(q.rows, 1)
    h = (rate * identity - q).inv() * ones
    f = ones - rate * h
    return f, h


def cost(weights, f, h):
    return sp.factor(sum(weights[i] * h[i] / f[i] for i in range(len(f))))


def main():
    report = {}
    q = sp.Matrix([[-3, 1, 1], [1, -4, 1], [1, 1, -5]])
    green = (-q).inv()
    f1, h1 = expLaw(q, sp.Rational(1))
    f4, h4 = expLaw(q, sp.Rational(4))
    f0, h0 = (f1 + 2 * f4) / 3, (h1 + 2 * h4) / 3
    z = (f0.T * f0)[0]
    weights = [value**2 / z for value in f0]
    f, h = expLaw(q, sp.Rational(2))
    j0, j = cost(weights, f0, h0), cost(weights, f, h)
    gap = sum(
        green[i, k]
        * f0[i]
        * f0[k]
        * (f[i] / f0[i] - f[k] / f0[k]) ** 2
        / ((f[i] / f0[i]) * (f[k] / f0[k]))
        for i in range(3)
        for k in range(3)
    ) / (2 * z)
    assert h == green * f and h0 == green * f0
    assert sp.factor(j - j0 - gap) == 0 and gap > 0
    report["reversibleExact"] = {
        "Q": str(q),
        "green": str(green),
        "referenceSuccess": str(f0),
        "weights": [str(value) for value in weights],
        "referenceCost": str(j0),
        "competitorCost": str(j),
        "gap": str(sp.factor(gap)),
        "identityResidual": "0",
    }
    print("Exact reversible-chain gap verified:", sp.factor(gap), flush=True)

    # A directed cycle with unequal killing: uniform reversible weighting is invalid.
    nonrev = sp.Matrix([[-2, 1, 0], [0, -3, 1], [1, 0, -4]])
    f0n, h0n = expLaw(nonrev, sp.Rational(1))
    zn = (f0n.T * f0n)[0]
    wn = [value**2 / zn for value in f0n]
    reference = cost(wn, f0n, h0n)
    candidates = []
    for rate in [sp.Rational(9, 10), sp.Rational(11, 10)]:
        fn, hn = expLaw(nonrev, rate)
        value = cost(wn, fn, hn)
        if rate == sp.Rational(9, 10):
            assert value - reference == -sp.Rational(761111595, 7705213313411)
            assert value < reference
        candidates.append(
            {
                "rate": str(rate),
                "cost": str(value),
                "difference": str(value - reference),
            }
        )
    report["nonreversibleDiagnostic"] = {
        "Q": str(nonrev),
        "weights": [str(value) for value in wn],
        "referenceCost": str(reference),
        "competitors": candidates,
    }
    print("Nonreversible diagnostic:", candidates, flush=True)

    greenChecks = []
    for t in [0.2, 1.0, 7.0]:
        for x in [0.1, 1.0, 3.0]:
            direct = quad(lambda s: erf(x / np.sqrt(4 * s)), 0, t, epsabs=1e-11)[0]
            kernel = quad(lambda y: y * erfc(y / np.sqrt(4 * t)), 0, x, epsabs=1e-11)[0]
            kernel += (
                x * quad(lambda y: erfc(y / np.sqrt(4 * t)), x, np.inf, epsabs=1e-11)[0]
            )
            assert np.isfinite(direct) and np.isfinite(kernel)
            assert abs(direct - kernel) < 1e-9
            greenChecks.append(
                {"t": t, "x": x, "directTimeIntegral": direct, "greenIntegral": kernel}
            )
    report["brownianGreenChecks"] = greenChecks
    print("Independent time and spatial integrals agree for all 9 checks", flush=True)

    def brownianCost(rates, mixing):
        rates, mixing = np.array(rates), np.array(mixing)

        def integrand(x):
            if x == 0:
                return 0.0
            exponents = -np.sqrt(rates) * x
            logf = logsumexp(np.log(mixing) + exponents)
            h = np.sum(mixing * (-np.expm1(exponents)) / rates)
            return np.exp(np.log(2) - 2 * x + np.log(h) - logf)

        return quad(integrand, 0, np.inf, epsabs=2e-10, epsrel=2e-10)

    examples = [
        ([1.0], [1.0]),
        ([0.25], [1.0]),
        ([2.25], [1.0]),
        ([0.2, 5.0], [0.4, 0.6]),
    ]
    rng = np.random.default_rng(20261017)
    for _ in range(36):
        rates = np.exp(rng.uniform(-2, 1, size=4))
        mixing = rng.dirichlet(np.ones(4))
        examples.append((rates.tolist(), mixing.tolist()))
    numerical = []
    for index, (rates, mixing) in enumerate(examples, 1):
        value, error = brownianCost(rates, mixing)
        assert np.isfinite(value) and np.isfinite(error)
        assert value >= 1 - 2e-9
        numerical.append(
            {
                "rates": rates,
                "weights": mixing,
                "cost": value,
                "quadratureErrorEstimate": error,
            }
        )
        print(
            f"Brownian comparison {index}/{len(examples)}: cost={value:.10f}, optimum=1",
            flush=True,
        )
    report["brownianExponentialTarget"] = numerical
    report["interpretation"] = (
        "These calculations check identities and examples; the all-law result rests on the proof. "
        "Random finite mixtures are not an exhaustive search and are not evidence of novelty."
    )
    (ROOT / "resetting_verification.json").write_text(json.dumps(report, indent=2))
    print("Saved resetting_verification.json", flush=True)


if __name__ == "__main__":
    main()
