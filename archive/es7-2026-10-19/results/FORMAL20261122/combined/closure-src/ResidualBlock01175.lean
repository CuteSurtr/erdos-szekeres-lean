import Catalog
import ErdosSzekeres.Omission.BlockGeometry
open ErdosSzekeres ErdosSzekeres.Omission BlockCompression
namespace OmissionResidual.ResidualBlock01175
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
def block : Block := { rowId := 1175, support := [34, 44, 53, 54, 64, 74, 76, 86, 88, 95, 97, 100, 104, 105, 108, 113, 115, 119, 122, 126, 128, 131, 134, 136, 140, 145, 148, 151], thresholds := [3, 3, 3, 2, 2, 2], active := [(1,6), (2,3), (2,4), (2,5), (2,6), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,1), (4,2), (4,3), (4,4)] }
def row : Fin 1187 := 1175
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
end OmissionResidual.ResidualBlock01175
