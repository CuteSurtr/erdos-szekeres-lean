import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00000
def cycles : Array (List (Fin 154)) := #[
  [0, 4, 8, 14, 23, 33, 25, 17],
  [0, 7, 12, 20, 30, 43, 25, 17],
  [0, 7, 12, 20, 30, 43, 33, 17],
  [0, 7, 12, 20, 30, 43, 33, 25],
  [1, 4, 8, 14, 23, 33, 25, 17],
  [1, 7, 12, 20, 30, 43, 25, 17],
  [1, 7, 12, 20, 30, 43, 33, 17],
  [1, 4, 13, 21, 31, 44, 34, 17],
  [1, 7, 18, 27, 39, 53, 34, 17],
  [1, 7, 18, 27, 39, 53, 44, 17],
  [2, 4, 13, 21, 31, 44, 34, 25],
  [2, 7, 18, 27, 39, 53, 34, 25],
  [2, 4, 19, 28, 40, 54, 34, 25],
  [2, 7, 26, 36, 49, 64, 34, 25],
  [2, 7, 18, 27, 39, 53, 44, 25],
  [2, 7, 26, 36, 49, 64, 54, 25],
  [2, 7, 26, 36, 49, 64, 54, 34],
  [3, 8, 13, 21, 31, 44, 34, 17],
  [3, 12, 18, 27, 39, 53, 34, 17],
  [3, 12, 18, 27, 39, 53, 44, 17],
  [3, 8, 13, 29, 41, 55, 45, 17],
  [3, 12, 18, 37, 50, 65, 45, 17],
  [3, 12, 18, 37, 50, 65, 55, 17],
  [4, 7, 18, 27, 39, 53, 44, 33],
  [4, 7, 26, 36, 49, 64, 44, 33],
  [4, 7, 35, 46, 59, 74, 44, 33],
  [4, 7, 26, 36, 49, 64, 54, 33],
  [4, 7, 35, 46, 59, 74, 54, 33],
  [4, 7, 26, 36, 49, 64, 54, 44],
  [4, 7, 35, 46, 59, 74, 54, 44],
  [5, 8, 13, 21, 31, 44, 34, 25],
  [5, 12, 18, 27, 39, 53, 34, 25]
]
def cycle (i : Fin 1164) := cycles[i.val - 0]!
theorem checked : ∀ i : Fin 1164,
    0 ≤ i.val → i.val < 32 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 0 ≤ i.val) (hhi : i.val < 32) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00000
end OmissionResidual
