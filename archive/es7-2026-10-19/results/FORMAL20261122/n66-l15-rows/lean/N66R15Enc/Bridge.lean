import EncB.Render
import N66R15Enc.Print
import N66E15.Bridge

/-!
# N66R15Enc.Bridge: from the printed texts to `CubesUnsat105R` (Std-only, theorem side)

Copy of the membership/text part of n66-level15's `N66E15.Bridge` for the printer `N66R15Enc.Print` (rows from
`R1_15`). The generic parts (`fullCnf`, `baseS`, `mem_fullS_of_mem_baseS`, `mem_fullS_of_cube`, `mem_quadStream`,
`unsat_of_sub`, `no_base_model`) are n66-level15's, used unchanged.

* `printClause_mem`: every clause the printer returns for leaf cube `c` is a clause of `fullCnf R1_15 c`, whatever
  the runtime descriptors are.
* `fullUnsat_of_text`: if every DIMACS parse of the text the exe writes for (c, ds) is unsatisfiable (the meaning of
  cake_lpr's verdict on that file, trust item E3), then `fullCnf R1_15 c` is unsatisfiable (ENCBLEAN's proved round
  trip `EncB.parseDimacs_render`).
* `CubesUnsat105R`: the 105 verdicts, as one proposition, on the row list `R1_15`.

Nothing here evaluates the instance (no `decide` on the data, no `#eval`).
-/

namespace N66R15Enc
open N66E15

/-- **Every clause the printer returns is a clause of `fullCnf R1_15 c`.** -/
theorem printClause_mem {c : Cube} {d : Desc} {cl : List Int} (h : printClause c d = some cl) :
    cl ∈ fullCnf R1_15 c := by
  unfold fullCnf
  cases d with
  | e k =>
    simp only [printClause, eagerArr, List.getElem?_toArray] at h
    obtain ⟨s, hs, rfl⟩ := List.mem_map.1 (List.mem_of_getElem? h)
    exact List.mem_map_of_mem (mem_fullS_of_mem_baseS (by simp [baseS, hs]))
  | q a b c' d' j =>
    simp only [printClause, Option.bind_eq_bind] at h
    obtain ⟨a', -, h⟩ := Option.bind_eq_some_iff.1 h
    obtain ⟨b', -, h⟩ := Option.bind_eq_some_iff.1 h
    obtain ⟨c'', -, h⟩ := Option.bind_eq_some_iff.1 h
    obtain ⟨d'', -, h⟩ := Option.bind_eq_some_iff.1 h
    split at h
    · rename_i hq
      obtain ⟨s, hs, rfl⟩ := Option.map_eq_some_iff.1 h
      exact List.mem_map_of_mem (mem_fullS_of_mem_baseS (by
        simp only [baseS, List.mem_append]
        exact Or.inl (Or.inl (Or.inl (Or.inl (Or.inr (mem_quadStream hq (List.mem_of_getElem? hs))))))))
    · simp at h
  | u k =>
    simp only [printClause] at h
    obtain ⟨s, hs, rfl⟩ := Option.map_eq_some_iff.1 h
    refine List.mem_map_of_mem ?_
    rcases List.mem_append.1 (List.mem_of_getElem? hs) with hs | hs
    · exact mem_fullS_of_mem_baseS (by simp [baseS, hs])
    · obtain ⟨z, hz, rfl⟩ := List.mem_map.1 hs
      exact mem_fullS_of_cube hz
  | r k =>
    simp only [printClause, R1arr, List.getElem?_toArray] at h
    obtain ⟨T, hT, rfl⟩ := Option.map_eq_some_iff.1 h
    exact List.mem_map_of_mem (mem_fullS_of_mem_baseS (by
      simp only [baseS, List.mem_append]
      exact Or.inl (Or.inl (Or.inr (List.mem_map_of_mem (List.mem_of_getElem? hT))))))
  | k k =>
    simp only [printClause, cardArr, List.getElem?_toArray] at h
    obtain ⟨s, hs, rfl⟩ := Option.map_eq_some_iff.1 h
    exact List.mem_map_of_mem (mem_fullS_of_mem_baseS (by
      simp only [baseS, List.mem_append]
      exact Or.inl (Or.inr (List.mem_of_getElem? hs))))
  | s k =>
    simp only [printClause, sbArr, List.getElem?_toArray] at h
    obtain ⟨s, hs, rfl⟩ := Option.map_eq_some_iff.1 h
    exact List.mem_map_of_mem (mem_fullS_of_mem_baseS (by
      simp only [baseS, List.mem_append]
      exact Or.inr (List.mem_of_getElem? hs)))

theorem printClauses_mem {c : Cube} {ds : List Desc} {L : List (List Int)} (h : printClauses c ds = some L) :
    ∀ cl ∈ L, cl ∈ fullCnf R1_15 c := by
  intro cl hcl
  unfold printClauses at h
  induction ds generalizing L with
  | nil => simp at h; subst h; simp at hcl
  | cons d ds ih =>
    simp only [List.mapM_cons, Option.bind_eq_bind, Option.bind_eq_some_iff, Option.pure_def,
      Option.some.injEq] at h
    obtain ⟨x, hx, xs, hxs, rfl⟩ := h
    rcases List.mem_cons.1 hcl with rfl | hcl
    · exact printClause_mem hx
    · exact ih hxs hcl

theorem litsBounded_spec {nv : Nat} {F : List (List Int)} (h : litsBounded nv F = true) :
    ∀ cl ∈ F, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nv := by
  intro cl hcl l hl
  have h1 := List.all_eq_true.1 h cl hcl
  have h2 := List.all_eq_true.1 h1 l hl
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h2
  exact h2

/-- **From the verdict on the printed text to the relaxation.** If the printer returns `L` for leaf cube `c` and
descriptors `ds`, its literals are in range (the exe checks this before writing), and every DIMACS parse of the
text `render nvHeader L` is unsatisfiable (E3 applied to the file cake_lpr certified, whose bytes are this text by
E1), then `fullCnf R1_15 c` is unsatisfiable. -/
theorem fullUnsat_of_text {c : Cube} {ds : List Desc} {L : List (List Int)} (hp : printClauses c ds = some L)
    (hb : litsBounded nvHeader L = true)
    (hv : ∀ nv F, EncB.parseDimacs (EncB.render nvHeader L) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) :
    ¬ EncB.DimacsSatisfiable (fullCnf R1_15 c) :=
  unsat_of_sub (printClauses_mem hp) (hv _ _ (EncB.parseDimacs_render nvHeader L (litsBounded_spec hb)))

/-- **The 105 level-15 cube verdicts, as one proposition**, on the row list `R1_15` (kernel-checked chunk
constants). Discharged outside the kernel by `fullUnsat_of_text` and the hash binding M9 (105/105), under trust
items E1-E6. -/
def CubesUnsat105R : Prop := ∀ c ∈ leaves105, ¬ EncB.DimacsSatisfiable (fullCnf R1_15 c)

end N66R15Enc

#print axioms N66R15Enc.printClause_mem
#print axioms N66R15Enc.fullUnsat_of_text
