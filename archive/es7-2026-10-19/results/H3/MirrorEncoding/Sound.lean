import MirrorEncoding.Gen
import ETVEncoding.TrackB

/-!
# Soundness of the mirror CNFs at the signotope level

If `σ` is a signotope on `N` points with no `K`-gon that is mirror-symmetric
(`σ(m-k,m-j,m-i) = σ(i,j,k)` for `lo ≤ i`), then
* `hullCnf N K` (= `hm33k7.sub.cnf` for `N = 33`, `K = 7`) is satisfiable when `σ` is in the
  `--hull` normal form (`X(0,i,j)` true);
* `interiorCnf N K` (= `m33k7int.sub.cnf`) is satisfiable when the axis point `(N-1)/2` is
  neither on the upper nor on the lower chain (`AxisInterior`). The unit `X(0,1,2)` is
  handled by complementing `σ` (the y-reflection), which keeps all other hypotheses.

The model is always `nuOf N K K (assn σ)`, the one of `results/H`. Orbit substitution is
sound because this model gives the same value to `X(i,j,k)` and to its mirror image.
-/

namespace Mir

open ETV Lit

/-- Mirror symmetry of a signotope for `gen_etv.py --mirror [--hull]` (0-based). -/
def MirSym (N : ℕ) (hull : Bool) (σ : Sig) : Prop :=
  ∀ i j k, lo hull ≤ i → i < j → j < k → k < N →
    σ (mm N hull - k) (mm N hull - j) (mm N hull - i) = σ i j k

/-- The axis point `c = (N-1)/2` is below some chord `ik` (`i < c < k`) and above some chord:
the combinatorial form of "`c` is not extreme". -/
def AxisInterior (N : ℕ) (σ : Sig) : Prop :=
  (∃ i k, i < axisPt N ∧ axisPt N < k ∧ k < N ∧ σ i (axisPt N) k = true) ∧
  (∃ i k, i < axisPt N ∧ axisPt N < k ∧ k < N ∧ σ i (axisPt N) k = false)

/-! ### Membership lemmas for the normalisation -/

theorem mem_eraseDups_int : ∀ (c : List ℤ) (z : ℤ), z ∈ c.eraseDups ↔ z ∈ c
  | [], z => by simp
  | a :: as, z => by
    rw [List.eraseDups_cons]
    have ih := mem_eraseDups_int (as.filter fun b => !b == a) z
    simp only [List.mem_cons, ih, List.mem_filter, Bool.not_eq_true', beq_eq_false_iff_ne]
    by_cases h : z = a
    · simp [h]
    · simp [h]
termination_by c => c.length
decreasing_by
  simp only [List.length_cons]
  exact Nat.lt_succ_of_le (List.length_filter_le _ _)

theorem mem_normClause {c : List ℤ} {z : ℤ} : z ∈ normClause c ↔ z ∈ c := by
  simp only [normClause, List.mem_mergeSort, mem_eraseDups_int]

/-! ### `mirgen` keeps only (normalised) input clauses -/

/-- A DIMACS literal holds under `ν`. -/
def LitSat (ν : ℕ → Bool) (z : ℤ) : Prop :=
  (0 < z ∧ ν z.natAbs = true) ∨ (z < 0 ∧ ν z.natAbs = false)

theorem dimacsSat_iff {cls : List (List ℤ)} {ν : ℕ → Bool} :
    DimacsSat cls ν ↔ ∀ c ∈ cls, ∃ z ∈ c, LitSat ν z := Iff.rfl

theorem foldl_mirStep (P : List ℤ → Prop) (hP : ∀ c, P c → P (normClause c)) :
    ∀ (l : List (List ℤ)) (st : Std.HashSet (List ℤ) × Array (List ℤ)),
      (∀ c ∈ l, P c) → (∀ k ∈ st.2.toList, P k) →
      ∀ k ∈ (l.foldl mirStep st).2.toList, P k
  | [], st, _, hst => hst
  | c :: l, st, hl, hst => by
    rw [List.foldl_cons]
    apply foldl_mirStep P hP l _ (fun c' hc' => hl c' (List.mem_cons_of_mem _ hc'))
    unfold mirStep
    split
    · exact hst
    · split
      · exact hst
      · intro k hk
        simp only [Array.toList_push, List.mem_append, List.mem_singleton] at hk
        rcases hk with hk | rfl
        · exact hst k hk
        · exact hP c (hl c (List.mem_cons_self))

/-- **`mirgen` is sound**: every model of the input is a model of the output. -/
theorem dimacsSat_mirgen {cls : List (List ℤ)} {ν : ℕ → Bool} (h : DimacsSat cls ν) :
    DimacsSat (mirgen cls) ν := by
  intro k hk
  refine foldl_mirStep (fun c => ∃ z ∈ c, LitSat ν z) ?_ cls (∅, #[]) h (by simp) k hk
  rintro c ⟨z, hz, hs⟩
  exact ⟨z, mem_normClause.2 hz, hs⟩

/-! ### The substitution respects the model of a symmetric signotope -/

theorem subVar_mem {N A U : ℕ} {hull : Bool} {v : Var} (hv : v ∈ allVars N A U) :
    subVar N hull v ∈ allVars N A U := by
  cases v with
  | x i j k =>
    simp only [subVar]
    split
    · rename_i h
      rw [mem_allVars_x]
      cases hull <;> simp only [mm, lo, if_true, Bool.false_eq_true, if_false] at h ⊢ <;> omega
    · exact hv
  | v => exact hv
  | e => exact hv

theorem assn_subVar {N : ℕ} {hull : Bool} {σ : Sig} (hS : MirSym N hull σ) {v : Var} :
    assn σ (subVar N hull v) ↔ assn σ v := by
  cases v with
  | x i j k =>
    simp only [subVar]
    split
    · rename_i h
      simp only [assn]
      rw [hS i j k h.1 h.2.1 h.2.2.1 h.2.2.2.1]
    · exact Iff.rfl
  | v => exact Iff.rfl
  | e => exact Iff.rfl

theorem holds_subLit {N : ℕ} {hull : Bool} {σ : Sig} (hS : MirSym N hull σ) (l : Lit) :
    (subLit N hull l).Holds (assn σ) ↔ l.Holds (assn σ) := by
  unfold subLit Lit.Holds
  cases l.pos <;> simp [assn_subVar hS]

/-- The DIMACS literal of an allocated structured literal holds iff the literal does. -/
theorem litSat_litToInt {N A U : ℕ} {τ : Var → Prop} {l : Lit} (hv : l.var ∈ allVars N A U)
    (h : l.Holds τ) : LitSat (nuOf N A U τ) (litToInt (num N A U) l) := by
  classical
  have hdec := decode_numberMap hv
  have hnum := numberMap_getD hv
  unfold litToInt num
  unfold Lit.Holds at h
  cases hpos : l.pos
  · simp only [hpos, Bool.false_eq_true, if_false] at h ⊢
    right
    refine ⟨by omega, ?_⟩
    simp only [nuOf, Int.natAbs_neg, Int.natAbs_natCast, hdec, decide_eq_false_iff_not]
    exact h
  · simp only [hpos, if_true] at h ⊢
    left
    refine ⟨by omega, ?_⟩
    simp only [nuOf, Int.natAbs_natCast, hdec, decide_eq_true_eq]
    exact h

/-! ### The clauses of `gen_etv.py --mirror [--hull]` -/

theorem mirClauses_vars {N A U K : ℕ} {hull : Bool} :
    ∀ c ∈ mirClauses N A U K hull, ∀ l ∈ c, l.var ∈ allVars N A U := by
  intro c hc l hl
  simp only [mirClauses, List.mem_append] at hc
  rcases hc with (hc | hc) | hc
  · exact etvClauses_vars c hc l hl
  · cases hull
    · simp at hc
    · simp only [if_true, hullUnits, List.mem_map, List.mem_filter, Prod.exists] at hc
      obtain ⟨i, j, ⟨hij, hi⟩, rfl⟩ := hc
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
      subst hl
      simp only [pos', mem_allVars_x]
      have := (mem_pairs (N := N)).1 hij
      simp at hi
      omega
  · simp only [mirrorEqs, List.mem_flatMap, Prod.exists] at hc
    obtain ⟨i, j, k, hijk, hc⟩ := hc
    have hr := mem_triples.1 hijk
    split at hc
    · rename_i h
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
      rcases hc with rfl | rfl <;>
        simp only [List.mem_cons, List.not_mem_nil, or_false] at hl <;>
        rcases hl with rfl | rfl <;>
        simp only [pos', neg', mem_allVars_x] <;>
        cases hull <;> simp only [mm, lo, if_true, Bool.false_eq_true, if_false] at h ⊢ <;> omega
    · simp at hc

theorem mirClauses_holds {N A U K : ℕ} {hull : Bool} {σ : Sig} (hσ : IsSignotope N σ)
    (hA : ¬HasCap σ N A) (hU : ¬HasCup σ N U) (hK : ¬HasGon σ N K)
    (hH : hull = true → HullForm N σ) (hS : MirSym N hull σ) :
    ∀ c ∈ mirClauses N A U K hull, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [mirClauses, List.mem_append] at hc
  rcases hc with (hc | hc) | hc
  · exact etvClauses_sound hσ hA hU hK c hc
  · cases hull
    · simp at hc
    · simp only [if_true, hullUnits, List.mem_map, List.mem_filter, Prod.exists] at hc
      obtain ⟨i, j, ⟨hij, hi⟩, rfl⟩ := hc
      have := (mem_pairs (N := N)).1 hij
      simp at hi
      refine ⟨_, List.mem_singleton_self _, ?_⟩
      simp only [Lit.Holds, pos', if_true, assn]
      exact hH rfl i j hi (by omega) (by omega)
  · simp only [mirrorEqs, List.mem_flatMap, Prod.exists] at hc
    obtain ⟨i, j, k, hijk, hc⟩ := hc
    have hr := mem_triples.1 hijk
    split at hc
    · rename_i h
      have e := hS i j k h.1 hr.1 hr.2.1 hr.2.2
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
      rcases hc with rfl | rfl
      · cases hv : σ i j k
        · exact ⟨_, List.mem_cons_self, by simp [Lit.Holds, neg', assn, hv]⟩
        · exact ⟨_, List.mem_cons_of_mem _ List.mem_cons_self,
            by simp [Lit.Holds, pos', assn, e, hv]⟩
      · cases hv : σ i j k
        · exact ⟨_, List.mem_cons_of_mem _ List.mem_cons_self,
            by simp [Lit.Holds, neg', assn, e, hv]⟩
        · exact ⟨_, List.mem_cons_self, by simp [Lit.Holds, pos', assn, hv]⟩
    · simp at hc

theorem dimacsSat_subDimacs {N A U K : ℕ} {hull : Bool} {σ : Sig} (hσ : IsSignotope N σ)
    (hA : ¬HasCap σ N A) (hU : ¬HasCup σ N U) (hK : ¬HasGon σ N K)
    (hH : hull = true → HullForm N σ) (hS : MirSym N hull σ) :
    DimacsSat (subDimacs N A U K hull) (nuOf N A U (assn σ)) := by
  intro c hc
  simp only [subDimacs, List.mem_map] at hc
  obtain ⟨c', hc', rfl⟩ := hc
  obtain ⟨l, hl, hhold⟩ := mirClauses_holds hσ hA hU hK hH hS c' hc'
  have hv := mirClauses_vars c' hc' l hl
  refine ⟨_, List.mem_map_of_mem hl, ?_⟩
  exact litSat_litToInt (subVar_mem hv) ((holds_subLit hS l).2 hhold)

/-! ### Main signotope-level theorems -/

theorem not_hasCap_of_not_hasGon {σ : Sig} {N K : ℕ} (hK2 : 2 ≤ K) (hK : ¬HasGon σ N K) :
    ¬HasCap σ N K := fun h => hK (hasGon_of_hasCap hK2 h)

theorem not_hasCup_of_not_hasGon {σ : Sig} {N K : ℕ} (hK2 : 2 ≤ K) (hK : ¬HasGon σ N K) :
    ¬HasCup σ N K := fun h => hK (hasGon_of_hasCup hK2 h)

/-- **Sub-case (i), signotope level.** A mirror-symmetric signotope in `--hull` normal form
with no `K`-gon satisfies `hullCnf N K` (= `hm33k7.sub.cnf` for `(33, 7)`). -/
theorem hullCnf_satisfiable {N K : ℕ} {σ : Sig} (hK2 : 2 ≤ K) (hσ : IsSignotope N σ)
    (hK : ¬HasGon σ N K) (hH : HullForm N σ) (hS : MirSym N true σ) :
    DimacsSatisfiable (hullCnf N K) :=
  ⟨_, dimacsSat_mirgen (dimacsSat_subDimacs hσ (not_hasCap_of_not_hasGon hK2 hK)
    (not_hasCup_of_not_hasGon hK2 hK) hK (fun _ => hH) hS)⟩

/-- The value of a substituted triple literal under the model. -/
theorem num_sub_pos {N A U i j k : ℕ} (h : i < j ∧ j < k ∧ k < N) :
    0 < (((num N A U).getD (subVar N false (.x i j k)) 0 : ℕ) : ℤ) := by
  have hv := subVar_mem (hull := false) ((mem_allVars_x (A := A) (U := U)).2 h)
  rw [num, numberMap_getD hv]
  omega

theorem nu_sub {N A U i j k : ℕ} {σ : Sig} (hS : MirSym N false σ) (h : i < j ∧ j < k ∧ k < N) :
    nuOf N A U (assn σ) ((num N A U).getD (subVar N false (.x i j k)) 0) = true ↔
      σ i j k = true := by
  have hv := subVar_mem (hull := false) ((mem_allVars_x (A := A) (U := U)).2 h)
  rw [num, nuOf_num hv, assn_subVar hS]
  rfl

theorem dimacsSat_interior {N A U : ℕ} {σ : Sig} (hS : MirSym N false σ)
    (hI : AxisInterior N σ) (hN : 3 ≤ N) (h012 : σ 0 1 2 = true) :
    DimacsSat (interiorClauses N A U ++ yflipUnit N A U) (nuOf N A U (assn σ)) := by
  obtain ⟨⟨i, k, hi, hk, hkN, hv⟩, ⟨i', k', hi', hk', hkN', hv'⟩⟩ := hI
  have memI : ∀ a b, a < axisPt N → axisPt N < b → b < N →
      (((num N A U).getD (subVar N false (.x a (axisPt N) b)) 0 : ℕ) : ℤ) ∈
        interiorLits N A U := by
    intro a b ha hb hbN
    simp only [interiorLits, mem_normClause, List.mem_flatMap, List.mem_range, List.mem_map,
      List.mem_range']
    exact ⟨a, ha, b, ⟨b - (axisPt N + 1), by omega, by omega⟩, rfl⟩
  intro c hc
  simp only [interiorClauses, yflipUnit, List.mem_append, List.mem_cons, List.not_mem_nil,
    or_false] at hc
  rcases hc with (rfl | rfl) | rfl
  · refine ⟨_, memI i k hi hk hkN, Or.inl ⟨num_sub_pos (by omega), ?_⟩⟩
    rw [Int.natAbs_natCast, nu_sub hS (by omega)]
    exact hv
  · refine ⟨_, List.mem_map_of_mem (memI i' k' hi' hk' hkN'), Or.inr ⟨?_, ?_⟩⟩
    · have := num_sub_pos (A := A) (U := U) (N := N) (i := i') (j := axisPt N) (k := k')
        (by omega)
      omega
    · rw [Int.natAbs_neg, Int.natAbs_natCast]
      cases e : nuOf N A U (assn σ) ((num N A U).getD (subVar N false (.x i' (axisPt N) k')) 0)
      · rfl
      · rw [nu_sub hS (by omega), hv'] at e
        exact absurd e (by decide)
  · refine ⟨_, List.mem_singleton_self _, Or.inl ⟨num_sub_pos (by omega), ?_⟩⟩
    rw [Int.natAbs_natCast, nu_sub hS (by omega)]
    exact h012

theorem mirSym_compl {N : ℕ} {hull : Bool} {σ : Sig} (hS : MirSym N hull σ) :
    MirSym N hull (ETV.compl σ) := by
  intro i j k h1 h2 h3 h4
  simp only [ETV.compl, hS i j k h1 h2 h3 h4]

theorem axisInterior_compl {N : ℕ} {σ : Sig} (hI : AxisInterior N σ) :
    AxisInterior N (ETV.compl σ) := by
  obtain ⟨⟨i, k, h1, h2, h3, hv⟩, ⟨i', k', h1', h2', h3', hv'⟩⟩ := hI
  exact ⟨⟨i', k', h1', h2', h3', by simp [ETV.compl, hv']⟩,
    ⟨i, k, h1, h2, h3, by simp [ETV.compl, hv]⟩⟩

/-- **Sub-case (ii), signotope level.** A mirror-symmetric signotope (`lo = 0`) with no
`K`-gon whose axis point `(N-1)/2` is interior satisfies `interiorCnf N K`
(= `m33k7int.sub.cnf` for `(33, 7)`). -/
theorem interiorCnf_satisfiable {N K : ℕ} {σ : Sig} (hN : 3 ≤ N) (hK2 : 2 ≤ K)
    (hσ : IsSignotope N σ) (hK : ¬HasGon σ N K) (hS : MirSym N false σ)
    (hI : AxisInterior N σ) : DimacsSatisfiable (interiorCnf N K) := by
  have main : ∀ τ : Sig, IsSignotope N τ → ¬HasGon τ N K → MirSym N false τ →
      AxisInterior N τ → τ 0 1 2 = true → DimacsSatisfiable (interiorCnf N K) := by
    intro τ hτ hKτ hSτ hIτ h012
    refine ⟨nuOf N K K (assn τ), ?_⟩
    intro c hc
    simp only [interiorCnf, List.append_assoc, List.mem_append] at hc
    rcases hc with hc | hc
    · exact dimacsSat_mirgen (dimacsSat_subDimacs hτ (not_hasCap_of_not_hasGon hK2 hKτ)
        (not_hasCup_of_not_hasGon hK2 hKτ) hKτ (by simp) hSτ) c hc
    · exact dimacsSat_interior hSτ hIτ hN h012 c (List.mem_append.2 hc)
  by_cases h0 : σ 0 1 2 = true
  · exact main σ hσ hK hS hI h0
  · exact main (ETV.compl σ) (isSignotope_compl hσ) (fun h => hK (hasGon_of_compl h))
      (mirSym_compl hS) (axisInterior_compl hI) (by simpa [ETV.compl] using h0)

end Mir
