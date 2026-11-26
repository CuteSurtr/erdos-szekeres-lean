import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00640
def cycles : Array (List (Fin 154)) := #[
  [30, 59, 70, 82, 107, 99, 89, 43],
  [31, 39, 49, 60, 75, 66, 55, 44],
  [31, 39, 59, 70, 85, 66, 55, 44],
  [31, 39, 49, 71, 86, 76, 55, 44],
  [31, 39, 59, 81, 95, 76, 55, 44],
  [31, 39, 49, 60, 87, 78, 67, 44],
  [31, 39, 59, 70, 96, 78, 67, 44],
  [31, 39, 49, 71, 97, 88, 67, 44],
  [31, 39, 59, 81, 105, 88, 67, 44],
  [31, 39, 49, 60, 99, 90, 79, 44],
  [31, 39, 49, 72, 99, 90, 79, 44],
  [31, 39, 59, 70, 107, 90, 79, 44],
  [31, 39, 59, 82, 107, 90, 79, 44],
  [31, 39, 70, 82, 107, 90, 79, 44],
  [31, 39, 49, 71, 108, 100, 79, 44],
  [31, 39, 49, 83, 108, 100, 79, 44],
  [31, 49, 71, 83, 108, 100, 79, 44],
  [31, 39, 59, 81, 115, 100, 79, 44],
  [31, 39, 59, 93, 115, 100, 79, 44],
  [31, 59, 81, 93, 115, 100, 79, 44],
  [32, 50, 60, 72, 87, 78, 56, 45],
  [32, 50, 60, 71, 97, 88, 56, 45],
  [32, 50, 60, 71, 106, 98, 56, 45],
  [32, 60, 71, 94, 106, 98, 56, 45],
  [32, 50, 60, 72, 99, 90, 68, 45],
  [32, 50, 60, 71, 108, 100, 68, 45],
  [32, 50, 60, 83, 108, 100, 68, 45],
  [32, 50, 71, 83, 108, 100, 68, 45],
  [32, 50, 60, 71, 116, 109, 68, 45],
  [32, 50, 60, 94, 116, 109, 68, 45],
  [32, 50, 71, 94, 116, 109, 68, 45],
  [32, 60, 71, 94, 116, 109, 68, 45]
]
def cycle (i : Fin 1164) := cycles[i.val - 640]!
theorem checked : ∀ i : Fin 1164,
    640 ≤ i.val → i.val < 672 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 640 ≤ i.val) (hhi : i.val < 672) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00640
end OmissionResidual
