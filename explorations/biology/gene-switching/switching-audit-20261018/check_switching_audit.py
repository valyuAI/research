"""Independent exact checks of finite-dose switching certificates and design.

Run: python3 check_switching_audit.py
Requires the existing SymPy installation; no downloads or experiment data.
"""

import json
from pathlib import Path

import sympy as sp


def main():
  checks = []

  def equal(name, observed, expected):
    difference = observed - expected
    if isinstance(difference, sp.MatrixBase):
      valid = all(sp.factor(item) == 0 for item in difference)
    else:
      valid = sp.factor(difference) == 0
    if not valid:
      raise AssertionError(f"{name}: {difference}")
    checks.append(name)
    print(f"PASS {len(checks):02d}: {name}", flush=True)

  c, b, k = sp.symbols("c b k", positive=True)
  q = sp.Matrix([
    [-b*c, b*c, 0, 0],
    [b, -b-k, k, 0],
    [0, k, -k-b*c, b*c],
    [0, 0, b, -b],
  ])
  pi = sp.Matrix([[1, c, c, c*c]]) / (1+c)**2
  equal("four-state stationary generator equation", pi*q, sp.zeros(1, 4))
  equal("four-state detailed balance", sp.diag(*pi)*q, q.T*sp.diag(*pi))
  offMeans = -q[:2, :2].inv()*sp.ones(2, 1)
  onMeans = -q[2:, 2:].inv()*sp.ones(2, 1)
  mOff = sp.factor(offMeans[1])
  mOn = sp.factor(onMeans[0])
  equal("OFF entry mean derived from killed generator", mOff, (1+c)/(k*c))
  equal("ON entry mean derived from killed generator", mOn, (1+c)/k)
  equal("mean-dwell invariant", 1/(1/mOff+1/mOn), 1/k)

  # Three identical Td values do not universally imply four states.
  qThree = sp.Matrix([[-13*c, 13*c, 0], [13, -13-c, c], [0, 1, -1]])
  piThree = sp.Matrix([[1, c, c*c]]) / (1+c+c*c)
  equal("old three-state witness stationarity", piThree*qThree, sp.zeros(1, 3))
  equal("old three-state witness detailed balance", sp.diag(*piThree)*qThree,
        qThree.T*sp.diag(*piThree))
  activity = piThree[1]
  crossingFlux = piThree[1]*(13+c)
  tdThree = sp.factor(activity*(1-activity)/crossingFlux)
  equal("three equal Td values factorization", tdThree-sp.Rational(1, 21),
        -(c-1)*(c-2)*(c-4)/(21*(c+13)*(c*c+c+1)))
  equal("three equal Td values", sp.Matrix([tdThree.subs(c, x) for x in (1, 2, 4)]),
        sp.ones(3, 1)/21)
  equal("three differing activity values", sp.Matrix([activity.subs(c, x) for x in (1, 2, 4)]),
        sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 7), sp.Rational(4, 21)]))

  x, y, z, epsilon = sp.symbols("x y z epsilon", positive=True)
  f = lambda dose: dose/(1+dose)
  positiveContrast = (z-y)*f(x)+(y-x)*f(z)
  negativeContrast = (z-x)*f(y)
  threshold = sp.factor((negativeContrast-positiveContrast)/(negativeContrast+positiveContrast))
  equal("general sharp target-box threshold", threshold,
        (y-x)*(z-y)/(2*x*y*z+x*y+x*z+y*y+y*z+2*y))
  contrast = positiveContrast/(1-epsilon)-negativeContrast/(1+epsilon)
  equal("contrast sign threshold", contrast,
        (positiveContrast+negativeContrast)*(epsilon-threshold)/(1-epsilon**2))
  chord = (y+x*z)/((1+x)*(1+z))
  equal("OFF chord at interior dose", positiveContrast/(z-x), chord)
  ratio = sp.factor(f(y)/chord)
  equal("optimal interior dose derivative", sp.diff(ratio, y),
        (1+x)*(1+z)*(x*z-y*y)/((1+y)**2*(y+x*z)**2))

  a, r = sp.symbols("a r", positive=True)
  peakRatio = (1+a/r)*(1+a*r)/(1+a)**2
  equal("fixed-span placement derivative", sp.diff(peakRatio, a),
        (r-1)**2*(1-a)/(r*(1+a)**3))
  optimizedThreshold = (r-1)**2/(r*r+6*r+1)
  equal("optimized dose triple threshold", threshold.subs({x: 1/r, y: 1, z: r}),
        optimizedThreshold)
  equal("ON endpoint threshold for symmetric triple", ((z-x)/(2+x+z)).subs({x: 1/r, z: r}),
        (r-1)/(r+1))

  # Any nonnegative OFF affine fit can be realized by a full three-state CTMC.
  A, B, d = sp.symbols("A B d", positive=True)
  qFit = sp.Matrix([[-A-B*c, A+B*c, 0], [k, -k-d*c, d*c], [0, d, -d]])
  rawFitPi = sp.Matrix([[k, A+B*c, c*(A+B*c)]])
  fitPi = rawFitPi/sum(rawFitPi)
  equal("fitting three-state generator stationarity", fitPi*qFit, sp.zeros(1, 3))
  equal("fitting three-state detailed balance", sp.diag(*fitPi)*qFit,
        qFit.T*sp.diag(*fitPi))
  fitOnMeans = -qFit[1:, 1:].inv()*sp.ones(2, 1)
  equal("fitting three-state ON mean", fitOnMeans[0], (1+c)/k)
  equal("fitting three-state OFF mean", -1/qFit[0, 0], 1/(A+B*c))
  twoPointLine = k*(c+x*z)/((1+x)*(1+z))
  for dose in (x, z):
    equal(f"three-state exact two-dose fit at {dose}", twoPointLine.subs(c, dose), k*f(dose))

  # At the target-box threshold the affine chord fits all mean intervals.
  boundaryLine = k*(c+x*z)/((1+x)*(1+z)*(1-threshold))
  for dose, sign in ((x, -1), (y, 1), (z, -1)):
    relativeMean = (1/boundaryLine.subs(c, dose))/((1+dose)/(k*dose))
    equal(f"full three-state boundary-box fit at {dose}", relativeMean, 1+sign*threshold)

  designs = []
  for doses in ((1, 2, 4), (sp.Rational(1, 2), 1, 2), (sp.Rational(1, 4), 1, 4),
                (sp.Rational(1, 10), 1, 10)):
    cx, cy, cz = map(sp.Rational, doses)
    error = threshold.subs({x: cx, y: cy, z: cz})
    line = sp.factor(boundaryLine.subs({x: cx, y: cy, z: cz, k: 1}))
    meansOn = [1+dose for dose in (cx, cy, cz)]
    meansOff = [(1+dose)/dose for dose in (cx, cy, cz)]
    for index, dose in enumerate((cx, cy, cz)):
      fitted = 1/line.subs(c, dose)
      assert (1-error)*meansOff[index] <= fitted <= (1+error)*meansOff[index]
    equal(f"boundary intercept nonnegative at {doses}", int(bool(line.subs(c, 0) >= 0)), 1)
    equal(f"boundary slope nonnegative at {doses}", int(bool(sp.diff(line, c) >= 0)), 1)
    designs.append({
      "concentrations": list(map(str, doses)),
      "relative_halfwidth_threshold": str(error),
      "relative_halfwidth_decimal": float(error),
      "ON_means_k1": list(map(str, meansOn)),
      "OFF_means_k1": list(map(str, meansOff)),
      "boundary_OFF_exit_rate_k1": str(line),
    })

  # A concrete 10% target-box contrast for the 16-fold dose design.
  practical = {x: sp.Rational(1, 4), y: 1, z: 4, epsilon: sp.Rational(1, 10)}
  equal("practical 10-percent OFF contrast is strictly negative", contrast.subs(practical),
        -sp.Rational(49, 132))
  onGap = 1/((1+x)*(1+epsilon))-1/((1+z)*(1-epsilon))
  equal("practical 10-percent ON monotonicity gap positive", onGap.subs(practical),
        sp.Rational(50, 99))
  result = {
    "date": "2026-10-18",
    "symbolic_checks_passed": len(checks),
    "checks": checks,
    "designs": designs,
    "scope": "Exact mathematical checks of target-centered deterministic mean intervals. No biological data, statistical coverage claim, or novelty claim.",
    "three_state_fit_scope": "Reversible nonnegative-affine rates at each dose; mixed A+B*c edge does not assert elementary mass-action ligand kinetics.",
  }
  output = Path(__file__).with_name("checks.json")
  output.write_text(json.dumps(result, indent=2)+"\n")
  print(f"Wrote {output}; all {len(checks)} checks passed", flush=True)


if __name__ == "__main__":
  main()
