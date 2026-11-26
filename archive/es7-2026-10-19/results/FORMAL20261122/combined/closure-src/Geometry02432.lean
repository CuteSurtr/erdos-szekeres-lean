import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02432
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [120, 137, 171, 188, 226, 206, 160, 141],
  [120, 137, 155, 172, 190, 208, 195, 163],
  [120, 137, 155, 191, 209, 197, 181, 163],
  [120, 137, 171, 204, 219, 197, 181, 163],
  [120, 137, 171, 188, 203, 218, 195, 163],
  [122, 139, 157, 174, 194, 180, 163, 144],
  [122, 139, 157, 190, 208, 195, 163, 144],
  [122, 139, 157, 190, 205, 220, 210, 181, 144],
  [122, 139, 173, 189, 207, 180, 163, 144],
  [122, 139, 173, 203, 218, 195, 163, 144],
  [123, 141, 159, 175, 192, 210, 164, 145],
  [123, 141, 159, 175, 206, 221, 164, 145],
  [123, 141, 159, 175, 192, 223, 182, 145],
  [123, 141, 159, 175, 206, 232, 182, 145],
  [123, 158, 174, 191, 209, 197, 164, 145],
  [123, 158, 174, 191, 222, 212, 182, 145],
  [124, 143, 178, 194, 209, 222, 212, 198],
  [125, 161, 178, 194, 209, 222, 212, 182],
  [125, 161, 178, 208, 220, 231, 223, 182],
  [126, 165, 213, 225, 216, 204, 189, 171],
  [126, 165, 224, 234, 226, 204, 189, 171],
  [127, 146, 165, 224, 201, 186, 168, 148],
  [127, 146, 165, 233, 201, 186, 168, 148],
  [127, 146, 165, 213, 225, 205, 190, 172],
  [127, 146, 214, 226, 217, 205, 190, 172],
  [128, 183, 199, 215, 203, 189, 173, 154],
  [128, 183, 213, 225, 216, 204, 173, 154],
  [129, 147, 166, 184, 203, 190, 174, 155],
  [129, 147, 166, 184, 218, 208, 194, 155],
  [129, 147, 183, 199, 215, 190, 174, 155],
  [129, 147, 183, 199, 227, 208, 194, 155],
  [130, 148, 166, 183, 224, 187, 170, 151]
]
def cycle (r : Fin 2685) := cycles[r.val - 2432]!
theorem checked : ∀ r : Fin 2685,
    2432 ≤ r.val → r.val < 2464 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2432 ≤ r.val) (hhi : r.val < 2464) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02432
