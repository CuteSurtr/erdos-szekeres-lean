import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01760
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [57, 71, 88, 131, 157, 140, 122, 101],
  [57, 71, 88, 201, 217, 206, 122, 101],
  [57, 71, 88, 107, 194, 180, 163, 144],
  [57, 71, 88, 107, 209, 197, 181, 144],
  [57, 71, 88, 127, 208, 195, 163, 144],
  [57, 71, 88, 127, 220, 210, 181, 144],
  [57, 71, 89, 132, 158, 141, 122, 101],
  [57, 71, 89, 152, 176, 160, 122, 101],
  [57, 71, 106, 126, 147, 171, 138, 120, 101],
  [57, 71, 106, 146, 166, 188, 156, 120, 101],
  [57, 71, 106, 149, 173, 140, 122, 101],
  [57, 71, 106, 214, 226, 206, 122, 101],
  [57, 71, 165, 199, 215, 141, 122, 101],
  [57, 71, 165, 213, 225, 160, 122, 101],
  [57, 71, 106, 126, 207, 180, 163, 144],
  [57, 71, 106, 126, 219, 197, 181, 144],
  [57, 71, 106, 146, 218, 195, 163, 144],
  [57, 71, 106, 146, 228, 210, 181, 144],
  [57, 72, 90, 133, 159, 141, 122, 101],
  [57, 72, 90, 153, 177, 160, 122, 101],
  [57, 72, 108, 151, 175, 141, 122, 101],
  [57, 72, 108, 170, 192, 160, 122, 101],
  [58, 73, 90, 153, 177, 142, 123, 102],
  [58, 89, 107, 169, 153, 116, 97, 78],
  [58, 89, 107, 127, 168, 151, 97, 78],
  [58, 89, 107, 150, 174, 159, 123, 102],
  [58, 89, 107, 127, 148, 172, 156, 102],
  [58, 89, 152, 176, 160, 142, 123, 102],
  [58, 89, 107, 127, 220, 210, 164, 145],
  [58, 89, 107, 127, 229, 221, 164, 145],
  [58, 126, 146, 200, 216, 142, 123, 102],
  [58, 126, 146, 214, 226, 142, 123, 102]
]
def cycle (r : Fin 2685) := cycles[r.val - 1760]!
theorem checked : ∀ r : Fin 2685,
    1760 ≤ r.val → r.val < 1792 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1760 ≤ r.val) (hhi : r.val < 1792) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01760
