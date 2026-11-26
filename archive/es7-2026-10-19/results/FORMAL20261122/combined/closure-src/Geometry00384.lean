import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00384
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [26, 59, 74, 111, 132, 158, 141, 123, 68, 38],
  [26, 59, 74, 92, 113, 161, 144, 125, 86, 38],
  [26, 59, 74, 111, 132, 179, 163, 145, 86, 38],
  [27, 64, 81, 100, 121, 143, 124, 105, 86],
  [27, 64, 98, 118, 139, 161, 144, 125, 86],
  [28, 69, 106, 128, 154, 136, 118, 100, 81],
  [28, 69, 126, 147, 171, 155, 137, 100, 81],
  [29, 39, 53, 107, 129, 112, 94, 77, 60],
  [29, 39, 53, 127, 148, 130, 94, 77, 60],
  [29, 39, 53, 107, 129, 155, 138, 120, 101, 82],
  [29, 39, 53, 127, 148, 172, 156, 120, 101, 82],
  [29, 39, 69, 126, 147, 112, 94, 77, 60],
  [29, 39, 69, 146, 166, 130, 94, 77, 60],
  [29, 39, 69, 126, 147, 171, 138, 120, 101, 82],
  [29, 39, 69, 146, 166, 188, 156, 120, 101, 82],
  [30, 87, 106, 128, 154, 136, 118, 100, 64],
  [30, 87, 106, 149, 173, 157, 139, 121, 64],
  [31, 41, 70, 88, 110, 93, 77, 61, 46],
  [31, 41, 70, 107, 129, 112, 94, 61, 46],
  [31, 41, 87, 126, 147, 112, 94, 61, 46],
  [31, 41, 70, 88, 131, 114, 96, 79, 46],
  [31, 41, 70, 107, 150, 133, 115, 79, 46],
  [31, 41, 87, 106, 149, 114, 96, 79, 46],
  [31, 41, 87, 126, 167, 133, 115, 79, 46],
  [31, 41, 70, 88, 110, 136, 119, 101, 83, 65],
  [31, 41, 70, 107, 129, 155, 138, 120, 83, 65],
  [31, 41, 70, 88, 131, 157, 140, 122, 103, 65],
  [31, 41, 70, 107, 150, 174, 159, 141, 103, 65],
  [31, 41, 87, 106, 128, 154, 119, 101, 83, 65],
  [31, 41, 87, 126, 147, 171, 138, 120, 83, 65],
  [31, 41, 87, 106, 149, 173, 140, 122, 103, 65],
  [31, 41, 87, 126, 167, 189, 159, 141, 103, 65]
]
def cycle (r : Fin 2685) := cycles[r.val - 384]!
theorem checked : ∀ r : Fin 2685,
    384 ≤ r.val → r.val < 416 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 384 ≤ r.val) (hhi : r.val < 416) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00384
