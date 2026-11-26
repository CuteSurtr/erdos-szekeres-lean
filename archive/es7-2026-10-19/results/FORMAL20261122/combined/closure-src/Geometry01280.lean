import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01280
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [23, 41, 54, 74, 98, 82, 66, 51],
  [23, 41, 54, 71, 92, 118, 101, 84, 67, 51],
  [23, 41, 54, 152, 176, 160, 142, 51],
  [23, 41, 56, 76, 100, 83, 67, 51],
  [23, 41, 56, 95, 121, 103, 85, 51],
  [23, 41, 70, 91, 117, 99, 66, 51],
  [23, 41, 127, 148, 172, 156, 67, 51],
  [23, 41, 70, 169, 191, 177, 142, 51],
  [23, 41, 127, 168, 190, 175, 85, 51],
  [23, 41, 54, 71, 161, 144, 125, 105],
  [23, 41, 54, 89, 179, 163, 145, 105],
  [23, 41, 70, 88, 178, 162, 125, 105],
  [23, 41, 70, 107, 194, 180, 145, 105],
  [23, 87, 106, 128, 154, 84, 67, 51],
  [23, 87, 126, 147, 171, 102, 67, 51],
  [23, 87, 106, 149, 173, 104, 85, 51],
  [23, 87, 126, 167, 189, 123, 85, 51],
  [24, 33, 44, 58, 116, 142, 68, 52],
  [24, 56, 71, 113, 96, 80, 49, 36],
  [24, 56, 71, 89, 111, 94, 78, 36],
  [24, 43, 57, 96, 122, 104, 68, 52],
  [24, 43, 57, 73, 94, 120, 102, 52],
  [24, 56, 71, 113, 139, 122, 104, 68, 52],
  [24, 56, 95, 121, 103, 85, 68, 52],
  [24, 56, 71, 92, 118, 101, 84, 52],
  [24, 56, 71, 89, 111, 137, 120, 102, 52],
  [24, 88, 107, 150, 174, 159, 68, 52],
  [24, 88, 107, 169, 191, 177, 68, 52],
  [24, 56, 71, 89, 179, 163, 145, 86],
  [24, 56, 71, 89, 196, 181, 164, 86],
  [25, 34, 46, 61, 79, 103, 85, 37],
  [25, 34, 46, 61, 79, 124, 105, 37]
]
def cycle (r : Fin 2685) := cycles[r.val - 1280]!
theorem checked : ∀ r : Fin 2685,
    1280 ≤ r.val → r.val < 1312 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1280 ≤ r.val) (hhi : r.val < 1312) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01280
