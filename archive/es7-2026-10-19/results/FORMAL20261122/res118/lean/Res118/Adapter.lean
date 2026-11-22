/-
res118-lean (22 November 2026): the compact-checker form of a residual slice exclusion.

Mirror of `CompactChecker.Bridge311Res.residual_of_root` (the budget-32 residual adapter of the ES(8) ≤ 311/310
compact recheck) and of FV304's `BridgeZ.balanced_z_of_root`: the root exclusion of a compact export of a slice
tree, over any catalog `cat` numbered like the slice's rows.txt (base rows 0..2649, capacity rows 2650 = (F, T)
and 2651 = (Lo, B − T), unit rows 2652 + j), with state 0 fixed occupied at the root (mask `[(0, 2)]`), gives
`ResSliceExcludes rows B T`. The catalog identities are the fields of `SliceCatalog`; a later run proves them for
its own catalog (as Bridge311Res does for `fcat2650` by `decide +kernel`).
-/
import CompactChecker.Path
import Res118.Glue

open scoped BigOperators
open ErdosSzekeres.OmissionCertificates CompactChecker OmissionResidual32Bridge2650

namespace Res118

/-- A compact-checker catalog in the row numbering of a slice tree. -/
structure SliceCatalog (cat : FCat) (rows : List (List ℕ)) (B T : ℕ) : Prop where
  base_supp : ∀ r : Fin 2650, fsupp cat 154 r.val = support2650 r
  base_dem : ∀ r : Fin 2650, cat.dem r.val = demand2650 r
  f_supp : fsupp cat 154 2650 = F
  f_dem : cat.dem 2650 = T
  lo_supp : fsupp cat 154 2651 = Lo
  lo_dem : cat.dem 2651 = B - T
  unit_supp : ∀ j (hj : j < rows.length), (cat.get (2652 + j)).1 = rows[j]
  unit_dem : ∀ j, j < rows.length → cat.dem (2652 + j) = 1

/-- The compact-checker root exclusion of a slice tree gives the slice statement. -/
theorem slice_of_root {cat : FCat} {rows : List (List ℕ)} {B T : ℕ} (hc : SliceCatalog cat rows B T)
    (h : ¬ ∃ holes : Fin 154 → ℕ,
      FFeas cat (2652 + rows.length) 154 B (pmask (zerosF 154) [(0, 2)]) holes) :
    ResSliceExcludes rows B T := by
  rintro ⟨holes, hb, h0, hr, hT, hL, hx, hB⟩
  refine h ⟨holes, hb, fun r => ?_, hB, fun i hi => ?_, fun i hi => ?_⟩
  · obtain ⟨r, hr'⟩ := r
    show cat.dem r ≤ ∑ i ∈ fsupp cat 154 r, holes i
    by_cases h1 : r < 2650
    · rw [hc.base_supp ⟨r, h1⟩, hc.base_dem ⟨r, h1⟩]
      exact hr ⟨r, h1⟩
    by_cases h2 : r = 2650
    · subst h2
      rw [hc.f_supp, hc.f_dem]
      exact hT
    by_cases h3 : r = 2651
    · subst h3
      rw [hc.lo_supp, hc.lo_dem]
      exact hL
    obtain ⟨j, rfl⟩ : ∃ j, r = 2652 + j := ⟨r - 2652, by omega⟩
    have hj : j < rows.length := by omega
    have hs : fsupp cat 154 (2652 + j) = lsupp rows[j] := by
      unfold fsupp lsupp
      rw [hc.unit_supp j hj]
    rw [hs, hc.unit_dem j hj]
    exact hx _ (List.getElem_mem hj)
  · rcases mem_mset_zero_occupied 1 i hi with h1 | h1 <;> omega
  · rcases mem_mset_zero_occupied 2 i hi with h1 | h1
    · have : i = 0 := Fin.ext h1.1
      rw [this]
      exact h0
    · omega

end Res118

#print axioms Res118.slice_of_root
