import ErdosSzekeres.Omission.CoupledTemplateThird

namespace ErdosSzekeres.Omission.CoupledTemplateThird
open Coupled

/-- Generic owner extraction for any injective support passing the frozen
core's finite compatibility tests. -/
theorem exists_missing_index (σ : Fin 13 → Fin 154) (injective : Function.Injective σ)
    (compatible : Compatible σ) {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ i, σ i ∉ c.residualOccupied noCap noOctagon noJunction := by
  classical
  by_contra! h
  have selected : ∀ i : Fin 13, ∃ v : Fin n,
      c.residualOwner noCap noOctagon noJunction v = σ i := by
    intro i
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp (h i)
    exact ⟨v, hv⟩
  choose owner owner_state using selected
  have owner_injective : Function.Injective owner := by
    intro i j he
    apply injective
    rw [← owner_state i, ← owner_state j, he]
  let C : Context 13 n σ := {
    config := c, noCap := noCap, noOctagon := noOctagon, noJunction := noJunction,
    owner := owner, injective := owner_injective, owner_state := owner_state,
    nonzero := fun i j l hij hil hjl => c.orient_ne_of_distinct _ _ _
      (owner_injective.ne hij) (owner_injective.ne hil) (owner_injective.ne hjl) }
  exact context_impossible compatible C

theorem hole_bound (σ : Fin 13 → Fin 154) (injective : Function.Injective σ)
    (compatible : Compatible σ) {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    1 ≤ ((Finset.univ.image σ) \ c.residualOccupied noCap noOctagon noJunction).card := by
  classical
  obtain ⟨i, hmissing⟩ := exists_missing_index σ injective compatible c noCap noOctagon noJunction
  exact Finset.one_le_card.mpr ⟨σ i, Finset.mem_sdiff.mpr
    ⟨Finset.mem_image.mpr ⟨i, Finset.mem_univ _, rfl⟩, hmissing⟩⟩

#print axioms hole_bound
end ErdosSzekeres.Omission.CoupledTemplateThird
