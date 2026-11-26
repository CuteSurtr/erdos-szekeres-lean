import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01088
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [8, 13, 20, 31, 46, 65, 51, 37],
  [8, 13, 20, 43, 61, 83, 67, 37],
  [8, 19, 39, 54, 42, 32, 23, 15],
  [8, 19, 39, 71, 57, 44, 33, 15],
  [8, 19, 28, 41, 59, 46, 35, 25],
  [8, 19, 28, 56, 76, 61, 48, 25],
  [8, 19, 28, 41, 59, 81, 65, 51, 37],
  [8, 19, 28, 56, 76, 100, 83, 67, 37],
  [8, 19, 89, 111, 137, 120, 102, 37],
  [8, 19, 107, 129, 155, 138, 102, 37],
  [8, 19, 39, 113, 139, 122, 104, 85],
  [8, 19, 53, 131, 157, 140, 104, 85],
  [8, 69, 87, 109, 135, 66, 51, 37],
  [8, 69, 106, 128, 154, 84, 67, 37],
  [9, 20, 29, 42, 60, 82, 66, 38],
  [9, 20, 43, 61, 83, 67, 52, 38],
  [9, 28, 56, 76, 61, 48, 36, 26],
  [9, 28, 39, 54, 74, 60, 47, 26],
  [9, 28, 39, 54, 74, 98, 82, 66, 38],
  [9, 28, 41, 59, 81, 65, 51, 38],
  [9, 28, 56, 76, 100, 83, 67, 52, 38],
  [9, 28, 39, 113, 139, 122, 104, 68],
  [9, 28, 39, 132, 158, 141, 123, 68],
  [9, 53, 88, 110, 136, 119, 52, 38],
  [9, 53, 107, 129, 155, 138, 52, 38],
  [10, 15, 23, 33, 48, 67, 52, 27],
  [10, 15, 32, 44, 62, 84, 52, 27],
  [10, 30, 41, 59, 46, 35, 26, 17],
  [10, 30, 54, 74, 60, 47, 26, 17],
  [10, 22, 31, 46, 65, 51, 38, 27],
  [10, 22, 42, 60, 82, 66, 38, 27],
  [10, 30, 41, 59, 81, 65, 51, 38, 27]
]
def cycle (r : Fin 2685) := cycles[r.val - 1088]!
theorem checked : ∀ r : Fin 2685,
    1088 ≤ r.val → r.val < 1120 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1088 ≤ r.val) (hhi : r.val < 1120) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01088
