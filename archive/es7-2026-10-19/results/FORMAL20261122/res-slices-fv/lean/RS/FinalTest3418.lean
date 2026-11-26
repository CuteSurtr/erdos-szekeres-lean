-- res-slices-fv: dry run of the Final3418 glue with the compact root as a hypothesis (no tree needed).
import RS.Bridge3418
import Res118.Final
open CompactChecker
example (root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3418 3672 154 34 (pmask (zerosF 154) [(0, 2)]) holes) :
    Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18 := by
  apply Res118.slice_of_root RS.cat3418_ok
  rw [List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1]
  exact root
