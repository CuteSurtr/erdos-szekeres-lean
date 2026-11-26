import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02208
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [94, 111, 129, 148, 186, 170, 134, 115],
  [94, 111, 129, 148, 201, 187, 134, 115],
  [94, 111, 147, 166, 200, 170, 134, 115],
  [94, 111, 147, 166, 214, 187, 134, 115],
  [94, 111, 129, 148, 168, 190, 175, 141, 120],
  [94, 111, 129, 150, 174, 159, 141, 120],
  [94, 111, 129, 169, 191, 177, 160, 141, 120],
  [94, 111, 129, 148, 168, 208, 195, 163, 120],
  [94, 111, 129, 148, 231, 223, 198, 120],
  [94, 111, 129, 148, 238, 232, 198, 120],
  [94, 111, 129, 150, 194, 180, 163, 120],
  [94, 111, 129, 169, 209, 197, 181, 163, 120],
  [94, 111, 147, 167, 189, 159, 141, 120],
  [94, 111, 147, 185, 204, 177, 160, 141, 120],
  [94, 111, 147, 166, 184, 203, 175, 141, 120],
  [94, 111, 183, 213, 225, 160, 141, 120],
  [94, 111, 183, 224, 234, 160, 141, 120],
  [94, 111, 147, 166, 184, 218, 195, 163, 120],
  [94, 111, 147, 167, 207, 180, 163, 120],
  [94, 111, 147, 185, 219, 197, 181, 163, 120],
  [94, 111, 147, 166, 237, 223, 198, 120],
  [94, 111, 147, 166, 243, 232, 198, 120],
  [94, 111, 183, 213, 235, 181, 163, 120],
  [94, 111, 183, 224, 241, 181, 163, 120],
  [94, 112, 130, 170, 192, 160, 141, 120],
  [94, 112, 130, 187, 206, 160, 141, 120],
  [94, 112, 130, 170, 210, 181, 163, 120],
  [94, 112, 130, 187, 221, 181, 163, 120],
  [95, 131, 150, 169, 209, 196, 143, 121],
  [95, 131, 150, 169, 222, 211, 143, 121],
  [95, 149, 167, 207, 194, 179, 143, 121],
  [95, 149, 167, 185, 204, 191, 176, 121]
]
def cycle (r : Fin 2685) := cycles[r.val - 2208]!
theorem checked : ∀ r : Fin 2685,
    2208 ≤ r.val → r.val < 2240 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2208 ≤ r.val) (hhi : r.val < 2240) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02208
