import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part03
private theorem checked048 : Function.Injective state048 ∧ Compatible state048 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked049 : Function.Injective state049 ∧ Compatible state049 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked050 : Function.Injective state050 ∧ Compatible state050 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked051 : Function.Injective state051 ∧ Compatible state051 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked052 : Function.Injective state052 ∧ Compatible state052 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked053 : Function.Injective state053 ∧ Compatible state053 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked054 : Function.Injective state054 ∧ Compatible state054 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked055 : Function.Injective state055 ∧ Compatible state055 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked056 : Function.Injective state056 ∧ Compatible state056 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked057 : Function.Injective state057 ∧ Compatible state057 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked058 : Function.Injective state058 ∧ Compatible state058 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked059 : Function.Injective state059 ∧ Compatible state059 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked060 : Function.Injective state060 ∧ Compatible state060 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked061 : Function.Injective state061 ∧ Compatible state061 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked062 : Function.Injective state062 ∧ Compatible state062 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked063 : Function.Injective state063 ∧ Compatible state063 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨48 + r.val, by omega⟩) ∧
    Compatible (maps ⟨48 + r.val, by omega⟩) := by
  intro r
  fin_cases r
  · exact checked048
  · exact checked049
  · exact checked050
  · exact checked051
  · exact checked052
  · exact checked053
  · exact checked054
  · exact checked055
  · exact checked056
  · exact checked057
  · exact checked058
  · exact checked059
  · exact checked060
  · exact checked061
  · exact checked062
  · exact checked063
#print axioms checked
end Part03
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
