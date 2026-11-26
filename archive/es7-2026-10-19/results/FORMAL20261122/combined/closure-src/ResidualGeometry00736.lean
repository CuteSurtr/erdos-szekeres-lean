import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00736
def cycles : Array (List (Fin 154)) := #[
  [49, 59, 81, 93, 105, 97, 87, 64],
  [49, 59, 92, 102, 113, 97, 87, 64],
  [49, 59, 81, 93, 115, 108, 99, 64],
  [49, 59, 92, 102, 122, 108, 99, 64],
  [50, 70, 81, 93, 105, 97, 77, 65],
  [50, 70, 81, 103, 114, 106, 77, 65],
  [50, 70, 81, 93, 115, 108, 89, 65],
  [50, 70, 81, 103, 123, 116, 89, 65],
  [51, 60, 71, 83, 97, 88, 78, 66],
  [51, 60, 81, 93, 105, 88, 78, 66],
  [51, 70, 81, 93, 105, 88, 78, 66],
  [51, 60, 92, 102, 113, 88, 78, 66],
  [51, 70, 92, 102, 113, 88, 78, 66],
  [51, 60, 71, 94, 106, 98, 78, 66],
  [51, 60, 81, 103, 114, 98, 78, 66],
  [51, 70, 92, 112, 121, 98, 78, 66],
  [51, 60, 71, 83, 108, 100, 90, 66],
  [51, 70, 81, 93, 115, 100, 90, 66],
  [51, 60, 70, 102, 122, 100, 90, 66],
  [51, 60, 92, 102, 122, 100, 90, 66],
  [51, 70, 92, 102, 122, 100, 90, 66],
  [51, 60, 71, 94, 116, 109, 90, 66],
  [51, 60, 81, 103, 123, 109, 90, 66],
  [51, 70, 81, 103, 123, 109, 90, 66],
  [51, 60, 92, 112, 129, 109, 90, 66],
  [51, 70, 92, 112, 129, 109, 90, 66],
  [52, 62, 72, 83, 108, 100, 79, 67],
  [52, 62, 82, 93, 115, 100, 79, 67],
  [52, 62, 72, 83, 116, 109, 79, 67],
  [52, 62, 83, 94, 116, 109, 79, 67],
  [52, 72, 83, 94, 116, 109, 79, 67],
  [52, 62, 82, 93, 123, 109, 79, 67]
]
def cycle (i : Fin 1164) := cycles[i.val - 736]!
theorem checked : ∀ i : Fin 1164,
    736 ≤ i.val → i.val < 768 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 736 ≤ i.val) (hhi : i.val < 768) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00736
end OmissionResidual
