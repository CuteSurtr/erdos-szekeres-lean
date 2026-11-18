import TerminalReal

noncomputable section

namespace Delta3.Balanced15.RealBridge

/-- All increasing-x triples of a real finite set have negative orientation. -/
def XOrderedCap (s : Finset ErdosSzekeres.Point) : Prop :=
  ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a 0 < b 0 → b 0 < c 0 →
    ErdosSzekeres.orient a b c < 0

/-- A k-cap contained in an ambient real finite set. -/
def HasXOrderedCap (k : ℕ) (s : Finset ErdosSzekeres.Point) : Prop :=
  ∃ t ⊆ s, t.card = k ∧ XOrderedCap t

theorem indices_strict : indices.Pairwise (· < ·) := by decide

theorem realCap_of_setCap (s : List Index) (hs : s.Pairwise (· < ·))
    (hc : XOrderedCap (s.toFinset.image realPoint)) : RealCap s := by
  classical
  intro a b c ht
  have hp := hs.sublist ht
  have hab : a < b := (List.pairwise_cons.mp hp).1 b (by simp)
  have hbc : b < c := (List.pairwise_cons.mp (List.pairwise_cons.mp hp).2).1 c (by simp)
  have hm : ∀ i ∈ [a, b, c], realPoint i ∈ s.toFinset.image realPoint := by
    intro i hi
    exact Finset.mem_image.mpr ⟨i, List.mem_toFinset.mpr (ht.subset hi), rfl⟩
  exact hc (realPoint a) (hm a (by simp)) (realPoint b) (hm b (by simp))
    (realPoint c) (hm c (by simp)) (real_x_strict hab) (real_x_strict hbc)

theorem no_real_five_cap : ¬HasXOrderedCap 5 realSet := by
  classical
  rintro ⟨t, ht, hcard, hc⟩
  obtain ⟨u, _, hut⟩ := Finset.subset_image_iff.mp ht
  have huc : u.card = 5 := by
    simpa only [← hut, Finset.card_image_of_injective _ realPoint_injective] using hcard
  let s := u.sort (· ≤ ·)
  have hs : s.Sublist indices :=
    sorted_subset_sublist u indices (fun i _ => indices_complete i) indices_sorted
  have hlen : s.length = 5 := (Finset.length_sort (r := (· ≤ ·))).trans huc
  apply no_real_five_cap_subsequence s hs hlen
  apply realCap_of_setCap s (indices_strict.sublist hs)
  simpa only [s, Finset.sort_toFinset, hut] using hc

/-- Every selected cap triple ends an ambient four-cap with the same last pair. -/
def SetTerminalSafe (s A : Finset ErdosSzekeres.Point) : Prop :=
  ∀ a ∈ A, ∀ b ∈ A, ∀ c ∈ A, a 0 < b 0 → b 0 < c 0 →
    ErdosSzekeres.orient a b c < 0 →
    ∃ u ∈ s, ∃ v ∈ s, u 0 < v 0 ∧ v 0 < b 0 ∧ b 0 < c 0 ∧
      XOrderedCap {u, v, b, c}

/-- A meets every six-element subset in genuine real convex position. -/
def HitsConvexSix (s A : Finset ErdosSzekeres.Point) : Prop :=
  ∀ t ⊆ s, t.card = 6 → ErdosSzekeres.ConvexPosition t → ∃ p ∈ t, p ∈ A

theorem realTerminalSafe_of_set (A : Finset ErdosSzekeres.Point)
    (h : SetTerminalSafe realSet A) : RealTerminalSafe (fun i => realPoint i ∈ A) := by
  classical
  intro a b c hab hbc ho ha hb hc
  obtain ⟨u, hu, v, hv, huv, hvb, _, hcap⟩ :=
    h (realPoint a) ha (realPoint b) hb (realPoint c) hc
      (real_x_strict hab) (real_x_strict hbc) ho
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hu
  obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hv
  have hij : i < j := real_x_strict.lt_iff_lt.mp huv
  have hjb : j < b := real_x_strict.lt_iff_lt.mp hvb
  refine ⟨i, j, hij, hjb, hbc, realCap_of_setCap _ ?_ ?_⟩
  · apply List.IsChain.pairwise
    simp only [List.isChain_cons_cons, List.IsChain.singleton, and_true]
    exact ⟨hij, hjb, hbc⟩
  · simpa using hcap

theorem realHitsSix_of_set (A : Finset ErdosSzekeres.Point)
    (h : HitsConvexSix realSet A) : RealHitsSix (fun i => realPoint i ∈ A) := by
  classical
  intro a b c d e f hab hbc hcd hde hef hc
  have hs : [a, b, c, d, e, f].Pairwise (· < ·) := by
    apply List.IsChain.pairwise
    simp only [List.isChain_cons_cons, List.IsChain.singleton, and_true]
    exact ⟨hab, hbc, hcd, hde, hef⟩
  have hsub : [a, b, c, d, e, f].toFinset.image realPoint ⊆ realSet := by
    intro p hp
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    exact Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩
  have hcard : ([a, b, c, d, e, f].toFinset.image realPoint).card = 6 := by
    rw [Finset.card_image_of_injective _ realPoint_injective,
      List.toFinset_card_of_nodup hs.nodup]
    rfl
  obtain ⟨p, hp, hpA⟩ := h _ hsub hcard hc
  obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hp
  simp only [List.toFinset_cons, List.toFinset_nil, Finset.mem_insert,
    Finset.notMem_empty, or_false] at hi
  rcases hi with rfl | rfl | rfl | rfl | rfl | rfl
  · exact Or.inl hpA
  · exact Or.inr (Or.inl hpA)
  · exact Or.inr (Or.inr (Or.inl hpA))
  · exact Or.inr (Or.inr (Or.inr (Or.inl hpA)))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl hpA))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr hpA))))

theorem no_real_subset_selection :
    ¬∃ A : Finset ErdosSzekeres.Point, A ⊆ realSet ∧
      SetTerminalSafe realSet A ∧ HitsConvexSix realSet A := by
  rintro ⟨A, _, hT, hH⟩
  exact no_real_terminal_selection
    ⟨(fun i => realPoint i ∈ A), realTerminalSafe_of_set A hT, realHitsSix_of_set A hH⟩

#print axioms indices_strict
#print axioms realCap_of_setCap
#print axioms no_real_five_cap
#print axioms realTerminalSafe_of_set
#print axioms realHitsSix_of_set
#print axioms no_real_subset_selection

end Delta3.Balanced15.RealBridge
