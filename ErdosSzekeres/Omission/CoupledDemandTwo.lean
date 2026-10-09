import ErdosSzekeres.Omission.TwoHoleAssembly
import ErdosSzekeres.Omission.CoupledVariants
import ErdosSzekeres.Omission.CoupledThirdObstruction

/-! A fourteen-state row with demand two, assembled from two original cycle
rows and two coupled obstructions. This is a necessary residual inequality;
it does not assert an improved total residual or ES(8) population bound. -/
namespace ErdosSzekeres.Omission.CoupledDemandTwo
set_option maxHeartbeats 10000000
set_option maxRecDepth 100000

def support : Finset (Fin 154) := {16,25,30,39,43,50,53,62,65,68,77,89,91,101}

def cycleOne : List (Fin 154) := [16,30,39,50,62,89,68,25]
def cycleTwo : List (Fin 154) := [25,43,53,65,77,89,110,101,91]

theorem cycles_checked : ResidualCycleValid cycleOne ∧ ResidualCycleValid cycleTwo := by
  decide +kernel

theorem support_card : support.card = 14 := by decide +kernel

/-- Each one-point deletion is excluded by an old cycle or a coupled core. -/
theorem deletion_coverage : ∀ p ∈ support,
    (cycleOne.toFinset \ support.erase p).card < 1 ∨
    (cycleTwo.toFinset \ support.erase p).card < 2 ∨
    (CoupledVariants.support 24 \ support.erase p).card < 1 ∨
    CoupledCoreThird.support.toFinset ⊆ support.erase p := by
  decide +kernel

/-- Pure finite assembly: these four necessary rows imply the new demand two. -/
theorem hole_bound_of_rows (occupied : Finset (Fin 154))
    (hcycleOne : 1 ≤ (cycleOne.toFinset \ occupied).card)
    (hcycleTwo : 2 ≤ (cycleTwo.toFinset \ occupied).card)
    (hfirst : 1 ≤ (CoupledVariants.support 24 \ occupied).card)
    (hthird : 1 ≤ (CoupledCoreThird.support.toFinset \ occupied).card) :
    2 ≤ (support \ occupied).card := by
  apply two_holes_of_deletions support occupied (by decide)
  intro p hp
  rcases deletion_coverage p hp with h | h | h | h
  · exact hole_of_card_deficit _ _ _ 1 hcycleOne h
  · exact hole_of_card_deficit _ _ _ 2 hcycleTwo h
  · exact hole_of_card_deficit _ _ _ 1 hfirst h
  · apply le_trans hthird
    apply Finset.card_le_card
    intro x hx
    obtain ⟨hxC, hxO⟩ := Finset.mem_sdiff.mp hx
    exact Finset.mem_sdiff.mpr ⟨h hxC, hxO⟩

/-- Every actual residual configuration omits at least two of these fourteen
states, under the standard residual no-cap/no-octagon/no-junction hypotheses. -/
theorem hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    2 ≤ (support \ c.residualOccupied noCap noOctagon noJunction).card := by
  apply hole_bound_of_rows
  · have bound := c.residual_list_cycle_hole_bound noCap noOctagon noJunction
      cycleOne cycles_checked.1
    simpa only [cycleOne, List.length_cons, List.length_nil] using bound
  · have bound := c.residual_list_cycle_hole_bound noCap noOctagon noJunction
      cycleTwo cycles_checked.2
    simpa only [cycleTwo, List.length_cons, List.length_nil] using bound
  · exact CoupledVariants.all_rows c noCap noOctagon noJunction 24
  · exact CoupledCoreThird.hole_bound c noCap noOctagon noJunction

end ErdosSzekeres.Omission.CoupledDemandTwo
