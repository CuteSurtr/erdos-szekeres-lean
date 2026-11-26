import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01216
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [17, 91, 110, 131, 157, 140, 68, 27],
  [17, 91, 110, 131, 178, 162, 86, 27],
  [17, 45, 59, 76, 95, 79, 63, 49],
  [17, 45, 74, 92, 113, 96, 80, 49],
  [18, 50, 65, 83, 103, 124, 105, 86],
  [18, 64, 81, 100, 121, 103, 85, 68],
  [19, 69, 87, 109, 91, 74, 59, 45],
  [19, 69, 106, 128, 110, 92, 76, 45],
  [19, 53, 70, 91, 117, 98, 81, 64],
  [19, 53, 88, 110, 136, 118, 100, 64],
  [20, 28, 53, 88, 72, 57, 43, 31],
  [20, 28, 53, 107, 90, 73, 43, 31],
  [20, 28, 69, 106, 72, 57, 43, 31],
  [20, 28, 69, 126, 90, 73, 43, 31],
  [20, 28, 39, 71, 92, 77, 61, 46],
  [20, 28, 39, 89, 111, 94, 61, 46],
  [20, 28, 39, 54, 74, 98, 82, 65],
  [20, 28, 39, 71, 92, 118, 101, 83, 65],
  [20, 28, 39, 89, 111, 137, 120, 83, 65],
  [20, 28, 53, 70, 91, 75, 60, 46],
  [20, 28, 69, 87, 109, 75, 60, 46],
  [20, 28, 53, 70, 91, 117, 99, 82, 65],
  [20, 28, 53, 131, 157, 140, 122, 103],
  [20, 28, 53, 150, 174, 159, 141, 103],
  [20, 28, 69, 87, 109, 135, 99, 82, 65],
  [20, 28, 127, 148, 172, 156, 83, 65],
  [20, 28, 146, 166, 188, 156, 83, 65],
  [20, 28, 69, 149, 173, 140, 122, 103],
  [20, 28, 69, 167, 189, 159, 141, 103],
  [20, 40, 72, 93, 119, 101, 83, 65],
  [20, 40, 90, 112, 138, 120, 83, 65],
  [21, 29, 40, 72, 93, 119, 84, 66]
]
def cycle (r : Fin 2685) := cycles[r.val - 1216]!
theorem checked : ∀ r : Fin 2685,
    1216 ≤ r.val → r.val < 1248 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1216 ≤ r.val) (hhi : r.val < 1248) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01216
