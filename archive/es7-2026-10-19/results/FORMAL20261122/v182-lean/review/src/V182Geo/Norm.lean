import V182Geo.Cover
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.FinCases

/-!
# V182Geo.Norm: the 10 symmetry units (wave-1 README 3.3; DESIGN.md §3.3)

For a rainbow 5-colouring `φ` put `a_x = φ(X0–X0+x)` (`x = 3..7`) and `b_y = φ(Y0−y–Y0)` (`y = 0..4`), with
`X0 = {0,1,2}`, `Y0 = {0..4}`. Rainbowness gives `a`, `b` injective and `{a_3, a_4} ∩ {b_3, b_4} = ∅` (4-cycle
`(X0, X0+3, Y0, X0+4)`).
1. Colour step (generic): `ρ1 = a⁻¹` makes `a_x = x − 3`.
2. Finite step (`norm_finite`, kernel check over the 120 permutations `B` of the normalised `b`): an explicit
   witness map `σ` of `{0..7}` (fixing 3 and 4, mapping `{0,1,2}` and `{5,6,7}` onto themselves) and colour map
   `ρ2` satisfy `ρ2(a_{σ x}) = x − 3` and `ρ2(b_{σ y}) = nf(y)`, `nf = (0,1,4,2,3)`.
Then `ψ = ρ2 ∘ ρ1 ∘ φ ∘ (σ•)` is rainbow (`isRainbowS_transform`) and satisfies the 10 units (`UnitsHold`).
-/

namespace V182Geo
open V182Enc

instance (a b c d : V) : Decidable (IsFourCycle a b c d) :=
  decidable_of_iff (a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d ∧
      G.Adj a b ∧ G.Adj b c ∧ G.Adj c d ∧ G.Adj d a)
    ⟨fun ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ => ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩,
      fun h => ⟨h.ne_ab, h.ne_ac, h.ne_ad, h.ne_bc, h.ne_bd, h.ne_cd, h.ab, h.bc, h.cd, h.da⟩⟩

def X0s : Finset (Fin 8) := {0, 1, 2}
def Y0s : Finset (Fin 8) := {0, 1, 2, 3, 4}

theorem hX0 : 3 ≤ X0s.card ∧ X0s.card ≤ 5 := by decide
theorem hY0 : 3 ≤ Y0s.card ∧ Y0s.card ≤ 5 := by decide
theorem hXa : ∀ x : Fin 8, 3 ≤ (insert x X0s).card ∧ (insert x X0s).card ≤ 5 := by decide
theorem hYb : ∀ y : Fin 8, 3 ≤ (Y0s.erase y).card ∧ (Y0s.erase y).card ≤ 5 := by decide
theorem hXaa : ∀ x x' : Fin 8, 3 ≤ (insert x' (insert x X0s)).card ∧ (insert x' (insert x X0s)).card ≤ 5 := by
  decide
theorem hYbb : ∀ y y' : Fin 8, 3 ≤ ((Y0s.erase y).erase y').card ∧ ((Y0s.erase y).erase y').card ≤ 5 := by
  decide

def vX0 : V := ⟨X0s, hX0⟩
def vY0 : V := ⟨Y0s, hY0⟩
def vXa (x : Fin 8) : V := ⟨insert x X0s, hXa x⟩
def vYb (y : Fin 8) : V := ⟨Y0s.erase y, hYb y⟩
def vXaa (x x' : Fin 8) : V := ⟨insert x' (insert x X0s), hXaa x x'⟩
def vYbb (y y' : Fin 8) : V := ⟨(Y0s.erase y).erase y', hYbb y y'⟩

/-- The edge `X0–X0+x`. -/
def eXn (x : Fin 8) : Sym2 V := s(vX0, vXa x)
/-- The edge `Y0−y–Y0`. -/
def eYn (y : Fin 8) : Sym2 V := s(vYb y, vY0)

theorem cycX : ∀ x x' : Fin 8, 3 ≤ x.val → 3 ≤ x'.val → x ≠ x' → IsFourCycle vX0 (vXa x) (vXaa x x') (vXa x') := by
  decide +kernel
theorem cycY : ∀ y y' : Fin 8, y.val < 5 → y'.val < 5 → y ≠ y' →
    IsFourCycle (vYbb y y') (vYb y') vY0 (vYb y) := by
  decide +kernel
theorem cycXY : IsFourCycle vX0 (vXa 3) vY0 (vXa 4) := by decide +kernel
theorem vXa3 : vXa 3 = vYb 4 := by decide
theorem vXa4 : vXa 4 = vYb 3 := by decide

/-- The unit edges in natural form (kernel checks on the numbering). -/
theorem e3 : edgeOfIdx 3 = eXn 3 := by decide +kernel
theorem e12 : edgeOfIdx 12 = eXn 4 := by decide +kernel
theorem e45 : edgeOfIdx 45 = eXn 5 := by decide +kernel
theorem e126 : edgeOfIdx 126 = eXn 6 := by decide +kernel
theorem e287 : edgeOfIdx 287 = eXn 7 := by decide +kernel
theorem e32 : edgeOfIdx 32 = eYn 0 := by decide +kernel
theorem e25 : edgeOfIdx 25 = eYn 1 := by decide +kernel
theorem e18 : edgeOfIdx 18 = eYn 2 := by decide +kernel
theorem e11 : edgeOfIdx 11 = eYn 3 := by decide +kernel
theorem e4 : edgeOfIdx 4 = eYn 4 := by decide +kernel

theorem nodup4 {α : Type*} {w x y z : α} (h : [w, x, y, z].Nodup) :
    w ≠ x ∧ w ≠ y ∧ w ≠ z ∧ x ≠ y ∧ x ≠ z ∧ y ≠ z := by
  rw [List.Nodup, List.pairwise_cons, List.pairwise_cons, List.pairwise_cons] at h
  exact ⟨h.1 x (by simp), h.1 y (by simp), h.1 z (by simp), h.2.1 y (by simp), h.2.1 z (by simp),
    h.2.2.1 z (by simp)⟩

/-! ## The finite step -/

/-- The witness ground map as a value list (from the normalised `b`, as the list `B`). -/
def wS (B : List ℕ) : List ℕ :=
  [B.idxOf 0, B.idxOf 1, B.idxOf (9 - B.getD 3 0 - B.getD 4 0), 3, 4, 3 + B.getD 3 0, 3 + B.getD 4 0,
    3 + (9 - B.getD 3 0 - B.getD 4 0)]

/-- The witness colour map as a value list. -/
def wR (B : List ℕ) : List ℕ :=
  (List.range 5).map fun c =>
    if c = B.getD 3 0 then 2 else if c = B.getD 4 0 then 3 else if c = 9 - B.getD 3 0 - B.getD 4 0 then 4 else c

def fS (B : List ℕ) (i : Fin 8) : Fin 8 := ⟨(wS B).getD i 0 % 8, Nat.mod_lt _ (by decide)⟩
def fR (B : List ℕ) (c : Fin 5) : Fin 5 := ⟨(wR B).getD c 0 % 5, Nat.mod_lt _ (by decide)⟩
def xi (x : Fin 8) : Fin 5 := ⟨(x.val - 3) % 5, Nat.mod_lt _ (by decide)⟩
def bB (B : List ℕ) (y : Fin 8) : Fin 5 := ⟨B.getD y 0 % 5, Nat.mod_lt _ (by decide)⟩
def nfF (y : Fin 8) : Fin 5 := ⟨[0, 1, 4, 2, 3].getD y 0 % 5, Nat.mod_lt _ (by decide)⟩

/-- **The finite step** (kernel check over the 120 permutations; the 36 with `B_3, B_4 ≥ 2` are checked). -/
theorem norm_finite : ∀ B ∈ perms5, 2 ≤ B.getD 3 0 → 2 ≤ B.getD 4 0 →
    (∀ i j : Fin 8, fS B i = fS B j → i = j) ∧ (∀ c d : Fin 5, fR B c = fR B d → c = d) ∧
    X0s.image (fS B) = X0s ∧ Y0s.image (fS B) = Y0s ∧
    (∀ x : Fin 8, 3 ≤ x.val → 3 ≤ (fS B x).val ∧ fR B (xi (fS B x)) = xi x) ∧
    (∀ y : Fin 8, y.val < 5 → (fS B y).val < 5 ∧ fR B (bB B (fS B y)) = nfF y) := by
  decide +kernel

/-! ## The action on the star edges -/

theorem vmap_vX0 {σ : Fin 8 ↪ Fin 8} (h : X0s.image σ = X0s) : vmap σ vX0 = vX0 :=
  Subtype.ext (by show X0s.map σ = X0s; rw [Finset.map_eq_image]; exact h)

theorem vmap_vY0 {σ : Fin 8 ↪ Fin 8} (h : Y0s.image σ = Y0s) : vmap σ vY0 = vY0 :=
  Subtype.ext (by show Y0s.map σ = Y0s; rw [Finset.map_eq_image]; exact h)

theorem vmap_vXa {σ : Fin 8 ↪ Fin 8} (h : X0s.image σ = X0s) (x : Fin 8) : vmap σ (vXa x) = vXa (σ x) :=
  Subtype.ext (by
    show (insert x X0s).map σ = insert (σ x) X0s
    rw [Finset.map_insert, Finset.map_eq_image, h])

theorem vmap_vYb {σ : Fin 8 ↪ Fin 8} (h : Y0s.image σ = Y0s) (y : Fin 8) : vmap σ (vYb y) = vYb (σ y) :=
  Subtype.ext (by
    show (Y0s.erase y).map σ = Y0s.erase (σ y)
    rw [Finset.map_erase, Finset.map_eq_image, h])

/-! ## Normalisation -/

/-- **Normalisation.** Every rainbow 5-colouring can be transformed into one satisfying the 10 units. -/
theorem normalize {φ : Sym2 V → Fin 5} (hφ : IsRainbowS φ) : ∃ ψ : Sym2 V → Fin 5, IsRainbowS ψ ∧ UnitsHold ψ := by
  -- consequences of rainbowness on the two stars
  have hXne : ∀ x x' : Fin 8, 3 ≤ x.val → 3 ≤ x'.val → x ≠ x' → φ (eXn x) ≠ φ (eXn x') := by
    intro x x' hx hx' hne
    have h := nodup4 (hφ _ _ _ _ (cycX x x' hx hx' hne))
    have e : s(vXa x', vX0) = eXn x' := Sym2.eq_swap
    rw [e] at h
    exact h.2.2.1
  have hYne : ∀ y y' : Fin 8, y.val < 5 → y'.val < 5 → y ≠ y' → φ (eYn y) ≠ φ (eYn y') := by
    intro y y' hy hy' hne
    have h := nodup4 (hφ _ _ _ _ (cycY y y' hy hy' hne))
    have e1 : s(vY0, vYb y) = eYn y := Sym2.eq_swap
    have e2 : s(vYb y', vY0) = eYn y' := rfl
    rw [e1, e2] at h
    exact fun heq => h.2.2.2.1 heq.symm
  have hXY := nodup4 (hφ _ _ _ _ cycXY)
  have ex3 : s(vX0, vXa 3) = eXn 3 := rfl
  have ey4 : s(vXa 3, vY0) = eYn 4 := by rw [vXa3]; rfl
  have ey3 : s(vY0, vXa 4) = eYn 3 := by rw [vXa4, Sym2.eq_swap]; rfl
  have ex4 : s(vXa 4, vX0) = eXn 4 := Sym2.eq_swap
  rw [ex3, ey4, ey3, ex4] at hXY
  -- step 1: the colour map ρ1 with ρ1 (a_x) = x - 3
  let A : Fin 5 → Fin 5 := fun i => φ (eXn ⟨i.val + 3, by omega⟩)
  have hAinj : Function.Injective A := by
    intro i j hij
    by_contra hne
    refine hXne ⟨i.val + 3, by omega⟩ ⟨j.val + 3, by omega⟩ (by simp) (by simp) ?_ hij
    intro e
    apply hne
    have := congrArg Fin.val e
    simp only at this
    exact Fin.ext (by omega)
  let ρ1 : Fin 5 ≃ Fin 5 := (Equiv.ofBijective A (Finite.injective_iff_bijective.1 hAinj)).symm
  have hρ1 : ∀ i : Fin 5, ρ1 (A i) = i := fun i =>
    (Equiv.ofBijective A (Finite.injective_iff_bijective.1 hAinj)).symm_apply_apply i
  have hX1 : ∀ x : Fin 8, 3 ≤ x.val → ρ1 (φ (eXn x)) = xi x := by
    intro x hx
    have hx8 := x.2
    have e : x = ⟨(x.val - 3) + 3, by omega⟩ := Fin.ext (by simp only; omega)
    have e2 : φ (eXn x) = A ⟨x.val - 3, by omega⟩ := by
      show φ (eXn x) = φ (eXn ⟨(x.val - 3) + 3, _⟩)
      rw [← e]
    rw [e2, hρ1]
    exact Fin.ext (by simp only [xi]; omega)
  -- step 2: the list B of normalised Y0-colours
  let L5 : List (Fin 8) := [0, 1, 2, 3, 4]
  have hL5 : ∀ z ∈ L5, z.val < 5 := by decide
  let g : Fin 8 → ℕ := fun y => (ρ1 (φ (eYn y))).val
  let B : List ℕ := L5.map g
  have hBnd : B.Nodup := by
    refine List.Nodup.map_on ?_ (by decide)
    intro y hy y' hy' hgy
    by_contra hne
    exact hYne y y' (hL5 y hy) (hL5 y' hy') hne (ρ1.injective (Fin.ext hgy))
  have hBlt : ∀ x ∈ B, x < 5 := by
    intro x hx
    obtain ⟨y, -, rfl⟩ := List.mem_map.1 hx
    exact (ρ1 (φ (eYn y))).2
  have hBmem : B ∈ perms5 := mem_perms5 hBnd rfl hBlt
  have hBget : ∀ y : Fin 8, y.val < 5 → B.getD y 0 = g y := by
    intro y hy
    fin_cases y <;> first | rfl | (simp at hy)
  have v0 : ρ1 (φ (eXn 3)) = 0 := (hX1 3 (by decide)).trans (by decide)
  have v1 : ρ1 (φ (eXn 4)) = 1 := (hX1 4 (by decide)).trans (by decide)
  have hB3 : 2 ≤ B.getD 3 0 := by
    have hg : B.getD 3 0 = g 3 := hBget 3 (by decide)
    rw [hg]
    have h0 : ρ1 (φ (eYn 3)) ≠ 0 := by
      rw [← v0]
      exact fun e => hXY.2.1 (ρ1.injective e).symm
    have h1 : ρ1 (φ (eYn 3)) ≠ 1 := by
      rw [← v1]
      exact fun e => hXY.2.2.2.2.2 (ρ1.injective e)
    have h0' : (ρ1 (φ (eYn 3))).val ≠ 0 := fun e => h0 (Fin.ext e)
    have h1' : (ρ1 (φ (eYn 3))).val ≠ 1 := fun e => h1 (Fin.ext e)
    show 2 ≤ (ρ1 (φ (eYn 3))).val
    omega
  have hB4 : 2 ≤ B.getD 4 0 := by
    have hg : B.getD 4 0 = g 4 := hBget 4 (by decide)
    rw [hg]
    have h0 : ρ1 (φ (eYn 4)) ≠ 0 := by
      rw [← v0]
      exact fun e => hXY.1 (ρ1.injective e).symm
    have h1 : ρ1 (φ (eYn 4)) ≠ 1 := by
      rw [← v1]
      exact fun e => hXY.2.2.2.2.1 (ρ1.injective e)
    have h0' : (ρ1 (φ (eYn 4))).val ≠ 0 := fun e => h0 (Fin.ext e)
    have h1' : (ρ1 (φ (eYn 4))).val ≠ 1 := fun e => h1 (Fin.ext e)
    show 2 ≤ (ρ1 (φ (eYn 4))).val
    omega
  obtain ⟨Q1, Q2, Q3, Q4, Q5, Q6⟩ := norm_finite B hBmem hB3 hB4
  -- the transformation
  let σ : Fin 8 ↪ Fin 8 := ⟨fS B, fun i j h => Q1 i j h⟩
  let ψ : Sym2 V → Fin 5 := fun e => fR B (ρ1 (φ (Sym2.map (vmap σ) e)))
  have hinj : Function.Injective (fun c => fR B (ρ1 c)) := fun c d h => ρ1.injective (Q2 _ _ h)
  have hψ : IsRainbowS ψ := isRainbowS_transform hφ σ hinj
  have hXψ : ∀ x : Fin 8, 3 ≤ x.val → ψ (eXn x) = xi x := by
    intro x hx
    show fR B (ρ1 (φ (Sym2.map (vmap σ) s(vX0, vXa x)))) = xi x
    rw [Sym2.map_pair_eq, vmap_vX0 (σ := σ) Q3, vmap_vXa (σ := σ) Q3]
    have h5 := Q5 x hx
    have e : s(vX0, vXa (σ x)) = eXn (fS B x) := rfl
    rw [e, hX1 _ h5.1]
    exact h5.2
  have hYψ : ∀ y : Fin 8, y.val < 5 → ψ (eYn y) = nfF y := by
    intro y hy
    show fR B (ρ1 (φ (Sym2.map (vmap σ) s(vYb y, vY0)))) = nfF y
    rw [Sym2.map_pair_eq, vmap_vY0 (σ := σ) Q4, vmap_vYb (σ := σ) Q4]
    have h6 := Q6 y hy
    have e : s(vYb (σ y), vY0) = eYn (fS B y) := rfl
    have e2 : ρ1 (φ (eYn (fS B y))) = bB B (fS B y) := by
      apply Fin.ext
      show (ρ1 (φ (eYn (fS B y)))).val = B.getD (fS B y) 0 % 5
      rw [hBget _ h6.1]
      exact (Nat.mod_eq_of_lt (ρ1 (φ (eYn (fS B y)))).2).symm
    rw [e, e2]
    exact h6.2
  refine ⟨ψ, hψ, ?_⟩
  intro ec hec
  simp only [unitPairs, List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hec
  rcases hec with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rw [e3, hXψ 3 (by decide)]; rfl
  · rw [e12, hXψ 4 (by decide)]; rfl
  · rw [e45, hXψ 5 (by decide)]; rfl
  · rw [e126, hXψ 6 (by decide)]; rfl
  · rw [e287, hXψ 7 (by decide)]; rfl
  · rw [e32, hYψ 0 (by decide)]; rfl
  · rw [e25, hYψ 1 (by decide)]; rfl
  · rw [e18, hYψ 2 (by decide)]; rfl
  · rw [e11, hYψ 3 (by decide)]; rfl
  · rw [e4, hYψ 4 (by decide)]; rfl

/-- **No rainbow 5-colouring** (modulo the verdicts). -/
theorem not_rainbowColorable_five (h : PieceVerdicts) : ¬ RainbowColorable 5 := by
  rintro ⟨col, hcol⟩
  obtain ⟨ψ, hψ, hu⟩ := normalize (isRainbowS_extend hcol)
  exact no_normal_colouring h hψ hu

end V182Geo
