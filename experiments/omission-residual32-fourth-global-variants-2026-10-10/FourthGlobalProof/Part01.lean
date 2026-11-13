import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part01
private theorem checked016 : Function.Injective state016 ∧ Compatible state016 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked017 : Function.Injective state017 ∧ Compatible state017 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked018 : Function.Injective state018 ∧ Compatible state018 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked019 : Function.Injective state019 ∧ Compatible state019 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

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

private theorem checked028 : Function.Injective state028 ∧ Compatible state028 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked029 : Function.Injective state029 ∧ Compatible state029 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked030 : Function.Injective state030 ∧ Compatible state030 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked031 : Function.Injective state031 ∧ Compatible state031 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨16 + r.val, by omega⟩) ∧
    Compatible (maps ⟨16 + r.val, by omega⟩) := by
  intro r
  fin_cases r
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
  · exact checked028
  · exact checked029
  · exact checked030
  · exact checked031
#print axioms checked
end Part01
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
