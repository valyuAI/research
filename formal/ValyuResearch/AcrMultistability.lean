import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# ACR with multistability: the two three-species examples

The mass-action vector field is built from the reaction lists of the paper, and we prove
for both examples that the positive steady states are exactly three explicit points, all
with `a = 1` (absolute concentration robustness in species A).

Not formalized here: the stability of the outer steady states (Routh-Hurwitz test on the
exact Jacobians, checked by two independent exact programs), the dimension-two theorem,
and the counting bounds.
-/

namespace ValyuResearch.AcrMultistability

/-- A reaction on three species: reactant complex, product complex, rate constant. -/
structure Rxn where
  src : ℕ × ℕ × ℕ
  dst : ℕ × ℕ × ℕ
  k : ℚ

/-- The mass-action monomial of a complex. -/
def mon (y : ℕ × ℕ × ℕ) (a b c : ℝ) : ℝ := a ^ y.1 * b ^ y.2.1 * c ^ y.2.2

/-- Net change of species A, B, C in a complex pair. -/
def dA (r : Rxn) : ℝ := ((r.dst.1 : ℤ) - r.src.1 : ℤ)
def dB (r : Rxn) : ℝ := ((r.dst.2.1 : ℤ) - r.src.2.1 : ℤ)
def dC (r : Rxn) : ℝ := ((r.dst.2.2 : ℤ) - r.src.2.2 : ℤ)

/-- The three components of the mass-action vector field. -/
def fA (R : List Rxn) (a b c : ℝ) : ℝ := (R.map fun r => (r.k : ℝ) * mon r.src a b c * dA r).sum
def fB (R : List Rxn) (a b c : ℝ) : ℝ := (R.map fun r => (r.k : ℝ) * mon r.src a b c * dB r).sum
def fC (R : List Rxn) (a b c : ℝ) : ℝ := (R.map fun r => (r.k : ℝ) * mon r.src a b c * dC r).sum

/-- Example 5.1: A+B -> 2B (2), B -> 0 (2), 0 -> A+C (60), 2C -> A+C (1),
A+C -> 2C (13), B+C -> B (2). -/
def ex1 : List Rxn :=
  [⟨(1, 1, 0), (0, 2, 0), 2⟩, ⟨(0, 1, 0), (0, 0, 0), 2⟩, ⟨(0, 0, 0), (1, 0, 1), 60⟩,
   ⟨(0, 0, 2), (1, 0, 1), 1⟩, ⟨(1, 0, 1), (0, 0, 2), 13⟩, ⟨(0, 1, 1), (0, 1, 0), 2⟩]

/-- Example 5.2: C <-> A+C (1,1), A -> A+C (6), B <-> 2B (11,1), C <-> B+C (6,6),
B+C -> B (1). -/
def ex2 : List Rxn :=
  [⟨(0, 0, 1), (1, 0, 1), 1⟩, ⟨(1, 0, 1), (0, 0, 1), 1⟩, ⟨(1, 0, 0), (1, 0, 1), 6⟩,
   ⟨(0, 1, 0), (0, 2, 0), 11⟩, ⟨(0, 2, 0), (0, 1, 0), 1⟩, ⟨(0, 1, 1), (0, 1, 0), 1⟩,
   ⟨(0, 1, 1), (0, 0, 1), 6⟩, ⟨(0, 0, 1), (0, 1, 1), 6⟩]

theorem ex1_field (a b c : ℝ) :
    fA ex1 a b c = -2 * a * b + 60 + c ^ 2 - 13 * a * c ∧
    fB ex1 a b c = 2 * b * (a - 1) ∧
    fC ex1 a b c = 60 - c ^ 2 + 13 * a * c - 2 * b * c := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [fA, fB, fC, ex1, mon, dA, dB, dC] <;> ring

theorem ex2_field (a b c : ℝ) :
    fA ex2 a b c = c * (1 - a) ∧
    fB ex2 a b c = 11 * b - b ^ 2 - 6 * b * c + 6 * c ∧
    fC ex2 a b c = 6 * a - b * c := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [fA, fB, fC, ex2, mon, dA, dB, dC] <;> ring

/-- Example 5.1: the positive steady states are exactly (1,15,3), (1,12,4), (1,10,5). -/
theorem ex1_steady_states (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    (fA ex1 a b c = 0 ∧ fB ex1 a b c = 0 ∧ fC ex1 a b c = 0) ↔
      ((a = 1 ∧ b = 15 ∧ c = 3) ∨ (a = 1 ∧ b = 12 ∧ c = 4) ∨ (a = 1 ∧ b = 10 ∧ c = 5)) := by
  obtain ⟨hfA, hfB, hfC⟩ := ex1_field a b c
  rw [hfA, hfB, hfC]
  constructor
  · rintro ⟨h1, h2, h3⟩
    have ha1 : a = 1 := by
      rcases mul_eq_zero.mp h2 with h | h
      · linarith
      · linarith
    subst ha1
    have hb' : b = (c ^ 2 - 13 * c + 60) / 2 := by linarith
    have hcub : (c - 3) * (c - 4) * (c - 5) = 0 := by
      linear_combination (-1 : ℝ) * h3 + (-2 * c) * hb'
    rcases mul_eq_zero.mp hcub with h | h
    · rcases mul_eq_zero.mp h with h | h
      · have hc3 : c = 3 := by linarith
        subst hc3
        left; exact ⟨rfl, by rw [hb']; norm_num, rfl⟩
      · have hc4 : c = 4 := by linarith
        subst hc4
        right; left; exact ⟨rfl, by rw [hb']; norm_num, rfl⟩
    · have hc5 : c = 5 := by linarith
      subst hc5
      right; right; exact ⟨rfl, by rw [hb']; norm_num, rfl⟩
  · rintro (⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩) <;> norm_num

/-- Example 5.2: the positive steady states are exactly (1,2,3), (1,3,2), (1,6,1). -/
theorem ex2_steady_states (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    (fA ex2 a b c = 0 ∧ fB ex2 a b c = 0 ∧ fC ex2 a b c = 0) ↔
      ((a = 1 ∧ b = 2 ∧ c = 3) ∨ (a = 1 ∧ b = 3 ∧ c = 2) ∨ (a = 1 ∧ b = 6 ∧ c = 1)) := by
  obtain ⟨hfA, hfB, hfC⟩ := ex2_field a b c
  rw [hfA, hfB, hfC]
  constructor
  · rintro ⟨h1, h2, h3⟩
    have ha1 : a = 1 := by
      rcases mul_eq_zero.mp h1 with h | h
      · linarith
      · linarith
    subst ha1
    have hbc : b * c = 6 := by linarith
    have hcub : (b - 2) * (b - 3) * (b - 6) = 0 := by
      linear_combination (-1 : ℝ) * b * h2 + (6 - 6 * b) * hbc
    rcases mul_eq_zero.mp hcub with h | h
    · rcases mul_eq_zero.mp h with h | h
      · have hb2 : b = 2 := by linarith
        subst hb2
        left; exact ⟨rfl, rfl, by linarith⟩
      · have hb3 : b = 3 := by linarith
        subst hb3
        right; left; exact ⟨rfl, rfl, by linarith⟩
    · have hb6 : b = 6 := by linarith
      subst hb6
      right; right; exact ⟨rfl, rfl, by linarith⟩
  · rintro (⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩ | ⟨rfl, rfl, rfl⟩) <;> norm_num

/-- ACR in A for both examples: every positive steady state has `a = 1`. -/
theorem ex1_acr (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c)
    (h : fA ex1 a b c = 0 ∧ fB ex1 a b c = 0 ∧ fC ex1 a b c = 0) : a = 1 := by
  rcases (ex1_steady_states a b c ha hb hc).mp h with h | h | h <;> exact h.1

theorem ex2_acr (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c)
    (h : fA ex2 a b c = 0 ∧ fB ex2 a b c = 0 ∧ fC ex2 a b c = 0) : a = 1 := by
  rcases (ex2_steady_states a b c ha hb hc).mp h with h | h | h <;> exact h.1

end ValyuResearch.AcrMultistability
