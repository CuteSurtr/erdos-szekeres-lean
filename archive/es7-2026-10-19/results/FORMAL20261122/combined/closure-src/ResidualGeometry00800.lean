import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00800
def cycles : Array (List (Fin 154)) := #[
  [63, 72, 82, 102, 122, 100, 90, 78],
  [63, 72, 83, 94, 116, 109, 90, 78],
  [63, 72, 93, 103, 123, 109, 90, 78],
  [63, 82, 93, 103, 123, 109, 90, 78],
  [63, 72, 102, 112, 129, 109, 90, 78],
  [63, 82, 102, 112, 129, 109, 90, 78],
  [63, 72, 83, 94, 124, 117, 90, 78],
  [63, 72, 82, 103, 130, 117, 90, 78],
  [63, 72, 93, 103, 130, 117, 90, 78],
  [63, 82, 93, 103, 130, 117, 90, 78],
  [63, 72, 102, 112, 135, 117, 90, 78],
  [63, 82, 102, 112, 135, 117, 90, 78],
  [71, 81, 92, 112, 121, 106, 97, 86],
  [71, 81, 92, 120, 128, 106, 97, 86],
  [71, 81, 92, 112, 129, 116, 108, 86],
  [71, 81, 92, 120, 134, 116, 108, 86],
  [72, 82, 93, 103, 123, 116, 99, 87],
  [72, 82, 102, 112, 129, 116, 99, 87],
  [72, 82, 93, 103, 130, 124, 99, 87],
  [72, 82, 102, 112, 135, 124, 99, 87],
  [73, 83, 93, 103, 123, 109, 100, 88],
  [73, 83, 93, 112, 129, 109, 100, 88],
  [73, 83, 93, 120, 134, 109, 100, 88],
  [73, 83, 102, 120, 134, 109, 100, 88],
  [73, 93, 102, 120, 134, 109, 100, 88],
  [73, 83, 93, 103, 130, 117, 100, 88],
  [73, 83, 93, 112, 135, 117, 100, 88],
  [73, 83, 102, 112, 135, 117, 100, 88],
  [73, 93, 102, 112, 135, 117, 100, 88],
  [73, 83, 93, 120, 140, 117, 100, 88],
  [73, 83, 102, 120, 140, 117, 100, 88],
  [73, 93, 102, 120, 140, 117, 100, 88]
]
def cycle (i : Fin 1164) := cycles[i.val - 800]!
theorem checked : ∀ i : Fin 1164,
    800 ≤ i.val → i.val < 832 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 800 ≤ i.val) (hhi : i.val < 832) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00800
end OmissionResidual
