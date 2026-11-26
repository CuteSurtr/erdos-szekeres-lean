import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01984
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [74, 109, 147, 171, 155, 137, 118, 98],
  [74, 109, 166, 188, 172, 137, 118, 98],
  [74, 109, 128, 149, 173, 157, 139, 98],
  [74, 109, 128, 149, 193, 178, 161, 98],
  [75, 91, 109, 147, 171, 138, 119, 99],
  [75, 91, 109, 166, 188, 156, 138, 119, 99],
  [75, 91, 109, 183, 202, 156, 138, 119, 99],
  [75, 91, 109, 128, 149, 173, 140, 99],
  [75, 91, 109, 128, 149, 193, 162, 99],
  [75, 91, 109, 147, 167, 189, 159, 140, 99],
  [75, 91, 109, 200, 216, 192, 177, 99],
  [75, 91, 109, 213, 225, 192, 177, 99],
  [75, 91, 109, 200, 228, 210, 197, 99],
  [75, 91, 109, 213, 235, 210, 197, 99],
  [75, 91, 148, 172, 156, 138, 119, 99],
  [75, 91, 129, 150, 174, 159, 140, 99],
  [75, 91, 129, 150, 194, 180, 162, 99],
  [75, 91, 148, 168, 190, 175, 159, 140, 99],
  [75, 91, 148, 168, 208, 195, 180, 162, 99],
  [75, 91, 109, 166, 184, 151, 133, 114],
  [75, 91, 109, 183, 199, 151, 133, 114],
  [76, 110, 129, 150, 174, 158, 121, 100],
  [76, 110, 129, 169, 191, 176, 121, 100],
  [76, 110, 129, 150, 194, 179, 143, 100],
  [76, 110, 129, 169, 209, 196, 143, 100],
  [76, 128, 149, 173, 157, 139, 121, 100],
  [76, 128, 149, 193, 178, 161, 143, 100],
  [77, 92, 110, 129, 150, 133, 115, 96],
  [77, 92, 110, 148, 168, 151, 115, 96],
  [77, 92, 110, 129, 169, 153, 134, 96],
  [77, 92, 110, 148, 186, 170, 134, 96],
  [77, 92, 128, 147, 167, 133, 115, 96]
]
def cycle (r : Fin 2685) := cycles[r.val - 1984]!
theorem checked : ∀ r : Fin 2685,
    1984 ≤ r.val → r.val < 2016 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1984 ≤ r.val) (hhi : r.val < 2016) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01984
