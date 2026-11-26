import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02368
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [113, 149, 184, 218, 208, 179, 161, 139],
  [113, 149, 167, 185, 204, 191, 176, 139],
  [113, 149, 184, 200, 216, 205, 176, 139],
  [114, 131, 149, 184, 203, 175, 159, 140],
  [114, 131, 149, 199, 215, 175, 159, 140],
  [114, 131, 149, 167, 207, 180, 162, 140],
  [114, 131, 149, 167, 185, 219, 197, 162, 140],
  [114, 131, 149, 167, 185, 230, 212, 162, 140],
  [114, 131, 149, 184, 218, 195, 180, 162, 140],
  [114, 131, 149, 199, 227, 195, 180, 162, 140],
  [114, 131, 149, 214, 236, 221, 162, 140],
  [114, 131, 149, 214, 243, 232, 162, 140],
  [114, 131, 149, 224, 241, 221, 162, 140],
  [114, 131, 149, 224, 246, 232, 162, 140],
  [114, 131, 149, 167, 185, 204, 177, 140],
  [114, 131, 149, 184, 200, 216, 192, 177, 140],
  [114, 131, 149, 199, 213, 225, 192, 177, 140],
  [114, 131, 150, 169, 209, 197, 162, 140],
  [114, 131, 150, 169, 222, 212, 162, 140],
  [114, 131, 168, 208, 195, 180, 162, 140],
  [114, 131, 168, 186, 220, 210, 197, 162, 140],
  [114, 131, 168, 186, 231, 223, 212, 162, 140],
  [114, 131, 168, 186, 205, 192, 177, 140],
  [115, 132, 150, 168, 201, 217, 206, 160, 141],
  [115, 132, 150, 169, 191, 177, 160, 141],
  [115, 132, 150, 168, 208, 195, 163, 141],
  [115, 132, 150, 168, 244, 239, 163, 141],
  [115, 132, 150, 169, 209, 197, 181, 163, 141],
  [115, 132, 150, 169, 222, 212, 198, 163, 141],
  [115, 132, 167, 185, 204, 177, 160, 141],
  [115, 132, 167, 184, 200, 216, 192, 160, 141],
  [115, 132, 167, 184, 214, 226, 206, 160, 141]
]
def cycle (r : Fin 2685) := cycles[r.val - 2368]!
theorem checked : ∀ r : Fin 2685,
    2368 ≤ r.val → r.val < 2400 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2368 ≤ r.val) (hhi : r.val < 2400) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02368
