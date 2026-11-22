import EncB.Render
import RowEnc.Enc
import Res118.Rows

/-!
# rowprint: the printer exe

* `row B I` — **trust path**: writes `RowEnc.rowText s` with `s = rows[I]` for the Lean list `rows` of block
  `B ∈ {P, Q, U, A}` (`Res118.rowsP/Q/U/A`, the lists `BlockValid` quantifies over); refuses (exit 1, nothing on
  stdout) for an unknown block or an index out of range. One `putStr` of the whole string.
* `list B` — one line per row of block `B`: `I a,b,c,…` (the support), for the binding script.
* `sup a b c …` — control only (not on the trust path): the text for a support given on the command line.
* `stats a b c …` — control only: `nv nc` of `rowCnf` for that support.
-/

def blockRows : String → Option (List (List Nat))
  | "P" => some Res118.rowsP
  | "Q" => some Res118.rowsQ
  | "U" => some Res118.rowsU
  | "A" => some Res118.rowsA
  | _ => none

def main (args : List String) : IO UInt32 := do
  let out ← IO.getStdout
  let err ← IO.getStderr
  match args with
  | ["row", b, idx] =>
    let some rows := blockRows b | err.putStrLn "unknown block"; return 1
    let some i := idx.toNat? | err.putStrLn "bad index"; return 1
    let some s := rows[i]? | err.putStrLn "no such row"; return 1
    out.putStr (RowEnc.rowText s)
    return 0
  | ["list", b] =>
    let some rows := blockRows b | err.putStrLn "unknown block"; return 1
    let mut i := 0
    for s in rows do
      out.putStrLn s!"{i} {",".intercalate (s.map toString)}"
      i := i + 1
    return 0
  | "sup" :: xs =>
    let some s := xs.mapM String.toNat? | err.putStrLn "bad support"; return 1
    out.putStr (RowEnc.rowText s)
    return 0
  | "stats" :: xs =>
    let some s := xs.mapM String.toNat? | err.putStrLn "bad support"; return 1
    out.putStrLn s!"{RowEnc.rowNv s} {(RowEnc.rowCnf s).length}"
    return 0
  | _ =>
    err.putStrLn "usage: rowprint row B I | list B | sup a b … | stats a b …"
    return 2
