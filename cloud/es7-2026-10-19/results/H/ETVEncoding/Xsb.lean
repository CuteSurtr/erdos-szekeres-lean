import ETVEncoding.Dimacs
import ETVEncoding.Targets

/-!
# Soundness of the x-reflection lex-leader clause (`gen_etv.py --xsb`)

The mirror `σ' i j k = σ (N-1-k) (N-1-j) (N-1-i)` of a signotope is a signotope, and a cap,
cup or gon of `σ'` reflects to one of `σ`. If `σ` violates `-X(0,1,2) ∨ X(N-3,N-2,N-1)`, then
`σ'` satisfies it, so one of the two gives a model of `dimacsXsb`.
-/

namespace ETV

open Lit
open ErdosSzekeres (PacketValid)

/-- The x-mirror of `σ` on the points `0, …, N-1`. -/
def mirror (N : ℕ) (σ : Sig) : Sig := fun i j k => σ (N - 1 - k) (N - 1 - j) (N - 1 - i)

theorem pv_reverse {a b c d : Bool} (h : PacketValid a b c d) : PacketValid d c b a := by
  revert h; cases a <;> cases b <;> cases c <;> cases d <;> decide

variable {σ : Sig} {N : ℕ}

theorem isSignotope_mirror (hσ : IsSignotope N σ) : IsSignotope N (mirror N σ) := by
  intro i j k l hij hjk hkl hl
  exact pv_reverse (hσ (N - 1 - l) (N - 1 - k) (N - 1 - j) (N - 1 - i) (by omega) (by omega)
    (by omega) (by omega))

theorem chain_of_allTriples {t : Bool} :
    ∀ {l : List ℕ}, l.Pairwise (· < ·) → AllTriples σ t l → Chain σ t l
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | [a, b], hs, _ => by
      simp only [List.pairwise_cons, List.mem_singleton, forall_eq, List.not_mem_nil,
        IsEmpty.forall_iff, implies_true, List.Pairwise.nil, and_true] at hs
      exact hs
  | a :: b :: c :: l, hs, hA => by
      have hab : a < b := (List.pairwise_cons.1 hs).1 b (by simp)
      have hbc : b < c := (List.pairwise_cons.1 (List.pairwise_cons.1 hs).2).1 c (by simp)
      refine ⟨hab, hA a (by simp) b (by simp) c (by simp) hab hbc,
        chain_of_allTriples (List.pairwise_cons.1 hs).2 ?_⟩
      intro p hp q hq r hr
      exact hA p (List.mem_cons_of_mem _ hp) q (List.mem_cons_of_mem _ hq) r
        (List.mem_cons_of_mem _ hr)

/-- The reflected list. -/
def mlist (N : ℕ) (l : List ℕ) : List ℕ := (l.map (fun p => N - 1 - p)).reverse

theorem mem_mlist {l : List ℕ} {q : ℕ} : q ∈ mlist N l ↔ ∃ p ∈ l, N - 1 - p = q := by
  simp [mlist]

theorem mlist_bound {l : List ℕ} (hlN : ∀ p ∈ l, p < N) : ∀ q ∈ mlist N l, q < N := by
  intro q hq
  obtain ⟨p, hp, rfl⟩ := mem_mlist.1 hq
  have := hlN p hp
  omega

/-- A chain of the mirror reflects to a chain of `σ`. -/
theorem chain_mlist (hσ : IsSignotope N σ) {t : Bool} {l : List ℕ}
    (hc : Chain (mirror N σ) t l) (hlN : ∀ p ∈ l, p < N) : Chain σ t (mlist N l) := by
  have hs := hc.pairwise
  have hA := hc.allTriples (isSignotope_mirror hσ) hlN
  apply chain_of_allTriples
  · simp only [mlist, List.pairwise_reverse, List.pairwise_map]
    exact hs.imp_of_mem (fun {a b} ha hb hab => by
      have := hlN a ha
      have := hlN b hb
      omega)
  · intro p hp q hq r hr hpq hqr
    obtain ⟨p', hp', rfl⟩ := mem_mlist.1 hp
    obtain ⟨q', hq', rfl⟩ := mem_mlist.1 hq
    obtain ⟨r', hr', rfl⟩ := mem_mlist.1 hr
    have h1 := hlN p' hp'
    have h2 := hlN q' hq'
    have h3 := hlN r' hr'
    have := hA r' hr' q' hq' p' hp' (by omega) (by omega)
    simp only [mirror] at this
    exact this

theorem hasChain_of_mirror (hσ : IsSignotope N σ) {t : Bool} {m : ℕ}
    (h : HasChain (mirror N σ) N t m) : HasChain σ N t m := by
  obtain ⟨l, hlen, hlN, hc⟩ := h
  exact ⟨mlist N l, by simp [mlist, hlen], mlist_bound hlN, chain_mlist hσ hc hlN⟩

theorem hasGon_of_mirror (hσ : IsSignotope N σ) {K : ℕ} (h : HasGon (mirror N σ) N K) :
    HasGon σ N K := by
  obtain ⟨l₁, l₂, h1, h2, hl1, hl2, hhead, hlast, hK, hN1, hN2⟩ := h
  refine ⟨mlist N l₁, mlist N l₂, chain_mlist hσ h1 hN1, chain_mlist hσ h2 hN2,
    by simpa [mlist] using hl1, by simpa [mlist] using hl2, ?_, ?_, by simp [mlist]; omega,
    mlist_bound hN1, mlist_bound hN2⟩
  · simp only [mlist, List.head?_reverse, List.getLast?_map, hlast]
  · simp only [mlist, List.getLast?_reverse, List.head?_map, hhead]

/-- **`--xsb` is sound.** -/
theorem xsbSound : XsbSound := by
  intro N A U K σ hN hσ hA hU hK
  have hx0 : Var.x 0 1 2 ∈ allVars N A U := mem_allVars_x.2 ⟨by omega, by omega, by omega⟩
  have hx1 : Var.x (N - 3) (N - 2) (N - 1) ∈ allVars N A U :=
    mem_allVars_x.2 ⟨by omega, by omega, by omega⟩
  -- any signotope satisfying the clause gives a model of `dimacsXsb`
  have key : ∀ ρ : Sig, IsSignotope N ρ → ¬HasCap ρ N A → ¬HasCup ρ N U → ¬HasGon ρ N K →
      (ρ 0 1 2 = true → ρ (N - 3) (N - 2) (N - 1) = true) →
      DimacsSatisfiable (dimacsXsb N A U K) := by
    intro ρ hρ hρA hρU hρK hcl
    have base := dimacsSat_of_holds (etvClauses_sound hρ hρA hρU hρK)
    refine ⟨nuOf N A U (assn ρ), ?_⟩
    intro c hc
    simp only [dimacsXsb, List.mem_append, List.mem_singleton] at hc
    rcases hc with hc | rfl
    · exact base c hc
    · have e0 := nuOf_num (τ := assn ρ) hx0
      have e1 := nuOf_num (τ := assn ρ) hx1
      have n0 := numberMap_getD hx0
      have n1 := numberMap_getD hx1
      simp only [assn] at e0 e1
      by_cases h0 : ρ 0 1 2 = true
      · refine ⟨_, List.mem_cons_of_mem _ (List.mem_singleton_self _), Or.inl ⟨by omega, ?_⟩⟩
        rw [Int.natAbs_natCast]
        exact e1.2 (hcl h0)
      · refine ⟨_, List.mem_cons_self, Or.inr ⟨by omega, ?_⟩⟩
        rw [Int.natAbs_neg, Int.natAbs_natCast]
        cases hv : nuOf N A U (assn ρ) ((numberMap (allVars N A U)).getD (Var.x 0 1 2) 0)
        · rfl
        · exact absurd (e0.1 hv) h0
  by_cases hc : σ 0 1 2 = true → σ (N - 3) (N - 2) (N - 1) = true
  · exact key σ hσ hA hU hK hc
  · refine key (mirror N σ) (isSignotope_mirror hσ) (fun h => hA (hasChain_of_mirror hσ h))
      (fun h => hU (hasChain_of_mirror hσ h)) (fun h => hK (hasGon_of_mirror hσ h)) ?_
    intro h
    exfalso
    apply hc
    intro _
    simp only [mirror] at h
    rwa [show N - 1 - 2 = N - 3 by omega, show N - 1 - 1 = N - 2 by omega,
      show N - 1 - 0 = N - 1 by omega] at h

/-- **What an UNSAT certificate for `gen_etv.py N A U K --xsb` proves** (`N ≥ 3`, `K ≥ 4`):
every `N`-point set in general position with distinct x-coordinates has an `A`-cap, a
`U`-cup or a convex `K`-gon. -/
theorem cap_cup_or_gon_of_unsat_xsb {N A U K : ℕ}
    (hunsat : ¬DimacsSatisfiable (dimacsXsb N A U K)) (hK : 4 ≤ K) (hN3 : 3 ≤ N)
    (S : Finset ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S)
    (hS : ErdosSzekeres.LowerBound.DistinctX S) (hN : S.card = N) :
    HasChainPts (-1) A S ∨ HasChainPts 1 U S ∨ ErdosSzekeres.HasConvexNGon K S := by
  obtain ⟨P, hx, hP⟩ := exists_xsorted S hS
  subst hN
  have hgp' : ErdosSzekeres.GeneralPosition (ptSet P S.card) := by rw [hP]; exact hgp
  by_contra h
  simp only [not_or] at h
  apply hunsat
  refine xsbSound S.card A U K (sigOf P) hN3 (isSignotope_sigOf hx) ?_ ?_ ?_
  · intro hc
    apply h.1
    rw [← hP]
    simpa using hasChainPts_of_hasChain hx hgp' hc
  · intro hc
    apply h.2.1
    rw [← hP]
    simpa using hasChainPts_of_hasChain hx hgp' hc
  · intro hc
    apply h.2.2
    rw [← hP]
    exact hasConvexNGon_of_hasGon hx hgp' hK hc

end ETV
