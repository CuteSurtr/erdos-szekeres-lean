import Catalog
import ErdosSzekeres.Omission.AdditionalResidualRows

namespace AdditionalResidualStrictness
open ErdosSzekeres.Omission.AdditionalResidualRows
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

-- This abstract 23-state witness has no claimed geometric realization.
def blockWitness : Finset (Fin 154) := {17, 33, 34, 45, 54, 56, 66, 68, 76, 78, 88, 90, 91, 98, 100, 101, 109, 111, 117, 119, 127, 133, 139}

theorem original_rows_allow_block : ∀ r : Fin 1187,
    OmissionResidual.demand r ≤ (OmissionResidual.support r \ blockWitness).card := by
  decide +kernel

theorem new_cycles_allow_block : ∀ i : Fin 20,
    1 ≤ ((cycle i).toFinset \ blockWitness).card := by
  decide +kernel

theorem block_witness_checked : blockWitness.card = 23 ∧
    (blockSupport \ blockWitness).card = 5 := by
  decide +kernel

#print axioms original_rows_allow_block
#print axioms new_cycles_allow_block
#print axioms block_witness_checked
end AdditionalResidualStrictness
