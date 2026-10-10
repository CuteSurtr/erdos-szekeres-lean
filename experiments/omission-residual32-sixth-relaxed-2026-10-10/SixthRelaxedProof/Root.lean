import SixthRelaxedProof.Part00
import SixthRelaxedProof.Part01
import SixthRelaxedProof.Part02

namespace ErdosSzekeres.Omission.CoupledSixthRelaxedVariants
open CoupledTemplateSixthRelaxed
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

theorem checked : ∀ r : Fin 48, Function.Injective (maps r) ∧ Compatible (maps r) := by
  intro r
  fin_cases r
  · exact Part00.checked 0
  · exact Part00.checked 1
  · exact Part00.checked 2
  · exact Part00.checked 3
  · exact Part00.checked 4
  · exact Part00.checked 5
  · exact Part00.checked 6
  · exact Part00.checked 7
  · exact Part00.checked 8
  · exact Part00.checked 9
  · exact Part00.checked 10
  · exact Part00.checked 11
  · exact Part00.checked 12
  · exact Part00.checked 13
  · exact Part00.checked 14
  · exact Part00.checked 15
  · exact Part01.checked 0
  · exact Part01.checked 1
  · exact Part01.checked 2
  · exact Part01.checked 3
  · exact Part01.checked 4
  · exact Part01.checked 5
  · exact Part01.checked 6
  · exact Part01.checked 7
  · exact Part01.checked 8
  · exact Part01.checked 9
  · exact Part01.checked 10
  · exact Part01.checked 11
  · exact Part01.checked 12
  · exact Part01.checked 13
  · exact Part01.checked 14
  · exact Part01.checked 15
  · exact Part02.checked 0
  · exact Part02.checked 1
  · exact Part02.checked 2
  · exact Part02.checked 3
  · exact Part02.checked 4
  · exact Part02.checked 5
  · exact Part02.checked 6
  · exact Part02.checked 7
  · exact Part02.checked 8
  · exact Part02.checked 9
  · exact Part02.checked 10
  · exact Part02.checked 11
  · exact Part02.checked 12
  · exact Part02.checked 13
  · exact Part02.checked 14
  · exact Part02.checked 15

/-- Every literal row is valid in an actual residual configuration. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 48, 1 ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplateSixthRelaxed.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction
#print axioms checked
#print axioms all_rows
end ErdosSzekeres.Omission.CoupledSixthRelaxedVariants
