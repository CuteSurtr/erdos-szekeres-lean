import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00672
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [71, 106, 126, 185, 204, 191, 176, 139, 118],
  [71, 106, 146, 184, 203, 190, 158, 139, 118],
  [71, 106, 146, 200, 216, 205, 176, 139, 118],
  [72, 88, 106, 146, 184, 151, 133, 114, 93],
  [72, 88, 106, 165, 199, 151, 133, 114, 93],
  [72, 88, 106, 146, 200, 170, 153, 114, 93],
  [72, 88, 106, 165, 213, 170, 153, 114, 93],
  [72, 88, 106, 146, 184, 203, 175, 159, 140, 119],
  [72, 88, 106, 146, 200, 216, 192, 177, 140, 119],
  [72, 88, 106, 165, 199, 215, 175, 159, 140, 119],
  [72, 88, 106, 165, 213, 225, 192, 177, 140, 119],
  [73, 89, 107, 127, 186, 170, 134, 115, 94],
  [73, 89, 107, 127, 201, 187, 134, 115, 94],
  [73, 89, 126, 146, 200, 170, 134, 115, 94],
  [73, 89, 126, 146, 214, 187, 134, 115, 94],
  [73, 89, 107, 127, 186, 205, 192, 160, 141, 120],
  [73, 89, 107, 127, 201, 217, 206, 160, 141, 120],
  [73, 89, 126, 146, 200, 216, 192, 160, 141, 120],
  [73, 89, 126, 146, 214, 226, 206, 160, 141, 120],
  [74, 109, 147, 167, 189, 174, 158, 139, 98],
  [74, 109, 166, 184, 203, 190, 158, 139, 98],
  [74, 109, 147, 167, 207, 194, 179, 161, 98],
  [74, 109, 166, 184, 218, 208, 179, 161, 98],
  [75, 91, 109, 166, 184, 203, 175, 159, 140, 99],
  [75, 91, 109, 183, 199, 215, 175, 159, 140, 99],
  [75, 91, 109, 147, 167, 207, 180, 162, 99],
  [75, 91, 109, 166, 184, 218, 195, 180, 162, 99],
  [75, 91, 109, 183, 199, 227, 195, 180, 162, 99],
  [76, 128, 147, 167, 189, 174, 158, 121, 100],
  [76, 128, 147, 185, 204, 191, 176, 121, 100],
  [76, 128, 147, 167, 207, 194, 179, 143, 100],
  [76, 128, 147, 185, 219, 209, 196, 143, 100]
]
def cycle (r : Fin 2685) := cycles[r.val - 672]!
theorem checked : ∀ r : Fin 2685,
    672 ≤ r.val → r.val < 704 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 672 ≤ r.val) (hhi : r.val < 704) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00672
