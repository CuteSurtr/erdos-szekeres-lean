import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01248
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [21, 29, 73, 94, 120, 102, 84, 66],
  [21, 39, 53, 127, 108, 58, 44, 32],
  [21, 39, 53, 88, 110, 93, 62, 47],
  [21, 39, 89, 111, 94, 78, 62, 47],
  [21, 39, 53, 70, 91, 117, 99, 66],
  [21, 39, 53, 88, 110, 136, 119, 84, 66],
  [21, 39, 53, 150, 174, 159, 123, 104],
  [21, 39, 53, 168, 190, 175, 123, 104],
  [21, 39, 71, 92, 118, 101, 84, 66],
  [21, 39, 89, 111, 137, 120, 102, 84, 66],
  [21, 69, 126, 147, 171, 102, 84, 66],
  [21, 69, 146, 166, 188, 102, 84, 66],
  [22, 30, 70, 91, 75, 60, 46, 34],
  [22, 30, 87, 109, 75, 60, 46, 34],
  [22, 30, 54, 71, 92, 77, 61, 34],
  [22, 30, 54, 71, 113, 96, 79, 34],
  [22, 30, 41, 56, 76, 100, 83, 50],
  [22, 30, 41, 56, 95, 121, 103, 50],
  [22, 30, 54, 74, 98, 82, 65, 50],
  [22, 30, 54, 71, 92, 118, 101, 83, 50],
  [22, 30, 54, 71, 113, 139, 122, 103, 50],
  [22, 30, 70, 91, 117, 99, 82, 65, 50],
  [22, 30, 87, 109, 135, 99, 82, 65, 50],
  [22, 30, 107, 129, 155, 138, 120, 50],
  [22, 30, 107, 150, 174, 159, 141, 50],
  [22, 30, 126, 147, 171, 138, 120, 50],
  [22, 30, 126, 167, 189, 159, 141, 50],
  [22, 30, 70, 88, 178, 162, 144, 124],
  [22, 30, 87, 106, 193, 162, 144, 124],
  [22, 55, 72, 93, 119, 101, 83, 50],
  [23, 31, 42, 57, 77, 62, 48, 35],
  [23, 41, 54, 71, 92, 77, 62, 48, 35]
]
def cycle (r : Fin 2685) := cycles[r.val - 1248]!
theorem checked : ∀ r : Fin 2685,
    1248 ≤ r.val → r.val < 1280 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1248 ≤ r.val) (hhi : r.val < 1280) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01248
