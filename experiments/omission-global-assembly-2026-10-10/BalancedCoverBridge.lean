import BalancedCoverProof.Catalog
import BalancedCoverCuts
import BalancedBudgets

open scoped BigOperators

namespace OmissionBalancedCover

set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def baseIndex (r : Fin 2685) : Fin 2905 := ⟨r.val, by omega⟩
def cutIndex (r : Fin 220) : Fin 2905 := ⟨2685 + r.val, by omega⟩

theorem base_catalog_matches : ∀ r : Fin 2685,
    support (baseIndex r) = OmissionBalanced.support r ∧
    demand (baseIndex r) = OmissionBalanced.demand r := by
  decide +kernel

theorem cut_catalog_matches : ∀ r : Fin 220,
    support (cutIndex r) = BalancedCoverCuts.support r ∧
    demand (cutIndex r) = BalancedCoverCuts.demand r := by
  decide +kernel

theorem all_cover_rows (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    ∀ r : Fin 2905, demand r ≤ ∑ i ∈ support r, holes i := by
  intro r
  by_cases h : r.val < 2685
  · let b : Fin 2685 := ⟨r.val, h⟩
    have hi : baseIndex b = r := Fin.ext rfl
    rw [← hi, (base_catalog_matches b).1, (base_catalog_matches b).2]
    exact hrows b
  · let b : Fin 220 := ⟨r.val - 2685, by omega⟩
    have hi : cutIndex b = r := Fin.ext (by dsimp [cutIndex, b]; omega)
    rw [← hi, (cut_catalog_matches b).1, (cut_catalog_matches b).2]
    exact BalancedCoverCuts.all_rows holes hbool hrows b

theorem exclusion_transfer {budget : ℕ}
    (verified : ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget) :
    OmissionBalanced.ExcludesHoleBudget budget := by
  rintro ⟨holes, hb, hr, hc⟩
  exact verified ⟨holes, hb, all_cover_rows holes hb hr, hc⟩

#print axioms base_catalog_matches
#print axioms cut_catalog_matches
#print axioms all_cover_rows
#print axioms exclusion_transfer

end OmissionBalancedCover
