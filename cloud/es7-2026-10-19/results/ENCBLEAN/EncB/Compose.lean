import EncB.Satisfiable
import EncB.Render

/-!
# M9 review fixes: the round trip on bytes, and the composition with M3 (Std-only)

Two additions asked for by the Lean-soundness review of M9 (`logs/m9_review_lean_soundness.log`, findings 3 and 4):

* **Bytes.** `parseDimacs_cube64_get` (Render.lean) is stated on the characters of the string `cnfText …`;
  `cnfText_bytes` only says that its UTF-8 bytes are the characters mapped by `·.val.toUInt8`. Here
  `cnfText_ascii` states that every character is ASCII, `parseDimacsBytes` reads a byte list (each byte as the
  character with that code) with the same automaton as `parseDimacs`, and `parseDimacsBytes_cube64_get` states the
  round trip on the bytes `(cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)).toUTF8`, which is what
  `IO.FS.Stream.putStr` writes.
* **Composition.** `no_model_6811_of_texts`: if each of the 64 texts that `twin-cube64 6 8 11 i` prints parses (by
  `parseDimacs`) to an unsatisfiable clause list, then no `Model 6 8 11` exists. It is `encB_satisfiable_6811`
  (M3) composed with `encB_unsat_of_texts_get` (M9). `no_model_6811_of_bytes` states the same with the hypothesis
  on the bytes, read by `parseDimacsBytes`.

This module is imported by `EncB.lean` only, not by the exe's root `EncB/Emit.lean`, so the exe is unchanged by it.
The declarations that mention the instance are term-mode applications of general theorems; nothing evaluates
`encB 6 8 11` (`scripts/audit.sh` check 4 and its time gate). Not proved here, and still trusted: that cake_lpr reads
a file as `parseDimacsBytes` reads its bytes and that its `s VERIFIED UNSAT` means `¬ DimacsSatisfiable` of that list
(trust item E3), and that the compiled exe writes these bytes (E4).
-/

namespace EncB

/-! ## The round trip on bytes -/

/-- The reference parser on a byte list: each byte is read as the character with that code, then `parseDimacsChars`
(the automaton of `parseDimacs`). -/
def parseDimacsBytes (bs : List UInt8) : Option (Nat × List (List Int)) :=
  parseDimacsChars (bs.map fun b => Char.ofNat b.toNat)

/-- An ASCII character survives the round trip through its byte. -/
theorem ofNat_toUInt8_ascii (c : Char) (h : c.toNat < 128) : Char.ofNat c.val.toUInt8.toNat = c := by
  have h1 : c.val.toUInt8.toNat = c.toNat := by
    rw [UInt32.toNat_toUInt8]
    exact Nat.mod_eq_of_lt (Nat.lt_trans h (by decide))
  rw [h1]
  exact Char.ofNat_toNat c

/-- **Every character of the text the exe writes is ASCII** (for any encoding `e` and cube). -/
theorem cnfText_ascii (e : Enc) (cube : List Int) : ∀ c ∈ (cnfText e cube).data, c.toNat < 128 := by
  rw [cnfText, renderCube_eq]
  exact render_ascii _ _

/-- Reading the UTF-8 bytes of the text with `parseDimacsBytes` is reading the text with `parseDimacs`. -/
theorem parseDimacsBytes_cnfText (e : Enc) (cube : List Int) :
    parseDimacsBytes (cnfText e cube).toUTF8.data.toList = parseDimacs (cnfText e cube) := by
  rw [parseDimacsBytes, cnfText_bytes, List.map_map, parseDimacs]
  congr 1
  conv => rhs; rw [← List.map_id (cnfText e cube).data]
  apply List.map_congr_left
  intro c hc
  exact ofNat_toUInt8_ascii c (cnfText_ascii e cube c hc)

/-- **The round trip on the bytes the exe writes for cube `i`** (`twin-cube64 6 8 11 i`); no evaluation of the
instance. -/
theorem parseDimacsBytes_cube64_get (i : Nat) (h : i < cubes64.length) :
    parseDimacsBytes (cnfText (encode 6 8 11) (cubes64.get ⟨i, h⟩)).toUTF8.data.toList =
      some (numVars 6 8 11, cubeCnf (encB 6 8 11) (cubes64.get ⟨i, h⟩)) :=
  (parseDimacsBytes_cnfText _ _).trans (parseDimacs_cube64_get i h)

/-! ## The composition with M3 -/

/-- **If the 64 texts printed by `twin-cube64 6 8 11 i` (i < 64) parse to unsatisfiable clause lists, no
`Model 6 8 11` exists.** `encB_satisfiable_6811` (M3) with `encB_unsat_of_texts_get` (M9). The hypothesis is what
cake_lpr's 64 verdicts are taken to mean (trust item E3); the step from a geometric configuration to a `Model` is
not proved here (M4–M6). -/
theorem no_model_6811_of_texts
    (h : ∀ (i : Nat) (hi : i < cubes64.length) (nv : Nat) (G : List (List Int)),
      parseDimacs (cnfText (encode 6 8 11) (cubes64.get ⟨i, hi⟩)) = some (nv, G) → ¬DimacsSatisfiable G) :
    Model 6 8 11 → False :=
  fun M => encB_unsat_of_texts_get h (encB_satisfiable_6811 M)

/-- The same, with the hypothesis on the UTF-8 bytes of the texts (what `putStr` writes), read by
`parseDimacsBytes`. -/
theorem no_model_6811_of_bytes
    (h : ∀ (i : Nat) (hi : i < cubes64.length) (nv : Nat) (G : List (List Int)),
      parseDimacsBytes (cnfText (encode 6 8 11) (cubes64.get ⟨i, hi⟩)).toUTF8.data.toList = some (nv, G) →
        ¬DimacsSatisfiable G) :
    Model 6 8 11 → False :=
  no_model_6811_of_texts fun i hi nv G hp => h i hi nv G ((parseDimacsBytes_cnfText _ _).trans hp)

/-! ## Axioms -/

/-- info: 'EncB.cnfText_ascii' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in #print axioms cnfText_ascii

/-- info: 'EncB.parseDimacsBytes_cnfText' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacsBytes_cnfText

/-- info: 'EncB.parseDimacsBytes_cube64_get' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacsBytes_cube64_get

/-- info: 'EncB.no_model_6811_of_texts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms no_model_6811_of_texts

/-- info: 'EncB.no_model_6811_of_bytes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms no_model_6811_of_bytes

end EncB
