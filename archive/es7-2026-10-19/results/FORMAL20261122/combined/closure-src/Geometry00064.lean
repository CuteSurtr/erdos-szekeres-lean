import BalancedProof.Catalog
import ErdosSzekeres.Omission.CycleGeometry
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionBalanced.Geometry00064
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def cycles : Array (List (Fin 252)) := #[
  [23, 31, 42, 73, 94, 78, 48, 35],
  [23, 31, 42, 57, 96, 80, 63, 35],
  [23, 31, 42, 73, 115, 97, 63, 35],
  [23, 31, 55, 72, 93, 62, 48, 35],
  [23, 31, 55, 90, 112, 78, 48, 35],
  [23, 31, 55, 72, 114, 80, 63, 35],
  [23, 31, 55, 90, 133, 97, 63, 35],
  [24, 33, 44, 58, 97, 123, 68, 52],
  [24, 43, 57, 73, 115, 97, 49, 36],
  [24, 43, 57, 73, 134, 116, 49, 36],
  [32, 42, 55, 90, 112, 78, 62, 47],
  [32, 42, 55, 108, 130, 78, 62, 47],
  [32, 42, 55, 90, 133, 97, 80, 47],
  [32, 42, 55, 108, 151, 97, 80, 47],
  [33, 43, 57, 73, 115, 97, 63, 48],
  [33, 43, 57, 73, 134, 116, 63, 48],
  [33, 43, 72, 90, 133, 97, 63, 48],
  [33, 43, 72, 90, 153, 116, 63, 48],
  [44, 57, 72, 90, 133, 97, 80, 62],
  [44, 57, 72, 90, 153, 116, 80, 62],
  [44, 57, 72, 108, 151, 97, 80, 62],
  [44, 57, 72, 108, 170, 116, 80, 62],
  [47, 60, 75, 93, 114, 162, 125, 66],
  [58, 73, 90, 108, 170, 116, 97, 78],
  [58, 73, 90, 108, 187, 116, 97, 78],
  [58, 73, 90, 108, 151, 175, 123, 102],
  [64, 135, 154, 173, 193, 178, 161, 143],
  [78, 94, 112, 130, 151, 175, 123, 102],
  [81, 135, 154, 173, 193, 178, 161, 143],
  [81, 135, 171, 189, 207, 194, 179, 143],
  [98, 135, 171, 189, 207, 194, 179, 161],
  [98, 135, 188, 203, 218, 208, 179, 161]
]
def cycle (r : Fin 2685) := cycles[r.val - 64]!
theorem checked : ∀ r : Fin 2685,
    64 ≤ r.val → r.val < 96 →
    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧
      (cycle r).length - 7 = demand r := by
  decide +kernel
theorem row_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (r : Fin 2685) (hlo : 64 ≤ r.val) (hhi : r.val < 96) :
    demand r ≤ (support r \ c.occupied noCap noCup).card := by
  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi
  simpa only [hs, hd] using
    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid
#print axioms row_bound
end OmissionBalanced.Geometry00064
