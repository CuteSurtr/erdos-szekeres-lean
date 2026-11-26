import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02496
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [133, 150, 167, 184, 200, 228, 210, 197, 180, 159],
  [133, 150, 167, 184, 247, 239, 180, 159],
  [133, 150, 167, 185, 219, 197, 180, 159],
  [133, 150, 167, 185, 230, 212, 180, 159],
  [133, 150, 167, 199, 227, 195, 180, 159],
  [133, 150, 167, 233, 245, 197, 180, 159],
  [133, 150, 167, 199, 249, 239, 180, 159],
  [133, 150, 167, 233, 248, 212, 180, 159],
  [133, 150, 168, 186, 205, 192, 177, 159],
  [133, 150, 168, 201, 217, 206, 177, 159],
  [133, 150, 168, 186, 220, 210, 197, 180, 159],
  [133, 150, 168, 186, 231, 223, 212, 180, 159],
  [133, 150, 168, 201, 229, 221, 197, 180, 159],
  [133, 150, 168, 201, 238, 232, 212, 180, 159],
  [134, 152, 169, 186, 231, 223, 198, 181, 160],
  [134, 152, 169, 186, 201, 229, 221, 181, 160],
  [134, 152, 169, 186, 220, 210, 181, 160],
  [134, 152, 169, 222, 212, 198, 181, 160],
  [134, 152, 169, 186, 201, 217, 206, 160],
  [134, 152, 185, 200, 237, 223, 198, 181, 160],
  [134, 152, 185, 230, 212, 198, 181, 160],
  [134, 152, 185, 200, 228, 210, 181, 160],
  [134, 152, 185, 200, 214, 236, 221, 181, 160],
  [134, 152, 213, 224, 246, 198, 181, 160],
  [134, 152, 213, 224, 249, 198, 181, 160],
  [134, 152, 185, 200, 214, 226, 206, 160],
  [134, 153, 170, 187, 232, 198, 181, 160],
  [134, 153, 170, 187, 239, 198, 181, 160],
  [138, 155, 171, 188, 216, 192, 177, 159],
  [138, 155, 171, 188, 226, 206, 177, 159],
  [138, 155, 171, 202, 225, 192, 177, 159],
  [138, 155, 171, 202, 234, 206, 177, 159]
]
def cycle (r : Fin 2685) := cycles[r.val - 2496]!
theorem checked : ∀ r : Fin 2685,
    2496 ≤ r.val → r.val < 2528 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2496 ≤ r.val) (hhi : r.val < 2528) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02496
