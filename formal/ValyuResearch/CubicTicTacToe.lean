import Mathlib

/-!
# Hall surplus certificates for pairing strategies

Slots `ι` (two per surviving winning line) must be matched injectively to free cells `α`,
slot `i` only to cells of `t i`. The computation for 7^3 tic-tac-toe checks, for each
configuration, the replication condition `ReplicationOK t d`: for every slot `i₀`, the slot
graph with `d` extra copies of `i₀` still has a slot-saturating matching.

* `surplus_of_replication`: replication implies Hall surplus `|N(s)| ≥ |s| + d` for every
  nonempty slot set `s`.
* `matching_avoiding`: Hall surplus `d` implies that, after deleting any set `D` of at most `d`
  cells (the unknown later Maker moves), a slot-saturating matching avoiding `D` exists.
* `pairing_of_replication`: the composition used in the paper.
-/

open Finset

namespace CubicTicTacToe

variable {ι α : Type*} [DecidableEq α]

/-- For every slot `i₀`, the graph with `d` extra copies of `i₀` has an injective
matching saturating all slots. -/
def ReplicationOK (t : ι → Finset α) (d : ℕ) : Prop :=
  ∀ i₀ : ι, ∃ f : ι ⊕ Fin d → α, Function.Injective f ∧
    (∀ i, f (Sum.inl i) ∈ t i) ∧ (∀ j, f (Sum.inr j) ∈ t i₀)

theorem surplus_of_replication [DecidableEq ι] (t : ι → Finset α) (d : ℕ)
    (h : ReplicationOK t d) (s : Finset ι) (hs : s.Nonempty) :
    #s + d ≤ #(s.biUnion t) := by
  obtain ⟨i₀, hi₀⟩ := hs
  obtain ⟨f, hinj, hl, hr⟩ := h i₀
  classical
  let u : Finset (ι ⊕ Fin d) := s.disjSum (univ : Finset (Fin d))
  have hu : #u = #s + d := by simp [u]
  have hsub : u.image f ⊆ s.biUnion t := by
    intro a ha
    rcases mem_image.1 ha with ⟨x, hx, rfl⟩
    rcases x with i | j
    · have : i ∈ s := by simpa [u] using hx
      exact mem_biUnion.2 ⟨i, this, hl i⟩
    · exact mem_biUnion.2 ⟨i₀, hi₀, hr j⟩
  calc #s + d = #u := hu.symm
    _ = #(u.image f) := (card_image_of_injective u hinj).symm
    _ ≤ #(s.biUnion t) := card_le_card hsub

theorem matching_avoiding (t : ι → Finset α) (d : ℕ)
    (h : ∀ s : Finset ι, s.Nonempty → #s + d ≤ #(s.biUnion t))
    (D : Finset α) (hD : #D ≤ d) :
    ∃ f : ι → α, Function.Injective f ∧ ∀ i, f i ∈ t i ∧ f i ∉ D := by
  classical
  have hall : ∀ s : Finset ι, #s ≤ #(s.biUnion fun i => t i \ D) := by
    intro s
    rcases s.eq_empty_or_nonempty with rfl | hs
    · simp
    · have h1 := h s hs
      have h2 : s.biUnion (fun i => t i \ D) = (s.biUnion t) \ D := by
        ext a; simp only [mem_biUnion, mem_sdiff]; constructor
        · rintro ⟨i, hi, hat, haD⟩; exact ⟨⟨i, hi, hat⟩, haD⟩
        · rintro ⟨⟨i, hi, hat⟩, haD⟩; exact ⟨i, hi, hat, haD⟩
      rw [h2]
      have h3 := le_card_sdiff D (s.biUnion t)
      omega
  obtain ⟨f, hinj, hf⟩ := (all_card_le_biUnion_card_iff_exists_injective _).1 hall
  exact ⟨f, hinj, fun i => by simpa [mem_sdiff] using hf i⟩

/-- The certificate checked by computer (replication for `d` extra copies) yields a
slot-saturating matching avoiding any `d` cells later claimed by Maker. -/
theorem pairing_of_replication [DecidableEq ι] (t : ι → Finset α) (d : ℕ)
    (h : ReplicationOK t d) (D : Finset α) (hD : #D ≤ d) :
    ∃ f : ι → α, Function.Injective f ∧ ∀ i, f i ∈ t i ∧ f i ∉ D :=
  matching_avoiding t d (fun s hs => surplus_of_replication t d h s hs) D hD

/-- Counting obstruction used for 6^3: a pairing of `L` surviving lines into `F` free cells
needs `2 * L ≤ F` (two distinct cells per line). -/
theorem pairing_needs_cells {L : Type*} [Fintype L] (F : Finset α)
    (p : L × Fin 2 → α) (hinj : Function.Injective p) (hF : ∀ x, p x ∈ F) :
    2 * Fintype.card L ≤ #F := by
  classical
  have : (univ.image p) ⊆ F := by
    intro a ha; rcases mem_image.1 ha with ⟨x, -, rfl⟩; exact hF x
  have h1 := card_le_card this
  rw [card_image_of_injective _ hinj] at h1
  simpa [Fintype.card_prod, mul_comm] using h1

end CubicTicTacToe
