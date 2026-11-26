import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00160
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [181, 196, 219, 228, 236, 247, 239, 198],
  [184, 199, 224, 241, 236, 228, 218, 203],
  [184, 199, 233, 245, 236, 228, 218, 203],
  [185, 213, 224, 246, 243, 230, 219, 204],
  [185, 213, 224, 249, 247, 230, 219, 204],
  [190, 203, 215, 234, 241, 229, 220, 208],
  [190, 203, 215, 240, 245, 229, 220, 208],
  [190, 203, 215, 234, 246, 238, 231, 208],
  [190, 203, 215, 240, 248, 238, 231, 208],
  [191, 204, 216, 226, 243, 238, 222, 209],
  [191, 204, 216, 226, 247, 244, 222, 209],
  [191, 204, 225, 234, 246, 238, 222, 209],
  [191, 204, 225, 234, 249, 244, 222, 209],
  [195, 208, 218, 227, 241, 246, 232, 223],
  [197, 209, 219, 228, 236, 247, 239, 212],
  [197, 209, 219, 235, 241, 249, 239, 212],
  [205, 216, 225, 234, 246, 238, 231, 220],
  [205, 216, 225, 234, 249, 244, 231, 220],
  [205, 216, 225, 240, 248, 238, 231, 220],
  [205, 216, 225, 240, 250, 244, 231, 220],
  [217, 226, 234, 240, 250, 244, 238, 229],
  [217, 226, 234, 240, 251, 244, 238, 229],
  [0, 7, 13, 22, 34, 50, 37, 27, 18],
  [0, 12, 19, 30, 45, 34, 25, 17, 11],
  [0, 12, 19, 30, 45, 64, 50, 37, 27, 18],
  [1, 7, 13, 22, 34, 50, 37, 27, 18],
  [1, 7, 20, 31, 46, 65, 51, 38, 18],
  [1, 12, 19, 30, 45, 34, 25, 17, 11],
  [1, 12, 28, 41, 59, 46, 35, 26, 11],
  [1, 12, 19, 30, 45, 64, 50, 37, 27, 18],
  [1, 12, 28, 41, 59, 81, 65, 51, 38, 18],
  [2, 7, 20, 31, 46, 65, 51, 38, 27]
]
def cycle (r : Fin 2685) := cycles[r.val - 160]!
theorem checked : ∀ r : Fin 2685,
    160 ≤ r.val → r.val < 192 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 160 ≤ r.val) (hhi : r.val < 192) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00160
