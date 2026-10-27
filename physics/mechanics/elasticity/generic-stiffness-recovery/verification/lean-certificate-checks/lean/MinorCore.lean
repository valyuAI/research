import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

-- Bound pending elaboration work; every theorem is still kernel checked.
set_option Elab.async false

noncomputable section

namespace ValyuResearch.ElasticityMinorCertificates

abbrev cadd (x y : ℂ) : ℂ := x + y
abbrev cmul (x y : ℂ) : ℂ := x * y
abbrev cpow (x : ℂ) (n : ℕ) : ℂ := x ^ n

/-- The supplied recursive normal matrix, in its original eight coordinates. -/
def normalMatrix (w : Fin 8 → ℂ) : Matrix (Fin 7) (Fin 13) ℂ :=
  !![(cmul (-2 : ℂ) (w 2)), (cadd (cmul (-2 : ℂ) (w 0)) (cmul (cmul (-6 : ℂ) Complex.I) (w 7))), 0, (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 4)) (cmul (-2 : ℂ) (w 5))), (cadd (cmul (-2 : ℂ) (w 0)) (cadd (cmul (-2 : ℂ) (w 6)) (cmul (cmul (-2 : ℂ) Complex.I) (w 7)))), 0, 0, 0, (cadd (cmul (2 : ℂ) (w 6)) (cmul (cmul (-4 : ℂ) Complex.I) (w 7))), (cadd (cmul (-2 : ℂ) (w 2)) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 4)) (cmul (-2 : ℂ) (w 5)))), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 6)) (cmul (-4 : ℂ) (w 7))), (cadd (cmul (-4 : ℂ) (w 4)) (cmul (cmul (4 : ℂ) Complex.I) (w 5))), (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 6)) (cmul (4 : ℂ) (w 7)));
    (cadd (cmul (4 : ℂ) (w 0)) (cadd (cmul (-2 : ℂ) (w 1)) (cmul (cmul (12 : ℂ) Complex.I) (w 7)))), (cadd (cmul (-2 : ℂ) (w 2)) (cmul (cmul (-2 : ℂ) Complex.I) (w 4))), (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 2)) (cmul (2 : ℂ) (w 4))), (cadd (cadd (cmul (2 : ℂ) (w 0)) (cmul (2 : ℂ) (w 3))) (cadd (cmul (2 : ℂ) (w 6)) (cmul (cmul (2 : ℂ) Complex.I) (w 7)))), (cadd (cmul (-2 : ℂ) (w 2)) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 4)) (cmul (-4 : ℂ) (w 5)))), 0, (cadd (cmul (2 : ℂ) (w 6)) (cmul (cmul (-4 : ℂ) Complex.I) (w 7))), (cadd (cmul (-6 : ℂ) (w 2)) (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 4)) (cmul (-2 : ℂ) (w 5)))), (cadd (cmul (2 : ℂ) (w 2)) (cmul (2 : ℂ) (w 5))), (cadd (cadd (cmul (-2 : ℂ) (w 0)) (cmul (-2 : ℂ) (w 1))) (cadd (cmul (2 : ℂ) (w 3)) (cmul (cmul (-6 : ℂ) Complex.I) (w 7)))), (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 2)) (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-4 : ℂ) Complex.I) (w 5)))), (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 3)) (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 6)) (cmul (-8 : ℂ) (w 7)))), (cmul (cmul (4 : ℂ) Complex.I) (w 5));
    (cmul (cmul (-2 : ℂ) Complex.I) (w 2)), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 0)) (cmul (6 : ℂ) (w 7))), 0, (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-2 : ℂ) Complex.I) (w 5))), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 0)) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 6)) (cmul (2 : ℂ) (w 7)))), 0, 0, 0, (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 6)) (cmul (4 : ℂ) (w 7))), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-2 : ℂ) Complex.I) (w 5)))), (cadd (cmul (2 : ℂ) (w 6)) (cmul (cmul (-4 : ℂ) Complex.I) (w 7))), (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 4)) (cmul (-4 : ℂ) (w 5))), (cadd (cmul (-2 : ℂ) (w 6)) (cmul (cmul (4 : ℂ) Complex.I) (w 7)));
    (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 0)) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 1)) (cmul (-6 : ℂ) (w 7)))), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cmul (2 : ℂ) (w 4))), (cadd (cmul (2 : ℂ) (w 2)) (cmul (-2 : ℂ) (w 5))), (cmul (cmul (2 : ℂ) Complex.I) (w 3)), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-4 : ℂ) Complex.I) (w 5)))), 0, (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 6)) (cmul (4 : ℂ) (w 7))), (cadd (cmul (cmul (-4 : ℂ) Complex.I) (w 2)) (cmul (2 : ℂ) (w 4))), (cmul (2 : ℂ) (w 4)), (cadd (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 0)) (cmul (cmul (-2 : ℂ) Complex.I) (w 1))) (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 3)) (cmul (6 : ℂ) (w 7)))), (cadd (cmul (2 : ℂ) (w 2)) (cmul (2 : ℂ) (w 5))), (cadd (cmul (4 : ℂ) (w 3)) (cadd (cmul (2 : ℂ) (w 6)) (cmul (cmul (-4 : ℂ) Complex.I) (w 7)))), (cmul (-4 : ℂ) (w 5));
    (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cmul (2 : ℂ) (w 4))), 0, (cadd (cadd (cmul (-2 : ℂ) (w 1)) (cmul (2 : ℂ) (w 3))) (cadd (cmul (2 : ℂ) (w 6)) (cmul (cmul (-4 : ℂ) Complex.I) (w 7)))), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-4 : ℂ) Complex.I) (w 5)))), 0, (cadd (cmul (1 : ℂ) (w 6)) (cmul (cmul (-2 : ℂ) Complex.I) (w 7))), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-2 : ℂ) Complex.I) (w 5)))), (cadd (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 1)) (cmul (cmul (-2 : ℂ) Complex.I) (w 3))) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 6)) (cmul (-4 : ℂ) (w 7)))), (cadd (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 0)) (cmul (cmul (-2 : ℂ) Complex.I) (w 1))) (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 3)) (cmul (6 : ℂ) (w 7)))), 0, (cadd (cadd (cmul (-2 : ℂ) (w 1)) (cmul (2 : ℂ) (w 3))) (cadd (cmul (1 : ℂ) (w 6)) (cmul (cmul (-2 : ℂ) Complex.I) (w 7)))), (cmul (-4 : ℂ) (w 5)), 0;
    (cmul (2 : ℂ) (w 7)), 0, (cmul (2 : ℂ) (w 5)), (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 6)) (cmul (2 : ℂ) (w 7))), 0, (cmul (2 : ℂ) (w 5)), (cadd (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 1)) (cmul (cmul (2 : ℂ) Complex.I) (w 3))) (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 6)) (cmul (4 : ℂ) (w 7)))), (cmul (cmul (-2 : ℂ) Complex.I) (w 5)), (cadd (cmul (cmul (-2 : ℂ) Complex.I) (w 2)) (cadd (cmul (2 : ℂ) (w 4)) (cmul (cmul (-2 : ℂ) Complex.I) (w 5)))), 0, 0, (cmul (2 : ℂ) (w 6)), 0;
    0, 0, 0, 0, 0, (cmul (-1 : ℂ) (w 6)), (cmul (cmul (2 : ℂ) Complex.I) (w 5)), 0, (cadd (cmul (cmul (2 : ℂ) Complex.I) (w 6)) (cmul (2 : ℂ) (w 7))), 0, (cmul (1 : ℂ) (w 6)), 0, 0]

-- Certificate SHA256: 54e6d4467405a6c5e33892369cbce7e9cd0d9a2ae5c41110df5c2aa8a177b11a

set_option maxHeartbeats 4000000 in
theorem det_fin_four {R : Type*} [CommRing R] (A : Matrix (Fin 4) (Fin 4) R) :
    Matrix.det A =
    A 0 0 * A 1 1 * A 2 2 * A 3 3
    - A 0 0 * A 1 1 * A 2 3 * A 3 2
    - A 0 0 * A 1 2 * A 2 1 * A 3 3
    + A 0 0 * A 1 2 * A 2 3 * A 3 1
    + A 0 0 * A 1 3 * A 2 1 * A 3 2
    - A 0 0 * A 1 3 * A 2 2 * A 3 1
    - A 0 1 * A 1 0 * A 2 2 * A 3 3
    + A 0 1 * A 1 0 * A 2 3 * A 3 2
    + A 0 1 * A 1 2 * A 2 0 * A 3 3
    - A 0 1 * A 1 2 * A 2 3 * A 3 0
    - A 0 1 * A 1 3 * A 2 0 * A 3 2
    + A 0 1 * A 1 3 * A 2 2 * A 3 0
    + A 0 2 * A 1 0 * A 2 1 * A 3 3
    - A 0 2 * A 1 0 * A 2 3 * A 3 1
    - A 0 2 * A 1 1 * A 2 0 * A 3 3
    + A 0 2 * A 1 1 * A 2 3 * A 3 0
    + A 0 2 * A 1 3 * A 2 0 * A 3 1
    - A 0 2 * A 1 3 * A 2 1 * A 3 0
    - A 0 3 * A 1 0 * A 2 1 * A 3 2
    + A 0 3 * A 1 0 * A 2 2 * A 3 1
    + A 0 3 * A 1 1 * A 2 0 * A 3 2
    - A 0 3 * A 1 1 * A 2 2 * A 3 0
    - A 0 3 * A 1 2 * A 2 0 * A 3 1
    + A 0 3 * A 1 2 * A 2 1 * A 3 0 := by
  rw [Matrix.det_succ_row_zero]
  simp only [Fin.sum_univ_four, Matrix.det_fin_three]
  norm_num [Fin.succAbove, Matrix.submatrix]
  ring


set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

-- Run each normalization stage only while a goal remains.
open Lean Elab Tactic in
elab "gaussian_ring" : tactic => do
  evalTactic (← `(tactic| try simp only [cadd, cmul, cpow]))
  unless (← getGoals).isEmpty do
    evalTactic (← `(tactic| ring_nf))
  unless (← getGoals).isEmpty do
    evalTactic (← `(tactic| norm_num [Complex.I_sq, Complex.I_pow_three, Complex.I_pow_four]))
  unless (← getGoals).isEmpty do
    evalTactic (← `(tactic| ring))

open Lean Elab Tactic in
elab "minor_ring" : tactic => do
  evalTactic (← `(tactic| norm_num [normalMatrix, Matrix.submatrix, cadd, cmul, cpow]))
  unless (← getGoals).isEmpty do
    evalTactic (← `(tactic| gaussian_ring))


end ValyuResearch.ElasticityMinorCertificates
