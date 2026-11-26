import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01056
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [4, 12, 28, 41, 59, 81, 65, 51, 37],
  [4, 12, 71, 92, 118, 101, 84, 67],
  [4, 12, 88, 110, 136, 119, 84, 67],
  [4, 69, 87, 109, 135, 66, 51, 37],
  [5, 8, 14, 23, 35, 51, 38, 27],
  [5, 8, 21, 32, 47, 66, 38, 27],
  [5, 19, 28, 41, 31, 23, 16, 10],
  [5, 19, 39, 54, 42, 32, 16, 10],
  [5, 19, 28, 56, 43, 33, 24, 10],
  [5, 19, 39, 71, 57, 44, 24, 10],
  [5, 19, 30, 45, 64, 50, 37, 27],
  [5, 19, 89, 111, 137, 120, 102, 27],
  [5, 19, 28, 95, 121, 103, 85, 68],
  [5, 19, 39, 113, 139, 122, 104, 68],
  [5, 53, 70, 91, 117, 99, 38, 27],
  [5, 53, 88, 110, 136, 119, 52, 27],
  [6, 30, 41, 59, 46, 35, 26, 11],
  [6, 15, 23, 33, 48, 67, 52, 18],
  [6, 22, 31, 46, 65, 51, 38, 18],
  [6, 30, 45, 64, 50, 37, 27, 18],
  [6, 30, 41, 59, 81, 65, 51, 38, 18],
  [6, 54, 71, 92, 118, 101, 84, 18],
  [6, 54, 71, 113, 139, 122, 104, 18],
  [6, 30, 41, 56, 143, 124, 105, 86],
  [7, 12, 53, 70, 55, 42, 31, 22],
  [7, 12, 69, 87, 55, 42, 31, 22],
  [7, 12, 28, 41, 59, 81, 65, 50],
  [7, 12, 39, 54, 74, 60, 46, 34],
  [7, 12, 39, 54, 74, 98, 82, 65, 50],
  [7, 12, 88, 110, 136, 119, 101, 83],
  [7, 12, 106, 128, 154, 119, 101, 83],
  [7, 40, 55, 75, 99, 82, 65, 50]
]
def cycle (r : Fin 2685) := cycles[r.val - 1056]!
theorem checked : ∀ r : Fin 2685,
    1056 ≤ r.val → r.val < 1088 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1056 ≤ r.val) (hhi : r.val < 1088) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01056
