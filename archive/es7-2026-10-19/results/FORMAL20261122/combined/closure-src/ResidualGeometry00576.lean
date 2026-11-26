import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00576
def cycles : Array (List (Fin 154)) := #[
  [20, 46, 57, 70, 85, 75, 65, 43],
  [20, 46, 57, 82, 96, 87, 77, 43],
  [21, 27, 36, 47, 60, 51, 41, 31],
  [21, 27, 46, 57, 70, 51, 41, 31],
  [21, 27, 36, 58, 71, 61, 41, 31],
  [21, 27, 46, 69, 81, 61, 41, 31],
  [21, 27, 36, 47, 72, 63, 52, 31],
  [21, 27, 46, 57, 82, 63, 52, 31],
  [21, 27, 36, 58, 83, 73, 52, 31],
  [21, 27, 46, 69, 93, 73, 52, 31],
  [21, 27, 36, 60, 75, 66, 55, 44],
  [22, 37, 47, 58, 83, 73, 42, 32],
  [22, 37, 47, 58, 94, 84, 42, 32],
  [22, 37, 47, 72, 87, 78, 56, 45],
  [22, 37, 58, 94, 106, 98, 56, 45],
  [22, 47, 58, 94, 106, 98, 56, 45],
  [23, 30, 49, 60, 75, 66, 55, 33],
  [23, 30, 59, 70, 85, 66, 55, 33],
  [23, 30, 49, 60, 87, 78, 67, 33],
  [23, 30, 59, 70, 96, 78, 67, 33],
  [23, 30, 49, 60, 99, 90, 79, 33],
  [23, 30, 49, 72, 99, 90, 79, 33],
  [23, 30, 60, 72, 99, 90, 79, 33],
  [23, 49, 60, 72, 99, 90, 79, 33],
  [23, 30, 59, 70, 107, 90, 79, 33],
  [23, 30, 59, 82, 107, 90, 79, 33],
  [23, 30, 70, 82, 107, 90, 79, 33],
  [23, 59, 70, 82, 107, 90, 79, 33],
  [24, 39, 49, 60, 75, 66, 45, 34],
  [24, 39, 49, 71, 86, 76, 45, 34],
  [24, 39, 50, 62, 77, 67, 56, 34],
  [24, 39, 49, 60, 87, 78, 56, 34]
]
def cycle (i : Fin 1164) := cycles[i.val - 576]!
theorem checked : ∀ i : Fin 1164,
    576 ≤ i.val → i.val < 608 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 576 ≤ i.val) (hhi : i.val < 608) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00576
end OmissionResidual
