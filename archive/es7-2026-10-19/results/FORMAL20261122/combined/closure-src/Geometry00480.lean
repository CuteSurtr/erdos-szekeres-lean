import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00480
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [41, 87, 126, 167, 189, 174, 158, 121, 81],
  [42, 54, 70, 107, 129, 112, 94, 77, 60],
  [42, 54, 70, 127, 148, 130, 94, 77, 60],
  [42, 54, 70, 107, 150, 133, 115, 96, 60],
  [42, 54, 70, 127, 168, 151, 115, 96, 60],
  [42, 54, 87, 126, 147, 112, 94, 77, 60],
  [42, 54, 87, 126, 167, 133, 115, 96, 60],
  [42, 54, 87, 146, 184, 151, 115, 96, 60],
  [42, 54, 70, 107, 129, 155, 138, 120, 101, 82],
  [42, 54, 70, 127, 148, 172, 156, 120, 101, 82],
  [42, 54, 70, 107, 150, 174, 159, 141, 122, 82],
  [42, 54, 70, 127, 168, 190, 175, 141, 122, 82],
  [42, 54, 87, 126, 147, 171, 138, 120, 101, 82],
  [42, 54, 87, 146, 166, 188, 156, 120, 101, 82],
  [42, 54, 87, 126, 167, 189, 159, 141, 122, 82],
  [42, 54, 87, 146, 184, 203, 175, 141, 122, 82],
  [43, 56, 88, 107, 150, 133, 115, 79, 61],
  [43, 56, 88, 107, 169, 153, 134, 79, 61],
  [43, 56, 106, 126, 167, 133, 115, 79, 61],
  [43, 56, 106, 126, 185, 153, 134, 79, 61],
  [43, 56, 88, 107, 150, 174, 159, 141, 103, 83],
  [43, 56, 88, 107, 169, 191, 177, 160, 103, 83],
  [43, 56, 106, 126, 167, 189, 159, 141, 103, 83],
  [43, 56, 106, 126, 185, 204, 177, 160, 103, 83],
  [44, 57, 72, 90, 133, 159, 123, 104, 84],
  [44, 57, 72, 90, 153, 177, 142, 104, 84],
  [44, 57, 72, 108, 151, 175, 123, 104, 84],
  [44, 57, 72, 108, 170, 192, 142, 104, 84],
  [44, 71, 88, 107, 150, 133, 97, 80, 62],
  [44, 71, 88, 127, 168, 151, 97, 80, 62],
  [44, 71, 88, 107, 169, 153, 116, 80, 62],
  [44, 71, 88, 127, 186, 170, 116, 80, 62]
]
def cycle (r : Fin 2685) := cycles[r.val - 480]!
theorem checked : ∀ r : Fin 2685,
    480 ≤ r.val → r.val < 512 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 480 ≤ r.val) (hhi : r.val < 512) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00480
