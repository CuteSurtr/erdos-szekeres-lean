import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01696
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [49, 79, 96, 115, 134, 160, 142, 68],
  [49, 95, 113, 161, 144, 125, 86, 68],
  [49, 95, 113, 132, 179, 163, 145, 86, 68],
  [49, 131, 150, 169, 209, 197, 86, 68],
  [49, 131, 150, 169, 222, 212, 86, 68],
  [49, 95, 113, 132, 158, 141, 123, 68],
  [50, 64, 98, 118, 139, 161, 144, 124],
  [50, 64, 117, 136, 157, 140, 122, 103],
  [50, 64, 135, 154, 173, 140, 122, 103],
  [51, 65, 82, 101, 122, 144, 125, 105],
  [51, 65, 82, 120, 141, 163, 145, 105],
  [51, 65, 99, 119, 140, 162, 125, 105],
  [51, 65, 99, 138, 159, 180, 145, 105],
  [51, 81, 98, 118, 139, 122, 104, 85],
  [51, 81, 98, 137, 158, 141, 123, 85],
  [51, 81, 117, 136, 157, 140, 104, 85],
  [51, 81, 117, 155, 174, 159, 123, 85],
  [52, 100, 118, 137, 158, 141, 123, 68],
  [52, 100, 118, 137, 176, 160, 142, 68],
  [52, 83, 101, 120, 141, 163, 145, 86],
  [52, 83, 101, 120, 160, 181, 164, 86],
  [52, 100, 118, 139, 161, 144, 125, 86],
  [53, 69, 146, 166, 148, 129, 110, 91],
  [53, 69, 165, 183, 148, 129, 110, 91],
  [53, 69, 126, 147, 171, 155, 136, 117],
  [54, 70, 107, 129, 155, 137, 118, 98],
  [54, 70, 107, 150, 174, 158, 139, 98],
  [54, 70, 127, 148, 172, 137, 118, 98],
  [54, 70, 127, 168, 190, 158, 139, 98],
  [54, 87, 126, 147, 129, 111, 92, 74],
  [54, 87, 146, 166, 148, 111, 92, 74],
  [54, 87, 126, 167, 150, 132, 113, 74]
]
def cycle (r : Fin 2685) := cycles[r.val - 1696]!
theorem checked : ∀ r : Fin 2685,
    1696 ≤ r.val → r.val < 1728 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1696 ≤ r.val) (hhi : r.val < 1728) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01696
