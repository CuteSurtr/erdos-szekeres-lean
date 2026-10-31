import ETVEncoding.Gon
import ETVEncoding.Dimacs
import ErdosSzekeres.OrientationConvexity
import ErdosSzekeres.Suk.FourPoint
import ErdosSzekeres.LowerBound.Defs

/-!
# From planar point sets to signotopes

Points `P 0, …, P (N-1)` with strictly increasing x-coordinates and no three collinear give
the signotope `sigOf P` (`σ i j k = decide (0 < orient (P i) (P j) (P k))`). We prove:

* `sigOf P` satisfies the 4-point axiom (`isSignotope_sigOf`, from the repository's
  `packetValid_of_xordered`);
* an `m`-chain of `sigOf P` is an `m`-point cap or cup of the point set in the geometric sense
  of `LowerBound.IsChain` (all x-increasing triples have the same orientation);
* a `K`-gon of `sigOf P` (`K ≥ 4`) is a convex `K`-gon of the point set
  (`HasConvexNGon`, i.e. `ConvexIndependent`);

and hence that the DIMACS clauses are satisfiable for every point set with no `A`-cap, no
`U`-cup and no convex `K`-gon.
-/

namespace ETV

open ErdosSzekeres

/-- `P 0, …, P (N-1)` have strictly increasing x-coordinates. -/
def XSorted (P : ℕ → Point) (N : ℕ) : Prop := ∀ i j, i < j → j < N → P i 0 < P j 0

/-- The point set `{P 0, …, P (N-1)}`. -/
noncomputable def ptSet (P : ℕ → Point) (N : ℕ) : Finset Point := (Finset.range N).image P

/-- The signotope of an x-sorted point sequence: `true` = counterclockwise. -/
noncomputable def sigOf (P : ℕ → Point) : Sig := fun i j k => decide (0 < orient (P i) (P j) (P k))

/-- `S` contains `m` points forming a chain of sign `s`: an `m`-cap for `s = -1`, an `m`-cup
for `s = 1` (all x-increasing triples have orientation of sign `s`). -/
def HasChainPts (s : ℝ) (m : ℕ) (S : Finset Point) : Prop :=
  ∃ T ⊆ S, T.card = m ∧ LowerBound.IsChain s T

variable {P : ℕ → Point} {N : ℕ}

theorem XSorted.lt_of_lt (hx : XSorted P N) {i j : ℕ} (hi : i < N) (_hj : j < N)
    (h : P i 0 < P j 0) : i < j := by
  by_contra hij
  rcases eq_or_lt_of_le (not_lt.1 hij) with e | e
  · subst e
    exact lt_irrefl _ h
  · exact lt_asymm h (hx j i e hi)

theorem XSorted.injOn (hx : XSorted P N) : Set.InjOn P ↑(Finset.range N) := by
  intro i hi j hj hij
  simp only [Finset.coe_range, Set.mem_Iio] at hi hj
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · have := hx i j h hj
    rw [hij] at this
    exact lt_irrefl _ this
  · have := hx j i h hi
    rw [hij] at this
    exact lt_irrefl _ this

theorem mem_ptSet {i : ℕ} (hi : i < N) : P i ∈ ptSet P N :=
  Finset.mem_image_of_mem P (Finset.mem_range.2 hi)

/-- The 4-point axiom holds for x-sorted points. -/
theorem isSignotope_sigOf (hx : XSorted P N) : IsSignotope N (sigOf P) :=
  fun i j k l hij hjk hkl hl =>
    packetValid_of_xordered _ _ _ _ (hx i j hij (by omega)) (hx j k hjk (by omega))
      (hx k l hkl hl)

theorem orient_ne_zero_of_gp (hx : XSorted P N) (hgp : GeneralPosition (ptSet P N))
    {i j k : ℕ} (hij : i < j) (hjk : j < k) (hk : k < N) :
    orient (P i) (P j) (P k) ≠ 0 := by
  have hi : i < N := by omega
  have hj : j < N := by omega
  refine (generalPosition_iff_orient_ne_zero _).1 hgp _ (mem_ptSet hi) _ (mem_ptSet hj) _
    (mem_ptSet hk) ?_ ?_ ?_
  · intro e
    have := hx i j hij hj
    rw [e] at this
    exact lt_irrefl _ this
  · intro e
    have := hx i k (by omega) hk
    rw [e] at this
    exact lt_irrefl _ this
  · intro e
    have := hx j k hjk hk
    rw [e] at this
    exact lt_irrefl _ this

/-- A chain of the signotope is a cap (`t = false`) or cup (`t = true`) of the points. -/
theorem hasChainPts_of_hasChain (hx : XSorted P N) (hgp : GeneralPosition (ptSet P N))
    {t : Bool} {m : ℕ} (h : HasChain (sigOf P) N t m) :
    HasChainPts (if t then 1 else -1) m (ptSet P N) := by
  classical
  obtain ⟨l, hlen, hlN, hc⟩ := h
  have hA := hc.allTriples (isSignotope_sigOf hx) hlN
  have hnd : l.Nodup := hc.pairwise.imp (fun h => ne_of_lt h)
  have hinj : Set.InjOn P ↑l.toFinset := by
    intro i hi j hj hij
    simp only [Finset.mem_coe, List.mem_toFinset] at hi hj
    exact hx.injOn (by simpa using hlN i hi) (by simpa using hlN j hj) hij
  refine ⟨l.toFinset.image P, ?_, ?_, ?_⟩
  · intro p hp
    simp only [Finset.mem_image, List.mem_toFinset] at hp
    obtain ⟨i, hi, rfl⟩ := hp
    exact mem_ptSet (hlN i hi)
  · rw [Finset.card_image_of_injOn hinj, List.toFinset_card_of_nodup hnd, hlen]
  · intro a ha b hb c hc' hab hbc
    simp only [Finset.mem_image, List.mem_toFinset] at ha hb hc'
    obtain ⟨i, hi, rfl⟩ := ha
    obtain ⟨j, hj, rfl⟩ := hb
    obtain ⟨k, hk, rfl⟩ := hc'
    have hij := hx.lt_of_lt (hlN i hi) (hlN j hj) hab
    have hjk := hx.lt_of_lt (hlN j hj) (hlN k hk) hbc
    have hs := hA i hi j hj k hk hij hjk
    have hne := orient_ne_zero_of_gp hx hgp hij hjk (hlN k hk)
    simp only [sigOf] at hs
    cases t
    · simp only [decide_eq_false_iff_not, not_lt] at hs
      simp only [Bool.false_eq_true, if_false]
      have : orient (P i) (P j) (P k) < 0 := lt_of_le_of_ne hs hne
      linarith
    · simp only [decide_eq_true_eq] at hs
      simp only [if_true, one_mul]
      exact hs

/-- A `K`-gon of the signotope (`K ≥ 4`) is a convex `K`-gon of the points. -/
theorem hasConvexNGon_of_hasGon (hx : XSorted P N) (hgp : GeneralPosition (ptSet P N))
    {K : ℕ} (hK : 4 ≤ K) (h : HasGon (sigOf P) N K) : HasConvexNGon K (ptSet P N) := by
  classical
  obtain ⟨G, hcard, hGN, hquad⟩ := h.vertices (isSignotope_sigOf hx)
  have hinj : Set.InjOn P ↑G := by
    intro i hi j hj hij
    exact hx.injOn (by simpa using hGN i hi) (by simpa using hGN j hj) hij
  refine ⟨G.image P, ?_, ?_, ?_⟩
  · intro p hp
    simp only [Finset.mem_image] at hp
    obtain ⟨i, hi, rfl⟩ := hp
    exact mem_ptSet (hGN i hi)
  · rw [Finset.card_image_of_injOn hinj, hcard]
  · apply Suk.convexPosition_of_four_subsets (by rw [Finset.card_image_of_injOn hinj]; omega)
    intro T hT hT4
    obtain ⟨U, hUG, rfl⟩ := Finset.subset_image_iff.1 hT
    have hU4 : U.card = 4 := by
      rw [Finset.card_image_of_injOn (hinj.mono (by simpa using hUG))] at hT4
      exact hT4
    let e := U.orderEmbOfFin hU4
    have hem (i : Fin 4) : e i ∈ G := hUG (Finset.orderEmbOfFin_mem U hU4 i)
    have hT' : U.image P = {P (e 0), P (e 1), P (e 2), P (e 3)} := by
      rw [← Finset.image_orderEmbOfFin_univ U hU4, Finset.image_image]
      have hf : (Finset.univ : Finset (Fin 4)) = {0, 1, 2, 3} := by decide
      rw [hf]
      simp [e]
    rw [hT']
    have h01 : e 0 < e 1 := e.strictMono (by decide)
    have h12 : e 1 < e 2 := e.strictMono (by decide)
    have h23 : e 2 < e 3 := e.strictMono (by decide)
    have h3N : e 3 < N := hGN _ (hem 3)
    rw [convexPosition_four_iff_signs _ _ _ _
      (orient_ne_zero_of_gp hx hgp h01 h12 (by omega))
      (orient_ne_zero_of_gp hx hgp h01 (lt_trans h12 h23) h3N)
      (orient_ne_zero_of_gp hx hgp (lt_trans h01 h12) h23 h3N)
      (orient_ne_zero_of_gp hx hgp h12 h23 h3N)]
    left
    exact hquad _ (hem 0) _ (hem 1) _ (hem 2) _ (hem 3) h01 h12 h23

/-- **Soundness for x-sorted point sets.** If `P 0, …, P (N-1)` are x-sorted points in
general position with no `A`-cap, no `U`-cup and no convex `K`-gon (`K ≥ 4`), then the
DIMACS clauses of `gen_etv.py N A U K` are satisfiable. -/
theorem dimacsSatisfiable_of_xsorted (hx : XSorted P N) (hgp : GeneralPosition (ptSet P N))
    {A U K : ℕ} (hK : 4 ≤ K) (hA : ¬HasChainPts (-1) A (ptSet P N))
    (hU : ¬HasChainPts 1 U (ptSet P N)) (hgon : ¬HasConvexNGon K (ptSet P N)) :
    DimacsSatisfiable (dimacs N A U K) :=
  dimacsSatisfiable_of_signotope (isSignotope_sigOf hx)
    (fun h => hA (by simpa using hasChainPts_of_hasChain hx hgp h))
    (fun h => hU (by simpa using hasChainPts_of_hasChain hx hgp h))
    (fun h => hgon (hasConvexNGon_of_hasGon hx hgp hK h))

end ETV
