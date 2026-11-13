import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part07
private theorem checked112 : Function.Injective state112 ∧ Compatible state112 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked113 : Function.Injective state113 ∧ Compatible state113 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked114 : Function.Injective state114 ∧ Compatible state114 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked115 : Function.Injective state115 ∧ Compatible state115 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked116 : Function.Injective state116 ∧ Compatible state116 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked117 : Function.Injective state117 ∧ Compatible state117 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked118 : Function.Injective state118 ∧ Compatible state118 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked119 : Function.Injective state119 ∧ Compatible state119 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked120 : Function.Injective state120 ∧ Compatible state120 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked121 : Function.Injective state121 ∧ Compatible state121 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked122 : Function.Injective state122 ∧ Compatible state122 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked123 : Function.Injective state123 ∧ Compatible state123 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked124 : Function.Injective state124 ∧ Compatible state124 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked125 : Function.Injective state125 ∧ Compatible state125 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked126 : Function.Injective state126 ∧ Compatible state126 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked127 : Function.Injective state127 ∧ Compatible state127 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨112 + r.val, by omega⟩) ∧
    Compatible (maps ⟨112 + r.val, by omega⟩) := by
  intro r
  fin_cases r
  · exact checked112
  · exact checked113
  · exact checked114
  · exact checked115
  · exact checked116
  · exact checked117
  · exact checked118
  · exact checked119
  · exact checked120
  · exact checked121
  · exact checked122
  · exact checked123
  · exact checked124
  · exact checked125
  · exact checked126
  · exact checked127
#print axioms checked
end Part07
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
