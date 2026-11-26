import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01824
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [60, 75, 130, 151, 195, 163, 144, 82],
  [61, 76, 110, 129, 150, 133, 115, 79],
  [61, 76, 110, 129, 169, 153, 134, 79],
  [61, 76, 128, 147, 167, 133, 115, 79],
  [61, 76, 128, 147, 185, 153, 134, 79],
  [61, 76, 92, 111, 152, 176, 160, 103, 83],
  [61, 76, 92, 113, 139, 122, 103, 83],
  [61, 76, 92, 111, 152, 196, 181, 124, 83],
  [61, 76, 92, 113, 161, 144, 124, 83],
  [61, 76, 110, 131, 157, 140, 122, 103, 83],
  [61, 76, 128, 149, 173, 140, 122, 103, 83],
  [61, 76, 148, 168, 190, 175, 103, 83],
  [61, 76, 148, 186, 205, 192, 103, 83],
  [61, 76, 166, 184, 203, 175, 103, 83],
  [61, 76, 166, 200, 216, 192, 103, 83],
  [61, 76, 110, 129, 155, 138, 120, 83],
  [61, 76, 110, 131, 178, 162, 144, 124, 83],
  [61, 76, 110, 129, 222, 212, 198, 83],
  [61, 76, 128, 147, 171, 138, 120, 83],
  [61, 76, 128, 149, 193, 162, 144, 124, 83],
  [61, 76, 148, 168, 208, 195, 124, 83],
  [61, 76, 148, 186, 220, 210, 124, 83],
  [61, 76, 166, 184, 218, 195, 124, 83],
  [61, 76, 166, 200, 228, 210, 124, 83],
  [61, 76, 128, 147, 230, 212, 198, 83],
  [61, 93, 112, 133, 159, 141, 103, 83],
  [61, 93, 112, 153, 177, 160, 103, 83],
  [61, 93, 112, 133, 180, 163, 124, 83],
  [61, 93, 112, 153, 197, 181, 124, 83],
  [62, 77, 94, 115, 141, 123, 104, 84],
  [62, 77, 94, 134, 160, 142, 104, 84],
  [62, 77, 94, 115, 163, 145, 125, 84]
]
def cycle (r : Fin 2685) := cycles[r.val - 1824]!
theorem checked : ∀ r : Fin 2685,
    1824 ≤ r.val → r.val < 1856 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1824 ≤ r.val) (hhi : r.val < 1856) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01824
