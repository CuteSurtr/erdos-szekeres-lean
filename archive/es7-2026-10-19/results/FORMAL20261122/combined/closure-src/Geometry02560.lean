import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02560
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [150, 167, 184, 200, 216, 205, 191, 174],
  [150, 167, 184, 214, 226, 217, 191, 174],
  [150, 167, 199, 213, 225, 205, 191, 174],
  [150, 167, 199, 224, 234, 217, 191, 174],
  [151, 168, 184, 199, 224, 234, 206, 192, 175],
  [151, 168, 184, 199, 233, 240, 206, 192, 175],
  [151, 168, 184, 199, 213, 225, 192, 175],
  [151, 168, 184, 214, 226, 206, 192, 175],
  [151, 168, 184, 199, 213, 235, 210, 195, 175],
  [151, 168, 184, 199, 213, 242, 223, 195, 175],
  [151, 168, 184, 199, 249, 239, 195, 175],
  [151, 168, 184, 199, 250, 239, 195, 175],
  [151, 168, 184, 200, 228, 210, 195, 175],
  [151, 168, 184, 200, 237, 223, 195, 175],
  [151, 168, 184, 214, 236, 221, 210, 195, 175],
  [151, 168, 184, 214, 243, 232, 223, 195, 175],
  [151, 168, 201, 229, 221, 210, 195, 175],
  [151, 168, 201, 238, 232, 223, 195, 175],
  [152, 169, 186, 201, 238, 211, 196, 176],
  [152, 185, 200, 237, 231, 211, 196, 176],
  [152, 185, 200, 214, 236, 229, 196, 176],
  [153, 169, 185, 200, 228, 210, 197, 177],
  [153, 169, 185, 200, 237, 223, 212, 197, 177],
  [153, 169, 185, 200, 214, 236, 221, 197, 177],
  [153, 169, 185, 213, 235, 210, 197, 177],
  [153, 169, 185, 213, 242, 223, 212, 197, 177],
  [153, 169, 185, 233, 248, 212, 197, 177],
  [153, 169, 185, 233, 250, 212, 197, 177],
  [153, 169, 185, 213, 224, 241, 221, 197, 177],
  [153, 169, 185, 200, 214, 226, 206, 177],
  [153, 169, 185, 213, 224, 234, 206, 177],
  [153, 169, 186, 201, 238, 232, 212, 197, 177]
]
def cycle (r : Fin 2685) := cycles[r.val - 2560]!
theorem checked : ∀ r : Fin 2685,
    2560 ≤ r.val → r.val < 2592 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2560 ≤ r.val) (hhi : r.val < 2592) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02560
