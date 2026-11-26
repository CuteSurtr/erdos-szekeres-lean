import Catalog
import ErdosSzekeres.Omission.ResidualCycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
/-- Cycle rows omit row 973 and the final 22 block rows. -/
def cycleRow (i : Fin 1164) : Fin 1187 :=
  ⟨if i.val < 973 then i.val else i.val + 1, by split <;> have := i.isLt <;> omega⟩
theorem cycleRow_coverage (r : Fin 1187) (hi : r.val < 1165)
    (skip : r.val ≠ 973) : ∃ i : Fin 1164, cycleRow i = r := by
  by_cases h : r.val < 973
  · refine ⟨⟨r.val, by omega⟩, ?_⟩
    apply Fin.ext; simp [cycleRow, h]
  · refine ⟨⟨r.val - 1, by omega⟩, ?_⟩
    apply Fin.ext; simp only [cycleRow]; split <;> omega
end OmissionResidual
