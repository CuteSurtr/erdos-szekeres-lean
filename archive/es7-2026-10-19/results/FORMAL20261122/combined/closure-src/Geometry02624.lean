import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02624
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [170, 186, 200, 213, 233, 240, 206, 192],
  [170, 186, 200, 213, 224, 241, 221, 210, 192],
  [170, 186, 200, 213, 233, 245, 221, 210, 192],
  [170, 186, 200, 213, 242, 223, 210, 192],
  [170, 186, 200, 213, 251, 223, 210, 192],
  [170, 186, 200, 214, 236, 221, 210, 192],
  [170, 186, 200, 214, 243, 232, 223, 210, 192],
  [170, 186, 200, 214, 247, 239, 223, 210, 192],
  [170, 186, 201, 238, 232, 223, 210, 192],
  [170, 186, 201, 244, 239, 223, 210, 192],
  [175, 190, 203, 215, 225, 235, 210, 195],
  [175, 190, 203, 226, 236, 221, 210, 195],
  [175, 190, 203, 215, 225, 242, 223, 195],
  [175, 190, 203, 226, 243, 232, 223, 195],
  [177, 191, 204, 216, 237, 223, 212, 197],
  [177, 191, 204, 225, 242, 223, 212, 197],
  [177, 191, 204, 216, 226, 236, 221, 197],
  [177, 191, 204, 225, 234, 241, 221, 197],
  [177, 191, 205, 217, 238, 232, 212, 197],
  [177, 191, 205, 217, 244, 239, 212, 197],
  [180, 194, 207, 218, 228, 237, 223, 212],
  [180, 194, 207, 218, 236, 243, 232, 212],
  [180, 194, 207, 227, 235, 242, 223, 212],
  [180, 194, 207, 227, 241, 246, 232, 212],
  [181, 196, 209, 220, 229, 238, 232, 198],
  [181, 196, 209, 220, 229, 244, 239, 198],
  [181, 196, 219, 228, 236, 243, 232, 198],
  [184, 199, 224, 246, 243, 237, 218, 203],
  [184, 199, 233, 248, 243, 237, 218, 203],
  [186, 200, 213, 224, 241, 229, 220, 205],
  [186, 200, 213, 233, 245, 229, 220, 205],
  [186, 200, 214, 243, 238, 231, 220, 205]
]
def cycle (r : Fin 2685) := cycles[r.val - 2624]!
theorem checked : ∀ r : Fin 2685,
    2624 ≤ r.val → r.val < 2656 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2624 ≤ r.val) (hhi : r.val < 2656) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02624
