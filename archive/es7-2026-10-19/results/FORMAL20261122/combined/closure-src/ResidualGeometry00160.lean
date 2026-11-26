import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00160
def cycles : Array (List (Fin 154)) := #[
  [21, 27, 46, 57, 82, 96, 67, 44],
  [21, 27, 36, 58, 83, 97, 67, 44],
  [21, 27, 46, 69, 93, 105, 67, 44],
  [21, 27, 36, 58, 71, 86, 76, 44],
  [21, 27, 46, 69, 81, 95, 76, 44],
  [21, 27, 36, 47, 72, 87, 78, 44],
  [21, 27, 46, 57, 82, 96, 78, 44],
  [21, 27, 36, 58, 83, 97, 88, 44],
  [21, 27, 46, 69, 93, 105, 88, 44],
  [21, 27, 36, 47, 60, 75, 66, 55],
  [21, 27, 46, 57, 70, 85, 66, 55],
  [21, 27, 36, 58, 71, 86, 76, 55],
  [21, 27, 46, 69, 81, 95, 76, 55],
  [21, 27, 36, 47, 72, 87, 78, 67],
  [21, 27, 46, 57, 82, 96, 78, 67],
  [21, 27, 36, 58, 83, 97, 88, 67],
  [21, 27, 46, 69, 93, 105, 88, 67],
  [22, 29, 38, 48, 73, 88, 56, 45],
  [22, 37, 47, 58, 83, 97, 56, 45],
  [22, 29, 38, 48, 84, 98, 56, 45],
  [22, 37, 47, 58, 94, 106, 56, 45],
  [22, 37, 47, 58, 71, 86, 76, 45],
  [22, 37, 47, 58, 83, 97, 88, 45],
  [22, 37, 47, 58, 94, 106, 98, 45],
  [22, 37, 47, 58, 94, 106, 98, 56],
  [23, 30, 39, 50, 62, 77, 67, 33],
  [23, 30, 49, 60, 72, 87, 67, 33],
  [23, 30, 59, 70, 82, 96, 67, 33],
  [23, 30, 49, 60, 72, 87, 78, 33],
  [23, 30, 59, 70, 82, 96, 78, 33],
  [23, 30, 39, 50, 62, 89, 79, 33],
  [23, 30, 49, 60, 72, 99, 79, 33]
]
def cycle (i : Fin 1164) := cycles[i.val - 160]!
theorem checked : ∀ i : Fin 1164,
    160 ≤ i.val → i.val < 192 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 160 ≤ i.val) (hhi : i.val < 192) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00160
end OmissionResidual
