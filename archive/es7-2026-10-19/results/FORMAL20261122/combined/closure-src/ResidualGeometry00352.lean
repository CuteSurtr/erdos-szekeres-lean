import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00352
def cycles : Array (List (Fin 154)) := #[
  [44, 53, 74, 95, 105, 115, 100, 79],
  [45, 65, 75, 86, 97, 108, 100, 68],
  [45, 65, 75, 86, 106, 116, 109, 68],
  [48, 58, 69, 80, 102, 113, 88, 76],
  [48, 58, 69, 80, 112, 121, 88, 76],
  [48, 58, 69, 80, 120, 128, 88, 76],
  [48, 58, 69, 80, 112, 121, 98, 76],
  [48, 58, 69, 80, 120, 128, 98, 76],
  [48, 58, 69, 80, 112, 121, 98, 88],
  [48, 58, 69, 80, 120, 128, 98, 88],
  [51, 60, 70, 92, 102, 113, 78, 66],
  [51, 60, 70, 81, 93, 105, 88, 66],
  [51, 60, 70, 92, 102, 113, 88, 66],
  [51, 60, 70, 81, 93, 115, 90, 66],
  [51, 60, 70, 92, 102, 122, 90, 66],
  [51, 60, 70, 81, 103, 123, 90, 66],
  [51, 60, 70, 92, 112, 129, 90, 66],
  [51, 60, 70, 81, 103, 114, 98, 66],
  [51, 60, 70, 92, 112, 121, 98, 66],
  [51, 60, 70, 81, 93, 115, 100, 66],
  [51, 60, 70, 92, 102, 122, 100, 66],
  [51, 60, 70, 81, 103, 123, 109, 66],
  [51, 60, 70, 92, 112, 129, 109, 66],
  [51, 60, 70, 81, 93, 105, 88, 78],
  [51, 60, 70, 92, 102, 113, 88, 78],
  [51, 60, 70, 81, 103, 114, 98, 78],
  [51, 60, 70, 92, 112, 121, 98, 78],
  [51, 60, 70, 81, 93, 115, 100, 90],
  [51, 60, 70, 92, 102, 122, 100, 90],
  [51, 60, 70, 81, 103, 123, 109, 90],
  [51, 60, 70, 92, 112, 129, 109, 90],
  [52, 62, 72, 83, 94, 116, 79, 67]
]
def cycle (i : Fin 1164) := cycles[i.val - 352]!
theorem checked : ∀ i : Fin 1164,
    352 ≤ i.val → i.val < 384 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 352 ≤ i.val) (hhi : i.val < 384) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00352
end OmissionResidual
