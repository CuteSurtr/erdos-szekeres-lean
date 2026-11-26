import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01568
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [42, 55, 108, 151, 175, 141, 122, 82],
  [43, 56, 71, 89, 132, 115, 79, 61],
  [43, 56, 71, 89, 152, 134, 79, 61],
  [43, 56, 88, 131, 114, 96, 79, 61],
  [43, 56, 106, 149, 114, 96, 79, 61],
  [43, 56, 88, 107, 129, 112, 94, 61],
  [43, 56, 106, 126, 147, 112, 94, 61],
  [43, 56, 71, 89, 132, 158, 141, 103, 83],
  [43, 56, 71, 89, 152, 176, 160, 103, 83],
  [43, 56, 71, 89, 111, 137, 120, 83],
  [43, 56, 71, 113, 139, 122, 103, 83],
  [43, 56, 88, 110, 136, 119, 101, 83],
  [43, 56, 88, 131, 157, 140, 122, 103, 83],
  [43, 56, 88, 107, 129, 155, 138, 120, 83],
  [43, 56, 106, 128, 154, 119, 101, 83],
  [43, 56, 106, 149, 173, 140, 122, 103, 83],
  [43, 56, 127, 168, 190, 175, 103, 83],
  [43, 56, 127, 186, 205, 192, 103, 83],
  [43, 56, 146, 184, 203, 175, 103, 83],
  [43, 56, 146, 200, 216, 192, 103, 83],
  [43, 56, 106, 126, 147, 171, 138, 120, 83],
  [43, 56, 88, 107, 194, 180, 163, 124],
  [43, 56, 88, 107, 209, 197, 181, 124],
  [43, 56, 106, 126, 207, 180, 163, 124],
  [43, 56, 106, 126, 219, 197, 181, 124],
  [43, 72, 90, 133, 159, 141, 103, 83],
  [43, 72, 90, 153, 177, 160, 103, 83],
  [44, 57, 72, 90, 112, 138, 102, 84],
  [44, 57, 72, 108, 130, 156, 102, 84],
  [44, 57, 73, 115, 141, 123, 104, 84],
  [44, 57, 73, 134, 160, 142, 104, 84],
  [44, 71, 88, 107, 129, 112, 78, 62]
]
def cycle (r : Fin 2685) := cycles[r.val - 1568]!
theorem checked : ∀ r : Fin 2685,
    1568 ≤ r.val → r.val < 1600 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1568 ≤ r.val) (hhi : r.val < 1600) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01568
