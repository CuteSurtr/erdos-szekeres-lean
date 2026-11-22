import RowGeo.Sound
/-! Negative control: the source-cup clause with threshold h₁ + 1 instead of h₁ + 2 (one less than coupled.py
line 64). The proof of `RowGeo.clause_source` must NOT go through. -/
namespace RowGeo
open RowEnc ErdosSzekeres ErdosSzekeres.Omission Coupled
theorem bad_source {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states) (u v : Fin k) (huv : u ≠ v) :
    C.clause [(before u v).neg, (ge true u v (h1 (states u) + 1)).neg] := by
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_neg, C.holds_before u v huv,
    C.holds_ge true u v huv, if_true]
  by_contra hcon
  rw [not_or, not_not, not_not] at hcon
  obtain ⟨hlt, hle⟩ := hcon
  have hb := cup_label_le_h1 C.config C.noCap C.noOctagon C.noJunction (C.owner u) (C.owner v) hlt
  rw [C.edge_of_lt hlt] at hle
  rw [C.owner_state u] at hb
  have e : h1 (states u) = (ResidualDomains.shape (states u)).getD 0 0 := by
    unfold h1; rw [st_eq_shape]
  omega
end RowGeo
