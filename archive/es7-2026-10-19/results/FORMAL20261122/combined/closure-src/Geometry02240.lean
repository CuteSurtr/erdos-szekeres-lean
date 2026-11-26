import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02240
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [96, 113, 131, 150, 174, 159, 141, 122],
  [96, 113, 131, 168, 190, 175, 141, 122],
  [96, 113, 131, 150, 194, 180, 163, 144, 122],
  [96, 113, 131, 168, 208, 195, 163, 144, 122],
  [96, 113, 131, 201, 229, 221, 144, 122],
  [96, 113, 131, 201, 238, 232, 144, 122],
  [96, 113, 131, 168, 186, 205, 192, 160, 122],
  [96, 113, 132, 152, 196, 181, 144, 122],
  [96, 113, 132, 152, 211, 198, 144, 122],
  [96, 113, 149, 167, 189, 159, 141, 122],
  [96, 113, 149, 184, 203, 175, 141, 122],
  [96, 113, 149, 167, 207, 180, 163, 144, 122],
  [96, 113, 149, 184, 218, 195, 163, 144, 122],
  [96, 113, 149, 214, 236, 221, 144, 122],
  [96, 113, 149, 214, 243, 232, 144, 122],
  [96, 113, 199, 213, 235, 181, 144, 122],
  [96, 113, 199, 213, 242, 198, 144, 122],
  [96, 113, 149, 167, 185, 204, 177, 160, 122],
  [96, 113, 149, 184, 200, 216, 192, 160, 122],
  [96, 114, 133, 153, 197, 181, 144, 122],
  [96, 114, 133, 153, 212, 198, 144, 122],
  [96, 114, 151, 170, 210, 181, 144, 122],
  [96, 114, 151, 170, 223, 198, 144, 122],
  [97, 115, 133, 151, 170, 192, 142, 123],
  [97, 115, 133, 151, 187, 206, 142, 123],
  [97, 115, 133, 153, 197, 164, 145, 123],
  [97, 115, 133, 153, 212, 182, 145, 123],
  [97, 132, 150, 168, 186, 205, 192, 142, 123],
  [97, 132, 150, 169, 191, 177, 142, 123],
  [97, 132, 150, 169, 209, 197, 164, 145, 123],
  [97, 132, 150, 168, 208, 195, 145, 123],
  [97, 132, 150, 168, 244, 239, 145, 123]
]
def cycle (r : Fin 2685) := cycles[r.val - 2240]!
theorem checked : ∀ r : Fin 2685,
    2240 ≤ r.val → r.val < 2272 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2240 ≤ r.val) (hhi : r.val < 2272) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02240
