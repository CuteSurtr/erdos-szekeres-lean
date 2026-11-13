import ETVEncoding.Points

/-!
# The soundness chain for finite point sets

A finite point set with distinct x-coordinates is listed in x-order, which turns it into a
signotope. Combined with `dimacsSatisfiable_of_xsorted` this gives:

* `dimacsSatisfiable_of_pointSet`: a point set in general position with distinct
  x-coordinates, no `A`-cap, no `U`-cup and no convex `K`-gon makes `dimacs |S| A U K`
  satisfiable;
* `cap_cup_or_gon_of_unsat`: if `dimacs N A U K` is unsatisfiable, every such `N`-point set
  has an `A`-cap, a `U`-cup or a convex `K`-gon.

`dimacs N A U K` is the clause list printed by `lake exe etv_dimacs N A U K`, which is
byte-identical to `gen_etv.py N A U K` on every instance tested (see the README).
-/

namespace ETV

open ErdosSzekeres

/-- Every finite point set with distinct x-coordinates is `{P 0, …, P (|S|-1)}` for an
x-sorted sequence `P`. -/
theorem exists_xsorted (S : Finset Point) (hS : LowerBound.DistinctX S) :
    ∃ P : ℕ → Point, XSorted P S.card ∧ ptSet P S.card = S := by
  classical
  let xs : Finset ℝ := S.image (fun p => p 0)
  have hxs : xs.card = S.card := Finset.card_image_of_injOn hS
  let e := xs.orderEmbOfFin hxs
  have hmem : ∀ i : Fin S.card, ∃ p ∈ S, p 0 = e i := fun i => by
    obtain ⟨p, hp, h⟩ := Finset.mem_image.1 (Finset.orderEmbOfFin_mem xs hxs i)
    exact ⟨p, hp, h⟩
  let P : ℕ → Point := fun i =>
    if h : i < S.card then Classical.choose (hmem ⟨i, h⟩) else 0
  have hP : ∀ i (h : i < S.card), P i ∈ S ∧ P i 0 = e ⟨i, h⟩ := fun i h => by
    simp only [P, dif_pos h]
    exact Classical.choose_spec (hmem ⟨i, h⟩)
  refine ⟨P, ?_, ?_⟩
  · intro i j hij hj
    rw [(hP i (by omega)).2, (hP j hj).2]
    exact e.strictMono (by simpa [Fin.lt_def] using hij)
  · ext p
    constructor
    · intro hp
      simp only [ptSet, Finset.mem_image, Finset.mem_range] at hp
      obtain ⟨i, hi, rfl⟩ := hp
      exact (hP i hi).1
    · intro hp
      have hrange : p 0 ∈ Set.range e := by
        rw [Finset.range_orderEmbOfFin]
        simp only [Finset.coe_image, Set.mem_image, Finset.mem_coe, xs]
        exact ⟨p, hp, rfl⟩
      obtain ⟨i, hi⟩ := hrange
      have hPi := hP i.1 i.2
      have heq : P i.1 = p := hS hPi.1 hp (by
        show P i.1 0 = p 0
        rw [hPi.2]
        exact hi)
      simp only [ptSet, Finset.mem_image, Finset.mem_range]
      exact ⟨i.1, i.2, heq⟩

/-- **Soundness for finite point sets.** -/
theorem dimacsSatisfiable_of_pointSet {A U K : ℕ} (hK : 4 ≤ K) (S : Finset Point)
    (hgp : GeneralPosition S) (hS : LowerBound.DistinctX S)
    (hA : ¬HasChainPts (-1) A S) (hU : ¬HasChainPts 1 U S) (hgon : ¬HasConvexNGon K S) :
    DimacsSatisfiable (dimacs S.card A U K) := by
  obtain ⟨P, hx, hP⟩ := exists_xsorted S hS
  refine dimacsSatisfiable_of_xsorted hx ?_ hK ?_ ?_ ?_
  · rw [hP]; exact hgp
  · rw [hP]; exact hA
  · rw [hP]; exact hU
  · rw [hP]; exact hgon

/-- **What an UNSAT certificate proves.** If the DIMACS file of `gen_etv.py N A U K`
(`K ≥ 4`) is unsatisfiable, then every set of `N` points in general position with distinct
x-coordinates contains an `A`-cap, a `U`-cup or a convex `K`-gon. -/
theorem cap_cup_or_gon_of_unsat {N A U K : ℕ} (hunsat : ¬DimacsSatisfiable (dimacs N A U K))
    (hK : 4 ≤ K) (S : Finset Point) (hgp : GeneralPosition S) (hS : LowerBound.DistinctX S)
    (hN : S.card = N) : HasChainPts (-1) A S ∨ HasChainPts 1 U S ∨ HasConvexNGon K S := by
  by_contra h
  simp only [not_or] at h
  subst hN
  exact hunsat (dimacsSatisfiable_of_pointSet hK S hgp hS h.1 h.2.1 h.2.2)

/-! ### The diagonal case `A = U = K`: caps and cups are gons -/

theorem Chain.ends {σ : Sig} {t : Bool} {l : List ℕ} (h : Chain σ t l) (hl : 2 ≤ l.length) :
    ∃ x y, x < y ∧ l.head? = some x ∧ l.getLast? = some y ∧ x ∈ l ∧ y ∈ l := by
  match l, h, hl with
  | [], _, hl => simp at hl
  | [_], _, hl => simp at hl
  | x :: z :: rest, h, _ =>
    obtain ⟨w, hw⟩ : ∃ w, (z :: rest).getLast? = some w :=
      ⟨_, List.getLast?_eq_getLast (by simp)⟩
    have hwm : w ∈ z :: rest := List.mem_of_getLast? hw
    exact ⟨x, w, Chain.head_lt h w hwm, rfl, by rw [List.getLast?_cons_cons]; exact hw,
      by simp, List.mem_cons_of_mem _ hwm⟩

/-- A `K`-cap is a `K`-gon (with the two-point cup joining its ends). -/
theorem hasGon_of_hasCap {σ : Sig} {N K : ℕ} (hK : 2 ≤ K) (h : HasCap σ N K) :
    HasGon σ N K := by
  obtain ⟨l, hlen, hlN, hc⟩ := h
  obtain ⟨x, y, hxy, hx, hy, hxl, hyl⟩ := hc.ends (by omega)
  refine ⟨l, [x, y], hc, hxy, by omega, by simp, by simp [hx], by simp [hy], by simp; omega,
    hlN, ?_⟩
  intro p hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl
  · exact hlN _ hxl
  · exact hlN _ hyl

/-- A `K`-cup is a `K`-gon (with the two-point cap joining its ends). -/
theorem hasGon_of_hasCup {σ : Sig} {N K : ℕ} (hK : 2 ≤ K) (h : HasCup σ N K) :
    HasGon σ N K := by
  obtain ⟨l, hlen, hlN, hc⟩ := h
  obtain ⟨x, y, hxy, hx, hy, hxl, hyl⟩ := hc.ends (by omega)
  refine ⟨[x, y], l, hxy, hc, by simp, by omega, by simp [hx], by simp [hy], by simp; omega,
    ?_, hlN⟩
  intro p hp
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
  rcases hp with rfl | rfl
  · exact hlN _ hxl
  · exact hlN _ hyl

/-- **The ES case.** If the DIMACS file of `gen_etv.py N K K K` (`K ≥ 4`) is unsatisfiable,
then every set of `N` points in general position with distinct x-coordinates contains a convex
`K`-gon. For example, UNSAT of `gen_etv.py 33 7 7 7` would give the heptagon statement for
point sets with distinct x-coordinates. -/
theorem hasConvexNGon_of_unsat {N K : ℕ} (hunsat : ¬DimacsSatisfiable (dimacs N K K K))
    (hK : 4 ≤ K) (S : Finset Point) (hgp : GeneralPosition S) (hS : LowerBound.DistinctX S)
    (hN : S.card = N) : HasConvexNGon K S := by
  obtain ⟨P, hx, hP⟩ := exists_xsorted S hS
  subst hN
  have hgp' : GeneralPosition (ptSet P S.card) := by rw [hP]; exact hgp
  have hgon : HasGon (sigOf P) S.card K := by
    rcases signotope_of_unsat hunsat (isSignotope_sigOf hx) with h | h | h
    · exact hasGon_of_hasCap (by omega) h
    · exact hasGon_of_hasCup (by omega) h
    · exact h
  rw [← hP]
  exact hasConvexNGon_of_hasGon hx hgp' hK hgon

end ETV
