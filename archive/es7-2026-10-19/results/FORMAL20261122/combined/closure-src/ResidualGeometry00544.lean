import ResidualCycleIndex
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
namespace ResidualGeometry00544
def cycles : Array (List (Fin 154)) := #[
  [14, 20, 36, 47, 75, 66, 55, 33],
  [14, 20, 36, 60, 75, 66, 55, 33],
  [14, 20, 46, 70, 85, 66, 55, 33],
  [14, 20, 36, 47, 87, 78, 67, 33],
  [14, 20, 36, 72, 87, 78, 67, 33],
  [15, 27, 36, 47, 60, 51, 32, 24],
  [15, 27, 36, 58, 71, 61, 32, 24],
  [15, 27, 36, 47, 72, 63, 42, 24],
  [15, 27, 36, 58, 83, 73, 42, 24],
  [15, 27, 37, 50, 65, 55, 45, 34],
  [15, 27, 36, 60, 75, 66, 45, 34],
  [15, 27, 37, 62, 77, 67, 56, 34],
  [15, 27, 36, 47, 87, 78, 56, 34],
  [16, 30, 39, 50, 65, 55, 45, 25],
  [16, 30, 49, 60, 75, 66, 45, 25],
  [16, 30, 39, 50, 77, 67, 56, 25],
  [16, 30, 49, 60, 87, 78, 56, 25],
  [16, 30, 60, 72, 87, 78, 56, 25],
  [16, 30, 39, 50, 89, 79, 68, 25],
  [16, 30, 39, 62, 89, 79, 68, 25],
  [16, 30, 50, 62, 89, 79, 68, 25],
  [16, 39, 50, 62, 89, 79, 68, 25],
  [16, 30, 49, 60, 99, 90, 68, 25],
  [16, 30, 49, 72, 99, 90, 68, 25],
  [16, 30, 60, 72, 99, 90, 68, 25],
  [18, 35, 57, 70, 85, 75, 65, 53],
  [18, 35, 69, 81, 95, 86, 65, 53],
  [19, 26, 35, 69, 81, 61, 51, 40],
  [19, 26, 35, 80, 92, 61, 51, 40],
  [19, 26, 58, 71, 86, 76, 66, 54],
  [19, 26, 35, 81, 95, 76, 66, 54],
  [19, 26, 35, 80, 104, 76, 66, 54]
]
def cycle (i : Fin 1164) := cycles[i.val - 544]!
theorem checked : ∀ i : Fin 1164,
    544 ≤ i.val → i.val < 576 →
    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧
      (cycle i).length - 7 = demand (cycleRow i) := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 1164) (hlo : 544 ≤ i.val) (hhi : i.val < 576) :
    demand (cycleRow i) ≤ (support (cycleRow i) \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi
  simpa only [hs, hd] using
    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid
#print axioms row_bound
end ResidualGeometry00544
end OmissionResidual
