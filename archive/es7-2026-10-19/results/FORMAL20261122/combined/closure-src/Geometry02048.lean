import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02048
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [77, 93, 130, 151, 175, 141, 122, 101],
  [77, 93, 130, 170, 192, 160, 122, 101],
  [77, 93, 130, 151, 195, 163, 144, 101],
  [77, 93, 130, 170, 210, 181, 144, 101],
  [78, 94, 112, 153, 177, 142, 123, 102],
  [78, 94, 112, 130, 151, 195, 145, 102],
  [78, 94, 112, 153, 197, 164, 145, 102],
  [78, 111, 129, 148, 186, 170, 116, 97],
  [78, 111, 129, 148, 201, 187, 116, 97],
  [78, 111, 129, 169, 191, 177, 142, 123, 102],
  [78, 111, 129, 148, 168, 190, 175, 123, 102],
  [78, 111, 129, 150, 174, 159, 123, 102],
  [78, 111, 152, 176, 160, 142, 123, 102],
  [78, 111, 129, 148, 168, 208, 195, 145, 102],
  [78, 111, 129, 150, 194, 180, 145, 102],
  [78, 111, 129, 169, 209, 197, 164, 145, 102],
  [78, 111, 129, 148, 231, 223, 182, 102],
  [78, 111, 129, 148, 238, 232, 182, 102],
  [78, 111, 152, 196, 181, 164, 145, 102],
  [78, 147, 166, 200, 216, 142, 123, 102],
  [78, 147, 166, 214, 226, 142, 123, 102],
  [78, 147, 166, 200, 228, 164, 145, 102],
  [78, 147, 166, 214, 236, 164, 145, 102],
  [79, 95, 113, 132, 152, 196, 181, 124, 103],
  [79, 95, 113, 132, 179, 163, 124, 103],
  [79, 95, 113, 132, 152, 176, 160, 103],
  [79, 95, 131, 178, 162, 144, 124, 103],
  [79, 95, 131, 150, 194, 180, 163, 124, 103],
  [79, 95, 149, 193, 162, 144, 124, 103],
  [79, 95, 149, 167, 207, 180, 163, 124, 103],
  [79, 95, 168, 186, 220, 210, 124, 103],
  [79, 95, 168, 186, 231, 223, 124, 103]
]
def cycle (r : Fin 2685) := cycles[r.val - 2048]!
theorem checked : ∀ r : Fin 2685,
    2048 ≤ r.val → r.val < 2080 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2048 ≤ r.val) (hhi : r.val < 2080) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02048
