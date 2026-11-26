import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00096
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [99, 117, 135, 171, 189, 207, 180, 162],
  [100, 154, 171, 189, 207, 194, 179, 143],
  [100, 154, 171, 204, 219, 209, 196, 143],
  [109, 183, 199, 227, 218, 207, 193, 135],
  [117, 135, 188, 203, 218, 208, 194, 178],
  [117, 135, 202, 215, 227, 208, 194, 178],
  [118, 154, 171, 189, 207, 194, 179, 161],
  [118, 154, 171, 204, 219, 209, 196, 161],
  [118, 154, 188, 203, 218, 208, 179, 161],
  [118, 154, 188, 216, 228, 220, 196, 161],
  [121, 173, 189, 204, 219, 209, 196, 143],
  [121, 173, 189, 204, 230, 222, 211, 143],
  [124, 143, 193, 207, 219, 230, 212, 198],
  [128, 183, 199, 227, 218, 207, 193, 154],
  [128, 183, 213, 235, 228, 219, 193, 154],
  [136, 154, 188, 203, 218, 208, 194, 178],
  [136, 154, 188, 216, 228, 220, 209, 178],
  [136, 154, 202, 215, 227, 208, 194, 178],
  [136, 154, 202, 225, 235, 220, 209, 178],
  [137, 171, 188, 216, 228, 220, 196, 179],
  [137, 171, 188, 226, 236, 229, 196, 179],
  [139, 173, 189, 204, 219, 209, 196, 161],
  [139, 173, 189, 204, 230, 222, 211, 161],
  [139, 173, 203, 216, 228, 220, 196, 161],
  [139, 173, 203, 216, 237, 231, 211, 161],
  [144, 161, 193, 207, 219, 230, 212, 198],
  [144, 161, 193, 218, 228, 237, 223, 198],
  [147, 183, 213, 235, 228, 219, 207, 171],
  [149, 199, 213, 235, 228, 219, 193, 173],
  [149, 199, 213, 242, 237, 230, 193, 173],
  [152, 169, 186, 201, 244, 211, 196, 176],
  [155, 171, 188, 216, 228, 220, 209, 194]
]
def cycle (r : Fin 2685) := cycles[r.val - 96]!
theorem checked : ∀ r : Fin 2685,
    96 ≤ r.val → r.val < 128 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 96 ≤ r.val) (hhi : r.val < 128) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00096
