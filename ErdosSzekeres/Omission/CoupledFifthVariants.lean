import ErdosSzekeres.Omission.CoupledTemplateFifthGeometry
import ErdosSzekeres.Omission.CoupledTemplateFifthCheck

/-! Literal support variants of the same coupled obstruction. Each variant
passes the entire frozen template in Lean; no new SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledFifthVariants
open CoupledTemplateFifth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

private def state000 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 39, 53, 50, 56, 65, 67, 91, 101, 110]

private def state001 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 39, 53, 50, 68, 65, 79, 91, 101, 110]

private def state002 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 39, 53, 50, 68, 77, 79, 91, 101, 110]

private def state003 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 39, 53, 62, 68, 77, 79, 91, 101, 110]

private def state004 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 39, 65, 50, 68, 77, 79, 91, 101, 110]

private def state005 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 39, 65, 62, 68, 77, 79, 91, 101, 110]

private def state006 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 50, 53, 62, 68, 77, 79, 91, 101, 110]

private def state007 : Fin 13 → Fin 154 := ![11, 17, 30, 43, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state008 : Fin 13 → Fin 154 := ![11, 17, 30, 53, 39, 65, 50, 68, 77, 79, 91, 101, 110]

private def state009 : Fin 13 → Fin 154 := ![11, 17, 30, 53, 39, 65, 62, 68, 77, 79, 91, 101, 110]

private def state010 : Fin 13 → Fin 154 := ![11, 17, 30, 53, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state011 : Fin 13 → Fin 154 := ![11, 17, 39, 43, 50, 53, 62, 68, 77, 79, 91, 101, 110]

private def state012 : Fin 13 → Fin 154 := ![11, 17, 39, 43, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state013 : Fin 13 → Fin 154 := ![11, 17, 39, 53, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state014 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 39, 53, 50, 56, 65, 67, 91, 101, 110]

private def state015 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 39, 53, 50, 68, 65, 79, 91, 101, 110]

private def state016 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 39, 53, 50, 68, 77, 79, 91, 101, 110]

private def state017 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 39, 53, 62, 68, 77, 79, 91, 101, 110]

private def state018 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 39, 65, 50, 68, 77, 79, 91, 101, 110]

private def state019 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 39, 65, 62, 68, 77, 79, 91, 101, 110]

private def state020 : Fin 13 → Fin 154 := ![16, 25, 30, 43, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state021 : Fin 13 → Fin 154 := ![16, 25, 30, 53, 39, 65, 50, 68, 77, 79, 91, 101, 110]

private def state022 : Fin 13 → Fin 154 := ![16, 25, 30, 53, 39, 65, 62, 68, 77, 79, 91, 101, 110]

private def state023 : Fin 13 → Fin 154 := ![16, 25, 30, 53, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state024 : Fin 13 → Fin 154 := ![16, 25, 39, 43, 50, 53, 62, 68, 77, 79, 91, 101, 110]

private def state025 : Fin 13 → Fin 154 := ![16, 25, 39, 43, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state026 : Fin 13 → Fin 154 := ![16, 25, 39, 53, 50, 65, 62, 68, 77, 79, 91, 101, 110]

private def state027 : Fin 13 → Fin 154 := ![24, 34, 39, 53, 50, 65, 62, 68, 77, 79, 91, 101, 110]

def maps : Fin 28 → Fin 13 → Fin 154 := ![state000, state001, state002, state003, state004, state005, state006, state007, state008, state009, state010, state011, state012, state013, state014, state015, state016, state017, state018, state019, state020, state021, state022, state023, state024, state025, state026, state027]

def support (r : Fin 28) : Finset (Fin 154) := Finset.univ.image (maps r)

private theorem checked000 : Function.Injective state000 ∧ Compatible state000 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked001 : Function.Injective state001 ∧ Compatible state001 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked002 : Function.Injective state002 ∧ Compatible state002 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked003 : Function.Injective state003 ∧ Compatible state003 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked004 : Function.Injective state004 ∧ Compatible state004 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked005 : Function.Injective state005 ∧ Compatible state005 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked006 : Function.Injective state006 ∧ Compatible state006 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked007 : Function.Injective state007 ∧ Compatible state007 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked008 : Function.Injective state008 ∧ Compatible state008 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked009 : Function.Injective state009 ∧ Compatible state009 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

#check checked009

private theorem checked010 : Function.Injective state010 ∧ Compatible state010 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked011 : Function.Injective state011 ∧ Compatible state011 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked012 : Function.Injective state012 ∧ Compatible state012 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked013 : Function.Injective state013 ∧ Compatible state013 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked014 : Function.Injective state014 ∧ Compatible state014 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked015 : Function.Injective state015 ∧ Compatible state015 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked016 : Function.Injective state016 ∧ Compatible state016 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked017 : Function.Injective state017 ∧ Compatible state017 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked018 : Function.Injective state018 ∧ Compatible state018 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked019 : Function.Injective state019 ∧ Compatible state019 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

#check checked019

private theorem checked020 : Function.Injective state020 ∧ Compatible state020 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked021 : Function.Injective state021 ∧ Compatible state021 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked022 : Function.Injective state022 ∧ Compatible state022 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked023 : Function.Injective state023 ∧ Compatible state023 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked024 : Function.Injective state024 ∧ Compatible state024 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked025 : Function.Injective state025 ∧ Compatible state025 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked026 : Function.Injective state026 ∧ Compatible state026 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked027 : Function.Injective state027 ∧ Compatible state027 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

#check checked027

theorem checked : ∀ r : Fin 28, Function.Injective (maps r) ∧ Compatible (maps r) := by
  intro r
  fin_cases r
  · exact checked000
  · exact checked001
  · exact checked002
  · exact checked003
  · exact checked004
  · exact checked005
  · exact checked006
  · exact checked007
  · exact checked008
  · exact checked009
  · exact checked010
  · exact checked011
  · exact checked012
  · exact checked013
  · exact checked014
  · exact checked015
  · exact checked016
  · exact checked017
  · exact checked018
  · exact checked019
  · exact checked020
  · exact checked021
  · exact checked022
  · exact checked023
  · exact checked024
  · exact checked025
  · exact checked026
  · exact checked027

/-- All 28 rows have demand one in every actual residual configuration. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 28, 1 ≤ (support r \ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplateFifth.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction

#print axioms checked
#print axioms all_rows
end ErdosSzekeres.Omission.CoupledFifthVariants
