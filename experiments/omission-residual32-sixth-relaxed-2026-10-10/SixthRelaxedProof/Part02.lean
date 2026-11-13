import SixthRelaxedProof.Data

namespace ErdosSzekeres.Omission.CoupledSixthRelaxedVariants
open CoupledTemplateSixthRelaxed
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

namespace Part02
private theorem checked032 : Function.Injective state032 ∧ Compatible state032 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked033 : Function.Injective state033 ∧ Compatible state033 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked034 : Function.Injective state034 ∧ Compatible state034 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked035 : Function.Injective state035 ∧ Compatible state035 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked036 : Function.Injective state036 ∧ Compatible state036 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked037 : Function.Injective state037 ∧ Compatible state037 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked038 : Function.Injective state038 ∧ Compatible state038 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked039 : Function.Injective state039 ∧ Compatible state039 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked040 : Function.Injective state040 ∧ Compatible state040 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked041 : Function.Injective state041 ∧ Compatible state041 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked042 : Function.Injective state042 ∧ Compatible state042 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked043 : Function.Injective state043 ∧ Compatible state043 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked044 : Function.Injective state044 ∧ Compatible state044 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked045 : Function.Injective state045 ∧ Compatible state045 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked046 : Function.Injective state046 ∧ Compatible state046 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

private theorem checked047 : Function.Injective state047 ∧ Compatible state047 := by
  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩

theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨32 + r.val, by omega⟩) ∧
    Compatible (maps ⟨32 + r.val, by omega⟩) := by
  intro r
  fin_cases r
  · exact checked032
  · exact checked033
  · exact checked034
  · exact checked035
  · exact checked036
  · exact checked037
  · exact checked038
  · exact checked039
  · exact checked040
  · exact checked041
  · exact checked042
  · exact checked043
  · exact checked044
  · exact checked045
  · exact checked046
  · exact checked047
#print axioms checked
end Part02
end ErdosSzekeres.Omission.CoupledSixthRelaxedVariants
