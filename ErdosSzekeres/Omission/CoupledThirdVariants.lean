import ErdosSzekeres.Omission.CoupledTemplateThirdGeometry
import ErdosSzekeres.Omission.CoupledTemplateThirdCheck

/-! Literal support variants of the same coupled obstruction. Each variant
passes the entire frozen template in Lean; no new SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledThirdVariants
open CoupledTemplateThird
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

private def state000 : Fin 13 → Fin 154 := ![16, 30, 39, 43, 50, 53, 62, 65, 68, 77, 89, 91, 110]

private def state001 : Fin 13 → Fin 154 := ![16, 30, 39, 43, 50, 53, 62, 65, 79, 77, 89, 101, 110]

private def state002 : Fin 13 → Fin 154 := ![23, 30, 39, 43, 50, 53, 62, 65, 79, 77, 89, 101, 110]

def maps : Fin 3 → Fin 13 → Fin 154 := ![state000, state001, state002]

def support (r : Fin 3) : Finset (Fin 154) := Finset.univ.image (maps r)

private theorem checked000 : Function.Injective state000 ∧ Compatible state000 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked001 : Function.Injective state001 ∧ Compatible state001 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked002 : Function.Injective state002 ∧ Compatible state002 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

#check checked002

theorem checked : ∀ r : Fin 3, Function.Injective (maps r) ∧ Compatible (maps r) := by
  intro r
  fin_cases r
  · exact checked000
  · exact checked001
  · exact checked002

/-- All 3 rows have demand one in every actual residual configuration. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 3, 1 ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplateThird.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction

#print axioms checked
#print axioms all_rows
end ErdosSzekeres.Omission.CoupledThirdVariants
