import N66Geo.Final4

/-!
# N66Geo.Pair: soundness of the empty and domain clauses (4.1-4.2) for every `Model`

For owners `X < Y` of states `u, v`, the pair label `d = labels X Y` lies in the **refined** domain
`D'(u → v)`: it is a cell of `v`'s state and not of `u`'s (state separation, `label_cells`), and
`d.2 ≤ cupH(u) + 1`, `d.1 ≤ capH(u) + 1` (**Lemma R**, N66 README §2.5: the predecessor `t` on a rank-attaining
path ending with `(X, Y)` gives an incoming label of `X` one below). Hence an empty refined domain forbids `X < Y`
(empty clause), and a pair `(a, b)` outside `D'(u → v)` is not the label (domain clause).
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks ErdosSzekeres.Omission.StateInterface
  N66Enc

/-! ## Lemma R -/

theorem endingPath_pred {cup : ℕ → ℕ → ℕ → Bool} {color : Bool} {u v L : ℕ}
    (h : EndingPath cup color u v L) (hL : 3 ≤ L) :
    ∃ t, t < u ∧ EndingPath cup color t u (L - 1) ∧ cup t u v = color := by
  cases h with
  | pair _ => omega
  | step path _ same => exact ⟨_, (length_bounds path).2.2, by simpa using path, same⟩

theorem label_ge_one (M : Model) {u v : ℕ} (huv : u < v) (hv : v < M.n) :
    1 ≤ (labels M.cup u v).1 ∧ 1 ≤ (labels M.cup u v).2 :=
  ⟨(label_bounds6 M huv hv).1, (label_bounds6 M huv hv).2.2.1⟩

/-- Lemma R, cup half. -/
theorem lemmaR_cup (M : Model) {X Y : ℕ} (hXY : X < Y) (hY : Y < M.n) :
    (labels M.cup X Y).2 ≤ column M.cup X 0 + 1 := by
  have hL := length_bounds (rank_attained M.cup true X Y hXY)
  by_cases h3 : 3 ≤ rank M.cup true X Y
  · obtain ⟨t, htX, path, -⟩ := endingPath_pred (rank_attained M.cup true X Y hXY) h3
    have hr := rank_ge path
    have hone := label_ge_one M htX (lt_trans hXY hY)
    have hcol : (if 0 + 1 ≤ (labels M.cup t X).1 then (labels M.cup t X).2 else 0) ≤ column M.cup X 0 :=
      Finset.le_sup (f := fun u => if 0 + 1 ≤ (labels M.cup u X).1 then (labels M.cup u X).2 else 0)
        (Finset.mem_range.2 htX)
    rw [if_pos (by omega)] at hcol
    simp only [labels] at hcol ⊢
    omega
  · simp only [labels]
    omega

/-- Lemma R, cap half: column `d.1 - 2` of `X`'s state is nonempty. -/
theorem lemmaR_cap (M : Model) {X Y : ℕ} (hXY : X < Y) (hY : Y < M.n) (h2 : 2 ≤ (labels M.cup X Y).1) :
    1 ≤ column M.cup X ((labels M.cup X Y).1 - 2) := by
  have h3 : 3 ≤ rank M.cup false X Y := by simp only [labels] at h2; omega
  obtain ⟨t, htX, path, -⟩ := endingPath_pred (rank_attained M.cup false X Y hXY) h3
  have hr := rank_ge path
  have hone := label_ge_one M htX (lt_trans hXY hY)
  have hcol : (if (labels M.cup X Y).1 - 2 + 1 ≤ (labels M.cup t X).1 then (labels M.cup t X).2 else 0) ≤
      column M.cup X ((labels M.cup X Y).1 - 2) :=
    Finset.le_sup (f := fun u => if (labels M.cup X Y).1 - 2 + 1 ≤ (labels M.cup u X).1 then
      (labels M.cup u X).2 else 0) (Finset.mem_range.2 htX)
  rw [if_pos (by simp only [labels] at hone ⊢; omega)] at hcol
  omega

theorem capH_profOf_ge (M : Model) {X Y : ℕ} (hXY : X < Y) (hY : Y < M.n) :
    (labels M.cup X Y).1 ≤ capH (profOf M.cup X) + 1 := by
  have bd := label_bounds6 M hXY hY
  have anti := column_antitone M.cup X
  unfold capH profOf
  simp only
  by_cases h2 : 2 ≤ (labels M.cup X Y).1
  · have hc := lemmaR_cap M hXY hY h2
    have a01 := anti (show 0 ≤ 1 by omega)
    have a12 := anti (show 1 ≤ 2 by omega)
    rcases (show (labels M.cup X Y).1 = 2 ∨ (labels M.cup X Y).1 = 3 ∨ (labels M.cup X Y).1 = 4 by omega)
      with e | e | e <;> rw [e] at hc <;> simp at hc <;> split_ifs <;> omega
  · omega

/-! ## The refined domain contains the label -/

theorem can_eq (u v : Fin 70) : can u v = canF u v := by
  have hu := u.isLt; have hv := v.isLt
  unfold can canArr
  rw [Array.getD_eq_getD_getElem?, Array.getElem?_ofFn, dif_pos (by omega), Option.getD_some]
  congr 1 <;> apply Fin.ext <;> simp only [] <;> omega

theorem label_domRef (M : Model) {X Y : ℕ} (hXY : X < Y) (hY : Y < M.n) :
    domRef (prof ⟨idxOf M.cup X, idxOf_lt M (lt_trans hXY hY)⟩) (prof ⟨idxOf M.cup Y, idxOf_lt M hY⟩)
      (labels M.cup X Y) = true := by
  have hd := (label_dom M hXY hY).2
  unfold domRef
  rw [hd, prof_idxOf M (lt_trans hXY hY)]
  simp only [Bool.true_and, Bool.and_eq_true, decide_eq_true_eq]
  refine ⟨capH_profOf_ge M hXY hY, ?_⟩
  have := lemmaR_cup M hXY hY
  simpa [cupH, profOf] using this

/-! ## The clauses -/

theorem geAtom_comm (cup : Bool) {a b : Fin 70} (hab : a ≠ b) (k : ℕ) : geAtom cup a b k = geAtom cup b a k := by
  unfold geAtom
  by_cases h : a < b
  · have h' : ¬ b < a := fun h2 => absurd (lt_trans h h2) (lt_irrefl a)
    simp [h, h']
  · have h' : b < a := lt_of_le_of_ne (not_lt.1 h) (Ne.symm hab)
    simp [h, h']

/-- **4.1-4.2** for one directed pair. -/
theorem holds_dirPair (M : Model) (i j u v : Fin 70) (hij : i ≠ j)
    (huv : (u = i ∧ v = j) ∨ (u = j ∧ v = i)) : M.Holds (dirPairClauses i j u v) := by
  classical
  have hne : u ≠ v := by rcases huv with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> [exact hij; exact Ne.symm hij]
  have hgeq : ∀ cup k, geAtom cup i j k = geAtom cup u v k := by
    intro cup k
    rcases huv with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · rfl
    · exact geAtom_comm cup hij k
  -- owners
  have hown : ∀ (pre : List SLit), (befLit u v).neg ∈ pre →
      (∀ X Y, X < Y → Y < M.n → idxOf M.cup X = u.val → idxOf M.cup Y = v.val →
        ∃ l ∈ pre ++ [guard u, guard v], Agree M l) →
      ∃ l ∈ pre ++ [guard u, guard v], Agree M l := by
    intro pre h1 h
    by_cases hu : M.occ u
    · by_cases hv : M.occ v
      · obtain ⟨X, hX, hXu⟩ := hu
        obtain ⟨Y, hY, hYv⟩ := hv
        by_cases hXY : X < Y
        · exact h X Y hXY hY hXu hYv
        · exact ⟨_, List.mem_append_left _ h1,
            (agree_neg M _).2 (fun hh => hXY ((agree_befLit M hne hX hY hXu hYv).1 hh))⟩
      · exact ⟨guard v, by simp, (agree_guard M v).2 hv⟩
    · exact ⟨guard u, by simp, (agree_guard M u).2 hu⟩
  intro cl hcl
  unfold dirPairClauses at hcl
  split at hcl
  · -- empty refined domain
    rename_i hcan
    simp only [List.mem_singleton] at hcl
    subst hcl
    apply hown [(befLit u v).neg] (by simp)
    intro X Y hXY hY hXu hYv
    exfalso
    have hd := label_domRef M hXY hY
    have eu : u = ⟨idxOf M.cup X, idxOf_lt M (lt_trans hXY hY)⟩ := Fin.ext hXu.symm
    have ev : v = ⟨idxOf M.cup Y, idxOf_lt M hY⟩ := Fin.ext hYv.symm
    have hc : canF u v = true := by
      rw [eu, ev]
      exact List.any_eq_true.2 ⟨_, (label_dom M hXY hY).1, hd⟩
    rw [← can_eq] at hc
    simp [hc] at hcan
  · -- a cell outside the refined domain
    obtain ⟨a', ha', hcl⟩ := List.mem_flatMap.1 hcl
    obtain ⟨b', hb', hcl⟩ := List.mem_filterMap.1 hcl
    rw [List.mem_range] at ha' hb'
    split at hcl
    · simp at hcl
    · rename_i hnot
      simp only [Option.some.injEq] at hcl
      subst hcl
      apply hown _ (by simp)
      intro X Y hXY hY hXu hYv
      have hd := label_domRef M hXY hY
      have eu : u = ⟨idxOf M.cup X, idxOf_lt M (lt_trans hXY hY)⟩ := Fin.ext hXu.symm
      have ev : v = ⟨idxOf M.cup Y, idxOf_lt M hY⟩ := Fin.ext hYv.symm
      have hdiff : labels M.cup X Y ≠ (a' + 1, b' + 1) := by
        intro he
        rw [← he] at hnot
        rw [eu, ev] at hnot
        rw [hd] at hnot
        exact hnot rfl
      have bd := label_bounds6 M hXY hY
      have lit_f : ∀ (cup : Bool) (k : ℕ), k < 5 →
          (Agree M (false, geAtom cup i j k) ↔ ¬ k ≤ (if cup then (labels M.cup X Y).2 else (labels M.cup X Y).1)) :=
        fun cup k hk => by rw [hgeq]; exact agree_geAtom_false M cup hXY hY hXu hYv hk
      have lit_t : ∀ (cup : Bool) (k : ℕ), k < 5 →
          (Agree M (true, geAtom cup i j k) ↔ k ≤ (if cup then (labels M.cup X Y).2 else (labels M.cup X Y).1)) :=
        fun cup k hk => by rw [hgeq]; exact agree_geAtom_true M cup hXY hY hXu hYv hk
      have hmem : ∀ l, l ∈ gePart false i j (a' + 1) ∨ l ∈ gePart true i j (b' + 1) →
          l ∈ ([(befLit u v).neg] ++ gePart false i j (a' + 1) ++ gePart true i j (b' + 1)) ++
            [guard u, guard v] := by
        intro l hl
        rcases hl with hl | hl <;> simp [hl]
      by_cases e1 : (labels M.cup X Y).1 = a' + 1
      · have e2 : (labels M.cup X Y).2 ≠ b' + 1 := fun e2 => hdiff (Prod.ext e1 e2)
        rcases Nat.lt_or_gt_of_ne e2 with h | h
        · refine ⟨(false, geAtom true i j (b' + 1)), hmem _ (Or.inr (by simp [gePart]; omega)), ?_⟩
          exact (lit_f true (b' + 1) (by omega)).2 (by simp; omega)
        · refine ⟨(true, geAtom true i j (b' + 1 + 1)), hmem _ (Or.inr (by simp [gePart]; omega)), ?_⟩
          exact (lit_t true (b' + 1 + 1) (by omega)).2 (by simp; omega)
      · rcases Nat.lt_or_gt_of_ne e1 with h | h
        · refine ⟨(false, geAtom false i j (a' + 1)), hmem _ (Or.inl (by simp [gePart]; omega)), ?_⟩
          exact (lit_f false (a' + 1) (by omega)).2 (by simp; omega)
        · refine ⟨(true, geAtom false i j (a' + 1 + 1)), hmem _ (Or.inl (by simp [gePart]; omega)), ?_⟩
          exact (lit_t false (a' + 1 + 1) (by omega)).2 (by simp; omega)

/-- **4.1-4.2.** -/
theorem holds_pair (M : Model) : M.Holds (pairClauses ()) := by
  intro cl hcl
  unfold pairClauses at hcl
  obtain ⟨p, hp, hcl⟩ := List.mem_flatMap.1 hcl
  have hlt : p.1 < p.2 := by
    unfold comb2 at hp
    simp only [List.mem_flatMap, List.mem_filterMap] at hp
    obtain ⟨i, -, j, -, hj⟩ := hp
    split at hj
    · rename_i hij
      simp only [Option.some.injEq] at hj
      subst hj
      exact hij
    · simp at hj
  have hij : p.1 ≠ p.2 := Fin.ne_of_lt hlt
  rcases List.mem_append.1 hcl with h | h
  · exact holds_dirPair M p.1 p.2 p.1 p.2 hij (Or.inl ⟨rfl, rfl⟩) cl h
  · exact holds_dirPair M p.1 p.2 p.2 p.1 hij (Or.inr ⟨rfl, rfl⟩) cl h

end N66Geo

#print axioms N66Geo.holds_pair
