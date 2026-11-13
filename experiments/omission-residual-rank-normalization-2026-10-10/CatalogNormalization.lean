import Normalization

namespace ErdosSzekeres.Omission.RankNormalization

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

private theorem checked_height_max : ∀ id : Fin 154, ∀ a : Fin 4,
    (ResidualDomains.shape id).getD a 0 ≤ (ResidualDomains.shape id).getD 0 0 := by
  decide +kernel

/-- The exact 154-state catalog satisfies the hypothesis of clipping. -/
theorem catalog_heightDominates {k : Nat} (states : Fin k → Fin 154) :
    HeightDominates (fun i => ResidualDomains.shape (states i)) := by
  intro i a ha ha4
  exact checked_height_max (states i) ⟨a - 1, by omega⟩

/-- The abstract domains are exactly the existing coupled semantic domains. -/
theorem catalog_allowed_iff {k : Nat} (states : Fin k → Fin 154)
    (i j : Fin k) (a b : Nat) :
    Allowed (fun i => ResidualDomains.shape (states i)) i j a b ↔
      Coupled.Allowed states i j (a, b) := by
  rfl

theorem catalog_exists_iff_sourceBound {k : Nat} (states : Fin k → Fin 154)
    (F : Frame k) :
    (∃ q, Valid (fun i => ResidualDomains.shape (states i)) F q) ↔
      ∃ q, Valid (fun i => ResidualDomains.shape (states i)) F q ∧
        SourceBound (fun i => ResidualDomains.shape (states i)) F q :=
  exists_iff_sourceBound _ (catalog_heightDominates states) F

/-- With arbitrary frame-only constraints, the added source-cup bounds do not
change abstract satisfiability for the exact catalog. -/
theorem catalog_exists_frame_iff_sourceBound {k : Nat} (states : Fin k → Fin 154)
    (P : Frame k → Prop) :
    (∃ F q, P F ∧ Valid (fun i => ResidualDomains.shape (states i)) F q) ↔
      ∃ F q, P F ∧ Valid (fun i => ResidualDomains.shape (states i)) F q ∧
        SourceBound (fun i => ResidualDomains.shape (states i)) F q :=
  exists_frame_iff_sourceBound _ (catalog_heightDominates states) P

end ErdosSzekeres.Omission.RankNormalization

#print axioms ErdosSzekeres.Omission.RankNormalization.catalog_heightDominates
#print axioms ErdosSzekeres.Omission.RankNormalization.catalog_allowed_iff
#print axioms ErdosSzekeres.Omission.RankNormalization.catalog_exists_iff_sourceBound
#print axioms ErdosSzekeres.Omission.RankNormalization.catalog_exists_frame_iff_sourceBound
