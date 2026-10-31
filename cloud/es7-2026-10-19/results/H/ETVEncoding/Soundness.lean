import ETVEncoding.Clauses
import ETVEncoding.Signotope

/-!
# Soundness of the ETV clauses

Every clause of `etvClauses N A U K` holds under the assignment `assn σ` induced by a
signotope `σ` on `N` points with no `A`-cap, no `U`-cup and no `K`-gon. The auxiliary
variables get their intended meaning (`ChainEnd`, `ChainE`), so this is the statement "the
encoding is sound" at the level of structured variables.
-/

namespace ETV

open Lit

/-- The assignment induced by a signotope: orientations, and the chain variables read as
"such a chain exists". -/
def assn (σ : Sig) : Var → Prop
  | .x i j k => σ i j k = true
  | .v t x a b r => ChainEnd σ t x a b r
  | .e t x b r => ChainE σ t x b r

/-- A literal holds under a `Prop`-valued assignment. -/
def Lit.Holds (τ : Var → Prop) (l : Lit) : Prop := if l.pos then τ l.var else ¬τ l.var

/-- A clause holds when one of its literals does. -/
def ClauseHolds (τ : Var → Prop) (c : Clause) : Prop := ∃ l ∈ c, l.Holds τ

variable {σ : Sig} {N : ℕ}

@[simp] theorem holds_pos' {τ : Var → Prop} {v : Var} : (pos' v).Holds τ ↔ τ v := by
  simp [Lit.Holds, pos']

@[simp] theorem holds_neg' {τ : Var → Prop} {v : Var} : (neg' v).Holds τ ↔ ¬τ v := by
  simp [Lit.Holds, neg']

@[simp] theorem holds_tlit {t : Bool} {i j k : ℕ} :
    (tlit t i j k).Holds (assn σ) ↔ σ i j k = t := by
  cases t <;> simp [Lit.Holds, tlit, assn]

@[simp] theorem holds_ntlit {t : Bool} {i j k : ℕ} :
    (ntlit t i j k).Holds (assn σ) ↔ σ i j k ≠ t := by
  cases t <;> simp [Lit.Holds, ntlit, assn]

@[simp] theorem clauseHolds_cons {τ : Var → Prop} {l : Lit} {c : Clause} :
    ClauseHolds τ (l :: c) ↔ l.Holds τ ∨ ClauseHolds τ c := by
  simp [ClauseHolds]

@[simp] theorem clauseHolds_nil {τ : Var → Prop} : ¬ClauseHolds τ [] := by
  simp [ClauseHolds]

/-! ### Membership in the index lists -/

@[simp] theorem mem_pairs {x b : ℕ} : (x, b) ∈ pairs N ↔ x < b ∧ b < N := by
  simp only [pairs, List.mem_flatMap, List.mem_range, List.mem_map, List.mem_range'_1,
    Prod.mk.injEq]
  constructor
  · rintro ⟨x', hx', b', ⟨hb1, hb2⟩, rfl, rfl⟩
    omega
  · rintro ⟨h1, h2⟩
    refine ⟨x, ?_, b, ⟨?_, ?_⟩, rfl, rfl⟩ <;> omega

@[simp] theorem mem_triples {i j k : ℕ} :
    (i, j, k) ∈ triples N ↔ i < j ∧ j < k ∧ k < N := by
  simp only [triples, List.mem_flatMap, List.mem_range, List.mem_map, List.mem_range'_1,
    Prod.mk.injEq]
  constructor
  · rintro ⟨i', hi', j', ⟨hj1, hj2⟩, k', ⟨hk1, hk2⟩, rfl, rfl, rfl⟩
    omega
  · rintro ⟨h1, h2, h3⟩
    refine ⟨i, ?_, j, ⟨?_, ?_⟩, k, ⟨?_, ?_⟩, rfl, rfl, rfl⟩ <;> omega

@[simp] theorem mem_quads {i j k l : ℕ} :
    (i, j, k, l) ∈ quads N ↔ i < j ∧ j < k ∧ k < l ∧ l < N := by
  simp only [quads, List.mem_flatMap, List.mem_range, List.mem_map, List.mem_range'_1,
    Prod.mk.injEq]
  constructor
  · rintro ⟨i', hi', j', ⟨hj1, hj2⟩, k', ⟨hk1, hk2⟩, l', ⟨hl1, hl2⟩, rfl, rfl, rfl, rfl⟩
    omega
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨i, ?_, j, ⟨?_, ?_⟩, k, ⟨?_, ?_⟩, l, ⟨?_, ?_⟩, rfl, rfl, rfl, rfl⟩ <;> omega

@[simp] theorem mem_vKeys {B x a b r : ℕ} :
    (x, a, b, r) ∈ vKeys B N ↔
      (x < a ∧ a < b ∧ b < N) ∧ 3 ≤ r ∧ r < B ∧ r ≤ a - x + 2 := by
  simp only [vKeys, List.mem_flatMap, List.mem_filterMap, List.mem_range'_1, Prod.exists,
    mem_triples]
  constructor
  · rintro ⟨x', a', b', hxab, r', ⟨hr1, hr2⟩, h⟩
    split_ifs at h with hc
    simp only [Option.some.injEq, Prod.mk.injEq] at h
    obtain ⟨rfl, rfl, rfl, rfl⟩ := h
    exact ⟨hxab, by omega, by omega, hc⟩
  · rintro ⟨hxab, h3, hB, hc⟩
    exact ⟨x, a, b, hxab, r, ⟨by omega, by omega⟩, by simp [hc]⟩

@[simp] theorem mem_eKeys {B x b r : ℕ} :
    (x, b, r) ∈ eKeys B N ↔ (x < b ∧ b < N) ∧ 3 ≤ r ∧ r < B ∧ r ≤ b - x + 1 := by
  simp only [eKeys, List.mem_flatMap, List.mem_filterMap, List.mem_range'_1, Prod.exists,
    mem_pairs]
  constructor
  · rintro ⟨x', b', hxb, r', ⟨hr1, hr2⟩, h⟩
    split_ifs at h with hc
    simp only [Option.some.injEq, Prod.mk.injEq] at h
    obtain ⟨rfl, rfl, rfl⟩ := h
    exact ⟨hxb, by omega, by omega, hc⟩
  · rintro ⟨hxb, h3, hB, hc⟩
    exact ⟨x, b, hxb, r, ⟨by omega, by omega⟩, by simp [hc]⟩

/-! ### The signotope clauses -/

theorem signotopeClauses_sound (hσ : IsSignotope N σ) :
    ∀ c ∈ signotopeClauses N, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [signotopeClauses, List.mem_flatMap, Prod.exists, mem_quads] at hc
  obtain ⟨i, j, k, l, ⟨hij, hjk, hkl, hl⟩, hc⟩ := hc
  have hp := pv_no_alt (hσ i j k l hij hjk hkl hl)
  simp only [sig4, tri3, List.cons_append, List.nil_append, List.mem_cons,
    List.not_mem_nil, or_false] at hc
  generalize hA : σ i j k = A at hp
  generalize hB : σ i j l = B at hp
  generalize hC : σ i k l = C at hp
  generalize hD : σ j k l = D at hp
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp only [clauseHolds_cons, holds_pos', holds_neg', clauseHolds_nil, or_false, assn,
      hA, hB, hC, hD] <;>
    revert hp <;> cases A <;> cases B <;> cases C <;> cases D <;> decide

/-! ### The cap and cup clauses -/

theorem hasChain_of_triple {t : Bool} {B x a b : ℕ} (hB : B ≤ 3) (hxa : x < a) (hab : a < b)
    (hb : b < N) (h : σ x a b = t) : HasChain σ N t B := by
  have hall : ∀ p ∈ [x, a, b], p < N := by
    intro p hp
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hp
    omega
  interval_cases B
  · exact ⟨[], rfl, by simp, trivial⟩
  · exact ⟨[x], rfl, by simp; omega, trivial⟩
  · exact ⟨[x, a], rfl, by simp; omega, hxa⟩
  · exact ⟨[x, a, b], rfl, hall, ⟨hxa, h, hab⟩⟩

theorem baseClauses_sound {t : Bool} {B : ℕ} (hB : ¬HasChain σ N t B) :
    ∀ c ∈ baseClauses t B N, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [baseClauses, List.mem_map, Prod.exists, mem_triples] at hc
  obtain ⟨x, a, b, ⟨hxa, hab, hb⟩, rfl⟩ := hc
  split_ifs with h3
  · by_cases h : σ x a b = t
    · simp only [clauseHolds_cons, holds_ntlit, holds_pos', clauseHolds_nil, or_false]
      exact Or.inr ⟨hxa, hab, h⟩
    · simp [h]
  · simp only [clauseHolds_cons, holds_ntlit, clauseHolds_nil, or_false]
    intro h
    exact hB (hasChain_of_triple (by omega) hxa hab hb h)

theorem extClauses_sound {t : Bool} {B : ℕ}
    (hB : ¬HasChain σ N t B) : ∀ c ∈ extClauses t B N, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [extClauses, List.mem_flatMap, Prod.exists, mem_quads, List.mem_filterMap,
    List.mem_range'_1] at hc
  obtain ⟨x, w, a, b, ⟨hxw, hwa, hab, hb⟩, r, ⟨hr4, hrB⟩, hc⟩ := hc
  split_ifs at hc with hkey hlt
  · simp only [Option.some.injEq] at hc
    subst hc
    obtain ⟨n, rfl⟩ : ∃ n, r = n + 4 := ⟨r - 4, by omega⟩
    simp only [clauseHolds_cons, holds_neg', holds_ntlit, holds_pos', clauseHolds_nil,
      or_false, assn, show n + 4 - 1 = n + 3 by omega]
    by_cases hV : ChainEnd σ t x w a (n + 3)
    · by_cases h : σ w a b = t
      · exact Or.inr (Or.inr ⟨hab, w, hV, h⟩)
      · exact Or.inr (Or.inl h)
    · exact Or.inl hV
  · simp only [Option.some.injEq] at hc
    subst hc
    obtain ⟨n, rfl⟩ : ∃ n, r = n + 4 := ⟨r - 4, by omega⟩
    simp only [clauseHolds_cons, holds_neg', holds_ntlit, clauseHolds_nil, or_false, assn,
      show n + 4 - 1 = n + 3 by omega]
    by_cases hV : ChainEnd σ t x w a (n + 3)
    · by_cases h : σ w a b = t
      · exfalso
        have hr : n + 4 = B := by omega
        exact hB (hr ▸ (show ChainEnd σ t x a b (n + 4) from ⟨hab, w, hV, h⟩).hasChain hb)
      · exact Or.inr h
    · exact Or.inl hV

theorem vClauses_sound (hσ : IsSignotope N σ) {t : Bool} {B : ℕ} :
    ∀ c ∈ vClauses t B N, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [vClauses, List.mem_flatMap, Prod.exists, mem_vKeys, List.mem_cons] at hc
  obtain ⟨x, a, b, r, ⟨⟨hxa, hab, hb⟩, h3, hrB, hkey⟩, hc⟩ := hc
  rcases hc with rfl | hc
  · simp only [clauseHolds_cons, holds_neg', holds_pos', clauseHolds_nil, or_false, assn]
    by_cases hV : ChainEnd σ t x a b r
    · exact Or.inr ⟨a, hV⟩
    · exact Or.inl hV
  · split_ifs at hc with h4
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
      subst hc
      simp only [clauseHolds_cons, holds_neg', holds_pos', clauseHolds_nil, or_false, assn]
      by_cases hV : ChainEnd σ t x a b r
      · obtain ⟨n, rfl⟩ : ∃ n, r = n + 1 := ⟨r - 1, by omega⟩
        exact Or.inr (by simpa using ChainEnd.pred hσ (by omega) hb hV)
      · exact Or.inl hV
    · simp at hc

theorem eClauses_sound (hσ : IsSignotope N σ) {t : Bool} {B : ℕ} :
    ∀ c ∈ eClauses t B N, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [eClauses, List.mem_filterMap, Prod.exists, mem_eKeys] at hc
  obtain ⟨x, b, r, ⟨⟨hxb, hb⟩, h3, hrB, hkey⟩, hc⟩ := hc
  split_ifs at hc with h4
  simp only [Option.some.injEq] at hc
  subst hc
  simp only [clauseHolds_cons, holds_neg', holds_pos', clauseHolds_nil, or_false, assn]
  by_cases hE : ChainE σ t x b r
  · obtain ⟨n, rfl⟩ : ∃ n, r = n + 1 := ⟨r - 1, by omega⟩
    exact Or.inr (by simpa using ChainE.pred hσ (by omega) hb hE)
  · exact Or.inl hE

theorem chainClauses_sound (hσ : IsSignotope N σ) {t : Bool} {B : ℕ}
    (hB : ¬HasChain σ N t B) : ∀ c ∈ chainClauses t B N, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [chainClauses, List.mem_append] at hc
  rcases hc with ((hc | hc) | hc) | hc
  · exact baseClauses_sound hB c hc
  · exact extClauses_sound hB c hc
  · exact vClauses_sound hσ c hc
  · exact eClauses_sound hσ c hc

/-! ### The gon clauses -/

theorem gonClauses_sound {A U K : ℕ} (hK : ¬HasGon σ N K) :
    ∀ c ∈ gonClauses N A U K, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [gonClauses, List.mem_flatMap, Prod.exists, mem_pairs, List.mem_filterMap,
    List.mem_range'_1] at hc
  obtain ⟨x, b, ⟨hxb, hb⟩, r, ⟨hr3, hrA⟩, hc⟩ := hc
  split_ifs at hc with hcond
  simp only [Option.some.injEq] at hc
  subst hc
  simp only [clauseHolds_cons, holds_neg', clauseHolds_nil, or_false, assn]
  by_cases h1 : ChainE σ false x b r
  · by_cases h2 : ChainE σ true x b (K + 2 - r)
    · exact (hK (hasGon_of_chainE h1 h2 hb (by omega))).elim
    · exact Or.inr h2
  · exact Or.inl h1

/-! ### The whole encoding -/

/-- **Soundness of the ETV encoding (structured variables).** For a signotope on `N` points
with no `A`-cap, no `U`-cup and no `K`-gon, every clause of `gen_etv.py N A U K` holds under
the induced assignment. -/
theorem etvClauses_sound {A U K : ℕ} (hσ : IsSignotope N σ) (hA : ¬HasCap σ N A)
    (hU : ¬HasCup σ N U) (hK : ¬HasGon σ N K) :
    ∀ c ∈ etvClauses N A U K, ClauseHolds (assn σ) c := by
  intro c hc
  simp only [etvClauses, List.mem_append] at hc
  rcases hc with ((hc | hc) | hc) | hc
  · exact signotopeClauses_sound hσ c hc
  · exact chainClauses_sound hσ hA c hc
  · exact chainClauses_sound hσ hU c hc
  · exact gonClauses_sound hK c hc

end ETV
