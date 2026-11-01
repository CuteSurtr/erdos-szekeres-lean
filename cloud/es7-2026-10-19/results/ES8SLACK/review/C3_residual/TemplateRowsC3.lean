import ErdosSzekeres.Omission.CoupledTemplateFourthGeometry
import ErdosSzekeres.Omission.CoupledTemplateFourthCheck
import ErdosSzekeres.Omission.CoupledTemplateNineGeometry
import ErdosSzekeres.Omission.CoupledTemplateNineCheck

/-!
NOT COMPILED during the review of claim C3: the per-process memory limit of that review (1.5 GB) is
below the ~2.7 GB baseline that the repository records for modules importing these templates.
To compile it, build the ErdosSzekeres library and run, from the repository root,
`lake env lean cloud/es7-2026-10-19/results/ES8SLACK/review/C3_residual/TemplateRowsC3.lean`
on a machine with about 5 GB free.

Five injective maps of existing, already kernel-checked coupled templates (Fourth: 13 owners,
Nine: 9 owners). For each map `s`, `CoupledTemplate*.hole_bound` gives the demand-one row
"image(s) contains a missing state" for every actual residual configuration. Each image lies
inside the occupied set of one of the three 33-hole residual witnesses of claim C3, so each
witness violates a geometrically valid row that is not among the 2,650 catalog rows.
A Python transcription of `check` accepts all five maps (ES8SLACK/review/C3_residual/lean_check_semantics.py).
-/

namespace TemplateRowsC3
open ErdosSzekeres.Omission

set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def w0a : Fin 13 → Fin 154 := ![15, 21, 36, 28, 24, 58, 48, 42, 56, 83, 73, 88, 97]
def w0b : Fin 13 → Fin 154 := ![22, 29, 37, 38, 32, 58, 48, 42, 56, 83, 73, 88, 97]
def w1a : Fin 9 → Fin 154 := ![33, 43, 53, 68, 65, 77, 91, 89, 110]
def w2a : Fin 13 → Fin 154 := ![15, 21, 27, 28, 24, 36, 38, 42, 56, 47, 63, 78, 87]
def w2b : Fin 13 → Fin 154 := ![22, 29, 37, 38, 32, 47, 48, 42, 56, 94, 84, 98, 106]

theorem w0a_ok : Function.Injective w0a ∧ CoupledTemplateFourth.Compatible w0a :=
  ⟨by decide +kernel, CoupledTemplateFourth.check_sound _ (by decide +kernel)⟩
theorem w0b_ok : Function.Injective w0b ∧ CoupledTemplateFourth.Compatible w0b :=
  ⟨by decide +kernel, CoupledTemplateFourth.check_sound _ (by decide +kernel)⟩
theorem w1a_ok : Function.Injective w1a ∧ CoupledTemplateNine.Compatible w1a :=
  ⟨by decide +kernel, CoupledTemplateNine.check_sound _ (by decide +kernel)⟩
theorem w2a_ok : Function.Injective w2a ∧ CoupledTemplateFourth.Compatible w2a :=
  ⟨by decide +kernel, CoupledTemplateFourth.check_sound _ (by decide +kernel)⟩
theorem w2b_ok : Function.Injective w2b ∧ CoupledTemplateFourth.Compatible w2b :=
  ⟨by decide +kernel, CoupledTemplateFourth.check_sound _ (by decide +kernel)⟩

/-- Hole sets of the three residual witnesses (ES8SLACK/witnesses.json). -/
def holes0 : Finset (Fin 154) := {12, 17, 25, 26, 27, 34, 45, 46, 47, 54, 66, 67, 69, 70, 71, 72,
  79, 91, 93, 95, 96, 98, 101, 109, 111, 113, 117, 119, 122, 123, 124, 132, 133}
def holes1 : Finset (Fin 154) := {12, 17, 25, 27, 34, 35, 36, 44, 50, 57, 58, 59, 60, 66, 67, 86,
  87, 88, 90, 98, 100, 101, 107, 109, 111, 114, 116, 117, 119, 124, 126, 132, 133}
def holes2 : Finset (Fin 154) := {11, 16, 17, 25, 26, 33, 34, 44, 45, 46, 57, 58, 60, 66, 67, 72,
  81, 88, 96, 100, 101, 102, 107, 109, 111, 116, 117, 119, 124, 126, 127, 132, 133}

theorem w0a_occupied : ∀ i, w0a i ∉ holes0 := by decide +kernel
theorem w0b_occupied : ∀ i, w0b i ∉ holes0 := by decide +kernel
theorem w1a_occupied : ∀ i, w1a i ∉ holes1 := by decide +kernel
theorem w2a_occupied : ∀ i, w2a i ∉ holes2 := by decide +kernel
theorem w2b_occupied : ∀ i, w2b i ∉ holes2 := by decide +kernel

-- The geometric rows themselves (types displayed by #check):
#check CoupledTemplateFourth.hole_bound w0a w0a_ok.1 w0a_ok.2
#check CoupledTemplateFourth.hole_bound w0b w0b_ok.1 w0b_ok.2
#check CoupledTemplateNine.hole_bound w1a w1a_ok.1 w1a_ok.2
#check CoupledTemplateFourth.hole_bound w2a w2a_ok.1 w2a_ok.2
#check CoupledTemplateFourth.hole_bound w2b w2b_ok.1 w2b_ok.2

#print axioms w0a_ok
#print axioms w1a_ok
#print axioms w2b_ok

end TemplateRowsC3
