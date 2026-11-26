import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01792
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [59, 91, 110, 131, 157, 139, 121, 81],
  [59, 91, 110, 131, 178, 161, 143, 81],
  [59, 91, 129, 150, 174, 158, 121, 81],
  [59, 91, 129, 150, 194, 179, 143, 81],
  [59, 109, 128, 154, 136, 118, 100, 81],
  [59, 109, 147, 171, 155, 137, 100, 81],
  [60, 74, 91, 110, 136, 119, 101, 82],
  [60, 74, 91, 110, 131, 157, 140, 122, 82],
  [60, 74, 91, 110, 131, 178, 162, 144, 82],
  [60, 74, 91, 169, 191, 177, 160, 82],
  [60, 74, 91, 186, 205, 192, 160, 82],
  [60, 74, 91, 169, 209, 197, 181, 82],
  [60, 74, 91, 186, 220, 210, 181, 82],
  [60, 74, 109, 128, 154, 119, 101, 82],
  [60, 74, 109, 147, 171, 138, 120, 101, 82],
  [60, 74, 109, 166, 188, 156, 120, 101, 82],
  [60, 74, 109, 128, 149, 173, 140, 122, 82],
  [60, 74, 109, 185, 204, 177, 160, 82],
  [60, 74, 109, 200, 216, 192, 160, 82],
  [60, 74, 109, 185, 219, 197, 181, 82],
  [60, 74, 109, 200, 228, 210, 181, 82],
  [60, 74, 111, 132, 158, 141, 122, 82],
  [60, 74, 111, 132, 179, 163, 144, 82],
  [60, 74, 183, 199, 215, 141, 122, 82],
  [60, 74, 183, 199, 227, 163, 144, 82],
  [60, 74, 91, 129, 150, 133, 115, 96],
  [60, 74, 91, 148, 168, 151, 115, 96],
  [60, 74, 109, 147, 167, 133, 115, 96],
  [60, 74, 109, 166, 184, 151, 115, 96],
  [60, 75, 112, 133, 159, 141, 122, 82],
  [60, 75, 112, 133, 180, 163, 144, 82],
  [60, 75, 130, 151, 175, 141, 122, 82]
]
def cycle (r : Fin 2685) := cycles[r.val - 1792]!
theorem checked : ∀ r : Fin 2685,
    1792 ≤ r.val → r.val < 1824 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1792 ≤ r.val) (hhi : r.val < 1824) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01792
