import Residual124.Catalog
import ResidualBudgets

open scoped BigOperators

namespace OmissionResidual124

/-- The original 29-hole tree uses a different arithmetic packing base and
module namespace, but its literal geometric supports and demands are identical. -/
theorem catalog_matches : ∀ r : Fin 1187,
    support r = OmissionResidual.support r ∧ demand r = OmissionResidual.demand r := by
  decide +kernel

/-- Transfer only the proved finite exclusion across the checked catalog
equality. This lemma does not presuppose that the original root has passed. -/
theorem exclusion_transfer
    (verified : ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ 29) :
    OmissionResidual.ExcludesHoleBudget 29 := by
  rintro ⟨holes, hb, hr, hc⟩
  apply verified
  refine ⟨holes, hb, ?_, hc⟩
  intro r
  rw [(catalog_matches r).1, (catalog_matches r).2]
  exact hr r

#print axioms catalog_matches
#print axioms exclusion_transfer

end OmissionResidual124
