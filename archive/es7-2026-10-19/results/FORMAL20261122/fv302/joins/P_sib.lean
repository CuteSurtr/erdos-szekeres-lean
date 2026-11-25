import E302ZZ.C908501
import E302ZZ.C908601
import CompactChecker.Path
open CompactChecker
set_option maxRecDepth 100000
set_option Elab.async false
set_option linter.all false
namespace E302ZZ.P_sib
-- FV302 (24 Nov 2026): joins of the ES(8) <= 302 compact check (budget-69 Z/Z*-row tree); Lean checks each step
theorem t_01000111000011 : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(221, 1), (54, 1), (84, 2), (95, 2), (62, 2), (43, 2), (77, 1), (232, 1), (168, 1), (152, 2), (149, 2), (200, 2), (233, 1), (122, 2), (0, 2)]) holes :=
  split_pm fcatZZs16 3133 252 69 (zerosF 252) [(221, 1), (54, 1), (84, 2), (95, 2), (62, 2), (43, 2), (77, 1), (232, 1), (168, 1), (152, 2), (149, 2), (200, 2), (233, 1), (122, 2), (0, 2)] 49 E302ZZ.C908501.ex0 E302ZZ.C908601.ex0
theorem root : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(221, 1), (54, 1), (84, 2), (95, 2), (62, 2), (43, 2), (77, 1), (232, 1), (168, 1), (152, 2), (149, 2), (200, 2), (233, 1), (122, 2), (0, 2)]) holes := t_01000111000011
#print axioms root
end E302ZZ.P_sib
