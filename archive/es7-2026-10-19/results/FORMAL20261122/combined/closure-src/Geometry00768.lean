import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00768
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [90, 107, 126, 146, 214, 226, 206, 177, 159, 138],
  [90, 107, 126, 165, 213, 225, 192, 177, 159, 138],
  [90, 107, 126, 165, 224, 234, 206, 177, 159, 138],
  [90, 107, 127, 201, 217, 206, 177, 159, 138],
  [91, 109, 166, 184, 203, 190, 174, 157, 117],
  [91, 109, 183, 199, 215, 190, 174, 157, 117],
  [91, 109, 166, 184, 218, 208, 194, 178, 117],
  [91, 109, 183, 199, 227, 208, 194, 178, 117],
  [92, 128, 147, 167, 189, 174, 158, 139, 118],
  [92, 128, 147, 185, 204, 191, 176, 139, 118],
  [92, 128, 166, 184, 203, 190, 158, 139, 118],
  [92, 128, 166, 200, 216, 205, 176, 139, 118],
  [92, 128, 147, 167, 207, 194, 179, 161, 118],
  [92, 128, 147, 185, 219, 209, 196, 161, 118],
  [92, 128, 166, 184, 218, 208, 179, 161, 118],
  [92, 128, 166, 200, 228, 220, 196, 161, 118],
  [93, 110, 128, 166, 184, 203, 175, 159, 140, 119],
  [93, 110, 128, 183, 199, 215, 175, 159, 140, 119],
  [93, 110, 128, 166, 200, 216, 192, 177, 140, 119],
  [93, 110, 128, 183, 213, 225, 192, 177, 140, 119],
  [93, 110, 128, 166, 184, 218, 195, 180, 162, 119],
  [93, 110, 128, 166, 200, 228, 210, 197, 162, 119],
  [93, 110, 128, 183, 199, 227, 195, 180, 162, 119],
  [93, 110, 128, 183, 213, 235, 210, 197, 162, 119],
  [94, 111, 129, 148, 186, 205, 192, 160, 141, 120],
  [94, 111, 129, 148, 201, 217, 206, 160, 141, 120],
  [94, 111, 129, 148, 186, 220, 210, 181, 163, 120],
  [94, 111, 129, 148, 201, 229, 221, 181, 163, 120],
  [94, 111, 147, 166, 200, 216, 192, 160, 141, 120],
  [94, 111, 147, 166, 214, 226, 206, 160, 141, 120],
  [94, 111, 147, 166, 200, 228, 210, 181, 163, 120],
  [94, 111, 147, 166, 214, 236, 221, 181, 163, 120]
]
def cycle (r : Fin 2685) := cycles[r.val - 768]!
theorem checked : ∀ r : Fin 2685,
    768 ≤ r.val → r.val < 800 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 768 ≤ r.val) (hhi : r.val < 800) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00768
