import ErdosSzekeres.Omission.CoupledCoreNine

/-! A coupled orientation/rank obstruction on nine residual states.
Unlike the earlier separate cycle and compression tests, the certificate uses
one chronological order and one shared pair label for all selected owners. -/

namespace ErdosSzekeres.Omission.CoupledCoreNine
open Coupled
set_option maxHeartbeats 10000000
set_option maxRecDepth 10000

theorem states_injective : Function.Injective states := by decide +kernel

/-- Every actual residual configuration omits at least one of the nine
literal states. The owners are extracted from this one ambient configuration. -/
theorem exists_missing_state {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ s ∈ support, s ∉ c.residualOccupied noCap noOctagon noJunction := by
  classical
  by_contra! h
  have selected : ∀ i : Fin 9, ∃ v : Fin n,
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
  let C : Context 9 n states := {
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

#print axioms exists_missing_state
#print axioms hole_bound
end ErdosSzekeres.Omission.CoupledCoreNine
