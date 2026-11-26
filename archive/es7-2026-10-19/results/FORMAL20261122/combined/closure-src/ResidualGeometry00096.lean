import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00096
def cycles : Array (List (Fin 154)) := #[
  [13, 18, 35, 69, 81, 95, 55, 44],
  [13, 18, 26, 47, 60, 75, 66, 44],
  [13, 18, 35, 57, 70, 85, 66, 44],
  [13, 18, 26, 58, 71, 86, 76, 44],
  [13, 18, 35, 69, 81, 95, 76, 44],
  [13, 18, 26, 47, 60, 75, 66, 55],
  [13, 18, 35, 57, 70, 85, 66, 55],
  [13, 18, 26, 58, 71, 86, 76, 55],
  [13, 18, 35, 69, 81, 95, 76, 55],
  [14, 20, 27, 37, 50, 65, 55, 33],
  [14, 20, 36, 47, 60, 75, 55, 33],
  [14, 20, 46, 57, 70, 85, 55, 33],
  [14, 20, 36, 47, 60, 75, 66, 33],
  [14, 20, 46, 57, 70, 85, 66, 33],
  [14, 20, 27, 37, 62, 77, 67, 33],
  [14, 20, 36, 47, 72, 87, 67, 33],
  [14, 20, 46, 57, 82, 96, 67, 33],
  [14, 20, 36, 47, 72, 87, 78, 33],
  [14, 20, 46, 57, 82, 96, 78, 33],
  [14, 20, 46, 57, 82, 96, 78, 67],
  [15, 21, 28, 38, 51, 66, 45, 34],
  [15, 27, 36, 47, 60, 75, 45, 34],
  [15, 21, 28, 48, 61, 76, 45, 34],
  [15, 27, 36, 58, 71, 86, 45, 34],
  [15, 21, 28, 38, 63, 78, 56, 34],
  [15, 27, 36, 47, 72, 87, 56, 34],
  [15, 21, 28, 48, 73, 88, 56, 34],
  [15, 27, 36, 58, 83, 97, 56, 34],
  [15, 27, 36, 47, 60, 75, 66, 34],
  [15, 27, 36, 58, 71, 86, 76, 34],
  [15, 27, 36, 47, 72, 87, 78, 34],
  [15, 27, 36, 58, 83, 97, 88, 34]
]
def cycle (i : Fin 1164) := cycles[i.val - 96]!
theorem checked : ∀ i : Fin 1164,
    96 ≤ i.val → i.val < 128 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 96 ≤ i.val) (hhi : i.val < 128) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00096
end OmissionResidual
