import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00768
def cycles : Array (List (Fin 154)) := #[
  [52, 82, 93, 103, 123, 109, 79, 67],
  [52, 62, 72, 83, 124, 117, 79, 67],
  [52, 62, 83, 94, 124, 117, 79, 67],
  [52, 72, 83, 94, 124, 117, 79, 67],
  [52, 62, 82, 93, 130, 117, 79, 67],
  [52, 62, 82, 103, 130, 117, 79, 67],
  [52, 62, 93, 103, 130, 117, 79, 67],
  [52, 82, 93, 103, 130, 117, 79, 67],
  [58, 69, 80, 112, 121, 106, 97, 86],
  [58, 69, 80, 120, 128, 106, 97, 86],
  [60, 70, 81, 93, 105, 97, 87, 75],
  [60, 70, 92, 102, 113, 97, 87, 75],
  [60, 70, 81, 103, 114, 106, 87, 75],
  [60, 70, 92, 112, 121, 106, 87, 75],
  [60, 70, 81, 93, 115, 108, 99, 75],
  [60, 70, 92, 102, 122, 108, 99, 75],
  [60, 70, 81, 103, 123, 116, 99, 75],
  [60, 70, 92, 112, 129, 116, 99, 75],
  [61, 71, 81, 103, 114, 98, 88, 76],
  [61, 71, 81, 112, 121, 98, 88, 76],
  [61, 81, 92, 112, 121, 98, 88, 76],
  [61, 71, 81, 120, 128, 98, 88, 76],
  [61, 81, 92, 120, 128, 98, 88, 76],
  [61, 71, 81, 103, 123, 109, 100, 76],
  [61, 71, 92, 112, 129, 109, 100, 76],
  [61, 81, 92, 112, 129, 109, 100, 76],
  [61, 71, 81, 120, 134, 109, 100, 76],
  [61, 71, 92, 120, 134, 109, 100, 76],
  [61, 81, 92, 120, 134, 109, 100, 76],
  [62, 82, 93, 103, 123, 116, 89, 77],
  [62, 82, 93, 103, 130, 124, 89, 77],
  [63, 72, 82, 93, 115, 100, 90, 78]
]
def cycle (i : Fin 1164) := cycles[i.val - 768]!
theorem checked : ∀ i : Fin 1164,
    768 ≤ i.val → i.val < 800 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 768 ≤ i.val) (hhi : i.val < 800) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00768
end OmissionResidual
