import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00896
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [122, 139, 157, 174, 191, 209, 197, 181, 144],
  [122, 139, 157, 174, 191, 222, 212, 198, 144],
  [122, 139, 157, 190, 205, 231, 223, 198, 144],
  [122, 139, 173, 189, 204, 219, 197, 181, 144],
  [122, 139, 173, 203, 216, 228, 210, 181, 144],
  [122, 139, 173, 189, 204, 230, 212, 198, 144],
  [122, 139, 173, 203, 216, 237, 223, 198, 144],
  [123, 158, 174, 190, 205, 220, 210, 164, 145],
  [123, 158, 174, 190, 217, 229, 221, 164, 145],
  [123, 158, 174, 190, 205, 231, 223, 182, 145],
  [123, 158, 174, 190, 217, 238, 232, 182, 145],
  [127, 146, 165, 224, 234, 217, 205, 190, 172],
  [127, 146, 165, 233, 240, 217, 205, 190, 172],
  [129, 147, 166, 200, 216, 205, 191, 174, 155],
  [129, 147, 166, 214, 226, 217, 191, 174, 155],
  [129, 147, 166, 200, 228, 220, 209, 194, 155],
  [129, 147, 166, 214, 236, 229, 209, 194, 155],
  [129, 147, 183, 213, 225, 205, 191, 174, 155],
  [129, 147, 183, 224, 234, 217, 191, 174, 155],
  [129, 147, 183, 213, 235, 220, 209, 194, 155],
  [129, 147, 183, 224, 241, 229, 209, 194, 155],
  [130, 148, 166, 183, 224, 234, 206, 192, 175, 156],
  [130, 148, 166, 183, 233, 240, 206, 192, 175, 156],
  [130, 148, 166, 183, 224, 241, 221, 210, 195, 156],
  [130, 148, 166, 183, 233, 245, 221, 210, 195, 156],
  [131, 149, 184, 200, 228, 220, 209, 178, 157],
  [131, 149, 184, 200, 237, 231, 222, 178, 157],
  [131, 149, 199, 213, 235, 220, 209, 178, 157],
  [131, 149, 199, 213, 242, 231, 222, 178, 157],
  [132, 167, 184, 200, 228, 220, 196, 179, 158],
  [132, 167, 184, 214, 236, 229, 196, 179, 158],
  [132, 167, 184, 200, 237, 231, 211, 179, 158]
]
def cycle (r : Fin 2685) := cycles[r.val - 896]!
theorem checked : ∀ r : Fin 2685,
    896 ≤ r.val → r.val < 928 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 896 ≤ r.val) (hhi : r.val < 928) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00896
