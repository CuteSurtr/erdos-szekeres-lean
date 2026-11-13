import ErdosSzekeres.Omission.ResidualRealization

/-! An attained past-cup rank cannot jump more than one above the source
vertex's incoming first-column height. No finite certificate is assumed. -/
namespace ErdosSzekeres.Omission.ResidualRankAttainment

open StateInterface ResidualRanks ResidualStates

private theorem ending_length_le_source_height_add_two (n cup)
    (noCap : ¬ (ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    {u v len : Nat} (path : ActualRanks.EndingPath cup true u v len)
    (hvn : v < n) : len ≤ column n cup u 0 + 2 := by
  cases path with
  | pair huv => omega
  | @step t u v len priorPath huv same =>
    have htu := (ActualRanks.length_bounds priorPath).2.2
    have lower := ActualRanks.rank_ge priorPath
    have capBound := rank_lt_no_cap n cup t u noCap htu (lt_trans huv hvn)
    have positive : 1 ≤ (labels n cup t u).1 := by
      simp only [labels]
      omega
    have height : (labels n cup t u).2 ≤ column n cup u 0 := by
      unfold column
      exact Finset.le_sup_of_le (Finset.mem_range.mpr htu)
        (by simp only [Nat.zero_add, if_pos positive]; exact le_rfl)
    simp only [labels] at height
    omega

/-- The only geometric restriction needed is absence of a six-cap. Neither
eight-cup avoidance nor the residual no-junction condition is assumed. -/
theorem cup_label_le_source_height_succ (n cup)
    (noCap : ¬ (ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (u v : Nat) (huv : u < v) (hvn : v < n) :
    (labels n cup u v).2 ≤ column n cup u 0 + 1 := by
  have bound := ending_length_le_source_height_add_two n cup noCap
    (ActualRanks.rank_attained cup true u v huv) hvn
  simp only [labels]
  omega

/-- Translation to the literal source profile in the checked 154-state catalog.
The extra hypotheses are exactly those needed to define its owner index. -/
theorem cup_label_le_source_shape_succ (n cup)
    (noCap : ¬ (ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (noCup : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup)
    (u v : Fin n) (huv : u < v) :
    (labels n cup u v).2 ≤
      (ResidualDomains.shape (ResidualCatalog.ownerIndex n cup noCap noCup junction u).val).getD 0 0 + 1 := by
  rw [ResidualDomains.owner_shape]
  simpa [stateList, state] using
    cup_label_le_source_height_succ n cup noCap u v huv v.isLt

end ErdosSzekeres.Omission.ResidualRankAttainment

namespace ErdosSzekeres.Omission.Configuration

/-- Direct actual-configuration form of the source-profile cup bound. -/
theorem residual_cup_label_le_source_shape_succ {n : Nat} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (u v : Fin n) (huv : u < v) :
    (ResidualRanks.labels n c.cup u v).2 ≤
      (ResidualDomains.shape (c.residualOwner noCap noOctagon noJunction u).val).getD 0 0 + 1 :=
  ResidualRankAttainment.cup_label_le_source_shape_succ n c.cup
    (fun h => noCap (ListGeometry.hasCap_of_list c h))
    (c.residual_avoids_cup noOctagon) (ResidualRanks.noJunction_of_lists n c.cup noJunction)
    u v huv

end ErdosSzekeres.Omission.Configuration

#print axioms ErdosSzekeres.Omission.ResidualRankAttainment.cup_label_le_source_height_succ
#print axioms ErdosSzekeres.Omission.ResidualRankAttainment.cup_label_le_source_shape_succ
#print axioms ErdosSzekeres.Omission.Configuration.residual_cup_label_le_source_shape_succ
