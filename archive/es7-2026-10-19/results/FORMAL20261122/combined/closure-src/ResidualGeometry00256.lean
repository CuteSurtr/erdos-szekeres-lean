import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00256
def cycles : Array (List (Fin 154)) := #[
  [31, 39, 59, 81, 93, 105, 88, 44],
  [31, 39, 49, 60, 72, 99, 90, 44],
  [31, 39, 59, 70, 82, 107, 90, 44],
  [31, 39, 49, 71, 83, 108, 100, 44],
  [31, 39, 59, 81, 93, 115, 100, 44],
  [31, 39, 49, 60, 72, 87, 78, 67],
  [31, 39, 59, 70, 82, 96, 78, 67],
  [31, 39, 49, 71, 83, 97, 88, 67],
  [31, 39, 59, 81, 93, 105, 88, 67],
  [31, 39, 49, 60, 72, 99, 90, 79],
  [31, 39, 59, 70, 82, 107, 90, 79],
  [31, 39, 49, 71, 83, 108, 100, 79],
  [31, 39, 59, 81, 93, 115, 100, 79],
  [32, 41, 51, 61, 73, 88, 56, 45],
  [32, 50, 60, 71, 83, 97, 56, 45],
  [32, 41, 51, 61, 84, 98, 56, 45],
  [32, 50, 60, 71, 94, 106, 56, 45],
  [32, 41, 51, 61, 73, 100, 68, 45],
  [32, 50, 60, 71, 83, 108, 68, 45],
  [32, 41, 51, 61, 84, 109, 68, 45],
  [32, 50, 60, 71, 94, 116, 68, 45],
  [32, 50, 60, 71, 83, 97, 88, 45],
  [32, 50, 60, 71, 94, 106, 98, 45],
  [32, 50, 60, 71, 83, 108, 100, 45],
  [32, 50, 60, 71, 94, 116, 109, 45],
  [32, 50, 60, 71, 83, 97, 88, 56],
  [32, 50, 60, 71, 94, 106, 98, 56],
  [32, 50, 60, 71, 94, 116, 109, 68],
  [33, 43, 64, 75, 87, 99, 90, 79],
  [33, 43, 74, 85, 96, 107, 90, 79],
  [34, 53, 64, 75, 87, 99, 90, 68],
  [34, 53, 64, 86, 97, 108, 100, 68]
]
def cycle (i : Fin 1164) := cycles[i.val - 256]!
theorem checked : ∀ i : Fin 1164,
    256 ≤ i.val → i.val < 288 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 256 ≤ i.val) (hhi : i.val < 288) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00256
end OmissionResidual
