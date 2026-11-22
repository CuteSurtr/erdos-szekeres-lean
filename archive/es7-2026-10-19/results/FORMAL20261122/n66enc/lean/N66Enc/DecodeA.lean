import N66Enc.Atoms

/-!
# N66Enc.Decode: model transfer for the numbering (Std-only)

For any meaning `m : Atom → Bool` of the atoms, `decodeNum m : Nat → Bool` is an assignment of DIMACS variables with
`decodeNum m (num a) = m a` for **every** atom (`decodeNum_num`). Hence a structured clause list in which every
clause has a literal that agrees with `m` becomes, through `toDimacs`, a satisfied DIMACS list
(`dimacsSat_of_holds`). Soundness never depends on the numbers being Python's (ENCBLEAN D4): allocated atoms are
decoded through `EncB.decode`/`EncB.decode_numberMap`, the others through their own code (`Atom.ofCode_code`).
-/

namespace N66Enc
open Atom

theorem d70_val (x : Nat) : (d70 x).val = x % 70 := rfl

set_option maxRecDepth 8000 in
/-- `ofCode` inverts `code` (the large literals need a recursion depth above the default). -/
theorem ofCode_code (a : Atom) : ofCode a.code = a := by
  cases a with
  | before i j =>
    have hi := i.isLt; have hj := j.isLt
    have hc : (before i j).code = i.val * 70 + j.val := rfl
    unfold ofCode
    rw [hc, if_pos (by omega)]
    simp only [Atom.before.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_⟩ <;> omega
  | capGe i j k =>
    have hi := i.isLt; have hj := j.isLt; have hk := k.isLt
    have hc : (capGe i j k).code = 4900 + (i.val * 70 + j.val) * 5 + k.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_pos (by omega)]
    simp only [Atom.capGe.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | cupGe i j k =>
    have hi := i.isLt; have hj := j.isLt; have hk := k.isLt
    have hc : (cupGe i j k).code = 29400 + (i.val * 70 + j.val) * 5 + k.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.cupGe.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | orient i j k =>
    have hi := i.isLt; have hj := j.isLt; have hk := k.isLt
    have hc : (orient i j k).code = 53900 + (i.val * 70 + j.val) * 70 + k.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.orient.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_, ?_⟩ <;> omega
  | convex i j k l =>
    have hi := i.isLt; have hj := j.isLt; have hk := k.isLt; have hl := l.isLt
    have hc : (convex i j k l).code = 396900 + ((i.val * 70 + j.val) * 70 + k.val) * 70 + l.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.convex.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_, ?_, ?_⟩ <;> omega
  | sel s =>
    have hs := s.isLt
    have hc : (sel s).code = 24406900 + s.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.sel.injEq, Fin.ext_iff, d70_val]
    omega
  | chC k a b c =>
    have hk := k.isLt; have ha := a.isLt; have hb := b.isLt; have hc := c.isLt
    have hc : (chC k a b c).code = 24406970 + ((k.val * 70 + a.val) * 70 + b.val) * 70 + c.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.chC.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_, ?_, ?_⟩ <;> omega
  | chU k a b c =>
    have hk := k.isLt; have ha := a.isLt; have hb := b.isLt; have hc := c.isLt
    have hc : (chU k a b c).code = 26464970 + ((k.val * 70 + a.val) * 70 + b.val) * 70 + c.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.chU.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_, ?_, ?_⟩ <;> omega
  | ce p q =>
    have hp := p.isLt; have hq := q.isLt
    have hc : (ce p q).code = 28522970 + p.val * 70 + q.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.ce.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_⟩ <;> omega
  | ue p q =>
    have hp := p.isLt; have hq := q.isLt
    have hc : (ue p q).code = 28527870 + p.val * 70 + q.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.ue.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_⟩ <;> omega
  | cnt a j =>
    have ha := a.isLt; have hj := j.isLt
    have hc : (cnt a j).code = 28532770 + a.val * 15 + j.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_pos (by omega)]
    simp only [Atom.cnt.injEq, Fin.ext_iff, d70_val]
    refine ⟨?_, ?_⟩ <;> omega
  | sbe j =>
    have hj := j.isLt
    have hc : (sbe j).code = 28533790 + j.val := rfl
    unfold ofCode
    rw [hc, if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega), if_neg (by omega)]
    simp only [Atom.sbe.injEq, Fin.ext_iff, d70_val]
    omega

end N66Enc
