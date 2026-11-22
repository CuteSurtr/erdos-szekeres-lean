import RowGeo.Sound
/-! Negative control: the forced-sign clause [positive i j l] justified by the six-order test on the wrong state
order (states i, states l, states j), i.e. the test of the negative clause. The proof must NOT go through. -/
namespace RowGeo
open RowEnc ErdosSzekeres ErdosSzekeres.Omission Coupled
theorem bad_fixed {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states) (i j l : Fin k)
    (hij : i ≠ j) (hjl : j ≠ l) (hil : i ≠ l)
    (h : ttB (states i) (states l) (states j) = true) : C.clause [positive i j l] := by
  simp only [Context.clause_cons, Context.clause_nil, or_false, C.holds_positive i j l hij hil hjl]
  apply positive_of_ttB C.config C.noCap C.noOctagon C.noJunction (C.owner i) (C.owner j) (C.owner l)
    (C.injective.ne hij) (C.injective.ne hjl) (C.injective.ne hil)
  simpa only [C.owner_state] using h
end RowGeo
