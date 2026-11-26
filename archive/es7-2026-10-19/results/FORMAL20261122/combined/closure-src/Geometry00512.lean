import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00512
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [44, 71, 88, 107, 150, 174, 159, 123, 104, 84],
  [44, 71, 88, 107, 169, 191, 177, 142, 104, 84],
  [44, 71, 88, 127, 168, 190, 175, 123, 104, 84],
  [44, 71, 88, 127, 186, 205, 192, 142, 104, 84],
  [45, 109, 128, 149, 173, 157, 139, 121, 64],
  [45, 109, 128, 149, 193, 178, 161, 143, 64],
  [46, 59, 74, 92, 113, 161, 144, 124, 65],
  [46, 59, 74, 111, 132, 179, 163, 124, 65],
  [46, 59, 91, 129, 155, 138, 120, 83, 65],
  [46, 59, 91, 110, 131, 157, 140, 122, 103, 65],
  [46, 59, 91, 129, 150, 174, 159, 141, 103, 65],
  [46, 59, 91, 110, 131, 178, 162, 144, 124, 65],
  [46, 59, 91, 129, 150, 194, 180, 163, 124, 65],
  [46, 59, 109, 128, 149, 173, 140, 122, 103, 65],
  [46, 59, 109, 147, 167, 189, 159, 141, 103, 65],
  [46, 59, 109, 128, 149, 193, 162, 144, 124, 65],
  [46, 59, 109, 147, 167, 207, 180, 163, 124, 65],
  [47, 60, 75, 112, 133, 159, 123, 104, 66],
  [47, 60, 75, 130, 151, 175, 123, 104, 66],
  [47, 60, 75, 112, 133, 180, 145, 125, 66],
  [47, 60, 75, 130, 151, 195, 145, 125, 66],
  [47, 74, 91, 129, 150, 174, 159, 123, 104, 66],
  [47, 74, 91, 148, 168, 190, 175, 123, 104, 66],
  [47, 74, 91, 129, 150, 194, 180, 145, 125, 66],
  [47, 74, 91, 148, 168, 208, 195, 145, 125, 66],
  [48, 61, 77, 94, 115, 141, 123, 85, 67],
  [48, 61, 77, 94, 134, 160, 142, 85, 67],
  [48, 61, 77, 94, 115, 163, 145, 105, 67],
  [48, 61, 77, 94, 134, 181, 164, 105, 67],
  [48, 61, 93, 112, 133, 159, 123, 85, 67],
  [48, 61, 93, 112, 153, 177, 142, 85, 67],
  [48, 61, 93, 112, 133, 180, 145, 105, 67]
]
def cycle (r : Fin 2685) := cycles[r.val - 512]!
theorem checked : ∀ r : Fin 2685,
    512 ≤ r.val → r.val < 544 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 512 ≤ r.val) (hhi : r.val < 544) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00512
