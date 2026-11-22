import N66E15.Clauses

/-!
# N66E15.Rows: R0_15, the row supports used by the 105 certificates (Std-only)

`data/rows_used15.txt` (465,335 bytes, SHA-256 `f45e25f1…af2f0511`; written by `tools/mk_data15.py`) has one sorted
support per line: the 10,859 distinct supports of the row clauses of the 105 level-15 trims (= the union of their
`used_rows.json`), in the order of `mono/rows_1832.json` (SHA-256 `80bec1b4…6b61f33`; every used row is in it).
`R0_15` is its parse; it is a different list from the level-14 `R0` (11,884 rows). The theorem quantifies over the row list
and assumes `RowsValid R0_15`; the printer prints row clauses only from `R0_15`, so the trims' rows are members by
construction. The kernel never evaluates `R0_15`.
-/

namespace N66E15

@[irreducible] def rowsText : String := include_str "data/rows_used15.txt"

/-- A token as a state (`none` unless a decimal below 70). -/
def parseState (w : String) : Option (Fin 70) :=
  match w.toNat? with
  | some n => if h : n < 70 then some ⟨n, h⟩ else none
  | none => none

/-- One support per nonempty line; a line with an invalid token is dropped. -/
def parseRows (s : String) : List (List (Fin 70)) :=
  (s.splitOn "\n").filterMap fun line =>
    let ws := (line.splitOn " ").filter (· ≠ "")
    if ws.isEmpty then none else ws.mapM parseState

@[irreducible] def R0_15 : List (List (Fin 70)) := parseRows rowsText

end N66E15
