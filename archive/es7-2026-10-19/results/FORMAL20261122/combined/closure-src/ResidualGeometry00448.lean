import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00448
def cycles : Array (List (Fin 154)) := #[
  [73, 83, 93, 102, 120, 140, 117, 100],
  [76, 86, 95, 104, 121, 129, 109, 100],
  [76, 86, 95, 104, 128, 134, 109, 100],
  [78, 87, 96, 105, 114, 123, 109, 90],
  [78, 87, 96, 113, 121, 129, 109, 90],
  [78, 87, 96, 105, 114, 130, 117, 90],
  [78, 87, 96, 113, 121, 135, 117, 90],
  [84, 94, 103, 112, 120, 144, 109, 98],
  [84, 94, 103, 112, 120, 140, 117, 98],
  [84, 94, 103, 112, 120, 144, 117, 98],
  [84, 94, 103, 112, 120, 140, 117, 109],
  [84, 94, 103, 112, 120, 144, 117, 109],
  [88, 97, 105, 113, 121, 129, 109, 100],
  [88, 97, 105, 113, 128, 134, 109, 100],
  [88, 97, 105, 113, 121, 135, 117, 100],
  [88, 97, 105, 113, 128, 140, 117, 100],
  [98, 106, 114, 121, 128, 140, 117, 109],
  [98, 106, 114, 121, 128, 144, 117, 109],
  [0, 7, 12, 20, 30, 23, 16, 11],
  [0, 7, 12, 20, 43, 33, 25, 17],
  [1, 7, 12, 20, 30, 23, 16, 11],
  [1, 7, 18, 27, 39, 31, 24, 11],
  [1, 7, 12, 20, 43, 33, 25, 17],
  [2, 7, 18, 27, 39, 31, 24, 16],
  [2, 7, 26, 36, 49, 40, 24, 16],
  [2, 7, 26, 36, 64, 54, 34, 25],
  [3, 12, 18, 27, 39, 31, 24, 11],
  [3, 12, 18, 37, 50, 41, 32, 11],
  [3, 12, 18, 37, 65, 55, 45, 17],
  [3, 12, 18, 50, 65, 55, 45, 17],
  [4, 7, 26, 36, 49, 40, 31, 23],
  [4, 7, 35, 46, 59, 40, 31, 23]
]
def cycle (i : Fin 1164) := cycles[i.val - 448]!
theorem checked : ∀ i : Fin 1164,
    448 ≤ i.val → i.val < 480 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 448 ≤ i.val) (hhi : i.val < 480) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00448
end OmissionResidual
