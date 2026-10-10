import ErdosSzekeres.Omission.ResidualCycleGeometry

open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionResidualZeroState

/-- The first vertex has no incoming pairs, independently of the two-sided
definition of the pair labels. Every incoming column is therefore zero. -/
theorem column_zero (n : ℕ) (cup : ℕ → ℕ → ℕ → Bool) (i : ℕ) :
    ResidualStates.column n cup 0 i = 0 := by
  simp [ResidualStates.column]

/-- The first vertex receives the literal all-zero catalog profile. -/
theorem ownerIndex_zero (n : ℕ) (cup : ℕ → ℕ → ℕ → Bool)
    (caps : ¬ (ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8)
    (junction : ResidualRanks.NoJunction n cup) (hn : 0 < n) :
    ResidualCatalog.ownerIndex n cup caps cups junction ⟨0, hn⟩ = 0 := by
  apply Fin.ext
  change ResidualCatalog.catalog.idxOf
    (ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨0, hn⟩)
      ++ [0]) = 0
  have profile :
      ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨0, hn⟩)
        ++ [0] = [0, 0, 0, 0, 0] := by
    simp [ResidualStates.stateList, ResidualStates.state, column_zero, List.ofFn_succ]
  rw [profile]
  decide +kernel

/-- Every nonempty actual residual configuration occupies source state zero.
This is an additional condition on actual rank realizations, not an assumption
about arbitrary Boolean models of the omission inequalities. -/
theorem zero_mem_residualOccupied {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (hn : 0 < n) :
    (0 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction := by
  apply Finset.mem_image.mpr
  refine ⟨⟨0, hn⟩, Finset.mem_univ _, ?_⟩
  exact ownerIndex_zero n c.cup _ _ _ hn

#print axioms column_zero
#print axioms ownerIndex_zero
#print axioms zero_mem_residualOccupied

end OmissionResidualZeroState
