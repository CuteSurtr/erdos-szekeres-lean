import Catalog
import ErdosSzekeres.Omission.AdditionalResidualRows

namespace AdditionalResidualStrictness
open ErdosSzekeres.Omission.AdditionalResidualRows
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

-- An abstract occupied set, not a realizable configuration.
theorem original_rows_allow_each_cycle : ∀ i : Fin 20, ∀ r : Fin 1187,
    OmissionResidual.demand r ≤
      (OmissionResidual.support r \ (cycle i).toFinset).card := by
  decide +kernel

theorem each_cycle_violates_its_new_row (i : Fin 20) :
    ¬ 1 ≤ ((cycle i).toFinset \ (cycle i).toFinset).card := by
  simp

#print axioms original_rows_allow_each_cycle
#print axioms each_cycle_violates_its_new_row
end AdditionalResidualStrictness
