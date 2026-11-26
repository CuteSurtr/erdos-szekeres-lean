import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00704
def cycles : Array (List (Fin 154)) := #[
  [40, 59, 92, 102, 122, 100, 90, 54],
  [41, 50, 60, 72, 87, 78, 67, 55],
  [41, 50, 70, 82, 96, 78, 67, 55],
  [41, 50, 60, 71, 97, 88, 67, 55],
  [41, 50, 71, 94, 106, 98, 67, 55],
  [41, 50, 60, 72, 99, 90, 79, 55],
  [41, 50, 70, 82, 107, 90, 79, 55],
  [41, 50, 60, 83, 108, 100, 79, 55],
  [41, 60, 71, 83, 108, 100, 79, 55],
  [41, 50, 70, 93, 115, 100, 79, 55],
  [41, 70, 81, 93, 115, 100, 79, 55],
  [41, 50, 71, 94, 116, 109, 79, 55],
  [41, 60, 71, 94, 116, 109, 79, 55],
  [42, 62, 72, 83, 108, 100, 68, 56],
  [42, 62, 72, 83, 116, 109, 68, 56],
  [42, 62, 72, 94, 116, 109, 68, 56],
  [42, 62, 83, 94, 116, 109, 68, 56],
  [42, 72, 83, 94, 116, 109, 68, 56],
  [42, 62, 72, 83, 124, 117, 68, 56],
  [42, 62, 72, 94, 124, 117, 68, 56],
  [42, 62, 83, 94, 124, 117, 68, 56],
  [42, 72, 83, 94, 124, 117, 68, 56],
  [47, 57, 69, 93, 105, 97, 87, 75],
  [47, 57, 80, 102, 113, 97, 87, 75],
  [47, 57, 69, 103, 114, 106, 87, 75],
  [47, 57, 80, 112, 121, 106, 87, 75],
  [48, 58, 69, 80, 112, 84, 73, 61],
  [48, 58, 69, 80, 120, 84, 73, 61],
  [48, 58, 69, 103, 114, 98, 88, 76],
  [48, 69, 80, 112, 121, 98, 88, 76],
  [48, 58, 80, 120, 128, 98, 88, 76],
  [48, 69, 80, 120, 128, 98, 88, 76]
]
def cycle (i : Fin 1164) := cycles[i.val - 704]!
theorem checked : ∀ i : Fin 1164,
    704 ≤ i.val → i.val < 736 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 704 ≤ i.val) (hhi : i.val < 736) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00704
end OmissionResidual
