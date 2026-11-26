import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02144
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [88, 106, 165, 199, 168, 150, 131, 110],
  [88, 106, 165, 213, 186, 169, 131, 110],
  [88, 106, 126, 167, 189, 174, 157, 136],
  [88, 106, 126, 185, 204, 191, 157, 136],
  [88, 106, 146, 166, 188, 172, 155, 136],
  [88, 106, 165, 183, 202, 172, 155, 136],
  [89, 107, 127, 186, 205, 176, 158, 137],
  [89, 107, 127, 201, 217, 176, 158, 137],
  [89, 126, 146, 200, 186, 152, 132, 111],
  [89, 126, 146, 214, 201, 152, 132, 111],
  [89, 126, 146, 184, 203, 190, 158, 137],
  [89, 126, 185, 204, 191, 176, 158, 137],
  [90, 107, 126, 146, 184, 151, 133, 112],
  [90, 107, 126, 165, 199, 151, 133, 112],
  [90, 107, 127, 186, 170, 153, 133, 112],
  [90, 107, 127, 201, 187, 153, 133, 112],
  [90, 107, 126, 146, 166, 188, 156, 138],
  [90, 107, 126, 146, 184, 203, 175, 159, 138],
  [90, 107, 126, 165, 183, 202, 156, 138],
  [90, 107, 126, 165, 199, 215, 175, 159, 138],
  [90, 107, 126, 185, 204, 177, 159, 138],
  [90, 107, 126, 233, 240, 177, 159, 138],
  [90, 107, 126, 146, 228, 210, 197, 180],
  [90, 107, 126, 146, 236, 221, 197, 180],
  [90, 107, 126, 165, 235, 210, 197, 180],
  [90, 107, 126, 165, 241, 221, 197, 180],
  [90, 107, 127, 168, 190, 175, 159, 138],
  [90, 107, 127, 186, 205, 192, 177, 159, 138],
  [91, 109, 166, 188, 172, 155, 136, 117],
  [91, 109, 183, 202, 172, 155, 136, 117],
  [91, 109, 147, 167, 189, 174, 157, 117],
  [91, 109, 147, 167, 207, 194, 178, 117]
]
def cycle (r : Fin 2685) := cycles[r.val - 2144]!
theorem checked : ∀ r : Fin 2685,
    2144 ≤ r.val → r.val < 2176 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2144 ≤ r.val) (hhi : r.val < 2176) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02144
