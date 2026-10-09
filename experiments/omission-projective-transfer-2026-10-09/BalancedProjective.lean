import BalancedGeometry
import ErdosSzekeres.Omission.ProjectiveTransfer

open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionBalanced

/-- Every octagon-free general-position set of at least 194 actual real points
has a root-deletion chart containing a 7-cup. The chart still avoids 7-caps and
convex octagons, and its explicit relation to the original set is retained. -/
theorem large_avoiding_set_has_chart_cup (S : Finset Point)
    (gp : GeneralPosition S) (size : 194 ≤ S.card) (avoid : ¬ HasConvexNGon 8 S) :
    ∃ n : ℕ, ∃ c : Configuration n, S.card = n + 1 ∧ IsRootDeletionChart S c ∧
      ¬ c.HasCap 7 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point) ∧ c.HasCup 7 := by
  have nonempty : S.Nonempty := Finset.card_pos.mp (by omega)
  obtain ⟨n, c, count, chart, noCap, noOctagon⟩ := exists_cap_free_chart S gp nonempty avoid
  refine ⟨n, c, count, chart, noCap, noOctagon, ?_⟩
  by_contra noCup
  have bound := real_configuration_bound c noCap noCup noOctagon
  omega

#print axioms large_avoiding_set_has_chart_cup

end OmissionBalanced
