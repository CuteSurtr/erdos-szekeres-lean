-- res-slices-fv: dry run of the Final3520 glue with the compact root as a hypothesis (no tree needed).
import RS.Bridge3520
import Res118.Final
open CompactChecker
example (root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) [(0, 2)]) holes) :
    Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 := by
  apply Res118.slice_of_root RS.cat3520_ok
  rw [List.length_append, List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1,
    Res118.rows_lengths.2.2.2]
  exact root
