import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02304
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [104, 139, 157, 174, 194, 180, 145, 125],
  [104, 139, 157, 190, 208, 195, 145, 125],
  [104, 139, 157, 190, 205, 220, 210, 164, 125],
  [104, 139, 158, 176, 196, 181, 164, 125],
  [104, 139, 158, 176, 211, 198, 182, 125],
  [105, 143, 161, 179, 196, 211, 198, 182],
  [105, 143, 178, 194, 209, 222, 212, 182],
  [106, 165, 199, 215, 203, 189, 173, 154],
  [106, 165, 213, 225, 216, 204, 173, 154],
  [107, 126, 146, 200, 186, 169, 150, 129],
  [107, 126, 146, 214, 201, 169, 150, 129],
  [107, 126, 165, 213, 186, 169, 150, 129],
  [107, 126, 165, 224, 201, 169, 150, 129],
  [107, 126, 146, 184, 203, 190, 174, 155],
  [107, 126, 165, 199, 215, 190, 174, 155],
  [108, 127, 146, 165, 213, 170, 151, 130],
  [108, 127, 146, 214, 187, 170, 151, 130],
  [108, 127, 146, 165, 213, 225, 192, 175, 156],
  [108, 127, 146, 165, 199, 215, 175, 156],
  [108, 127, 146, 200, 216, 192, 175, 156],
  [108, 127, 146, 214, 226, 206, 192, 175, 156],
  [108, 127, 146, 165, 241, 221, 210, 195],
  [108, 127, 146, 165, 245, 221, 210, 195],
  [108, 127, 201, 217, 206, 192, 175, 156],
  [109, 183, 199, 215, 203, 189, 173, 135],
  [110, 128, 147, 167, 189, 174, 157, 136],
  [110, 128, 147, 185, 204, 191, 157, 136],
  [110, 128, 147, 167, 207, 194, 178, 136],
  [110, 128, 147, 185, 219, 209, 178, 136],
  [111, 129, 148, 186, 205, 176, 158, 137],
  [111, 129, 148, 201, 217, 176, 158, 137],
  [111, 129, 148, 186, 220, 196, 179, 137]
]
def cycle (r : Fin 2685) := cycles[r.val - 2304]!
theorem checked : ∀ r : Fin 2685,
    2304 ≤ r.val → r.val < 2336 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2304 ≤ r.val) (hhi : r.val < 2336) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02304
