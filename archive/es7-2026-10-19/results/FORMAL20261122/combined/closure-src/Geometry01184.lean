import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01184
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [15, 30, 107, 150, 174, 159, 123, 37],
  [15, 30, 54, 71, 161, 144, 125, 105],
  [15, 30, 70, 88, 178, 162, 125, 105],
  [15, 87, 106, 128, 154, 84, 67, 37],
  [15, 87, 106, 149, 173, 104, 85, 37],
  [16, 23, 32, 44, 62, 84, 52, 38],
  [16, 41, 56, 76, 61, 48, 36, 26],
  [16, 41, 56, 95, 79, 63, 49, 26],
  [16, 31, 43, 61, 83, 67, 52, 38],
  [16, 31, 43, 79, 103, 85, 68, 38],
  [16, 41, 56, 76, 100, 83, 67, 52, 38],
  [16, 41, 54, 74, 98, 82, 66, 38],
  [16, 41, 54, 152, 176, 160, 142, 38],
  [16, 41, 56, 95, 121, 103, 85, 68, 38],
  [16, 70, 88, 110, 136, 119, 52, 38],
  [16, 70, 107, 129, 155, 138, 52, 38],
  [16, 70, 88, 131, 157, 140, 68, 38],
  [16, 70, 107, 150, 174, 159, 68, 38],
  [16, 41, 54, 71, 161, 144, 125, 86],
  [16, 41, 54, 89, 179, 163, 145, 86],
  [17, 25, 35, 48, 63, 85, 68, 27],
  [17, 25, 35, 48, 63, 105, 86, 27],
  [17, 25, 47, 62, 80, 104, 68, 27],
  [17, 25, 47, 62, 80, 125, 86, 27],
  [17, 34, 46, 61, 83, 67, 52, 27],
  [17, 34, 60, 77, 101, 84, 52, 27],
  [17, 45, 59, 81, 65, 51, 38, 27],
  [17, 45, 74, 98, 82, 66, 38, 27],
  [17, 45, 59, 76, 100, 83, 67, 52, 27],
  [17, 45, 74, 92, 118, 101, 84, 52, 27],
  [17, 45, 111, 132, 158, 141, 123, 27],
  [17, 45, 111, 132, 179, 163, 145, 27]
]
def cycle (r : Fin 2685) := cycles[r.val - 1184]!
theorem checked : ∀ r : Fin 2685,
    1184 ≤ r.val → r.val < 1216 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1184 ≤ r.val) (hhi : r.val < 1216) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01184
