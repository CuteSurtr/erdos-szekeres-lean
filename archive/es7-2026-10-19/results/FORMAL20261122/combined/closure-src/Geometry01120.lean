import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01120
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [10, 30, 54, 74, 98, 82, 66, 38, 27],
  [10, 30, 89, 111, 137, 120, 102, 27],
  [10, 30, 89, 132, 158, 141, 123, 27],
  [10, 70, 88, 110, 136, 119, 52, 27],
  [10, 70, 88, 131, 157, 140, 68, 27],
  [10, 30, 41, 56, 143, 124, 105, 86],
  [10, 30, 54, 71, 161, 144, 125, 86],
  [11, 25, 35, 48, 63, 85, 68, 18],
  [11, 25, 35, 48, 63, 105, 86, 18],
  [11, 34, 46, 61, 83, 67, 52, 18],
  [11, 45, 59, 81, 65, 51, 38, 18],
  [11, 45, 59, 76, 100, 83, 67, 52, 18],
  [11, 74, 92, 113, 139, 122, 104, 18],
  [11, 74, 92, 113, 161, 144, 125, 18],
  [11, 45, 59, 76, 95, 79, 63, 49],
  [12, 69, 87, 109, 91, 74, 59, 45],
  [12, 53, 70, 91, 117, 98, 81, 64],
  [13, 19, 53, 70, 55, 42, 31, 22],
  [13, 19, 69, 87, 55, 42, 31, 22],
  [13, 19, 53, 88, 72, 57, 43, 22],
  [13, 19, 69, 106, 72, 57, 43, 22],
  [13, 19, 28, 41, 59, 81, 65, 50],
  [13, 19, 28, 56, 76, 100, 83, 50],
  [13, 19, 39, 54, 74, 60, 46, 34],
  [13, 19, 39, 71, 92, 77, 61, 34],
  [13, 19, 39, 54, 74, 98, 82, 65, 50],
  [13, 19, 39, 71, 92, 118, 101, 83, 50],
  [13, 19, 107, 129, 155, 138, 120, 50],
  [13, 19, 126, 147, 171, 138, 120, 50],
  [13, 19, 53, 131, 157, 140, 122, 103],
  [13, 19, 69, 149, 173, 140, 122, 103],
  [13, 40, 55, 75, 99, 82, 65, 50]
]
def cycle (r : Fin 2685) := cycles[r.val - 1120]!
theorem checked : ∀ r : Fin 2685,
    1120 ≤ r.val → r.val < 1152 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1120 ≤ r.val) (hhi : r.val < 1152) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01120
