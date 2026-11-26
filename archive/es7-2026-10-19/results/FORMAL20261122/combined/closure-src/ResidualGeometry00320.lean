import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00320
def cycles : Array (List (Fin 154)) := #[
  [41, 50, 60, 71, 83, 108, 79, 55],
  [41, 50, 70, 81, 93, 115, 79, 55],
  [41, 50, 60, 71, 94, 116, 79, 55],
  [41, 50, 70, 81, 103, 123, 79, 55],
  [41, 50, 60, 71, 83, 97, 88, 55],
  [41, 50, 70, 81, 93, 105, 88, 55],
  [41, 50, 60, 71, 94, 106, 98, 55],
  [41, 50, 70, 81, 103, 114, 98, 55],
  [41, 50, 60, 71, 83, 108, 100, 55],
  [41, 50, 70, 81, 93, 115, 100, 55],
  [41, 50, 60, 71, 94, 116, 109, 55],
  [41, 50, 70, 81, 103, 123, 109, 55],
  [41, 50, 60, 71, 83, 97, 88, 67],
  [41, 50, 70, 81, 93, 105, 88, 67],
  [41, 50, 60, 71, 94, 106, 98, 67],
  [41, 50, 70, 81, 103, 114, 98, 67],
  [41, 50, 60, 71, 83, 108, 100, 79],
  [41, 50, 70, 81, 93, 115, 100, 79],
  [41, 50, 60, 71, 94, 116, 109, 79],
  [41, 50, 70, 81, 103, 123, 109, 79],
  [42, 52, 63, 73, 84, 109, 68, 56],
  [42, 62, 72, 83, 94, 116, 68, 56],
  [42, 52, 63, 73, 84, 117, 68, 56],
  [42, 62, 72, 83, 94, 124, 68, 56],
  [42, 62, 72, 83, 94, 106, 98, 56],
  [42, 62, 72, 83, 94, 116, 109, 56],
  [42, 62, 72, 83, 94, 124, 117, 56],
  [42, 62, 72, 83, 94, 116, 109, 68],
  [42, 62, 72, 83, 94, 124, 117, 68],
  [44, 53, 64, 75, 87, 99, 90, 79],
  [44, 53, 74, 85, 96, 107, 90, 79],
  [44, 53, 64, 86, 97, 108, 100, 79]
]
def cycle (i : Fin 1164) := cycles[i.val - 320]!
theorem checked : ∀ i : Fin 1164,
    320 ≤ i.val → i.val < 352 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 320 ≤ i.val) (hhi : i.val < 352) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00320
end OmissionResidual
