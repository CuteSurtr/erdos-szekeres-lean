import N66Enc.Clauses

/-!
# N66Enc.Rows: R0, the row supports used by the 132 certificates (Std-only)

`data/rows_used.txt` (507,715 bytes, SHA-256 `236e46de…3018a609`) has one sorted support per line: the 11,884
distinct supports of the row clauses of the 132 trims, in the order of `mono/rows_1832.json`
(SHA-256 `80bec1b4…6b61f33`; every used row is in it). `R0` is its parse. The theorem quantifies over the row list
and assumes `RowsValid R0`; the printer prints row clauses only from `R0`, so the trims' rows are members by
construction. The kernel never evaluates `R0`.
-/

namespace N66Enc

@[irreducible] def rowsText : String := include_str "data/rows_used.txt"

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

@[irreducible] def R0 : List (List (Fin 70)) := parseRows rowsText

end N66Enc
