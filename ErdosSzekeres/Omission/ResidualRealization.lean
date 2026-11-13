import ErdosSzekeres.Omission.ResidualDomains

namespace ErdosSzekeres.Omission.Configuration

open ActualRanks Subsets

/-- Octagon avoidance rules out an actual attained eight-cup. -/
theorem residual_avoids_cup {n : ℕ} (c : Configuration n)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) : Avoids n c.cup true 8 :=
  avoids_of_no_cup n 8 c.cup (fun h => noOctagon (ListGeometry.hasNCup_octagon c h))

/-- The exact 154-state source-index assignment for actual residual points.
All three inputs are geometric restrictions supplied by the proved partition. -/
noncomputable def residualOwner {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) : Fin n → Fin 154 :=
  ResidualCatalog.ownerIndex n c.cup (fun h => noCap (ListGeometry.hasCap_of_list c h))
    (c.residual_avoids_cup noOctagon) (ResidualRanks.noJunction_of_lists n c.cup noJunction)

theorem residualOwner_injective {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    Function.Injective (c.residualOwner noCap noOctagon noJunction) :=
  ResidualCatalog.ownerIndex_injective n c.cup _ _ _

/-- The finite residual universe bound, before the cycle and block cuts.
This does not assert the target residual population bound of 123. -/
theorem residual_universe_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) : n ≤ 154 := by
  simpa using Fintype.card_le_of_injective _
    (c.residualOwner_injective noCap noOctagon noJunction)

end ErdosSzekeres.Omission.Configuration
