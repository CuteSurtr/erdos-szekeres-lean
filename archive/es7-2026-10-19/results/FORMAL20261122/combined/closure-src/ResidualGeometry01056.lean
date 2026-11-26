import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry01056
def cycles : Array (List (Fin 154)) := #[
  [67, 77, 96, 105, 115, 131, 119, 101],
  [68, 79, 90, 100, 109, 117, 133, 91],
  [68, 79, 90, 100, 109, 117, 139, 91],
  [68, 89, 99, 108, 116, 124, 138, 133, 91],
  [68, 89, 99, 108, 116, 124, 143, 139, 91],
  [68, 89, 99, 108, 116, 132, 127, 91],
  [73, 83, 93, 102, 112, 141, 127, 119],
  [73, 83, 93, 102, 112, 146, 133, 119],
  [73, 83, 93, 102, 120, 145, 127, 119],
  [73, 83, 93, 102, 120, 148, 133, 119],
  [75, 85, 95, 105, 115, 131, 126, 118],
  [75, 85, 95, 114, 123, 137, 132, 118],
  [75, 85, 104, 113, 122, 136, 126, 118],
  [75, 85, 104, 121, 129, 141, 132, 118],
  [76, 86, 95, 104, 113, 122, 136, 119],
  [76, 86, 95, 104, 121, 129, 141, 127, 119],
  [76, 86, 95, 104, 128, 134, 145, 127, 119],
  [76, 86, 95, 114, 123, 137, 127, 119],
  [77, 96, 105, 114, 123, 137, 132, 110],
  [77, 96, 105, 114, 130, 142, 138, 110],
  [78, 87, 96, 105, 114, 123, 137, 127, 111],
  [78, 87, 96, 105, 114, 130, 142, 133, 111],
  [78, 87, 96, 105, 115, 131, 119, 111],
  [78, 87, 96, 113, 122, 136, 119, 111],
  [78, 87, 96, 113, 121, 129, 141, 127, 111],
  [78, 87, 96, 113, 121, 135, 146, 133, 111],
  [78, 87, 97, 106, 116, 132, 127, 111],
  [78, 87, 97, 106, 124, 138, 133, 111],
  [79, 89, 99, 108, 116, 124, 138, 133, 101],
  [79, 89, 99, 108, 116, 124, 143, 139, 101],
  [79, 89, 99, 108, 116, 132, 127, 101],
  [79, 89, 107, 115, 123, 137, 127, 101]
]
def cycle (i : Fin 1164) := cycles[i.val - 1056]!
theorem checked : ∀ i : Fin 1164,
    1056 ≤ i.val → i.val < 1088 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 1056 ≤ i.val) (hhi : i.val < 1088) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry01056
end OmissionResidual
