import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part00
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

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨0 + r.val, by omega⟩) ∧
    Compatible (maps ⟨0 + r.val, by omega⟩) := by
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
#print axioms checked
end Part00
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
