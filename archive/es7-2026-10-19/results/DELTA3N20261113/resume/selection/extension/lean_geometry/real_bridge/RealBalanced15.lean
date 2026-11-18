import PointSetBridge

/-! Real-coordinate consequences of the separately frozen balanced-15 certificate.
This file states terminal-pair membership, not an envelope domination condition. -/

noncomputable section

namespace Delta3.Balanced15.RealBridge

/-- Distinct points of a real finite set have distinct horizontal coordinates. -/
def DistinctX (s : Finset ErdosSzekeres.Point) : Prop :=
  ∀ p ∈ s, ∀ q ∈ s, p 0 = q 0 → p = q

theorem realSet_distinct_x : DistinctX realSet := by
  classical
  intro p hp q hq hx
  obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
  obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hq
  exact congrArg realPoint (real_x_strict.injective hx)

/-- The exact integer-coordinate witness, viewed in the standard real plane. -/
theorem balanced15_real_obstruction :
    realSet.card = 15 ∧
    DistinctX realSet ∧
    ErdosSzekeres.GeneralPosition realSet ∧
    ¬HasXOrderedCap 5 realSet ∧
    ¬ErdosSzekeres.HasConvexNGon 7 realSet ∧
    ¬∃ A : Finset ErdosSzekeres.Point, A ⊆ realSet ∧
      SetTerminalSafe realSet A ∧ HitsConvexSix realSet A :=
  ⟨realSet_card, realSet_distinct_x, realSet_generalPosition, no_real_five_cap,
    no_real_heptagon, no_real_subset_selection⟩

/-- Existence of an actual real finite configuration with the stated obstruction. -/
theorem exists_real_terminal_obstruction :
    ∃ s : Finset ErdosSzekeres.Point,
      s.card = 15 ∧ DistinctX s ∧ ErdosSzekeres.GeneralPosition s ∧
      ¬HasXOrderedCap 5 s ∧ ¬ErdosSzekeres.HasConvexNGon 7 s ∧
      ¬∃ A : Finset ErdosSzekeres.Point, A ⊆ s ∧
        SetTerminalSafe s A ∧ HitsConvexSix s A :=
  ⟨realSet, balanced15_real_obstruction⟩

#print axioms realSet_distinct_x
#print axioms balanced15_real_obstruction
#print axioms exists_real_terminal_obstruction

end Delta3.Balanced15.RealBridge
