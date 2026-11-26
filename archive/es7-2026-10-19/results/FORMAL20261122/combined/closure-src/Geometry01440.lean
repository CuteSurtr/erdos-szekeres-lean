import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01440
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [33, 56, 88, 110, 136, 119, 84, 67],
  [33, 56, 88, 131, 157, 140, 104, 85, 67],
  [33, 56, 127, 168, 190, 175, 85, 67],
  [33, 56, 127, 186, 205, 192, 85, 67],
  [33, 56, 88, 107, 129, 155, 138, 102, 67],
  [33, 56, 71, 89, 179, 163, 145, 105],
  [33, 56, 71, 89, 196, 181, 164, 105],
  [33, 56, 88, 107, 194, 180, 145, 105],
  [33, 56, 88, 107, 209, 197, 164, 105],
  [33, 106, 126, 167, 189, 123, 85, 67],
  [33, 106, 126, 185, 204, 142, 85, 67],
  [34, 45, 59, 76, 95, 121, 103, 50],
  [34, 45, 59, 76, 95, 143, 124, 50],
  [34, 45, 91, 117, 99, 82, 65, 50],
  [34, 45, 109, 135, 99, 82, 65, 50],
  [34, 45, 74, 92, 118, 101, 83, 50],
  [34, 45, 74, 92, 113, 161, 144, 124, 50],
  [34, 45, 91, 110, 136, 119, 101, 83, 50],
  [34, 45, 109, 128, 154, 119, 101, 83, 50],
  [34, 45, 129, 150, 174, 159, 141, 50],
  [34, 45, 129, 150, 194, 180, 163, 50],
  [34, 45, 147, 167, 189, 159, 141, 50],
  [34, 45, 147, 167, 207, 180, 163, 50],
  [34, 45, 91, 110, 131, 114, 96, 79],
  [34, 45, 109, 128, 149, 114, 96, 79],
  [34, 75, 93, 114, 140, 122, 103, 50],
  [34, 75, 93, 114, 162, 144, 124, 50],
  [35, 46, 60, 77, 101, 84, 67, 51],
  [35, 46, 60, 94, 120, 102, 67, 51],
  [35, 46, 60, 77, 96, 122, 104, 85, 51],
  [35, 46, 60, 94, 115, 141, 123, 85, 51],
  [35, 46, 75, 93, 119, 84, 67, 51]
]
def cycle (r : Fin 2685) := cycles[r.val - 1440]!
theorem checked : ∀ r : Fin 2685,
    1440 ≤ r.val → r.val < 1472 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1440 ≤ r.val) (hhi : r.val < 1472) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01440
