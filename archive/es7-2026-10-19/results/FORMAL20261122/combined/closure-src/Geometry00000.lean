import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00000
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [0, 4, 8, 15, 25, 37, 27, 18],
  [0, 12, 19, 30, 22, 15, 10, 6],
  [0, 7, 13, 22, 34, 25, 17, 11],
  [1, 7, 13, 22, 34, 25, 17, 11],
  [1, 7, 20, 31, 46, 35, 26, 11],
  [2, 4, 21, 32, 47, 66, 38, 27],
  [2, 7, 20, 31, 46, 35, 26, 17],
  [2, 7, 29, 42, 60, 47, 26, 17],
  [2, 12, 39, 54, 42, 32, 16, 10],
  [3, 19, 28, 41, 31, 23, 16, 6],
  [3, 13, 20, 31, 46, 35, 26, 11],
  [3, 13, 20, 43, 61, 48, 36, 11],
  [4, 7, 29, 42, 60, 47, 35, 25],
  [4, 7, 40, 55, 75, 47, 35, 25],
  [4, 12, 53, 70, 55, 32, 23, 15],
  [5, 8, 14, 33, 48, 67, 52, 27],
  [5, 8, 21, 44, 62, 84, 52, 27],
  [5, 13, 20, 31, 46, 35, 26, 17],
  [5, 13, 20, 43, 61, 48, 36, 17],
  [5, 13, 29, 42, 60, 47, 26, 17],
  [5, 13, 29, 57, 77, 62, 36, 17],
  [6, 22, 31, 43, 61, 48, 36, 11],
  [6, 22, 31, 43, 79, 63, 49, 11],
  [6, 15, 23, 33, 63, 85, 68, 18],
  [8, 13, 29, 42, 60, 47, 35, 25],
  [8, 13, 29, 57, 77, 62, 48, 25],
  [8, 13, 40, 55, 75, 47, 35, 25],
  [8, 13, 40, 72, 93, 62, 48, 25],
  [8, 19, 53, 70, 55, 32, 23, 15],
  [8, 19, 53, 88, 72, 44, 33, 15],
  [9, 14, 21, 44, 62, 84, 52, 38],
  [9, 14, 21, 58, 78, 102, 52, 38]
]
def cycle (r : Fin 2685) := cycles[r.val - 0]!
theorem checked : ∀ r : Fin 2685,
    0 ≤ r.val → r.val < 32 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 0 ≤ r.val) (hhi : r.val < 32) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00000
