import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry01120
def cycles : Array (List (Fin 154)) := #[
  [97, 105, 113, 128, 140, 148, 138, 126],
  [98, 106, 114, 121, 128, 140, 148, 133, 127],
  [98, 106, 114, 121, 128, 144, 150, 133, 127],
  [98, 106, 114, 121, 128, 134, 145, 127],
  [99, 107, 115, 123, 130, 142, 138, 118],
  [99, 107, 115, 123, 130, 147, 143, 118],
  [99, 107, 122, 129, 135, 146, 138, 118],
  [99, 107, 122, 129, 135, 149, 143, 118],
  [100, 108, 115, 122, 129, 141, 127, 119],
  [100, 108, 115, 122, 129, 135, 146, 133, 119],
  [100, 108, 115, 122, 129, 135, 149, 139, 119],
  [100, 108, 115, 122, 134, 140, 148, 133, 119],
  [100, 108, 115, 122, 134, 140, 151, 139, 119],
  [100, 108, 115, 123, 130, 142, 133, 119],
  [100, 108, 115, 123, 130, 147, 139, 119],
  [101, 110, 118, 126, 132, 138, 143, 139],
  [101, 110, 125, 131, 137, 142, 147, 139],
  [106, 114, 121, 128, 140, 148, 138, 132],
  [106, 114, 121, 128, 144, 150, 138, 132],
  [108, 115, 122, 129, 135, 146, 138, 126],
  [108, 115, 122, 129, 135, 149, 143, 126],
  [108, 115, 122, 134, 140, 148, 138, 126],
  [108, 115, 122, 134, 140, 151, 143, 126],
  [109, 116, 123, 129, 134, 140, 148, 133, 127],
  [109, 116, 123, 129, 134, 144, 150, 133, 127],
  [109, 116, 123, 129, 134, 140, 151, 139, 127],
  [109, 116, 123, 129, 134, 144, 152, 139, 127],
  [111, 118, 125, 131, 137, 142, 147, 139],
  [111, 118, 125, 136, 141, 146, 149, 139],
  [116, 123, 129, 134, 140, 148, 138, 132],
  [116, 123, 129, 134, 144, 150, 138, 132],
  [116, 123, 129, 134, 140, 151, 143, 132]
]
def cycle (i : Fin 1164) := cycles[i.val - 1120]!
theorem checked : ∀ i : Fin 1164,
    1120 ≤ i.val → i.val < 1152 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 1120 ≤ i.val) (hhi : i.val < 1152) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry01120
end OmissionResidual
