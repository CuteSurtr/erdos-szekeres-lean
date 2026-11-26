import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01920
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [68, 121, 139, 158, 179, 163, 145, 86],
  [69, 165, 183, 202, 188, 171, 154, 135],
  [70, 87, 146, 166, 148, 129, 110, 91],
  [70, 87, 165, 183, 148, 129, 110, 91],
  [70, 87, 146, 184, 168, 150, 131, 91],
  [70, 87, 165, 199, 168, 150, 131, 91],
  [70, 87, 126, 147, 171, 155, 136, 117],
  [70, 87, 126, 167, 189, 174, 157, 117],
  [71, 88, 107, 150, 174, 158, 139, 118],
  [71, 88, 107, 169, 191, 176, 139, 118],
  [71, 88, 127, 168, 190, 158, 139, 118],
  [71, 88, 127, 186, 205, 176, 139, 118],
  [71, 106, 126, 167, 150, 132, 113, 92],
  [71, 106, 126, 185, 169, 152, 113, 92],
  [71, 106, 146, 184, 168, 132, 113, 92],
  [71, 106, 146, 200, 186, 152, 113, 92],
  [71, 106, 126, 147, 171, 155, 137, 118],
  [71, 106, 146, 166, 188, 172, 137, 118],
  [72, 88, 106, 146, 166, 130, 112, 93],
  [72, 88, 106, 165, 183, 130, 112, 93],
  [72, 88, 106, 126, 167, 133, 114, 93],
  [72, 88, 106, 126, 185, 153, 114, 93],
  [72, 88, 127, 168, 151, 133, 114, 93],
  [72, 88, 127, 186, 170, 153, 114, 93],
  [72, 88, 106, 126, 147, 171, 138, 119],
  [72, 88, 106, 126, 167, 189, 159, 140, 119],
  [72, 88, 106, 126, 185, 204, 177, 140, 119],
  [72, 88, 106, 146, 166, 188, 156, 138, 119],
  [72, 88, 106, 165, 183, 202, 156, 138, 119],
  [72, 88, 106, 214, 226, 206, 140, 119],
  [72, 88, 106, 224, 234, 206, 140, 119],
  [72, 88, 106, 146, 218, 195, 180, 162]
]
def cycle (r : Fin 2685) := cycles[r.val - 1920]!
theorem checked : ∀ r : Fin 2685,
    1920 ≤ r.val → r.val < 1952 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1920 ≤ r.val) (hhi : r.val < 1952) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01920
