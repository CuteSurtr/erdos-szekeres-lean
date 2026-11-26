import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00320
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [19, 69, 106, 128, 154, 136, 118, 100, 64],
  [20, 28, 53, 88, 110, 93, 77, 61, 46],
  [20, 28, 53, 107, 129, 112, 94, 61, 46],
  [20, 28, 69, 106, 128, 93, 77, 61, 46],
  [20, 28, 69, 126, 147, 112, 94, 61, 46],
  [20, 28, 53, 88, 110, 136, 119, 101, 83, 65],
  [20, 28, 53, 107, 129, 155, 138, 120, 83, 65],
  [20, 28, 69, 106, 128, 154, 119, 101, 83, 65],
  [20, 28, 69, 126, 147, 171, 138, 120, 83, 65],
  [21, 29, 40, 90, 112, 138, 102, 84, 66],
  [21, 29, 40, 108, 130, 156, 102, 84, 66],
  [21, 39, 53, 107, 129, 112, 78, 62, 47],
  [21, 39, 53, 127, 148, 130, 78, 62, 47],
  [21, 39, 53, 107, 129, 155, 138, 102, 84, 66],
  [21, 39, 53, 127, 148, 172, 156, 102, 84, 66],
  [22, 30, 70, 88, 110, 93, 77, 61, 34],
  [22, 30, 87, 106, 128, 93, 77, 61, 34],
  [22, 30, 70, 88, 131, 114, 96, 79, 34],
  [22, 30, 87, 106, 149, 114, 96, 79, 34],
  [22, 30, 70, 88, 110, 136, 119, 101, 83, 50],
  [22, 30, 70, 88, 131, 157, 140, 122, 103, 50],
  [22, 30, 87, 106, 128, 154, 119, 101, 83, 50],
  [22, 30, 87, 106, 149, 173, 140, 122, 103, 50],
  [23, 31, 42, 57, 77, 101, 84, 67, 51],
  [23, 31, 42, 57, 96, 122, 104, 85, 51],
  [23, 31, 42, 73, 94, 120, 102, 67, 51],
  [23, 31, 42, 73, 115, 141, 123, 85, 51],
  [23, 31, 55, 72, 93, 119, 84, 67, 51],
  [23, 31, 55, 90, 112, 138, 102, 67, 51],
  [23, 31, 55, 72, 114, 140, 104, 85, 51],
  [23, 31, 55, 90, 133, 159, 123, 85, 51],
  [23, 41, 54, 89, 111, 94, 78, 48, 35]
]
def cycle (r : Fin 2685) := cycles[r.val - 320]!
theorem checked : ∀ r : Fin 2685,
    320 ≤ r.val → r.val < 352 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 320 ≤ r.val) (hhi : r.val < 352) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00320
