import Mathlib

/-!
# Potential step for common quartets of phylogenetic trees

Lemma 2.6 of the note "Three phylogenetic trees on fourteen leaves always share a quartet"
(maths/combinatorics/phylogenetics/common-quartet-number).

For sizes `a ≤ d` of two separated leaf sets `X`, `Y`, a new tree has an edge that splits `Y` in
proportions `y ∈ [1/3, 2/3]`; `x` is the proportion of `X` on the same side. The two diagonal pairs
have sizes `(x a, (1 - y) d)` and `((1 - x) a, y d)`. With the potential
`Ψ(a, d) = min (a d) (min (2 a²) (2 d²))`, one diagonal keeps at least `3/16` of the potential.
-/

namespace ValyuResearch.CommonQuartet

/-- The potential `Ψ(a, d) = min(a d, 2 a², 2 d²)`. -/
noncomputable def psi (a d : ℝ) : ℝ := min (a * d) (min (2 * a ^ 2) (2 * d ^ 2))

/-- The potential step when the side `Z` holds at most half of the leaves in the sense `x + y ≤ 1`. -/
theorem potential_step_aux (a d x y : ℝ) (ha : 0 < a) (had : a ≤ d)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (hy0 : 1 / 3 ≤ y) (hy1 : y ≤ 2 / 3) (hxy : x + y ≤ 1) :
    3 / 16 * psi a d ≤ max (psi (x * a) ((1 - y) * d)) (psi ((1 - x) * a) (y * d)) := by
  have hd : 0 < d := lt_of_lt_of_le ha had
  -- the potential is at most `a d` and at most `2 a²`
  have hP1 : psi a d ≤ a * d := min_le_left _ _
  have hP2 : psi a d ≤ 2 * a ^ 2 := le_trans (min_le_right _ _) (min_le_left _ _)
  have hP1' : 3 / 16 * psi a d ≤ 3 / 16 * (a * d) := by linarith
  have hP2' : 3 / 16 * psi a d ≤ 3 / 16 * (2 * a ^ 2) := by linarith
  by_cases h : 7 / 16 ≤ x
  · apply le_max_of_le_left
    have h1y : x ≤ 1 - y := by linarith
    have hxa : x * a ≤ (1 - y) * d := by
      have : x * a ≤ (1 - y) * a := mul_le_mul_of_nonneg_right h1y ha.le
      have : (1 - y) * a ≤ (1 - y) * d := mul_le_mul_of_nonneg_left had (by linarith)
      linarith
    have hxa0 : 0 ≤ x * a := mul_nonneg hx0 ha.le
    have hxx : 49 / 256 ≤ x * (1 - y) := by nlinarith
    refine le_min ?_ (le_min ?_ ?_)
    · -- x a (1 - y) d ≥ (49/256) a d ≥ (3/16) a d
      have had0 : 0 ≤ a * d := mul_nonneg ha.le hd.le
      have : x * a * ((1 - y) * d) = (x * (1 - y)) * (a * d) := by ring
      nlinarith
    · -- 2 x² a² ≥ (98/256) a² ≥ (3/16)(2 a²)
      have hx2 : 49 / 256 ≤ x ^ 2 := by nlinarith
      have ha2 : 0 ≤ a ^ 2 := sq_nonneg a
      have : 2 * (x * a) ^ 2 = 2 * x ^ 2 * a ^ 2 := by ring
      nlinarith
    · -- 2 ((1 - y) d)² ≥ 2 (x a)² ≥ (3/16)(2 a²)
      have hx2 : 49 / 256 ≤ x ^ 2 := by nlinarith
      have ha2 : 0 ≤ a ^ 2 := sq_nonneg a
      have hsq : (x * a) ^ 2 ≤ ((1 - y) * d) ^ 2 := by
        exact pow_le_pow_left₀ hxa0 hxa 2
      have : 2 * (x * a) ^ 2 = 2 * x ^ 2 * a ^ 2 := by ring
      nlinarith
  · apply le_max_of_le_right
    have hx' : x < 7 / 16 := lt_of_not_ge h
    refine le_min ?_ (le_min ?_ ?_)
    · -- (1 - x) a y d ≥ (3/16) a d
      have had0 : 0 ≤ a * d := mul_nonneg ha.le hd.le
      have hc : 3 / 16 ≤ (1 - x) * y := by nlinarith
      have : (1 - x) * a * (y * d) = ((1 - x) * y) * (a * d) := by ring
      nlinarith
    · -- 2 (1 - x)² a² ≥ (3/16)(2 a²)
      have hc : 81 / 256 ≤ (1 - x) ^ 2 := by nlinarith
      have ha2 : 0 ≤ a ^ 2 := sq_nonneg a
      have : 2 * ((1 - x) * a) ^ 2 = 2 * (1 - x) ^ 2 * a ^ 2 := by ring
      nlinarith
    · -- 2 y² d² ≥ (2/9) d² ≥ (2/9) a d ≥ (3/16) a d
      have hy2 : 1 / 9 ≤ y ^ 2 := by nlinarith
      have hdd : a * d ≤ d ^ 2 := by nlinarith
      have hd2 : 0 ≤ d ^ 2 := sq_nonneg d
      have : 2 * (y * d) ^ 2 = 2 * y ^ 2 * d ^ 2 := by ring
      nlinarith

/-- **Lemma 2.6.** If `0 < a ≤ d`, `x ∈ [0,1]` and `y ∈ [1/3, 2/3]`, then one of the diagonal pairs
keeps at least `3/16` of the potential. -/
theorem potential_step (a d x y : ℝ) (ha : 0 < a) (had : a ≤ d)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (hy0 : 1 / 3 ≤ y) (hy1 : y ≤ 2 / 3) :
    3 / 16 * psi a d ≤ max (psi (x * a) ((1 - y) * d)) (psi ((1 - x) * a) (y * d)) := by
  by_cases hxy : x + y ≤ 1
  · exact potential_step_aux a d x y ha had hx0 hx1 hy0 hy1 hxy
  · -- swap the two sides of the edge: (x, y) ↦ (1 - x, 1 - y)
    have h := potential_step_aux a d (1 - x) (1 - y) ha had (by linarith) (by linarith)
      (by linarith) (by linarith) (by linarith)
    have e1 : (1 - (1 - y)) = y := by ring
    have e2 : (1 - (1 - x)) = x := by ring
    rw [e1, e2] at h
    rw [max_comm]
    exact h

/-- The sharp step with the positive root of `3 t² + t = 1`, in one orientation. -/
theorem potential_step_sharp_aux (a d x y t : ℝ) (ha : 0 < a) (had : a ≤ d)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (hy0 : 1 / 3 ≤ y) (hy1 : y ≤ 2 / 3)
    (ht0 : 1 / 3 ≤ t) (ht1 : t ≤ 1 / 2) (ht : 3 * t ^ 2 + t = 1)
    (hxy : x + y ≤ 1) :
    t ^ 2 * psi a d ≤ max (psi (x * a) ((1 - y) * d))
      (psi ((1 - x) * a) (y * d)) := by
  have hd : 0 < d := lt_of_lt_of_le ha had
  have htpos : 0 ≤ t := by linarith
  have hP1 : psi a d ≤ a * d := min_le_left _ _
  have hP2 : psi a d ≤ 2 * a ^ 2 := le_trans (min_le_right _ _) (min_le_left _ _)
  have hP1' := mul_le_mul_of_nonneg_left hP1 (sq_nonneg t)
  have hP2' := mul_le_mul_of_nonneg_left hP2 (sq_nonneg t)
  have had0 : 0 ≤ a * d := mul_nonneg ha.le hd.le
  by_cases h : t ≤ x
  · apply le_max_of_le_left
    have h1y : x ≤ 1 - y := by linarith
    have hx2 : t ^ 2 ≤ x ^ 2 := pow_le_pow_left₀ htpos h 2
    have hxx : t ^ 2 ≤ x * (1 - y) := by
      have hm := mul_le_mul_of_nonneg_left h1y hx0
      nlinarith only [hm, hx2]
    have hxa : x * a ≤ (1 - y) * d := by
      have := mul_le_mul_of_nonneg_right h1y ha.le
      have := mul_le_mul_of_nonneg_left had (show 0 ≤ 1 - y by linarith)
      linarith
    have hsq := pow_le_pow_left₀ (mul_nonneg hx0 ha.le) hxa 2
    have hprod := mul_le_mul_of_nonneg_right hxx had0
    have hsquare := mul_le_mul_of_nonneg_right hx2 (sq_nonneg a)
    refine le_min ?_ (le_min ?_ ?_)
    · nlinarith only [hP1', hprod]
    · nlinarith only [hP2', hsquare]
    · nlinarith only [hP2', hsquare, hsq]
  · apply le_max_of_le_right
    have hx' : x < t := lt_of_not_ge h
    have hxpos : 0 ≤ 1 - x := by linarith
    have hc : t ^ 2 ≤ (1 - x) * y := by
      have hm := mul_le_mul_of_nonneg_left hy0 hxpos
      nlinarith only [hm, hx', ht]
    have hs : t ^ 2 ≤ (1 - x) ^ 2 :=
      pow_le_pow_left₀ htpos (by linarith) 2
    have hprod := mul_le_mul_of_nonneg_right hc had0
    have hsquare := mul_le_mul_of_nonneg_right hs (sq_nonneg a)
    refine le_min ?_ (le_min ?_ ?_)
    · nlinarith only [hP1', hprod]
    · nlinarith only [hP2', hsquare]
    · have hy2 : 1 / 9 ≤ y ^ 2 := by nlinarith
      have hdd : a * d ≤ d ^ 2 := by nlinarith
      have hc2 : t ^ 2 ≤ 2 / 9 := by nlinarith
      have hsmall := mul_le_mul_of_nonneg_right hc2 had0
      have hlarge := mul_le_mul_of_nonneg_right hy2 (sq_nonneg d)
      nlinarith only [hP1', hsmall, hlarge, hdd]

/-- **Sharp version of Lemma 2.6.** Only the real-variable inequality is formalised. -/
theorem potential_step_sharp (a d x y : ℝ) (ha : 0 < a) (had : a ≤ d)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1) (hy0 : 1 / 3 ≤ y) (hy1 : y ≤ 2 / 3) :
    (7 - Real.sqrt 13) / 18 * psi a d ≤
      max (psi (x * a) ((1 - y) * d)) (psi ((1 - x) * a) (y * d)) := by
  let t : ℝ := (Real.sqrt 13 - 1) / 6
  have hs : (Real.sqrt 13) ^ 2 = 13 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 ≤ Real.sqrt 13 := Real.sqrt_nonneg _
  have ht0 : 1 / 3 ≤ t := by dsimp [t]; nlinarith only [hs, hs0]
  have ht1 : t ≤ 1 / 2 := by dsimp [t]; nlinarith only [hs, hs0]
  have ht : 3 * t ^ 2 + t = 1 := by dsimp [t]; nlinarith only [hs, hs0]
  have hc : t ^ 2 = (7 - Real.sqrt 13) / 18 := by dsimp [t]; nlinarith only [hs, hs0]
  rw [← hc]
  by_cases hxy : x + y ≤ 1
  · exact potential_step_sharp_aux a d x y t ha had hx0 hx1 hy0 hy1 ht0 ht1 ht hxy
  · have h := potential_step_sharp_aux a d (1 - x) (1 - y) t ha had
      (by linarith) (by linarith) (by linarith) (by linarith) ht0 ht1 ht (by linarith)
    have e1 : 1 - (1 - y) = y := by ring
    have e2 : 1 - (1 - x) = x := by ring
    rw [e1, e2, max_comm] at h
    exact h

/-- Equality in the sharp real-variable inequality. The fraction `t` is irrational. -/
theorem potential_step_sharp_witness :
    let t : ℝ := (Real.sqrt 13 - 1) / 6
    max (psi t (4 / 3)) (psi (1 - t) (2 / 3)) =
      (7 - Real.sqrt 13) / 18 * psi 1 2 := by
  dsimp only
  let t : ℝ := (Real.sqrt 13 - 1) / 6
  change max (psi t (4 / 3)) (psi (1 - t) (2 / 3)) = _
  have hs : (Real.sqrt 13) ^ 2 = 13 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 ≤ Real.sqrt 13 := Real.sqrt_nonneg _
  have ht0 : 1 / 3 ≤ t := by dsimp [t]; nlinarith only [hs, hs0]
  have ht1 : t ≤ 1 / 2 := by dsimp [t]; nlinarith only [hs, hs0]
  have ht : 3 * t ^ 2 + t = 1 := by dsimp [t]; nlinarith only [hs]
  have hc : t ^ 2 = (7 - Real.sqrt 13) / 18 := by dsimp [t]; nlinarith only [hs]
  have hleft : psi t (4 / 3) = 2 * t ^ 2 := by
    unfold psi
    rw [min_eq_left (show 2 * t ^ 2 ≤ 2 * (4 / 3 : ℝ) ^ 2 by nlinarith only [ht0, ht])]
    exact min_eq_right (by nlinarith only [ht0, ht])
  have hright : psi (1 - t) (2 / 3) = 2 * t ^ 2 := by
    unfold psi
    have hp : (1 - t) * (2 / 3) = 2 * t ^ 2 := by nlinarith only [ht]
    rw [hp]
    apply min_eq_left
    apply le_min
    · nlinarith only [ht1]
    · nlinarith only [ht0, ht]
  rw [hleft, hright, max_self, hc]
  norm_num [psi]
  ring

end ValyuResearch.CommonQuartet
