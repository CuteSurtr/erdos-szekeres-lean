import E302ZZ.C1297501
import CompactChecker.Path
open CompactChecker
set_option maxRecDepth 100000
set_option Elab.async false
set_option linter.all false
namespace E302ZZ.P_12975
-- FV302 (24 Nov 2026): joins of the ES(8) <= 302 compact check (budget-69 Z/Z*-row tree); Lean checks each step
theorem root : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(221, 1), (54, 1), (168, 1), (95, 2), (62, 1), (43, 1), (77, 2), (232, 1), (152, 2), (79, 2), (200, 1), (233, 1), (122, 2), (0, 2)]) holes := E302ZZ.C1297501.ex0
#print axioms root
end E302ZZ.P_12975
