import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00288
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [15, 22, 55, 72, 93, 119, 84, 67, 37],
  [15, 22, 55, 72, 114, 140, 104, 85, 37],
  [15, 30, 54, 71, 92, 77, 62, 48, 25],
  [15, 30, 70, 88, 110, 93, 62, 48, 25],
  [15, 30, 54, 71, 113, 96, 80, 63, 25],
  [15, 30, 70, 88, 131, 114, 80, 63, 25],
  [15, 30, 54, 71, 92, 118, 101, 84, 67, 37],
  [15, 30, 54, 71, 113, 139, 122, 104, 85, 37],
  [15, 30, 70, 88, 110, 136, 119, 84, 67, 37],
  [15, 30, 70, 88, 131, 157, 140, 104, 85, 37],
  [16, 41, 54, 71, 92, 77, 62, 36, 26],
  [16, 41, 54, 89, 111, 94, 78, 36, 26],
  [16, 41, 54, 71, 113, 96, 80, 49, 26],
  [16, 41, 54, 89, 132, 115, 97, 49, 26],
  [16, 31, 42, 57, 77, 101, 84, 52, 38],
  [16, 31, 42, 73, 94, 120, 102, 52, 38],
  [16, 31, 42, 57, 96, 122, 104, 68, 38],
  [16, 31, 42, 73, 115, 141, 123, 68, 38],
  [16, 41, 54, 71, 92, 118, 101, 84, 52, 38],
  [16, 41, 54, 89, 111, 137, 120, 102, 52, 38],
  [16, 41, 54, 71, 113, 139, 122, 104, 68, 38],
  [16, 41, 54, 89, 132, 158, 141, 123, 68, 38],
  [17, 34, 46, 61, 79, 103, 85, 68, 27],
  [17, 34, 46, 61, 79, 124, 105, 86, 27],
  [17, 34, 60, 77, 96, 122, 104, 68, 27],
  [17, 34, 60, 77, 96, 144, 125, 86, 27],
  [17, 45, 59, 76, 95, 121, 103, 85, 68, 27],
  [17, 45, 59, 76, 95, 143, 124, 105, 86, 27],
  [17, 45, 74, 92, 113, 139, 122, 104, 68, 27],
  [17, 45, 74, 92, 113, 161, 144, 125, 86, 27],
  [18, 64, 81, 100, 121, 143, 124, 105, 86],
  [19, 69, 87, 109, 135, 117, 98, 81, 64]
]
def cycle (r : Fin 2685) := cycles[r.val - 288]!
theorem checked : ∀ r : Fin 2685,
    288 ≤ r.val → r.val < 320 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 288 ≤ r.val) (hhi : r.val < 320) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00288
