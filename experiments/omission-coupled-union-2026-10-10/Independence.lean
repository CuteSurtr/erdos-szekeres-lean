import Independent00
import Independent01
import Independent02
import Independent03
import Independent04
import Independent05
import Independent06
import Independent07
import Independent08
import Redundancy
import ErdosSzekeres.Omission.AdditionalResidualRows
import ErdosSzekeres.Omission.GeneralResidualBlocks

/-! Exactly nine of the 57 deduplicated rows independently strengthen the
original 1,187 and prior 45 rows. Each complement witness satisfies all other
56 union rows. The witness has 141 holes, so this asserts no population bound
or geometric realization. -/
namespace ErdosSzekeres.Omission.CoupledUnion
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

theorem original_rows : ∀ k : Fin 9, ∀ r : Fin 1187,
    OmissionResidual.demand r ≤
      (OmissionResidual.support r \ support (independentIndex k)).card := by
  intro k
  fin_cases k
  · exact original_rows_00
  · exact original_rows_01
  · exact original_rows_02
  · exact original_rows_03
  · exact original_rows_04
  · exact original_rows_05
  · exact original_rows_06
  · exact original_rows_07
  · exact original_rows_08

theorem prior_additional_rows : ∀ k : Fin 9, ∀ r : Fin 21,
    AdditionalResidualRows.demand r ≤
      (AdditionalResidualRows.support r \ support (independentIndex k)).card := by
  simp only [matches_literal]
  decide +kernel

theorem prior_block_rows : ∀ k : Fin 9, ∀ r : Fin 24,
    GeneralResidualBlocks.demand r ≤
      (GeneralResidualBlocks.support r \ support (independentIndex k)).card := by
  simp only [matches_literal]
  decide +kernel

theorem other_union_rows : ∀ k : Fin 9, ∀ j : Fin 57,
    j ≠ independentIndex k → 1 ≤ (support j \ support (independentIndex k)).card := by
  simp only [matches_literal]
  decide +kernel

theorem witness_hole_count : ∀ k : Fin 9,
    (Finset.univ \ support (independentIndex k)).card = 141 := by
  simp only [matches_literal]
  decide +kernel

/-- Independent additions over all original rows, all prior 45 rows, and every
other member of the deduplicated union. No total-hole budget is imposed. -/
theorem independent_each_selected_row (k : Fin 9) :
    ∃ occupied : Finset (Fin 154),
      (∀ r : Fin 1187, OmissionResidual.demand r ≤
        (OmissionResidual.support r \ occupied).card) ∧
      (∀ r : Fin 21, AdditionalResidualRows.demand r ≤
        (AdditionalResidualRows.support r \ occupied).card) ∧
      (∀ r : Fin 24, GeneralResidualBlocks.demand r ≤
        (GeneralResidualBlocks.support r \ occupied).card) ∧
      (∀ j : Fin 57, j ≠ independentIndex k → 1 ≤ (support j \ occupied).card) ∧
      ¬1 ≤ (support (independentIndex k) \ occupied).card := by
  exact ⟨support (independentIndex k), original_rows k,
    prior_additional_rows k, prior_block_rows k, other_union_rows k, by simp⟩

#print axioms original_rows
#print axioms prior_additional_rows
#print axioms prior_block_rows
#print axioms other_union_rows
#print axioms witness_hole_count
#print axioms independent_each_selected_row
end ErdosSzekeres.Omission.CoupledUnion
