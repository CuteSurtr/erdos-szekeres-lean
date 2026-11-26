import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00640
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [62, 92, 110, 129, 169, 191, 177, 142, 104, 84],
  [62, 92, 110, 148, 186, 205, 192, 142, 104, 84],
  [62, 92, 110, 129, 150, 194, 180, 145, 125, 84],
  [62, 92, 110, 129, 169, 209, 197, 164, 125, 84],
  [62, 92, 110, 148, 168, 208, 195, 145, 125, 84],
  [62, 92, 110, 148, 186, 220, 210, 164, 125, 84],
  [63, 79, 96, 115, 134, 181, 164, 105, 85],
  [63, 79, 96, 115, 134, 198, 182, 105, 85],
  [63, 79, 114, 133, 153, 197, 164, 105, 85],
  [63, 79, 114, 133, 153, 212, 182, 105, 85],
  [63, 95, 113, 132, 152, 196, 181, 164, 105, 85],
  [63, 95, 113, 132, 152, 211, 198, 182, 105, 85],
  [63, 95, 131, 150, 169, 209, 197, 164, 105, 85],
  [63, 95, 131, 150, 169, 222, 212, 182, 105, 85],
  [63, 95, 113, 132, 152, 176, 160, 142, 85],
  [65, 81, 117, 136, 157, 178, 162, 144, 124],
  [65, 81, 117, 155, 174, 194, 180, 163, 124],
  [65, 81, 135, 154, 173, 193, 162, 144, 124],
  [65, 81, 135, 171, 189, 207, 180, 163, 124],
  [66, 98, 117, 155, 174, 194, 180, 145, 125],
  [66, 98, 117, 172, 190, 208, 195, 145, 125],
  [67, 100, 118, 137, 158, 179, 163, 145, 105],
  [67, 100, 118, 137, 176, 196, 181, 164, 105],
  [67, 100, 136, 155, 174, 194, 180, 145, 105],
  [67, 100, 136, 155, 191, 209, 197, 164, 105],
  [68, 121, 139, 158, 176, 196, 181, 164, 86],
  [68, 121, 139, 158, 176, 211, 198, 182, 86],
  [70, 87, 146, 166, 188, 172, 155, 136, 117],
  [70, 87, 165, 183, 202, 172, 155, 136, 117],
  [70, 87, 146, 184, 203, 190, 174, 157, 117],
  [70, 87, 165, 199, 215, 190, 174, 157, 117],
  [71, 106, 126, 167, 189, 174, 158, 139, 118]
]
def cycle (r : Fin 2685) := cycles[r.val - 640]!
theorem checked : ∀ r : Fin 2685,
    640 ≤ r.val → r.val < 672 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 640 ≤ r.val) (hhi : r.val < 672) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00640
