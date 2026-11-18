import BridgeBase
import SubsequenceFacts
import ErdosSzekeres.Suk.FourPoint

/-! Auxiliary declarations for the separately checked real-coordinate bridge. -/

noncomputable section

namespace Delta3.Balanced15.RealBridge

theorem quad_real_iff (q : List Index) (hn : q.Nodup) (hlen : q.length = 4) :
    quadConvex q = true ↔ ErdosSzekeres.ConvexPosition (q.toFinset.image realPoint) := by
  classical
  obtain ⟨a, b, c, d, rfl⟩ := List.length_eq_four.mp hlen
  simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false, not_or,
    List.nodup_nil, not_false_eq_true, and_true] at hn
  obtain ⟨⟨hab, hac, had⟩, ⟨hbc, hbd⟩, hcd⟩ := hn
  simpa [quadConvex, ErdosSzekeres.QuadConvexSigns, real_orient] using
    (ErdosSzekeres.convexPosition_four_iff_signs (realPoint a) (realPoint b)
      (realPoint c) (realPoint d) (real_orient_ne a b c hab hac hbc)
      (real_orient_ne a b d hab had hbd) (real_orient_ne a c d hac had hcd)
      (real_orient_ne b c d hbc hbd hcd)).symm

theorem signConvex_of_real (s : List Index) (hn : s.Nodup)
    (hc : ErdosSzekeres.ConvexPosition (s.toFinset.image realPoint)) : signConvex s = true := by
  classical
  apply List.all_eq_true.mpr
  intro q hq
  obtain ⟨hqsub, hqlen⟩ := choose_sound hq
  apply (quad_real_iff q (hn.sublist hqsub) hqlen).mpr
  apply hc.mono
  intro p hp
  obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hp
  exact Finset.mem_image.mpr ⟨i, List.mem_toFinset.mpr
    (hqsub.subset (List.mem_toFinset.mp hi)), rfl⟩

theorem sorted_subset_sublist (u : Finset Index) (s : List Index)
    (hmem : ∀ i ∈ u, i ∈ s) (hs : s.Pairwise (· ≤ ·)) :
    (u.sort (· ≤ ·)).Sublist s :=
  List.sublist_of_subperm_of_sorted
    ((Finset.sort_nodup (· ≤ ·) u).subperm
      (fun i hi => hmem i ((Finset.mem_sort (r := (· ≤ ·))).mp hi)))
    (Finset.sort_sorted (· ≤ ·) u) hs

theorem real_of_signConvex (s : List Index) (hn : s.Nodup)
    (hs : s.Pairwise (· ≤ ·)) (hlen : 4 ≤ s.length) (hc : signConvex s = true) :
    ErdosSzekeres.ConvexPosition (s.toFinset.image realPoint) := by
  classical
  apply ErdosSzekeres.Suk.convexPosition_of_four_subsets
    (by simpa only [Finset.card_image_of_injective _ realPoint_injective,
      List.toFinset_card_of_nodup hn] using hlen)
  intro t hts ht
  obtain ⟨u, hu, hut⟩ := Finset.subset_image_iff.mp hts
  have huc : u.card = 4 := by
    simpa only [← hut, Finset.card_image_of_injective _ realPoint_injective] using ht
  let q := u.sort (· ≤ ·)
  have hqsub : q.Sublist s :=
    sorted_subset_sublist u s (fun i hi => List.mem_toFinset.mp (hu hi)) hs
  have hqlen : q.length = 4 := (Finset.length_sort (r := (· ≤ ·))).trans huc
  have hmem : q ∈ choose 4 s := by
    simpa only [hqlen] using mem_choose_of_sublist hqsub
  have hqc := (quad_real_iff q (hn.sublist hqsub) hqlen).mp
    (List.all_eq_true.mp hc q hmem)
  simpa only [q, Finset.sort_toFinset, hut] using hqc

theorem no_real_seven_subsequence (s : List Index) (hs : s.Sublist indices)
    (hlen : s.length = 7) : ¬ErdosSzekeres.ConvexPosition (s.toFinset.image realPoint) :=
  fun hc => Bool.noConfusion ((seven_subsequence_not_signConvex s hs hlen).symm.trans
    (signConvex_of_real s (indices_nodup.sublist hs) hc))

theorem no_real_heptagon : ¬ErdosSzekeres.HasConvexNGon 7 realSet := by
  classical
  rintro ⟨t, ht, hcard, hc⟩
  obtain ⟨u, _, hut⟩ := Finset.subset_image_iff.mp ht
  have huc : u.card = 7 := by
    simpa only [← hut, Finset.card_image_of_injective _ realPoint_injective] using hcard
  let s := u.sort (· ≤ ·)
  have hs : s.Sublist indices :=
    sorted_subset_sublist u indices (fun i _ => indices_complete i) indices_sorted
  have hlen : s.length = 7 := (Finset.length_sort (r := (· ≤ ·))).trans huc
  apply no_real_seven_subsequence s hs hlen
  simpa only [s, Finset.sort_toFinset, hut] using hc

#print axioms quad_real_iff
#print axioms signConvex_of_real
#print axioms sorted_subset_sublist
#print axioms real_of_signConvex
#print axioms no_real_seven_subsequence
#print axioms no_real_heptagon

end Delta3.Balanced15.RealBridge
