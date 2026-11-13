import UnionCatalog
import Catalog

namespace ErdosSzekeres.Omission.CoupledUnion
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

theorem original_rows_03 : ∀ r : Fin 1187,
    OmissionResidual.demand r ≤
      (OmissionResidual.support r \ support (independentIndex 3)).card := by
  simp only [matches_literal]
  decide +kernel

#print axioms original_rows_03
end ErdosSzekeres.Omission.CoupledUnion
