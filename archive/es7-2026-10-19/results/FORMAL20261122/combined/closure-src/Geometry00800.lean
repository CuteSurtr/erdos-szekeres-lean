import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00800
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [95, 149, 167, 185, 219, 209, 196, 143, 121],
  [95, 149, 167, 185, 230, 222, 211, 143, 121],
  [96, 113, 131, 150, 169, 209, 197, 181, 144, 122],
  [96, 113, 131, 150, 169, 222, 212, 198, 144, 122],
  [96, 113, 131, 168, 186, 220, 210, 181, 144, 122],
  [96, 113, 131, 168, 186, 231, 223, 198, 144, 122],
  [96, 113, 131, 150, 169, 191, 177, 160, 122],
  [96, 113, 149, 167, 185, 219, 197, 181, 144, 122],
  [96, 113, 149, 167, 185, 230, 212, 198, 144, 122],
  [96, 113, 149, 184, 200, 228, 210, 181, 144, 122],
  [96, 113, 149, 184, 200, 237, 223, 198, 144, 122],
  [97, 115, 133, 151, 170, 210, 164, 145, 123],
  [97, 115, 133, 151, 187, 221, 164, 145, 123],
  [97, 115, 133, 151, 170, 223, 182, 145, 123],
  [97, 115, 133, 151, 187, 232, 182, 145, 123],
  [97, 132, 150, 168, 201, 217, 206, 142, 123],
  [97, 132, 150, 168, 186, 220, 210, 164, 145, 123],
  [97, 132, 150, 168, 201, 229, 221, 164, 145, 123],
  [97, 132, 150, 168, 186, 231, 223, 182, 145, 123],
  [97, 132, 150, 168, 201, 238, 232, 182, 145, 123],
  [99, 117, 135, 188, 203, 218, 195, 180, 162],
  [99, 117, 135, 202, 215, 227, 195, 180, 162],
  [101, 118, 136, 155, 174, 194, 180, 163, 144],
  [101, 118, 136, 155, 191, 209, 197, 181, 144],
  [101, 118, 136, 172, 190, 208, 195, 163, 144],
  [101, 118, 136, 172, 205, 220, 210, 181, 144],
  [101, 118, 154, 171, 189, 207, 180, 163, 144],
  [101, 118, 154, 188, 203, 218, 195, 163, 144],
  [101, 118, 154, 171, 204, 219, 197, 181, 144],
  [101, 118, 154, 188, 216, 228, 210, 181, 144],
  [102, 137, 155, 172, 205, 220, 210, 164, 145],
  [102, 137, 155, 172, 217, 229, 221, 164, 145]
]
def cycle (r : Fin 2685) := cycles[r.val - 800]!
theorem checked : ∀ r : Fin 2685,
    800 ≤ r.val → r.val < 832 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 800 ≤ r.val) (hhi : r.val < 832) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00800
