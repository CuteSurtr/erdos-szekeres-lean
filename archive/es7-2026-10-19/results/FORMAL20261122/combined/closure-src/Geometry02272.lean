import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02272
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [97, 132, 150, 169, 222, 212, 182, 145, 123],
  [97, 132, 152, 196, 181, 164, 145, 123],
  [97, 132, 152, 211, 198, 182, 145, 123],
  [97, 167, 184, 200, 228, 164, 145, 123],
  [97, 167, 184, 214, 236, 164, 145, 123],
  [97, 167, 184, 200, 237, 182, 145, 123],
  [97, 167, 184, 214, 243, 182, 145, 123],
  [99, 117, 135, 188, 203, 175, 159, 140],
  [99, 117, 135, 202, 215, 175, 159, 140],
  [99, 117, 172, 190, 208, 195, 180, 162],
  [101, 118, 136, 155, 174, 159, 141, 122],
  [101, 118, 136, 172, 190, 175, 141, 122],
  [101, 118, 136, 155, 191, 177, 160, 122],
  [101, 118, 136, 172, 205, 192, 160, 122],
  [101, 118, 154, 171, 189, 159, 141, 122],
  [101, 118, 154, 188, 203, 175, 141, 122],
  [101, 118, 154, 171, 204, 177, 160, 122],
  [101, 118, 154, 188, 216, 192, 160, 122],
  [102, 120, 138, 156, 192, 210, 164, 145],
  [102, 120, 138, 156, 206, 221, 164, 145],
  [102, 137, 155, 172, 205, 192, 142, 123],
  [102, 137, 155, 172, 217, 206, 142, 123],
  [102, 137, 155, 191, 209, 197, 164, 145],
  [102, 137, 155, 172, 190, 208, 195, 145],
  [103, 121, 139, 158, 176, 196, 181, 124],
  [103, 121, 139, 158, 176, 211, 198, 124],
  [103, 121, 157, 174, 194, 180, 163, 124],
  [103, 121, 173, 189, 207, 180, 163, 124],
  [104, 122, 140, 159, 177, 197, 164, 125],
  [104, 122, 140, 159, 177, 212, 182, 125],
  [104, 122, 140, 175, 192, 210, 164, 125],
  [104, 122, 140, 175, 192, 223, 182, 125]
]
def cycle (r : Fin 2685) := cycles[r.val - 2272]!
theorem checked : ∀ r : Fin 2685,
    2272 ≤ r.val → r.val < 2304 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2272 ≤ r.val) (hhi : r.val < 2304) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02272
