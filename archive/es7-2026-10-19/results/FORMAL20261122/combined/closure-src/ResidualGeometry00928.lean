import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00928
def cycles : Array (List (Fin 154)) := #[
  [38, 47, 57, 80, 102, 113, 88, 78, 66],
  [38, 47, 57, 69, 103, 114, 98, 78, 66],
  [38, 47, 57, 80, 112, 121, 98, 78, 66],
  [40, 49, 59, 81, 93, 105, 88, 78, 54],
  [40, 49, 59, 92, 102, 113, 88, 78, 54],
  [40, 49, 59, 81, 93, 115, 100, 90, 54],
  [40, 49, 59, 92, 102, 122, 100, 90, 54],
  [41, 50, 60, 71, 83, 97, 88, 67, 55],
  [41, 50, 70, 81, 93, 105, 88, 67, 55],
  [41, 50, 60, 71, 94, 106, 98, 67, 55],
  [41, 50, 70, 81, 103, 114, 98, 67, 55],
  [41, 50, 60, 71, 83, 108, 100, 79, 55],
  [41, 50, 70, 81, 93, 115, 100, 79, 55],
  [41, 50, 60, 71, 94, 116, 109, 79, 55],
  [41, 50, 70, 81, 103, 123, 109, 79, 55],
  [42, 62, 72, 83, 94, 116, 109, 68, 56],
  [42, 62, 72, 83, 94, 124, 117, 68, 56],
  [48, 58, 69, 80, 112, 121, 98, 88, 76],
  [48, 58, 69, 80, 120, 128, 98, 88, 76],
  [51, 60, 70, 81, 93, 105, 88, 78, 66],
  [51, 60, 70, 92, 102, 113, 88, 78, 66],
  [51, 60, 70, 81, 103, 114, 98, 78, 66],
  [51, 60, 70, 92, 112, 121, 98, 78, 66],
  [51, 60, 70, 81, 93, 115, 100, 90, 66],
  [51, 60, 70, 92, 102, 122, 100, 90, 66],
  [51, 60, 70, 81, 103, 123, 109, 90, 66],
  [51, 60, 70, 92, 112, 129, 109, 90, 66],
  [52, 62, 72, 83, 94, 116, 109, 79, 67],
  [52, 62, 82, 93, 103, 123, 109, 79, 67],
  [52, 62, 72, 83, 94, 124, 117, 79, 67],
  [52, 62, 82, 93, 103, 130, 117, 79, 67],
  [61, 71, 81, 92, 112, 121, 98, 88, 76]
]
def cycle (i : Fin 1164) := cycles[i.val - 928]!
theorem checked : ∀ i : Fin 1164,
    928 ≤ i.val → i.val < 960 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 928 ≤ i.val) (hhi : i.val < 960) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00928
end OmissionResidual
