import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01664
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [47, 109, 166, 184, 203, 123, 104, 66],
  [47, 109, 147, 167, 207, 145, 125, 66],
  [47, 109, 166, 184, 218, 145, 125, 66],
  [47, 74, 91, 129, 150, 133, 97, 80],
  [47, 74, 91, 148, 168, 151, 97, 80],
  [48, 61, 77, 96, 122, 104, 85, 67],
  [48, 61, 77, 96, 144, 125, 105, 67],
  [48, 61, 93, 114, 140, 104, 85, 67],
  [48, 61, 93, 114, 162, 125, 105, 67],
  [48, 76, 92, 111, 132, 115, 97, 63],
  [48, 76, 92, 111, 152, 134, 116, 63],
  [48, 76, 110, 129, 150, 133, 97, 63],
  [48, 76, 110, 129, 169, 153, 116, 63],
  [48, 76, 92, 113, 139, 122, 104, 85, 67],
  [48, 76, 110, 131, 157, 140, 104, 85, 67],
  [48, 76, 148, 168, 190, 175, 85, 67],
  [48, 76, 148, 186, 205, 192, 85, 67],
  [48, 76, 92, 111, 137, 120, 102, 67],
  [48, 76, 92, 113, 161, 144, 125, 105, 67],
  [48, 76, 92, 111, 211, 198, 182, 67],
  [48, 76, 110, 129, 155, 138, 102, 67],
  [48, 76, 110, 131, 178, 162, 125, 105, 67],
  [48, 76, 148, 168, 208, 195, 105, 67],
  [48, 76, 148, 186, 220, 210, 105, 67],
  [48, 76, 110, 129, 222, 212, 182, 67],
  [48, 128, 147, 167, 189, 123, 85, 67],
  [48, 128, 147, 185, 204, 142, 85, 67],
  [48, 128, 147, 167, 207, 145, 105, 67],
  [48, 128, 147, 185, 219, 164, 105, 67],
  [49, 63, 80, 97, 116, 164, 86, 68],
  [49, 63, 80, 97, 116, 182, 86, 68],
  [49, 79, 96, 115, 163, 145, 86, 68]
]
def cycle (r : Fin 2685) := cycles[r.val - 1664]!
theorem checked : ∀ r : Fin 2685,
    1664 ≤ r.val → r.val < 1696 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1664 ≤ r.val) (hhi : r.val < 1696) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01664
