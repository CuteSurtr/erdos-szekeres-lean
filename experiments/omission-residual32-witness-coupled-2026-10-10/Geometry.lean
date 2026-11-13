import LeanCore
import Witness

/-! A coupled orientation/rank obstruction on thirteen residual states.
Unlike the earlier separate cycle and compression tests, the certificate uses
one chronological order and one shared pair label for all selected owners. -/

namespace ErdosSzekeres.Omission.CoupledCoreSixth
open Coupled
set_option maxHeartbeats 10000000
set_option maxRecDepth 10000

theorem states_injective : Function.Injective states := by decide +kernel

/-- Every actual residual configuration omits at least one of the thirteen
literal states. The owners are extracted from this one ambient configuration. -/
theorem exists_missing_state {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ s ∈ support, s ∉ c.residualOccupied noCap noOctagon noJunction := by
  classical
  by_contra! h
  have selected : ∀ i : Fin 13, ∃ v : Fin n,
      c.residualOwner noCap noOctagon noJunction v = states i := by
    intro i
    have hi : states i ∈ support := List.get_mem support i
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp (h (states i) hi)
    exact ⟨v, hv⟩
  choose owner owner_state using selected
  have injective : Function.Injective owner := by
    intro i j he
    apply states_injective
    rw [← owner_state i, ← owner_state j, he]
  let C : Context 13 n states := {
    config := c, noCap := noCap, noOctagon := noOctagon, noJunction := noJunction,
    owner := owner, injective := injective, owner_state := owner_state,
    nonzero := fun i j l hij hil hjl => c.orient_ne_of_distinct _ _ _
      (injective.ne hij) (injective.ne hil) (injective.ne hjl) }
  exact context_impossible C

/-- A universally valid demand-one omission row on this literal support. -/
theorem hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    1 ≤ (support.toFinset \ c.residualOccupied noCap noOctagon noJunction).card := by
  classical
  obtain ⟨s, hs, hmissing⟩ := exists_missing_state c noCap noOctagon noJunction
  exact Finset.one_le_card.mpr ⟨s, Finset.mem_sdiff.mpr ⟨List.mem_toFinset.mpr hs, hmissing⟩⟩

open scoped BigOperators

theorem witness_violates_coupled :
    ¬ 1 ≤ (support.toFinset ∩ OmissionResidual32Case4.missing).card := by
  decide +kernel

/-- This new row is independent of every one of the exact 2469 frozen rows,
even restricted to the witnessed 32-hole assignment with occupied state zero. -/
theorem strict_strengthening :
    ∃ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) ∧
      (∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
        ∑ i ∈ OmissionResidual32Contexts.support r, h i) ∧
      (∑ i, h i) = 32 ∧ h 0 = 0 ∧ ¬ 1 ≤ ∑ i ∈ support.toFinset, h i := by
  refine ⟨OmissionResidual32Case4.holes, OmissionResidual32Case4.holes_boolean,
    ?_, OmissionResidual32Case4.total_holes, ?_, ?_⟩
  · intro r
    rw [OmissionResidual32Case4.sum_holes]
    exact OmissionResidual32Case4.all_rows r
  · simp [OmissionResidual32Case4.holes, OmissionResidual32Case4.zero_occupied]
  · rw [OmissionResidual32Case4.sum_holes]
    exact witness_violates_coupled

theorem countermodel_not_realizable {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    c.residualOccupied noCap noOctagon noJunction ≠
      Finset.univ \ OmissionResidual32Case4.missing := by
  intro he
  have bound := hole_bound c noCap noOctagon noJunction
  rw [he] at bound
  have eq : support.toFinset \ (Finset.univ \ OmissionResidual32Case4.missing) =
      support.toFinset ∩ OmissionResidual32Case4.missing := by ext i; simp
  exact witness_violates_coupled (eq ▸ bound)

#print axioms states_injective
#print axioms witness_violates_coupled
#print axioms strict_strengthening
#print axioms countermodel_not_realizable
#print axioms exists_missing_state
#print axioms hole_bound
end ErdosSzekeres.Omission.CoupledCoreSixth
