import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00864
def cycles : Array (List (Fin 154)) := #[
  [9, 18, 26, 58, 71, 86, 76, 45, 34],
  [10, 20, 27, 37, 50, 65, 55, 45, 25],
  [10, 20, 36, 47, 60, 75, 66, 45, 25],
  [10, 20, 27, 37, 62, 77, 67, 56, 25],
  [10, 20, 36, 47, 72, 87, 78, 56, 25],
  [11, 30, 39, 50, 62, 77, 67, 56, 17],
  [11, 30, 39, 50, 62, 89, 79, 68, 17],
  [13, 18, 26, 47, 60, 75, 66, 55, 44],
  [13, 18, 35, 57, 70, 85, 66, 55, 44],
  [13, 18, 26, 58, 71, 86, 76, 55, 44],
  [13, 18, 35, 69, 81, 95, 76, 55, 44],
  [14, 20, 36, 47, 60, 75, 66, 55, 33],
  [14, 20, 46, 57, 70, 85, 66, 55, 33],
  [14, 20, 36, 47, 72, 87, 78, 67, 33],
  [14, 20, 46, 57, 82, 96, 78, 67, 33],
  [15, 27, 36, 47, 60, 75, 66, 45, 34],
  [15, 27, 36, 58, 71, 86, 76, 45, 34],
  [15, 27, 36, 47, 72, 87, 78, 56, 34],
  [15, 27, 36, 58, 83, 97, 88, 56, 34],
  [16, 30, 39, 50, 62, 77, 67, 56, 25],
  [16, 30, 49, 60, 72, 87, 78, 56, 25],
  [16, 30, 39, 50, 62, 89, 79, 68, 25],
  [16, 30, 49, 60, 72, 99, 90, 68, 25],
  [19, 26, 35, 69, 81, 95, 76, 66, 54],
  [19, 26, 35, 80, 92, 104, 76, 66, 54],
  [21, 27, 36, 47, 60, 75, 66, 55, 44],
  [21, 27, 46, 57, 70, 85, 66, 55, 44],
  [21, 27, 36, 58, 71, 86, 76, 55, 44],
  [21, 27, 46, 69, 81, 95, 76, 55, 44],
  [21, 27, 36, 47, 72, 87, 78, 67, 44],
  [21, 27, 46, 57, 82, 96, 78, 67, 44],
  [21, 27, 36, 58, 83, 97, 88, 67, 44]
]
def cycle (i : Fin 1164) := cycles[i.val - 864]!
theorem checked : ∀ i : Fin 1164,
    864 ≤ i.val → i.val < 896 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 864 ≤ i.val) (hhi : i.val < 896) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00864
end OmissionResidual
