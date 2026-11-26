import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02176
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [92, 110, 129, 150, 174, 158, 139, 118],
  [92, 110, 129, 169, 191, 176, 139, 118],
  [92, 110, 129, 150, 194, 179, 161, 118],
  [92, 110, 129, 169, 209, 196, 161, 118],
  [92, 110, 148, 168, 190, 158, 139, 118],
  [92, 110, 148, 186, 205, 176, 139, 118],
  [92, 110, 148, 168, 208, 179, 161, 118],
  [92, 110, 148, 186, 220, 196, 161, 118],
  [93, 110, 128, 166, 184, 151, 133, 114],
  [93, 110, 128, 183, 199, 151, 133, 114],
  [93, 110, 128, 166, 200, 170, 153, 114],
  [93, 110, 128, 183, 213, 170, 153, 114],
  [93, 110, 128, 166, 188, 156, 138, 119],
  [93, 110, 128, 183, 202, 156, 138, 119],
  [93, 110, 128, 147, 167, 189, 159, 140, 119],
  [93, 110, 128, 147, 185, 204, 177, 140, 119],
  [93, 110, 128, 214, 226, 206, 140, 119],
  [93, 110, 128, 224, 234, 206, 140, 119],
  [93, 110, 128, 147, 167, 207, 180, 162, 119],
  [93, 110, 128, 147, 185, 219, 197, 162, 119],
  [93, 110, 128, 214, 236, 221, 162, 119],
  [93, 110, 128, 224, 241, 221, 162, 119],
  [93, 110, 128, 166, 237, 223, 212, 119],
  [93, 110, 128, 183, 242, 223, 212, 119],
  [93, 110, 129, 150, 174, 159, 140, 119],
  [93, 110, 129, 169, 191, 177, 140, 119],
  [93, 110, 129, 150, 194, 180, 162, 119],
  [93, 110, 129, 169, 209, 197, 162, 119],
  [93, 110, 148, 168, 190, 175, 159, 140, 119],
  [93, 110, 148, 186, 205, 192, 177, 140, 119],
  [93, 110, 148, 168, 208, 195, 180, 162, 119],
  [93, 110, 148, 186, 220, 210, 197, 162, 119]
]
def cycle (r : Fin 2685) := cycles[r.val - 2176]!
theorem checked : ∀ r : Fin 2685,
    2176 ≤ r.val → r.val < 2208 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2176 ≤ r.val) (hhi : r.val < 2208) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02176
