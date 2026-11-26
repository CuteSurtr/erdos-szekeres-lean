import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02464
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [130, 148, 166, 183, 233, 187, 170, 151],
  [130, 148, 166, 183, 213, 225, 192, 175, 156],
  [130, 148, 166, 183, 199, 215, 175, 156],
  [130, 148, 166, 200, 216, 192, 175, 156],
  [130, 148, 166, 214, 226, 206, 192, 175, 156],
  [130, 148, 166, 183, 199, 227, 195, 156],
  [130, 148, 166, 183, 213, 235, 210, 195, 156],
  [130, 148, 166, 183, 246, 232, 223, 156],
  [130, 148, 166, 183, 248, 232, 223, 156],
  [130, 148, 166, 200, 228, 210, 195, 156],
  [130, 148, 166, 214, 236, 221, 210, 195, 156],
  [130, 148, 201, 217, 206, 192, 175, 156],
  [130, 148, 201, 229, 221, 210, 195, 156],
  [131, 149, 167, 185, 219, 209, 178, 157],
  [131, 149, 167, 185, 230, 222, 178, 157],
  [131, 149, 184, 218, 208, 194, 178, 157],
  [131, 149, 199, 227, 208, 194, 178, 157],
  [131, 149, 184, 200, 216, 205, 191, 157],
  [131, 149, 199, 213, 225, 205, 191, 157],
  [132, 150, 168, 186, 220, 196, 179, 158],
  [132, 150, 168, 186, 231, 211, 179, 158],
  [132, 150, 168, 201, 229, 196, 179, 158],
  [132, 150, 168, 201, 238, 211, 179, 158],
  [132, 167, 184, 200, 216, 205, 176, 158],
  [132, 167, 184, 214, 226, 217, 176, 158],
  [132, 167, 185, 219, 209, 196, 179, 158],
  [132, 167, 185, 230, 222, 211, 179, 158],
  [133, 150, 167, 184, 200, 216, 192, 177, 159],
  [133, 150, 167, 184, 214, 226, 206, 177, 159],
  [133, 150, 167, 199, 213, 225, 192, 177, 159],
  [133, 150, 167, 199, 224, 234, 206, 177, 159],
  [133, 150, 167, 184, 218, 195, 180, 159]
]
def cycle (r : Fin 2685) := cycles[r.val - 2464]!
theorem checked : ∀ r : Fin 2685,
    2464 ≤ r.val → r.val < 2496 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2464 ≤ r.val) (hhi : r.val < 2496) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02464
