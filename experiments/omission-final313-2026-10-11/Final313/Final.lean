import Final313.Match
import Residual2650ZeroProof.Root
import Residual32Bridge2650.Final

/-!
ES(8) ≤ 313. The exported certificate `OmissionResidual2650Zero.node1` excludes every
0/1 hole vector with state 0 occupied that satisfies the 2,650 residual rows with at
most 32 holes. The bridge turns this into the residual bound 121 and, with the
balanced bound 190, into `ForcesConvexNGon 313 8`.
-/

open ErdosSzekeres

namespace ErdosSzekeres.Omission

theorem residual_excludes_2650_zero : OmissionResidual32Bridge2650.Excludes2650Zero 32 :=
  OmissionResidual32Bridge2650.excludes2650Zero_of_node
    OmissionResidual2650ZeroMatch.support_eq OmissionResidual2650ZeroMatch.demand_eq
    OmissionResidual2650Zero.node1

/-- Every set of at least 313 points in general position contains a convex octagon. -/
theorem forces_convex_octagon_313 : ForcesConvexNGon 313 8 :=
  OmissionResidual32Bridge2650.forces_convex_octagon_313_of_excludes residual_excludes_2650_zero

theorem convex_octagon_of_card_ge_313 (S : Finset (Fin 2 → ℝ))
    (gp : GeneralPosition S) (size : 313 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  OmissionResidual32Bridge2650.convex_octagon_of_card_ge_313_of_excludes
    residual_excludes_2650_zero S gp size

#print axioms residual_excludes_2650_zero
#print axioms forces_convex_octagon_313
#print axioms convex_octagon_of_card_ge_313

end ErdosSzekeres.Omission
