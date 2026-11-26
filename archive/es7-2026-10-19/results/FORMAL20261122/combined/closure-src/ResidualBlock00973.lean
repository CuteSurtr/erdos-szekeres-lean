import Catalog
import ErdosSzekeres.Omission.BlockGeometry
open ErdosSzekeres ErdosSzekeres.Omission BlockCompression
namespace OmissionResidual.ResidualBlock00973
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
def block : Block := { rowId := 973, support := [91, 101, 110, 111, 118, 119, 125, 126, 127, 131, 132, 133, 136, 137, 138, 139, 141, 142, 143, 145, 146, 147, 148, 149, 150, 151, 152, 153], thresholds := [3, 3, 3, 3, 3, 3], active := [(3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6)] }
def row : Fin 1187 := 973
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
end OmissionResidual.ResidualBlock00973
