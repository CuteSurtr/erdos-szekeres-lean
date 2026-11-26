import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01536
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [41, 87, 106, 128, 110, 92, 76, 59],
  [41, 87, 126, 147, 129, 111, 76, 59],
  [41, 87, 106, 149, 131, 113, 95, 59],
  [41, 87, 126, 167, 150, 132, 95, 59],
  [41, 70, 88, 110, 136, 118, 100, 81],
  [41, 70, 88, 131, 157, 139, 121, 81],
  [41, 70, 107, 129, 155, 137, 100, 81],
  [41, 70, 107, 150, 174, 158, 121, 81],
  [42, 54, 70, 88, 110, 93, 77, 60],
  [42, 54, 70, 88, 131, 114, 96, 60],
  [42, 54, 87, 106, 128, 93, 77, 60],
  [42, 54, 87, 146, 166, 130, 94, 77, 60],
  [42, 54, 87, 106, 149, 114, 96, 60],
  [42, 54, 70, 88, 110, 136, 119, 101, 82],
  [42, 54, 70, 88, 131, 157, 140, 122, 82],
  [42, 54, 70, 169, 191, 177, 160, 82],
  [42, 54, 70, 186, 205, 192, 160, 82],
  [42, 54, 70, 107, 194, 180, 163, 144],
  [42, 54, 70, 127, 208, 195, 163, 144],
  [42, 54, 87, 106, 128, 154, 119, 101, 82],
  [42, 54, 87, 106, 149, 173, 140, 122, 82],
  [42, 54, 87, 185, 204, 177, 160, 82],
  [42, 54, 87, 200, 216, 192, 160, 82],
  [42, 54, 89, 111, 137, 120, 101, 82],
  [42, 54, 89, 132, 158, 141, 122, 82],
  [42, 54, 165, 183, 202, 120, 101, 82],
  [42, 54, 165, 199, 215, 141, 122, 82],
  [42, 54, 87, 126, 207, 180, 163, 144],
  [42, 54, 87, 146, 218, 195, 163, 144],
  [42, 55, 90, 112, 138, 120, 101, 82],
  [42, 55, 90, 133, 159, 141, 122, 82],
  [42, 55, 108, 130, 156, 120, 101, 82]
]
def cycle (r : Fin 2685) := cycles[r.val - 1536]!
theorem checked : ∀ r : Fin 2685,
    1536 ≤ r.val → r.val < 1568 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1536 ≤ r.val) (hhi : r.val < 1568) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01536
