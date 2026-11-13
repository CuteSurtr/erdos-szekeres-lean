import ErdosSzekeres.Omission.CoupledTemplateFifth

/-! A computational Boolean form of the template's bounded prerequisites.
The soundness proof avoids reducing a large dependent Decidable instance when
checking many literal supports. No native evaluation is used. -/
namespace ErdosSzekeres.Omission.CoupledTemplateFifth
open Coupled

def check (σ : Fin 13 → Fin 154) : Bool :=
  emptyTests.all (fun t => emptyCheck σ t.1 t.2) &&
    (domainTests.all (fun t => decide (¬Allowed σ t.1 t.2.1 (t.2.2.1, t.2.2.2))) &&
    positiveTests.all (fun t => CycleSigns.CheckTriple ResidualDomains.computedTable
      (σ t.1) (σ t.2.1) (σ t.2.2)))

theorem check_sound (σ : Fin 13 → Fin 154) (h : check σ = true) : Compatible σ := by
  simp only [check, Bool.and_eq_true] at h
  refine ⟨?_, ?_, ?_⟩
  · intro t ht
    exact List.all_eq_true.mp h.1 t ht
  · intro t ht
    exact of_decide_eq_true (List.all_eq_true.mp h.2.1 t ht)
  · intro t ht
    exact List.all_eq_true.mp h.2.2 t ht

end ErdosSzekeres.Omission.CoupledTemplateFifth
