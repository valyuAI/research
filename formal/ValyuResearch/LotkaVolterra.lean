import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Linarith

/-!
# The local path obstruction for Lotka-Volterra tree systems

These theorems verify the algebraic obstruction used in the completeness proof.
They do not formalize the graph-theoretic support argument, classification of all
dependent triples, reconstruction of a tree, or the full linear-equivalence theorem.
-/

namespace ValyuResearch.LotkaVolterra

/-- The three pair-coefficient equations on a path force the middle sum to vanish.
The polynomial combination is beta * hUV - alpha * hVW + C * hUW. -/
theorem path_cancellation {K : Type*} [Field K]
    (pu pv pw alpha beta B C : K)
    (hpu : pu ≠ 0) (hbeta : beta ≠ 0)
    (hUV : pu * B + pv * alpha = 0)
    (hVW : pv * beta + pw * C = 0)
    (hUW : pu * beta + pw * alpha = 0) :
    B + C = 0 := by
  have hproduct : pu * beta * (B + C) = 0 := by
    linear_combination beta * hUV - alpha * hVW + C * hUW
  exact (mul_eq_zero.mp hproduct).resolve_left (mul_ne_zero hpu hbeta)

/-- Matrix-entry form of the obstruction, after using the column equalities
on the path u-v-w. The symbols vu and uw are the common entries in columns u,w. -/
theorem path_forces_middle_sum {K : Type*} [Field K]
    (pu pv pw au av aw vu uw uv wv : K)
    (hpu : pu ≠ 0) (huw : uw - aw ≠ 0)
    (hUV : pu * (uv - av) + pv * (vu - au) = 0)
    (hVW : pv * (uw - aw) + pw * (wv - av) = 0)
    (hUW : pu * (uw - aw) + pw * (vu - au) = 0) :
    uv + wv = 2 * av := by
  have hsum := path_cancellation pu pv pw (vu - au) (uw - aw)
    (uv - av) (wv - av) hpu huw hUV hVW hUW
  linear_combination hsum

/-- The generic forbidden-middle-sum condition rules out a nonzero-supported
path satisfying the Darboux pair-coefficient equations. -/
theorem no_path_coefficients {K : Type*} [Field K]
    (pu pv pw au av aw vu uw uv wv : K)
    (hpu : pu ≠ 0) (huw : uw - aw ≠ 0)
    (hgeneric : uv + wv ≠ 2 * av)
    (hUV : pu * (uv - av) + pv * (vu - au) = 0)
    (hVW : pv * (uw - aw) + pw * (wv - av) = 0)
    (hUW : pu * (uw - aw) + pw * (vu - au) = 0) :
    False := by
  exact hgeneric (path_forces_middle_sum pu pv pw au av aw vu uw uv wv
    hpu huw hUV hVW hUW)

/-- Positive off-diagonal and negative diagonal choices satisfy the two
inequalities needed for the local obstruction. Distinct component parameters
are still needed separately in the paper's graph-connectivity argument. -/
theorem positive_off_diagonal_no_path_coefficients
    (pu pv pw au av aw vu uw uv wv : ℝ)
    (hpu : pu ≠ 0)
    (hav : av < 0) (haw : aw < 0)
    (huw : 0 < uw) (huv : 0 < uv) (hwv : 0 < wv)
    (hUV : pu * (uv - av) + pv * (vu - au) = 0)
    (hVW : pv * (uw - aw) + pw * (wv - av) = 0)
    (hUW : pu * (uw - aw) + pw * (vu - au) = 0) :
    False := by
  have hdiff : uw - aw ≠ 0 := by linarith
  have hsum : uv + wv ≠ 2 * av := by linarith
  exact no_path_coefficients pu pv pw au av aw vu uw uv wv
    hpu hdiff hsum hUV hVW hUW

end ValyuResearch.LotkaVolterra

#print axioms ValyuResearch.LotkaVolterra.path_cancellation
#print axioms ValyuResearch.LotkaVolterra.path_forces_middle_sum
#print axioms ValyuResearch.LotkaVolterra.no_path_coefficients
#print axioms ValyuResearch.LotkaVolterra.positive_off_diagonal_no_path_coefficients
