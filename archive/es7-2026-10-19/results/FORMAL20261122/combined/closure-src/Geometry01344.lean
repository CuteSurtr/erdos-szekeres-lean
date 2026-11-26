import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01344
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [26, 91, 110, 131, 157, 140, 68, 38],
  [26, 91, 129, 150, 174, 159, 68, 38],
  [26, 91, 110, 131, 178, 162, 86, 38],
  [26, 91, 129, 150, 194, 180, 86, 38],
  [26, 59, 74, 92, 113, 96, 80, 49],
  [26, 59, 74, 111, 132, 115, 97, 49],
  [27, 50, 65, 83, 103, 124, 105, 86],
  [27, 50, 82, 101, 122, 144, 125, 86],
  [27, 64, 81, 100, 121, 103, 85, 68],
  [27, 64, 98, 118, 139, 122, 104, 68],
  [28, 53, 88, 110, 136, 118, 100, 81],
  [28, 53, 107, 129, 155, 137, 100, 81],
  [28, 69, 106, 128, 110, 92, 76, 59],
  [28, 69, 126, 147, 129, 111, 76, 59],
  [28, 69, 87, 109, 135, 117, 98, 81],
  [29, 39, 53, 107, 90, 73, 57, 42],
  [29, 39, 53, 127, 108, 73, 57, 42],
  [29, 39, 69, 126, 90, 73, 57, 42],
  [29, 39, 69, 146, 108, 73, 57, 42],
  [29, 39, 53, 88, 110, 93, 77, 60],
  [29, 39, 53, 70, 91, 117, 99, 82],
  [29, 39, 53, 88, 110, 136, 119, 101, 82],
  [29, 39, 53, 150, 174, 159, 141, 122],
  [29, 39, 53, 168, 190, 175, 141, 122],
  [29, 39, 69, 106, 128, 93, 77, 60],
  [29, 39, 69, 87, 109, 135, 99, 82],
  [29, 39, 69, 106, 128, 154, 119, 101, 82],
  [29, 39, 69, 167, 189, 159, 141, 122],
  [29, 39, 69, 184, 203, 175, 141, 122],
  [29, 39, 89, 111, 137, 120, 101, 82],
  [29, 39, 165, 183, 202, 120, 101, 82],
  [29, 40, 90, 112, 138, 120, 101, 82]
]
def cycle (r : Fin 2685) := cycles[r.val - 1344]!
theorem checked : ∀ r : Fin 2685,
    1344 ≤ r.val → r.val < 1376 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1344 ≤ r.val) (hhi : r.val < 1376) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01344
