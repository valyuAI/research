import Mathlib.Algebra.BigOperators.Field
import Mathlib.Basic.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# A finite symmetric-kernel certificate for renewal restarting

This file proves the finite algebraic gap identity and global minimum used in
the resetting argument. It does not formalize Brownian motion, renewal theory,
the Green-operator representation, or injectivity of the waiting-law transform.
-/

namespace ValyuResearch.Resetting

open scoped BigOperators

variable {ι : Type*} [Fintype ι]

/-- The unnormalized finite positive-kernel objective. -/
noncomputable def kernelCost (K : ι → ι → ℝ) (u v : ι → ℝ) : ℝ :=
  ∑ i, ∑ j, K i j * (u i) ^ 2 * v j / v i

/-- The reference quadratic form. -/
def kernelBaseline (K : ι → ι → ℝ) (u : ι → ℝ) : ℝ :=
  ∑ i, ∑ j, K i j * u i * u j

/-- The exact nonnegative gap, before dividing by two or by a prior normalizer. -/
noncomputable def kernelGap (K : ι → ι → ℝ) (u v : ι → ℝ) : ℝ :=
  ∑ i, ∑ j, K i j * (u i * v j - u j * v i) ^ 2 / (v i * v j)

/-- The double-sum cost equals the squared-prior weighted kernel ratio. -/
theorem kernelCost_eq_ratio (K : ι → ι → ℝ) (u v : ι → ℝ) :
    kernelCost K u v = ∑ i, (u i) ^ 2 * ((∑ j, K i j * v j) / v i) := by
  unfold kernelCost
  apply Finset.sum_congr rfl
  intro i hi
  rw [Finset.sum_div, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  ring

theorem pair_gap (a u v x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) :
    a * u ^ 2 * y / x + a * v ^ 2 * x / y - 2 * (a * u * v) =
      a * (u * y - v * x) ^ 2 / (x * y) := by
  field_simp [hx, hy]
  ring

/-- Symmetry gives an exact gap identity for every nonzero competitor vector. -/
theorem kernel_gap_identity (K : ι → ι → ℝ) (u v : ι → ℝ)
    (hK : ∀ i j, K i j = K j i) (hv : ∀ i, v i ≠ 0) :
    2 * (kernelCost K u v - kernelBaseline K u) = kernelGap K u v := by
  have hswap :
      (∑ i, ∑ j, K i j * (u j) ^ 2 * v i / v j) = kernelCost K u v := by
    rw [Finset.sum_comm]
    unfold kernelCost
    apply Finset.sum_congr rfl
    intro i hi
    apply Finset.sum_congr rfl
    intro j hj
    rw [hK j i]
  have hsum :
      (∑ i, ∑ j,
        (K i j * (u i) ^ 2 * v j / v i +
          K i j * (u j) ^ 2 * v i / v j -
          2 * (K i j * u i * u j))) = kernelGap K u v := by
    unfold kernelGap
    apply Finset.sum_congr rfl
    intro i hi
    apply Finset.sum_congr rfl
    intro j hj
    exact pair_gap (K i j) (u i) (u j) (v i) (v j) (hv i) (hv j)
  simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib,
    ← Finset.mul_sum] at hsum
  change kernelCost K u v +
    (∑ i, ∑ j, K i j * (u j) ^ 2 * v i / v j) -
    2 * kernelBaseline K u = kernelGap K u v at hsum
  rw [hswap] at hsum
  linarith

theorem kernel_gap_nonnegative (K : ι → ι → ℝ) (u v : ι → ℝ)
    (hK : ∀ i j, 0 ≤ K i j) (hv : ∀ i, 0 < v i) :
    0 ≤ kernelGap K u v := by
  unfold kernelGap
  apply Finset.sum_nonneg
  intro i hi
  apply Finset.sum_nonneg
  intro j hj
  exact div_nonneg (mul_nonneg (hK i j) (sq_nonneg _))
    (le_of_lt (mul_pos (hv i) (hv j)))

theorem kernel_baseline_le_cost (K : ι → ι → ℝ) (u v : ι → ℝ)
    (hsymm : ∀ i j, K i j = K j i)
    (hK : ∀ i j, 0 ≤ K i j) (hv : ∀ i, 0 < v i) :
    kernelBaseline K u ≤ kernelCost K u v := by
  have hidentity := kernel_gap_identity K u v hsymm (fun i => ne_of_gt (hv i))
  have hnonneg := kernel_gap_nonnegative K u v hK hv
  linarith

theorem kernel_self_cost (K : ι → ι → ℝ) (u : ι → ℝ)
    (hu : ∀ i, u i ≠ 0) :
    kernelCost K u u = kernelBaseline K u := by
  unfold kernelCost kernelBaseline
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  field_simp [hu i]

/-- Every positive reference vector is globally optimal for its squared prior. -/
theorem kernel_global_minimum (K : ι → ι → ℝ) (u v : ι → ℝ)
    (hsymm : ∀ i j, K i j = K j i)
    (hK : ∀ i j, 0 ≤ K i j)
    (hu : ∀ i, 0 < u i) (hv : ∀ i, 0 < v i) :
    kernelCost K u u ≤ kernelCost K u v := by
  rw [kernel_self_cost K u (fun i => ne_of_gt (hu i))]
  exact kernel_baseline_le_cost K u v hsymm hK hv

/-!
## Exact three-state failure certificate

These rational identities verify the generator, Green matrix, success and
duration vectors, squared-success weights, and strict objective decrease.
The probabilistic interpretation of the resolvent is outside this file.
-/

def exampleQ : Matrix (Fin 3) (Fin 3) ℚ :=
  !![-2, 1, 0; 0, -3, 1; 1, 0, -4]

def exampleG : Matrix (Fin 3) (Fin 3) ℚ :=
  !![12 / 23, 4 / 23, 1 / 23;
    1 / 23, 8 / 23, 2 / 23;
    3 / 23, 1 / 23, 6 / 23]

def referenceSuccess : Fin 3 → ℚ := ![33 / 59, 40 / 59, 42 / 59]
def referenceDuration : Fin 3 → ℚ := ![26 / 59, 19 / 59, 17 / 59]
def competitorSuccess : Fin 3 → ℚ := ![31910 / 54419, 38120 / 54419, 39830 / 54419]
def competitorDuration : Fin 3 → ℚ := ![25010 / 54419, 18110 / 54419, 16210 / 54419]
def exampleWeights : Fin 3 → ℚ := ![1089 / 4453, 1600 / 4453, 1764 / 4453]

def exampleCost (f h : Fin 3 → ℚ) : ℚ :=
  ∑ i, exampleWeights i * h i / f i

theorem example_green_inverse : (-exampleQ) * exampleG = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [exampleQ, exampleG, Matrix.mul_apply, Fin.sum_univ_succ]

theorem example_nonsymmetric : exampleG 0 1 ≠ exampleG 1 0 := by
  norm_num [exampleG]

theorem reference_green_identity :
    exampleG.mulVec referenceSuccess = referenceDuration := by
  ext i
  fin_cases i <;>
    norm_num [exampleG, referenceSuccess, referenceDuration,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ]

theorem competitor_green_identity :
    exampleG.mulVec competitorSuccess = competitorDuration := by
  ext i
  fin_cases i <;>
    norm_num [exampleG, competitorSuccess, competitorDuration,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ]

theorem reference_resolvent_identity :
    ((1 : Matrix (Fin 3) (Fin 3) ℚ) - exampleQ).mulVec referenceDuration =
      fun _ => 1 := by
  ext i
  fin_cases i <;>
    norm_num [exampleQ, referenceDuration, Matrix.mulVec, Matrix.one_apply, dotProduct,
      Fin.sum_univ_succ]

theorem competitor_resolvent_identity :
    (((9 / 10 : ℚ) • (1 : Matrix (Fin 3) (Fin 3) ℚ)) - exampleQ).mulVec
      competitorDuration = fun _ => 1 := by
  ext i
  fin_cases i <;>
    norm_num [exampleQ, competitorDuration, Matrix.mulVec, Matrix.one_apply, dotProduct,
      Fin.sum_univ_succ]

theorem reference_success_identity (i : Fin 3) :
    referenceSuccess i = 1 - referenceDuration i := by
  fin_cases i <;> norm_num [referenceSuccess, referenceDuration]

theorem competitor_success_identity (i : Fin 3) :
    competitorSuccess i = 1 - (9 / 10 : ℚ) * competitorDuration i := by
  fin_cases i <;> norm_num [competitorSuccess, competitorDuration]

theorem example_squared_weights (i : Fin 3) :
    exampleWeights i = referenceSuccess i ^ 2 / (∑ j, referenceSuccess j ^ 2) := by
  fin_cases i <;> norm_num [exampleWeights, referenceSuccess, Fin.sum_univ_succ]

theorem example_weights_sum : (∑ i, exampleWeights i) = 1 := by
  norm_num [exampleWeights, Fin.sum_univ_succ]

theorem example_reference_cost :
    exampleCost referenceSuccess referenceDuration = 2332 / 4453 := by
  norm_num [exampleCost, exampleWeights, referenceSuccess, referenceDuration,
    Fin.sum_univ_succ]

theorem example_strict_improvement :
    exampleCost competitorSuccess competitorDuration -
      exampleCost referenceSuccess referenceDuration =
        -(761111595 / 7705213313411 : ℚ) := by
  norm_num [exampleCost, exampleWeights, referenceSuccess, referenceDuration,
    competitorSuccess, competitorDuration, Fin.sum_univ_succ]

theorem example_competitor_better :
    exampleCost competitorSuccess competitorDuration <
      exampleCost referenceSuccess referenceDuration := by
  have h := example_strict_improvement
  linarith

end ValyuResearch.Resetting
