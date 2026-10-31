import ETVEncoding.ClausesB
import ETVEncoding.Shear

/-!
# Soundness of the track-B CNF (`gen_cnf.py N K`)

Every clause of `gen_cnf.py N K` except the symmetry-breaking ones is a clause of
`gen_etv.py N K K K`. The symmetry-breaking clauses hold for signotopes in the corresponding
normal form. This file proves the signotope-level statement for all options, the soundness
of `--flip` (complementing a signotope swaps caps and cups), and the point-set consequence
for the option-free and `--flip` files. `--hull` and `--mirror` are in `ETVEncoding.Hull`.
-/

namespace ETV

open Lit ErdosSzekeres

/-! ### A general transfer lemma -/

/-- Any clause list over allocated variables that holds under `τ` gives a DIMACS model. -/
theorem dimacsSat_of_clauses {N A U : ℕ} {τ : Var → Prop} (cls : List Clause)
    (hvars : ∀ c ∈ cls, ∀ l ∈ c, l.var ∈ allVars N A U) (h : ∀ c ∈ cls, ClauseHolds τ c) :
    DimacsSat (cls.map fun c => c.map (litToInt (numberMap (allVars N A U))))
      (nuOf N A U τ) := by
  classical
  intro c hc
  simp only [List.mem_map] at hc
  obtain ⟨c', hc', rfl⟩ := hc
  obtain ⟨l, hl, hhold⟩ := h c' hc'
  have hv := hvars c' hc' l hl
  refine ⟨litToInt (numberMap (allVars N A U)) l, List.mem_map_of_mem hl, ?_⟩
  have hdec := decode_numberMap hv
  have hnum := numberMap_getD hv
  unfold litToInt
  unfold Lit.Holds at hhold
  cases hpos : l.pos
  · simp only [hpos, Bool.false_eq_true, if_false] at hhold ⊢
    right
    refine ⟨by omega, ?_⟩
    simp only [nuOf, Int.natAbs_neg, Int.natAbs_natCast, hdec, decide_eq_false_iff_not]
    exact hhold
  · simp only [hpos, if_true] at hhold ⊢
    left
    refine ⟨by omega, ?_⟩
    simp only [nuOf, Int.natAbs_natCast, hdec, decide_eq_true_eq]
    exact hhold

/-! ### The option-free part is a subset of the ETV clauses -/

theorem mem_chainClauses_of_mem_chainClausesB {t : Bool} {K N : ℕ} {mono : Bool} {c : Clause}
    (hc : c ∈ chainClausesB t K N mono) : c ∈ chainClauses t K N := by
  simp only [chainClausesB, chainClauses, List.mem_append] at hc ⊢
  rcases hc with ((hc | hc) | hc) | hc
  · exact Or.inl (Or.inl (Or.inl hc))
  · exact Or.inl (Or.inl (Or.inr hc))
  · left; right
    simp only [endClauses, List.mem_map, Prod.exists] at hc
    obtain ⟨x, a, b, r, hk, rfl⟩ := hc
    simp only [vClauses, List.mem_flatMap, Prod.exists]
    exact ⟨x, a, b, r, hk, List.mem_cons_self⟩
  · split_ifs at hc
    · simp only [List.mem_append] at hc
      rcases hc with hc | hc
      · left; right
        simp only [vMonoClauses, List.mem_filterMap, Prod.exists] at hc
        obtain ⟨x, a, b, r, hk, hc⟩ := hc
        split_ifs at hc with h4
        simp only [Option.some.injEq] at hc
        subst hc
        simp only [vClauses, List.mem_flatMap, Prod.exists]
        exact ⟨x, a, b, r, hk, List.mem_cons_of_mem _ (by simp [h4])⟩
      · exact Or.inr hc
    · simp at hc

/-- The symmetry-breaking part of `trackBClauses`. -/
def sbClauses (N : ℕ) (hull mirror flip : Bool) : List Clause :=
  (if hull then hullClauses N else []) ++ (if mirror then mirrorClausesB N else []) ++
    (if flip then flipClauses else [])

theorem mem_trackBClauses {N K : ℕ} {hull mirror flip mono : Bool} {c : Clause}
    (hc : c ∈ trackBClauses N K hull mirror flip mono) :
    c ∈ etvClauses N K K K ∨ c ∈ sbClauses N hull mirror flip := by
  simp only [trackBClauses, etvClauses, sbClauses, List.mem_append] at hc ⊢
  rcases hc with (((hc | hc) | hc) | hc) | hc
  · exact Or.inl (Or.inl (Or.inl (Or.inl hc)))
  · exact Or.inl (Or.inl (Or.inl (Or.inr (mem_chainClauses_of_mem_chainClausesB hc))))
  · exact Or.inl (Or.inl (Or.inr (mem_chainClauses_of_mem_chainClausesB hc)))
  · exact Or.inl (Or.inr hc)
  · exact Or.inr hc

/-! ### Normal forms and soundness at the signotope level -/

/-- The `--hull` normal form: `X(0,i,j)` for all `0 < i < j < N`. -/
def HullForm (N : ℕ) (σ : Sig) : Prop := ∀ i j, 1 ≤ i → i < j → j < N → σ 0 i j = true

/-- The `--mirror` lex-leader: `X(1,2,3) → X(N-3,N-2,N-1)` (for `N ≥ 7`). -/
def MirrorForm (N : ℕ) (σ : Sig) : Prop :=
  7 ≤ N → σ 1 2 3 = true → σ (N - 3) (N - 2) (N - 1) = true

theorem sbClauses_holds {N : ℕ} {σ : Sig} {hull mirror flip : Bool}
    (hh : hull = true → HullForm N σ) (hm : mirror = true → MirrorForm N σ)
    (hf : flip = true → σ 0 1 2 = true) :
    ∀ c ∈ sbClauses N hull mirror flip, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [sbClauses, List.mem_append] at hc
  rcases hc with (hc | hc) | hc
  · split_ifs at hc with h
    · simp only [hullClauses, List.mem_filterMap, Prod.exists, mem_pairs] at hc
      obtain ⟨i, j, ⟨hij, hj⟩, hc⟩ := hc
      split_ifs at hc with hi
      simp only [Option.some.injEq] at hc
      subst hc
      simp only [clauseHolds_cons, holds_pos', clauseHolds_nil, or_false, assn]
      exact hh h i j hi hij hj
    · simp at hc
  · split_ifs at hc with h
    · simp only [mirrorClausesB] at hc
      split_ifs at hc with h7
      · simp only [List.mem_singleton] at hc
        subst hc
        simp only [clauseHolds_cons, holds_pos', holds_neg', clauseHolds_nil, or_false, assn]
        by_cases h1 : σ 1 2 3 = true
        · exact Or.inr (hm h h7 h1)
        · exact Or.inl h1
      · simp at hc
    · simp at hc
  · split_ifs at hc with h
    · simp only [flipClauses, List.mem_singleton] at hc
      subst hc
      simp only [clauseHolds_cons, holds_pos', clauseHolds_nil, or_false, assn]
      exact hf h
    · simp at hc

theorem sbClauses_vars {N K : ℕ} {hull mirror flip : Bool} (hN : 3 ≤ N) :
    ∀ c ∈ sbClauses N hull mirror flip, ∀ l ∈ c, l.var ∈ allVars N K K := by
  intro c hc l hl
  simp only [sbClauses, List.mem_append] at hc
  rcases hc with (hc | hc) | hc
  · split_ifs at hc with h
    · simp only [hullClauses, List.mem_filterMap, Prod.exists, mem_pairs] at hc
      obtain ⟨i, j, ⟨hij, hj⟩, hc⟩ := hc
      split_ifs at hc with hi
      simp only [Option.some.injEq] at hc
      subst hc
      simp only [List.mem_singleton] at hl
      subst hl
      exact mem_allVars_x.2 ⟨by omega, hij, hj⟩
    · simp at hc
  · split_ifs at hc with h
    · simp only [mirrorClausesB] at hc
      split_ifs at hc with h7
      · simp only [List.mem_singleton] at hc
        subst hc
        simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
        rcases hl with rfl | rfl
        · exact mem_allVars_x.2 ⟨by omega, by omega, by omega⟩
        · exact mem_allVars_x.2 ⟨by omega, by omega, by omega⟩
      · simp at hc
    · simp at hc
  · split_ifs at hc with h
    · simp only [flipClauses, List.mem_singleton] at hc
      subst hc
      simp only [List.mem_singleton] at hl
      subst hl
      exact mem_allVars_x.2 ⟨by omega, by omega, by omega⟩
    · simp at hc

/-- **Soundness of `gen_cnf.py N K` (all options) at the signotope level.** A signotope on
`N ≥ 3` points with no `K`-gon (`K ≥ 2`), in the normal forms required by the chosen options,
gives a model of `dimacsB N K hull mirror flip mono`. -/
theorem dimacsB_satisfiable_of_signotope {N K : ℕ} {σ : Sig} {hull mirror flip mono : Bool}
    (hN : 3 ≤ N) (hK2 : 2 ≤ K) (hσ : IsSignotope N σ) (hK : ¬HasGon σ N K)
    (hh : hull = true → HullForm N σ) (hm : mirror = true → MirrorForm N σ)
    (hf : flip = true → σ 0 1 2 = true) :
    DimacsSatisfiable (dimacsB N K hull mirror flip mono) := by
  have hA : ¬HasCap σ N K := fun h => hK (hasGon_of_hasCap hK2 h)
  have hU : ¬HasCup σ N K := fun h => hK (hasGon_of_hasCup hK2 h)
  refine ⟨nuOf N K K (assn σ), dimacsSat_of_clauses _ ?_ ?_⟩
  · intro c hc l hl
    rcases mem_trackBClauses hc with hc | hc
    · exact etvClauses_vars c hc l hl
    · exact sbClauses_vars hN c hc l hl
  · intro c hc
    rcases mem_trackBClauses hc with hc | hc
    · exact etvClauses_sound hσ hA hU hK c hc
    · exact sbClauses_holds hh hm hf c hc

/-! ### `--flip`: complementing a signotope -/

/-- The complement (y-reflection) of `σ`. -/
def compl (σ : Sig) : Sig := fun i j k => !σ i j k

theorem isSignotope_compl {N : ℕ} {σ : Sig} (hσ : IsSignotope N σ) : IsSignotope N (compl σ) := by
  intro i j k l hij hjk hkl hl
  have h := hσ i j k l hij hjk hkl hl
  simp only [compl]
  revert h
  cases σ i j k <;> cases σ i j l <;> cases σ i k l <;> cases σ j k l <;> decide

theorem chain_compl {σ : Sig} {t : Bool} : ∀ {l : List ℕ}, Chain (compl σ) t l → Chain σ (!t) l
  | [], _ => trivial
  | [_], _ => trivial
  | [_, _], h => h
  | _ :: _ :: _ :: _, ⟨h1, h2, h3⟩ =>
      ⟨h1, by simp only [compl] at h2; rw [← h2, Bool.not_not], chain_compl h3⟩

theorem hasGon_of_compl {N K : ℕ} {σ : Sig} (h : HasGon (compl σ) N K) : HasGon σ N K := by
  obtain ⟨l₁, l₂, h1, h2, hl1, hl2, hhead, hlast, hK, hN1, hN2⟩ := h
  exact ⟨l₂, l₁, chain_compl h2, chain_compl h1, hl2, hl1, hhead.symm, hlast.symm,
    by omega, hN2, hN1⟩

/-- **`--flip` is sound**, and so are the option-free files: a signotope on `N ≥ 3` points
with no `K`-gon gives a model of `gen_cnf.py N K [--flip] [--no-mono]`. -/
theorem dimacsB_noHull_satisfiable {N K : ℕ} {σ : Sig} {flip mono : Bool} (hN : 3 ≤ N)
    (hK2 : 2 ≤ K) (hσ : IsSignotope N σ) (hK : ¬HasGon σ N K) :
    DimacsSatisfiable (dimacsB N K false false flip mono) := by
  by_cases h0 : σ 0 1 2 = true
  · exact dimacsB_satisfiable_of_signotope hN hK2 hσ hK (by simp) (by simp) (fun _ => h0)
  · refine dimacsB_satisfiable_of_signotope hN hK2 (isSignotope_compl hσ)
      (fun h => hK (hasGon_of_compl h)) (by simp) (by simp) (fun _ => ?_)
    simp only [compl]
    simpa using h0

/-- **What an UNSAT certificate for `gen_cnf.py N K [--flip] [--no-mono]` proves**
(`N ≥ 3`, `K ≥ 4`): every `N` points in general position contain a convex `K`-gon. -/
theorem forcesConvexNGon_of_unsat_trackB {N K : ℕ} {flip mono : Bool}
    (hunsat : ¬DimacsSatisfiable (dimacsB N K false false flip mono)) (hN : 3 ≤ N)
    (hK : 4 ≤ K) : ForcesConvexNGon N K := by
  apply distinctXReduction N K
  intro S hgp hS hcard
  obtain ⟨P, hx, hP⟩ := exists_xsorted S hS
  subst hcard
  have hgp' : GeneralPosition (ptSet P S.card) := by rw [hP]; exact hgp
  by_contra hno
  apply hunsat
  refine dimacsB_noHull_satisfiable hN (by omega) (isSignotope_sigOf hx) ?_
  intro hg
  apply hno
  rw [← hP]
  exact hasConvexNGon_of_hasGon hx hgp' hK hg

end ETV
