import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00032
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [9, 28, 39, 71, 57, 44, 24, 16],
  [9, 28, 39, 89, 73, 58, 24, 16],
  [9, 20, 29, 57, 77, 62, 36, 26],
  [9, 20, 29, 73, 94, 78, 36, 26],
  [10, 15, 23, 33, 63, 85, 68, 27],
  [10, 15, 32, 44, 80, 104, 68, 27],
  [10, 22, 31, 43, 61, 48, 36, 17],
  [10, 22, 31, 43, 79, 63, 49, 17],
  [10, 22, 42, 57, 77, 62, 36, 17],
  [10, 22, 42, 57, 96, 80, 49, 17],
  [14, 20, 29, 57, 77, 62, 48, 35],
  [14, 20, 29, 73, 94, 78, 48, 35],
  [14, 20, 40, 72, 93, 62, 48, 35],
  [14, 20, 40, 90, 112, 78, 48, 35],
  [14, 28, 39, 89, 73, 58, 33, 23],
  [14, 28, 53, 88, 72, 44, 33, 23],
  [14, 28, 53, 107, 90, 58, 33, 23],
  [15, 22, 42, 57, 77, 62, 48, 25],
  [15, 22, 42, 57, 96, 80, 63, 25],
  [15, 22, 55, 72, 93, 62, 48, 25],
  [15, 22, 55, 72, 114, 80, 63, 25],
  [16, 23, 32, 44, 80, 104, 68, 38],
  [16, 23, 32, 58, 78, 102, 52, 38],
  [16, 23, 32, 58, 97, 123, 68, 38],
  [16, 31, 42, 57, 77, 62, 36, 26],
  [16, 31, 42, 73, 94, 78, 36, 26],
  [16, 31, 42, 57, 96, 80, 49, 26],
  [16, 31, 42, 73, 115, 97, 49, 26],
  [21, 29, 40, 90, 112, 78, 62, 47],
  [21, 29, 40, 108, 130, 78, 62, 47],
  [21, 39, 53, 107, 90, 58, 44, 32],
  [22, 55, 72, 114, 140, 122, 103, 50]
]
def cycle (r : Fin 2685) := cycles[r.val - 32]!
theorem checked : ∀ r : Fin 2685,
    32 ≤ r.val → r.val < 64 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 32 ≤ r.val) (hhi : r.val < 64) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00032
