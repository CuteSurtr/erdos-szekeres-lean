import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00992
def cycles : Array (List (Fin 154)) := #[
  [33, 43, 64, 75, 87, 99, 118, 111, 101],
  [33, 43, 74, 85, 96, 107, 125, 111, 101],
  [34, 53, 64, 75, 87, 99, 118, 111, 91],
  [34, 53, 64, 86, 97, 108, 126, 119, 91],
  [34, 53, 65, 77, 89, 110, 101, 91],
  [40, 49, 59, 81, 93, 131, 119, 111],
  [40, 49, 59, 92, 102, 136, 119, 111],
  [41, 50, 60, 71, 83, 126, 119, 101],
  [41, 50, 60, 71, 94, 132, 127, 101],
  [41, 50, 70, 81, 93, 131, 119, 101],
  [41, 50, 70, 81, 103, 137, 127, 101],
  [42, 62, 72, 83, 94, 132, 127, 91],
  [42, 62, 72, 83, 94, 138, 133, 91],
  [43, 74, 85, 96, 107, 125, 118, 110],
  [44, 53, 64, 75, 87, 99, 118, 111, 101],
  [44, 53, 64, 86, 97, 108, 126, 119, 101],
  [44, 53, 74, 85, 96, 107, 125, 111, 101],
  [44, 53, 74, 95, 105, 115, 131, 119, 101],
  [45, 65, 75, 86, 97, 108, 126, 119, 91],
  [45, 65, 75, 86, 106, 116, 132, 127, 91],
  [51, 60, 70, 81, 93, 131, 119, 111],
  [51, 60, 70, 81, 103, 137, 127, 111],
  [51, 60, 70, 92, 102, 136, 119, 111],
  [51, 60, 70, 92, 112, 141, 127, 111],
  [52, 62, 72, 83, 94, 132, 127, 101],
  [52, 62, 72, 83, 94, 138, 133, 101],
  [52, 62, 82, 93, 103, 137, 127, 101],
  [52, 62, 82, 93, 103, 142, 133, 101],
  [53, 74, 85, 96, 107, 125, 118, 110],
  [53, 74, 95, 105, 115, 131, 126, 110],
  [54, 64, 74, 85, 96, 107, 125, 111],
  [54, 64, 74, 95, 105, 115, 131, 119, 111]
]
def cycle (i : Fin 1164) := cycles[i.val - 992]!
theorem checked : ∀ i : Fin 1164,
    992 ≤ i.val → i.val < 1024 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 992 ≤ i.val) (hhi : i.val < 1024) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00992
end OmissionResidual
