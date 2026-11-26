import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry01088
def cycles : Array (List (Fin 154)) := #[
  [79, 89, 107, 115, 123, 130, 142, 133, 101],
  [79, 89, 107, 115, 123, 130, 147, 139, 101],
  [84, 94, 103, 112, 135, 117, 109, 98],
  [84, 94, 103, 112, 120, 134, 109, 98],
  [84, 94, 103, 112, 120, 148, 133, 127],
  [84, 94, 103, 112, 120, 150, 133, 127],
  [86, 95, 104, 121, 129, 141, 132, 126],
  [86, 95, 104, 128, 134, 145, 132, 126],
  [87, 96, 105, 114, 123, 137, 132, 118],
  [87, 96, 105, 114, 130, 142, 138, 118],
  [87, 96, 113, 121, 129, 141, 132, 118],
  [87, 96, 113, 121, 135, 146, 138, 118],
  [88, 97, 105, 113, 121, 129, 141, 127, 119],
  [88, 97, 105, 113, 121, 135, 146, 133, 119],
  [88, 97, 105, 113, 128, 134, 145, 127, 119],
  [88, 97, 105, 113, 128, 140, 148, 133, 119],
  [88, 97, 105, 114, 123, 137, 127, 119],
  [88, 97, 105, 114, 130, 142, 133, 119],
  [89, 107, 115, 123, 130, 142, 138, 110],
  [89, 107, 115, 123, 130, 147, 143, 110],
  [90, 99, 107, 115, 123, 137, 127, 111],
  [90, 99, 107, 115, 123, 130, 142, 133, 111],
  [90, 99, 107, 115, 123, 130, 147, 139, 111],
  [90, 99, 107, 122, 129, 141, 127, 111],
  [90, 99, 107, 122, 129, 135, 146, 133, 111],
  [90, 99, 107, 122, 129, 135, 149, 139, 111],
  [90, 99, 108, 116, 124, 138, 133, 111],
  [90, 99, 108, 116, 124, 143, 139, 111],
  [91, 110, 118, 126, 132, 138, 143, 139],
  [97, 105, 113, 121, 129, 141, 132, 126],
  [97, 105, 113, 121, 135, 146, 138, 126],
  [97, 105, 113, 128, 134, 145, 132, 126]
]
def cycle (i : Fin 1164) := cycles[i.val - 1088]!
theorem checked : ∀ i : Fin 1164,
    1088 ≤ i.val → i.val < 1120 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 1088 ≤ i.val) (hhi : i.val < 1120) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry01088
end OmissionResidual
