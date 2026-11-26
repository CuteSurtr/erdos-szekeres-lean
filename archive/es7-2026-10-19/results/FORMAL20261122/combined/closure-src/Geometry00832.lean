import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00832
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [103, 121, 157, 174, 191, 209, 197, 181, 124],
  [103, 121, 157, 174, 191, 222, 212, 198, 124],
  [103, 121, 173, 189, 204, 219, 197, 181, 124],
  [103, 121, 173, 189, 204, 230, 212, 198, 124],
  [104, 139, 157, 174, 191, 209, 197, 164, 125],
  [104, 139, 157, 174, 191, 222, 212, 182, 125],
  [104, 139, 157, 190, 205, 231, 223, 182, 125],
  [107, 126, 146, 200, 216, 205, 191, 174, 155],
  [107, 126, 146, 214, 226, 217, 191, 174, 155],
  [107, 126, 165, 213, 225, 205, 191, 174, 155],
  [107, 126, 165, 224, 234, 217, 191, 174, 155],
  [108, 127, 146, 165, 224, 187, 170, 151, 130],
  [108, 127, 146, 165, 233, 187, 170, 151, 130],
  [108, 127, 146, 165, 224, 234, 206, 192, 175, 156],
  [108, 127, 146, 165, 233, 240, 206, 192, 175, 156],
  [110, 128, 166, 184, 203, 190, 174, 157, 136],
  [110, 128, 166, 200, 216, 205, 191, 157, 136],
  [110, 128, 183, 199, 215, 190, 174, 157, 136],
  [110, 128, 183, 213, 225, 205, 191, 157, 136],
  [110, 128, 166, 184, 218, 208, 194, 178, 136],
  [110, 128, 166, 200, 228, 220, 209, 178, 136],
  [110, 128, 183, 199, 227, 208, 194, 178, 136],
  [110, 128, 183, 213, 235, 220, 209, 178, 136],
  [111, 147, 166, 200, 216, 205, 176, 158, 137],
  [111, 147, 166, 214, 226, 217, 176, 158, 137],
  [111, 147, 166, 200, 228, 220, 196, 179, 137],
  [111, 147, 166, 214, 236, 229, 196, 179, 137],
  [112, 129, 147, 166, 200, 216, 192, 177, 159, 138],
  [112, 129, 147, 166, 214, 226, 206, 177, 159, 138],
  [112, 129, 147, 183, 213, 225, 192, 177, 159, 138],
  [112, 129, 147, 183, 224, 234, 206, 177, 159, 138],
  [112, 129, 147, 166, 200, 228, 210, 197, 180, 138]
]
def cycle (r : Fin 2685) := cycles[r.val - 832]!
theorem checked : ∀ r : Fin 2685,
    832 ≤ r.val → r.val < 864 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 832 ≤ r.val) (hhi : r.val < 864) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00832
