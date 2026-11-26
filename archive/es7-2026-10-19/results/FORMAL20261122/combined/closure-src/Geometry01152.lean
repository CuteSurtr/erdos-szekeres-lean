import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01152
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [13, 40, 72, 93, 119, 101, 83, 50],
  [14, 20, 29, 42, 60, 82, 66, 51],
  [14, 20, 40, 55, 75, 99, 66, 51],
  [14, 28, 39, 71, 57, 44, 33, 23],
  [14, 28, 39, 54, 74, 60, 47, 35],
  [14, 28, 53, 70, 91, 75, 47, 35],
  [14, 28, 39, 54, 74, 98, 82, 66, 51],
  [14, 28, 39, 113, 139, 122, 104, 85],
  [14, 28, 39, 132, 158, 141, 123, 85],
  [14, 28, 53, 70, 91, 117, 99, 66, 51],
  [14, 28, 56, 76, 100, 83, 67, 51],
  [14, 28, 127, 148, 172, 156, 67, 51],
  [14, 28, 53, 131, 157, 140, 104, 85],
  [14, 28, 53, 150, 174, 159, 123, 85],
  [14, 69, 106, 128, 154, 84, 67, 51],
  [14, 69, 126, 147, 171, 102, 67, 51],
  [15, 22, 31, 43, 61, 83, 67, 37],
  [15, 22, 31, 43, 79, 103, 85, 37],
  [15, 22, 42, 60, 82, 66, 51, 37],
  [15, 22, 55, 75, 99, 66, 51, 37],
  [15, 30, 54, 74, 60, 47, 35, 25],
  [15, 30, 70, 91, 75, 47, 35, 25],
  [15, 30, 41, 56, 76, 61, 48, 25],
  [15, 30, 41, 56, 95, 79, 63, 25],
  [15, 30, 41, 59, 81, 65, 51, 37],
  [15, 30, 41, 56, 76, 100, 83, 67, 37],
  [15, 30, 41, 56, 95, 121, 103, 85, 37],
  [15, 30, 54, 74, 98, 82, 66, 51, 37],
  [15, 30, 70, 91, 117, 99, 66, 51, 37],
  [15, 30, 89, 111, 137, 120, 102, 37],
  [15, 30, 89, 132, 158, 141, 123, 37],
  [15, 30, 107, 129, 155, 138, 102, 37]
]
def cycle (r : Fin 2685) := cycles[r.val - 1152]!
theorem checked : ∀ r : Fin 2685,
    1152 ≤ r.val → r.val < 1184 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1152 ≤ r.val) (hhi : r.val < 1184) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01152
