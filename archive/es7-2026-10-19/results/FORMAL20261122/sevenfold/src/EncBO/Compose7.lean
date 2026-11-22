import EncBO.SatisfiableO
import EncB.Compose

/-!
# M9 (Lean side) for (7,8,10): the text `twin-base 7 8 10` prints, its round trip, and the composition with M3

`cnfText (encode 7 8 10) []` is, by ENCBLEAN's `cnfText_encode` (definitional) and Emit.lean:187-195, the exact
string the exe `encb_dimacs twin-base 7 8 10` writes to stdout. ENCBLEAN's `parseDimacs_cnfText` (generic in
`m K t`, symbolic well-formedness `encB_wf`) gives its round trip; nothing here evaluates the instance (no tactic in
a declaration that mentions `7 8 10`).

The external facts this file does not prove (ENCBLEAN trust items, re-read for this instance):
* E1: the text's SHA-256 is `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2`, the hash of the CNF
  cake_lpr certified (`C7UPPER/SHA256SUMS.txt`, `cnfb/m7K8t10.cnf`);
* E2: cake_lpr printed `s VERIFIED UNSAT` on that CNF with the proof `75f9bd35…` (`C7UPPER/logs/cake_B.out`,
  `C6C7REVIEW/logs/cake_B7.log`);
* E3: that verdict means `¬ DimacsSatisfiable` of what `parseDimacs` reads from the text.
-/

namespace EncB

/-- **The text `twin-base 7 8 10` prints parses to the theorem's clause list.** -/
theorem parseDimacs_base7810 :
    parseDimacs (cnfText (encode 7 8 10) []) = some (numVars 7 8 10, cubeCnf (encB 7 8 10) []) :=
  parseDimacs_cnfText 7 8 10 [] (fun _ hz => absurd hz List.not_mem_nil)

/-- The verdict about the text gives `¬ DimacsSatisfiable (encB 7 8 10)`. -/
theorem encB7810_unsat_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), parseDimacs (cnfText (encode 7 8 10) []) = some (nv, G) →
      ¬DimacsSatisfiable G) :
    ¬DimacsSatisfiable (encB 7 8 10) :=
  cubeCnf_nil (encB 7 8 10) ▸ h _ _ parseDimacs_base7810

/-- **If the text printed by `twin-base 7 8 10` parses to an unsatisfiable clause list, no `ModelO 7 8 10`
exists.** `encB_satisfiable_7810` (M3, odd) with `encB7810_unsat_of_text` (M9). -/
theorem no_modelO_7810_of_text
    (h : ∀ (nv : Nat) (G : List (List Int)), parseDimacs (cnfText (encode 7 8 10) []) = some (nv, G) →
      ¬DimacsSatisfiable G) :
    ModelO 7 8 10 → False :=
  fun M => encB7810_unsat_of_text h (encB_satisfiable_7810 M)

/-- The same, with the hypothesis on the UTF-8 bytes of the text (what `putStr` writes), read by
`parseDimacsBytes`. -/
theorem no_modelO_7810_of_bytes
    (h : ∀ (nv : Nat) (G : List (List Int)),
      parseDimacsBytes (cnfText (encode 7 8 10) []).toUTF8.data.toList = some (nv, G) → ¬DimacsSatisfiable G) :
    ModelO 7 8 10 → False :=
  no_modelO_7810_of_text fun nv G hp => h nv G ((parseDimacsBytes_cnfText _ _).trans hp)

/-- The hypothesis is not vacuous: it is equivalent to `¬ DimacsSatisfiable (encB 7 8 10)`. -/
theorem text7810_iff :
    (∀ (nv : Nat) (G : List (List Int)), parseDimacs (cnfText (encode 7 8 10) []) = some (nv, G) →
      ¬DimacsSatisfiable G) ↔ ¬DimacsSatisfiable (encB 7 8 10) :=
  ⟨encB7810_unsat_of_text, fun hu _nv _G hp =>
    (Prod.mk.inj (Option.some.inj (parseDimacs_base7810.symm.trans hp))).2 ▸ (cubeCnf_nil (encB 7 8 10)).symm ▸ hu⟩

/-- info: 'EncB.parseDimacs_base7810' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms parseDimacs_base7810

/-- info: 'EncB.no_modelO_7810_of_text' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms no_modelO_7810_of_text

/-- info: 'EncB.no_modelO_7810_of_bytes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms no_modelO_7810_of_bytes

/-- info: 'EncB.text7810_iff' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms text7810_iff

end EncB
