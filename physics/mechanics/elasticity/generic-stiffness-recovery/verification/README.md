# Exact arithmetic certificates

The default check needs Python and SymPy (tested with Python 3.13 and SymPy 1.14.0). It uses exact rational, Gaussian-rational, or finite-field arithmetic, makes no network requests, and does not require Singular. Run without Python's `-O` option so that assertions remain enabled; the driver rejects optimized execution.

From the parent paper directory, with the listed software installed:

```bash
python3 verification/verify_all.py
```

The driver prints progress and fails on unexpected arithmetic, a timeout, or a nonzero exit status. It reconstructs the Christoffel map and trace kernel; verifies the Borel fixed lines, both normal quotients, and the separate rank-eleven tangent bound; reconstructs the projective-slice certificates; verifies the rank-one equations by rational linear algebra; and checks eleven explicit identities in the original minors of the second normal quotient. It confirms that the embedded certificate matrix agrees exactly with the reconstructed matrix. It also reconstructs and verifies the separate eleven-direction cubic-slice certificate, binding the source and identity SHA256 hashes. Outputs are retained beside the scripts, including `verification_summary.json` and per-stage logs.

The `verification/linear-certificates/` package certifies **upper bounds** of two and three for the affine dimensions of the rank-at-most-two and rank-at-most-three loci of `N2`. Six cubic identities give the first bound; four quartic identities and one quintic give the second. Their leading monomials generate ideals contained in the corresponding initial minor ideals. Minimum variable-cover sizes of six and five prove the required bounds in eight variables. The proof needs no equality of these dimensions and no complete Gröbner basis. The standalone checker uses only the Python standard library:

```bash
python3 verification/linear-certificates/verify_certificates.py
```

This standalone command checks the supplied matrix. Use the main driver to also verify its derivation and agreement with the elasticity construction. The minor-identity checker and both finite-direction checkers below are standard-library-only; the other matrix checks use SymPy.

The compact [finite-direction certificate](finite-directions/README.md) proves the dimension bound for pairs whose quartic collision polynomial divides their sextic collision polynomial. Its two standalone checks are also included in the default driver:

```bash
python3 -O -u verification/finite-directions/verify_gcd4_slice_source.py 11
python3 -O -u verification/finite-directions/verify_direct_powers.py
```

These checkers deliberately run with assertions disabled and use explicit exceptions. The first verifies the original tensor-to-cubic identities on complete unisolvent grids. The second multiplies eleven direct ideal-membership identities and checks their pure leading powers. Their approximately one-megabyte certificate needs no intermediate basis or CAS. Source/identity hashes appear in their audit files and the main verification summary. The full geometric argument and its remaining hypotheses are in the paper and `finite-directions/INCIDENCE_PROOF.md`.

The script proves the arithmetic assertions, not the entire geometric argument. The paper supplies the deductions using Borel fixed points, tangent cones, projective intersection, and proper specialization.

Saved slice certificates can also be checked without Singular after the source matrix is reconstructed:

```bash
python3 verification/check_collision_incidence.py
python3 verification/certify_rank14_pencil.py
python3 verification/verify_slice_certificates.py
```

The latter checker multiplies the complete Bezout identities and verifies every saved determinant polynomial on an unisolvent grid of the full required degree. These are polynomial-identity checks, not random sampling. The finite-field identities imply geometric emptiness over the algebraic closure, and the paper explains the transfer to characteristic zero.

The original Gröbner computations remain as **optional corroboration**, tested with Singular 4.4.1p5:

```bash
python3 verification/verify_all.py --with-groebner
```

This runs the default checks and then reconstructs both determinantal ideals in two monomial orders, independently checking each dimension readout from the supports of its leading monomials. It also fails on a missing Singular binary or a Singular error marker. The saved original runs give exact dimensions two and three; these equality claims are not required by the main proof.

The original default run passed, and an isolated extraction of the original portable archive passed the optional full replay. Its separate records are `verification/portable_optional_run.log` and `verification/portable_optional_verification_summary.json`. Those historical records predate the eleven-direction extension. The primary `verification_summary.json` records the latest default run; its finite-direction fields must be present to certify coverage of the added checks. `verification/package_replay_audit.json` records the earlier source hashes and standalone standard-library check with site packages disabled.

`prepare_rank_slice.py` and `prepare_recursive_normal_ideals.py` retain the construction procedure for the exact Singular inputs. The former recreates nested slices and selected minors; the saved complete Bezout files are the proof certificates. The certificate generators and intermediate discovery workspaces are unnecessary for checking the eleven identities and are omitted. Old unsuccessful experiments and incomplete outputs are not part of this package.


The retained portable-replay records refer to the original package layout, where this directory was named `certificates` and the alternate PDF was `journal_version.pdf`. The source checks are unchanged. This collection uses the shared [Lean project](../../../../../formal/) for formalized components.
