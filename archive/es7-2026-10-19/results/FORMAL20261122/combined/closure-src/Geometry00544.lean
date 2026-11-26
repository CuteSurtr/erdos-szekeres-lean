import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00544
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [48, 61, 93, 112, 153, 197, 164, 105, 67],
  [48, 76, 92, 111, 132, 158, 141, 123, 85, 67],
  [48, 76, 92, 111, 152, 176, 160, 142, 85, 67],
  [48, 76, 110, 129, 150, 174, 159, 123, 85, 67],
  [48, 76, 110, 129, 169, 191, 177, 142, 85, 67],
  [48, 76, 92, 111, 132, 179, 163, 145, 105, 67],
  [48, 76, 92, 111, 152, 196, 181, 164, 105, 67],
  [48, 76, 110, 129, 150, 194, 180, 145, 105, 67],
  [48, 76, 110, 129, 169, 209, 197, 164, 105, 67],
  [49, 79, 96, 115, 134, 181, 164, 86, 68],
  [49, 79, 96, 115, 134, 198, 182, 86, 68],
  [49, 95, 113, 132, 152, 196, 181, 164, 86, 68],
  [49, 95, 113, 132, 152, 211, 198, 182, 86, 68],
  [49, 95, 113, 132, 152, 176, 160, 142, 68],
  [50, 64, 117, 136, 157, 178, 162, 144, 124],
  [50, 64, 135, 154, 173, 193, 162, 144, 124],
  [51, 81, 98, 118, 139, 161, 144, 125, 105],
  [51, 81, 98, 137, 158, 179, 163, 145, 105],
  [51, 81, 117, 136, 157, 178, 162, 125, 105],
  [51, 81, 117, 155, 174, 194, 180, 145, 105],
  [52, 100, 118, 137, 158, 179, 163, 145, 86],
  [52, 100, 118, 137, 176, 196, 181, 164, 86],
  [53, 69, 146, 166, 188, 172, 155, 136, 117],
  [53, 69, 165, 183, 202, 172, 155, 136, 117],
  [54, 87, 126, 147, 171, 155, 137, 118, 98],
  [54, 87, 146, 166, 188, 172, 137, 118, 98],
  [54, 87, 126, 167, 189, 174, 158, 139, 98],
  [54, 87, 146, 184, 203, 190, 158, 139, 98],
  [55, 70, 87, 146, 166, 130, 112, 93, 75],
  [55, 70, 87, 165, 183, 130, 112, 93, 75],
  [55, 70, 87, 146, 184, 151, 133, 114, 75],
  [55, 70, 87, 165, 199, 151, 133, 114, 75]
]
def cycle (r : Fin 2685) := cycles[r.val - 544]!
theorem checked : ∀ r : Fin 2685,
    544 ≤ r.val → r.val < 576 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 544 ≤ r.val) (hhi : r.val < 576) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00544
