import ResidualGeometry00000
import ResidualGeometry00032
import ResidualGeometry00064
import ResidualGeometry00096
import ResidualGeometry00128
import ResidualGeometry00160
import ResidualGeometry00192
import ResidualGeometry00224
import ResidualGeometry00256
import ResidualGeometry00288
import ResidualGeometry00320
import ResidualGeometry00352
import ResidualGeometry00384
import ResidualGeometry00416
import ResidualGeometry00448
import ResidualGeometry00480
import ResidualGeometry00512
import ResidualGeometry00544
import ResidualGeometry00576
import ResidualGeometry00608
import ResidualGeometry00640
import ResidualGeometry00672
import ResidualGeometry00704
import ResidualGeometry00736
import ResidualGeometry00768
import ResidualGeometry00800
import ResidualGeometry00832
import ResidualGeometry00864
import ResidualGeometry00896
import ResidualGeometry00928
import ResidualGeometry00960
import ResidualGeometry00992
import ResidualGeometry01024
import ResidualGeometry01056
import ResidualGeometry01088
import ResidualGeometry01120
import ResidualGeometry01152
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
theorem all_cycle_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  have hb : i.val / 32 < 37 := by have := i.isLt; omega
  generalize he : i.val / 32 = block at hb
  interval_cases block
  · exact ResidualGeometry00000.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00032.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00064.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00096.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00128.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00160.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00192.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00224.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00256.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00288.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00320.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00352.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00384.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00416.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00448.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00480.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00512.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00544.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00576.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00608.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00640.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00672.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00704.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00736.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00768.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00800.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00832.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00864.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00896.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00928.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00960.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry00992.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry01024.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry01056.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry01088.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry01120.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
  · exact ResidualGeometry01152.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)
theorem all_nonblock_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (r : Fin 1187) (hi : r.val < 1165) (skip : r.val ≠ 973) :
    demand r ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨i, rfl⟩ := cycleRow_coverage r hi skip
  exact all_cycle_rows c noCap noOctagon noJunction i
#print axioms all_cycle_rows
#print axioms all_nonblock_rows
end OmissionResidual
