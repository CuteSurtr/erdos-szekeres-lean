import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00896
def cycles : Array (List (Fin 154)) := #[
  [21, 27, 46, 69, 93, 105, 88, 67, 44],
  [22, 37, 47, 58, 83, 97, 88, 56, 45],
  [22, 37, 47, 58, 94, 106, 98, 56, 45],
  [23, 30, 49, 60, 72, 87, 78, 67, 33],
  [23, 30, 59, 70, 82, 96, 78, 67, 33],
  [23, 30, 49, 60, 72, 99, 90, 79, 33],
  [23, 30, 59, 70, 82, 107, 90, 79, 33],
  [24, 39, 49, 60, 72, 87, 78, 56, 34],
  [24, 39, 49, 71, 83, 97, 88, 56, 34],
  [24, 39, 49, 60, 72, 99, 90, 68, 34],
  [24, 39, 49, 71, 83, 108, 100, 68, 34],
  [28, 36, 46, 69, 81, 95, 76, 66, 54],
  [28, 36, 46, 80, 92, 104, 76, 66, 54],
  [28, 36, 46, 69, 93, 105, 88, 78, 54],
  [28, 36, 46, 80, 102, 113, 88, 78, 54],
  [29, 37, 47, 58, 83, 97, 88, 67, 55],
  [29, 37, 57, 69, 93, 105, 88, 67, 55],
  [29, 37, 47, 58, 94, 106, 98, 67, 55],
  [29, 37, 57, 69, 103, 114, 98, 67, 55],
  [31, 39, 49, 60, 72, 87, 78, 67, 44],
  [31, 39, 59, 70, 82, 96, 78, 67, 44],
  [31, 39, 49, 71, 83, 97, 88, 67, 44],
  [31, 39, 59, 81, 93, 105, 88, 67, 44],
  [31, 39, 49, 60, 72, 99, 90, 79, 44],
  [31, 39, 59, 70, 82, 107, 90, 79, 44],
  [31, 39, 49, 71, 83, 108, 100, 79, 44],
  [31, 39, 59, 81, 93, 115, 100, 79, 44],
  [32, 50, 60, 71, 83, 97, 88, 56, 45],
  [32, 50, 60, 71, 94, 106, 98, 56, 45],
  [32, 50, 60, 71, 83, 108, 100, 68, 45],
  [32, 50, 60, 71, 94, 116, 109, 68, 45],
  [38, 47, 57, 69, 93, 105, 88, 78, 66]
]
def cycle (i : Fin 1164) := cycles[i.val - 896]!
theorem checked : ∀ i : Fin 1164,
    896 ≤ i.val → i.val < 928 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 896 ≤ i.val) (hhi : i.val < 928) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00896
end OmissionResidual
