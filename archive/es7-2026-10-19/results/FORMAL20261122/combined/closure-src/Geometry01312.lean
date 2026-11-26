import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01312
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [25, 34, 60, 77, 101, 84, 67, 37],
  [25, 34, 75, 93, 119, 84, 67, 37],
  [25, 45, 74, 98, 82, 66, 51, 37],
  [25, 45, 91, 117, 99, 66, 51, 37],
  [25, 45, 59, 76, 100, 83, 67, 37],
  [25, 45, 59, 76, 95, 121, 103, 85, 37],
  [25, 45, 59, 76, 95, 143, 124, 105, 37],
  [25, 45, 74, 92, 118, 101, 84, 67, 37],
  [25, 45, 91, 110, 136, 119, 84, 67, 37],
  [25, 45, 111, 132, 158, 141, 123, 37],
  [25, 45, 111, 132, 179, 163, 145, 37],
  [25, 45, 129, 150, 174, 159, 123, 37],
  [25, 45, 129, 150, 194, 180, 145, 37],
  [25, 109, 128, 149, 173, 104, 85, 37],
  [25, 109, 128, 149, 193, 125, 105, 37],
  [25, 45, 74, 92, 113, 96, 80, 63],
  [25, 45, 91, 110, 131, 114, 80, 63],
  [26, 35, 47, 62, 80, 104, 68, 38],
  [26, 35, 47, 62, 80, 125, 86, 38],
  [26, 35, 47, 78, 97, 123, 68, 38],
  [26, 35, 47, 78, 97, 145, 86, 38],
  [26, 46, 60, 77, 101, 84, 52, 38],
  [26, 46, 60, 94, 120, 102, 52, 38],
  [26, 46, 61, 79, 103, 85, 68, 38],
  [26, 46, 61, 79, 124, 105, 86, 38],
  [26, 59, 76, 100, 83, 67, 52, 38],
  [26, 59, 74, 92, 118, 101, 84, 52, 38],
  [26, 59, 74, 111, 137, 120, 102, 52, 38],
  [26, 59, 76, 95, 121, 103, 85, 68, 38],
  [26, 59, 74, 152, 176, 160, 142, 38],
  [26, 59, 74, 152, 196, 181, 164, 38],
  [26, 59, 76, 95, 143, 124, 105, 86, 38]
]
def cycle (r : Fin 2685) := cycles[r.val - 1312]!
theorem checked : ∀ r : Fin 2685,
    1312 ≤ r.val → r.val < 1344 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1312 ≤ r.val) (hhi : r.val < 1344) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01312
