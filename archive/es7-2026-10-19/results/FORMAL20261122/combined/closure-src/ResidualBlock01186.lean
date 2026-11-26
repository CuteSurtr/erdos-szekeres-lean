import Catalog
import ErdosSzekeres.Omission.BlockGeometry
open ErdosSzekeres ErdosSzekeres.Omission BlockCompression
namespace OmissionResidual.ResidualBlock01186
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
def block : Block := { rowId := 1186, support := [68, 79, 89, 90, 99, 100, 107, 108, 109, 115, 116, 117, 122, 123, 124, 129, 130, 134, 135, 139, 140, 143, 144, 147, 149, 151, 152, 153], thresholds := [3, 3, 3, 3, 3, 3], active := [(1,6), (2,6), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6)] }
def row : Fin 1187 := 1186
theorem checked : pairsOK block = true ∧ growthOK block = true ∧
    block.support.toFinset = (support row).image Fin.val ∧
    demand row = (support row).card - 22 := by decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    : demand row ≤ (support row \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨pairs, growth, hs, hd⟩ := checked
  rw [hd]
  exact BlockGeometry.block_hole_bound c noCap noOctagon noJunction block pairs growth (support row) hs
#print axioms row_bound
end OmissionResidual.ResidualBlock01186
