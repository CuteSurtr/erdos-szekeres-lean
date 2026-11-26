import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00736
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [80, 96, 114, 151, 170, 223, 182, 125, 104],
  [80, 113, 131, 150, 169, 209, 197, 164, 125, 104],
  [80, 113, 131, 150, 169, 222, 212, 182, 125, 104],
  [80, 113, 131, 168, 186, 220, 210, 164, 125, 104],
  [80, 113, 131, 168, 186, 231, 223, 182, 125, 104],
  [82, 98, 117, 155, 174, 194, 180, 163, 144],
  [82, 98, 117, 172, 190, 208, 195, 163, 144],
  [82, 98, 135, 171, 189, 207, 180, 163, 144],
  [82, 98, 135, 188, 203, 218, 195, 163, 144],
  [83, 100, 136, 155, 174, 194, 180, 163, 124],
  [83, 100, 136, 155, 191, 209, 197, 181, 124],
  [83, 100, 154, 171, 189, 207, 180, 163, 124],
  [83, 100, 154, 171, 204, 219, 197, 181, 124],
  [84, 118, 136, 155, 174, 194, 180, 145, 125],
  [84, 118, 136, 172, 190, 208, 195, 145, 125],
  [84, 118, 136, 155, 191, 209, 197, 164, 125],
  [84, 118, 136, 172, 205, 220, 210, 164, 125],
  [85, 121, 139, 158, 176, 196, 181, 164, 105],
  [85, 121, 139, 158, 176, 211, 198, 182, 105],
  [85, 121, 157, 174, 191, 209, 197, 164, 105],
  [85, 121, 157, 174, 191, 222, 212, 182, 105],
  [88, 106, 146, 184, 203, 190, 174, 157, 136],
  [88, 106, 146, 200, 216, 205, 191, 157, 136],
  [88, 106, 165, 199, 215, 190, 174, 157, 136],
  [88, 106, 165, 213, 225, 205, 191, 157, 136],
  [89, 126, 146, 200, 216, 205, 176, 158, 137],
  [89, 126, 146, 214, 226, 217, 176, 158, 137],
  [90, 107, 126, 146, 200, 170, 153, 133, 112],
  [90, 107, 126, 146, 214, 187, 153, 133, 112],
  [90, 107, 126, 165, 213, 170, 153, 133, 112],
  [90, 107, 126, 165, 224, 187, 153, 133, 112],
  [90, 107, 126, 146, 200, 216, 192, 177, 159, 138]
]
def cycle (r : Fin 2685) := cycles[r.val - 736]!
theorem checked : ∀ r : Fin 2685,
    736 ≤ r.val → r.val < 768 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 736 ≤ r.val) (hhi : r.val < 768) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00736
