import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00608
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [59, 109, 147, 167, 207, 194, 179, 143, 81],
  [60, 74, 91, 129, 155, 138, 120, 101, 82],
  [60, 74, 91, 148, 172, 156, 120, 101, 82],
  [60, 74, 91, 129, 150, 174, 159, 141, 122, 82],
  [60, 74, 91, 148, 168, 190, 175, 141, 122, 82],
  [60, 74, 91, 129, 150, 194, 180, 163, 144, 82],
  [60, 74, 91, 148, 168, 208, 195, 163, 144, 82],
  [60, 74, 109, 147, 167, 189, 159, 141, 122, 82],
  [60, 74, 109, 166, 184, 203, 175, 141, 122, 82],
  [60, 74, 109, 128, 149, 193, 162, 144, 82],
  [60, 74, 109, 147, 167, 207, 180, 163, 144, 82],
  [60, 74, 109, 166, 184, 218, 195, 163, 144, 82],
  [61, 76, 92, 111, 132, 158, 141, 103, 83],
  [61, 76, 92, 111, 132, 179, 163, 124, 83],
  [61, 76, 110, 129, 150, 174, 159, 141, 103, 83],
  [61, 76, 110, 129, 169, 191, 177, 160, 103, 83],
  [61, 76, 128, 147, 167, 189, 159, 141, 103, 83],
  [61, 76, 128, 147, 185, 204, 177, 160, 103, 83],
  [61, 76, 110, 129, 150, 194, 180, 163, 124, 83],
  [61, 76, 110, 129, 169, 209, 197, 181, 124, 83],
  [61, 76, 128, 147, 167, 207, 180, 163, 124, 83],
  [61, 76, 128, 147, 185, 219, 197, 181, 124, 83],
  [62, 77, 93, 112, 133, 159, 123, 104, 84],
  [62, 77, 93, 112, 153, 177, 142, 104, 84],
  [62, 77, 93, 130, 151, 175, 123, 104, 84],
  [62, 77, 93, 130, 170, 192, 142, 104, 84],
  [62, 77, 93, 112, 133, 180, 145, 125, 84],
  [62, 77, 93, 112, 153, 197, 164, 125, 84],
  [62, 77, 93, 130, 151, 195, 145, 125, 84],
  [62, 77, 93, 130, 170, 210, 164, 125, 84],
  [62, 92, 110, 129, 150, 174, 159, 123, 104, 84],
  [62, 92, 110, 148, 168, 190, 175, 123, 104, 84]
]
def cycle (r : Fin 2685) := cycles[r.val - 608]!
theorem checked : ∀ r : Fin 2685,
    608 ≤ r.val → r.val < 640 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 608 ≤ r.val) (hhi : r.val < 640) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00608
