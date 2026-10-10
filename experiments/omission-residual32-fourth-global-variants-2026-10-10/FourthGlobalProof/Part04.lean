import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part04
private theorem checked064 : Function.Injective state064 ∧ Compatible state064 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked065 : Function.Injective state065 ∧ Compatible state065 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked066 : Function.Injective state066 ∧ Compatible state066 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked067 : Function.Injective state067 ∧ Compatible state067 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked068 : Function.Injective state068 ∧ Compatible state068 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked069 : Function.Injective state069 ∧ Compatible state069 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked070 : Function.Injective state070 ∧ Compatible state070 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked071 : Function.Injective state071 ∧ Compatible state071 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked072 : Function.Injective state072 ∧ Compatible state072 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked073 : Function.Injective state073 ∧ Compatible state073 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked074 : Function.Injective state074 ∧ Compatible state074 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked075 : Function.Injective state075 ∧ Compatible state075 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked076 : Function.Injective state076 ∧ Compatible state076 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked077 : Function.Injective state077 ∧ Compatible state077 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked078 : Function.Injective state078 ∧ Compatible state078 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked079 : Function.Injective state079 ∧ Compatible state079 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨64 + r.val, by omega⟩) ∧
    Compatible (maps ⟨64 + r.val, by omega⟩) := by
  intro r
  fin_cases r
  · exact checked064
  · exact checked065
  · exact checked066
  · exact checked067
  · exact checked068
  · exact checked069
  · exact checked070
  · exact checked071
  · exact checked072
  · exact checked073
  · exact checked074
  · exact checked075
  · exact checked076
  · exact checked077
  · exact checked078
  · exact checked079
#print axioms checked
end Part04
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
