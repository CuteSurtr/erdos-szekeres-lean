import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00448
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [35, 46, 75, 112, 133, 159, 123, 85, 51],
  [35, 46, 75, 93, 114, 162, 125, 105, 51],
  [35, 46, 75, 112, 133, 180, 145, 105, 51],
  [35, 59, 74, 111, 132, 158, 141, 123, 85, 51],
  [35, 59, 74, 92, 113, 161, 144, 125, 105, 51],
  [35, 59, 74, 111, 132, 179, 163, 145, 105, 51],
  [35, 59, 91, 110, 131, 157, 140, 104, 85, 51],
  [35, 59, 91, 129, 150, 174, 159, 123, 85, 51],
  [35, 59, 91, 110, 131, 178, 162, 125, 105, 51],
  [35, 59, 91, 129, 150, 194, 180, 145, 105, 51],
  [36, 61, 77, 94, 115, 141, 123, 68, 52],
  [36, 61, 77, 94, 134, 160, 142, 68, 52],
  [36, 61, 77, 94, 115, 163, 145, 86, 52],
  [36, 61, 77, 94, 134, 181, 164, 86, 52],
  [36, 76, 92, 111, 132, 158, 141, 123, 68, 52],
  [36, 76, 92, 111, 152, 176, 160, 142, 68, 52],
  [36, 76, 92, 111, 132, 179, 163, 145, 86, 52],
  [36, 76, 92, 111, 152, 196, 181, 164, 86, 52],
  [37, 64, 98, 118, 139, 161, 144, 125, 105],
  [37, 64, 117, 136, 157, 178, 162, 125, 105],
  [38, 81, 98, 118, 139, 161, 144, 125, 86],
  [38, 81, 98, 137, 158, 179, 163, 145, 86],
  [39, 69, 126, 147, 171, 155, 137, 118, 98],
  [39, 69, 146, 166, 188, 172, 137, 118, 98],
  [40, 53, 69, 146, 166, 130, 112, 93, 75],
  [40, 53, 69, 165, 183, 130, 112, 93, 75],
  [40, 53, 69, 146, 166, 188, 156, 138, 119, 99],
  [40, 53, 69, 165, 183, 202, 156, 138, 119, 99],
  [40, 53, 127, 148, 172, 156, 138, 119, 99],
  [41, 87, 106, 128, 154, 136, 118, 100, 81],
  [41, 87, 126, 147, 171, 155, 137, 100, 81],
  [41, 87, 106, 149, 173, 157, 139, 121, 81]
]
def cycle (r : Fin 2685) := cycles[r.val - 448]!
theorem checked : ∀ r : Fin 2685,
    448 ≤ r.val → r.val < 480 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 448 ≤ r.val) (hhi : r.val < 480) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00448
