import ErdosSzekeres.Suk.ChainAntichain
import Mathlib.Data.Finset.Sort

namespace ErdosSzekeres.Suk

/-- A finite chain in a partial order has a strictly increasing enumeration.
This bridges the finite-set output of Dilworth to the ordered cups-caps input. -/
theorem enumerate_finset_chain {α : Type*} [PartialOrder α] (s : Finset α)
    (hs : DilworthTheorem.IsChain (s : Set α)) :
    ∃ f : Fin s.card → α, StrictMono f ∧ ∀ x, x ∈ s ↔ ∃ i, f i = x := by
  classical
  letI : LinearOrder ↥s := {
    __ := inferInstanceAs (PartialOrder ↥s)
    le_total := fun a b => hs a.val b.val a.property b.property
    toDecidableLE := Classical.decRel _ }
  let e : Fin s.card ≃o ↥s :=
    Fintype.orderIsoFinOfCardEq ↥s (by simp)
  refine ⟨fun i => (e i).val, ?_, ?_⟩
  · intro i j hij
    exact e.strictMono hij
  · intro x
    constructor
    · intro hx
      exact ⟨e.symm ⟨x, hx⟩, by simp⟩
    · rintro ⟨i, rfl⟩
      exact (e i).property

end ErdosSzekeres.Suk
