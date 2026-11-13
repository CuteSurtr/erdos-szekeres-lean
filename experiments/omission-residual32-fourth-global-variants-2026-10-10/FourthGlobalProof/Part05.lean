import FourthGlobalProof.Data

namespace ErdosSzekeres.Omission.CoupledFourthGlobalVariants
open CoupledTemplateFourth
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part05
private theorem checked080 : Function.Injective state080 ∧ Compatible state080 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked081 : Function.Injective state081 ∧ Compatible state081 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked082 : Function.Injective state082 ∧ Compatible state082 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked083 : Function.Injective state083 ∧ Compatible state083 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked084 : Function.Injective state084 ∧ Compatible state084 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked085 : Function.Injective state085 ∧ Compatible state085 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked086 : Function.Injective state086 ∧ Compatible state086 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked087 : Function.Injective state087 ∧ Compatible state087 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked088 : Function.Injective state088 ∧ Compatible state088 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked089 : Function.Injective state089 ∧ Compatible state089 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked090 : Function.Injective state090 ∧ Compatible state090 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked091 : Function.Injective state091 ∧ Compatible state091 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked092 : Function.Injective state092 ∧ Compatible state092 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked093 : Function.Injective state093 ∧ Compatible state093 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked094 : Function.Injective state094 ∧ Compatible state094 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked095 : Function.Injective state095 ∧ Compatible state095 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨80 + r.val, by omega⟩) ∧
    Compatible (maps ⟨80 + r.val, by omega⟩) := by
  intro r
  fin_cases r
  · exact checked080
  · exact checked081
  · exact checked082
  · exact checked083
  · exact checked084
  · exact checked085
  · exact checked086
  · exact checked087
  · exact checked088
  · exact checked089
  · exact checked090
  · exact checked091
  · exact checked092
  · exact checked093
  · exact checked094
  · exact checked095
#print axioms checked
end Part05
end ErdosSzekeres.Omission.CoupledFourthGlobalVariants
