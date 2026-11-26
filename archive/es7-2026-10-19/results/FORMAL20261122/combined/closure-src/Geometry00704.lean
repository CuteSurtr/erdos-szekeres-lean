import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00704
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [77, 92, 110, 129, 150, 174, 159, 141, 122, 101],
  [77, 92, 110, 129, 169, 191, 177, 160, 122, 101],
  [77, 92, 110, 148, 168, 190, 175, 141, 122, 101],
  [77, 92, 110, 148, 186, 205, 192, 160, 122, 101],
  [77, 92, 110, 129, 169, 209, 197, 181, 144, 101],
  [77, 92, 110, 148, 168, 208, 195, 163, 144, 101],
  [77, 92, 110, 148, 186, 220, 210, 181, 144, 101],
  [77, 92, 128, 147, 167, 189, 159, 141, 122, 101],
  [77, 92, 128, 166, 184, 203, 175, 141, 122, 101],
  [77, 92, 128, 147, 185, 204, 177, 160, 122, 101],
  [77, 92, 128, 166, 200, 216, 192, 160, 122, 101],
  [77, 92, 128, 147, 167, 207, 180, 163, 144, 101],
  [77, 92, 128, 147, 185, 219, 197, 181, 144, 101],
  [77, 92, 128, 166, 184, 218, 195, 163, 144, 101],
  [77, 92, 128, 166, 200, 228, 210, 181, 144, 101],
  [78, 94, 112, 130, 170, 192, 142, 123, 102],
  [78, 94, 112, 130, 187, 206, 142, 123, 102],
  [78, 94, 112, 130, 170, 210, 164, 145, 102],
  [78, 94, 112, 130, 187, 221, 164, 145, 102],
  [78, 111, 129, 148, 186, 205, 192, 142, 123, 102],
  [78, 111, 129, 148, 201, 217, 206, 142, 123, 102],
  [78, 111, 129, 148, 186, 220, 210, 164, 145, 102],
  [78, 111, 129, 148, 201, 229, 221, 164, 145, 102],
  [79, 95, 113, 132, 152, 211, 198, 124, 103],
  [79, 95, 131, 150, 169, 209, 197, 181, 124, 103],
  [79, 95, 131, 150, 169, 222, 212, 198, 124, 103],
  [79, 95, 149, 167, 185, 219, 197, 181, 124, 103],
  [79, 95, 149, 167, 185, 230, 212, 198, 124, 103],
  [79, 95, 131, 150, 169, 191, 177, 160, 103],
  [80, 96, 114, 133, 153, 197, 164, 125, 104],
  [80, 96, 114, 133, 153, 212, 182, 125, 104],
  [80, 96, 114, 151, 170, 210, 164, 125, 104]
]
def cycle (r : Fin 2685) := cycles[r.val - 704]!
theorem checked : ∀ r : Fin 2685,
    704 ≤ r.val → r.val < 736 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 704 ≤ r.val) (hhi : r.val < 736) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00704
