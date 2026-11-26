import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01600
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [44, 71, 88, 127, 148, 130, 78, 62],
  [44, 71, 89, 132, 115, 97, 80, 62],
  [44, 71, 89, 152, 134, 116, 80, 62],
  [44, 71, 88, 107, 129, 155, 138, 102, 84],
  [44, 71, 88, 127, 148, 172, 156, 102, 84],
  [44, 71, 88, 131, 157, 140, 104, 84],
  [44, 71, 88, 201, 217, 206, 104, 84],
  [44, 71, 89, 111, 137, 120, 102, 84],
  [44, 71, 89, 132, 158, 141, 123, 104, 84],
  [44, 71, 89, 152, 176, 160, 142, 104, 84],
  [44, 71, 88, 107, 194, 180, 145, 125],
  [44, 71, 88, 107, 209, 197, 164, 125],
  [44, 71, 88, 127, 208, 195, 145, 125],
  [44, 71, 88, 127, 220, 210, 164, 125],
  [44, 106, 126, 167, 189, 123, 104, 84],
  [44, 106, 146, 184, 203, 123, 104, 84],
  [44, 106, 126, 185, 204, 142, 104, 84],
  [44, 106, 146, 200, 216, 142, 104, 84],
  [45, 91, 110, 131, 157, 139, 121, 64],
  [45, 91, 110, 131, 178, 161, 143, 64],
  [45, 109, 128, 154, 136, 118, 100, 64],
  [46, 59, 74, 92, 118, 101, 83, 65],
  [46, 59, 74, 111, 137, 120, 83, 65],
  [46, 59, 74, 92, 113, 139, 122, 103, 65],
  [46, 59, 74, 111, 132, 158, 141, 103, 65],
  [46, 59, 91, 110, 136, 119, 101, 83, 65],
  [46, 59, 109, 128, 154, 119, 101, 83, 65],
  [46, 59, 109, 147, 171, 138, 120, 83, 65],
  [46, 59, 91, 169, 191, 177, 160, 65],
  [46, 59, 91, 169, 209, 197, 181, 65],
  [46, 59, 148, 168, 190, 175, 103, 65],
  [46, 59, 166, 184, 203, 175, 103, 65]
]
def cycle (r : Fin 2685) := cycles[r.val - 1600]!
theorem checked : ∀ r : Fin 2685,
    1600 ≤ r.val → r.val < 1632 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1600 ≤ r.val) (hhi : r.val < 1632) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01600
