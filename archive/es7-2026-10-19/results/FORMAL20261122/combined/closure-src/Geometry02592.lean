import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02592
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [153, 169, 186, 201, 229, 221, 197, 177],
  [153, 169, 186, 231, 223, 212, 197, 177],
  [156, 172, 188, 202, 234, 206, 192, 175],
  [156, 172, 188, 202, 240, 206, 192, 175],
  [156, 172, 188, 202, 225, 235, 210, 195],
  [156, 172, 188, 226, 236, 221, 210, 195],
  [159, 174, 190, 205, 220, 210, 197, 180],
  [159, 174, 190, 217, 229, 221, 197, 180],
  [159, 174, 190, 205, 231, 223, 212, 180],
  [159, 174, 190, 217, 238, 232, 212, 180],
  [160, 176, 191, 205, 231, 223, 198, 181],
  [160, 176, 191, 205, 217, 229, 221, 181],
  [160, 176, 204, 216, 237, 223, 198, 181],
  [160, 176, 204, 216, 226, 236, 221, 181],
  [163, 179, 194, 208, 220, 231, 223, 198],
  [163, 179, 194, 208, 229, 238, 232, 198],
  [164, 196, 209, 220, 229, 238, 232, 182],
  [164, 196, 209, 220, 229, 244, 239, 182],
  [166, 183, 224, 234, 226, 216, 203, 188],
  [166, 183, 233, 240, 226, 216, 203, 188],
  [167, 199, 213, 242, 237, 230, 207, 189],
  [168, 184, 199, 224, 234, 217, 205, 190],
  [168, 184, 199, 233, 240, 217, 205, 190],
  [168, 184, 199, 213, 235, 220, 208, 190],
  [168, 184, 199, 213, 242, 231, 208, 190],
  [168, 184, 214, 236, 229, 220, 208, 190],
  [168, 184, 214, 243, 238, 231, 208, 190],
  [169, 185, 200, 214, 236, 229, 209, 191],
  [169, 185, 200, 237, 231, 222, 209, 191],
  [169, 185, 213, 242, 231, 222, 209, 191],
  [169, 185, 213, 224, 241, 229, 209, 191],
  [170, 186, 200, 213, 224, 234, 206, 192]
]
def cycle (r : Fin 2685) := cycles[r.val - 2592]!
theorem checked : ∀ r : Fin 2685,
    2592 ≤ r.val → r.val < 2624 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2592 ≤ r.val) (hhi : r.val < 2624) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02592
