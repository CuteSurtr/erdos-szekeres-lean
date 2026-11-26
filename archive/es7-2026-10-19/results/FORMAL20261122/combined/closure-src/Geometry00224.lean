import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00224
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [6, 22, 31, 43, 79, 103, 85, 68, 18],
  [6, 30, 41, 56, 76, 100, 83, 67, 52, 18],
  [6, 30, 41, 56, 95, 121, 103, 85, 68, 18],
  [7, 12, 53, 70, 91, 75, 60, 46, 34],
  [7, 12, 69, 87, 109, 75, 60, 46, 34],
  [7, 12, 53, 70, 91, 117, 99, 82, 65, 50],
  [7, 12, 69, 87, 109, 135, 99, 82, 65, 50],
  [8, 13, 29, 42, 60, 82, 66, 51, 37],
  [8, 13, 29, 57, 77, 101, 84, 67, 37],
  [8, 13, 40, 55, 75, 99, 66, 51, 37],
  [8, 13, 40, 72, 93, 119, 84, 67, 37],
  [8, 19, 39, 54, 74, 60, 47, 35, 25],
  [8, 19, 53, 70, 91, 75, 47, 35, 25],
  [8, 19, 39, 71, 92, 77, 62, 48, 25],
  [8, 19, 53, 88, 110, 93, 62, 48, 25],
  [8, 19, 39, 54, 74, 98, 82, 66, 51, 37],
  [8, 19, 39, 71, 92, 118, 101, 84, 67, 37],
  [8, 19, 53, 70, 91, 117, 99, 66, 51, 37],
  [8, 19, 53, 88, 110, 136, 119, 84, 67, 37],
  [9, 20, 29, 57, 77, 101, 84, 52, 38],
  [9, 20, 29, 73, 94, 120, 102, 52, 38],
  [9, 28, 39, 71, 92, 77, 62, 36, 26],
  [9, 28, 39, 89, 111, 94, 78, 36, 26],
  [9, 28, 39, 71, 92, 118, 101, 84, 52, 38],
  [9, 28, 39, 89, 111, 137, 120, 102, 52, 38],
  [10, 30, 41, 56, 76, 61, 48, 36, 17],
  [10, 30, 54, 71, 92, 77, 62, 36, 17],
  [10, 30, 41, 56, 95, 79, 63, 49, 17],
  [10, 30, 54, 71, 113, 96, 80, 49, 17],
  [10, 22, 31, 43, 61, 83, 67, 52, 27],
  [10, 22, 31, 43, 79, 103, 85, 68, 27],
  [10, 22, 42, 57, 77, 101, 84, 52, 27]
]
def cycle (r : Fin 2685) := cycles[r.val - 224]!
theorem checked : ∀ r : Fin 2685,
    224 ≤ r.val → r.val < 256 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 224 ≤ r.val) (hhi : r.val < 256) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00224
