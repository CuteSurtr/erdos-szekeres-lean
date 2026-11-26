import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01376
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [29, 40, 108, 130, 156, 120, 101, 82],
  [30, 87, 106, 128, 110, 92, 76, 45],
  [30, 87, 106, 149, 131, 113, 95, 45],
  [30, 70, 88, 110, 136, 118, 100, 64],
  [30, 70, 88, 131, 157, 139, 121, 64],
  [30, 87, 109, 135, 117, 98, 81, 64],
  [31, 41, 54, 71, 92, 77, 61, 46],
  [31, 41, 54, 89, 111, 94, 61, 46],
  [31, 41, 54, 71, 113, 96, 79, 46],
  [31, 41, 54, 89, 132, 115, 79, 46],
  [31, 41, 87, 106, 128, 93, 77, 61, 46],
  [31, 41, 54, 71, 92, 118, 101, 83, 65],
  [31, 41, 54, 71, 113, 139, 122, 103, 65],
  [31, 41, 54, 89, 111, 137, 120, 83, 65],
  [31, 41, 54, 89, 132, 158, 141, 103, 65],
  [31, 41, 70, 91, 117, 99, 82, 65],
  [31, 41, 70, 169, 191, 177, 160, 65],
  [31, 41, 87, 109, 135, 99, 82, 65],
  [31, 41, 127, 148, 172, 156, 83, 65],
  [31, 41, 146, 166, 188, 156, 83, 65],
  [31, 41, 87, 185, 204, 177, 160, 65],
  [31, 41, 127, 168, 190, 175, 103, 65],
  [31, 41, 146, 184, 203, 175, 103, 65],
  [31, 41, 70, 88, 178, 162, 144, 124],
  [31, 41, 70, 107, 194, 180, 163, 124],
  [31, 41, 87, 106, 193, 162, 144, 124],
  [31, 41, 87, 126, 207, 180, 163, 124],
  [31, 55, 72, 93, 119, 101, 83, 65],
  [31, 55, 72, 114, 140, 122, 103, 65],
  [31, 55, 90, 112, 138, 120, 83, 65],
  [31, 55, 90, 133, 159, 141, 103, 65],
  [32, 42, 55, 72, 93, 119, 84, 66]
]
def cycle (r : Fin 2685) := cycles[r.val - 1376]!
theorem checked : ∀ r : Fin 2685,
    1376 ≤ r.val → r.val < 1408 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1376 ≤ r.val) (hhi : r.val < 1408) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01376
