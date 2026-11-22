import RowEnc.DataT
import RowEnc.DataC

/-!
# RowEnc.Main: the printer `rowprint`

* `rowprint t <k>` / `rowprint c <k>`: writes `certText` of template / core `k` (`render (nvOf n) (certCnf t)`).
* `rowprint st <k> <file>` / `rowprint sc <k> <file>`: writes `subText` for the 0-based clause indices listed in
  `file` (one per line), i.e. `render (nvOf n) (subCnf t idx)`; refuses (exit 1, no output) if an index is out of
  range. Used for VB's trimmed certificate of the n = 29 template (`lrattrim` keeps original clauses verbatim and
  in order). Soundness never depends on the index list (`subCnf_mem`, RowEnc.Bridge).
-/

open RowEnc

def certOf (kind : String) (k : Nat) : Option Cert :=
  if kind == "t" || kind == "st" then templates[k]? else if kind == "c" || kind == "sc" then cores[k]? else none

def main (args : List String) : IO UInt32 := do
  let out ← IO.getStdout
  match args with
  | [kind, ks] =>
    match ks.toNat? >>= certOf kind with
    | some t => out.putStr (certText t); out.flush; return 0
    | none => IO.eprintln "bad arguments"; return 2
  | [kind, ks, file] =>
    match ks.toNat? >>= certOf kind with
    | some t =>
      let txt ← IO.FS.readFile file
      let idx := ((txt.splitOn "\n").filter (· ≠ "")).filterMap String.toNat?
      match subCnfChecked t idx with
      | some F => out.putStr (EncB.render (nvOf t.n) F); out.flush; return 0
      | none => IO.eprintln "index out of range"; return 1
    | none => IO.eprintln "bad arguments"; return 2
  | _ => IO.eprintln "usage: rowprint (t|c) k | (st|sc) k indexfile"; return 2
