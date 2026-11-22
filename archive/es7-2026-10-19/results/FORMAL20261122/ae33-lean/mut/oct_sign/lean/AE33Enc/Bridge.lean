import AE33Enc.Data

/-!
# AE33Enc.Bridge: from the printed texts to the CNFs (Std-only, theorem side)

* `mem_cnf`: every clause of `cnf B` is `clauseOf B d` for some descriptor `d` (DESIGN.md D1), with literals in range.
* `parse_cnfText`: the text the exe prints parses (ENCBLEAN's reference parser) to `(numVars B, cnf B)`, by
  `EncB.parseDimacs_render`; no runtime hypothesis (DESIGN.md D3).
* `texts_iff_cnfs`: the verdict hypothesis on the texts is equivalent to unsatisfiability of the CNFs.

Nothing here evaluates `gen`, `cnf` or the data.
-/

namespace AE33

theorem clauseB_spec {B : Array Pt} {d : Desc} {cl : List Int} (h : clauseB B d = some cl) :
    clauseOf B d = some cl ∧ bounded (numVars B) cl = true := by
  unfold clauseB at h
  split at h
  · rename_i c hc
    split at h
    · rename_i hb
      cases h
      exact ⟨hc, hb⟩
    · cases h
  · cases h

theorem mem_cnf {B : Array Pt} {cl : List Int} (h : cl ∈ cnf B) :
    ∃ d, clauseOf B d = some cl ∧ bounded (numVars B) cl = true := by
  unfold cnf at h
  obtain ⟨d, -, hd⟩ := List.mem_filterMap.1 h
  exact ⟨d, clauseB_spec hd⟩

theorem bounded_spec {nv : Nat} {cl : List Int} (h : bounded nv cl = true) :
    ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nv := by
  intro l hl
  have h1 := List.all_eq_true.1 h l hl
  simp only [Bool.and_eq_true, bne_iff_ne, ne_eq, decide_eq_true_eq] at h1
  exact h1

theorem cnf_wf (B : Array Pt) : ∀ cl ∈ cnf B, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ numVars B := by
  intro cl hcl
  obtain ⟨_, _, hb⟩ := mem_cnf hcl
  exact bounded_spec hb

/-- **The printed text parses back to the CNF.** -/
theorem parse_cnfText (i : Nat) :
    EncB.parseDimacs (cnfText i) = some (numVars (baseOf i), cnf (baseOf i)) := by
  unfold cnfText
  exact EncB.parseDimacs_render _ _ (cnf_wf _)

/-- **The verdict hypothesis on the texts is the unsatisfiability of the 203 CNFs.** -/
theorem texts_iff_cnfs : TextsUnsat203 ↔ CnfsUnsat203 := by
  constructor
  · intro h i hi
    exact h i hi _ _ (parse_cnfText i)
  · intro h i hi nv F hp
    rw [parse_cnfText i] at hp
    simp only [Option.some.injEq, Prod.mk.injEq] at hp
    obtain ⟨-, rfl⟩ := hp
    exact h i hi

end AE33

#print axioms AE33.mem_cnf
#print axioms AE33.parse_cnfText
#print axioms AE33.texts_iff_cnfs
