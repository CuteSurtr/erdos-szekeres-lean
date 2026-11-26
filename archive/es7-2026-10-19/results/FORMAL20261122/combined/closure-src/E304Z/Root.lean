import E304Z.S3_0
import E304Z.S3_1
import E304Z.S3_2
import E304Z.S3_3
import E304Z.S3_4
import E304Z.S3_5
import E304Z.S3_6
import E304Z.S3_7
import CompactChecker.Path
open CompactChecker
set_option maxRecDepth 100000
set_option Elab.async false
set_option linter.all false
namespace E304Z
-- FV304 (20 Nov 2026): joins of the ES(8) <= 304 compact check (budget-67 Z-row tree); Lean checks each step
theorem t2_0 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) [(214, 2), (0, 2)]) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [(214, 2), (0, 2)] 232 E304Z.S3_0.root E304Z.S3_1.root
theorem t2_1 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) [(214, 1), (0, 2)]) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [(214, 1), (0, 2)] 232 E304Z.S3_2.root E304Z.S3_3.root
theorem t2_2 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) [(214, 2), (0, 1)]) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [(214, 2), (0, 1)] 85 E304Z.S3_4.root E304Z.S3_5.root
theorem t2_3 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) [(214, 1), (0, 1)]) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [(214, 1), (0, 1)] 85 E304Z.S3_6.root E304Z.S3_7.root
theorem t1_0 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) [(0, 2)]) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [(0, 2)] 214 t2_0 t2_1
theorem t1_1 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) [(0, 1)]) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [(0, 1)] 214 t2_2 t2_3
theorem t0_0 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) []) holes :=
  split_pm fcatZ 3132 252 67 (zerosF 252) [] 0 t1_0 t1_1
theorem root : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) []) holes := t0_0
#print axioms root
end E304Z
