import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00480
def cycles : Array (List (Fin 154)) := #[
  [4, 7, 26, 36, 64, 54, 44, 33],
  [4, 7, 36, 49, 64, 54, 44, 33],
  [5, 12, 18, 27, 39, 31, 24, 16],
  [5, 12, 26, 36, 49, 40, 24, 16],
  [5, 12, 18, 37, 50, 41, 32, 16],
  [5, 12, 26, 47, 60, 51, 32, 16],
  [5, 12, 26, 36, 64, 54, 34, 25],
  [5, 12, 18, 37, 65, 55, 45, 25],
  [5, 12, 26, 47, 75, 66, 45, 25],
  [5, 12, 26, 60, 75, 66, 45, 25],
  [6, 20, 27, 37, 50, 41, 32, 11],
  [6, 20, 27, 37, 62, 52, 42, 11],
  [6, 20, 27, 50, 65, 55, 45, 17],
  [6, 20, 27, 37, 77, 67, 56, 17],
  [7, 35, 46, 59, 74, 64, 53, 43],
  [8, 12, 26, 36, 49, 40, 31, 23],
  [8, 12, 35, 46, 59, 40, 31, 23],
  [8, 12, 26, 47, 60, 51, 41, 23],
  [8, 12, 35, 57, 70, 51, 41, 23],
  [8, 12, 26, 36, 64, 54, 44, 33],
  [8, 12, 36, 49, 64, 54, 44, 33],
  [8, 12, 35, 46, 74, 54, 44, 33],
  [8, 12, 26, 47, 75, 66, 55, 33],
  [8, 12, 26, 60, 75, 66, 55, 33],
  [8, 12, 35, 57, 85, 66, 55, 33],
  [8, 12, 35, 70, 85, 66, 55, 33],
  [9, 18, 26, 47, 60, 51, 32, 24],
  [9, 18, 26, 58, 71, 61, 32, 24],
  [9, 18, 37, 50, 65, 55, 45, 34],
  [9, 18, 26, 47, 75, 66, 45, 34],
  [9, 18, 26, 58, 86, 76, 45, 34],
  [9, 18, 26, 71, 86, 76, 45, 34]
]
def cycle (i : Fin 1164) := cycles[i.val - 480]!
theorem checked : ∀ i : Fin 1164,
    480 ≤ i.val → i.val < 512 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 480 ≤ i.val) (hhi : i.val < 512) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00480
end OmissionResidual
