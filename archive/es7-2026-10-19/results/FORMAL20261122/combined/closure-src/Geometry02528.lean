import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02528
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [138, 155, 171, 188, 203, 218, 195, 180],
  [138, 155, 171, 202, 215, 227, 195, 180],
  [138, 155, 172, 205, 220, 210, 197, 180],
  [138, 155, 172, 217, 229, 221, 197, 180],
  [140, 157, 173, 203, 218, 195, 180, 162],
  [140, 157, 173, 215, 227, 195, 180, 162],
  [140, 157, 173, 189, 204, 219, 197, 162],
  [140, 157, 173, 189, 204, 230, 212, 162],
  [140, 157, 190, 205, 220, 210, 197, 162],
  [140, 157, 190, 205, 231, 223, 212, 162],
  [141, 158, 174, 190, 217, 229, 221, 181, 163],
  [141, 158, 174, 191, 209, 197, 181, 163],
  [141, 158, 174, 191, 222, 212, 198, 163],
  [141, 158, 189, 204, 219, 197, 181, 163],
  [141, 158, 189, 204, 230, 212, 198, 163],
  [142, 160, 177, 192, 206, 232, 182, 164],
  [142, 160, 177, 192, 206, 239, 182, 164],
  [142, 176, 191, 205, 231, 223, 182, 164],
  [142, 176, 191, 205, 217, 229, 221, 164],
  [144, 161, 178, 194, 209, 222, 212, 198],
  [144, 161, 178, 208, 220, 231, 223, 198],
  [145, 179, 194, 208, 220, 231, 223, 182],
  [145, 179, 194, 208, 229, 238, 232, 182],
  [146, 165, 224, 234, 226, 216, 203, 188],
  [146, 165, 233, 240, 226, 216, 203, 188],
  [147, 183, 213, 225, 216, 204, 189, 171],
  [147, 183, 224, 234, 226, 204, 189, 171],
  [147, 183, 224, 241, 236, 219, 207, 171],
  [148, 166, 183, 213, 225, 205, 190, 172],
  [148, 166, 183, 213, 235, 220, 208, 172],
  [148, 166, 214, 226, 217, 205, 190, 172],
  [148, 166, 214, 236, 229, 220, 208, 172]
]
def cycle (r : Fin 2685) := cycles[r.val - 2528]!
theorem checked : ∀ r : Fin 2685,
    2528 ≤ r.val → r.val < 2560 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2528 ≤ r.val) (hhi : r.val < 2560) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02528
