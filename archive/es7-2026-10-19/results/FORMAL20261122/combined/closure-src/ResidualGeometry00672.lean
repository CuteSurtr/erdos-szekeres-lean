import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00672
def cycles : Array (List (Fin 154)) := #[
  [36, 46, 69, 81, 95, 86, 75, 64],
  [36, 46, 80, 92, 104, 86, 75, 64],
  [36, 46, 69, 93, 105, 97, 87, 64],
  [36, 46, 80, 102, 113, 97, 87, 64],
  [37, 57, 69, 93, 105, 97, 77, 65],
  [37, 57, 69, 103, 114, 106, 77, 65],
  [38, 47, 57, 69, 93, 73, 63, 51],
  [38, 47, 57, 80, 102, 73, 63, 51],
  [38, 47, 57, 69, 103, 84, 63, 51],
  [38, 47, 57, 80, 112, 84, 63, 51],
  [38, 47, 57, 80, 113, 88, 78, 66],
  [38, 47, 80, 102, 113, 88, 78, 66],
  [38, 57, 80, 102, 113, 88, 78, 66],
  [38, 47, 58, 94, 106, 98, 78, 66],
  [38, 47, 69, 103, 114, 98, 78, 66],
  [38, 57, 69, 103, 114, 98, 78, 66],
  [38, 47, 80, 112, 121, 98, 78, 66],
  [38, 57, 80, 112, 121, 98, 78, 66],
  [39, 59, 70, 82, 96, 87, 77, 53],
  [39, 59, 81, 93, 105, 97, 77, 53],
  [39, 59, 70, 82, 107, 99, 89, 53],
  [39, 59, 81, 93, 115, 108, 89, 53],
  [40, 49, 59, 81, 95, 76, 66, 54],
  [40, 49, 59, 92, 104, 76, 66, 54],
  [40, 49, 71, 83, 97, 88, 78, 54],
  [40, 49, 59, 81, 105, 88, 78, 54],
  [40, 49, 59, 92, 113, 88, 78, 54],
  [40, 49, 71, 83, 108, 100, 90, 54],
  [40, 49, 59, 93, 115, 100, 90, 54],
  [40, 49, 59, 92, 122, 100, 90, 54],
  [40, 49, 59, 102, 122, 100, 90, 54],
  [40, 49, 92, 102, 122, 100, 90, 54]
]
def cycle (i : Fin 1164) := cycles[i.val - 672]!
theorem checked : ∀ i : Fin 1164,
    672 ≤ i.val → i.val < 704 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 672 ≤ i.val) (hhi : i.val < 704) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00672
end OmissionResidual
