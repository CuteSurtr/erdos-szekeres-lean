import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00352
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [23, 41, 70, 88, 110, 93, 62, 48, 35],
  [23, 41, 70, 107, 129, 112, 78, 48, 35],
  [23, 41, 54, 71, 113, 96, 80, 63, 35],
  [23, 41, 54, 89, 132, 115, 97, 63, 35],
  [23, 41, 70, 88, 131, 114, 80, 63, 35],
  [23, 41, 70, 107, 150, 133, 97, 63, 35],
  [23, 41, 54, 89, 111, 137, 120, 102, 67, 51],
  [23, 41, 54, 71, 113, 139, 122, 104, 85, 51],
  [23, 41, 54, 89, 132, 158, 141, 123, 85, 51],
  [23, 41, 70, 88, 110, 136, 119, 84, 67, 51],
  [23, 41, 70, 107, 129, 155, 138, 102, 67, 51],
  [23, 41, 70, 88, 131, 157, 140, 104, 85, 51],
  [23, 41, 70, 107, 150, 174, 159, 123, 85, 51],
  [24, 56, 71, 89, 132, 115, 97, 49, 36],
  [24, 56, 71, 89, 152, 134, 116, 49, 36],
  [24, 43, 57, 73, 115, 141, 123, 68, 52],
  [24, 43, 57, 73, 134, 160, 142, 68, 52],
  [24, 56, 71, 89, 132, 158, 141, 123, 68, 52],
  [24, 56, 71, 89, 152, 176, 160, 142, 68, 52],
  [25, 34, 60, 77, 96, 122, 104, 85, 37],
  [25, 34, 60, 77, 96, 144, 125, 105, 37],
  [25, 34, 75, 93, 114, 140, 104, 85, 37],
  [25, 34, 75, 93, 114, 162, 125, 105, 37],
  [25, 45, 74, 92, 113, 139, 122, 104, 85, 37],
  [25, 45, 74, 92, 113, 161, 144, 125, 105, 37],
  [25, 45, 91, 110, 131, 157, 140, 104, 85, 37],
  [25, 45, 91, 110, 131, 178, 162, 125, 105, 37],
  [26, 46, 60, 77, 96, 122, 104, 68, 38],
  [26, 46, 60, 94, 115, 141, 123, 68, 38],
  [26, 46, 60, 77, 96, 144, 125, 86, 38],
  [26, 46, 60, 94, 115, 163, 145, 86, 38],
  [26, 59, 74, 92, 113, 139, 122, 104, 68, 38]
]
def cycle (r : Fin 2685) := cycles[r.val - 352]!
theorem checked : ∀ r : Fin 2685,
    352 ≤ r.val → r.val < 384 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 352 ≤ r.val) (hhi : r.val < 384) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00352
