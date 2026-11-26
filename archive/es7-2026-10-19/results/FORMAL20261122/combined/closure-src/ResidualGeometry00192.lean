import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00192
def cycles : Array (List (Fin 154)) := #[
  [23, 30, 59, 70, 82, 107, 79, 33],
  [23, 30, 49, 60, 72, 99, 90, 33],
  [23, 30, 59, 70, 82, 107, 90, 33],
  [23, 30, 49, 60, 72, 87, 78, 67],
  [23, 30, 59, 70, 82, 96, 78, 67],
  [23, 30, 49, 60, 72, 99, 90, 79],
  [23, 30, 59, 70, 82, 107, 90, 79],
  [24, 31, 40, 51, 63, 78, 56, 34],
  [24, 39, 49, 60, 72, 87, 56, 34],
  [24, 31, 40, 61, 73, 88, 56, 34],
  [24, 39, 49, 71, 83, 97, 56, 34],
  [24, 31, 40, 51, 63, 90, 68, 34],
  [24, 39, 49, 60, 72, 99, 68, 34],
  [24, 31, 40, 61, 73, 100, 68, 34],
  [24, 39, 49, 71, 83, 108, 68, 34],
  [24, 39, 49, 60, 72, 87, 78, 34],
  [24, 39, 49, 71, 83, 97, 88, 34],
  [24, 39, 49, 60, 72, 99, 90, 34],
  [24, 39, 49, 71, 83, 108, 100, 34],
  [24, 39, 49, 60, 72, 87, 78, 56],
  [24, 39, 49, 71, 83, 97, 88, 56],
  [24, 39, 49, 60, 72, 99, 90, 68],
  [24, 39, 49, 71, 83, 108, 100, 68],
  [25, 43, 53, 65, 77, 89, 79, 68],
  [25, 43, 64, 75, 87, 99, 90, 68],
  [28, 36, 46, 57, 70, 85, 66, 54],
  [28, 36, 46, 69, 81, 95, 66, 54],
  [28, 36, 46, 80, 92, 104, 66, 54],
  [28, 36, 46, 69, 81, 95, 76, 54],
  [28, 36, 46, 80, 92, 104, 76, 54],
  [28, 36, 46, 57, 82, 96, 78, 54],
  [28, 36, 46, 69, 93, 105, 78, 54]
]
def cycle (i : Fin 1164) := cycles[i.val - 192]!
theorem checked : ∀ i : Fin 1164,
    192 ≤ i.val → i.val < 224 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 192 ≤ i.val) (hhi : i.val < 224) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00192
end OmissionResidual
