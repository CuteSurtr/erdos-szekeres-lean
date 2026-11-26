import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry01632
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [46, 59, 109, 185, 204, 177, 160, 65],
  [46, 59, 109, 185, 219, 197, 181, 65],
  [46, 59, 148, 168, 208, 195, 124, 65],
  [46, 59, 166, 184, 218, 195, 124, 65],
  [46, 59, 91, 110, 131, 114, 96, 79],
  [46, 59, 91, 129, 150, 133, 115, 79],
  [46, 59, 109, 128, 149, 114, 96, 79],
  [46, 59, 109, 147, 167, 133, 115, 79],
  [46, 75, 93, 114, 140, 122, 103, 65],
  [46, 75, 93, 114, 162, 144, 124, 65],
  [46, 75, 112, 133, 159, 141, 103, 65],
  [46, 75, 112, 133, 180, 163, 124, 65],
  [47, 60, 75, 112, 138, 102, 84, 66],
  [47, 60, 75, 130, 156, 102, 84, 66],
  [47, 60, 75, 93, 114, 140, 104, 66],
  [47, 60, 94, 115, 141, 123, 104, 66],
  [47, 60, 94, 115, 163, 145, 125, 66],
  [47, 74, 91, 129, 155, 138, 102, 84, 66],
  [47, 74, 91, 148, 172, 156, 102, 84, 66],
  [47, 74, 91, 110, 136, 119, 84, 66],
  [47, 74, 111, 137, 120, 102, 84, 66],
  [47, 74, 91, 110, 131, 157, 140, 104, 66],
  [47, 74, 91, 110, 131, 178, 162, 125, 66],
  [47, 74, 91, 169, 191, 177, 142, 66],
  [47, 74, 91, 186, 205, 192, 142, 66],
  [47, 74, 91, 169, 209, 197, 164, 66],
  [47, 74, 91, 186, 220, 210, 164, 66],
  [47, 74, 92, 113, 139, 122, 104, 66],
  [47, 74, 92, 113, 161, 144, 125, 66],
  [47, 74, 111, 132, 158, 141, 123, 104, 66],
  [47, 74, 111, 132, 179, 163, 145, 125, 66],
  [47, 109, 147, 167, 189, 123, 104, 66]
]
def cycle (r : Fin 2685) := cycles[r.val - 1632]!
theorem checked : ∀ r : Fin 2685,
    1632 ≤ r.val → r.val < 1664 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 1632 ≤ r.val) (hhi : r.val < 1664) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry01632
