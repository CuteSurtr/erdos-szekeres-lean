import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01408
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [32, 42, 55, 72, 114, 140, 104, 66],
  [32, 42, 73, 94, 120, 102, 84, 66],
  [32, 42, 73, 115, 141, 123, 104, 66],
  [32, 54, 70, 88, 110, 93, 62, 47],
  [32, 54, 89, 111, 94, 78, 62, 47],
  [32, 54, 70, 88, 131, 114, 80, 47],
  [32, 54, 89, 132, 115, 97, 80, 47],
  [32, 54, 70, 88, 110, 136, 119, 84, 66],
  [32, 54, 70, 88, 131, 157, 140, 104, 66],
  [32, 54, 70, 169, 191, 177, 142, 66],
  [32, 54, 70, 186, 205, 192, 142, 66],
  [32, 54, 71, 92, 118, 101, 84, 66],
  [32, 54, 71, 113, 139, 122, 104, 66],
  [32, 54, 89, 111, 137, 120, 102, 84, 66],
  [32, 54, 89, 132, 158, 141, 123, 104, 66],
  [32, 54, 70, 107, 194, 180, 145, 125],
  [32, 54, 70, 127, 208, 195, 145, 125],
  [32, 87, 126, 147, 171, 102, 84, 66],
  [32, 87, 146, 166, 188, 102, 84, 66],
  [32, 87, 126, 167, 189, 123, 104, 66],
  [32, 87, 146, 184, 203, 123, 104, 66],
  [33, 43, 57, 73, 94, 120, 102, 67],
  [33, 43, 57, 96, 122, 104, 85, 67],
  [33, 43, 72, 114, 140, 104, 85, 67],
  [33, 43, 72, 90, 112, 138, 102, 67],
  [33, 56, 71, 113, 96, 80, 63, 48],
  [33, 56, 88, 131, 114, 80, 63, 48],
  [33, 56, 71, 89, 111, 94, 78, 48],
  [33, 56, 88, 107, 129, 112, 78, 48],
  [33, 56, 71, 92, 118, 101, 84, 67],
  [33, 56, 71, 113, 139, 122, 104, 85, 67],
  [33, 56, 71, 89, 111, 137, 120, 102, 67]
]
def cycle (r : Fin 2685) := cycles[r.val - 1408]!
theorem checked : ∀ r : Fin 2685,
    1408 ≤ r.val → r.val < 1440 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1408 ≤ r.val) (hhi : r.val < 1440) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01408
