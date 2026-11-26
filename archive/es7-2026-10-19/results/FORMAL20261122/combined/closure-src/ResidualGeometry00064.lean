import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00064
def cycles : Array (List (Fin 154)) := #[
  [9, 13, 19, 48, 61, 76, 45, 34],
  [9, 18, 26, 58, 71, 86, 45, 34],
  [9, 18, 26, 36, 49, 64, 54, 34],
  [9, 18, 26, 47, 60, 75, 66, 34],
  [9, 18, 26, 58, 71, 86, 76, 34],
  [9, 18, 26, 58, 71, 86, 76, 45],
  [10, 14, 21, 29, 41, 55, 45, 25],
  [10, 20, 27, 37, 50, 65, 45, 25],
  [10, 14, 28, 38, 51, 66, 45, 25],
  [10, 20, 36, 47, 60, 75, 45, 25],
  [10, 20, 27, 37, 50, 65, 55, 25],
  [10, 14, 21, 29, 52, 67, 56, 25],
  [10, 20, 27, 37, 62, 77, 56, 25],
  [10, 14, 28, 38, 63, 78, 56, 25],
  [10, 20, 36, 47, 72, 87, 56, 25],
  [10, 20, 36, 47, 60, 75, 66, 25],
  [10, 20, 27, 37, 62, 77, 67, 25],
  [10, 20, 36, 47, 72, 87, 78, 25],
  [10, 20, 36, 47, 72, 87, 78, 56],
  [11, 23, 31, 41, 52, 67, 56, 17],
  [11, 30, 39, 50, 62, 77, 56, 17],
  [11, 30, 39, 50, 62, 77, 67, 17],
  [11, 23, 31, 41, 52, 79, 68, 17],
  [11, 30, 39, 50, 62, 89, 68, 17],
  [11, 30, 39, 50, 62, 89, 79, 17],
  [11, 30, 39, 50, 62, 77, 67, 56],
  [11, 30, 39, 50, 62, 89, 79, 68],
  [13, 18, 26, 36, 49, 64, 54, 44],
  [13, 18, 35, 46, 59, 74, 54, 44],
  [13, 18, 26, 47, 60, 75, 55, 44],
  [13, 18, 35, 57, 70, 85, 55, 44],
  [13, 18, 26, 58, 71, 86, 55, 44]
]
def cycle (i : Fin 1164) := cycles[i.val - 64]!
theorem checked : ∀ i : Fin 1164,
    64 ≤ i.val → i.val < 96 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 64 ≤ i.val) (hhi : i.val < 96) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00064
end OmissionResidual
