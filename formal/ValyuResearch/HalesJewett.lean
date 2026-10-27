import Mathlib.Algebra.Field.ZMod
import Mathlib.Data.Fintype.Card
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Push

/-!
# Prime-successor off-diagonal Hales-Jewett numbers

The blue class is the zero-sum word together with words whose coordinate
sum is greater than one and congruent to one modulo the prime.
-/

namespace ValyuResearch.HalesJewett

def blue (p s : ℕ) : Prop := s = 0 ∨ (s % p = 1 ∧ 1 < s)

theorem no_blue_gap {p d : ℕ} (hd0 : 0 < d) (hdp : d < p) (x : ℕ) :
    ¬ (blue p x ∧ blue p (x + d)) := by
  rintro ⟨hx, hy⟩
  rcases hx with hx | ⟨hxmod, hxgt⟩
  · subst x
    rcases hy with hy | ⟨hymod, hygt⟩
    · simp at hy
      omega
    · simp only [Nat.zero_add] at hymod hygt
      rw [Nat.mod_eq_of_lt hdp] at hymod
      omega
  · rcases hy with hy | ⟨hymod, _⟩
    · omega
    · have hmod : (1 + d) % p = 1 := by
        simpa [Nat.add_mod, hxmod, Nat.mod_eq_of_lt hdp] using hymod
      by_cases hlt : 1 + d < p
      · rw [Nat.mod_eq_of_lt hlt] at hmod
        omega
      · have heq : 1 + d = p := by omega
        rw [heq, Nat.mod_self] at hmod
        omega

theorem blue_multiple_iff {p : ℕ} (hp : 2 ≤ p) (a : ℕ) :
    blue p (p * a) ↔ a = 0 := by
  have hp0 : p ≠ 0 := by omega
  simp [blue, hp0]

theorem line_no_blue_adjacent {p d S : ℕ} (hp : 2 ≤ p)
    (hd0 : 0 < d) (hdp : d ≤ p) (hmax : d = p → S = 0) (a : ℕ) :
    ¬ (blue p (S + d * a) ∧ blue p (S + d * (a + 1))) := by
  by_cases hd : d = p
  · subst d
    have hs : S = 0 := hmax rfl
    subst S
    simp only [Nat.zero_add, blue_multiple_iff hp]
    omega
  · have hlt : d < p := by omega
    have h := no_blue_gap hd0 hlt (S + d * a)
    simpa [Nat.mul_add, Nat.add_assoc] using h

theorem residue_one {p d : ℕ} (hp : p.Prime) (hd0 : 0 < d)
    (hdp : d < p) (S : ℕ) : ∃ a < p, (S + d * a) % p = 1 := by
  let _ : Fact p.Prime := ⟨hp⟩
  let _ : NeZero p := ⟨hp.ne_zero⟩
  have hd : (d : ZMod p) ≠ 0 := by
    intro h
    have hv := congrArg ZMod.val h
    have : d = 0 := by
      simpa [ZMod.val_natCast_of_lt hdp] using hv
    omega
  let a : ZMod p := (d : ZMod p)⁻¹ * (1 - (S : ZMod p))
  have hz : (S : ZMod p) + (d : ZMod p) * a = 1 := by
    dsimp [a]
    rw [← mul_assoc, mul_inv_cancel₀ hd, one_mul]
    ring
  have hcast : ((S + d * a.val : ℕ) : ZMod p) = (1 : ZMod p) := by
    push_cast
    rw [ZMod.natCast_zmod_val]
    exact hz
  have hmod := (ZMod.natCast_eq_natCast_iff' (S + d * a.val) 1 p).mp
    (by simpa only [Nat.cast_one] using hcast)
  refine ⟨a.val, ZMod.val_lt a, ?_⟩
  simpa [Nat.mod_eq_of_lt hp.one_lt] using hmod

theorem line_contains_blue {p d S : ℕ} (hp : p.Prime)
    (hd0 : 0 < d) (hdp : d ≤ p) (hmax : d = p → S = 0) :
    ∃ a ≤ p, blue p (S + d * a) := by
  by_cases hd : d = p
  · have hs : S = 0 := hmax hd
    exact ⟨0, Nat.zero_le _, Or.inl (by simp [hs])⟩
  · have hlt : d < p := by omega
    obtain ⟨a, hap, hmod⟩ := residue_one hp hd0 hlt S
    by_cases hgt : 1 < S + d * a
    · exact ⟨a, Nat.le_of_lt hap, Or.inr ⟨hmod, hgt⟩⟩
    · have hsum : S + d * a = 1 := by
        have hne : S + d * a ≠ 0 := by
          intro hz
          simp [hz] at hmod
        omega
      by_cases ha : a = 0
      · have hs : S = 1 := by simpa [ha] using hsum
        refine ⟨p, le_rfl, Or.inr ⟨?_, ?_⟩⟩
        · simp [hs, Nat.add_mod, Nat.mod_eq_of_lt hp.one_lt]
        · have hp0 : 0 < p := hp.pos
          have hprod : 0 < d * p := Nat.mul_pos hd0 hp0
          omega
      · have ha0 : 0 < a := by omega
        have hprod : 0 < d * a := Nat.mul_pos hd0 ha0
        have hs : S = 0 := by omega
        exact ⟨0, Nat.zero_le _, Or.inl (by simp [hs])⟩

abbrev Word (k n : ℕ) := Fin n → Fin k

def linePoint {k n : ℕ} (s : Finset (Fin n)) (w : Word k n) (a : Fin k) : Word k n :=
  fun i => if i ∈ s then a else w i

def wordSum {k n : ℕ} (w : Word k n) : ℕ := ∑ i, (w i).val

def fixedSum {k n : ℕ} (s : Finset (Fin n)) (w : Word k n) : ℕ :=
  ∑ i ∈ sᶜ, (w i).val

theorem sum_linePoint {k n : ℕ} (s : Finset (Fin n)) (w : Word k n) (a : Fin k) :
    wordSum (linePoint s w a) = fixedSum s w + s.card * a.val := by
  unfold wordSum linePoint fixedSum
  rw [← Finset.sum_add_sum_compl s]
  have hleft : (∑ i ∈ s, (if i ∈ s then a else w i).val) = s.card * a.val := by
    calc
      (∑ i ∈ s, (if i ∈ s then a else w i).val) = ∑ _i ∈ s, a.val := by
        apply Finset.sum_congr rfl
        intro i hi
        simp [hi]
      _ = s.card * a.val := by simp
  have hright : (∑ i ∈ sᶜ, (if i ∈ s then a else w i).val) =
      ∑ i ∈ sᶜ, (w i).val := by
    apply Finset.sum_congr rfl
    intro i hi
    simp [Finset.mem_compl.mp hi]
  rw [hleft, hright, Nat.add_comm]

def Avoids {k n : ℕ} (B : Word k n → Prop) : Prop :=
  (∀ (s : Finset (Fin n)), s.Nonempty → ∀ w, ∃ a, B (linePoint s w a)) ∧
  (∀ (s : Finset (Fin n)), s.Nonempty → ∀ w (a b : Fin k),
    b.val = a.val + 1 → ¬ (B (linePoint s w a) ∧ B (linePoint s w b)))

def Forces (k n : ℕ) : Prop := ∀ B : Word k n → Prop, ¬ Avoids B

theorem prime_coloring_avoids_of_le {p k n : ℕ} (hp : p.Prime) (hpk : p < k)
    (hnp : n ≤ p) : Avoids (fun w : Word k n => blue p (wordSum w)) := by
  have hcardn (s : Finset (Fin n)) : s.card ≤ n := by
    simpa using s.card_le_univ
  have hcard (s : Finset (Fin n)) : s.card ≤ p := le_trans (hcardn s) hnp
  have hmax (s : Finset (Fin n)) (w : Word k n) (hs : s.card = p) :
      fixedSum s w = 0 := by
    have hcn : s.card = n := by have := hcardn s; omega
    have heq : s = Finset.univ := s.eq_univ_of_card (by simpa using hcn)
    simp [fixedSum, heq]
  constructor
  · intro s hs w
    obtain ⟨a, hap, ha⟩ := line_contains_blue hp (Finset.card_pos.mpr hs)
      (hcard s) (hmax s w)
    refine ⟨⟨a, by omega⟩, ?_⟩
    dsimp only
    rw [sum_linePoint]
    exact ha
  · intro s hs w a b hab
    dsimp only
    rw [sum_linePoint, sum_linePoint, hab]
    exact line_no_blue_adjacent hp.two_le (Finset.card_pos.mpr hs)
      (hcard s) (hmax s w) a.val

theorem prime_coloring_avoids {p k : ℕ} (hp : p.Prime) (hpk : p < k) :
    Avoids (fun w : Word k p => blue p (wordSum w)) :=
  prime_coloring_avoids_of_le hp hpk le_rfl

theorem not_forces_of_le_prime {p k n : ℕ} (hp : p.Prime) (hpk : p < k)
    (hnp : n ≤ p) : ¬ Forces k n := by
  intro h
  exact h _ (prime_coloring_avoids_of_le hp hpk hnp)

theorem not_forces_prime_dimension {p k : ℕ} (hp : p.Prime) (hpk : p < k) :
    ¬ Forces k p := by
  intro h
  exact h _ (prime_coloring_avoids hp hpk)

def Consecutive {k n : ℕ} (x y : Word k n) : Prop :=
  ∃ a b : Fin k, b.val = a.val + 1 ∧ x ≠ y ∧
    ∀ i, x i = y i ∨ (x i = a ∧ y i = b)

theorem avoids_no_consecutive {k n : ℕ} {B : Word k n → Prop}
    (hB : Avoids B) {x y : Word k n} (hxy : Consecutive x y) :
    ¬ (B x ∧ B y) := by
  classical
  obtain ⟨a, b, hab, hne, hcoord⟩ := hxy
  let s : Finset (Fin n) := Finset.univ.filter (fun i => x i ≠ y i)
  obtain ⟨i, hi⟩ := Function.ne_iff.mp hne
  have hs : s.Nonempty := ⟨i, by simp [s, hi]⟩
  have hleft : linePoint s x a = x := by
    funext j
    by_cases hj : x j = y j
    · simp [linePoint, s, hj]
    · have h := (hcoord j).resolve_left hj
      simp [linePoint, s, h.1]
  have hright : linePoint s x b = y := by
    funext j
    by_cases hj : x j = y j
    · simp [linePoint, s, hj]
    · have h := (hcoord j).resolve_left hj
      simp [linePoint, s, h.2]
  have h := hB.2 s hs x a b hab
  simpa [hleft, hright] using h

def chainPoint {k : ℕ} (a b i z : Fin k) : Word k k :=
  fun t => if t.val = k - 1 then z else if t.val < i.val then b else a

theorem chain_consecutive {k : ℕ} {a b : Fin k} (hab : b.val = a.val + 1)
    (i j z : Fin k) (hij : i.val < j.val) :
    Consecutive (chainPoint a b i z) (chainPoint a b j z) := by
  have hne : a ≠ b := by
    intro h
    have := congrArg Fin.val h
    omega
  refine ⟨a, b, hab, ?_, ?_⟩
  · intro h
    have hi : i.val ≠ k - 1 := by have := j.isLt; omega
    have hval := congrArg (fun w : Word k k => w i) h
    have : a = b := by simpa [chainPoint, hi, hij] using hval
    exact hne this
  · intro t
    by_cases ht : t.val = k - 1
    · exact Or.inl (by simp [chainPoint, ht])
    · by_cases hti : t.val < i.val
      · have htj : t.val < j.val := lt_trans hti hij
        exact Or.inl (by simp [chainPoint, ht, hti, htj])
      · by_cases htj : t.val < j.val
        · exact Or.inr ⟨by simp [chainPoint, ht, hti], by simp [chainPoint, ht, htj]⟩
        · exact Or.inl (by simp [chainPoint, ht, hti, htj])

theorem constant_to_chain {k : ℕ} {a b : Fin k} (hab : b.val = a.val + 1)
    (i : Fin k) : Consecutive (fun _ => a) (chainPoint a b i b) := by
  have hk : 0 < k := by have := b.isLt; omega
  let last : Fin k := ⟨k - 1, by omega⟩
  have hne : a ≠ b := by intro h; have := congrArg Fin.val h; omega
  refine ⟨a, b, hab, ?_, ?_⟩
  · intro h
    have hval := congrArg (fun w : Word k k => w last) h
    exact hne (by simpa [chainPoint, last] using hval)
  · intro t
    by_cases ht : t.val = k - 1
    · exact Or.inr ⟨rfl, by simp [chainPoint, ht]⟩
    · by_cases hti : t.val < i.val
      · exact Or.inr ⟨rfl, by simp [chainPoint, ht, hti]⟩
      · exact Or.inl (by simp [chainPoint, ht, hti])

theorem chain_to_constant {k : ℕ} {a b : Fin k} (hab : b.val = a.val + 1)
    (i : Fin k) : Consecutive (chainPoint a b i a) (fun _ => b) := by
  have hk : 0 < k := by have := b.isLt; omega
  let last : Fin k := ⟨k - 1, by omega⟩
  have hne : a ≠ b := by intro h; have := congrArg Fin.val h; omega
  refine ⟨a, b, hab, ?_, ?_⟩
  · intro h
    have hval := congrArg (fun w : Word k k => w last) h
    exact hne (by simpa [chainPoint, last] using hval)
  · intro t
    by_cases ht : t.val = k - 1
    · exact Or.inr ⟨by simp [chainPoint, ht], rfl⟩
    · by_cases hti : t.val < i.val
      · exact Or.inl (by simp [chainPoint, ht, hti])
      · exact Or.inr ⟨by simp [chainPoint, ht, hti], rfl⟩

theorem chain_blue_completions {k : ℕ} {B : Word k k → Prop} (hB : Avoids B)
    (a b i : Fin k) : ∃ z, B (chainPoint a b i z) := by
  have hk : 0 < k := by have := a.isLt; omega
  let last : Fin k := ⟨k - 1, by omega⟩
  obtain ⟨z, hz⟩ := hB.1 {last} (by simp) (chainPoint a b i a)
  refine ⟨z, ?_⟩
  have heq : linePoint {last} (chainPoint a b i a) z = chainPoint a b i z := by
    funext t
    by_cases ht : t = last
    · subst t
      simp [linePoint, chainPoint, last]
    · have htval : t.val ≠ k - 1 := by
        intro h
        apply ht
        exact Fin.ext h
      simp [linePoint, chainPoint, ht, htval]
  rwa [heq] at hz

theorem chain_blue_surjective {k : ℕ} {B : Word k k → Prop} (hB : Avoids B)
    {a b : Fin k} (hab : b.val = a.val + 1) :
    ∀ z, ∃ i, B (chainPoint a b i z) := by
  classical
  choose f hf using chain_blue_completions hB a b
  have hinj : Function.Injective f := by
    intro i j hsame
    by_contra hne
    have hneval : i.val ≠ j.val := by intro h; exact hne (Fin.ext h)
    by_cases hij : i.val < j.val
    · apply avoids_no_consecutive hB (chain_consecutive hab i j (f i) hij)
      exact ⟨hf i, by simpa [hsame] using hf j⟩
    · have hji : j.val < i.val := by omega
      apply avoids_no_consecutive hB (chain_consecutive hab j i (f j) hji)
      exact ⟨hf j, by simpa [hsame] using hf i⟩
  intro z
  obtain ⟨i, hi⟩ := Finite.surjective_of_injective hinj z
  exact ⟨i, by simpa [hi] using hf i⟩

theorem forces_self {k : ℕ} (hk : 2 ≤ k) : Forces k k := by
  classical
  intro B hB
  let zero : Fin k := ⟨0, by omega⟩
  obtain ⟨c, hc⟩ := hB.1 Finset.univ ⟨zero, Finset.mem_univ _⟩ (fun _ => zero)
  have heq : linePoint Finset.univ (fun _ : Fin k => zero) c = (fun _ => c) := by
    funext i
    simp [linePoint]
  have hc' : B (fun _ => c) := by rwa [heq] at hc
  by_cases hcnext : c.val + 1 < k
  · let b : Fin k := ⟨c.val + 1, hcnext⟩
    obtain ⟨i, hi⟩ := chain_blue_surjective hB (a := c) (b := b) rfl b
    exact avoids_no_consecutive hB (constant_to_chain (a := c) (b := b) rfl i) ⟨hc', hi⟩
  · have hclast : c.val = k - 1 := by have := c.isLt; omega
    let a : Fin k := ⟨k - 2, by omega⟩
    have hab : c.val = a.val + 1 := by dsimp [a]; omega
    obtain ⟨i, hi⟩ := chain_blue_surjective hB hab a
    exact avoids_no_consecutive hB (chain_to_constant hab i) ⟨hi, hc'⟩

noncomputable def HJ (k : ℕ) : ℕ := by
  classical
  exact if hk : 2 ≤ k then Nat.find (⟨k, forces_self hk⟩ : ∃ n, Forces k n) else 0

theorem forces_HJ {k : ℕ} (hk : 2 ≤ k) : Forces k (HJ k) := by
  classical
  unfold HJ
  rw [dite_eq_left hk]
  exact Nat.find_spec (⟨k, forces_self hk⟩ : ∃ n, Forces k n)

theorem HJ_le_self {k : ℕ} (hk : 2 ≤ k) : HJ k ≤ k := by
  classical
  unfold HJ
  rw [dite_eq_left hk]
  exact Nat.find_min' (⟨k, forces_self hk⟩ : ∃ n, Forces k n) (forces_self hk)

theorem prime_lower_bound {p k : ℕ} (hp : p.Prime) (hpk : p < k) :
    p + 1 ≤ HJ k := by
  have hk : 2 ≤ k := by have := hp.two_le; omega
  by_contra h
  have hnp : HJ k ≤ p := by omega
  exact not_forces_of_le_prime hp hpk hnp (forces_HJ hk)

theorem HJ_prime_successor {p : ℕ} (hp : p.Prime) : HJ (p + 1) = p + 1 := by
  have hk : 2 ≤ p + 1 := by have := hp.two_le; omega
  exact Nat.le_antisymm (HJ_le_self hk) (prime_lower_bound hp (by omega))

theorem HJ_eight : HJ 8 = 8 := by
  exact HJ_prime_successor (by decide : Nat.Prime 7)

theorem HJ_twelve : HJ 12 = 12 := by
  exact HJ_prime_successor (by decide : Nat.Prime 11)

end ValyuResearch.HalesJewett
