import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00416
def cycles : Array (List (Fin 154)) := #[
  [61, 71, 81, 92, 112, 129, 109, 100],
  [61, 71, 81, 92, 120, 134, 109, 100],
  [63, 72, 82, 93, 103, 123, 90, 78],
  [63, 72, 82, 102, 112, 129, 90, 78],
  [63, 72, 82, 93, 103, 114, 98, 78],
  [63, 72, 82, 102, 112, 121, 98, 78],
  [63, 72, 82, 93, 103, 123, 109, 78],
  [63, 72, 82, 102, 112, 129, 109, 78],
  [63, 72, 82, 93, 103, 130, 117, 78],
  [63, 72, 82, 102, 112, 135, 117, 78],
  [63, 72, 82, 93, 103, 123, 109, 90],
  [63, 72, 82, 102, 112, 129, 109, 90],
  [63, 72, 82, 93, 103, 130, 117, 90],
  [63, 72, 82, 102, 112, 135, 117, 90],
  [66, 75, 85, 95, 105, 115, 100, 90],
  [66, 75, 85, 104, 113, 122, 100, 90],
  [66, 75, 85, 95, 114, 123, 109, 90],
  [66, 75, 85, 104, 121, 129, 109, 90],
  [67, 77, 87, 97, 106, 116, 109, 79],
  [67, 77, 96, 105, 114, 123, 109, 79],
  [67, 77, 87, 97, 106, 124, 117, 79],
  [67, 77, 96, 105, 114, 130, 117, 79],
  [73, 83, 93, 102, 112, 121, 98, 88],
  [73, 83, 93, 102, 120, 128, 98, 88],
  [73, 83, 93, 102, 120, 134, 100, 88],
  [73, 83, 93, 102, 112, 129, 109, 88],
  [73, 83, 93, 102, 120, 134, 109, 88],
  [73, 83, 93, 102, 112, 135, 117, 88],
  [73, 83, 93, 102, 120, 140, 117, 88],
  [73, 83, 93, 102, 112, 129, 109, 100],
  [73, 83, 93, 102, 120, 134, 109, 100],
  [73, 83, 93, 102, 112, 135, 117, 100]
]
def cycle (i : Fin 1164) := cycles[i.val - 416]!
theorem checked : ∀ i : Fin 1164,
    416 ≤ i.val → i.val < 448 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 416 ≤ i.val) (hhi : i.val < 448) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00416
end OmissionResidual
