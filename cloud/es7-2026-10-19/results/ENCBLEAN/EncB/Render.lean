import EncB.Coded
import EncB.Cover

/-!
# M9 (trust items E3/E4): the DIMACS text of the twin, a reference parser, and the round trip (Std-only)

`encb_dimacs` writes the CNF files of the trust path (`twin-base`, `twin-cube64`; also `twin-cube`, `twin-cubes64`)
with the functions of this file and nothing else:

* `pushNat` / `pushInt`: a decimal printer written here (recursion on the value, plain `String.push`), so the
  exe no longer calls core's `toString` on `Nat`/`Int` for the trust path. Core's `toString` cannot be reasoned
  about for negative numbers: `toString (Int.negSucc m)` is `String.Internal.append "-" …`
  (`Init/Data/ToString/Basic.lean:95`), and `String.Internal.append` is an `opaque` with no body
  (`Init/Data/String/Bootstrap.lean:69-70`). For `Nat` the kernel definition agrees (`pushNat_eq_append_toString`),
  but the compiled code is `Nat.reprFast` (`@[implemented_by]`, `Init/Data/Repr.lean:243`), which for `n < 2^64`
  uses the C function `lean_string_of_usize` (directly or through a memo table). Neither is used by the twin
  printer any more; the switch kept every byte (A1 exe against A2 exe on all modes, and the hash binding 68/68,
  `logs/m9_a2_regress_modes.log`, `logs/m9_a2_hash_binding.log`).
* `pushClauseR`, `bodyR`, `headerR`, `cubeBodyR`, `renderCube`, `cnfText`: the layout of gen_b2.py:191-194
  (`p cnf nv nc`, then `' '.join(map(str, cl)) + ' 0\n'` per clause) and of mkcubes.py:11-15 (units appended as
  one-literal clauses, header count raised).

`parseDimacs` is a reference parser for the plain DIMACS subset written by this printer: the line
`p cnf <nv> <nc>`, then exactly `nc` clause lines, each `l₁ l₂ … lₖ 0` (single spaces, `k ≥ 0`; for `k = 0` the
line is ` 0`, as Python prints it), each literal a nonzero decimal with no leading zero and no `+`, an optional
`-`, and `|l| ≤ nv`; every line ends with `\n`; nothing else (no comment lines, no blank lines, no tabs, no `\r`,
no trailing text). It is a deterministic automaton (`bodyStep`) over the characters. The HOL4/CakeML source of
cake_lpr's parser was not found on this machine (the `HOL/` and `cakeml/` submodules of the clone
`/home/jay/research/sat/tools/cake_lpr` at commit `033aad53` are empty, and the cake_lpr part of
`C2P/vendor/tools-src.tar.xz` is `cake_lpr.S`, `basis_ffi.c`, the Makefile, README and examples), so the accepted
language is not modelled on it with file:line citations; it is the plain subset above. Evidence only:
`logs/m9_a2_cake_parse.log` (cake_lpr's printout of what it parsed is byte-identical to 21 twin texts and to
(6,8,11) samples; it rejects or reads in the standard way the 13 texts `parseDimacs` rejects below).

**Theorems.**
* `parseDimacs_render`: for every `F` whose literals are nonzero with `natAbs ≤ nv`,
  `parseDimacs (render nv F) = some (nv, F)`.
* `renderCube_eq`: `renderCube nv F (bodyR F) cube = render nv (cubeCnf F cube)`; with `parseDimacs_renderCube`.
* `cnfText_encode` (by definition): `cnfText (encode m K t) cube`, the exact expression whose value `twin-base`
  (`cube = []`) and `twin-cube64` (`cube = cubes64.get i`) write to stdout, is
  `renderCube (numVars m K t) (encB m K t) (bodyR (encB m K t)) cube`.
* `parseDimacs_cube64`, `parseDimacs_cube64_get`, `parseDimacs_base6811`: the instance (6,8,11), derived from
  `encB_wf` and a symbolic bound `45 ≤ numVars 6 8 11` (the 45 Y codes are allocated first, `prefixCodes`); nothing
  evaluates `encB 6 8 11`.
* `cubesUnsat64_of_texts` / `encB_unsat_of_texts`: if each of the 64 printed texts parses to an unsatisfiable
  formula, then `CubesUnsat64` and `¬ DimacsSatisfiable (encB 6 8 11)`. `cubesUnsat64_of_texts_get` /
  `encB_unsat_of_texts_get` state the same with the hypothesis by index, on the exact expression
  `cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)` that `twin-cube64 6 8 11 i` prints and `scripts/hash_binding.sh`
  hashes.
* `render_ascii`, `cnfText_bytes`: every character of the text is ASCII, so its UTF-8 encoding (`String.toUTF8`,
  what `putStr` writes) is one byte per character, the character's code.
-/

namespace EncB

/-! ## The decimal printer -/

/-- The decimal digits of `n`, most significant first, no leading zero (`= Nat.toDigits 10 n`,
`natDigits_eq_toDigits`). The specification of `pushNat`; never run by the exe. -/
def natDigits (n : Nat) : List Char :=
  if n < 10 then [Nat.digitChar n] else natDigits (n / 10) ++ [Nat.digitChar (n % 10)]
termination_by n
decreasing_by omega

/-- The characters of an integer: the digits of `|x|`, after a `-` if `x < 0`. -/
def intChars : Int → List Char
  | .ofNat n => natDigits n
  | .negSucc n => '-' :: natDigits (n + 1)

/-- Append the decimal digits of `n` to `s` (the exe's printer for natural numbers). -/
def pushNat (s : String) (n : Nat) : String :=
  if n < 10 then s.push (Nat.digitChar n) else (pushNat s (n / 10)).push (Nat.digitChar (n % 10))
termination_by n
decreasing_by omega

/-- Append the decimal form of `x` to `s` (the exe's printer for literals). -/
def pushInt (s : String) : Int → String
  | .ofNat n => pushNat s n
  | .negSucc n => pushNat (s.push '-') (n + 1)

theorem pushNat_data (s : String) (n : Nat) : (pushNat s n).data = s.data ++ natDigits n := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    rw [pushNat, natDigits]
    by_cases h : n < 10
    · rw [if_pos h, if_pos h, String.data_push]
    · rw [if_neg h, if_neg h, String.data_push, ih (n / 10) (by omega), List.append_assoc]

theorem pushInt_data (s : String) (x : Int) : (pushInt s x).data = s.data ++ intChars x := by
  cases x with
  | ofNat n => simp only [pushInt, intChars, pushNat_data]
  | negSucc n => simp only [pushInt, intChars, pushNat_data, String.data_push, List.append_assoc,
      List.singleton_append]

/-! ### Agreement with core's printer on `Nat` (kernel definitions) -/

theorem toDigitsCore_ten : ∀ (fuel n : Nat) (ds : List Char), n < fuel →
    Nat.toDigitsCore 10 fuel n ds = natDigits n ++ ds
  | 0, n, _, h => absurd h (Nat.not_lt_zero n)
  | fuel + 1, n, ds, h => by
    rw [Nat.toDigitsCore]
    by_cases h10 : n < 10
    · have h0 : n / 10 = 0 := Nat.div_eq_of_lt h10
      have hm : n % 10 = n := Nat.mod_eq_of_lt h10
      rw [natDigits, if_pos h10]
      simp only [h0, if_true, hm, List.singleton_append]
    · have h0 : n / 10 ≠ 0 := by omega
      rw [natDigits, if_neg h10]
      simp only [h0, if_false]
      rw [toDigitsCore_ten fuel (n / 10) _ (by omega)]
      simp only [List.append_assoc, List.singleton_append]

/-- The digits are core's `Nat.toDigits 10` (the kernel definition behind `toString` on `Nat`). -/
theorem natDigits_eq_toDigits (n : Nat) : natDigits n = Nat.toDigits 10 n := by
  rw [Nat.toDigits, toDigitsCore_ten (n + 1) n [] (Nat.lt_succ_self n), List.append_nil]

/-- On `Nat`, `pushNat` is `s ++ toString n` as kernel definitions (core's compiled `Nat.repr` is `reprFast`,
`@[implemented_by]`, which this theorem does not see; the exe does not call it on the trust path). -/
theorem pushNat_eq_append_toString (s : String) (n : Nat) : pushNat s n = s ++ toString n := by
  apply String.ext
  rw [pushNat_data, String.data_append, natDigits_eq_toDigits]
  rfl

/-! ## The CNF text -/

/-- Append one clause line `' '.join(map(str, cl)) + ' 0\n'` (gen_b2.py:193) to `s`. -/
def pushClauseR (s : String) (cl : List Int) : String :=
  match cl with
  | [] => ((s.push ' ').push '0').push '\n'
  | l :: ls => (((ls.foldl (fun acc x => pushInt (acc.push ' ') x) (pushInt s l)).push ' ').push '0').push '\n'

/-- The clause lines of `F` (everything after the header). -/
def bodyR (F : List (List Int)) : String := F.foldl pushClauseR ""

/-- The header line `p cnf nv nc` (gen_b2.py:192). -/
def headerR (nv nc : Nat) : String := (pushNat ((pushNat "p cnf " nv).push ' ') nc).push '\n'

/-- The clause lines of a cube file after the header: the base lines `bodyF`, then one line `u 0` per unit
(mkcubes.py:13-15). -/
def cubeBodyR (bodyF : String) (cube : List Int) : String := (cube.map fun z => [z]).foldl pushClauseR bodyF

/-- **The CNF text of `F` with header count `nv`.** -/
def render (nv : Nat) (F : List (List Int)) : String := headerR nv F.length ++ bodyR F

/-- **What the exe writes for a cube** (`cube = []`: the base file): the header of `cubeCnf F cube`, then
`cubeBodyR bodyF cube`. The exe passes `bodyF = bodyR F`, computed once (`renderCube_eq`). -/
def renderCube (nv : Nat) (F : List (List Int)) (bodyF : String) (cube : List Int) : String :=
  headerR nv (cubeCnf F cube).length ++ cubeBodyR bodyF cube

/-- **The text `twin-base` (`cube = []`), `twin-cube` and `twin-cube64` write to stdout** for the encoding `e`
(the exe calls exactly `out.putStr (cnfText e cube)` with `e = encode M K T`, see `EncB/Emit.lean`). -/
def cnfText (e : Enc) (cube : List Int) : String := renderCube e.nv e.clauses (bodyR e.clauses) cube

/-- The exe's text for `encode m K t` is the rendering of the theorem's objects `numVars`/`encB` (by definition;
generic in `m K t`, nothing is evaluated). -/
theorem cnfText_encode (m K t : Nat) (cube : List Int) :
    cnfText (encode m K t) cube = renderCube (numVars m K t) (encB m K t) (bodyR (encB m K t)) cube := rfl

/-- The base is the empty cube: `cubeCnf F [] = F`. -/
theorem cubeCnf_nil (F : List (List Int)) : cubeCnf F [] = F := by
  simp only [cubeCnf, List.map_nil, List.append_nil]

/-- What the exe prints for a cube is the rendering of the clause list `cubeCnf F cube` of the theorems. -/
theorem renderCube_eq (nv : Nat) (F : List (List Int)) (cube : List Int) :
    renderCube nv F (bodyR F) cube = render nv (cubeCnf F cube) := by
  simp only [renderCube, render, cubeBodyR, bodyR, cubeCnf, List.foldl_append]

/-! ### The characters of the text -/

/-- The characters of one clause line. For `l :: ls` this is `l ls₁ … lsₖ 0\n` written as "each literal followed
by a space, then `0\n`" (`pushClauseR_data` shows it is the joined form the printer builds). -/
def clauseChars : List Int → List Char
  | [] => [' ', '0', '\n']
  | l :: ls => (l :: ls).flatMap (fun x => intChars x ++ [' ']) ++ ['0', '\n']

/-- The characters of the header line. -/
def headerChars (nv nc : Nat) : List Char :=
  ['p', ' ', 'c', 'n', 'f', ' '] ++ natDigits nv ++ ' ' :: (natDigits nc ++ ['\n'])

theorem join_spaces (f : Int → List Char) : ∀ (l : Int) (ls : List Int),
    f l ++ ls.flatMap (fun x => ' ' :: f x) ++ [' '] = (l :: ls).flatMap (fun x => f x ++ [' '])
  | l, [] => by simp
  | l, x :: xs => by
    have ih := join_spaces f x xs
    simp only [List.flatMap_cons] at ih ⊢
    rw [← ih]
    simp only [List.append_assoc, List.cons_append, List.nil_append]

theorem foldl_pushLit_data (ls : List Int) (acc : String) :
    (ls.foldl (fun acc x => pushInt (acc.push ' ') x) acc).data =
      acc.data ++ ls.flatMap (fun x => ' ' :: intChars x) := by
  induction ls generalizing acc with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldl_cons, ih, pushInt_data, String.data_push, List.flatMap_cons, List.append_assoc,
      List.cons_append, List.nil_append]

theorem pushClauseR_data (s : String) (cl : List Int) : (pushClauseR s cl).data = s.data ++ clauseChars cl := by
  cases cl with
  | nil => simp [pushClauseR, clauseChars]
  | cons l ls =>
    simp only [pushClauseR, clauseChars, String.data_push, foldl_pushLit_data, pushInt_data]
    rw [← join_spaces intChars l ls]
    simp only [List.append_assoc, List.cons_append, List.nil_append]

theorem foldl_pushClauseR_data (F : List (List Int)) (s : String) :
    (F.foldl pushClauseR s).data = s.data ++ F.flatMap clauseChars := by
  induction F generalizing s with
  | nil => simp
  | cons cl F ih => simp only [List.foldl_cons, ih, pushClauseR_data, List.flatMap_cons, List.append_assoc]

theorem headerR_data (nv nc : Nat) : (headerR nv nc).data = headerChars nv nc := by
  simp only [headerR, headerChars, String.data_push, pushNat_data, List.append_assoc, List.cons_append]
  rfl

theorem headerChars_append (nv nc : Nat) (B : List Char) :
    headerChars nv nc ++ B = ['p', ' ', 'c', 'n', 'f', ' '] ++ (natDigits nv ++ ' ' :: (natDigits nc ++ '\n' :: B)) := by
  simp only [headerChars, List.append_assoc, List.cons_append, List.nil_append]

theorem render_data (nv : Nat) (F : List (List Int)) :
    (render nv F).data = headerChars nv F.length ++ F.flatMap clauseChars := by
  rw [render, String.data_append, headerR_data, bodyR, foldl_pushClauseR_data]
  rfl

/-! ## The reference parser -/

/-- The value of a decimal digit character. -/
def digitVal (c : Char) : Nat := c.toNat - 48

/-- `'1'` to `'9'`. -/
def isPosDigit (c : Char) : Bool := c.isDigit && c != '0'

/-- One digit more: `10 · a + digit`. -/
def dstep (a : Nat) (c : Char) : Nat := 10 * a + digitVal c

/-- Remove the prefix `p`; `none` if `cs` does not start with it. -/
def stripPrefix : List Char → List Char → Option (List Char)
  | [], cs => some cs
  | _ :: _, [] => none
  | p :: ps, c :: cs => if c = p then stripPrefix ps cs else none

/-- Digits up to the terminator `term`, accumulated onto `v`. -/
def natRun (term : Char) (v : Nat) : List Char → Option (Nat × List Char)
  | [] => none
  | c :: cs => if c = term then some (v, cs) else if c.isDigit then natRun term (dstep v c) cs else none

/-- A natural number without leading zero (`0` or `[1-9][0-9]*`) followed by `term`; returns the rest. -/
def parseNatTerm (term : Char) : List Char → Option (Nat × List Char)
  | [] => none
  | c :: cs =>
    if c = '0' then
      match cs with
      | d :: ds => if d = term then some (0, ds) else none
      | [] => none
    else if c.isDigit then natRun term (digitVal c) cs else none

/-- The states of the clause-line automaton. -/
inductive LineMode where
  /-- at the beginning of a line -/
  | start
  /-- after the space that begins the empty clause ` 0` -/
  | lead
  /-- after `-` -/
  | neg
  /-- in the digits of a literal (negative iff `neg`), value so far `v` -/
  | num (neg : Bool) (v : Nat)
  /-- after the space that ends a literal -/
  | sep
  /-- after the terminating `0` -/
  | zero
  deriving DecidableEq, Repr

/-- The parser state: the mode, the literals of the current line (last first) and the finished clauses (last
first). -/
structure PState where
  mode : LineMode
  cur : List Int
  done : List (List Int)
  deriving DecidableEq, Repr

/-- The start of a literal: `-` or `1`–`9`. -/
def litStart (st : PState) (c : Char) : Option PState :=
  if c = '-' then some { st with mode := .neg }
  else if isPosDigit c then some { st with mode := .num false (digitVal c) }
  else none

/-- One character of the clause lines. `none` rejects. -/
def bodyStep (nv : Nat) (st : PState) (c : Char) : Option PState :=
  match st.mode with
  | .start => if c = ' ' then some { st with mode := .lead } else litStart st c
  | .lead => if c = '0' then some { st with mode := .zero } else none
  | .neg => if isPosDigit c then some { st with mode := .num true (digitVal c) } else none
  | .num b v =>
    if c.isDigit then some { st with mode := .num b (dstep v c) }
    else if c = ' ' ∧ v ≤ nv then some { st with mode := .sep, cur := (if b then -(v : Int) else v) :: st.cur }
    else none
  | .sep => if c = '0' then some { st with mode := .zero } else litStart st c
  | .zero => if c = '\n' then some ⟨.start, [], st.cur.reverse :: st.done⟩ else none

/-- Run the automaton over the clause lines. -/
def runBody (nv : Nat) : PState → List Char → Option PState
  | st, [] => some st
  | st, c :: cs => (bodyStep nv st c).bind fun st' => runBody nv st' cs

/-- **The reference parser** on characters: header `p cnf <nv> <nc>`, then exactly `nc` clause lines. -/
def parseDimacsChars (cs : List Char) : Option (Nat × List (List Int)) :=
  match stripPrefix ['p', ' ', 'c', 'n', 'f', ' '] cs with
  | none => none
  | some r1 =>
    match parseNatTerm ' ' r1 with
    | none => none
    | some (nv, r2) =>
      match parseNatTerm '\n' r2 with
      | none => none
      | some (nc, r3) =>
        match runBody nv ⟨.start, [], []⟩ r3 with
        | none => none
        | some st => if st.mode = .start ∧ st.done.length = nc then some (nv, st.done.reverse) else none

/-- **The reference parser**: `some (nv, F)` iff the text is the plain DIMACS file of `F` with header count `nv`. -/
def parseDimacs (s : String) : Option (Nat × List (List Int)) := parseDimacsChars s.data

/-! ### Rejections (kernel-checked examples of what is outside the subset) -/

theorem parseDimacs_example : parseDimacs "p cnf 3 3\n1 -2 0\n 0\n3 0\n" = some (3, [[1, -2], [], [3]]) := by
  decide
/-- wrong clause count -/
theorem parseDimacs_rejects_count : parseDimacs "p cnf 3 2\n1 -2 0\n" = none := by decide
/-- literal `0` inside a clause -/
theorem parseDimacs_rejects_inner_zero : parseDimacs "p cnf 3 1\n1 0 2 0\n" = none := by decide
/-- variable `> nv` -/
theorem parseDimacs_rejects_big_var : parseDimacs "p cnf 3 1\n-4 0\n" = none := by decide
/-- leading zero in a literal, in the header -/
theorem parseDimacs_rejects_leading_zero : parseDimacs "p cnf 3 1\n01 0\n" = none := by decide
theorem parseDimacs_rejects_leading_zero_header : parseDimacs "p cnf 03 1\n1 0\n" = none := by decide
/-- `-0` -/
theorem parseDimacs_rejects_neg_zero : parseDimacs "p cnf 3 1\n-0 0\n" = none := by decide
/-- two spaces, a leading space, a missing final newline, a blank line, a bare `0` line, a comment line, `+1` -/
theorem parseDimacs_rejects_double_space : parseDimacs "p cnf 3 1\n1  0\n" = none := by decide
theorem parseDimacs_rejects_leading_space : parseDimacs "p cnf 3 1\n 1 0\n" = none := by decide
theorem parseDimacs_rejects_no_newline : parseDimacs "p cnf 3 1\n1 0" = none := by decide
theorem parseDimacs_rejects_blank_line : parseDimacs "p cnf 3 1\n1 0\n\n" = none := by decide
theorem parseDimacs_rejects_bare_zero : parseDimacs "p cnf 3 1\n0\n" = none := by decide
theorem parseDimacs_rejects_comment : parseDimacs "c x\np cnf 3 1\n1 0\n" = none := by decide
theorem parseDimacs_rejects_plus : parseDimacs "p cnf 3 1\n+1 0\n" = none := by decide

/-! ### Digits -/

theorem digitChar_facts : ∀ d : Nat, d < 10 →
    (Nat.digitChar d).isDigit = true ∧ digitVal (Nat.digitChar d) = d ∧ (0 < d → isPosDigit (Nat.digitChar d) = true)
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | 3, _ => by decide
  | 4, _ => by decide
  | 5, _ => by decide
  | 6, _ => by decide
  | 7, _ => by decide
  | 8, _ => by decide
  | 9, _ => by decide
  | _ + 10, h => absurd h (by omega)

theorem natDigits_isDigit (n : Nat) : ∀ c ∈ natDigits n, c.isDigit = true := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    rw [natDigits]
    by_cases h : n < 10
    · rw [if_pos h]
      intro c hc
      rw [List.mem_singleton.1 hc]
      exact (digitChar_facts n h).1
    · rw [if_neg h]
      intro c hc
      rcases List.mem_append.1 hc with hc | hc
      · exact ih (n / 10) (by omega) c hc
      · rw [List.mem_singleton.1 hc]
        exact (digitChar_facts (n % 10) (Nat.mod_lt n (by omega))).1

theorem natDigits_val (n : Nat) : (natDigits n).foldl dstep 0 = n := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    rw [natDigits]
    by_cases h : n < 10
    · rw [if_pos h]
      simp only [List.foldl_cons, List.foldl_nil, dstep, (digitChar_facts n h).2.1, Nat.mul_zero, Nat.zero_add]
    · rw [if_neg h, List.foldl_append, ih (n / 10) (by omega)]
      simp only [List.foldl_cons, List.foldl_nil, dstep, (digitChar_facts (n % 10) (Nat.mod_lt n (by omega))).2.1]
      omega

theorem natDigits_zero : natDigits 0 = ['0'] := by
  rw [natDigits, if_pos (by decide)]
  rfl

theorem natDigits_pos (n : Nat) (hn : 0 < n) : ∃ d ds, natDigits n = d :: ds ∧ isPosDigit d = true := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    rw [natDigits]
    by_cases h : n < 10
    · rw [if_pos h]
      exact ⟨_, [], rfl, (digitChar_facts n h).2.2 hn⟩
    · rw [if_neg h]
      obtain ⟨d, ds, he, hd⟩ := ih (n / 10) (by omega) (by omega)
      exact ⟨d, ds ++ [Nat.digitChar (n % 10)], by rw [he, List.cons_append], hd⟩

theorem isPosDigit_isDigit {c : Char} (h : isPosDigit c = true) : c.isDigit = true := by
  simp only [isPosDigit, Bool.and_eq_true] at h
  exact h.1

theorem isPosDigit_ne_zero {c : Char} (h : isPosDigit c = true) : c ≠ '0' := by
  simp only [isPosDigit, Bool.and_eq_true, bne_iff_ne, ne_eq] at h
  exact h.2

theorem ne_of_isDigit {c d : Char} (hc : c.isDigit = true) (hd : d.isDigit = false) : c ≠ d := by
  intro e
  rw [e, hd] at hc
  exact Bool.false_ne_true hc

theorem space_not_digit : ' '.isDigit = false := by decide
theorem minus_not_digit : '-'.isDigit = false := by decide
theorem newline_not_digit : '\n'.isDigit = false := by decide

/-! ### The header -/

theorem stripPrefix_append : ∀ (p rest : List Char), stripPrefix p (p ++ rest) = some rest
  | [], _ => rfl
  | c :: ps, rest => by
    simp only [List.cons_append, stripPrefix, if_true]
    exact stripPrefix_append ps rest

theorem natRun_digits (term : Char) (ht : term.isDigit = false) (rest : List Char) :
    ∀ (ds : List Char) (v : Nat), (∀ c ∈ ds, c.isDigit = true) →
      natRun term v (ds ++ term :: rest) = some (ds.foldl dstep v, rest)
  | [], v, _ => by simp [natRun]
  | c :: cs, v, h => by
    have hc : c.isDigit = true := h c List.mem_cons_self
    simp only [List.cons_append, natRun, ne_of_isDigit hc ht, if_false, hc, if_true, List.foldl_cons]
    exact natRun_digits term ht rest cs (dstep v c) (fun x hx => h x (List.mem_cons_of_mem c hx))

theorem parseNatTerm_natDigits (term : Char) (ht : term.isDigit = false) (n : Nat) (rest : List Char) :
    parseNatTerm term (natDigits n ++ term :: rest) = some (n, rest) := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · rw [natDigits_zero]
    simp [parseNatTerm]
  · obtain ⟨d, ds, he, hd⟩ := natDigits_pos n hn
    have hall := natDigits_isDigit n
    rw [he] at hall
    have hval := natDigits_val n
    rw [he, List.foldl_cons] at hval
    rw [he, List.cons_append]
    simp only [parseNatTerm, isPosDigit_ne_zero hd, if_false, isPosDigit_isDigit hd, if_true]
    rw [natRun_digits term ht rest ds _ (fun c hc => hall c (List.mem_cons_of_mem d hc))]
    have h0 : dstep 0 d = digitVal d := by simp [dstep]
    rw [← h0, hval]

/-! ### The clause lines -/

theorem runBody_append (nv : Nat) : ∀ (xs ys : List Char) (st : PState),
    runBody nv st (xs ++ ys) = (runBody nv st xs).bind fun st' => runBody nv st' ys
  | [], ys, st => rfl
  | c :: cs, ys, st => by
    simp only [List.cons_append, runBody]
    cases bodyStep nv st c with
    | none => rfl
    | some st' => exact runBody_append nv cs ys st'

theorem runBody_cons_of {nv : Nat} {st st' : PState} {c : Char} {cs : List Char}
    (h : bodyStep nv st c = some st') : runBody nv st (c :: cs) = runBody nv st' cs := by
  simp only [runBody, h, Option.bind_some]

theorem runBody_digits (nv : Nat) (b : Bool) (cur : List Int) (done : List (List Int)) :
    ∀ (ds : List Char) (v : Nat), (∀ c ∈ ds, c.isDigit = true) →
      runBody nv ⟨.num b v, cur, done⟩ ds = some ⟨.num b (ds.foldl dstep v), cur, done⟩
  | [], v, _ => rfl
  | c :: cs, v, h => by
    have hc : c.isDigit = true := h c List.mem_cons_self
    have hs : bodyStep nv ⟨.num b v, cur, done⟩ c = some ⟨.num b (dstep v c), cur, done⟩ := by
      simp only [bodyStep, hc, if_true]
    rw [runBody_cons_of hs, List.foldl_cons]
    exact runBody_digits nv b cur done cs (dstep v c) (fun x hx => h x (List.mem_cons_of_mem c hx))

/-- The modes in which a literal may begin. -/
def LitReady : LineMode → Prop
  | .start => True
  | .sep => True
  | _ => False

theorem bodyStep_ready {nv : Nat} {m : LineMode} (hm : LitReady m) {cur : List Int} {done : List (List Int)}
    {c : Char} (h1 : c ≠ ' ') (h2 : c ≠ '0') : bodyStep nv ⟨m, cur, done⟩ c = litStart ⟨m, cur, done⟩ c := by
  cases m <;> simp_all [LitReady, bodyStep]

/-- A literal followed by a space, read where a literal may begin, ends in `sep` with the literal pushed. -/
theorem runBody_lit {nv : Nat} {m : LineMode} (hm : LitReady m) (cur : List Int) (done : List (List Int))
    (x : Int) (hx0 : x ≠ 0) (hxv : x.natAbs ≤ nv) :
    runBody nv ⟨m, cur, done⟩ (intChars x ++ [' ']) = some ⟨.sep, x :: cur, done⟩ := by
  -- the digits of a positive value `n`, read from `.num b (digitVal d)`, then the space
  have digitsThenSpace : ∀ (b : Bool) (n : Nat) (d : Char) (ds : List Char), natDigits n = d :: ds →
      n ≤ nv → runBody nv ⟨.num b (digitVal d), cur, done⟩ (ds ++ [' ']) =
        some ⟨.sep, (if b then -(n : Int) else n) :: cur, done⟩ := by
    intro b n d ds he hn
    have hall := natDigits_isDigit n
    rw [he] at hall
    have hval := natDigits_val n
    rw [he, List.foldl_cons] at hval
    have h0 : dstep 0 d = digitVal d := by simp [dstep]
    rw [h0] at hval
    rw [runBody_append, runBody_digits nv b cur done ds _ (fun c hc => hall c (List.mem_cons_of_mem d hc)),
      Option.bind_some, hval]
    have hs : bodyStep nv ⟨.num b n, cur, done⟩ ' ' = some ⟨.sep, (if b then -(n : Int) else n) :: cur, done⟩ := by
      simp only [bodyStep, space_not_digit, Bool.false_eq_true, if_false, true_and, hn, if_true]
    rw [runBody_cons_of hs]
    rfl
  cases x with
  | ofNat n =>
    have hn : 0 < n := by
      rcases Nat.eq_zero_or_pos n with rfl | h
      · exact absurd rfl hx0
      · exact h
    have hnv : n ≤ nv := hxv
    obtain ⟨d, ds, he, hd⟩ := natDigits_pos n hn
    have hd1 : d ≠ ' ' := ne_of_isDigit (isPosDigit_isDigit hd) space_not_digit
    have hd2 : d ≠ '-' := ne_of_isDigit (isPosDigit_isDigit hd) minus_not_digit
    have hs : bodyStep nv ⟨m, cur, done⟩ d = some ⟨.num false (digitVal d), cur, done⟩ := by
      rw [bodyStep_ready hm hd1 (isPosDigit_ne_zero hd)]
      simp only [litStart, hd2, if_false, hd, if_true]
    simp only [intChars]
    rw [he, List.cons_append, runBody_cons_of hs, digitsThenSpace false n d ds he hnv]
    rfl
  | negSucc n =>
    have hnv : n + 1 ≤ nv := hxv
    obtain ⟨d, ds, he, hd⟩ := natDigits_pos (n + 1) (Nat.succ_pos n)
    have hs1 : bodyStep nv ⟨m, cur, done⟩ '-' = some ⟨.neg, cur, done⟩ := by
      rw [bodyStep_ready hm (by decide) (by decide)]
      simp only [litStart, if_true]
    have hs2 : bodyStep nv ⟨.neg, cur, done⟩ d = some ⟨.num true (digitVal d), cur, done⟩ := by
      simp only [bodyStep, hd, if_true]
    simp only [intChars]
    rw [List.cons_append, runBody_cons_of hs1, he, List.cons_append, runBody_cons_of hs2,
      digitsThenSpace true (n + 1) d ds he hnv]
    rfl

/-- Literals, each followed by a space, read from `sep`. -/
theorem runBody_lits_sep {nv : Nat} (done : List (List Int)) :
    ∀ (ls : List Int) (cur : List Int), (∀ x ∈ ls, x ≠ 0 ∧ x.natAbs ≤ nv) →
      runBody nv ⟨.sep, cur, done⟩ (ls.flatMap fun x => intChars x ++ [' ']) =
        some ⟨.sep, ls.reverse ++ cur, done⟩
  | [], cur, _ => rfl
  | x :: xs, cur, h => by
    have hx := h x List.mem_cons_self
    rw [List.flatMap_cons, runBody_append, runBody_lit (m := .sep) trivial cur done x hx.1 hx.2, Option.bind_some,
      runBody_lits_sep done xs (x :: cur) (fun y hy => h y (List.mem_cons_of_mem x hy))]
    simp only [List.reverse_cons, List.append_assoc, List.singleton_append]

/-- One clause line, read from the start of a line. -/
theorem runBody_clause {nv : Nat} (done : List (List Int)) (cl : List Int)
    (h : ∀ x ∈ cl, x ≠ 0 ∧ x.natAbs ≤ nv) :
    runBody nv ⟨.start, [], done⟩ (clauseChars cl) = some ⟨.start, [], cl :: done⟩ := by
  cases cl with
  | nil => rfl
  | cons l ls =>
    have hl := h l List.mem_cons_self
    simp only [clauseChars]
    rw [List.flatMap_cons, List.append_assoc, runBody_append, runBody_lit (m := .start) trivial [] done l hl.1 hl.2,
      Option.bind_some, runBody_append,
      runBody_lits_sep done ls [l] (fun y hy => h y (List.mem_cons_of_mem l hy)), Option.bind_some]
    have hz : bodyStep nv ⟨.sep, ls.reverse ++ [l], done⟩ '0' = some ⟨.zero, ls.reverse ++ [l], done⟩ := rfl
    have hn : bodyStep nv ⟨.zero, ls.reverse ++ [l], done⟩ '\n' =
        some ⟨.start, [], (ls.reverse ++ [l]).reverse :: done⟩ := rfl
    rw [runBody_cons_of hz, runBody_cons_of hn]
    simp [runBody]

/-- All clause lines. -/
theorem runBody_clauses {nv : Nat} : ∀ (F : List (List Int)) (done : List (List Int)),
    (∀ cl ∈ F, ∀ x ∈ cl, x ≠ 0 ∧ x.natAbs ≤ nv) →
      runBody nv ⟨.start, [], done⟩ (F.flatMap clauseChars) = some ⟨.start, [], F.reverse ++ done⟩
  | [], done, _ => rfl
  | cl :: F, done, h => by
    rw [List.flatMap_cons, runBody_append, runBody_clause done cl (h cl List.mem_cons_self), Option.bind_some,
      runBody_clauses F (cl :: done) (fun c hc => h c (List.mem_cons_of_mem cl hc))]
    simp

/-! ## The round trip -/

/-- **Round trip.** The text `render nv F` parses back to `(nv, F)`, for every clause list `F` whose literals are
nonzero with `natAbs ≤ nv` (the shape of `encB_wf`). -/
theorem parseDimacs_render (nv : Nat) (F : List (List Int))
    (hF : ∀ cl ∈ F, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nv) :
    parseDimacs (render nv F) = some (nv, F) := by
  have h1 : stripPrefix ['p', ' ', 'c', 'n', 'f', ' '] (render nv F).data =
      some (natDigits nv ++ ' ' :: (natDigits F.length ++ '\n' :: F.flatMap clauseChars)) := by
    rw [render_data, headerChars_append, stripPrefix_append]
  have h2 := parseNatTerm_natDigits ' ' space_not_digit nv (natDigits F.length ++ '\n' :: F.flatMap clauseChars)
  have h3 := parseNatTerm_natDigits '\n' newline_not_digit F.length (F.flatMap clauseChars)
  have h4 := runBody_clauses F [] hF
  simp only [parseDimacs, parseDimacsChars, h1, h2, h3, h4, List.append_nil, List.length_reverse,
    List.reverse_reverse, and_self, if_true]

/-- The round trip for what the exe prints for a cube (or, with `cube = []`, the base). -/
theorem parseDimacs_renderCube (nv : Nat) (F : List (List Int)) (cube : List Int)
    (hF : ∀ cl ∈ F, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nv) (hc : ∀ z ∈ cube, z ≠ 0 ∧ z.natAbs ≤ nv) :
    parseDimacs (renderCube nv F (bodyR F) cube) = some (nv, cubeCnf F cube) := by
  rw [renderCube_eq]
  apply parseDimacs_render
  intro cl hcl l hl
  simp only [cubeCnf, List.mem_append, List.mem_map] at hcl
  rcases hcl with hcl | ⟨z, hz, rfl⟩
  · exact hF cl hcl l hl
  · rw [List.mem_singleton.1 hl]
    exact hc z hz

theorem parseDimacs_renderCube_nil (nv : Nat) (F : List (List Int))
    (hF : ∀ cl ∈ F, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nv) :
    parseDimacs (renderCube nv F (bodyR F) []) = some (nv, F) := by
  rw [parseDimacs_renderCube nv F [] hF (fun _ h => absurd h List.not_mem_nil), cubeCnf_nil]

/-- The exe's text for any instance parses to `(numVars m K t, cubeCnf (encB m K t) cube)` (by `encB_wf`), for a
cube of nonzero literals with `natAbs ≤ numVars m K t`. -/
theorem parseDimacs_cnfText (m K t : Nat) (cube : List Int)
    (hc : ∀ z ∈ cube, z ≠ 0 ∧ z.natAbs ≤ numVars m K t) :
    parseDimacs (cnfText (encode m K t) cube) = some (numVars m K t, cubeCnf (encB m K t) cube) := by
  rw [cnfText_encode]
  exact parseDimacs_renderCube _ _ cube encB_wf hc

/-! ## The bytes: the text is ASCII, so its UTF-8 encoding is its character codes -/

theorem natDigits_digitChar (n : Nat) : ∀ c ∈ natDigits n, ∃ d, d < 10 ∧ c = Nat.digitChar d := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    rw [natDigits]
    by_cases h : n < 10
    · rw [if_pos h]
      intro c hc
      exact ⟨n, h, List.mem_singleton.1 hc⟩
    · rw [if_neg h]
      intro c hc
      rcases List.mem_append.1 hc with hc | hc
      · exact ih (n / 10) (by omega) c hc
      · exact ⟨n % 10, Nat.mod_lt n (by omega), List.mem_singleton.1 hc⟩

theorem digitChar_ascii : ∀ d : Nat, d < 10 → (Nat.digitChar d).toNat < 128
  | 0, _ => by decide
  | 1, _ => by decide
  | 2, _ => by decide
  | 3, _ => by decide
  | 4, _ => by decide
  | 5, _ => by decide
  | 6, _ => by decide
  | 7, _ => by decide
  | 8, _ => by decide
  | 9, _ => by decide
  | _ + 10, h => absurd h (by omega)

theorem natDigits_ascii (n : Nat) : ∀ c ∈ natDigits n, c.toNat < 128 := by
  intro c hc
  obtain ⟨d, hd, rfl⟩ := natDigits_digitChar n c hc
  exact digitChar_ascii d hd

theorem ascii_append {A B : List Char} (ha : ∀ c ∈ A, c.toNat < 128) (hb : ∀ c ∈ B, c.toNat < 128) :
    ∀ c ∈ A ++ B, c.toNat < 128 :=
  fun c hc => (List.mem_append.1 hc).elim (ha c) (hb c)

theorem ascii_cons {a : Char} {B : List Char} (ha : a.toNat < 128) (hb : ∀ c ∈ B, c.toNat < 128) :
    ∀ c ∈ a :: B, c.toNat < 128 :=
  fun c hc => (List.mem_cons.1 hc).elim (fun e => e ▸ ha) (hb c)

theorem intChars_ascii (x : Int) : ∀ c ∈ intChars x, c.toNat < 128 := by
  cases x with
  | ofNat n => exact natDigits_ascii n
  | negSucc n => exact ascii_cons (by decide) (natDigits_ascii (n + 1))

theorem clauseChars_ascii (cl : List Int) : ∀ c ∈ clauseChars cl, c.toNat < 128 := by
  cases cl with
  | nil => decide
  | cons l ls =>
    refine ascii_append (fun c hc => ?_) (by decide)
    obtain ⟨x, _, hx⟩ := List.mem_flatMap.1 hc
    exact ascii_append (intChars_ascii x) (by decide) c hx

theorem headerChars_ascii (nv nc : Nat) : ∀ c ∈ headerChars nv nc, c.toNat < 128 :=
  ascii_append (ascii_append (by decide) (natDigits_ascii nv))
    (ascii_cons (by decide) (ascii_append (natDigits_ascii nc) (by decide)))

/-- **Every character of the text is ASCII.** -/
theorem render_ascii (nv : Nat) (F : List (List Int)) : ∀ c ∈ (render nv F).data, c.toNat < 128 := by
  rw [render_data]
  refine ascii_append (headerChars_ascii _ _) (fun c hc => ?_)
  obtain ⟨cl, _, h⟩ := List.mem_flatMap.1 hc
  exact clauseChars_ascii cl c h

theorem utf8EncodeChar_ascii (c : Char) (h : c.toNat < 128) : String.utf8EncodeChar c = [c.val.toUInt8] := by
  rw [String.utf8EncodeChar_eq_utf8EncodeCharFast, String.utf8EncodeCharFast]
  have hv : c.val ≤ 0x7f := by
    rw [UInt32.le_iff_toNat_le]
    exact Nat.le_of_lt_succ h
  simp only [hv, if_true]

theorem flatMap_utf8EncodeChar_ascii : ∀ (l : List Char), (∀ c ∈ l, c.toNat < 128) →
    l.flatMap String.utf8EncodeChar = l.map fun c => c.val.toUInt8
  | [], _ => rfl
  | c :: cs, h => by
    rw [List.flatMap_cons, List.map_cons, utf8EncodeChar_ascii c (h c List.mem_cons_self),
      flatMap_utf8EncodeChar_ascii cs (fun d hd => h d (List.mem_cons_of_mem c hd)), List.singleton_append]

/-- **The bytes.** The UTF-8 encoding of the text (core's `String.toUTF8`, what `IO.FS.Stream.putStr` writes) is
one byte per character, the character's code: the file is the character list that `parseDimacs` reads. -/
theorem renderCube_bytes (nv : Nat) (F : List (List Int)) (bodyF : String) (cube : List Int) (hb : bodyF = bodyR F) :
    (renderCube nv F bodyF cube).toUTF8.data.toList = (renderCube nv F bodyF cube).data.map fun c => c.val.toUInt8 := by
  subst hb
  rw [renderCube_eq]
  exact flatMap_utf8EncodeChar_ascii _ (render_ascii _ _)

theorem cnfText_bytes (e : Enc) (cube : List Int) :
    (cnfText e cube).toUTF8.data.toList = (cnfText e cube).data.map fun c => c.val.toUInt8 :=
  renderCube_bytes e.nv e.clauses (bodyR e.clauses) cube rfl

/-! ## The cube literals are variables of `encB 6 8 11`, symbolically -/

/-- The Y codes, allocated first (the first part of `prefixCodes`, Coded.lean). -/
def yCodesOf (t : Nat) : List Nat := (rng 1 t).flatMap fun i => (rng (i + 1) t).map (yCode t i)

theorem yCodesOf_sub_allCodes (m K t : Nat) : ∀ x ∈ yCodesOf t, x ∈ allCodes m K t := by
  intro x hx
  have hp : x ∈ prefixCodes m t := List.mem_append_left _ (List.mem_append_left _ hx)
  have h0 := mem_dedup_foldl (prefixCodes m t) _ (seenInv_init (codeBound m K t))
  rw [allCodes_eq, allCodesOf, List.mem_reverse]
  exact (mem_dedup_clauses (genCoded m K t) _ h0.1).2.2 x (h0.2.1 x hp)

theorem length_le_of_nodup_sub : ∀ {D l : List Nat}, D.Nodup → (∀ x ∈ D, x ∈ l) → D.length ≤ l.length
  | [], _, _, _ => Nat.zero_le _
  | x :: D, l, hD, h => by
    rw [List.nodup_cons] at hD
    have hx : x ∈ l := h x List.mem_cons_self
    have hsub : ∀ y ∈ D, y ∈ l.erase x := fun y hy =>
      (List.mem_erase_of_ne (fun (e : y = x) => hD.1 (by rw [← e]; exact hy))).2 (h y (List.mem_cons_of_mem x hy))
    have ih := length_le_of_nodup_sub hD.2 hsub
    rw [List.length_erase_of_mem hx] at ih
    have hl : 0 < l.length := List.length_pos_of_mem hx
    rw [List.length_cons]
    omega

/-- A symbolic lower bound on the header count: every Y code gets a number. -/
theorem yCodesOf_length_le_numVars (m K t : Nat) (h : (yCodesOf t).Nodup) :
    (yCodesOf t).length ≤ numVars m K t := by
  rw [numVars_eq]
  exact length_le_of_nodup_sub h (yCodesOf_sub_allCodes m K t)

theorem yCodesOf_nodup_11 : (yCodesOf 11).Nodup := by decide
theorem length_yCodesOf_11 : (yCodesOf 11).length = 45 := by decide

theorem mem_signPatterns : ∀ {vs : List Int} {c : List Int}, c ∈ signPatterns vs → ∀ z ∈ c, z ∈ vs ∨ -z ∈ vs
  | [], c, hc, z, hz => by
    rw [signPatterns, List.mem_singleton] at hc
    rw [hc] at hz
    exact absurd hz List.not_mem_nil
  | v :: vs, c, hc, z, hz => by
    rw [signPatterns, List.mem_append, List.mem_map, List.mem_map] at hc
    rcases hc with ⟨c', hc', rfl⟩ | ⟨c', hc', rfl⟩
    · rcases List.mem_cons.1 hz with rfl | hz
      · exact Or.inl List.mem_cons_self
      · rcases mem_signPatterns hc' z hz with h | h
        · exact Or.inl (List.mem_cons_of_mem _ h)
        · exact Or.inr (List.mem_cons_of_mem _ h)
    · rcases List.mem_cons.1 hz with rfl | hz
      · exact Or.inr (by rw [Int.neg_neg]; exact List.mem_cons_self)
      · rcases mem_signPatterns hc' z hz with h | h
        · exact Or.inl (List.mem_cons_of_mem _ h)
        · exact Or.inr (List.mem_cons_of_mem _ h)

theorem cubeVars64_bound : ∀ v ∈ cubeVars64, v ≠ 0 ∧ v.natAbs ≤ 45 := by decide

/-- Every literal of every cube of `cubes64` is nonzero with `natAbs ≤ 45`. -/
theorem cubes64_lits {c : List Int} (hc : c ∈ cubes64) : ∀ z ∈ c, z ≠ 0 ∧ z.natAbs ≤ 45 := by
  intro z hz
  rcases mem_signPatterns hc z hz with h | h
  · exact cubeVars64_bound z h
  · have := cubeVars64_bound (-z) h
    rw [Int.natAbs_neg] at this
    exact ⟨fun e => this.1 (by rw [e]; rfl), this.2⟩

/-- `45 ≤ numVars m K 11` for every `m K`: the 45 Y codes of `t = 11` all get numbers. -/
theorem numVars_ge_45 (m K : Nat) : 45 ≤ numVars m K 11 :=
  length_yCodesOf_11 ▸ yCodesOf_length_le_numVars m K 11 yCodesOf_nodup_11

/-- The cube literals, against the header count of the instance (generic in `m K`; instantiated at 6 8 below). -/
theorem cubes64_lits_le (m K : Nat) {c : List Int} (hc : c ∈ cubes64) :
    ∀ z ∈ c, z ≠ 0 ∧ z.natAbs ≤ numVars m K 11 :=
  fun z hz => ⟨(cubes64_lits hc z hz).1, Nat.le_trans (cubes64_lits hc z hz).2 (numVars_ge_45 m K)⟩

/-! ## The instance (6,8,11): the text printed by `twin-cube64` / `twin-base` is the theorems' clause list

These declarations mention `encB 6 8 11`; their proofs are applications of the generic theorems above, so
`scripts/audit.sh` check 4 applies (no `decide`/`rfl`/`simp`/`omega`) and nothing evaluates the instance. -/

/-- **For every cube of `cubes64`, the text `twin-cube64` prints parses to the clause list of the theorem.** -/
theorem parseDimacs_cube64 {c : List Int} (hc : c ∈ cubes64) :
    parseDimacs (renderCube (numVars 6 8 11) (encB 6 8 11) (bodyR (encB 6 8 11)) c) =
      some (numVars 6 8 11, cubeCnf (encB 6 8 11) c) :=
  parseDimacs_renderCube (numVars 6 8 11) (encB 6 8 11) c encB_wf (cubes64_lits_le 6 8 hc)

/-- The same for the index `I` that `twin-cube64 6 8 11 I` takes, in the exe's own form `cnfText (encode 6 8 11)`. -/
theorem parseDimacs_cube64_get (i : Nat) (h : i < cubes64.length) :
    parseDimacs (cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)) =
      some (numVars 6 8 11, cubeCnf (encB 6 8 11) (cubes64.get ⟨i, h⟩)) :=
  parseDimacs_cnfText 6 8 11 _ (cubes64_lits_le 6 8 (List.get_mem cubes64 ⟨i, h⟩))

/-- **The text `twin-base 6 8 11` prints parses to `(numVars 6 8 11, encB 6 8 11)`.** -/
theorem parseDimacs_base6811 :
    parseDimacs (renderCube (numVars 6 8 11) (encB 6 8 11) (bodyR (encB 6 8 11)) []) =
      some (numVars 6 8 11, encB 6 8 11) :=
  parseDimacs_renderCube_nil (numVars 6 8 11) (encB 6 8 11) encB_wf

/-- **The verdicts about the texts give `CubesUnsat64`.** If, for each cube of `cubes64`, the text `twin-cube64`
prints parses (by `parseDimacs`) to an unsatisfiable clause list, then `CubesUnsat64`. What remains external is that
cake_lpr's `s VERIFIED UNSAT` on a file with these bytes means exactly this (trust item E3). -/
theorem cubesUnsat64_of_texts
    (h : ∀ c ∈ cubes64, ∀ nv G,
      parseDimacs (renderCube (numVars 6 8 11) (encB 6 8 11) (bodyR (encB 6 8 11)) c) = some (nv, G) →
        ¬DimacsSatisfiable G) :
    CubesUnsat64 :=
  fun c hc => h c hc _ _ (parseDimacs_cube64 hc)

theorem encB_unsat_of_texts
    (h : ∀ c ∈ cubes64, ∀ nv G,
      parseDimacs (renderCube (numVars 6 8 11) (encB 6 8 11) (bodyR (encB 6 8 11)) c) = some (nv, G) →
        ¬DimacsSatisfiable G) :
    ¬DimacsSatisfiable (encB 6 8 11) :=
  encB_unsat_of_cubesUnsat64 (cubesUnsat64_of_texts h)

/-- **The verdicts by index, in the exe's own form.** The hypothesis is stated on the exact expression that
`twin-cube64 6 8 11 i` writes to stdout, `cnfText (encode 6 8 11) (cubes64.get ⟨i, hi⟩)` (Emit.lean), for every
index `i` that `scripts/hash_binding.sh` binds by hash (0 ≤ i < 64): if each of these texts parses (by
`parseDimacs`) to an unsatisfiable clause list, then `CubesUnsat64`. The bridge from the index to the membership
form is `List.mem_iff_get` with `parseDimacs_cube64_get`. -/
theorem cubesUnsat64_of_texts_get
    (h : ∀ (i : Nat) (hi : i < cubes64.length) (nv : Nat) (G : List (List Int)),
      parseDimacs (cnfText (encode 6 8 11) (cubes64.get ⟨i, hi⟩)) = some (nv, G) → ¬DimacsSatisfiable G) :
    CubesUnsat64 := by
  intro c hc
  obtain ⟨⟨i, hi⟩, hget⟩ := List.mem_iff_get.1 hc
  subst hget
  exact h i hi _ _ (parseDimacs_cube64_get i hi)

theorem encB_unsat_of_texts_get
    (h : ∀ (i : Nat) (hi : i < cubes64.length) (nv : Nat) (G : List (List Int)),
      parseDimacs (cnfText (encode 6 8 11) (cubes64.get ⟨i, hi⟩)) = some (nv, G) → ¬DimacsSatisfiable G) :
    ¬DimacsSatisfiable (encB 6 8 11) :=
  encB_unsat_of_cubesUnsat64 (cubesUnsat64_of_texts_get h)


/-! ## Axioms -/

/-- info: 'EncB.parseDimacs_render' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_render

/-- info: 'EncB.renderCube_eq' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms renderCube_eq

/-- info: 'EncB.parseDimacs_renderCube' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_renderCube

/-- info: 'EncB.parseDimacs_cnfText' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_cnfText

/-- info: 'EncB.parseDimacs_cube64' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_cube64

/-- info: 'EncB.parseDimacs_cube64_get' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_cube64_get

/-- info: 'EncB.parseDimacs_base6811' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_base6811

/-- info: 'EncB.cubesUnsat64_of_texts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms cubesUnsat64_of_texts

/-- info: 'EncB.encB_unsat_of_texts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_unsat_of_texts

/-- info: 'EncB.cubesUnsat64_of_texts_get' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms cubesUnsat64_of_texts_get

/-- info: 'EncB.encB_unsat_of_texts_get' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms encB_unsat_of_texts_get

/-- info: 'EncB.pushNat_eq_append_toString' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms pushNat_eq_append_toString

/-- info: 'EncB.cnfText_bytes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms cnfText_bytes

end EncB
