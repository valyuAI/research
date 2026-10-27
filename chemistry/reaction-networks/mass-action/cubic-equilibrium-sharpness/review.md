# Independent audit: sharp equilibrium counts with cubic sources

18 October 2026. Mathematical audit of the all-species construction in
`paper.tex`. This is an internal proof review,
not external peer review or a completed priority assessment. Paths have been adapted for this package; the mathematical audit is unchanged.

## Source and precise target

The current primary source is Murad Banaji and Elisenda Feliu, *Positive
equilibria in mass action networks: geometry and bounds*, Journal of
Mathematical Biology 93, article 37 (2026),
<https://doi.org/10.1007/s00285-026-02429-8>. The relevant statements were checked in the complete 61-page publisher
PDF. Third-party full text is not bundled here. The arXiv contents
extraction previously supplied an obsolete single-author manuscript even
when a v5 URL was requested; that obsolete text is not the basis of this
claim.

On printed pages 38-39, Corollary 4.21(i) bounds the number of positive
nondegenerate equilibria of an n-species, n-reaction, rank-(n-1) network by
n. Remark 4.23 explicitly asks whether this is attained for every n and
the minimum source molecularity required. Corollary 5.16 bounds quadratic
networks of this size and rank by two positive nondegenerate equilibria.
For n=2, Remark 4.23 explicitly excludes multiple positive nondegenerate
equilibria in the quadratic case. These are the exact published statements
used below.

## All-n proof audit

Fix n >= 2. Let A have rows A_i=2e_i+e_(i+1) for i<n and A_n=2e_n.
It is upper triangular with determinant D=2^n. The vector p=D A^{-1}1 is

    p_i = (2^n + (-1)^(n-i) 2^(i-1))/3.

Substitution verifies 2p_i+p_(i+1)=D and 2p_n=D. The numerator is positive
and divisible by 3. Distinct signed powers of two show that the p_i are
pairwise distinct. Thus the exponents 0,p_1,...,p_n are distinct
nonnegative integers.

For any n distinct positive rational numbers r_j, solve

    a_0 + sum_i a_i r_j^(p_i) = 0  (j=1,...,n).

Every n-column minor of this n-by-(n+1) evaluation matrix is nonsingular:
otherwise a nonzero polynomial with at most n monomials would have n
distinct positive roots, contrary to Descartes' rule of signs. Consequently
the rational kernel is one-dimensional and every coefficient of any
nonzero kernel vector is nonzero. The resulting polynomial P has exactly
the n prescribed positive roots, all simple, because n+1 monomials permit
at most n positive roots counted with multiplicity. Its signs alternate
when coefficients are ordered by exponent. Set c_i=|a_i| and
z_i=sign(a_i). In particular z has both signs for n>=2.

Define reaction columns

    gamma_i = -e_i + (z_i/z_(i+1)) e_(i+1)  (i<n),
    gamma_n = -sum_(i<n) gamma_i.

For i<n, the product is

    A_i + gamma_i = e_i + (1+z_i/z_(i+1)) e_(i+1).

For the last reaction, the product is

    e_1 + sum_(j=2)^(n-1) (1-z_(j-1)/z_j)e_j
        + (2-z_(n-1)/z_n)e_n.

Every coefficient is a nonnegative integer. Maximum source molecularity
is exactly three; product molecularity is at most 2n. The first n-1
columns have a triangular nonsingular (n-1)-by-(n-1) block, so Gamma has
rank n-1. Its right kernel is span(1), its left kernel is span(z), and
its image S is z-perpendicular.

With positive rational rates kappa_i=c^(-A_i), any positive equilibrium
has equal positive reaction fluxes lambda. Taking logarithms yields
A log(x/c)=log(lambda)1, hence the complete positive equilibrium curve is

    x_i(t)=c_i t^(p_i), t>0.

Conversely every point on this curve has all fluxes t^D. Its intersections
with the class z.x=-a_0 are exactly the positive roots of P, so there are
exactly n such equilibria.

At a point on the curve,

    J = t^D Gamma A diag(1/x).

It has rank n-1 and kernel span(diag(x)p)=span(t x'(t)). Its image is S,
so J restricted to S is nonsingular precisely when x'(t) is not in S.
At every prescribed root, z.x'(r_j)=P'(r_j) is nonzero. This proves
nondegeneracy on the stoichiometric class, not nonsingularity of the full
n-by-n Jacobian.

For n>=3, the published quadratic upper bound of two is below n. For
n=2, the published rank-one exception excludes two quadratic equilibria.
Together with this construction, the minimum possible maximum source
molecularity for attaining n is exactly three for every n>=2. This says
nothing about minimum product molecularity or stability.

## Robustness is valid, with a useful precision

Fix A and Gamma from the construction. For arbitrary positive rates,
define c(kappa)=exp(-A^{-1}log(kappa)). The complete positive equilibrium
curve is still x_i=c_i(kappa)t^(p_i). The class equation is

    sum_i z_i c_i(kappa)t^(p_i) - K = 0.

The n simple positive roots persist in disjoint positive intervals under
small simultaneous changes of (kappa,K), by the implicit function theorem.
Descartes' rule bounds the total number of positive roots counted with
multiplicity by n, since the equation has at most n+1 monomials. Thus
there are exactly n positive, nondegenerate equilibria throughout an open
neighborhood of the constructed parameter pair.

It would be insufficient to exclude additional degenerate equilibria
using Corollary 4.21 alone, because that result bounds only nondegenerate
equilibria. The direct monomial-curve argument above excludes them. No
quantitative neighborhood size, condition number or stability is asserted.

## Independent finite-case replay and code review

Both commands were independently read and executed successfully:

    python3 -B -O verification/verify_cubic_sharpness.py
    python3 -B -O verification/independent_cubic_check.py

Each covers n=2,...,8 and all 35 prescribed positive equilibria. The
second checker uses only standard-library rational arithmetic. It builds
Gamma directly from the supplied source and product complexes, evaluates
the actual mass-action vector field, differentiates those monomials, and
tests the determinant formed from the first n-1 Jacobian rows plus z.
The checked top-left Gamma minor guarantees that the selected field rows
are independent coordinates on S. It additionally rejects corrupted
products, concentrations and rates. No correctness-affecting issue or
useful simplification was found. These finite checks support the proof
but do not substitute for its all-n argument or establish priority.

As a small independent example, for n=3:

    P(t)=11t^4-60t^3+85t^2-36
        =(t-1)(t-2)(t-3)(11t+6),
    p=(3,2,4), c=(60,85,11), z=(-1,1,1).

The reactions are 2X+Y -> X, 2Y+Z -> Y+2Z and 2Z -> X+2Y+Z, with rates
1/306000, 1/79475 and 1/121. The curve (60t^3,85t^2,11t^4) intersects
-X+Y+Z=36 at t=1,2,3. Every reaction flux there equals t^8.

## Interpretation boundary

The proof is sound under the stated mathematical mass-action definitions.
The conservation vector has mixed signs, and its positive classes are
unbounded. It does not furnish a positive conserved mass vector or a
closed mass-balanced chemical mechanism. Multiple nondegenerate equilibria
do not imply multiple stable equilibria. Products can have molecularity
above three. The result is a mathematical sharpness construction addressing
the published question; it is not an experimental finding. Further work
must separately assess subsequent prior literature and any external review.
