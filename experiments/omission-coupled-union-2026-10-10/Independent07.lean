import UnionCatalog
import Catalog

namespace ErdosSzekeres.Omission.CoupledUnion
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

theorem original_rows_07 : ∀ r : Fin 1187,
    OmissionResidual.demand r ≤
      (OmissionResidual.support r \ support (independentIndex 7)).card := by
  simp only [matches_literal]
  decide +kernel

#print axioms original_rows_07
end ErdosSzekeres.Omission.CoupledUnion
