import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00384
def cycles : Array (List (Fin 154)) := #[
  [52, 62, 82, 93, 103, 123, 79, 67],
  [52, 62, 72, 83, 94, 124, 79, 67],
  [52, 62, 72, 83, 94, 106, 98, 67],
  [52, 62, 82, 93, 103, 114, 98, 67],
  [52, 62, 72, 83, 94, 116, 109, 67],
  [52, 62, 82, 93, 103, 123, 109, 67],
  [52, 62, 72, 83, 94, 124, 117, 67],
  [52, 62, 82, 93, 103, 130, 117, 67],
  [52, 62, 72, 83, 94, 116, 109, 79],
  [52, 62, 82, 93, 103, 123, 109, 79],
  [52, 62, 72, 83, 94, 124, 117, 79],
  [52, 62, 82, 93, 103, 130, 117, 79],
  [54, 64, 74, 95, 105, 115, 100, 90],
  [54, 64, 74, 104, 113, 122, 100, 90],
  [55, 65, 75, 86, 97, 108, 100, 79],
  [55, 65, 85, 95, 105, 115, 100, 79],
  [55, 65, 75, 86, 106, 116, 109, 79],
  [55, 65, 85, 95, 114, 123, 109, 79],
  [56, 77, 87, 97, 106, 116, 109, 68],
  [56, 77, 87, 97, 106, 124, 117, 68],
  [61, 71, 81, 92, 102, 113, 88, 76],
  [61, 71, 81, 92, 112, 121, 88, 76],
  [61, 71, 81, 92, 120, 128, 88, 76],
  [61, 71, 81, 92, 112, 121, 98, 76],
  [61, 71, 81, 92, 120, 128, 98, 76],
  [61, 71, 81, 92, 102, 122, 100, 76],
  [61, 71, 81, 92, 112, 129, 100, 76],
  [61, 71, 81, 92, 120, 134, 100, 76],
  [61, 71, 81, 92, 112, 129, 109, 76],
  [61, 71, 81, 92, 120, 134, 109, 76],
  [61, 71, 81, 92, 112, 121, 98, 88],
  [61, 71, 81, 92, 120, 128, 98, 88]
]
def cycle (i : Fin 1164) := cycles[i.val - 384]!
theorem checked : ∀ i : Fin 1164,
    384 ≤ i.val → i.val < 416 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 384 ≤ i.val) (hhi : i.val < 416) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00384
end OmissionResidual
