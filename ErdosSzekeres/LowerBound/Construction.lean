import ErdosSzekeres.LowerBound.Stacking
import ErdosSzekeres.LowerBound.Placement

/-! The Erdős–Szekeres construction of `2 ^ (n - 2)` points without a convex
`n`-gon.

First, for `k, l ≥ 2` a set of `choose (k + l - 4) (k - 2)` points with no
`k`-cup and no `l`-cap is built by stacking upward. Then the blocks
`T i` with parameters `(n - i, i + 2)`, `i = 0, …, n - 2`, are stacked
downward. A convex subset meeting several blocks is a cap in its first block,
uses at most one point of each later intermediate block, and is a cup in its
last block; this gives at most `n - 1` points. -/

namespace ErdosSzekeres.LowerBound

/-- A subset of a singleton has at most one point. -/
private theorem card_le_of_subset_singleton {t : Finset Point} {p : Point} (ht : t ⊆ {p})
    {m : ℕ} (hm : 1 ≤ m) : t.card ≤ m :=
  (Finset.card_le_card ht).trans (by simpa using hm)

/-- A single point satisfies every bound of the construction. -/
private theorem singleton_spec (p : Point) {c m m' : ℕ}
    (hc : 1 ≤ c) (hm : 1 ≤ m) (hm' : 1 ≤ m') :
    GeneralPosition {p} ∧ DistinctX {p} ∧ ChainBound 1 m {p} ∧ ChainBound (-1) m' {p} ∧
      ConvexBound c {p} := by
  refine ⟨?_, by simp [DistinctX], fun t ht _ => card_le_of_subset_singleton ht hm,
    fun t ht _ => card_le_of_subset_singleton ht hm',
    fun t ht _ => card_le_of_subset_singleton ht hc⟩
  intro a ha b hb _ _ hab
  simp only [Finset.mem_singleton] at ha hb
  exact absurd (ha.trans hb.symm) hab

/-- Erdős–Szekeres: point sets with no `k`-cup and no `l`-cap of binomial size.
Their convex subsets have fewer than `k + l - 2` points. -/
theorem exists_cupCapFree (k l : ℕ) (hk : 2 ≤ k) (hl : 2 ≤ l) :
    ∃ s : Finset Point, GeneralPosition s ∧ DistinctX s ∧
      s.card = (k + l - 4).choose (k - 2) ∧
      ChainBound 1 (k - 1) s ∧ ChainBound (-1) (l - 1) s ∧ ConvexBound (k + l - 3) s := by
  by_cases hk2 : k = 2
  · subst hk2
    obtain ⟨h1, h2, h3, h4, h5⟩ := singleton_spec 0 (c := 2 + l - 3) (m := 1) (m' := l - 1)
      (by omega) le_rfl (by omega)
    exact ⟨{0}, h1, h2, by simp, h3, h4, h5⟩
  by_cases hl2 : l = 2
  · subst hl2
    obtain ⟨h1, h2, h3, h4, h5⟩ := singleton_spec 0 (c := k + 2 - 3) (m := k - 1) (m' := 1)
      (by omega) (by omega) le_rfl
    exact ⟨{0}, h1, h2, by simp, h3, h4, h5⟩
  obtain ⟨A, hAgp, hAx, hAcard, hAcup, hAcap, hAconv⟩ :=
    exists_cupCapFree (k - 1) l (by omega) hl
  obtain ⟨B, hBgp, hBx, hBcard, hBcup, hBcap, hBconv⟩ :=
    exists_cupCapFree k (l - 1) hk (by omega)
  obtain ⟨v, hst⟩ := exists_stacked 1 one_ne_zero A B
  refine ⟨A ∪ translate v B, hst.generalPosition_union hAgp (generalPosition_translate hBgp)
    hAx (distinctX_translate hBx), hst.distinctX_union hAx (distinctX_translate hBx), ?_,
    (hst.chainBound_union (distinctX_translate hBx) hAcup (chainBound_translate hBcup)).mono
      (by omega),
    (hst.chainBound_neg_union hAx hAcap (chainBound_translate hBcap)).mono (by omega),
    (hst.convexBound_union one_ne_zero hAgp (generalPosition_translate hBgp) hAconv
      (convexBound_translate hBconv) hAcup (chainBound_translate hBcap)).mono (by omega)⟩
  rw [hst.card_union, card_translate, hAcard, hBcard]
  convert (Nat.choose_succ_succ (k + l - 5) (k - 3)).symm using 2 <;> congr 1 <;> omega
termination_by k + l
decreasing_by all_goals omega

/-- The first `j` blocks of the construction, stacked downward. -/
theorem exists_capChain (n : ℕ) (hn : 3 ≤ n) (j : ℕ) (hj : 1 ≤ j) (hjn : j ≤ n - 1) :
    ∃ s : Finset Point, GeneralPosition s ∧ DistinctX s ∧
      s.card = ∑ i ∈ Finset.range j, (n - 2).choose i ∧
      ChainBound (-1) j s ∧ ConvexBound (n - 1) s := by
  induction j, hj using Nat.le_induction with
  | base =>
    obtain ⟨s, hgp, hx, hcard, -, hcap, hconv⟩ := exists_cupCapFree n 2 (by omega) le_rfl
    refine ⟨s, hgp, hx, ?_, hcap, hconv.mono (by omega)⟩
    rw [hcard, show n + 2 - 4 = n - 2 by omega]
    simp
  | succ j hj ih =>
    obtain ⟨U, hUgp, hUx, hUcard, hUcap, hUconv⟩ := ih (by omega)
    obtain ⟨T, hTgp, hTx, hTcard, hTcup, hTcap, hTconv⟩ :=
      exists_cupCapFree (n - j) (j + 2) (by omega) (by omega)
    obtain ⟨v, hst⟩ := exists_stacked (-1) (by norm_num) U T
    have hTcup' : ChainBound (-(-1)) (n - j - 1) (translate v T) := by
      rw [neg_neg]
      exact chainBound_translate hTcup
    refine ⟨U ∪ translate v T, hst.generalPosition_union hUgp (generalPosition_translate hTgp)
      hUx (distinctX_translate hTx), hst.distinctX_union hUx (distinctX_translate hTx), ?_,
      (hst.chainBound_union (distinctX_translate hTx) hUcap (chainBound_translate hTcap)).mono
        (by omega),
      (hst.convexBound_union (by norm_num) hUgp (generalPosition_translate hTgp) hUconv
        (convexBound_translate hTconv) hUcap hTcup').mono (by omega)⟩
    rw [hst.card_union, card_translate, hUcard, hTcard, Finset.sum_range_succ,
      show n - j + (j + 2) - 4 = n - 2 by omega, show n - j - 2 = n - 2 - j by omega,
      Nat.choose_symm (by omega)]

/-- Erdős–Szekeres (1961): there are `2 ^ (n - 2)` points in general position
with no `n` points in convex position. -/
theorem exists_generalPosition_without_convexNGon (n : ℕ) (hn : 3 ≤ n) :
    ∃ s : Finset Point, GeneralPosition s ∧ s.card = 2 ^ (n - 2) ∧ ¬ HasConvexNGon n s := by
  obtain ⟨s, hgp, -, hcard, -, hconv⟩ := exists_capChain n hn (n - 1) (by omega) le_rfl
  refine ⟨s, hgp, ?_, not_hasConvexNGon_of_convexBound hconv (by omega)⟩
  rw [hcard, show n - 1 = n - 2 + 1 by omega, Nat.sum_range_choose]

end ErdosSzekeres.LowerBound

namespace ErdosSzekeres

/-- `2 ^ (n - 2)` points do not force a convex `n`-gon. -/
theorem not_forcesConvexNGon_two_pow (n : ℕ) (hn : 3 ≤ n) :
    ¬ ForcesConvexNGon (2 ^ (n - 2)) n := by
  intro h
  obtain ⟨s, hgp, hcard, hno⟩ := LowerBound.exists_generalPosition_without_convexNGon n hn
  exact hno (h s hgp hcard.ge)

/-- Every sufficient number of points is at least the conjectured value. -/
theorem conjecturedBound_le_of_forces {N n : ℕ} (hn : 3 ≤ n) (h : ForcesConvexNGon N n) :
    conjecturedBound n ≤ N := by
  by_contra hN
  exact not_forcesConvexNGon_two_pow n hn (h.mono (by unfold conjecturedBound at hN; omega))

/-- The conjecture asserts exactly that `2 ^ (n - 2) + 1` is the least sufficient number. -/
theorem erdosSzekeresConjecture_iff_isLeast :
    ErdosSzekeresConjecture ↔
      ∀ n : ℕ, 3 ≤ n → IsLeast {N : ℕ | ForcesConvexNGon N n} (conjecturedBound n) :=
  ⟨fun h n hn => ⟨h n hn, fun _ hN => conjecturedBound_le_of_forces hn hN⟩,
    fun h n hn => (h n hn).1⟩

/-- There are 64 points in general position with no convex octagon. -/
theorem not_forcesConvexNGon_64_8 : ¬ ForcesConvexNGon 64 8 :=
  not_forcesConvexNGon_two_pow 8 (by norm_num)

/-- Lower bound for octagons: any number of points forcing a convex octagon is at least 65. -/
theorem octagon_lower_bound {N : ℕ} (h : ForcesConvexNGon N 8) : 65 ≤ N :=
  conjecturedBound_le_of_forces (by norm_num) h

end ErdosSzekeres
