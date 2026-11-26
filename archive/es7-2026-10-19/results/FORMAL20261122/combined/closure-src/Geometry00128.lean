import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00128
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [155, 171, 188, 226, 236, 229, 209, 194],
  [155, 171, 202, 225, 235, 220, 209, 194],
  [155, 171, 202, 234, 241, 229, 209, 194],
  [157, 173, 203, 216, 228, 220, 209, 178],
  [157, 173, 203, 216, 237, 231, 222, 178],
  [157, 173, 215, 225, 235, 220, 209, 178],
  [157, 173, 215, 225, 242, 231, 222, 178],
  [158, 189, 203, 216, 228, 220, 196, 179],
  [158, 189, 203, 226, 236, 229, 196, 179],
  [158, 189, 203, 216, 237, 231, 211, 179],
  [158, 189, 203, 226, 243, 238, 211, 179],
  [162, 178, 193, 218, 228, 237, 223, 212],
  [162, 178, 193, 227, 235, 242, 223, 212],
  [163, 179, 207, 218, 228, 237, 223, 198],
  [163, 179, 207, 218, 236, 243, 232, 198],
  [166, 183, 224, 241, 236, 228, 218, 188],
  [166, 183, 233, 245, 236, 228, 218, 188],
  [167, 199, 213, 235, 228, 219, 207, 189],
  [167, 199, 224, 241, 236, 219, 207, 189],
  [167, 199, 224, 246, 243, 230, 207, 189],
  [172, 188, 202, 234, 241, 229, 220, 208],
  [172, 188, 202, 240, 245, 229, 220, 208],
  [174, 189, 203, 216, 228, 220, 209, 194],
  [174, 189, 203, 226, 236, 229, 209, 194],
  [174, 189, 203, 216, 237, 231, 222, 194],
  [174, 189, 203, 226, 243, 238, 222, 194],
  [174, 189, 215, 225, 235, 220, 209, 194],
  [174, 189, 215, 234, 241, 229, 209, 194],
  [174, 189, 215, 225, 242, 231, 222, 194],
  [174, 189, 215, 234, 246, 238, 222, 194],
  [176, 204, 216, 226, 243, 238, 211, 196],
  [176, 204, 216, 226, 247, 244, 211, 196]
]
def cycle (r : Fin 2685) := cycles[r.val - 128]!
theorem checked : ∀ r : Fin 2685,
    128 ≤ r.val → r.val < 160 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 128 ≤ r.val) (hhi : r.val < 160) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00128
