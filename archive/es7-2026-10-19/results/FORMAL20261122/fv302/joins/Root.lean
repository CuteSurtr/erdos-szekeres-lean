import E302ZZ.S_00000
import E302ZZ.S_00001
import E302ZZ.S_00010
import E302ZZ.S_00011
import E302ZZ.S_00100
import E302ZZ.S_00101
import E302ZZ.S_00110
import E302ZZ.S_00111
import E302ZZ.S_01000
import E302ZZ.S_01001
import E302ZZ.S_01010
import E302ZZ.S_01011
import E302ZZ.S_01100
import E302ZZ.S_01101
import E302ZZ.S_01110
import E302ZZ.S_01111
import E302ZZ.S_10000
import E302ZZ.S_10001
import E302ZZ.S_10010
import E302ZZ.S_10011
import E302ZZ.S_10100
import E302ZZ.S_10101
import E302ZZ.S_10110
import E302ZZ.S_10111
import E302ZZ.S_11000
import E302ZZ.S_11001
import E302ZZ.S_11010
import E302ZZ.S_11011
import E302ZZ.S_11100
import E302ZZ.S_11101
import E302ZZ.S_11110
import E302ZZ.S_11111
import CompactChecker.Path
open CompactChecker
set_option maxRecDepth 100000
set_option Elab.async false
set_option linter.all false
namespace E302ZZ
-- FV302 (24 Nov 2026): joins of the ES(8) <= 302 compact check (budget-69 Z/Z*-row tree); Lean checks each step
theorem t_0000 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(102, 2), (25, 2), (233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(102, 2), (25, 2), (233, 2), (122, 2), (0, 2)] 192 E302ZZ.S_00000.root E302ZZ.S_00001.root
theorem t_0001 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(102, 1), (25, 2), (233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(102, 1), (25, 2), (233, 2), (122, 2), (0, 2)] 169 E302ZZ.S_00010.root E302ZZ.S_00011.root
theorem t_0010 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(75, 2), (25, 1), (233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(75, 2), (25, 1), (233, 2), (122, 2), (0, 2)] 109 E302ZZ.S_00100.root E302ZZ.S_00101.root
theorem t_0011 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(75, 1), (25, 1), (233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(75, 1), (25, 1), (233, 2), (122, 2), (0, 2)] 231 E302ZZ.S_00110.root E302ZZ.S_00111.root
theorem t_0100 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(149, 2), (200, 2), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(149, 2), (200, 2), (233, 1), (122, 2), (0, 2)] 152 E302ZZ.S_01000.root E302ZZ.S_01001.root
theorem t_0101 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(149, 1), (200, 2), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(149, 1), (200, 2), (233, 1), (122, 2), (0, 2)] 152 E302ZZ.S_01010.root E302ZZ.S_01011.root
theorem t_0110 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(79, 2), (200, 1), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(79, 2), (200, 1), (233, 1), (122, 2), (0, 2)] 152 E302ZZ.S_01100.root E302ZZ.S_01101.root
theorem t_0111 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(79, 1), (200, 1), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(79, 1), (200, 1), (233, 1), (122, 2), (0, 2)] 152 E302ZZ.S_01110.root E302ZZ.S_01111.root
theorem t_1000 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(97, 2), (137, 2), (61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(97, 2), (137, 2), (61, 2), (122, 1), (0, 2)] 152 E302ZZ.S_10000.root E302ZZ.S_10001.root
theorem t_1001 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(97, 1), (137, 2), (61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(97, 1), (137, 2), (61, 2), (122, 1), (0, 2)] 152 E302ZZ.S_10010.root E302ZZ.S_10011.root
theorem t_1010 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(233, 2), (137, 1), (61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(233, 2), (137, 1), (61, 2), (122, 1), (0, 2)] 152 E302ZZ.S_10100.root E302ZZ.S_10101.root
theorem t_1011 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(233, 1), (137, 1), (61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(233, 1), (137, 1), (61, 2), (122, 1), (0, 2)] 152 E302ZZ.S_10110.root E302ZZ.S_10111.root
theorem t_1100 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(135, 2), (109, 2), (61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(135, 2), (109, 2), (61, 1), (122, 1), (0, 2)] 152 E302ZZ.S_11000.root E302ZZ.S_11001.root
theorem t_1101 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(135, 1), (109, 2), (61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(135, 1), (109, 2), (61, 1), (122, 1), (0, 2)] 152 E302ZZ.S_11010.root E302ZZ.S_11011.root
theorem t_1110 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(11, 2), (109, 1), (61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(11, 2), (109, 1), (61, 1), (122, 1), (0, 2)] 152 E302ZZ.S_11100.root E302ZZ.S_11101.root
theorem t_1111 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(11, 1), (109, 1), (61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(11, 1), (109, 1), (61, 1), (122, 1), (0, 2)] 152 E302ZZ.S_11110.root E302ZZ.S_11111.root
theorem t_000 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(25, 2), (233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(25, 2), (233, 2), (122, 2), (0, 2)] 102 t_0000 t_0001
theorem t_001 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(25, 1), (233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(25, 1), (233, 2), (122, 2), (0, 2)] 75 t_0010 t_0011
theorem t_010 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(200, 2), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(200, 2), (233, 1), (122, 2), (0, 2)] 149 t_0100 t_0101
theorem t_011 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(200, 1), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(200, 1), (233, 1), (122, 2), (0, 2)] 79 t_0110 t_0111
theorem t_100 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(137, 2), (61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(137, 2), (61, 2), (122, 1), (0, 2)] 97 t_1000 t_1001
theorem t_101 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(137, 1), (61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(137, 1), (61, 2), (122, 1), (0, 2)] 233 t_1010 t_1011
theorem t_110 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(109, 2), (61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(109, 2), (61, 1), (122, 1), (0, 2)] 135 t_1100 t_1101
theorem t_111 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(109, 1), (61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(109, 1), (61, 1), (122, 1), (0, 2)] 11 t_1110 t_1111
theorem t_00 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(233, 2), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(233, 2), (122, 2), (0, 2)] 25 t_000 t_001
theorem t_01 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(233, 1), (122, 2), (0, 2)] 200 t_010 t_011
theorem t_10 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(61, 2), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(61, 2), (122, 1), (0, 2)] 137 t_100 t_101
theorem t_11 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(61, 1), (122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(61, 1), (122, 1), (0, 2)] 109 t_110 t_111
theorem t_0 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(122, 2), (0, 2)] 233 t_00 t_01
theorem t_1 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(122, 1), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(122, 1), (0, 2)] 61 t_10 t_11
theorem t_e : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(0, 2)] 122 t_0 t_1
theorem root : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(0, 2)]) holes := t_e
#print axioms root
end E302ZZ
