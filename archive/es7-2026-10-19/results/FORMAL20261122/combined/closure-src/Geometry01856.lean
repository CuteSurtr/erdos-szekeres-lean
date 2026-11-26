import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01856
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [62, 77, 94, 134, 181, 164, 125, 84],
  [62, 92, 110, 129, 150, 133, 97, 80],
  [62, 92, 110, 148, 168, 151, 97, 80],
  [62, 92, 110, 129, 169, 153, 116, 80],
  [62, 92, 110, 148, 186, 170, 116, 80],
  [62, 92, 110, 129, 155, 138, 102, 84],
  [62, 92, 110, 148, 172, 156, 102, 84],
  [62, 92, 110, 131, 157, 140, 104, 84],
  [62, 92, 110, 201, 217, 206, 104, 84],
  [62, 92, 111, 132, 158, 141, 123, 104, 84],
  [62, 92, 111, 152, 176, 160, 142, 104, 84],
  [62, 92, 110, 131, 178, 162, 125, 84],
  [62, 92, 110, 201, 229, 221, 125, 84],
  [62, 92, 110, 129, 222, 212, 182, 84],
  [62, 92, 110, 148, 231, 223, 182, 84],
  [62, 92, 111, 132, 179, 163, 145, 125, 84],
  [62, 92, 111, 152, 196, 181, 164, 125, 84],
  [62, 128, 147, 167, 189, 123, 104, 84],
  [62, 128, 166, 184, 203, 123, 104, 84],
  [62, 128, 147, 185, 204, 142, 104, 84],
  [62, 128, 166, 200, 216, 142, 104, 84],
  [62, 128, 147, 167, 207, 145, 125, 84],
  [62, 128, 166, 184, 218, 145, 125, 84],
  [62, 128, 147, 185, 219, 164, 125, 84],
  [62, 128, 166, 200, 228, 164, 125, 84],
  [63, 79, 96, 115, 163, 145, 105, 85],
  [63, 79, 96, 115, 134, 160, 142, 85],
  [63, 79, 114, 133, 180, 145, 105, 85],
  [63, 79, 114, 133, 153, 177, 142, 85],
  [63, 95, 113, 161, 144, 125, 105, 85],
  [63, 95, 113, 132, 179, 163, 145, 105, 85],
  [63, 95, 131, 178, 162, 125, 105, 85]
]
def cycle (r : Fin 2685) := cycles[r.val - 1856]!
theorem checked : ∀ r : Fin 2685,
    1856 ≤ r.val → r.val < 1888 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1856 ≤ r.val) (hhi : r.val < 1888) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01856
