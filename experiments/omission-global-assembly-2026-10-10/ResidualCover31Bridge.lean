import ResidualCover31Proof.Catalog
import ResidualCoverCuts
import ResidualBudgets

open scoped BigOperators

namespace OmissionResidualCover31

set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def baseIndex (r : Fin 1187) : Fin 1589 := ⟨r.val, by omega⟩
def cutIndex (r : Fin 402) : Fin 1589 := ⟨1187 + r.val, by omega⟩

theorem base_catalog_matches : ∀ r : Fin 1187,
    support (baseIndex r) = OmissionResidual.support r ∧
    demand (baseIndex r) = OmissionResidual.demand r := by
  decide +kernel

theorem cut_catalog_matches : ∀ r : Fin 402,
    support (cutIndex r) = ResidualCoverCuts.support r ∧
    demand (cutIndex r) = ResidualCoverCuts.demand r := by
  decide +kernel

theorem all_cover_rows (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    ∀ r : Fin 1589, demand r ≤ ∑ i ∈ support r, holes i := by
  intro r
  by_cases h : r.val < 1187
  · let b : Fin 1187 := ⟨r.val, h⟩
    have hi : baseIndex b = r := Fin.ext rfl
    rw [← hi, (base_catalog_matches b).1, (base_catalog_matches b).2]
    exact hrows b
  · let b : Fin 402 := ⟨r.val - 1187, by omega⟩
    have hi : cutIndex b = r := Fin.ext (by dsimp [cutIndex, b]; omega)
    rw [← hi, (cut_catalog_matches b).1, (cut_catalog_matches b).2]
    exact ResidualCoverCuts.all_rows holes hbool hrows b

theorem exclusion_transfer {budget : ℕ}
    (verified : ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget) :
    OmissionResidual.ExcludesHoleBudget budget := by
  rintro ⟨holes, hb, hr, hc⟩
  exact verified ⟨holes, hb, all_cover_rows holes hb hr, hc⟩

#print axioms base_catalog_matches
#print axioms cut_catalog_matches
#print axioms all_cover_rows
#print axioms exclusion_transfer

end OmissionResidualCover31
