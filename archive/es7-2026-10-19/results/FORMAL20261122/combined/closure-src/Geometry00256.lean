import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00256
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [10, 22, 42, 57, 96, 122, 104, 68, 27],
  [10, 30, 41, 56, 76, 100, 83, 67, 52, 27],
  [10, 30, 41, 56, 95, 121, 103, 85, 68, 27],
  [10, 30, 54, 71, 92, 118, 101, 84, 52, 27],
  [10, 30, 54, 71, 113, 139, 122, 104, 68, 27],
  [11, 34, 46, 61, 79, 103, 85, 68, 18],
  [11, 34, 46, 61, 79, 124, 105, 86, 18],
  [11, 45, 59, 76, 95, 121, 103, 85, 68, 18],
  [11, 45, 59, 76, 95, 143, 124, 105, 86, 18],
  [12, 69, 87, 109, 135, 117, 98, 81, 64],
  [13, 19, 53, 70, 91, 75, 60, 46, 34],
  [13, 19, 69, 87, 109, 75, 60, 46, 34],
  [13, 19, 53, 88, 110, 93, 77, 61, 34],
  [13, 19, 69, 106, 128, 93, 77, 61, 34],
  [13, 19, 53, 70, 91, 117, 99, 82, 65, 50],
  [13, 19, 53, 88, 110, 136, 119, 101, 83, 50],
  [13, 19, 69, 87, 109, 135, 99, 82, 65, 50],
  [13, 19, 69, 106, 128, 154, 119, 101, 83, 50],
  [14, 20, 29, 57, 77, 101, 84, 67, 51],
  [14, 20, 29, 73, 94, 120, 102, 67, 51],
  [14, 20, 40, 72, 93, 119, 84, 67, 51],
  [14, 20, 40, 90, 112, 138, 102, 67, 51],
  [14, 28, 39, 71, 92, 77, 62, 48, 35],
  [14, 28, 39, 89, 111, 94, 78, 48, 35],
  [14, 28, 53, 88, 110, 93, 62, 48, 35],
  [14, 28, 53, 107, 129, 112, 78, 48, 35],
  [14, 28, 39, 71, 92, 118, 101, 84, 67, 51],
  [14, 28, 39, 89, 111, 137, 120, 102, 67, 51],
  [14, 28, 53, 88, 110, 136, 119, 84, 67, 51],
  [14, 28, 53, 107, 129, 155, 138, 102, 67, 51],
  [15, 22, 42, 57, 77, 101, 84, 67, 37],
  [15, 22, 42, 57, 96, 122, 104, 85, 37]
]
def cycle (r : Fin 2685) := cycles[r.val - 256]!
theorem checked : ∀ r : Fin 2685,
    256 ≤ r.val → r.val < 288 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 256 ≤ r.val) (hhi : r.val < 288) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00256
