import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00928
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [132, 167, 184, 214, 243, 238, 211, 179, 158],
  [133, 150, 167, 184, 214, 236, 221, 197, 180, 159],
  [133, 150, 167, 184, 200, 237, 223, 212, 180, 159],
  [133, 150, 167, 184, 214, 243, 232, 212, 180, 159],
  [133, 150, 167, 199, 213, 235, 210, 197, 180, 159],
  [133, 150, 167, 199, 224, 241, 221, 197, 180, 159],
  [133, 150, 167, 199, 213, 242, 223, 212, 180, 159],
  [133, 150, 167, 199, 224, 246, 232, 212, 180, 159],
  [134, 152, 169, 186, 201, 238, 232, 198, 181, 160],
  [134, 152, 169, 186, 201, 244, 239, 198, 181, 160],
  [134, 152, 185, 200, 214, 243, 232, 198, 181, 160],
  [134, 152, 185, 200, 214, 247, 239, 198, 181, 160],
  [138, 155, 171, 188, 216, 228, 210, 197, 180],
  [138, 155, 171, 188, 226, 236, 221, 197, 180],
  [138, 155, 171, 202, 225, 235, 210, 197, 180],
  [138, 155, 171, 202, 234, 241, 221, 197, 180],
  [140, 157, 173, 203, 216, 228, 210, 197, 162],
  [140, 157, 173, 215, 225, 235, 210, 197, 162],
  [140, 157, 173, 203, 216, 237, 223, 212, 162],
  [140, 157, 173, 215, 225, 242, 223, 212, 162],
  [141, 158, 174, 190, 205, 220, 210, 181, 163],
  [141, 158, 174, 190, 205, 231, 223, 198, 163],
  [141, 158, 174, 190, 217, 238, 232, 198, 163],
  [141, 158, 189, 203, 216, 228, 210, 181, 163],
  [141, 158, 189, 203, 226, 236, 221, 181, 163],
  [141, 158, 189, 203, 216, 237, 223, 198, 163],
  [141, 158, 189, 203, 226, 243, 232, 198, 163],
  [142, 176, 191, 205, 217, 238, 232, 182, 164],
  [142, 176, 191, 205, 217, 244, 239, 182, 164],
  [148, 166, 183, 224, 234, 217, 205, 190, 172],
  [148, 166, 183, 233, 240, 217, 205, 190, 172],
  [148, 166, 183, 224, 241, 229, 220, 208, 172]
]
def cycle (r : Fin 2685) := cycles[r.val - 928]!
theorem checked : ∀ r : Fin 2685,
    928 ≤ r.val → r.val < 960 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 928 ≤ r.val) (hhi : r.val < 960) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00928
