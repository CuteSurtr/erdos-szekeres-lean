import ErdosSzekeres.Omission.BlockGeometry

/-! Additional residual constraints found by finite search on 10 October 2026.
The state catalog and geometric methods follow Schroeder, DOI 10.5281/zenodo.22842891.
Each literal candidate is rechecked in Lean; the search programs are not trusted.
These lemmas do not assert a stronger residual population or global bound. -/

namespace ErdosSzekeres.Omission.AdditionalResidualRows
open BlockCompression

set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def cycles : Array (List (Fin 154)) := #[
  [3, 12, 20, 30, 43, 33, 25, 17],
  [6, 20, 27, 39, 53, 44, 34, 17],
  [10, 20, 27, 39, 53, 44, 34, 25],
  [10, 20, 36, 49, 64, 54, 34, 25],
  [14, 20, 46, 59, 74, 54, 44, 33],
  [17, 33, 44, 55, 67, 79, 101, 91],
  [25, 33, 54, 66, 78, 90, 111, 91],
  [34, 44, 54, 66, 78, 90, 111, 91],
  [34, 44, 54, 76, 88, 100, 119, 91],
  [38, 47, 58, 83, 97, 88, 78, 66],
  [45, 55, 66, 76, 88, 100, 119, 91],
  [45, 55, 66, 76, 98, 109, 127, 91],
  [45, 65, 75, 87, 99, 118, 111, 91],
  [56, 67, 78, 88, 98, 109, 127, 91],
  [56, 67, 78, 88, 98, 117, 133, 91],
  [98, 106, 114, 121, 135, 146, 133, 127],
  [100, 108, 115, 122, 134, 145, 127, 119],
  [109, 116, 123, 129, 135, 146, 133, 127],
  [109, 116, 123, 129, 135, 149, 139, 127],
  [117, 124, 130, 135, 140, 151, 139, 133]
]

def cycle (i : Fin 20) : List (Fin 154) := cycles[i.val]!

theorem cycles_checked : ∀ i : Fin 20,
    ResidualCycleValid (cycle i) ∧ (cycle i).length = 8 := by
  decide +kernel

def extraBlock : Block :=
  { rowId := 1187, support := [17, 25, 33, 34, 44, 45, 54, 55, 56, 66, 67, 68, 76, 78, 79, 88, 90, 91, 98, 100, 101, 109, 111, 117, 119, 127, 133, 139],
    thresholds := [2, 2, 2, 2, 2, 2],
    active := [(2, 1), (3, 1), (2, 2), (3, 2), (2, 3), (3, 3), (2, 4), (3, 4), (2, 5), (3, 5), (1, 6), (2, 6), (3, 6)] }

def blockSupport : Finset (Fin 154) :=
  {17, 25, 33, 34, 44, 45, 54, 55, 56, 66, 67, 68, 76, 78, 79, 88, 90, 91, 98, 100, 101, 109, 111, 117, 119, 127, 133, 139}

theorem block_checked : pairsOK extraBlock = true ∧ growthOK extraBlock = true ∧
    extraBlock.support.toFinset = blockSupport.image Fin.val ∧ blockSupport.card = 28 := by
  decide +kernel

theorem cycle_hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (i : Fin 20) :
    1 ≤ ((cycle i).toFinset \ c.residualOccupied noCap noOctagon noJunction).card := by
  have bound := c.residual_list_cycle_hole_bound noCap noOctagon noJunction
    (cycle i) (cycles_checked i).1
  simpa only [(cycles_checked i).2] using bound

theorem block_hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    6 ≤ (blockSupport \ c.residualOccupied noCap noOctagon noJunction).card := by
  obtain ⟨pairs, growth, support, size⟩ := block_checked
  have bound := BlockGeometry.block_hole_bound c noCap noOctagon noJunction
    extraBlock pairs growth blockSupport support
  simpa only [size] using bound

def support (i : Fin 21) : Finset (Fin 154) :=
  if h : i.val < 20 then (cycle ⟨i.val, h⟩).toFinset else blockSupport

def demand (i : Fin 21) : ℕ := if i.val < 20 then 1 else 6

theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (i : Fin 21) :
    demand i ≤ (support i \ c.residualOccupied noCap noOctagon noJunction).card := by
  by_cases h : i.val < 20
  · simpa only [support, demand, h, dif_pos, if_pos] using
      cycle_hole_bound c noCap noOctagon noJunction ⟨i.val, h⟩
  · simpa only [support, demand, h, dif_neg, if_neg] using
      block_hole_bound c noCap noOctagon noJunction

end ErdosSzekeres.Omission.AdditionalResidualRows
