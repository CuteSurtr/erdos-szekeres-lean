import ErdosSzekeres.HMPT.MixedCapObstruction

namespace ErdosSzekeres.HMPT.MixedCap

open Suk

theorem chain_mem_spike (i : Fin 8) : chainPoint i ∈ firstFrame.spike := by
  change orient (anchor 0) (anchor 1) (chainPoint i) < 0 ∧
    0 < orient (anchor 1) (anchor 2) (chainPoint i) ∧
    orient (anchor 2) (anchor 3) (chainPoint i) < 0
  simp only [anchor, chainPoint, orient_integerToReal]
  exact_mod_cast chain_spike_signs i

theorem inner_mem_spike (i : Fin 8) : innerPoint i ∈ lastFrame.spike := by
  change orient (anchor 2) (anchor 3) (innerPoint i) < 0 ∧
    0 < orient (anchor 3) (anchor 4) (innerPoint i) ∧
    orient (anchor 4) (anchor 5) (innerPoint i) < 0
  simp only [anchor, innerPoint, orient_integerToReal]
  exact_mod_cast inner_spike_signs i

noncomputable def verticalChain : SpikeChain firstFrame where
  length := 8
  point i := ⟨chainPoint i, chain_mem_spike i⟩
  increasing := by
    intro i j hij
    rw [AboveBase.lt_iff]
    refine ⟨?_, (chain_nested i j hij).mem_triangle⟩
    intro he
    exact (ne_of_lt hij) (chain_injective (congrArg AboveBase.val he))

theorem verticalChain_points : verticalChain.points = chainPoints := rfl

private theorem left_image :
    Finset.univ.image (fun i => integerToReal (leftZ i)) = insert (anchor 2) chainPoints := by
  classical
  ext p
  constructor
  · rintro hp
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    by_cases hi : i.val < 8
    · apply Finset.mem_insert_of_mem
      exact Finset.mem_image.mpr ⟨⟨i.val, hi⟩, Finset.mem_univ _, by simp [leftZ, hi, chainPoint]⟩
    · simp [leftZ, hi, anchor]
  · intro hp
    rcases Finset.mem_insert.mp hp with rfl | hp
    · exact Finset.mem_image.mpr ⟨8, Finset.mem_univ _, by simp [leftZ, anchor]⟩
    · obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
      exact Finset.mem_image.mpr ⟨⟨i.val, by omega⟩, Finset.mem_univ _,
        by simp [leftZ, i.isLt, chainPoint]⟩

theorem vertical_left_cap : verticalChain.LeftCap 8 := by
  classical
  refine ⟨Finset.univ, by decide, ?_⟩
  change ConvexPosition (insert (anchor 2) chainPoints)
  rw [← left_image]
  apply convexPosition_integer_image_of_supports
  intro i
  exact ⟨i + 1, (left_support_certificate i).1, 1,
    by simpa only [one_mul] using (left_support_certificate i).2⟩

theorem inner_antichain : SpikeAntichain lastFrame innerPoints := by
  classical
  rintro p hp q hq hpq
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
  obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hq
  have hij : j ≠ i := fun he => hpq (congrArg innerPoint he).symm
  have hside : 0 < orient (innerPoint j) (innerPoint i) (anchor 2) *
      orient (innerPoint j) (innerPoint i) (anchor 5) := by
    simp only [innerPoint, anchor, orient_integerToReal]
    exact_mod_cast inner_pair_sides j i hij
  have hpos : 0 < orient (innerPoint i) (anchor 2) (anchor 5) := by
    rw [orient_cycle, orient_cycle]
    simp only [innerPoint, anchor, orient_integerToReal]
    exact_mod_cast inner_outer_pos i
  have hn := not_mem_triangle_of_same_side (innerPoint j) (innerPoint i)
    (anchor 2) (anchor 5) hside (ne_of_gt hpos)
  have he : ({lastFrame.a, lastFrame.d, innerPoint i} : Set Point) =
      {innerPoint i, anchor 2, anchor 5} := by
    ext p
    simp [lastFrame, support, ClockwiseAnchors.frame, or_comm, or_left_comm]
  rw [he]
  exact hn

theorem inner_cap : InnerCap lastFrame innerPoints := by
  classical
  intro p hp
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
  refine ⟨innerPoint (innerNeighbor i), Finset.mem_image.mpr
    ⟨innerNeighbor i, Finset.mem_univ _, rfl⟩, ?_, ?_⟩
  · intro he
    exact (inner_support_certificate i).1 (integerToReal_injective he)
  · intro z hz hzp hzq
    obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hz
    have hki : innerZ k ≠ innerZ i := fun he => hzp (congrArg integerToReal he)
    have hkj : innerZ k ≠ innerZ (innerNeighbor i) :=
      fun he => hzq (congrArg integerToReal he)
    change 0 < orient (innerPoint i) (innerPoint (innerNeighbor i)) (anchor 2) *
      orient (innerPoint i) (innerPoint (innerNeighbor i)) (innerPoint k)
    simp only [innerPoint, anchor, orient_integerToReal]
    exact_mod_cast (inner_support_certificate i).2 k hki hkj

def allPoint (i : Fin 22) : Point := integerToReal (allZ i)

theorem ambient_eq_image : ambient = Finset.univ.image allPoint := by
  classical
  ext p
  constructor
  · intro hp
    rcases Finset.mem_union.mp hp with hp | hp
    · rcases Finset.mem_union.mp hp with hp | hp
      · obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
        exact Finset.mem_image.mpr ⟨⟨i.val, by omega⟩, Finset.mem_univ _,
          by simp [allPoint, allZ, i.isLt, anchor]⟩
      · obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
        exact Finset.mem_image.mpr ⟨⟨i.val + 6, by omega⟩, Finset.mem_univ _, by
          simp [allPoint, allZ, show ¬ i.val + 6 < 6 by omega,
            show i.val + 6 < 14 by omega, chainPoint]⟩
    · obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
      exact Finset.mem_image.mpr ⟨⟨i.val + 14, by omega⟩, Finset.mem_univ _, by
        simp [allPoint, allZ, show ¬ i.val + 14 < 6 by omega,
          show ¬ i.val + 14 < 14 by omega, innerPoint]⟩
  · intro hp
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    by_cases hi : i.val < 6
    · apply Finset.mem_union_left
      apply Finset.mem_union_left
      exact Finset.mem_image.mpr ⟨⟨i.val, hi⟩, Finset.mem_univ _,
        by simp [allPoint, allZ, hi, anchor]⟩
    · by_cases hj : i.val < 14
      · apply Finset.mem_union_left
        apply Finset.mem_union_right
        exact Finset.mem_image.mpr ⟨⟨i.val - 6, by omega⟩, Finset.mem_univ _,
          by simp [allPoint, allZ, hi, hj, chainPoint]⟩
      · apply Finset.mem_union_right
        exact Finset.mem_image.mpr ⟨⟨i.val - 14, by omega⟩, Finset.mem_univ _,
          by simp [allPoint, allZ, hi, hj, innerPoint]⟩

theorem general_position : GeneralPosition ambient := by
  classical
  rw [ambient_eq_image, generalPosition_iff_orient_ne_zero]
  intro a ha b hb c hc hab hac hbc
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp ha
  obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hb
  obtain ⟨k, _, rfl⟩ := Finset.mem_image.mp hc
  have hij : i ≠ j := fun he => hab (congrArg allPoint he)
  have hik : i ≠ k := fun he => hac (congrArg allPoint he)
  have hjk : j ≠ k := fun he => hbc (congrArg allPoint he)
  simp only [allPoint, orient_integerToReal, ne_eq, Int.cast_eq_zero]
  exact all_general_position i j k hij hik hjk

theorem allPoint_injective : Function.Injective allPoint := by
  intro i j he
  by_contra hij
  have hz := integerToReal_injective he
  exact all_distinct_x i j hij (congrFun hz 0)

theorem card_ambient : ambient.card = 22 := by
  classical
  rw [ambient_eq_image, Finset.card_image_of_injective _ allPoint_injective]
  rfl

theorem frames_horizontal (i : Fin 3) : (support.frame i).Horizontal := by
  fin_cases i <;> norm_num [CapFrame.Horizontal, ClockwiseAnchors.frame,
    support, anchor, integerToReal, anchorZ]

theorem distinct_x : ∀ p ∈ ambient, ∀ q ∈ ambient, p ≠ q → p 0 ≠ q 0 := by
  classical
  rw [ambient_eq_image]
  intro p hp q hq hpq
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
  obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hq
  have hij : i ≠ j := fun he => hpq (congrArg allPoint he)
  change ((allZ i 0 : ℤ) : ℝ) ≠ ((allZ j 0 : ℤ) : ℝ)
  exact_mod_cast all_distinct_x i j hij

theorem contains_fifteen : HasConvexNGon 15 ambient := by
  classical
  let p := fun i => integerToReal (fifteenZ i)
  have hinj : Function.Injective p := by
    intro i j he
    by_contra hij
    exact fifteen_distinct_x i j hij (congrFun (integerToReal_injective he) 0)
  refine ⟨Finset.univ.image p, ?_, ?_, ?_⟩
  · intro x hx
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hx
    by_cases hi : i.val < 6
    · apply Finset.mem_union_left
      apply Finset.mem_union_left
      exact Finset.mem_image.mpr ⟨⟨i.val, hi⟩, Finset.mem_univ _,
        by simp [p, fifteenZ, hi, anchor]⟩
    · by_cases hj : i.val < 14
      · apply Finset.mem_union_right
        exact Finset.mem_image.mpr ⟨⟨i.val - 6, by omega⟩, Finset.mem_univ _,
          by simp [p, fifteenZ, hi, hj, innerPoint]⟩
      · apply Finset.mem_union_left
        apply Finset.mem_union_right
        exact Finset.mem_image.mpr ⟨7, Finset.mem_univ _,
          by simp [p, fifteenZ, hi, hj, chainPoint]⟩
  · simp [Finset.card_image_of_injective _ hinj]
  · apply convexPosition_integer_image_of_supports
    intro i
    obtain ⟨j, hij, hs⟩ := fifteen_support_certificate i
    exact ⟨j, hij, 1, by simpa only [one_mul] using hs⟩

/-- A counterexample to an unconditional additive budget for a vertical left
cap and an inner cap two spikes away. Both caps and every support anchor lie
in the same general-position ambient configuration. This does not refute the
Erdős–Szekeres conjecture or improve its known upper bound. -/
theorem mixed_cap_budget_counterexample :
    ∃ (P : Finset Point) (A : ClockwiseAnchors 6)
      (C : SpikeChain (A.frame (0 : Fin 3))) (T : Finset Point),
      GeneralPosition P ∧ P.card = 22 ∧ (∀ i, A.point i ∈ P) ∧
      (∀ i, (A.frame i).Horizontal) ∧
      (∀ p ∈ P, ∀ q ∈ P, p ≠ q → p 0 ≠ q 0) ∧
      C.points ⊆ P ∧ C.LeftCap 8 ∧ T ⊆ P ∧ T.card = 8 ∧
      (∀ p ∈ T, p ∈ (A.frame (2 : Fin 3)).spike) ∧
      SpikeAntichain (A.frame (2 : Fin 3)) T ∧
      InnerCap (A.frame (2 : Fin 3)) T ∧
      HasConvexNGon 15 P ∧ ¬ HasConvexNGon (8 + T.card) P := by
  classical
  refine ⟨ambient, support, verticalChain, innerPoints, general_position, card_ambient,
    ?_, frames_horizontal, distinct_x, ?_, vertical_left_cap, ?_, card_innerPoints,
    ?_, inner_antichain, inner_cap,
    contains_fifteen, ?_⟩
  · intro i
    exact Finset.mem_union_left _ (Finset.mem_union_left _
      (Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩))
  · rw [verticalChain_points]
    exact (Finset.subset_union_right).trans Finset.subset_union_left
  · exact Finset.subset_union_right
  · intro p hp
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    exact inner_mem_spike i
  · simpa only [card_innerPoints] using avoids_sixteen

end ErdosSzekeres.HMPT.MixedCap
