import Mathlib.Tactic.Sat.FromLRAT

/-! A literal propositional certificate only. A separate geometric extraction
proof is required before this can imply a residual missing-state inequality. -/

open Lean Elab Term

/-- Thin term-producing wrapper around Mathlib's existing LRAT proof builder.
The output declarations are checked by Lean's ordinary kernel. -/
elab "lrat_raw " name:ident ppSpace cnf:term:max ppSpace lrat:term:max : command => do
  let full := (← getCurrNamespace) ++ name.getId
  Command.liftTermElabM do
    let cnf ← unsafe evalTerm String (mkConst ``String) cnf
    let lrat ← unsafe evalTerm String (mkConst ``String) lrat
    let (_, context, _, proof) ← Mathlib.Tactic.Sat.fromLRATAux cnf lrat full
    let formulaName := full ++ `formula
    addDecl <| Declaration.defnDecl {
      name := formulaName, levelParams := [], type := mkConst ``Sat.Fmla,
      value := context, hints := ReducibilityHints.regular 0, safety := .safe }
    addDecl <| Declaration.thmDecl {
      name := full, levelParams := [],
      type := mkApp2 (mkConst ``Sat.Fmla.proof) (mkConst formulaName)
        (mkConst ``Sat.Clause.nil), value := proof }

