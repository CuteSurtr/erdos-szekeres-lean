import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00960
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [148, 166, 183, 233, 245, 229, 220, 208, 172],
  [150, 167, 184, 200, 228, 220, 209, 194, 174],
  [150, 167, 184, 200, 237, 231, 222, 194, 174],
  [150, 167, 184, 214, 236, 229, 209, 194, 174],
  [150, 167, 184, 214, 243, 238, 222, 194, 174],
  [150, 167, 199, 213, 235, 220, 209, 194, 174],
  [150, 167, 199, 224, 241, 229, 209, 194, 174],
  [150, 167, 199, 213, 242, 231, 222, 194, 174],
  [150, 167, 199, 224, 246, 238, 222, 194, 174],
  [151, 168, 184, 199, 224, 241, 221, 210, 195, 175],
  [151, 168, 184, 199, 233, 245, 221, 210, 195, 175],
  [151, 168, 184, 199, 224, 246, 232, 223, 195, 175],
  [151, 168, 184, 199, 233, 248, 232, 223, 195, 175],
  [152, 185, 200, 214, 243, 238, 211, 196, 176],
  [152, 185, 200, 214, 247, 244, 211, 196, 176],
  [153, 169, 185, 200, 214, 243, 232, 212, 197, 177],
  [153, 169, 185, 200, 214, 247, 239, 212, 197, 177],
  [153, 169, 185, 213, 224, 246, 232, 212, 197, 177],
  [153, 169, 185, 213, 224, 249, 239, 212, 197, 177],
  [153, 169, 186, 201, 244, 239, 212, 197, 177],
  [156, 172, 188, 202, 234, 241, 221, 210, 195],
  [156, 172, 188, 202, 240, 245, 221, 210, 195],
  [159, 174, 189, 203, 216, 228, 210, 197, 180],
  [159, 174, 189, 203, 226, 236, 221, 197, 180],
  [159, 174, 189, 215, 225, 235, 210, 197, 180],
  [159, 174, 189, 215, 234, 241, 221, 197, 180],
  [159, 174, 189, 203, 216, 237, 223, 212, 180],
  [159, 174, 189, 203, 226, 243, 232, 212, 180],
  [159, 174, 189, 215, 225, 242, 223, 212, 180],
  [159, 174, 189, 215, 234, 246, 232, 212, 180],
  [160, 176, 191, 205, 217, 238, 232, 198, 181],
  [160, 176, 191, 205, 217, 244, 239, 198, 181]
]
def cycle (r : Fin 2685) := cycles[r.val - 960]!
theorem checked : ∀ r : Fin 2685,
    960 ≤ r.val → r.val < 992 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 960 ≤ r.val) (hhi : r.val < 992) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00960
