import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00992
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [160, 176, 204, 216, 226, 243, 232, 198, 181],
  [160, 176, 204, 216, 226, 247, 239, 198, 181],
  [168, 184, 199, 224, 241, 229, 220, 208, 190],
  [168, 184, 199, 233, 245, 229, 220, 208, 190],
  [168, 184, 199, 224, 246, 238, 231, 208, 190],
  [168, 184, 199, 233, 248, 238, 231, 208, 190],
  [169, 185, 200, 214, 243, 238, 222, 209, 191],
  [169, 185, 200, 214, 247, 244, 222, 209, 191],
  [169, 185, 213, 224, 246, 238, 222, 209, 191],
  [169, 185, 213, 224, 249, 244, 222, 209, 191],
  [170, 186, 200, 213, 224, 246, 232, 223, 210, 192],
  [170, 186, 200, 213, 224, 249, 239, 223, 210, 192],
  [170, 186, 200, 213, 233, 248, 232, 223, 210, 192],
  [170, 186, 200, 213, 233, 250, 239, 223, 210, 192],
  [175, 190, 203, 215, 234, 241, 221, 210, 195],
  [175, 190, 203, 215, 240, 245, 221, 210, 195],
  [175, 190, 203, 215, 234, 246, 232, 223, 195],
  [175, 190, 203, 215, 240, 248, 232, 223, 195],
  [177, 191, 204, 216, 226, 243, 232, 212, 197],
  [177, 191, 204, 216, 226, 247, 239, 212, 197],
  [177, 191, 204, 225, 234, 246, 232, 212, 197],
  [177, 191, 204, 225, 234, 249, 239, 212, 197],
  [186, 200, 213, 224, 246, 238, 231, 220, 205],
  [186, 200, 213, 224, 249, 244, 231, 220, 205],
  [186, 200, 213, 233, 248, 238, 231, 220, 205],
  [186, 200, 213, 233, 250, 244, 231, 220, 205],
  [187, 201, 214, 224, 233, 250, 239, 232, 221, 206],
  [187, 201, 214, 224, 233, 251, 239, 232, 221, 206],
  [192, 205, 216, 225, 234, 246, 232, 223, 210],
  [192, 205, 216, 225, 240, 248, 232, 223, 210],
  [192, 205, 216, 225, 234, 249, 239, 223, 210],
  [192, 205, 216, 225, 240, 250, 239, 223, 210]
]
def cycle (r : Fin 2685) := cycles[r.val - 992]!
theorem checked : ∀ r : Fin 2685,
    992 ≤ r.val → r.val < 1024 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 992 ≤ r.val) (hhi : r.val < 1024) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00992
