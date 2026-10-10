import ErdosSzekeres.Omission.CoupledTemplateFourthGeometry
import ErdosSzekeres.Omission.CoupledTemplateFourthCheck
import Witness

namespace ErdosSzekeres.Omission.CoupledFourthWitnessVariant
open CoupledTemplateFourth
open scoped BigOperators
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def states : Fin 13 → Fin 154 := ![6,14,20,21,11,27,29,32,17,37,41,45,65]
def support : Finset (Fin 154) := Finset.univ.image states

theorem checked : Function.Injective states ∧ Compatible states := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    1 ≤ (support \ c.residualOccupied noCap noOctagon noJunction).card :=
  CoupledTemplateFourth.hole_bound states checked.1 checked.2
    c noCap noOctagon noJunction

theorem witness_violates_row :
    ¬ 1 ≤ (support ∩ OmissionResidual32Case4.missing).card := by decide +kernel

theorem strict_strengthening :
    ∃ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) ∧
      (∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
        ∑ i ∈ OmissionResidual32Contexts.support r, h i) ∧
      (∑ i, h i) = 32 ∧ h 0 = 0 ∧ ¬ 1 ≤ ∑ i ∈ support, h i := by
  refine ⟨OmissionResidual32Case4.holes, OmissionResidual32Case4.holes_boolean,
    ?_, OmissionResidual32Case4.total_holes, ?_, ?_⟩
  · intro r
    rw [OmissionResidual32Case4.sum_holes]
    exact OmissionResidual32Case4.all_rows r
  · simp [OmissionResidual32Case4.holes, OmissionResidual32Case4.zero_occupied]
  · rw [OmissionResidual32Case4.sum_holes]
    exact witness_violates_row

#print axioms checked
#print axioms hole_bound
#print axioms witness_violates_row
#print axioms strict_strengthening
end ErdosSzekeres.Omission.CoupledFourthWitnessVariant
