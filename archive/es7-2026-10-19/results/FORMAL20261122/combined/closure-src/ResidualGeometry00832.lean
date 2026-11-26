import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00832
def cycles : Array (List (Fin 154)) := #[
  [83, 93, 102, 112, 129, 116, 108, 97],
  [83, 93, 102, 120, 134, 116, 108, 97],
  [83, 93, 102, 112, 135, 124, 108, 97],
  [83, 93, 102, 120, 140, 124, 108, 97],
  [84, 94, 103, 120, 140, 117, 109, 98],
  [84, 94, 112, 120, 140, 117, 109, 98],
  [84, 103, 112, 120, 140, 117, 109, 98],
  [84, 94, 103, 120, 144, 117, 109, 98],
  [84, 94, 112, 120, 144, 117, 109, 98],
  [84, 103, 112, 120, 144, 117, 109, 98],
  [94, 103, 112, 120, 140, 124, 116, 106],
  [94, 103, 112, 120, 144, 124, 116, 106],
  [0, 7, 12, 20, 30, 43, 33, 25, 17],
  [1, 7, 12, 20, 30, 43, 33, 25, 17],
  [1, 7, 18, 27, 39, 53, 44, 34, 17],
  [2, 7, 18, 27, 39, 53, 44, 34, 25],
  [2, 7, 26, 36, 49, 64, 54, 34, 25],
  [3, 12, 18, 27, 39, 53, 44, 34, 17],
  [3, 12, 18, 37, 50, 65, 55, 45, 17],
  [4, 7, 26, 36, 49, 64, 54, 44, 33],
  [4, 7, 35, 46, 59, 74, 54, 44, 33],
  [5, 12, 18, 27, 39, 53, 44, 34, 25],
  [5, 12, 26, 36, 49, 64, 54, 34, 25],
  [5, 12, 18, 37, 50, 65, 55, 45, 25],
  [5, 12, 26, 47, 60, 75, 66, 45, 25],
  [6, 20, 27, 37, 50, 65, 55, 45, 17],
  [6, 20, 27, 37, 62, 77, 67, 56, 17],
  [8, 12, 26, 36, 49, 64, 54, 44, 33],
  [8, 12, 35, 46, 59, 74, 54, 44, 33],
  [8, 12, 26, 47, 60, 75, 66, 55, 33],
  [8, 12, 35, 57, 70, 85, 66, 55, 33],
  [9, 18, 26, 47, 60, 75, 66, 45, 34]
]
def cycle (i : Fin 1164) := cycles[i.val - 832]!
theorem checked : ∀ i : Fin 1164,
    832 ≤ i.val → i.val < 864 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 832 ≤ i.val) (hhi : i.val < 864) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00832
end OmissionResidual
