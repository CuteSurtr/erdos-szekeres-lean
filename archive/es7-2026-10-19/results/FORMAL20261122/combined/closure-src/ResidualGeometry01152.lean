import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry01152
def cycles : Array (List (Fin 154)) := #[
  [116, 123, 129, 134, 144, 152, 143, 132],
  [117, 124, 130, 135, 140, 144, 152, 139, 133],
  [117, 124, 130, 135, 140, 144, 153, 139, 133],
  [117, 124, 130, 135, 140, 144, 150, 133],
  [119, 126, 131, 136, 141, 146, 149, 139],
  [119, 126, 131, 136, 145, 148, 151, 139],
  [124, 130, 135, 140, 144, 152, 143, 138],
  [124, 130, 135, 140, 144, 153, 143, 138],
  [127, 132, 137, 141, 145, 148, 151, 139],
  [127, 132, 137, 141, 145, 150, 152, 139],
  [133, 138, 142, 146, 148, 150, 152, 139],
  [133, 138, 142, 146, 148, 150, 153, 139]
]
def cycle (i : Fin 1164) := cycles[i.val - 1152]!
theorem checked : ∀ i : Fin 1164,
    1152 ≤ i.val → i.val < 1164 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 1152 ≤ i.val) (hhi : i.val < 1164) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry01152
end OmissionResidual
