import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00288
def cycles : Array (List (Fin 154)) := #[
  [38, 47, 57, 69, 81, 95, 76, 66],
  [38, 47, 57, 80, 92, 104, 76, 66],
  [38, 47, 57, 69, 93, 105, 78, 66],
  [38, 47, 57, 80, 102, 113, 78, 66],
  [38, 47, 57, 69, 103, 114, 78, 66],
  [38, 47, 57, 80, 112, 121, 78, 66],
  [38, 47, 57, 69, 93, 105, 88, 66],
  [38, 47, 57, 80, 102, 113, 88, 66],
  [38, 47, 57, 69, 103, 114, 98, 66],
  [38, 47, 57, 80, 112, 121, 98, 66],
  [38, 47, 57, 69, 93, 105, 88, 78],
  [38, 47, 57, 80, 102, 113, 88, 78],
  [38, 47, 57, 69, 103, 114, 98, 78],
  [38, 47, 57, 80, 112, 121, 98, 78],
  [40, 49, 59, 70, 82, 96, 78, 54],
  [40, 49, 59, 81, 93, 105, 78, 54],
  [40, 49, 59, 92, 102, 113, 78, 54],
  [40, 49, 59, 81, 93, 105, 88, 54],
  [40, 49, 59, 92, 102, 113, 88, 54],
  [40, 49, 59, 70, 82, 107, 90, 54],
  [40, 49, 59, 81, 93, 115, 90, 54],
  [40, 49, 59, 92, 102, 122, 90, 54],
  [40, 49, 59, 81, 93, 115, 100, 54],
  [40, 49, 59, 92, 102, 122, 100, 54],
  [40, 49, 59, 81, 93, 105, 88, 78],
  [40, 49, 59, 92, 102, 113, 88, 78],
  [40, 49, 59, 81, 93, 115, 100, 90],
  [40, 49, 59, 92, 102, 122, 100, 90],
  [41, 50, 60, 71, 83, 97, 67, 55],
  [41, 50, 70, 81, 93, 105, 67, 55],
  [41, 50, 60, 71, 94, 106, 67, 55],
  [41, 50, 70, 81, 103, 114, 67, 55]
]
def cycle (i : Fin 1164) := cycles[i.val - 288]!
theorem checked : ∀ i : Fin 1164,
    288 ≤ i.val → i.val < 320 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 288 ≤ i.val) (hhi : i.val < 320) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00288
end OmissionResidual
