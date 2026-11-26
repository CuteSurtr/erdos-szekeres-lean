import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00960
def cycles : Array (List (Fin 154)) := #[
  [61, 71, 81, 92, 120, 128, 98, 88, 76],
  [61, 71, 81, 92, 112, 129, 109, 100, 76],
  [61, 71, 81, 92, 120, 134, 109, 100, 76],
  [63, 72, 82, 93, 103, 123, 109, 90, 78],
  [63, 72, 82, 102, 112, 129, 109, 90, 78],
  [63, 72, 82, 93, 103, 130, 117, 90, 78],
  [63, 72, 82, 102, 112, 135, 117, 90, 78],
  [73, 83, 93, 102, 112, 129, 109, 100, 88],
  [73, 83, 93, 102, 120, 134, 109, 100, 88],
  [73, 83, 93, 102, 112, 135, 117, 100, 88],
  [73, 83, 93, 102, 120, 140, 117, 100, 88],
  [84, 94, 103, 112, 120, 140, 117, 109, 98],
  [84, 94, 103, 112, 120, 144, 117, 109, 98],
  [2, 7, 12, 20, 30, 43, 33, 25],
  [11, 30, 39, 50, 62, 110, 101, 91],
  [16, 30, 39, 50, 62, 110, 101, 91],
  [16, 30, 49, 60, 72, 118, 111, 91],
  [17, 43, 53, 65, 77, 89, 110, 101, 91],
  [23, 30, 49, 60, 72, 118, 111, 101],
  [23, 30, 59, 70, 82, 125, 111, 101],
  [24, 39, 49, 60, 72, 118, 111, 91],
  [24, 39, 49, 71, 83, 126, 119, 91],
  [25, 33, 44, 55, 67, 79, 101, 91],
  [25, 43, 53, 65, 77, 89, 110, 101, 91],
  [25, 43, 64, 75, 87, 99, 118, 111, 91],
  [31, 39, 49, 60, 72, 118, 111, 101],
  [31, 39, 49, 71, 83, 126, 119, 101],
  [31, 39, 59, 70, 82, 125, 111, 101],
  [31, 39, 59, 81, 93, 131, 119, 101],
  [32, 50, 60, 71, 83, 126, 119, 91],
  [32, 50, 60, 71, 94, 132, 127, 91],
  [33, 43, 53, 65, 77, 89, 110, 101]
]
def cycle (i : Fin 1164) := cycles[i.val - 960]!
theorem checked : ∀ i : Fin 1164,
    960 ≤ i.val → i.val < 992 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 960 ≤ i.val) (hhi : i.val < 992) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00960
end OmissionResidual
