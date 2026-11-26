import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02080
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [79, 95, 184, 200, 228, 210, 124, 103],
  [79, 95, 184, 200, 237, 223, 124, 103],
  [79, 95, 131, 150, 174, 159, 141, 103],
  [79, 95, 149, 167, 189, 159, 141, 103],
  [79, 95, 149, 167, 185, 204, 177, 160, 103],
  [79, 114, 133, 153, 197, 181, 124, 103],
  [79, 114, 133, 153, 212, 198, 124, 103],
  [80, 96, 114, 133, 180, 145, 125, 104],
  [80, 96, 114, 151, 195, 145, 125, 104],
  [80, 96, 114, 133, 153, 177, 142, 104],
  [80, 96, 114, 151, 170, 192, 142, 104],
  [80, 96, 115, 134, 181, 164, 125, 104],
  [80, 96, 115, 134, 198, 182, 125, 104],
  [80, 113, 131, 150, 174, 159, 123, 104],
  [80, 113, 131, 168, 190, 175, 123, 104],
  [80, 113, 131, 150, 194, 180, 145, 125, 104],
  [80, 113, 131, 168, 208, 195, 145, 125, 104],
  [80, 113, 131, 201, 229, 221, 125, 104],
  [80, 113, 131, 201, 238, 232, 125, 104],
  [80, 113, 132, 179, 163, 145, 125, 104],
  [80, 113, 132, 152, 196, 181, 164, 125, 104],
  [80, 113, 132, 152, 211, 198, 182, 125, 104],
  [80, 113, 131, 150, 169, 191, 177, 142, 104],
  [80, 113, 131, 168, 186, 205, 192, 142, 104],
  [80, 113, 132, 152, 176, 160, 142, 104],
  [80, 149, 167, 185, 219, 164, 125, 104],
  [80, 149, 184, 200, 228, 164, 125, 104],
  [80, 149, 167, 185, 230, 182, 125, 104],
  [80, 149, 184, 200, 237, 182, 125, 104],
  [82, 98, 117, 155, 174, 159, 141, 122],
  [82, 98, 117, 172, 190, 175, 141, 122],
  [82, 98, 117, 136, 157, 178, 162, 144]
]
def cycle (r : Fin 2685) := cycles[r.val - 2080]!
theorem checked : ∀ r : Fin 2685,
    2080 ≤ r.val → r.val < 2112 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2080 ≤ r.val) (hhi : r.val < 2112) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02080
