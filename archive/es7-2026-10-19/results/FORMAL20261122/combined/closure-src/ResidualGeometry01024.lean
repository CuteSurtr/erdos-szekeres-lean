import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry01024
def cycles : Array (List (Fin 154)) := #[
  [54, 64, 74, 104, 113, 122, 136, 119, 111],
  [54, 64, 86, 97, 108, 126, 119, 111],
  [55, 65, 75, 86, 97, 108, 126, 119, 101],
  [55, 65, 75, 86, 106, 116, 132, 127, 101],
  [55, 65, 75, 87, 99, 118, 111, 101],
  [55, 65, 85, 95, 105, 115, 131, 119, 101],
  [55, 65, 85, 95, 114, 123, 137, 127, 101],
  [55, 65, 85, 96, 107, 125, 111, 101],
  [56, 77, 87, 97, 106, 116, 132, 127, 91],
  [56, 77, 87, 97, 106, 124, 138, 133, 91],
  [56, 77, 87, 97, 108, 126, 119, 91],
  [61, 71, 81, 92, 112, 141, 127, 119],
  [61, 71, 81, 92, 120, 145, 127, 119],
  [63, 72, 82, 93, 103, 137, 127, 111],
  [63, 72, 82, 93, 103, 142, 133, 111],
  [63, 72, 82, 102, 112, 141, 127, 111],
  [63, 72, 82, 102, 112, 146, 133, 111],
  [64, 74, 95, 105, 115, 131, 126, 118],
  [64, 74, 104, 113, 122, 136, 126, 118],
  [65, 85, 95, 105, 115, 131, 126, 110],
  [65, 85, 95, 114, 123, 137, 132, 110],
  [66, 75, 85, 95, 105, 115, 131, 119, 111],
  [66, 75, 85, 95, 114, 123, 137, 127, 111],
  [66, 75, 85, 104, 113, 122, 136, 119, 111],
  [66, 75, 85, 104, 121, 129, 141, 127, 111],
  [66, 75, 86, 97, 108, 126, 119, 111],
  [66, 75, 86, 106, 116, 132, 127, 111],
  [67, 77, 87, 97, 106, 116, 132, 127, 101],
  [67, 77, 87, 97, 106, 124, 138, 133, 101],
  [67, 77, 87, 97, 108, 126, 119, 101],
  [67, 77, 96, 105, 114, 123, 137, 127, 101],
  [67, 77, 96, 105, 114, 130, 142, 133, 101]
]
def cycle (i : Fin 1164) := cycles[i.val - 1024]!
theorem checked : ∀ i : Fin 1164,
    1024 ≤ i.val → i.val < 1056 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 1024 ≤ i.val) (hhi : i.val < 1056) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry01024
end OmissionResidual
