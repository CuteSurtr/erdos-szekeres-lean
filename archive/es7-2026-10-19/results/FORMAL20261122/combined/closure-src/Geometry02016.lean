import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02016
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [77, 92, 128, 166, 184, 151, 115, 96],
  [77, 92, 128, 147, 185, 153, 134, 96],
  [77, 92, 128, 166, 200, 170, 134, 96],
  [77, 92, 110, 129, 155, 138, 120, 101],
  [77, 92, 110, 148, 172, 156, 120, 101],
  [77, 92, 110, 131, 157, 140, 122, 101],
  [77, 92, 110, 201, 217, 206, 122, 101],
  [77, 92, 110, 129, 150, 194, 180, 163, 144, 101],
  [77, 92, 110, 129, 222, 212, 198, 101],
  [77, 92, 110, 131, 178, 162, 144, 101],
  [77, 92, 110, 201, 229, 221, 144, 101],
  [77, 92, 110, 148, 231, 223, 198, 101],
  [77, 92, 111, 132, 158, 141, 122, 101],
  [77, 92, 111, 152, 176, 160, 122, 101],
  [77, 92, 111, 132, 179, 163, 144, 101],
  [77, 92, 111, 152, 196, 181, 144, 101],
  [77, 92, 128, 147, 171, 138, 120, 101],
  [77, 92, 128, 166, 188, 156, 120, 101],
  [77, 92, 128, 149, 173, 140, 122, 101],
  [77, 92, 128, 214, 226, 206, 122, 101],
  [77, 92, 183, 199, 215, 141, 122, 101],
  [77, 92, 183, 213, 225, 160, 122, 101],
  [77, 92, 128, 149, 193, 162, 144, 101],
  [77, 92, 128, 214, 236, 221, 144, 101],
  [77, 92, 128, 147, 230, 212, 198, 101],
  [77, 92, 128, 166, 237, 223, 198, 101],
  [77, 92, 183, 199, 227, 163, 144, 101],
  [77, 92, 183, 213, 235, 181, 144, 101],
  [77, 93, 112, 133, 159, 141, 122, 101],
  [77, 93, 112, 153, 177, 160, 122, 101],
  [77, 93, 112, 133, 180, 163, 144, 101],
  [77, 93, 112, 153, 197, 181, 144, 101]
]
def cycle (r : Fin 2685) := cycles[r.val - 2016]!
theorem checked : ∀ r : Fin 2685,
    2016 ≤ r.val → r.val < 2048 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2016 ≤ r.val) (hhi : r.val < 2048) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02016
