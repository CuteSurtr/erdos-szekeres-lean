import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry02400
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [115, 132, 167, 185, 219, 197, 181, 163, 141],
  [115, 132, 167, 184, 218, 195, 163, 141],
  [115, 132, 167, 184, 247, 239, 163, 141],
  [115, 132, 167, 185, 230, 212, 198, 163, 141],
  [115, 132, 199, 213, 235, 181, 163, 141],
  [115, 132, 199, 224, 241, 181, 163, 141],
  [115, 132, 199, 213, 242, 198, 163, 141],
  [115, 132, 199, 224, 246, 198, 163, 141],
  [115, 133, 151, 170, 210, 181, 163, 141],
  [115, 133, 151, 170, 223, 198, 163, 141],
  [115, 133, 151, 187, 221, 181, 163, 141],
  [115, 133, 151, 187, 232, 198, 163, 141],
  [116, 134, 153, 170, 223, 182, 164, 142],
  [116, 134, 153, 170, 187, 221, 164, 142],
  [116, 152, 169, 186, 231, 223, 182, 164, 142],
  [116, 152, 169, 222, 212, 182, 164, 142],
  [116, 152, 169, 186, 201, 229, 221, 164, 142],
  [116, 152, 169, 186, 220, 210, 164, 142],
  [116, 152, 169, 186, 201, 217, 206, 142],
  [116, 185, 200, 214, 243, 182, 164, 142],
  [116, 185, 200, 214, 247, 182, 164, 142],
  [119, 136, 154, 188, 203, 175, 159, 140],
  [119, 136, 154, 202, 215, 175, 159, 140],
  [119, 136, 154, 188, 216, 192, 177, 140],
  [119, 136, 154, 202, 225, 192, 177, 140],
  [119, 136, 154, 171, 189, 207, 180, 162],
  [119, 136, 154, 171, 204, 219, 197, 162],
  [119, 136, 172, 190, 208, 195, 180, 162],
  [119, 136, 172, 205, 220, 210, 197, 162],
  [120, 137, 155, 172, 205, 192, 160, 141],
  [120, 137, 155, 172, 217, 206, 160, 141],
  [120, 137, 171, 188, 216, 192, 160, 141]
]
def cycle (r : Fin 2685) := cycles[r.val - 2400]!
theorem checked : ∀ r : Fin 2685,
    2400 ≤ r.val → r.val < 2432 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 2400 ≤ r.val) (hhi : r.val < 2432) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry02400
