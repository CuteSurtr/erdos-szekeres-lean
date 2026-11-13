import FourthGlobalProof.Part00
import FourthGlobalProof.Part01
import FourthGlobalProof.Part02
import FourthGlobalProof.Part03
import FourthGlobalProof.Part04
import FourthGlobalProof.Part05
import FourthGlobalProof.Part06
import FourthGlobalProof.Part07

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

theorem checked : ∀ r : Fin 128, Function.Injective (maps r) ∧ Compatible (maps r) := by
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
  · exact Part03.checked 0
  · exact Part03.checked 1
  · exact Part03.checked 2
  · exact Part03.checked 3
  · exact Part03.checked 4
  · exact Part03.checked 5
  · exact Part03.checked 6
  · exact Part03.checked 7
  · exact Part03.checked 8
  · exact Part03.checked 9
  · exact Part03.checked 10
  · exact Part03.checked 11
  · exact Part03.checked 12
  · exact Part03.checked 13
  · exact Part03.checked 14
  · exact Part03.checked 15
  · exact Part04.checked 0
  · exact Part04.checked 1
  · exact Part04.checked 2
  · exact Part04.checked 3
  · exact Part04.checked 4
  · exact Part04.checked 5
  · exact Part04.checked 6
  · exact Part04.checked 7
  · exact Part04.checked 8
  · exact Part04.checked 9
  · exact Part04.checked 10
  · exact Part04.checked 11
  · exact Part04.checked 12
  · exact Part04.checked 13
  · exact Part04.checked 14
  · exact Part04.checked 15
  · exact Part05.checked 0
  · exact Part05.checked 1
  · exact Part05.checked 2
  · exact Part05.checked 3
  · exact Part05.checked 4
  · exact Part05.checked 5
  · exact Part05.checked 6
  · exact Part05.checked 7
  · exact Part05.checked 8
  · exact Part05.checked 9
  · exact Part05.checked 10
  · exact Part05.checked 11
  · exact Part05.checked 12
  · exact Part05.checked 13
  · exact Part05.checked 14
  · exact Part05.checked 15
  · exact Part06.checked 0
  · exact Part06.checked 1
  · exact Part06.checked 2
  · exact Part06.checked 3
  · exact Part06.checked 4
  · exact Part06.checked 5
  · exact Part06.checked 6
  · exact Part06.checked 7
  · exact Part06.checked 8
  · exact Part06.checked 9
  · exact Part06.checked 10
  · exact Part06.checked 11
  · exact Part06.checked 12
  · exact Part06.checked 13
  · exact Part06.checked 14
  · exact Part06.checked 15
  · exact Part07.checked 0
  · exact Part07.checked 1
  · exact Part07.checked 2
  · exact Part07.checked 3
  · exact Part07.checked 4
  · exact Part07.checked 5
  · exact Part07.checked 6
  · exact Part07.checked 7
  · exact Part07.checked 8
  · exact Part07.checked 9
  · exact Part07.checked 10
  · exact Part07.checked 11
  · exact Part07.checked 12
  · exact Part07.checked 13
  · exact Part07.checked 14
  · exact Part07.checked 15

/-- Every literal row has demand one in an actual residual configuration. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 128, 1 ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplateFourth.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction
#print axioms checked
#print axioms all_rows
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
