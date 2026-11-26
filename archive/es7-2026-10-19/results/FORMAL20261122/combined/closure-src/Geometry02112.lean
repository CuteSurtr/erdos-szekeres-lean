import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02112
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [82, 98, 135, 171, 189, 159, 141, 122],
  [82, 98, 135, 188, 203, 175, 141, 122],
  [82, 98, 135, 154, 173, 193, 162, 144],
  [83, 100, 136, 155, 174, 159, 141, 103],
  [83, 100, 136, 155, 191, 177, 160, 103],
  [83, 100, 154, 171, 189, 159, 141, 103],
  [83, 100, 154, 171, 204, 177, 160, 103],
  [83, 100, 118, 137, 158, 179, 163, 124],
  [83, 100, 118, 137, 176, 196, 181, 124],
  [83, 100, 136, 157, 178, 162, 144, 124],
  [83, 100, 154, 173, 193, 162, 144, 124],
  [84, 101, 119, 138, 159, 180, 145, 125],
  [84, 101, 119, 138, 177, 197, 164, 125],
  [84, 101, 119, 156, 175, 195, 145, 125],
  [84, 101, 119, 156, 192, 210, 164, 125],
  [84, 118, 136, 155, 174, 159, 123, 104],
  [84, 118, 136, 172, 190, 175, 123, 104],
  [84, 118, 136, 155, 191, 177, 142, 104],
  [84, 118, 136, 172, 205, 192, 142, 104],
  [84, 118, 137, 158, 179, 163, 145, 125],
  [84, 118, 137, 176, 196, 181, 164, 125],
  [85, 103, 122, 141, 160, 181, 164, 105],
  [85, 103, 122, 141, 160, 198, 182, 105],
  [85, 103, 140, 159, 177, 197, 164, 105],
  [85, 103, 140, 159, 177, 212, 182, 105],
  [85, 121, 139, 158, 179, 163, 145, 105],
  [85, 121, 157, 174, 194, 180, 145, 105],
  [86, 143, 161, 179, 196, 211, 198, 182],
  [87, 165, 183, 202, 188, 171, 154, 135],
  [87, 165, 199, 215, 203, 189, 173, 135],
  [88, 106, 146, 184, 168, 150, 131, 110],
  [88, 106, 146, 200, 186, 169, 131, 110]
]
def cycle (r : Fin 2685) := cycles[r.val - 2112]!
theorem checked : ∀ r : Fin 2685,
    2112 ≤ r.val → r.val < 2144 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2112 ≤ r.val) (hhi : r.val < 2144) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02112
