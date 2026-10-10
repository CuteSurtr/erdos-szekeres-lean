import RankAttainment
import ErdosSzekeres.Omission.CoupledSemantics

/-! Direct domain and threshold-clause consequences of the attained cup bound.
The source is the chronologically earlier owner, not the smaller catalog index. -/
namespace ErdosSzekeres.Omission.Coupled.Context

variable {k n : Nat} {states : Fin k → Fin 154} (C : Context k n states)

theorem edge_cup_le_source_shape_succ {i j : Fin k} (h : C.owner i < C.owner j) :
    (C.edge i j).2 ≤ (ResidualDomains.shape (states i)).getD 0 0 + 1 := by
  have bound := C.config.residual_cup_label_le_source_shape_succ
    C.noCap C.noOctagon C.noJunction (C.owner i) (C.owner j) h
  rw [C.owner_state i] at bound
  simpa only [C.edge_of_lt h] using bound

/-- A two-literal clause: if owner i precedes owner j, their cup coordinate
cannot reach two more than the first height of state i. -/
theorem source_cup_clause (i j : Fin k) (ne : i ≠ j) :
    C.clause [(before i j).neg,
      (ge true i j ((ResidualDomains.shape (states i)).getD 0 0 + 2)).neg] := by
  simp only [clause_cons, clause_nil, or_false, holds_neg,
    C.holds_before i j ne, C.holds_ge true i j ne, ↓reduceIte]
  by_contra! h
  have bound := C.edge_cup_le_source_shape_succ h.1
  omega

/-- The same bound in the existing five-literal domain-clause API. -/
theorem source_cup_domain_clause (i j : Fin k) (ne : i ≠ j) (a b : Nat)
    (checked : (ResidualDomains.shape (states i)).getD 0 0 + 1 < b) :
    C.clause (domainClause i j a b) := by
  simp only [domainClause, clause_cons, clause_nil, or_false, holds_neg,
    C.holds_before i j ne, C.holds_ge false i j ne, C.holds_ge true i j ne,
    Bool.false_eq_true, ↓reduceIte]
  by_contra! h
  have bound := C.edge_cup_le_source_shape_succ h.1
  omega

end ErdosSzekeres.Omission.Coupled.Context

#print axioms ErdosSzekeres.Omission.Coupled.Context.edge_cup_le_source_shape_succ
#print axioms ErdosSzekeres.Omission.Coupled.Context.source_cup_clause
#print axioms ErdosSzekeres.Omission.Coupled.Context.source_cup_domain_clause
