import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01472
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [35, 46, 75, 112, 138, 102, 67, 51],
  [35, 59, 74, 92, 118, 101, 84, 67, 51],
  [35, 59, 74, 111, 137, 120, 102, 67, 51],
  [35, 59, 91, 110, 136, 119, 84, 67, 51],
  [35, 59, 91, 129, 155, 138, 102, 67, 51],
  [35, 59, 74, 92, 113, 139, 122, 104, 85, 51],
  [35, 59, 74, 152, 176, 160, 142, 51],
  [35, 59, 74, 152, 196, 181, 164, 51],
  [35, 59, 76, 95, 121, 103, 85, 51],
  [35, 59, 76, 95, 143, 124, 105, 51],
  [35, 59, 148, 168, 190, 175, 85, 51],
  [35, 59, 91, 169, 191, 177, 142, 51],
  [35, 59, 91, 169, 209, 197, 164, 51],
  [35, 59, 148, 168, 208, 195, 105, 51],
  [35, 109, 128, 149, 173, 104, 85, 51],
  [35, 109, 147, 167, 189, 123, 85, 51],
  [35, 109, 128, 149, 193, 125, 105, 51],
  [35, 109, 147, 167, 207, 145, 105, 51],
  [35, 59, 74, 92, 113, 96, 80, 63],
  [35, 59, 74, 111, 132, 115, 97, 63],
  [35, 59, 91, 110, 131, 114, 80, 63],
  [35, 59, 91, 129, 150, 133, 97, 63],
  [36, 48, 62, 78, 97, 123, 68, 52],
  [36, 48, 62, 78, 116, 142, 68, 52],
  [36, 48, 62, 78, 97, 145, 86, 52],
  [36, 48, 62, 78, 116, 164, 86, 52],
  [36, 76, 92, 111, 132, 115, 97, 49],
  [36, 76, 92, 111, 152, 134, 116, 49],
  [36, 61, 77, 96, 122, 104, 68, 52],
  [36, 61, 77, 96, 144, 125, 86, 52],
  [36, 76, 95, 121, 103, 85, 68, 52],
  [36, 76, 92, 113, 139, 122, 104, 68, 52]
]
def cycle (r : Fin 2685) := cycles[r.val - 1472]!
theorem checked : ∀ r : Fin 2685,
    1472 ≤ r.val → r.val < 1504 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1472 ≤ r.val) (hhi : r.val < 1504) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01472
