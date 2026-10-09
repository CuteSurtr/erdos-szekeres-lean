import ErdosSzekeres.Omission.CoupledTemplateNineGeometry
import ErdosSzekeres.Omission.CoupledTemplateNineCheck

/-! A second nine-state omission row, reusing the same fully checked
orientation/rank refutation with new literal owners. -/
namespace ErdosSzekeres.Omission.CoupledNineVariant
open CoupledTemplateNine
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def states : Fin 9 → Fin 154 := ![44, 53, 64, 68, 75, 87, 91, 99, 118]

def support : Finset (Fin 154) := Finset.univ.image states

theorem checked : Function.Injective states ∧ Compatible states := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem exists_missing_state {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ i, states i ∉ c.residualOccupied noCap noOctagon noJunction :=
  CoupledTemplateNine.exists_missing_index states checked.1 checked.2
    c noCap noOctagon noJunction

theorem hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    1 ≤ (support \ c.residualOccupied noCap noOctagon noJunction).card :=
  CoupledTemplateNine.hole_bound states checked.1 checked.2
    c noCap noOctagon noJunction

#print axioms checked
#print axioms exists_missing_state
#print axioms hole_bound
end ErdosSzekeres.Omission.CoupledNineVariant
