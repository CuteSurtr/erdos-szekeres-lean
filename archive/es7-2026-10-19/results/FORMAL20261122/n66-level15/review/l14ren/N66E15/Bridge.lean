import EncB.Render
import N66E15.Print
import N66E15.DecodeB

/-!
# N66E15.Bridge: from the printed texts to `CubesUnsat105`, and the cube cover (Std-only, theorem side)

* `printClause_mem`: every clause the printer returns for leaf cube `c` is a clause of `fullCnf R0_15 c`, whatever the
  runtime descriptors are (DESIGN.md D3).
* `unsat_of_sub`: a sub-list that is unsatisfiable makes the whole list unsatisfiable.
* `fullUnsat_of_text`: if every DIMACS parse of the text the exe writes for (c, ds) is unsatisfiable (the meaning of
  cake_lpr's verdict on that file, trust item E3), then `fullCnf R0_15 c` is unsatisfiable. Uses ENCBLEAN's proved
  round trip `EncB.parseDimacs_render`.
* `covers_leaves`, `no_base_model`: the 132 leaves cover every assignment of the selectors, so refuting
  `fullCnf R c` for every leaf refutes the cube-free relaxation `baseCnf R`.

Nothing here evaluates the instance (no `decide` on the data, no `#eval`).
-/

namespace N66E15

/-! ## Membership of the printed clauses -/

/-- The cube-free part of the relaxation. -/
noncomputable def baseS (R : List (List (Fin 70))) : List (List SLit) :=
  eagerStream () ++ quadStream ++ fixedUnits ++ R.map rowClause ++ cardClauses ++ sbClauses

noncomputable def baseCnf (R : List (List (Fin 70))) : List (List Int) := (baseS R).map toDimacs

theorem mem_fullS_of_mem_baseS {R : List (List (Fin 70))} {c : Cube} {cl : List SLit} (h : cl ∈ baseS R) :
    cl ∈ fullS R c := by
  simp only [baseS, fullS, List.mem_append] at h ⊢
  rcases h with ((((h | h) | h) | h) | h) | h <;> simp [h]

theorem mem_fullS_of_cube {R : List (List (Fin 70))} {c : Cube} {z : Fin 70 × Bool} (h : z ∈ c) :
    cubeUnit z ∈ fullS R c := by
  simp only [fullS, List.mem_append]
  exact Or.inl (Or.inl (Or.inl (Or.inr (List.mem_map_of_mem h))))

theorem mem_fr70 (a : Fin 70) : a ∈ fr70 := by
  unfold fr70 List.finRange
  exact List.mem_ofFn.2 ⟨a, rfl⟩

theorem mem_perm4 {a b c d : Fin 70} (h : okQuad a b c d = true) : (a, b, c, d) ∈ perm4 := by
  unfold perm4
  simp only [List.mem_flatMap, List.mem_filterMap]
  exact ⟨a, mem_fr70 a, b, mem_fr70 b, c, mem_fr70 c, d, mem_fr70 d, by simp [h]⟩

theorem mem_quadStream {a b c d : Fin 70} {cl : List SLit} (h : okQuad a b c d = true)
    (hc : cl ∈ quadClauses a b c d) : cl ∈ quadStream := by
  unfold quadStream
  exact List.mem_flatMap.2 ⟨(a, b, c, d), mem_perm4 h, hc⟩

/-- **Every clause the printer returns is a clause of `fullCnf R0_15 c`.** -/
theorem printClause_mem {c : Cube} {d : Desc} {cl : List Int} (h : printClause c d = some cl) :
    cl ∈ fullCnf R0_15 c := by
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
    simp only [printClause, R0arr, List.getElem?_toArray] at h
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
    ∀ cl ∈ L, cl ∈ fullCnf R0_15 c := by
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

/-! ## Sub-lists and the text -/

/-- A refuted sub-list refutes the whole list. -/
theorem unsat_of_sub {L F : List (List Int)} (hsub : ∀ cl ∈ L, cl ∈ F) (h : ¬ EncB.DimacsSatisfiable L) :
    ¬ EncB.DimacsSatisfiable F := by
  rintro ⟨ν, hν⟩
  exact h ⟨ν, fun cl hcl => hν cl (hsub cl hcl)⟩

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
E1), then `fullCnf R0_15 c` is unsatisfiable. -/
theorem fullUnsat_of_text {c : Cube} {ds : List Desc} {L : List (List Int)} (hp : printClauses c ds = some L)
    (hb : litsBounded nvHeader L = true)
    (hv : ∀ nv F, EncB.parseDimacs (EncB.render nvHeader L) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) :
    ¬ EncB.DimacsSatisfiable (fullCnf R0_15 c) :=
  unsat_of_sub (printClauses_mem hp) (hv _ _ (EncB.parseDimacs_render nvHeader L (litsBounded_spec hb)))

/-! ## The cover -/

theorem leavesFrom_cover : ∀ (t : SplitTree) (pre : Cube) (x : Fin 70 → Bool), (∀ z ∈ pre, x z.1 = z.2) →
    ∃ c ∈ t.leavesFrom pre, ∀ z ∈ c, x z.1 = z.2
  | .leaf, pre, x, h => ⟨pre, List.mem_singleton_self _, h⟩
  | .node s occ hole, pre, x, h => by
    by_cases hs : x s = true
    · obtain ⟨c, hc, hcx⟩ := leavesFrom_cover occ (pre ++ [(s, true)]) x (by
        intro z hz
        rcases List.mem_append.1 hz with hz | hz
        · exact h z hz
        · simp at hz; subst hz; exact hs)
      exact ⟨c, List.mem_append_left _ hc, hcx⟩
    · obtain ⟨c, hc, hcx⟩ := leavesFrom_cover hole (pre ++ [(s, false)]) x (by
        intro z hz
        rcases List.mem_append.1 hz with hz | hz
        · exact h z hz
        · simp at hz; subst hz; simpa using hs)
      exact ⟨c, List.mem_append_right _ hc, hcx⟩

/-- **The leaves of a split tree cover every assignment of the split states.** -/
theorem covers_leaves (t : SplitTree) (x : Fin 70 → Bool) : ∃ c ∈ t.leaves, ∀ z ∈ c, x z.1 = z.2 :=
  leavesFrom_cover t [] x (fun _ hz => absurd hz List.not_mem_nil)

theorem litSat_cubeUnit (ν : Nat → Bool) (z : Fin 70 × Bool) (h : ν (num (Atom.sel z.1)) = z.2) :
    ∀ l ∈ toDimacs (cubeUnit z), EncB.LitSat ν l := by
  obtain ⟨s, b⟩ := z
  intro l hl
  simp only [toDimacs, cubeUnit, List.map_cons, List.map_nil, List.mem_singleton] at hl
  subst hl
  cases b with
  | true =>
    simp only [litInt, if_true]
    exact (litSat_pos ν _ (num_pos _)).2 h
  | false =>
    simp only [litInt, Bool.false_eq_true, if_false]
    exact (litSat_neg' ν _ (num_pos _)).2 h

/-- **Composition (M3).** If `fullCnf R c` is refuted for every leaf, the cube-free relaxation `baseCnf R` has no
model: any model picks, through the cover, the leaf whose units it satisfies. -/
theorem no_base_model {R : List (List (Fin 70))}
    (h : ∀ c ∈ leaves105, ¬ EncB.DimacsSatisfiable (fullCnf R c)) : ¬ EncB.DimacsSatisfiable (baseCnf R) := by
  rintro ⟨ν, hν⟩
  obtain ⟨c, hc, hcx⟩ := covers_leaves tree15 (fun s => ν (num (Atom.sel s)))
  apply h c hc
  refine ⟨ν, fun cl hcl => ?_⟩
  obtain ⟨s, hs, rfl⟩ := List.mem_map.1 hcl
  simp only [fullS, List.mem_append] at hs
  rcases hs with (((((hs | hs) | hs) | hs) | hs) | hs) | hs
  · exact hν _ (List.mem_map_of_mem (by simp [baseS, hs]))
  · exact hν _ (List.mem_map_of_mem (by simp [baseS, hs]))
  · exact hν _ (List.mem_map_of_mem (by simp [baseS, hs]))
  · obtain ⟨z, hz, rfl⟩ := List.mem_map.1 hs
    obtain ⟨l, hl⟩ : ∃ l, l ∈ toDimacs (cubeUnit z) := ⟨_, List.mem_singleton_self _⟩
    exact ⟨l, hl, litSat_cubeUnit ν z (hcx z hz) l hl⟩
  · exact hν _ (List.mem_map_of_mem (by simp [baseS, hs]))
  · exact hν _ (List.mem_map_of_mem (by simp [baseS, hs]))
  · exact hν _ (List.mem_map_of_mem (by simp [baseS, hs]))

/-- **The 132 verdicts refute the cube-free relaxation over R0_15.** -/
theorem base_unsat_of_cubes (h : CubesUnsat105) : ¬ EncB.DimacsSatisfiable (baseCnf R0_15) := no_base_model h

end N66E15

#print axioms N66E15.printClause_mem
#print axioms N66E15.fullUnsat_of_text
#print axioms N66E15.no_base_model
#print axioms N66E15.base_unsat_of_cubes
