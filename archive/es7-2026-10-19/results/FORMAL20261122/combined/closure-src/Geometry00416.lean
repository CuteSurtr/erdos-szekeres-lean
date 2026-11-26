import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00416
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [32, 42, 55, 90, 112, 138, 102, 84, 66],
  [32, 42, 55, 108, 130, 156, 102, 84, 66],
  [32, 42, 55, 90, 133, 159, 123, 104, 66],
  [32, 42, 55, 108, 151, 175, 123, 104, 66],
  [32, 54, 70, 107, 129, 112, 78, 62, 47],
  [32, 54, 70, 127, 148, 130, 78, 62, 47],
  [32, 54, 70, 107, 150, 133, 97, 80, 47],
  [32, 54, 70, 127, 168, 151, 97, 80, 47],
  [32, 54, 70, 107, 129, 155, 138, 102, 84, 66],
  [32, 54, 70, 127, 148, 172, 156, 102, 84, 66],
  [32, 54, 70, 107, 150, 174, 159, 123, 104, 66],
  [32, 54, 70, 127, 168, 190, 175, 123, 104, 66],
  [33, 43, 57, 73, 115, 141, 123, 85, 67],
  [33, 43, 57, 73, 134, 160, 142, 85, 67],
  [33, 43, 72, 90, 133, 159, 123, 85, 67],
  [33, 43, 72, 90, 153, 177, 142, 85, 67],
  [33, 56, 71, 89, 132, 115, 97, 63, 48],
  [33, 56, 71, 89, 152, 134, 116, 63, 48],
  [33, 56, 88, 107, 150, 133, 97, 63, 48],
  [33, 56, 88, 107, 169, 153, 116, 63, 48],
  [33, 56, 71, 89, 132, 158, 141, 123, 85, 67],
  [33, 56, 71, 89, 152, 176, 160, 142, 85, 67],
  [33, 56, 88, 107, 150, 174, 159, 123, 85, 67],
  [33, 56, 88, 107, 169, 191, 177, 142, 85, 67],
  [34, 45, 74, 92, 113, 139, 122, 103, 50],
  [34, 45, 91, 110, 131, 157, 140, 122, 103, 50],
  [34, 45, 91, 110, 131, 178, 162, 144, 124, 50],
  [34, 45, 109, 128, 149, 173, 140, 122, 103, 50],
  [34, 45, 109, 128, 149, 193, 162, 144, 124, 50],
  [35, 46, 60, 77, 96, 144, 125, 105, 51],
  [35, 46, 60, 94, 115, 163, 145, 105, 51],
  [35, 46, 75, 93, 114, 140, 104, 85, 51]
]
def cycle (r : Fin 2685) := cycles[r.val - 416]!
theorem checked : ∀ r : Fin 2685,
    416 ≤ r.val → r.val < 448 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 416 ≤ r.val) (hhi : r.val < 448) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00416
