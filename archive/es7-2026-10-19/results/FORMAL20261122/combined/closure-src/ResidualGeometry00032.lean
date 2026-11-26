import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00032
def cycles : Array (List (Fin 154)) := #[
  [5, 8, 19, 28, 40, 54, 34, 25],
  [5, 12, 26, 36, 49, 64, 34, 25],
  [5, 12, 18, 27, 39, 53, 44, 25],
  [5, 8, 13, 29, 41, 55, 45, 25],
  [5, 12, 18, 37, 50, 65, 45, 25],
  [5, 8, 19, 38, 51, 66, 45, 25],
  [5, 12, 26, 47, 60, 75, 45, 25],
  [5, 12, 26, 36, 49, 64, 54, 25],
  [5, 12, 18, 37, 50, 65, 55, 25],
  [5, 12, 26, 47, 60, 75, 66, 25],
  [5, 12, 26, 36, 49, 64, 54, 34],
  [6, 14, 21, 29, 41, 55, 45, 17],
  [6, 20, 27, 37, 50, 65, 45, 17],
  [6, 20, 27, 37, 50, 65, 55, 17],
  [6, 14, 21, 29, 52, 67, 56, 17],
  [6, 20, 27, 37, 62, 77, 56, 17],
  [6, 20, 27, 37, 62, 77, 67, 17],
  [8, 12, 18, 27, 39, 53, 44, 33],
  [8, 12, 26, 36, 49, 64, 44, 33],
  [8, 12, 35, 46, 59, 74, 44, 33],
  [8, 12, 26, 36, 49, 64, 54, 33],
  [8, 12, 35, 46, 59, 74, 54, 33],
  [8, 12, 18, 37, 50, 65, 55, 33],
  [8, 12, 26, 47, 60, 75, 55, 33],
  [8, 12, 35, 57, 70, 85, 55, 33],
  [8, 12, 26, 47, 60, 75, 66, 33],
  [8, 12, 35, 57, 70, 85, 66, 33],
  [8, 12, 26, 36, 49, 64, 54, 44],
  [8, 12, 35, 46, 59, 74, 54, 44],
  [8, 12, 35, 57, 70, 85, 66, 55],
  [9, 13, 19, 38, 51, 66, 45, 34],
  [9, 18, 26, 47, 60, 75, 45, 34]
]
def cycle (i : Fin 1164) := cycles[i.val - 32]!
theorem checked : ∀ i : Fin 1164,
    32 ≤ i.val → i.val < 64 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 32 ≤ i.val) (hhi : i.val < 64) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00032
end OmissionResidual
