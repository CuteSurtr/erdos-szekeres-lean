import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01504
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [36, 110, 129, 150, 174, 159, 68, 52],
  [36, 110, 129, 169, 191, 177, 68, 52],
  [36, 76, 92, 113, 161, 144, 125, 86, 52],
  [36, 76, 95, 143, 124, 105, 86, 52],
  [36, 76, 92, 111, 137, 120, 102, 52],
  [36, 76, 92, 111, 211, 198, 182, 52],
  [36, 110, 129, 150, 194, 180, 86, 52],
  [36, 110, 129, 169, 209, 197, 86, 52],
  [37, 50, 82, 101, 122, 144, 125, 105],
  [37, 50, 99, 119, 140, 162, 125, 105],
  [37, 64, 81, 100, 121, 143, 124, 105],
  [37, 64, 98, 118, 139, 122, 104, 85],
  [37, 64, 117, 136, 157, 140, 104, 85],
  [38, 65, 82, 101, 122, 144, 125, 86],
  [38, 65, 82, 120, 141, 163, 145, 86],
  [38, 81, 98, 118, 139, 122, 104, 68],
  [38, 81, 98, 137, 158, 141, 123, 68],
  [38, 81, 100, 121, 143, 124, 105, 86],
  [39, 53, 107, 129, 155, 137, 118, 98],
  [39, 53, 127, 148, 172, 137, 118, 98],
  [39, 69, 126, 147, 129, 111, 92, 74],
  [39, 69, 146, 166, 148, 111, 92, 74],
  [39, 69, 106, 128, 154, 136, 118, 98],
  [40, 53, 69, 146, 108, 90, 72, 55],
  [40, 53, 69, 165, 108, 90, 72, 55],
  [40, 53, 69, 126, 147, 112, 93, 75],
  [40, 53, 69, 106, 128, 154, 119, 99],
  [40, 53, 69, 126, 147, 171, 138, 119, 99],
  [40, 53, 69, 184, 203, 175, 159, 140],
  [40, 53, 69, 199, 215, 175, 159, 140],
  [40, 53, 127, 148, 130, 112, 93, 75],
  [40, 53, 107, 129, 155, 138, 119, 99]
]
def cycle (r : Fin 2685) := cycles[r.val - 1504]!
theorem checked : ∀ r : Fin 2685,
    1504 ≤ r.val → r.val < 1536 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1504 ≤ r.val) (hhi : r.val < 1536) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01504
