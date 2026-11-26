import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00576
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [55, 70, 87, 146, 166, 188, 156, 138, 119, 99],
  [55, 70, 87, 165, 183, 202, 156, 138, 119, 99],
  [55, 70, 87, 146, 184, 203, 175, 159, 140, 99],
  [55, 70, 87, 165, 199, 215, 175, 159, 140, 99],
  [56, 106, 126, 167, 189, 174, 158, 121, 100],
  [56, 106, 126, 185, 204, 191, 176, 121, 100],
  [57, 71, 88, 107, 150, 133, 115, 96, 77],
  [57, 71, 88, 107, 169, 153, 134, 96, 77],
  [57, 71, 88, 127, 168, 151, 115, 96, 77],
  [57, 71, 88, 127, 186, 170, 134, 96, 77],
  [57, 71, 106, 126, 167, 133, 115, 96, 77],
  [57, 71, 106, 146, 184, 151, 115, 96, 77],
  [57, 71, 106, 126, 185, 153, 134, 96, 77],
  [57, 71, 106, 146, 200, 170, 134, 96, 77],
  [57, 71, 88, 107, 169, 191, 177, 160, 122, 101],
  [57, 71, 88, 127, 168, 190, 175, 141, 122, 101],
  [57, 71, 88, 127, 186, 205, 192, 160, 122, 101],
  [57, 71, 106, 126, 167, 189, 159, 141, 122, 101],
  [57, 71, 106, 126, 185, 204, 177, 160, 122, 101],
  [57, 71, 106, 146, 184, 203, 175, 141, 122, 101],
  [57, 71, 106, 146, 200, 216, 192, 160, 122, 101],
  [58, 73, 90, 108, 170, 192, 142, 123, 102],
  [58, 73, 90, 108, 187, 206, 142, 123, 102],
  [58, 89, 107, 127, 186, 170, 116, 97, 78],
  [58, 89, 107, 127, 201, 187, 116, 97, 78],
  [58, 89, 107, 127, 186, 205, 192, 142, 123, 102],
  [58, 89, 107, 127, 201, 217, 206, 142, 123, 102],
  [58, 89, 107, 127, 168, 190, 175, 123, 102],
  [58, 89, 107, 169, 191, 177, 142, 123, 102],
  [59, 109, 128, 149, 173, 157, 139, 121, 81],
  [59, 109, 147, 167, 189, 174, 158, 121, 81],
  [59, 109, 128, 149, 193, 178, 161, 143, 81]
]
def cycle (r : Fin 2685) := cycles[r.val - 576]!
theorem checked : ∀ r : Fin 2685,
    576 ≤ r.val → r.val < 608 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 576 ≤ r.val) (hhi : r.val < 608) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00576
