import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01888
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [63, 95, 131, 150, 194, 180, 145, 105, 85],
  [63, 95, 168, 186, 220, 210, 105, 85],
  [63, 95, 168, 186, 231, 223, 105, 85],
  [63, 95, 113, 132, 158, 141, 123, 85],
  [63, 95, 131, 150, 174, 159, 123, 85],
  [63, 95, 131, 150, 169, 191, 177, 142, 85],
  [63, 149, 167, 185, 219, 164, 105, 85],
  [63, 149, 167, 185, 230, 182, 105, 85],
  [65, 81, 98, 118, 139, 161, 144, 124],
  [65, 81, 98, 137, 158, 179, 163, 124],
  [65, 81, 117, 136, 157, 140, 122, 103],
  [65, 81, 117, 155, 174, 159, 141, 103],
  [65, 81, 135, 154, 173, 140, 122, 103],
  [65, 81, 135, 171, 189, 159, 141, 103],
  [66, 82, 99, 138, 159, 180, 145, 125],
  [66, 82, 99, 156, 175, 195, 145, 125],
  [66, 98, 117, 155, 174, 159, 123, 104],
  [66, 98, 117, 172, 190, 175, 123, 104],
  [66, 98, 117, 136, 157, 178, 162, 125],
  [66, 98, 137, 158, 179, 163, 145, 125],
  [67, 83, 101, 120, 141, 163, 145, 105],
  [67, 83, 101, 120, 160, 181, 164, 105],
  [67, 83, 119, 138, 159, 180, 145, 105],
  [67, 83, 119, 138, 177, 197, 164, 105],
  [67, 100, 118, 137, 158, 141, 123, 85],
  [67, 100, 118, 137, 176, 160, 142, 85],
  [67, 100, 136, 155, 174, 159, 123, 85],
  [67, 100, 136, 155, 191, 177, 142, 85],
  [67, 100, 118, 139, 161, 144, 125, 105],
  [67, 100, 136, 157, 178, 162, 125, 105],
  [68, 103, 122, 141, 160, 181, 164, 86],
  [68, 103, 122, 141, 160, 198, 182, 86]
]
def cycle (r : Fin 2685) := cycles[r.val - 1888]!
theorem checked : ∀ r : Fin 2685,
    1888 ≤ r.val → r.val < 1920 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1888 ≤ r.val) (hhi : r.val < 1920) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01888
