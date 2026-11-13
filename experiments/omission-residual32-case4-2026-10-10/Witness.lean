import Residual32ContextsProof.Catalog

/-! A 32-hole Boolean model of the exact frozen 2469-row catalog.
This is not asserted to be realizable by any planar point configuration. -/
namespace OmissionResidual32Case4
open scoped BigOperators
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

def missing : Finset (Fin 154) :=
  {7, 12, 33, 39, 44, 47, 50, 51, 52, 54, 55, 56, 69, 71, 73, 75, 76, 77, 78, 90, 97, 99, 101, 109, 115, 117, 118, 119, 124, 127, 132, 133}

theorem missing_card : missing.card = 32 := by decide +kernel

theorem all_rows : ∀ r : Fin 2469,
    OmissionResidual32Contexts.demand r ≤
      (OmissionResidual32Contexts.support r ∩ missing).card := by
  decide +kernel

theorem fixed_context : (54 : Fin 154) ∈ missing ∧
    (43 : Fin 154) ∉ missing ∧ (67 : Fin 154) ∉ missing := by decide +kernel

theorem zero_occupied : (0 : Fin 154) ∉ missing := by decide +kernel

def holes (i : Fin 154) : ℕ := if i ∈ missing then 1 else 0

theorem holes_boolean (i : Fin 154) : holes i ≤ 1 := by
  unfold holes
  split_ifs <;> omega

theorem sum_holes (s : Finset (Fin 154)) :
    (∑ i ∈ s, holes i) = (s ∩ missing).card := by
  simp [holes]

theorem total_holes : (∑ i, holes i) = 32 := by
  simpa using (sum_holes Finset.univ).trans (by simpa using missing_card)

theorem allows_thirty_two_holes :
    ∃ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) ∧
      (∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
        ∑ i ∈ OmissionResidual32Contexts.support r, h i) ∧
      (∑ i, h i) = 32 ∧ h 54 = 1 ∧ h 43 = 0 ∧ h 67 = 0 ∧ h 0 = 0 := by
  refine ⟨holes, holes_boolean, ?_, total_holes, ?_⟩
  · intro r
    rw [sum_holes]
    exact all_rows r
  · simp [holes, fixed_context.1, fixed_context.2.1, fixed_context.2.2, zero_occupied]

theorem no_universal_thirty_three_hole_bound :
    ¬ (∀ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) →
      (∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
        ∑ i ∈ OmissionResidual32Contexts.support r, h i) →
      h 54 = 1 → h 43 = 0 → h 67 = 0 → h 0 = 0 → 33 ≤ ∑ i, h i) := by
  intro claimed
  obtain ⟨h, hb, hr, ht, h54, h43, h67, h0⟩ := allows_thirty_two_holes
  have := claimed h hb hr h54 h43 h67 h0
  omega

#print axioms missing_card
#print axioms all_rows
#print axioms fixed_context
#print axioms zero_occupied
#print axioms holes_boolean
#print axioms sum_holes
#print axioms total_holes
#print axioms allows_thirty_two_holes
#print axioms no_universal_thirty_three_hole_bound
end OmissionResidual32Case4
