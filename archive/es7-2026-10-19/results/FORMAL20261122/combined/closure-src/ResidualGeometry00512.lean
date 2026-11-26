import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00512
def cycles : Array (List (Fin 154)) := #[
  [10, 20, 27, 37, 50, 41, 32, 16],
  [10, 20, 36, 47, 60, 51, 32, 16],
  [10, 20, 27, 37, 62, 52, 42, 16],
  [10, 20, 36, 47, 72, 63, 42, 16],
  [10, 20, 27, 50, 65, 55, 45, 25],
  [10, 20, 36, 47, 75, 66, 45, 25],
  [10, 20, 36, 60, 75, 66, 45, 25],
  [10, 20, 27, 37, 77, 67, 56, 25],
  [11, 30, 39, 50, 65, 55, 45, 17],
  [11, 30, 39, 50, 77, 67, 56, 17],
  [11, 30, 39, 50, 89, 79, 68, 17],
  [11, 30, 39, 62, 89, 79, 68, 17],
  [11, 30, 50, 62, 89, 79, 68, 17],
  [11, 39, 50, 62, 89, 79, 68, 17],
  [12, 35, 46, 59, 74, 64, 53, 43],
  [12, 35, 57, 70, 85, 75, 65, 43],
  [13, 18, 26, 47, 60, 51, 41, 31],
  [13, 18, 35, 57, 70, 51, 41, 31],
  [13, 18, 26, 58, 71, 61, 41, 31],
  [13, 18, 35, 69, 81, 61, 41, 31],
  [13, 18, 26, 47, 75, 66, 55, 44],
  [13, 18, 26, 60, 75, 66, 55, 44],
  [13, 18, 35, 57, 85, 66, 55, 44],
  [13, 18, 35, 70, 85, 66, 55, 44],
  [13, 18, 26, 58, 86, 76, 55, 44],
  [13, 18, 26, 71, 86, 76, 55, 44],
  [13, 18, 35, 69, 95, 76, 55, 44],
  [14, 20, 36, 47, 60, 51, 41, 23],
  [14, 20, 46, 57, 70, 51, 41, 23],
  [14, 20, 36, 47, 72, 63, 52, 23],
  [14, 20, 46, 57, 82, 63, 52, 23],
  [14, 20, 36, 49, 64, 54, 44, 33]
]
def cycle (i : Fin 1164) := cycles[i.val - 512]!
theorem checked : ∀ i : Fin 1164,
    512 ≤ i.val → i.val < 544 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 512 ≤ i.val) (hhi : i.val < 544) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00512
end OmissionResidual
