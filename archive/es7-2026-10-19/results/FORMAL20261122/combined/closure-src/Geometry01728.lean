import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01728
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [54, 87, 146, 184, 168, 132, 113, 74],
  [54, 87, 106, 128, 154, 136, 118, 98],
  [54, 87, 106, 149, 173, 157, 139, 98],
  [55, 70, 87, 126, 147, 112, 93, 75],
  [55, 70, 87, 126, 167, 133, 114, 75],
  [55, 70, 127, 148, 130, 112, 93, 75],
  [55, 70, 127, 168, 151, 133, 114, 75],
  [55, 70, 87, 106, 128, 154, 119, 99],
  [55, 70, 87, 106, 149, 173, 140, 99],
  [55, 70, 87, 126, 147, 171, 138, 119, 99],
  [55, 70, 87, 126, 167, 189, 159, 140, 99],
  [55, 70, 87, 200, 216, 192, 177, 99],
  [55, 70, 87, 213, 225, 192, 177, 99],
  [55, 70, 87, 146, 218, 195, 180, 162],
  [55, 70, 87, 165, 227, 195, 180, 162],
  [55, 70, 107, 129, 155, 138, 119, 99],
  [55, 70, 107, 150, 174, 159, 140, 99],
  [55, 70, 127, 148, 172, 156, 138, 119, 99],
  [55, 70, 127, 168, 190, 175, 159, 140, 99],
  [56, 106, 126, 167, 150, 132, 95, 76],
  [56, 106, 126, 185, 169, 152, 95, 76],
  [56, 88, 107, 150, 174, 158, 121, 100],
  [56, 88, 107, 169, 191, 176, 121, 100],
  [56, 106, 149, 173, 157, 139, 121, 100],
  [56, 106, 126, 147, 171, 155, 137, 100],
  [57, 71, 88, 107, 129, 112, 94, 77],
  [57, 71, 88, 127, 148, 130, 94, 77],
  [57, 71, 106, 126, 147, 112, 94, 77],
  [57, 71, 106, 146, 166, 130, 94, 77],
  [57, 71, 88, 107, 129, 155, 138, 120, 101],
  [57, 71, 88, 107, 150, 174, 159, 141, 122, 101],
  [57, 71, 88, 127, 148, 172, 156, 120, 101]
]
def cycle (r : Fin 2685) := cycles[r.val - 1728]!
theorem checked : ∀ r : Fin 2685,
    1728 ≤ r.val → r.val < 1760 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1728 ≤ r.val) (hhi : r.val < 1760) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01728
