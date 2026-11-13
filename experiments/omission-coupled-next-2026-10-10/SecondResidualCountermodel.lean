import Catalog
import ErdosSzekeres.Omission.CoupledVariants
import ErdosSzekeres.Omission.AdditionalResidualRows
import ErdosSzekeres.Omission.GeneralResidualBlocks

/-! A Boolean countermodel to excluding 32 holes from the original omission
rows. No realization by real points is claimed. -/
namespace SecondResidualCountermodel
open scoped BigOperators
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

def missing : Finset (Fin 154) :=
  {12,26,27,33,44,45,46,47,54,56,67,68,69,70,71,78,85,89,97,98,99,100,101,109,111,117,119,124,126,127,132,138}

theorem missing_card : missing.card = 32 := by decide +kernel

theorem original_rows : ∀ r : Fin 1187,
    OmissionResidual.demand r ≤ (OmissionResidual.support r ∩ missing).card := by
  decide +kernel

theorem prior_additional_rows : ∀ r : Fin 21,
    ErdosSzekeres.Omission.AdditionalResidualRows.demand r ≤
      (ErdosSzekeres.Omission.AdditionalResidualRows.support r ∩ missing).card := by
  decide +kernel

theorem general_block_rows : ∀ r : Fin 24,
    ErdosSzekeres.Omission.GeneralResidualBlocks.demand r ≤
      (ErdosSzekeres.Omission.GeneralResidualBlocks.support r ∩ missing).card := by
  decide +kernel

theorem prior_coupled_rows : ∀ r : Fin 42,
    1 ≤ (ErdosSzekeres.Omission.CoupledVariants.support r ∩ missing).card := by
  decide +kernel

/-- The thirteen-state support under investigation is fully occupied in this
abstract witness; this definition alone asserts no geometric property. -/
def coupledCandidate : Finset (Fin 154) :=
  {16,25,30,39,43,50,53,62,65,77,79,91,110}

theorem candidate_occupied : coupledCandidate ∩ missing = ∅ := by decide +kernel

def holes (i : Fin 154) : ℕ := if i ∈ missing then 1 else 0

theorem holes_bool (i : Fin 154) : holes i ≤ 1 := by
  unfold holes
  split_ifs <;> omega

theorem sum_holes (s : Finset (Fin 154)) :
    (∑ i ∈ s, holes i) = (s ∩ missing).card := by
  simp [holes]

theorem total_holes : (∑ i, holes i) = 32 := by
  simpa using (sum_holes Finset.univ).trans (by simpa using missing_card)

theorem allows_thirty_two_holes :
    ∃ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) ∧
      (∀ r : Fin 1187, OmissionResidual.demand r ≤
        ∑ i ∈ OmissionResidual.support r, h i) ∧ (∑ i, h i) = 32 := by
  refine ⟨holes, holes_bool, ?_, total_holes⟩
  intro r
  rw [sum_holes]
  exact original_rows r

#print axioms missing_card
#print axioms original_rows
#print axioms prior_additional_rows
#print axioms general_block_rows
#print axioms prior_coupled_rows
#print axioms candidate_occupied
#print axioms allows_thirty_two_holes
end SecondResidualCountermodel
