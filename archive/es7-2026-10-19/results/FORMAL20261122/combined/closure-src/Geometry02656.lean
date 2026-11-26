import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02656
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [186, 200, 214, 247, 244, 231, 220, 205],
  [187, 201, 214, 224, 233, 248, 232, 221, 206],
  [187, 201, 214, 224, 249, 239, 232, 221, 206],
  [187, 201, 214, 224, 246, 232, 221, 206],
  [187, 201, 214, 224, 233, 245, 221, 206],
  [187, 201, 214, 247, 239, 232, 221, 206],
  [192, 205, 216, 225, 234, 241, 221, 210],
  [192, 205, 216, 225, 240, 245, 221, 210],
  [192, 205, 216, 226, 243, 232, 223, 210],
  [192, 205, 216, 226, 247, 239, 223, 210],
  [195, 208, 218, 227, 245, 248, 232, 223],
  [197, 209, 219, 228, 236, 243, 232, 212],
  [197, 209, 219, 235, 241, 246, 232, 212],
  [200, 213, 224, 246, 243, 237, 228, 216],
  [200, 213, 224, 249, 247, 237, 228, 216],
  [200, 213, 233, 248, 243, 237, 228, 216],
  [200, 213, 233, 250, 247, 237, 228, 216],
  [201, 214, 224, 233, 248, 238, 229, 217],
  [201, 214, 224, 249, 244, 238, 229, 217],
  [206, 217, 226, 234, 249, 239, 232, 221],
  [206, 217, 226, 234, 240, 248, 232, 221],
  [210, 220, 228, 235, 241, 246, 232, 223],
  [210, 220, 228, 235, 245, 248, 232, 223],
  [210, 220, 228, 235, 241, 249, 239, 223],
  [210, 220, 228, 235, 245, 250, 239, 223],
  [214, 224, 233, 250, 247, 243, 236, 226],
  [214, 224, 233, 251, 247, 243, 236, 226],
  [221, 229, 236, 241, 245, 250, 239, 232],
  [221, 229, 236, 241, 245, 251, 239, 232]
]
def cycle (r : Fin 2685) := cycles[r.val - 2656]!
theorem checked : ∀ r : Fin 2685,
    2656 ≤ r.val → r.val < 2685 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2656 ≤ r.val) (hhi : r.val < 2685) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02656
