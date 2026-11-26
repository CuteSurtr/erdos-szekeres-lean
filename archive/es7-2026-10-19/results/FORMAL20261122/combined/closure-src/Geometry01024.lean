import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01024
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [201, 214, 224, 233, 250, 244, 238, 229, 217],
  [201, 214, 224, 233, 251, 244, 238, 229, 217],
  [206, 217, 226, 234, 240, 250, 239, 232, 221],
  [206, 217, 226, 234, 240, 251, 239, 232, 221],
  [0, 28, 41, 59, 81, 65, 51, 38],
  [1, 4, 8, 15, 25, 37, 27, 18],
  [1, 4, 14, 23, 35, 51, 38, 18],
  [1, 12, 19, 30, 22, 15, 10, 6],
  [1, 12, 28, 41, 31, 23, 16, 6],
  [1, 12, 56, 76, 100, 83, 67, 52],
  [1, 39, 54, 74, 98, 82, 66, 18],
  [2, 4, 14, 23, 35, 51, 38, 27],
  [2, 7, 13, 22, 34, 50, 37, 27],
  [2, 12, 28, 41, 31, 23, 16, 10],
  [2, 12, 19, 30, 45, 34, 25, 17],
  [2, 12, 19, 30, 45, 64, 50, 37, 27],
  [2, 12, 56, 76, 100, 83, 67, 52],
  [2, 12, 71, 92, 118, 101, 84, 52],
  [2, 53, 70, 91, 117, 99, 38, 27],
  [3, 19, 28, 56, 43, 33, 24, 6],
  [3, 8, 14, 23, 35, 51, 38, 18],
  [3, 8, 14, 33, 48, 67, 52, 18],
  [3, 19, 30, 45, 34, 25, 17, 11],
  [3, 13, 22, 34, 50, 37, 27, 18],
  [3, 19, 30, 45, 64, 50, 37, 27, 18],
  [3, 39, 54, 74, 98, 82, 66, 18],
  [3, 39, 71, 92, 118, 101, 84, 18],
  [3, 19, 28, 95, 121, 103, 85, 68],
  [4, 7, 20, 31, 46, 65, 51, 37],
  [4, 12, 39, 54, 42, 32, 23, 15],
  [4, 12, 19, 30, 45, 64, 50, 37],
  [4, 12, 28, 41, 59, 46, 35, 25]
]
def cycle (r : Fin 2685) := cycles[r.val - 1024]!
theorem checked : ∀ r : Fin 2685,
    1024 ≤ r.val → r.val < 1056 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1024 ≤ r.val) (hhi : r.val < 1056) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01024
