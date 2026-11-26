import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02336
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [111, 129, 148, 201, 229, 196, 179, 137],
  [111, 147, 166, 184, 203, 190, 158, 137],
  [111, 147, 185, 204, 191, 176, 158, 137],
  [111, 147, 166, 184, 218, 208, 179, 137],
  [111, 147, 185, 219, 209, 196, 179, 137],
  [112, 129, 147, 166, 200, 170, 153, 133],
  [112, 129, 147, 166, 214, 187, 153, 133],
  [112, 129, 147, 183, 213, 170, 153, 133],
  [112, 129, 147, 183, 224, 187, 153, 133],
  [112, 129, 147, 166, 184, 203, 175, 159, 138],
  [112, 129, 147, 183, 199, 215, 175, 159, 138],
  [112, 129, 147, 185, 204, 177, 159, 138],
  [112, 129, 147, 233, 240, 177, 159, 138],
  [112, 129, 147, 166, 184, 218, 195, 180, 138],
  [112, 129, 147, 166, 237, 223, 212, 138],
  [112, 129, 147, 166, 243, 232, 212, 138],
  [112, 129, 147, 183, 199, 227, 195, 180, 138],
  [112, 129, 147, 185, 219, 197, 180, 138],
  [112, 129, 147, 233, 245, 197, 180, 138],
  [112, 129, 147, 183, 242, 223, 212, 138],
  [112, 129, 147, 183, 246, 232, 212, 138],
  [112, 129, 148, 168, 190, 175, 159, 138],
  [112, 129, 148, 186, 205, 192, 177, 159, 138],
  [112, 129, 148, 201, 217, 206, 177, 159, 138],
  [112, 129, 148, 168, 208, 195, 180, 138],
  [112, 129, 148, 186, 220, 210, 197, 180, 138],
  [112, 129, 148, 201, 229, 221, 197, 180, 138],
  [113, 131, 150, 169, 209, 196, 161, 139],
  [113, 131, 150, 169, 222, 211, 161, 139],
  [113, 131, 168, 186, 220, 196, 161, 139],
  [113, 131, 168, 186, 231, 211, 161, 139],
  [113, 149, 167, 207, 194, 179, 161, 139]
]
def cycle (r : Fin 2685) := cycles[r.val - 2336]!
theorem checked : ∀ r : Fin 2685,
    2336 ≤ r.val → r.val < 2368 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2336 ≤ r.val) (hhi : r.val < 2368) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02336
