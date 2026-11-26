import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01952
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [72, 88, 106, 146, 228, 210, 197, 162],
  [72, 88, 106, 165, 227, 195, 180, 162],
  [72, 88, 106, 165, 235, 210, 197, 162],
  [72, 88, 107, 150, 174, 159, 140, 119],
  [72, 88, 107, 169, 191, 177, 140, 119],
  [72, 88, 127, 148, 172, 156, 138, 119],
  [72, 88, 127, 168, 190, 175, 159, 140, 119],
  [72, 88, 127, 186, 205, 192, 177, 140, 119],
  [73, 89, 107, 127, 168, 151, 115, 94],
  [73, 89, 107, 169, 153, 134, 115, 94],
  [73, 89, 126, 185, 153, 134, 115, 94],
  [73, 89, 126, 146, 184, 151, 115, 94],
  [73, 89, 107, 127, 168, 190, 175, 141, 120],
  [73, 89, 107, 127, 148, 172, 156, 120],
  [73, 89, 107, 150, 174, 159, 141, 120],
  [73, 89, 107, 169, 191, 177, 160, 141, 120],
  [73, 89, 107, 127, 220, 210, 181, 163],
  [73, 89, 107, 127, 229, 221, 181, 163],
  [73, 89, 126, 146, 184, 203, 175, 141, 120],
  [73, 89, 126, 167, 189, 159, 141, 120],
  [73, 89, 126, 185, 204, 177, 160, 141, 120],
  [73, 89, 126, 146, 166, 188, 156, 120],
  [73, 89, 165, 213, 225, 160, 141, 120],
  [73, 89, 165, 224, 234, 160, 141, 120],
  [73, 89, 126, 146, 228, 210, 181, 163],
  [73, 89, 126, 146, 236, 221, 181, 163],
  [73, 90, 108, 170, 192, 160, 141, 120],
  [73, 90, 108, 187, 206, 160, 141, 120],
  [74, 91, 129, 150, 174, 158, 139, 98],
  [74, 91, 129, 150, 194, 179, 161, 98],
  [74, 91, 148, 168, 190, 158, 139, 98],
  [74, 91, 148, 168, 208, 179, 161, 98]
]
def cycle (r : Fin 2685) := cycles[r.val - 1952]!
theorem checked : ∀ r : Fin 2685,
    1952 ≤ r.val → r.val < 1984 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1952 ≤ r.val) (hhi : r.val < 1984) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01952
