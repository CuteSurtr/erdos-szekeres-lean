import ErdosSzekeres.HMPT.MixedCapData

namespace ErdosSzekeres.HMPT.MixedCap

private theorem chain_filter_image (s : Finset Point) :
    (Finset.univ.filter (fun i => chainPoint i ∈ s)).image chainPoint =
      s ∩ chainPoints := by
  classical
  ext p
  simp only [Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and,
    Finset.mem_inter, chainPoints]
  aesop

/-- A convex subset meeting the inner cap contains at most two chain vertices. -/
theorem chain_count_le_two {s : Finset Point} (hs : ConvexPosition s)
    {t : Fin 8} (ht : innerPoint t ∈ s) : (s ∩ chainPoints).card ≤ 2 := by
  classical
  let U := Finset.univ.filter (fun i => chainPoint i ∈ s)
  have hU : U.card ≤ 2 := by
    by_contra! hn
    obtain ⟨v, hv, hcard⟩ := Finset.exists_subset_card_eq (show 3 ≤ U.card by omega)
    let f := v.orderEmbOfFin hcard
    have hm (i : Fin 3) : chainPoint (f i) ∈ s :=
      (Finset.mem_filter.mp (hv (v.orderEmbOfFin_mem hcard i))).2
    exact (three_chain_one_inner (f 0) (f 1) (f 2) t
      (f.strictMono (by decide)) (f.strictMono (by decide))).not_convexPosition
      (hm 1) (hm 0) (hm 2) ht hs
  rw [← chain_filter_image]
  exact (Finset.card_image_le).trans hU

/-- Retaining the middle anchor restricts a mixed convex subset to one chain vertex. -/
theorem chain_count_le_one {s : Finset Point} (hs : ConvexPosition s)
    {t : Fin 8} (ht : innerPoint t ∈ s) (ha : anchor 2 ∈ s) :
    (s ∩ chainPoints).card ≤ 1 := by
  classical
  let U := Finset.univ.filter (fun i => chainPoint i ∈ s)
  have hU : U.card ≤ 1 := by
    by_contra! hn
    obtain ⟨v, hv, hcard⟩ := Finset.exists_subset_card_eq (show 2 ≤ U.card by omega)
    let f := v.orderEmbOfFin hcard
    have hm (i : Fin 2) : chainPoint (f i) ∈ s :=
      (Finset.mem_filter.mp (hv (v.orderEmbOfFin_mem hcard i))).2
    exact (two_chain_anchor_inner (f 0) (f 1) t (f.strictMono (by decide))).not_convexPosition
      (hm 1) (hm 0) ha ht hs
  rw [← chain_filter_image]
  exact (Finset.card_image_le).trans hU

/-- The complete ambient set includes all six support anchors. Even so, it
contains no convex subset of size sixteen. No search algorithm is trusted. -/
theorem convex_subset_card_le {s : Finset Point} (hsub : s ⊆ ambient)
    (hs : ConvexPosition s) : s.card ≤ 15 := by
  classical
  have hpartition : s = (s ∩ anchors) ∪ (s ∩ chainPoints) ∪ (s ∩ innerPoints) := by
    ext p
    simp only [Finset.mem_union, Finset.mem_inter]
    constructor
    · intro hp
      have := hsub hp
      simp only [ambient, Finset.mem_union] at this
      tauto
    · tauto
  have htotal : s.card ≤ (s ∩ anchors).card + (s ∩ chainPoints).card +
      (s ∩ innerPoints).card := by
    conv_lhs => rw [hpartition]
    exact (Finset.card_union_le _ _).trans
      (Nat.add_le_add_right (Finset.card_union_le _ _) _)
  have hA : (s ∩ anchors).card ≤ 6 := by
    simpa only [card_anchors] using
      Finset.card_le_card (show s ∩ anchors ⊆ anchors from Finset.inter_subset_right)
  have hC : (s ∩ chainPoints).card ≤ 8 := by
    simpa only [card_chainPoints] using
      Finset.card_le_card (show s ∩ chainPoints ⊆ chainPoints from Finset.inter_subset_right)
  have hT : (s ∩ innerPoints).card ≤ 8 := by
    simpa only [card_innerPoints] using
      Finset.card_le_card (show s ∩ innerPoints ⊆ innerPoints from Finset.inter_subset_right)
  by_cases ht : ∃ t, innerPoint t ∈ s
  · obtain ⟨t, ht⟩ := ht
    by_cases ha : anchor 2 ∈ s
    · have := chain_count_le_one hs ht ha
      omega
    · have hA' : (s ∩ anchors).card ≤ 5 := by
        have hsa : s ∩ anchors ⊆ anchors.erase (anchor 2) := by
          intro p hp
          exact Finset.mem_erase.mpr ⟨fun he => ha (he ▸ (Finset.mem_inter.mp hp).1),
            (Finset.mem_inter.mp hp).2⟩
        have ham : anchor 2 ∈ anchors := Finset.mem_image.mpr ⟨2, Finset.mem_univ _, rfl⟩
        have := Finset.card_le_card hsa
        simpa only [Finset.card_erase_of_mem ham, card_anchors] using this
      have := chain_count_le_two hs ht
      omega
  · have hempty : s ∩ innerPoints = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro p hp
      obtain ⟨hps, hpT⟩ := Finset.mem_inter.mp hp
      obtain ⟨t, _, rfl⟩ := Finset.mem_image.mp hpT
      exact ht ⟨t, hps⟩
    rw [hempty, Finset.card_empty] at htotal
    omega

theorem avoids_sixteen : ¬ HasConvexNGon 16 ambient := by
  rintro ⟨s, hsub, hcard, hs⟩
  have := convex_subset_card_le hsub hs
  omega

end ErdosSzekeres.HMPT.MixedCap
