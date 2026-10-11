import ErdosSzekeres.LowerBound.Triangle
import ErdosSzekeres.LowerBound.StackUnion

/-! Cups, caps and convex subsets of a stacked union.

Let `B` be stacked on `A` with sign `σ`. A `σ`-chain meeting `A` has at most
one point in `B`, and a `(-σ)`-chain meeting `B` has at most one point in `A`.
A convex subset meeting both blocks is a `σ`-chain in `A` and a `(-σ)`-chain
in `B`: otherwise one of its points lies in a triangle of three others. -/

namespace ErdosSzekeres.LowerBound

variable {σ : ℝ} {A B : Finset Point}

/-- A `σ`-chain meeting `A` has at most one point in `B`. -/
theorem Stacked.card_inter_right_le_one (h : Stacked σ A B) (hB : DistinctX B)
    {Q : Finset Point} (hQ : IsChain σ Q) {a : Point} (haQ : a ∈ Q) (haA : a ∈ A) :
    (Q ∩ B).card ≤ 1 := by
  have key : ∀ x ∈ Q ∩ B, ∀ y ∈ Q ∩ B, ¬ x 0 < y 0 := by
    intro x hx y hy hxy
    rw [Finset.mem_inter] at hx hy
    exact lt_asymm (h.pair_right a haA x hx.2 y hy.2 hxy)
      (hQ a haQ x hx.1 y hy.1 (h.left_lt a haA x hx.2) hxy)
  refine Finset.card_le_one.2 fun x hx y hy =>
    hB (Finset.mem_inter.1 hx).2 (Finset.mem_inter.1 hy).2 ?_
  exact le_antisymm (not_lt.1 (key y hy x hx)) (not_lt.1 (key x hx y hy))

/-- A `(-σ)`-chain meeting `B` has at most one point in `A`. -/
theorem Stacked.card_inter_left_le_one (h : Stacked σ A B) (hA : DistinctX A)
    {Q : Finset Point} (hQ : IsChain (-σ) Q) {b : Point} (hbQ : b ∈ Q) (hbB : b ∈ B) :
    (Q ∩ A).card ≤ 1 := by
  have key : ∀ x ∈ Q ∩ A, ∀ y ∈ Q ∩ A, ¬ x 0 < y 0 := by
    intro x hx y hy hxy
    rw [Finset.mem_inter] at hx hy
    have hc := hQ x hx.1 y hy.1 b hbQ hxy (h.left_lt y hy.2 b hbB)
    rw [neg_mul] at hc
    exact lt_asymm (neg_pos.1 hc) (h.pair_left x hx.2 y hy.2 b hbB hxy)
  refine Finset.card_le_one.2 fun x hx y hy =>
    hA (Finset.mem_inter.1 hx).2 (Finset.mem_inter.1 hy).2 ?_
  exact le_antisymm (not_lt.1 (key y hy x hx)) (not_lt.1 (key x hx y hy))

/-- A convex subset meeting `B` is a `σ`-chain in `A`. -/
theorem Stacked.isChain_inter_left (h : Stacked σ A B) (hσ : σ ≠ 0) (hgp : GeneralPosition A)
    {P : Finset Point} (hP : ConvexPosition P) {b : Point} (hbP : b ∈ P) (hbB : b ∈ B) :
    IsChain σ (P ∩ A) := by
  intro x hx y hy z hz hxy hyz
  rw [Finset.mem_inter] at hx hy hz
  have hxz := hxy.trans hyz
  have hne : σ * orient x y z ≠ 0 := mul_ne_zero hσ <|
    (generalPosition_iff_orient_ne_zero A).1 hgp x hx.2 y hy.2 z hz.2
      (ne_of_apply_ne (· 0) hxy.ne) (ne_of_apply_ne (· 0) hxz.ne) (ne_of_apply_ne (· 0) hyz.ne)
  refine lt_of_le_of_ne (not_lt.1 fun hneg => ?_) hne.symm
  refine hP.not_mem_convexHull_triple hx.1 hz.1 hbP hy.1
    (ne_of_apply_ne (· 0) hxy.ne') (ne_of_apply_ne (· 0) hyz.ne)
    (ne_of_apply_ne (· 0) (h.left_lt y hy.2 b hbB).ne)
    (mem_convexHull_of_orient σ x z b y (h.pair_left x hx.2 z hz.2 b hbB hxz) ?_ ?_ ?_)
  · rw [orient_swap, mul_neg]
    exact neg_pos.2 hneg
  · rw [orient_cycle]
    exact h.pair_left y hy.2 z hz.2 b hbB hyz
  · rw [← orient_cycle]
    exact h.pair_left x hx.2 y hy.2 b hbB hxy

/-- A convex subset meeting `A` is a `(-σ)`-chain in `B`. -/
theorem Stacked.isChain_inter_right (h : Stacked σ A B) (hσ : σ ≠ 0) (hgp : GeneralPosition B)
    {P : Finset Point} (hP : ConvexPosition P) {a : Point} (haP : a ∈ P) (haA : a ∈ A) :
    IsChain (-σ) (P ∩ B) := by
  intro x hx y hy z hz hxy hyz
  rw [Finset.mem_inter] at hx hy hz
  have hxz := hxy.trans hyz
  have hne : -σ * orient x y z ≠ 0 := mul_ne_zero (neg_ne_zero.2 hσ) <|
    (generalPosition_iff_orient_ne_zero B).1 hgp x hx.2 y hy.2 z hz.2
      (ne_of_apply_ne (· 0) hxy.ne) (ne_of_apply_ne (· 0) hxz.ne) (ne_of_apply_ne (· 0) hyz.ne)
  refine lt_of_le_of_ne (not_lt.1 fun hneg => ?_) hne.symm
  refine hP.not_mem_convexHull_triple haP hx.1 hz.1 hy.1
    (ne_of_apply_ne (· 0) (h.left_lt a haA y hy.2).ne') (ne_of_apply_ne (· 0) hxy.ne')
    (ne_of_apply_ne (· 0) hyz.ne) (mem_convexHull_of_orient (-σ) a x z y ?_ ?_ ?_ ?_)
  · rw [neg_mul]
    exact neg_pos.2 (h.pair_right a haA x hx.2 z hz.2 hxz)
  · rw [neg_mul]
    exact neg_pos.2 (h.pair_right a haA x hx.2 y hy.2 hxy)
  · rw [orient_swap, mul_neg]
    exact neg_pos.2 hneg
  · rw [← orient_cycle, neg_mul]
    exact neg_pos.2 (h.pair_right a haA y hy.2 z hz.2 hyz)

/-- A subset of `A ∪ B` disjoint from `A` lies in `B`. -/
private theorem subset_right_of_disjoint {t : Finset Point} (ht : t ⊆ A ∪ B)
    (hd : Disjoint t A) : t ⊆ B := fun _ hx =>
  (Finset.mem_union.1 (ht hx)).resolve_left (Finset.disjoint_left.1 hd hx)

/-- A subset of `A ∪ B` disjoint from `B` lies in `A`. -/
private theorem subset_left_of_disjoint {t : Finset Point} (ht : t ⊆ A ∪ B)
    (hd : Disjoint t B) : t ⊆ A := fun _ hx =>
  (Finset.mem_union.1 (ht hx)).resolve_right (Finset.disjoint_left.1 hd hx)

private theorem card_le_card_inter_add {t : Finset Point} (ht : t ⊆ A ∪ B) :
    t.card ≤ (t ∩ A).card + (t ∩ B).card := by
  calc t.card = (t ∩ A ∪ t ∩ B).card := by
        rw [← Finset.inter_union_distrib_left, Finset.inter_eq_left.2 ht]
    _ ≤ _ := Finset.card_union_le _ _

theorem Stacked.chainBound_union (h : Stacked σ A B) (hB : DistinctX B) {m m' : ℕ}
    (hAm : ChainBound σ m A) (hBm : ChainBound σ m' B) :
    ChainBound σ (max (m + 1) m') (A ∪ B) := by
  intro t ht hc
  by_cases hd : Disjoint t A
  · exact (hBm t (subset_right_of_disjoint ht hd) hc).trans (le_max_right _ _)
  obtain ⟨a, hat, haA⟩ := Finset.not_disjoint_iff.1 hd
  have h1 := hAm _ Finset.inter_subset_right (hc.mono Finset.inter_subset_left)
  have h2 := h.card_inter_right_le_one hB hc hat haA
  have h3 := card_le_card_inter_add ht
  omega

theorem Stacked.chainBound_neg_union (h : Stacked σ A B) (hA : DistinctX A) {m m' : ℕ}
    (hAm : ChainBound (-σ) m A) (hBm : ChainBound (-σ) m' B) :
    ChainBound (-σ) (max m (m' + 1)) (A ∪ B) := by
  intro t ht hc
  by_cases hd : Disjoint t B
  · exact (hAm t (subset_left_of_disjoint ht hd) hc).trans (le_max_left _ _)
  obtain ⟨b, hbt, hbB⟩ := Finset.not_disjoint_iff.1 hd
  have h1 := h.card_inter_left_le_one hA hc hbt hbB
  have h2 := hBm _ Finset.inter_subset_right (hc.mono Finset.inter_subset_left)
  have h3 := card_le_card_inter_add ht
  omega

theorem Stacked.convexBound_union (h : Stacked σ A B) (hσ : σ ≠ 0)
    (hgpA : GeneralPosition A) (hgpB : GeneralPosition B) {c c' m m' : ℕ}
    (hAc : ConvexBound c A) (hBc : ConvexBound c' B)
    (hAm : ChainBound σ m A) (hBm : ChainBound (-σ) m' B) :
    ConvexBound (max (max c c') (m + m')) (A ∪ B) := by
  intro t ht hc
  by_cases hdA : Disjoint t A
  · have := hBc t (subset_right_of_disjoint ht hdA) hc
    omega
  by_cases hdB : Disjoint t B
  · have := hAc t (subset_left_of_disjoint ht hdB) hc
    omega
  obtain ⟨a, hat, haA⟩ := Finset.not_disjoint_iff.1 hdA
  obtain ⟨b, hbt, hbB⟩ := Finset.not_disjoint_iff.1 hdB
  have h1 := hAm _ Finset.inter_subset_right (h.isChain_inter_left hσ hgpA hc hbt hbB)
  have h2 := hBm _ Finset.inter_subset_right (h.isChain_inter_right hσ hgpB hc hat haA)
  have h3 := card_le_card_inter_add ht
  omega

end ErdosSzekeres.LowerBound
