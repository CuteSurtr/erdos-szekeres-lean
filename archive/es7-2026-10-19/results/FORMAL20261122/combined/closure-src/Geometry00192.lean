import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00192
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [2, 7, 29, 42, 60, 82, 66, 38, 27],
  [2, 12, 28, 41, 59, 46, 35, 26, 17],
  [2, 12, 39, 54, 74, 60, 47, 26, 17],
  [2, 12, 28, 41, 59, 81, 65, 51, 38, 27],
  [2, 12, 39, 54, 74, 98, 82, 66, 38, 27],
  [3, 19, 28, 41, 59, 46, 35, 26, 11],
  [3, 19, 28, 56, 76, 61, 48, 36, 11],
  [3, 13, 20, 31, 46, 65, 51, 38, 18],
  [3, 13, 20, 43, 61, 83, 67, 52, 18],
  [3, 19, 28, 41, 59, 81, 65, 51, 38, 18],
  [3, 19, 28, 56, 76, 100, 83, 67, 52, 18],
  [4, 7, 29, 42, 60, 82, 66, 51, 37],
  [4, 7, 40, 55, 75, 99, 66, 51, 37],
  [4, 12, 39, 54, 74, 60, 47, 35, 25],
  [4, 12, 53, 70, 91, 75, 47, 35, 25],
  [4, 12, 39, 54, 74, 98, 82, 66, 51, 37],
  [4, 12, 53, 70, 91, 117, 99, 66, 51, 37],
  [5, 13, 20, 31, 46, 65, 51, 38, 27],
  [5, 13, 20, 43, 61, 83, 67, 52, 27],
  [5, 13, 29, 42, 60, 82, 66, 38, 27],
  [5, 13, 29, 57, 77, 101, 84, 52, 27],
  [5, 19, 28, 41, 59, 46, 35, 26, 17],
  [5, 19, 39, 54, 74, 60, 47, 26, 17],
  [5, 19, 28, 56, 76, 61, 48, 36, 17],
  [5, 19, 39, 71, 92, 77, 62, 36, 17],
  [5, 19, 28, 41, 59, 81, 65, 51, 38, 27],
  [5, 19, 28, 56, 76, 100, 83, 67, 52, 27],
  [5, 19, 39, 54, 74, 98, 82, 66, 38, 27],
  [5, 19, 39, 71, 92, 118, 101, 84, 52, 27],
  [6, 30, 41, 56, 76, 61, 48, 36, 11],
  [6, 30, 41, 56, 95, 79, 63, 49, 11],
  [6, 22, 31, 43, 61, 83, 67, 52, 18]
]
def cycle (r : Fin 2685) := cycles[r.val - 192]!
theorem checked : ∀ r : Fin 2685,
    192 ≤ r.val → r.val < 224 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 192 ≤ r.val) (hhi : r.val < 224) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00192
