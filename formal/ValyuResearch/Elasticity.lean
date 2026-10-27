import Mathlib.LinearAlgebra.Matrix.Adjugate
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic.Ring
import Mathlib.Tactic.LinearCombination

/-!
Exact matrix identities underlying the elastic collision reduction.

This file does not formalize the algebraic-geometric dimension argument,
Borel fixed points, determinantal certificates, or the generic recovery theorem.
-/

namespace ValyuResearch.ExploratoryElasticity

open Matrix

variable {K : Type*} [Field K]

abbrev Mat3 (K : Type*) := Matrix (Fin 3) (Fin 3) K

def secondCoefficient (A : Mat3 K) : K :=
  A 0 0 * A 1 1 - A 0 1 * A 1 0 +
  A 0 0 * A 2 2 - A 0 2 * A 2 0 +
  A 1 1 * A 2 2 - A 1 2 * A 2 1

theorem second_coefficient_difference (X H : Mat3 K) :
    secondCoefficient (X + H) - secondCoefficient (X - H) =
      2 * (trace X * trace H - trace (X * H)) := by
  simp [secondCoefficient, trace, diag, mul_apply, Fin.sum_univ_succ]
  ring

theorem determinant_difference (X H : Mat3 K) :
    det (X + H) - det (X - H) =
      2 * (trace (adjugate X * H) + det H) := by
  simp [det_fin_three, adjugate_fin_three, trace, diag, mul_apply, Fin.sum_univ_succ]
  ring

theorem characteristic_expansion (A : Mat3 K) (t : K) :
    det (A - t • (1 : Mat3 K)) =
      det A - secondCoefficient A * t + trace A * t^2 - t^3 := by
  simp [det_fin_three, secondCoefficient, trace, diag, Fin.sum_univ_succ,
    Matrix.sub_apply, Matrix.smul_apply]
  ring

variable [CharZero K]

theorem trace_collision (X H : Mat3 K)
    (h : trace (X + H) = trace (X - H)) : trace H = 0 := by
  rw [trace_add, trace_sub] at h
  linear_combination (1 / 2 : K) * h

theorem quadratic_collision (X H : Mat3 K)
    (ht : trace (X + H) = trace (X - H))
    (hq : secondCoefficient (X + H) = secondCoefficient (X - H)) :
    trace (X * H) = 0 := by
  have hH := trace_collision X H ht
  have hid := second_coefficient_difference X H
  rw [hq, sub_self, hH, mul_zero, zero_sub] at hid
  linear_combination (1 / 2 : K) * hid

theorem cubic_collision (X H : Mat3 K)
    (hd : det (X + H) = det (X - H)) :
    trace (adjugate X * H) + det H = 0 := by
  have hid := determinant_difference X H
  rw [hd, sub_self] at hid
  linear_combination -(1 / 2 : K) * hid

theorem coefficient_collision_iff (X H : Mat3 K) :
    (trace (X + H) = trace (X - H) ∧
      secondCoefficient (X + H) = secondCoefficient (X - H) ∧
      det (X + H) = det (X - H)) ↔
    (trace H = 0 ∧ trace (X * H) = 0 ∧
      trace (adjugate X * H) + det H = 0) := by
  constructor
  · rintro ⟨ht, hq, hd⟩
    exact ⟨trace_collision X H ht, quadratic_collision X H ht hq,
      cubic_collision X H hd⟩
  · rintro ⟨ht, hq, hd⟩
    refine ⟨?_, ?_, ?_⟩
    · simp [trace_add, trace_sub, ht]
    · apply sub_eq_zero.mp
      rw [second_coefficient_difference, ht, hq]
      ring
    · apply sub_eq_zero.mp
      rw [determinant_difference, hd, mul_zero]

#print axioms second_coefficient_difference
#print axioms determinant_difference
#print axioms characteristic_expansion
#print axioms trace_collision
#print axioms quadratic_collision
#print axioms cubic_collision
#print axioms coefficient_collision_iff

end ValyuResearch.ExploratoryElasticity
