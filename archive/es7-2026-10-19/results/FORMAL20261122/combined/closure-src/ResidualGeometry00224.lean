import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00224
def cycles : Array (List (Fin 154)) := #[
  [28, 36, 46, 80, 102, 113, 78, 54],
  [28, 36, 46, 69, 93, 105, 88, 54],
  [28, 36, 46, 80, 102, 113, 88, 54],
  [28, 36, 46, 69, 81, 95, 76, 66],
  [28, 36, 46, 80, 92, 104, 76, 66],
  [28, 36, 46, 69, 93, 105, 88, 78],
  [28, 36, 46, 80, 102, 113, 88, 78],
  [29, 37, 47, 58, 83, 97, 67, 55],
  [29, 37, 57, 69, 93, 105, 67, 55],
  [29, 37, 47, 58, 94, 106, 67, 55],
  [29, 37, 57, 69, 103, 114, 67, 55],
  [29, 37, 47, 58, 71, 86, 76, 55],
  [29, 37, 57, 69, 81, 95, 76, 55],
  [29, 37, 47, 58, 83, 97, 88, 55],
  [29, 37, 57, 69, 93, 105, 88, 55],
  [29, 37, 47, 58, 94, 106, 98, 55],
  [29, 37, 57, 69, 103, 114, 98, 55],
  [29, 37, 47, 58, 83, 97, 88, 67],
  [29, 37, 57, 69, 93, 105, 88, 67],
  [29, 37, 47, 58, 94, 106, 98, 67],
  [29, 37, 57, 69, 103, 114, 98, 67],
  [31, 39, 49, 60, 72, 87, 67, 44],
  [31, 39, 59, 70, 82, 96, 67, 44],
  [31, 39, 49, 71, 83, 97, 67, 44],
  [31, 39, 59, 81, 93, 105, 67, 44],
  [31, 39, 49, 60, 72, 87, 78, 44],
  [31, 39, 59, 70, 82, 96, 78, 44],
  [31, 39, 49, 60, 72, 99, 79, 44],
  [31, 39, 59, 70, 82, 107, 79, 44],
  [31, 39, 49, 71, 83, 108, 79, 44],
  [31, 39, 59, 81, 93, 115, 79, 44],
  [31, 39, 49, 71, 83, 97, 88, 44]
]
def cycle (i : Fin 1164) := cycles[i.val - 224]!
theorem checked : ∀ i : Fin 1164,
    224 ≤ i.val → i.val < 256 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 224 ≤ i.val) (hhi : i.val < 256) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00224
end OmissionResidual
