import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part06
private theorem checked096 : Function.Injective state096 ∧ Compatible state096 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked097 : Function.Injective state097 ∧ Compatible state097 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked098 : Function.Injective state098 ∧ Compatible state098 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked099 : Function.Injective state099 ∧ Compatible state099 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked100 : Function.Injective state100 ∧ Compatible state100 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked101 : Function.Injective state101 ∧ Compatible state101 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked102 : Function.Injective state102 ∧ Compatible state102 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked103 : Function.Injective state103 ∧ Compatible state103 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked104 : Function.Injective state104 ∧ Compatible state104 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked105 : Function.Injective state105 ∧ Compatible state105 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked106 : Function.Injective state106 ∧ Compatible state106 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked107 : Function.Injective state107 ∧ Compatible state107 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked108 : Function.Injective state108 ∧ Compatible state108 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked109 : Function.Injective state109 ∧ Compatible state109 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked110 : Function.Injective state110 ∧ Compatible state110 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked111 : Function.Injective state111 ∧ Compatible state111 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨96 + r.val, by omega⟩) ∧
    Compatible (maps ⟨96 + r.val, by omega⟩) := by
  intro r
  fin_cases r
  · exact checked096
  · exact checked097
  · exact checked098
  · exact checked099
  · exact checked100
  · exact checked101
  · exact checked102
  · exact checked103
  · exact checked104
  · exact checked105
  · exact checked106
  · exact checked107
  · exact checked108
  · exact checked109
  · exact checked110
  · exact checked111
#print axioms checked
end Part06
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
