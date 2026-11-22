import V182Enc.Gen

/-!
# v182print: the printer exe

* `stats` — sizes (families, cycles, pieces) and the two stars, for the M1 controls.
* `base` — the text of B: `EncB.render nVars baseCnf`.
* `list` — the 4,404 pieces, one per line: `index n m` (`m = -` for a direct Y1 piece).
* `piece I` — **the text of piece I**: `pieceText pieces[I]` (exit 1, nothing on stdout, if `I` is out of range).
* `all DIR` — writes `pieceText pieces[I]` to `DIR/I.cnf` for every I (the M9 path; same bytes as `piece I`).
* `cube N M` — control only (not on the trust path): `pieceText (N, some M)`, or `pieceText (N, none)` for `M = -`,
  for any `N`, `M`, listed or not.
-/

open V182Enc

def main (args : List String) : IO UInt32 := do
  let out ← IO.getStdout
  let err ← IO.getStderr
  match args with
  | ["stats"] =>
    out.putStrLn s!"fourMasks {fourMasks.length} threeMasks {threeMasks.length} vtxMasks {vtxMasks.length} cycles {cycles.length}"
    out.putStrLn s!"alo {aloCls.length} conf {confCls.length} amo {amoCls.length} surj {surjCls.length} units {unitCls.length} base {baseCnf.length}"
    out.putStrLn s!"star47 {star 47} star55 {star 55} star7 {star 7} star31 {star 31}"
    out.putStrLn s!"perms5 {perms5.length} first {perms5.head?} last {perms5.getLast?} pieces {pieces.length}"
    return 0
  | ["base"] =>
    out.putStr baseText
    return 0
  | ["list"] =>
    let mut i := 0
    for q in pieces do
      out.putStrLn s!"{i} {q.1} {match q.2 with | some m => toString m | none => "-"}"
      i := i + 1
    return 0
  | ["piece", s] =>
    let some i := s.toNat? | err.putStrLn "bad index"; return 1
    let some q := pieces[i]? | err.putStrLn "no such piece"; return 1
    out.putStr (pieceText q)
    return 0
  | ["cube", sn, sm] =>
    let some n := sn.toNat? | err.putStrLn "bad N"; return 1
    let m := sm.toNat?
    if m.isNone && sm != "-" then err.putStrLn "bad M"; return 1
    out.putStr (pieceText (n, m))
    return 0
  | ["all", dir] =>
    let mut i := 0
    for q in pieces do
      let h ← IO.FS.Handle.mk s!"{dir}/{i}.cnf" IO.FS.Mode.write
      h.putStr (pieceText q)
      h.flush
      i := i + 1
    err.putStrLn s!"wrote {i} pieces"
    return 0
  | _ =>
    err.putStrLn "usage: v182print stats | base | list | piece I | cube N M | all DIR"
    return 1
