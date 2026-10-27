"""Antiprisms (needs sympy): every n-antiprism (n >= 3), regular n-gon caps twisted by pi/n, any height, is
first-order rigid in the point-hyperplane model.  Proof data for Section 'Prisms and antiprisms' of the paper.

By AHWZ Prop. 3.6 it suffices to show there is no non-zero stress (omega, eta).  On a triangle, sum eta_i p_i = 0
with three linearly independent p_i forces eta = 0, so eta lives only on the two n-gon caps.  The cyclic shift
(rotation by 2 pi / n) acts on stresses; on the eigenspace with eigenvalue z (z^n = 1) a stress is
omega_X(k) = omega_X z^k for the four edge orbits X = T (top), B (bottom), L (a_k b_k), M (b_k a_{k+1}) and
eta_A(k) = eta_A z^k, eta_B(k) = eta_B z^k.  Writing vertex equilibrium in the local frame of a_0 and b_0 gives the
x, y equations M4(z) (omega) = 0 below (eta enters only the z equations).  This script computes det M4 and the
low-mode (z = 1, z = e^{+-2 i phi}) systems including the z equations with eta = 0."""
import sympy as sp

c, s, R, z, z0 = sp.symbols('c s R z z0')       # c = cos(phi), s = sin(phi), phi = pi/n; z0 = half height
C2, S2 = 2 * c**2 - 1, 2 * c * s


def v(cs, sn, zz):
  return sp.Matrix([R * cs, R * sn, zz])


wT, wB, wL, wM = sp.symbols('wT wB wL wM')
# vertex a_0 at angle 0 (height z0), neighbours a_1, a_{-1} at +-2phi, b_0 at phi, b_{-1} at -phi (height -z0)
a, ap, am, bk, bkm = v(1, 0, z0), v(C2, S2, z0), v(C2, -S2, z0), v(c, s, -z0), v(c, -s, -z0)
EqA = wT * (a - ap) + wT / z * (a - am) + wL * (a - bk) + wM / z * (a - bkm)
# vertex b_0 in its local frame: b_1, b_{-1} at +-2phi, a_0 at -phi, a_1 at +phi
b, bp, bm, ak, akp = v(1, 0, -z0), v(C2, S2, -z0), v(C2, -S2, -z0), v(c, -s, z0), v(c, s, z0)
EqB = wB * (b - bp) + wB / z * (b - bm) + wL * (b - ak) + wM * (b - akp)
unk = [wT, wB, wL, wM]
M4 = sp.Matrix([[sp.diff(e, u) for u in unk] for e in [EqA[0], EqA[1], EqB[0], EqB[1]]])
num, den = sp.fraction(sp.together(M4.det(method='berkowitz')))
num = sp.expand(num)
for _ in range(6):
  num = sp.expand(num.subs(s**2, 1 - c**2))
claimed = 4 * R**4 * (c - 1)**3 * (c + 1) * (z - 1) * (z**2 - 2 * (2 * c**2 - 1) * z + 1)
if sp.expand(num - claimed) != 0 or den != z**3:
  raise ValueError('generic Fourier determinant mismatch')
print('det M4(z) = 4 R^4 (c-1)^3 (c+1) (z-1) (z^2 - 2 cos(2 phi) z + 1) / z^3   [verified]')
print('  -> nonzero for every n-th root of unity z != 1, e^{+-2 i phi}, i.e. every mode 2 <= j <= n-2')
# low modes: eta = 0 there (cap equations), so all six components must vanish with omega only
M6 = sp.Matrix([[sp.diff(e, u) for u in unk] for e in list(EqA) + list(EqB)])
m_low = sp.factor(sp.together(M6.extract([0, 2, 3, 5], [0, 1, 2, 3]).det(method='berkowitz')))
claimed_low = 16 * R**2 * z0**2 * (c - 1)**2 * (c + 1)**2 * (z - 1) * (z + 1)**2 / z**3
if sp.simplify(m_low - claimed_low) != 0:
  raise ValueError('low-mode minor mismatch')
print('modes j = +-1: minor (x_a, z_a, x_b, z_b) =', m_low)
print('  -> nonzero at z = e^{+-2 i phi} because z != +-1 for n >= 3, c != +-1 and z0 > 0')
M0 = M6.subs(z, 1)
m0 = sp.factor(sp.expand(M0.extract([0, 1, 2, 3], [0, 1, 2, 3]).det(method='berkowitz')))
claimed_zero = -64 * R**3 * s * z0 * (c - 1)**2 * (c + 1)**2
if sp.simplify(m0 - claimed_zero) != 0:
  raise ValueError('zero-mode minor mismatch')
print('mode j = 0: minor (x_a, y_a, z_a, x_b) at z = 1 =', m0)
print('  -> nonzero since R, s, z0 > 0 and c != +-1')
