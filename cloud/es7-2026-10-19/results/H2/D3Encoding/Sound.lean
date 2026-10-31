import D3Encoding.Conv

/-!
# Soundness of the whole D3 CNF at the chirotope level

`d3Cnf_sat`: if `χ` is an alternating, D3-equivariant sign function on the `3 t + 1` points
(orbit points and centre) satisfying A4, the 3-term Grassmann–Plücker relations, the centre
facts and the labelling normal form, and no `K` set points are in convex position, then
the clause list of `d3cnf.py (3 t) K` has a model.
-/

namespace D3

open Std

section
variable {t K : Nat} {χ : Nat → Nat → Nat → Int}

/-! ### The conv keys -/

theorem mem_convKeys {R : List Nat} :
    R ∈ convKeys t K ↔ 4 ≤ R.length ∧ R.length < K ∧ R ∈ combs (List.range (3 * t)) R.length ∧
      isCanon t R = true := by
  unfold convKeys
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨r, hr, hR⟩
    rw [List.mem_range'] at hr
    rw [List.mem_filter] at hR
    have hl := (mem_combs_range.1 hR.1).2.2
    subst hl
    exact ⟨by omega, by omega, hR.1, hR.2⟩
  · rintro ⟨h1, h2, h3, h4⟩
    exact ⟨R.length, List.mem_range'.2 ⟨R.length - 4, by omega, by omega⟩,
      List.mem_filter.2 ⟨h3, h4⟩⟩

theorem convKeys_lengths :
    (convKeys t K).Pairwise (fun X Y => X.length ≤ Y.length) := by
  unfold convKeys
  rw [List.pairwise_flatMap]
  refine ⟨fun r _ => ?_, ?_⟩
  · apply List.Pairwise.imp_of_mem _ (List.pairwise_iff_forall_sublist.2 fun _ => trivial)
    intro X Y hX hY _
    rw [(mem_combs_range.1 (List.mem_filter.1 hX).1).2.2,
      (mem_combs_range.1 (List.mem_filter.1 hY).1).2.2]
    exact Nat.le_refl _
  · apply List.Pairwise.imp_of_mem _ (List.pairwise_lt_range' (s := 4) (n := K - 4) (step := 1))
    intro a b _ _ hab X hX Y hY
    rw [(mem_combs_range.1 (List.mem_filter.1 hX).1).2.2,
      (mem_combs_range.1 (List.mem_filter.1 hY).1).2.2]
    omega

/-- `canon` of a set of `r ≥ 1` set points minus one point is a canonical key of size
`r - 1`. -/
theorem canon_erase_spec (hG : GroupClosed t) {S : List Nat}
    (hS : S.Pairwise (· < ·)) (hSP : ∀ y ∈ S, y < 3 * t) (i : Nat) :
    (canon t (S.eraseIdx i)).length = (S.eraseIdx i).length ∧
    canon t (S.eraseIdx i) ∈ combs (List.range (3 * t)) (canon t (S.eraseIdx i)).length ∧
    isCanon t (canon t (S.eraseIdx i)) = true := by
  have hY : (S.eraseIdx i).Pairwise (· < ·) := hS.sublist (List.eraseIdx_sublist S i)
  have hYP : ∀ y ∈ S.eraseIdx i, y < 3 * t := fun y hy =>
    hSP y ((List.eraseIdx_sublist S i).subset hy)
  have hYP' : ∀ y ∈ S.eraseIdx i, y < 3 * t + 1 := fun y hy => by have := hYP y hy; omega
  obtain ⟨hm, -⟩ := canon_spec hY hYP'
  obtain ⟨g, hg, he⟩ := image_of_mem_orbit hm
  obtain ⟨h1, h2⟩ := sorted_image hY hYP hg
  rw [← he] at h1 h2
  refine ⟨orbit_length hm, mem_combs_range.2 ⟨h1, h2, rfl⟩, ?_⟩
  unfold isCanon
  rw [canon_canon hG hY hYP]
  simp

/-! ### The assignment -/

/-- The intended value of conv variable `v`: the key with number `v` is convex. -/
def NuC (χ : Nat → Nat → Nat → Int) (A : List (List Nat)) (nX v : Nat) : Prop :=
  ∃ j X, A[j]? = some X ∧ v = nX + 1 + j ∧ ConvAll χ X

open Classical in
noncomputable def nuD3 (χ : Nat → Nat → Nat → Int) (tv : TV) (nX : Nat) (A : List (List Nat))
    (v : Nat) : Bool :=
  if v ≤ nX then decide (NuT χ tv v) else decide (NuC χ A nX v)

open Classical in
theorem nuD3_conv {tv : TV} {nX : Nat} {A : List (List Nat)} {j : Nat} {X : List Nat}
    (h : A[j]? = some X) : nuD3 χ tv nX A (nX + 1 + j) = true ↔ ConvAll χ X := by
  unfold nuD3
  rw [if_neg (by omega), decide_eq_true_iff]
  constructor
  · rintro ⟨j', X', h', hv, hc⟩
    have : j' = j := by omega
    subst this
    rw [h] at h'
    cases h'
    exact hc
  · intro hc; exact ⟨j, X, h, rfl, hc⟩

/-! ### The fold over the conv keys -/

/-- The conv map after the prefix `done`: key `R` gets `nX + 1 + done.idxOf R`. -/
def CVForm (nX : Nat) (done : List (List Nat)) (cv : CV) : Prop :=
  ∀ R, cv[R]? = if R ∈ done then some (nX + 1 + done.idxOf R) else none

theorem cvForm_step {nX : Nat} {done : List (List Nat)} {cv : CV} (h : CVForm nX done cv)
    (S : List Nat) : CVForm nX (done ++ [S]) (cv.insertIfNew S (nX + done.length + 1)) := by
  intro R
  rw [HashMap.getElem?_insertIfNew, h R, List.idxOf_append]
  by_cases hR : R ∈ done
  · have hSR : ¬((S == R) = true ∧ S ∉ cv) := by
      rintro ⟨e, hS⟩
      have e' : S = R := by simpa using e
      subst e'
      apply hS
      rw [HashMap.mem_iff_isSome_getElem?, h S, if_pos hR]
      rfl
    rw [if_neg hSR, if_pos hR, if_pos (List.mem_append_left _ hR), if_pos hR]
  · rw [if_neg hR]
    by_cases e : S = R
    · subst e
      have hS : S ∉ cv := by
        rw [HashMap.mem_iff_isSome_getElem?, h S, if_neg hR]; simp
      rw [if_pos ⟨by simp, hS⟩, if_pos (by simp), if_neg hR]
      simp [List.idxOf_cons_self]
      omega
    · have hSR : ¬((S == R) = true ∧ S ∉ cv) := by
        rintro ⟨e', -⟩; exact e (by simpa using e')
      rw [if_neg hSR, if_neg]
      simp only [List.mem_append, List.mem_singleton, not_or]
      exact ⟨hR, Ne.symm e⟩

/-- Everything the clause soundness needs about the model. -/
structure Model (t K : Nat) (χ : Nat → Nat → Nat → Int) where
  hK : 5 ≤ K
  hG : GroupClosed t
  hχ : Chirotope t χ
  hNo : ∀ X : List Nat, X.Pairwise (· < ·) → X.length = K → (∀ x ∈ X, x < 3 * t) →
    ¬ConvAll χ X

theorem getElem?_of_prefix {A done rest : List (List Nat)} {S : List Nat}
    (hA : A = done ++ S :: rest) : A[done.length]? = some S := by
  subst hA; simp

theorem idx_of_mem {R : List Nat} : ∀ {A : List (List Nat)}, R ∈ A → A[A.idxOf R]? = some R
  | a :: A, hR => by
    rw [List.idxOf_cons]
    by_cases e : a = R
    · subst e; simp
    · have hR' : R ∈ A := by
        rcases List.mem_cons.1 hR with h | h
        · exact absurd h.symm e
        · exact h
      have : (a == R) = false := by simpa using e
      rw [this]
      simpa using idx_of_mem hR'

theorem lit_pos {ν : Nat → Bool} {v : Nat} (h : ν v = true) (hv : 1 ≤ v) :
    LitSat ν (v : Int) := Or.inl ⟨by omega, by simpa using h⟩

theorem lit_neg {ν : Nat → Bool} {v : Nat} (h : ν v = false) (hv : 1 ≤ v) :
    LitSat ν (-(v : Int)) := Or.inr ⟨by omega, by simpa using h⟩

end

end D3
