-- res-slices-fv: dry run of the Final3419 glue with the compact root as a hypothesis (no tree needed).
import RS.Bridge3419
import Res118.Final
open CompactChecker
example (root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3419 3464 154 34 (pmask (zerosF 154) [(0, 2)]) holes) :
    Res118.ResSliceExcludes Res118.rowsP 34 19 := by
  apply Res118.slice_of_root RS.cat3419_ok
  rw [Res118.rows_lengths.1]
  exact root
