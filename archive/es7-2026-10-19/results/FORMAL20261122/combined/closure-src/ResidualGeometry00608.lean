import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00608
def cycles : Array (List (Fin 154)) := #[
  [24, 39, 49, 72, 87, 78, 56, 34],
  [24, 39, 49, 71, 97, 88, 56, 34],
  [24, 39, 50, 62, 89, 79, 68, 34],
  [24, 39, 49, 60, 99, 90, 68, 34],
  [24, 39, 49, 72, 99, 90, 68, 34],
  [24, 39, 60, 72, 99, 90, 68, 34],
  [24, 39, 49, 71, 108, 100, 68, 34],
  [24, 39, 71, 83, 108, 100, 68, 34],
  [26, 35, 69, 81, 95, 86, 75, 64],
  [26, 35, 80, 92, 104, 86, 75, 64],
  [27, 46, 57, 70, 85, 75, 65, 53],
  [27, 46, 69, 81, 95, 86, 65, 53],
  [27, 46, 57, 82, 96, 87, 77, 53],
  [27, 46, 69, 93, 105, 97, 77, 53],
  [28, 36, 46, 69, 81, 61, 51, 40],
  [28, 36, 46, 80, 92, 61, 51, 40],
  [28, 36, 46, 69, 93, 73, 63, 40],
  [28, 36, 46, 80, 102, 73, 63, 40],
  [28, 36, 58, 71, 86, 76, 66, 54],
  [28, 36, 58, 83, 97, 88, 78, 54],
  [28, 36, 46, 69, 105, 88, 78, 54],
  [29, 37, 47, 58, 83, 73, 52, 41],
  [29, 37, 57, 69, 93, 73, 52, 41],
  [29, 37, 47, 58, 94, 84, 52, 41],
  [29, 37, 57, 69, 103, 84, 52, 41],
  [29, 37, 47, 72, 87, 78, 67, 55],
  [29, 37, 57, 82, 96, 78, 67, 55],
  [29, 37, 47, 94, 106, 98, 67, 55],
  [29, 37, 58, 94, 106, 98, 67, 55],
  [29, 47, 58, 94, 106, 98, 67, 55],
  [29, 37, 57, 103, 114, 98, 67, 55],
  [30, 59, 70, 82, 96, 87, 77, 43]
]
def cycle (i : Fin 1164) := cycles[i.val - 608]!
theorem checked : ∀ i : Fin 1164,
    608 ≤ i.val → i.val < 640 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 608 ≤ i.val) (hhi : i.val < 640) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00608
end OmissionResidual
