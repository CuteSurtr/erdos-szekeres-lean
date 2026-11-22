import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Nat.Lattice

/-!
# V182Geo.Defs: the 182-vertex omission-layer graph and rainbow-C4 edge colourings (DESIGN.md §1.1)

* `V`: the subsets of `{0, …, 7}` with 3, 4 or 5 elements (56 + 70 + 56 = 182).
* `G`: `u ~ v` iff one contains the other and the sizes differ by one (inclusions between consecutive sizes only;
  560 edges).
* `IsFourCycle a b c d`: four distinct, cyclically adjacent vertices (a 4-cycle subgraph; chords are allowed by the
  definition).
* `IsRainbow col` for an edge colouring `col : G.edgeSet → α` (not necessarily proper): every 4-cycle subgraph gets
  four distinct colours. `RainbowColorable k`: some colouring with at most `k` colours (`Fin k`) is rainbow.
  `chiRainbow`: the least such `k`.

Internal tools: `IsRainbowS` for colourings of all unordered pairs (only edges matter), monotonicity in `k`, and the
action of an injective map of the ground set (`vmap`), which maps 4-cycle subgraphs to 4-cycle subgraphs.
-/

namespace V182Geo

/-- The vertices of `G`: the subsets of `{0, …, 7}` with 3, 4 or 5 elements. -/
abbrev V : Type := {s : Finset (Fin 8) // 3 ≤ s.card ∧ s.card ≤ 5}

/-- Adjacency in `G`: one set contains the other and their sizes differ by one. -/
def Adj (u v : V) : Prop :=
  (u.1 ⊆ v.1 ∧ v.1.card = u.1.card + 1) ∨ (v.1 ⊆ u.1 ∧ u.1.card = v.1.card + 1)

instance : DecidableRel Adj := fun u v => by unfold Adj; infer_instance

/-- **The 182-vertex omission-layer graph** `G`. -/
def G : SimpleGraph V where
  Adj := Adj
  symm := fun _ _ h => h.symm
  loopless := fun u h => by rcases h with ⟨-, h⟩ | ⟨-, h⟩ <;> omega

instance : DecidableRel G.Adj := inferInstanceAs (DecidableRel Adj)

/-- A **4-cycle subgraph** `a-b-c-d-a` of `G`: four pairwise distinct vertices with `a ~ b ~ c ~ d ~ a` (chords
allowed). -/
structure IsFourCycle (a b c d : V) : Prop where
  ne_ab : a ≠ b
  ne_ac : a ≠ c
  ne_ad : a ≠ d
  ne_bc : b ≠ c
  ne_bd : b ≠ d
  ne_cd : c ≠ d
  ab : G.Adj a b
  bc : G.Adj b c
  cd : G.Adj c d
  da : G.Adj d a

/-- An edge colouring of `G` with colours in `α` (not necessarily proper) is **rainbow** if the four edges of every
4-cycle subgraph get four distinct colours. -/
def IsRainbow {α : Type*} (col : G.edgeSet → α) : Prop :=
  ∀ a b c d (h : IsFourCycle a b c d),
    [col ⟨s(a, b), G.mem_edgeSet.2 h.ab⟩, col ⟨s(b, c), G.mem_edgeSet.2 h.bc⟩,
      col ⟨s(c, d), G.mem_edgeSet.2 h.cd⟩, col ⟨s(d, a), G.mem_edgeSet.2 h.da⟩].Nodup

/-- `G` has a rainbow edge colouring with at most `k` colours. -/
def RainbowColorable (k : ℕ) : Prop := ∃ col : G.edgeSet → Fin k, IsRainbow col

/-- **The rainbow-C4 chromatic index of `G`**: the least number of colours of a rainbow edge colouring. -/
noncomputable def chiRainbow : ℕ := sInf {k | RainbowColorable k}

/-! ## Colourings of all unordered pairs -/

/-- Rainbow for a colouring of all unordered pairs of vertices (only the edges of 4-cycles are looked at). -/
def IsRainbowS {α : Type*} (col : Sym2 V → α) : Prop :=
  ∀ a b c d, IsFourCycle a b c d → [col s(a, b), col s(b, c), col s(c, d), col s(d, a)].Nodup

/-- The extension by `0` of an edge colouring to all pairs. -/
noncomputable def extend {k : ℕ} (col : G.edgeSet → Fin (k + 1)) (e : Sym2 V) : Fin (k + 1) :=
  open Classical in if he : e ∈ G.edgeSet then col ⟨e, he⟩ else 0

theorem extend_edge {k : ℕ} (col : G.edgeSet → Fin (k + 1)) {a b : V} (h : G.Adj a b) :
    extend col s(a, b) = col ⟨s(a, b), G.mem_edgeSet.2 h⟩ := by
  unfold extend
  rw [dif_pos (G.mem_edgeSet.2 h)]

theorem isRainbowS_extend {k : ℕ} {col : G.edgeSet → Fin (k + 1)} (h : IsRainbow col) :
    IsRainbowS (extend col) := by
  intro a b c d hc
  rw [extend_edge col hc.ab, extend_edge col hc.bc, extend_edge col hc.cd, extend_edge col hc.da]
  exact h a b c d hc

theorem isRainbow_restrict {α : Type*} {col : Sym2 V → α} (h : IsRainbowS col) :
    IsRainbow (fun e : G.edgeSet => col e.1) :=
  fun a b c d hc => h a b c d hc

theorem rainbowColorable_of_S {k : ℕ} {col : Sym2 V → Fin k} (h : IsRainbowS col) : RainbowColorable k :=
  ⟨fun e => col e.1, isRainbow_restrict h⟩

/-! ## Monotonicity and the least number of colours -/

theorem nodup_map4 {α β : Type*} {f : α → β} (hf : Function.Injective f) {x y z w : α}
    (h : [x, y, z, w].Nodup) : [f x, f y, f z, f w].Nodup := by
  have := h.map hf
  simpa using this

theorem rainbowColorable_mono {k k' : ℕ} (hk : k ≤ k') (h : RainbowColorable k) : RainbowColorable k' := by
  obtain ⟨col, hc⟩ := h
  exact ⟨fun e => Fin.castLE hk (col e), fun a b c d h4 => nodup_map4 (Fin.castLE_injective hk) (hc a b c d h4)⟩

/-- `chiRainbow = 6` from a rainbow 6-colouring and the absence of a rainbow 5-colouring. -/
theorem chiRainbow_eq_six_of (h6 : RainbowColorable 6) (h5 : ¬ RainbowColorable 5) : chiRainbow = 6 := by
  apply le_antisymm
  · exact Nat.sInf_le h6
  · apply le_csInf ⟨6, h6⟩
    intro k hk
    by_contra hlt
    exact h5 (rainbowColorable_mono (by omega) hk)

/-! ## Injective maps of the ground set act on `G` -/

/-- The image of a vertex under an injective map of `{0, …, 7}`. -/
def vmap (σ : Fin 8 ↪ Fin 8) (u : V) : V := ⟨u.1.map σ, by rw [Finset.card_map]; exact u.2⟩

theorem vmap_injective (σ : Fin 8 ↪ Fin 8) : Function.Injective (vmap σ) := fun u v h =>
  Subtype.ext (Finset.map_injective σ (congrArg Subtype.val h))

theorem vmap_adj (σ : Fin 8 ↪ Fin 8) {u v : V} (h : G.Adj u v) : G.Adj (vmap σ u) (vmap σ v) := by
  change Adj u v at h
  change Adj (vmap σ u) (vmap σ v)
  unfold Adj at h ⊢
  simp only [vmap, Finset.card_map, Finset.map_subset_map]
  exact h

theorem isFourCycle_vmap (σ : Fin 8 ↪ Fin 8) {a b c d : V} (h : IsFourCycle a b c d) :
    IsFourCycle (vmap σ a) (vmap σ b) (vmap σ c) (vmap σ d) :=
  ⟨(vmap_injective σ).ne h.ne_ab, (vmap_injective σ).ne h.ne_ac, (vmap_injective σ).ne h.ne_ad,
    (vmap_injective σ).ne h.ne_bc, (vmap_injective σ).ne h.ne_bd, (vmap_injective σ).ne h.ne_cd,
    vmap_adj σ h.ab, vmap_adj σ h.bc, vmap_adj σ h.cd, vmap_adj σ h.da⟩

/-- **Symmetry.** Relabelling the ground set injectively and the colours injectively keeps a colouring rainbow. -/
theorem isRainbowS_transform {α β : Type*} {col : Sym2 V → α} (h : IsRainbowS col) (σ : Fin 8 ↪ Fin 8)
    {ρ : α → β} (hρ : Function.Injective ρ) : IsRainbowS (fun e => ρ (col (Sym2.map (vmap σ) e))) := by
  intro a b c d h4
  simp only [Sym2.map_pair_eq]
  exact nodup_map4 hρ (h _ _ _ _ (isFourCycle_vmap σ h4))

end V182Geo
