import ErdosSzekeres.Definitions
import ErdosSzekeres.OrientationGeometry
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.GroupTheory.Perm.Sign

/-!
# Orbit variables and phase variables of the layered encoders

Two soundness facts used by the layered SAT encoders (`C7UPPER/gen.py`, step 1 and step 0):

* **(a)** `orient` is invariant under every rotation `rotAbout c θ` (`orient_rotAbout_inv`), hence
  under every composition of rotations about `c` (`RotComp.preservesOrient`).
* **(b)** `orient` is alternating under the six permutations of an ordered triple
  (`orient3_perm`).  Together: if `t' = g ∘ t ∘ σ` with `g` a composition of rotations by multiples
  of `2π/m` and `σ` a permutation of the three positions, then
  `orient3 t' = sign σ * orient3 t` (`orient3_rot_perm`).  Consequently the sign attached to an
  ordered triple does not depend on which rotation/permutation maps it to the canonical
  representative (`sign_eq_of_two_reps`), and the encoder's literal (one variable per orbit,
  negated when the parity of the sorting permutations is odd) has the truth value of
  `orient > 0` (`literal_sound`, label-level form `encoder_literal_sound`).
* **(c)** For even `m`, in an invariant set in general position no two distinct points lie on the
  same open ray from `c` (`same_ray_false`): the antipode `2c - x` of `x` is in `S` and is collinear
  with `x` and `y`.  Hence two points whose directions agree modulo `2π/m` are in the same orbit
  (`eq_iterate_of_phase_eq`, `eq_iterate_of_phase_eq_int`), i.e. points of distinct layers have
  distinct phases (`phase_ne_of_not_mem_orbit`).

Definitions `iterate_mem`, `Invariant`, `toC`, `ofC`, `crot`, `rotAbout`, `polar` and their basic
lemmas are copied verbatim from `LAYERLEAN/LayerLemma.lean`.

Compile from the repository root: `lake env lean <this file>`.
-/

namespace ErdosSzekeres.OrbitConsistency

open Function Complex

/-! ## 0. Copied definitions -/

theorem iterate_mem {α : Type*} {f : α → α} {S : Finset α} (hinv : ∀ y ∈ S, f y ∈ S) {x : α}
    (hx : x ∈ S) : ∀ i, f^[i] x ∈ S
  | 0 => hx
  | i + 1 => by
    rw [iterate_succ_apply']
    exact hinv _ (iterate_mem hinv hx i)

/-- `f` maps `S` into itself. -/
def Invariant (f : Point → Point) (S : Finset Point) : Prop := ∀ p ∈ S, f p ∈ S

/-- Complex coordinate of a point. -/
def toC (p : Point) : ℂ := ⟨p 0, p 1⟩

/-- The point with complex coordinate `z`. -/
def ofC (z : ℂ) : Point := ![z.re, z.im]

@[simp] theorem toC_re (p : Point) : (toC p).re = p 0 := rfl
@[simp] theorem toC_im (p : Point) : (toC p).im = p 1 := rfl
@[simp] theorem ofC_zero (z : ℂ) : ofC z 0 = z.re := rfl
@[simp] theorem ofC_one (z : ℂ) : ofC z 1 = z.im := rfl

@[simp] theorem toC_ofC (z : ℂ) : toC (ofC z) = z := by
  apply Complex.ext <;> rfl

@[simp] theorem ofC_toC (p : Point) : ofC (toC p) = p := by
  funext i
  fin_cases i <;> rfl

theorem toC_injective : Function.Injective toC := fun p q h => by
  rw [← ofC_toC p, h, ofC_toC]

/-- Rotation about `c` by the complex factor `w` (a rotation when `|w| = 1`). -/
def crot (c w : ℂ) (p : Point) : Point := ofC (c + w * (toC p - c))

@[simp] theorem toC_crot (c w : ℂ) (p : Point) : toC (crot c w p) = c + w * (toC p - c) :=
  toC_ofC _

theorem crot_one (c : ℂ) : crot c 1 = id := by
  funext p
  apply toC_injective
  simp

theorem crot_comp (c w v : ℂ) (p : Point) : crot c w (crot c v p) = crot c (w * v) p := by
  apply toC_injective
  simp only [toC_crot]
  ring

theorem crot_iterate (c w : ℂ) : ∀ k : ℕ, (crot c w)^[k] = crot c (w ^ k)
  | 0 => by simp [crot_one]
  | k + 1 => by
    funext p
    rw [iterate_succ_apply', crot_iterate c w k, crot_comp, pow_succ']

/-- Rotation about `c` by the angle `θ`, in coordinates. -/
noncomputable def rotAbout (c : Point) (θ : ℝ) (p : Point) : Point :=
  ![c 0 + Real.cos θ * (p 0 - c 0) - Real.sin θ * (p 1 - c 1),
    c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)]

theorem rotAbout_eq_crot (c : Point) (θ : ℝ) :
    rotAbout c θ = crot (toC c) (Complex.exp (θ * Complex.I)) := by
  funext p
  apply toC_injective
  rw [toC_crot]
  apply Complex.ext <;>
    simp [rotAbout, Complex.exp_ofReal_mul_I_re, Complex.exp_ofReal_mul_I_im] <;> ring

theorem rotAbout_iterate (c : Point) (α : ℝ) (j : ℕ) :
    (rotAbout c α)^[j] = rotAbout c (j * α) := by
  rw [rotAbout_eq_crot, crot_iterate, rotAbout_eq_crot, ← Complex.exp_nat_mul]
  push_cast
  ring_nf

/-- The point `c + r (cos θ, sin θ)`. -/
noncomputable def polar (c : Point) (r θ : ℝ) : Point := ![c 0 + r * Real.cos θ, c 1 + r * Real.sin θ]

/-! ## (a) Rotations preserve orientation -/

/-- **(a)** `orient` is invariant under the rotation `rotAbout c θ`. -/
theorem orient_rotAbout_inv (c : Point) (θ : ℝ) (a b d : Point) :
    orient (rotAbout c θ a) (rotAbout c θ b) (rotAbout c θ d) = orient a b d := by
  simp only [orient, rotAbout, Matrix.cons_val_zero, Matrix.cons_val_one]
  linear_combination ((b 0 - a 0) * (d 1 - a 1) - (b 1 - a 1) * (d 0 - a 0)) *
    Real.sin_sq_add_cos_sq θ

/-- A map of the plane that preserves every orientation. -/
def PreservesOrient (f : Point → Point) : Prop :=
  ∀ a b d : Point, orient (f a) (f b) (f d) = orient a b d

theorem preservesOrient_id : PreservesOrient id := fun _ _ _ => rfl

theorem PreservesOrient.comp {f g : Point → Point} (hf : PreservesOrient f)
    (hg : PreservesOrient g) : PreservesOrient (f ∘ g) := fun a b d => by
  show orient (f (g a)) (f (g b)) (f (g d)) = orient a b d
  rw [hf, hg]

theorem PreservesOrient.iterate {f : Point → Point} (hf : PreservesOrient f) :
    ∀ n : ℕ, PreservesOrient f^[n]
  | 0 => preservesOrient_id
  | n + 1 => by
    rw [iterate_succ]
    exact (PreservesOrient.iterate hf n).comp hf

theorem preservesOrient_rotAbout (c : Point) (θ : ℝ) : PreservesOrient (rotAbout c θ) :=
  orient_rotAbout_inv c θ

/-- Compositions of rotations about `c` by integer multiples of `2π/m`. -/
inductive RotComp (c : Point) (m : ℕ) : (Point → Point) → Prop
  | id : RotComp c m id
  | step (k : ℤ) {g : Point → Point} :
      RotComp c m g → RotComp c m (rotAbout c (k * (2 * Real.pi / m)) ∘ g)

theorem RotComp.preservesOrient {c : Point} {m : ℕ} {g : Point → Point} (h : RotComp c m g) :
    PreservesOrient g := by
  induction h with
  | id => exact preservesOrient_id
  | step k _ ih => exact PreservesOrient.comp (preservesOrient_rotAbout c _) ih

/-- The powers of the generator `ρ = rotAbout c (2π/m)` are rotation compositions. -/
theorem rotComp_iterate (c : Point) (m : ℕ) :
    ∀ s : ℕ, RotComp c m (rotAbout c (2 * Real.pi / m))^[s]
  | 0 => RotComp.id
  | s + 1 => by
    rw [iterate_succ']
    have h := RotComp.step (c := c) (m := m) 1 (rotComp_iterate c m s)
    simpa using h

/-! ## (b) Permutations and the consistency of one variable per orbit -/

/-- The orientation of an ordered triple `t 0, t 1, t 2`. -/
def orient3 (t : Fin 3 → Point) : ℝ := orient (t 0) (t 1) (t 2)

/-- A transposition of two positions negates the orientation. -/
theorem orient3_swap (t : Fin 3 → Point) {x y : Fin 3} (hxy : x ≠ y) :
    orient3 (t ∘ Equiv.swap x y) = -orient3 t := by
  fin_cases x <;> fin_cases y <;> simp at hxy <;>
    simp [orient3, Equiv.swap_apply_def, orient] <;> ring

/-- **(b), permutation part.** For each of the six permutations `σ` of the positions,
`orient3 (t ∘ σ) = sign σ * orient3 t`. -/
theorem orient3_perm (σ : Equiv.Perm (Fin 3)) :
    ∀ t : Fin 3 → Point, orient3 (t ∘ σ) = ((Equiv.Perm.sign σ : ℤ) : ℝ) * orient3 t := by
  refine Equiv.Perm.swap_induction_on σ ?_ ?_
  · intro t
    simp
  · intro f x y hxy ih t
    have hcomp : t ∘ ⇑(Equiv.swap x y * f) = (t ∘ Equiv.swap x y) ∘ f := by
      funext i
      simp
    rw [hcomp, ih, orient3_swap t hxy, Equiv.Perm.sign_mul, Equiv.Perm.sign_swap hxy]
    push_cast
    ring

/-- **(b), consistency.** If the ordered triple `t'` is obtained from `t` by a permutation `σ` of
the positions followed by a composition `g` of rotations about `c` by multiples of `2π/m`, then
`orient3 t' = sign σ * orient3 t`. -/
theorem orient3_rot_perm {c : Point} {m : ℕ} {g : Point → Point} (hg : RotComp c m g)
    (σ : Equiv.Perm (Fin 3)) (t t' : Fin 3 → Point) (h : t' = g ∘ t ∘ σ) :
    orient3 t' = ((Equiv.Perm.sign σ : ℤ) : ℝ) * orient3 t := by
  subst h
  have hg' : orient3 (g ∘ t ∘ σ) = orient3 (t ∘ σ) :=
    hg.preservesOrient ((t ∘ σ) 0) ((t ∘ σ) 1) ((t ∘ σ) 2)
  rw [hg', orient3_perm]

/-- Well-definedness of the sign: two ways of mapping `t` to the same triple `t'` use
permutations of the same sign, as soon as `orient3 t ≠ 0`. -/
theorem sign_eq_of_two_reps {c : Point} {m : ℕ} {g₁ g₂ : Point → Point} (hg₁ : RotComp c m g₁)
    (hg₂ : RotComp c m g₂) (σ₁ σ₂ : Equiv.Perm (Fin 3)) (t t' : Fin 3 → Point)
    (h₁ : t' = g₁ ∘ t ∘ σ₁) (h₂ : t' = g₂ ∘ t ∘ σ₂) (hne : orient3 t ≠ 0) :
    Equiv.Perm.sign σ₁ = Equiv.Perm.sign σ₂ := by
  have e₁ := orient3_rot_perm hg₁ σ₁ t t' h₁
  have e₂ := orient3_rot_perm hg₂ σ₂ t t' h₂
  have e : ((Equiv.Perm.sign σ₁ : ℤ) : ℝ) = ((Equiv.Perm.sign σ₂ : ℤ) : ℝ) :=
    mul_right_cancel₀ hne (e₁.symm.trans e₂)
  exact Units.ext (by exact_mod_cast e)

/-- Two triples mapped to the same representative have orientations related by the product of
the two signs. -/
theorem orient3_of_common_rep {c : Point} {m : ℕ} {g₁ g₂ : Point → Point} (hg₁ : RotComp c m g₁)
    (hg₂ : RotComp c m g₂) (σ₁ σ₂ : Equiv.Perm (Fin 3)) (t₁ t₂ C : Fin 3 → Point)
    (h₁ : C = g₁ ∘ t₁ ∘ σ₁) (h₂ : C = g₂ ∘ t₂ ∘ σ₂) :
    ((Equiv.Perm.sign σ₁ : ℤ) : ℝ) * orient3 t₁ = ((Equiv.Perm.sign σ₂ : ℤ) : ℝ) * orient3 t₂ :=
  (orient3_rot_perm hg₁ σ₁ t₁ C h₁).symm.trans (orient3_rot_perm hg₂ σ₂ t₂ C h₂)

/-- The literal of the encoder: the orbit variable `0 < orient3 C`, negated when the sign is odd. -/
def litVal (ε : ℤˣ) (C : Fin 3 → Point) : Prop :=
  if ε = 1 then 0 < orient3 C else ¬ 0 < orient3 C

/-- **Literal soundness.** If `C = g ∘ t ∘ σ` and `orient3 t ≠ 0` (general position), then
`orient3 t > 0` holds exactly when the literal `litVal (sign σ) C` holds. -/
theorem literal_sound {c : Point} {m : ℕ} {g : Point → Point} (hg : RotComp c m g)
    (σ : Equiv.Perm (Fin 3)) (t C : Fin 3 → Point) (h : C = g ∘ t ∘ σ) (hne : orient3 t ≠ 0) :
    0 < orient3 t ↔ litVal (Equiv.Perm.sign σ) C := by
  have e := orient3_rot_perm hg σ t C h
  unfold litVal
  rcases Int.units_eq_one_or (Equiv.Perm.sign σ) with hs | hs
  · rw [if_pos hs, e, hs]
    simp
  · have hne1 : Equiv.Perm.sign σ ≠ 1 := by rw [hs]; decide
    rw [if_neg hne1, e, hs]
    push_cast
    constructor
    · intro hp hn
      linarith
    · intro hn
      rcases lt_or_gt_of_ne hne with hlt | hgt
      · exact absurd (by linarith) hn
      · exact hgt

/-- **Label-level form, as in the encoder.** Points carry labels `ι`, `P : ι → Point`, and the label
rotation `r` realises `ρ = rotAbout c (2π/m)`.  The encoder sorts the ordered label triple `T`
(`T₀ = T ∘ σ₁`, parity `sign σ₁`), then takes the canonical representative
`C = r^[s] ∘ T₀ ∘ σ₂` (parity `sign σ₂`), and uses the orbit variable of `C`, negated when
`sign σ₁ * sign σ₂ ≠ 1`.  Under general position this literal is true exactly when
`orient (P (T 0)) (P (T 1)) (P (T 2)) > 0`. -/
theorem encoder_literal_sound {ι : Type*} (P : ι → Point) (r : ι → ι) {c : Point} {m : ℕ}
    (hr : ∀ i, P (r i) = rotAbout c (2 * Real.pi / m) (P i))
    (T T₀ C : Fin 3 → ι) (σ₁ σ₂ : Equiv.Perm (Fin 3)) (s : ℕ)
    (h₁ : T₀ = T ∘ σ₁) (h₂ : C = r^[s] ∘ T₀ ∘ σ₂) (hne : orient3 (P ∘ T) ≠ 0) :
    0 < orient3 (P ∘ T) ↔ litVal (Equiv.Perm.sign σ₁ * Equiv.Perm.sign σ₂) (P ∘ C) := by
  have hsc : Semiconj P r (rotAbout c (2 * Real.pi / m)) := hr
  have hcomm : P ∘ r^[s] = (rotAbout c (2 * Real.pi / m))^[s] ∘ P := by
    funext i
    exact (hsc.iterate_right s) i
  have hPC : P ∘ C = (rotAbout c (2 * Real.pi / m))^[s] ∘ (P ∘ T) ∘ ⇑(σ₁ * σ₂) := by
    rw [h₂, h₁]
    funext i
    simp only [comp_apply, Equiv.Perm.mul_apply]
    exact congrFun hcomm _
  rw [← Equiv.Perm.sign_mul]
  exact literal_sound (rotComp_iterate c m s) (σ₁ * σ₂) (P ∘ T) (P ∘ C) hPC hne

/-! ## (c) Even order: no two points on one ray, so phases of distinct layers differ -/

/-- For even `m`, the antipode `2c - x` of a point of an invariant set lies in the set. -/
theorem antipode_mem_of_even {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) {x : Point} (hx : x ∈ S) :
    (![2 * c 0 - x 0, 2 * c 1 - x 1] : Point) ∈ S := by
  have hq : (rotAbout c (2 * Real.pi / m))^[m / 2] x ∈ S := iterate_mem hinv hx (m / 2)
  have hhalf : ((m / 2 : ℕ) : ℝ) * (2 * Real.pi / m) = Real.pi := by
    obtain ⟨k, hk⟩ := heven
    have hk' : m / 2 = k := by omega
    have hkpos : (0 : ℝ) < k := by exact_mod_cast (show 0 < k by omega)
    rw [hk', hk]
    push_cast
    field_simp
    ring
  have hqval : (rotAbout c (2 * Real.pi / m))^[m / 2] x = ![2 * c 0 - x 0, 2 * c 1 - x 1] := by
    rw [rotAbout_iterate, hhalf]
    funext i
    fin_cases i <;> simp [rotAbout] <;> ring
  rw [← hqval]
  exact hq

/-- **(c)** For even `m`, an invariant set in general position has no two distinct points `x, y`
on one open ray from `c` (`y - c = λ (x - c)`, `λ > 0`): `x`, `y` and `2c - x ∈ S` would be
collinear. -/
theorem same_ray_false {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m) (hm : 0 < m)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {x y : Point} (hx : x ∈ S) (hy : y ∈ S) (hxy : x ≠ y) {l : ℝ} (hl : 0 < l)
    (hray : y - c = l • (x - c)) : False := by
  set q : Point := ![2 * c 0 - x 0, 2 * c 1 - x 1] with hqdef
  have hq : q ∈ S := antipode_mem_of_even heven hm hinv hx
  have hy0 : y 0 = c 0 + l * (x 0 - c 0) := by
    have := congrFun hray 0
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this
    linarith
  have hy1 : y 1 = c 1 + l * (x 1 - c 1) := by
    have := congrFun hray 1
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this
    linarith
  have hxc : x ≠ c := by
    intro h
    apply hxy
    funext i
    fin_cases i
    · show x 0 = y 0
      rw [hy0, h]
      ring
    · show x 1 = y 1
      rw [hy1, h]
      ring
  have hcoord : x 0 ≠ c 0 ∨ x 1 ≠ c 1 := by
    by_contra hcon
    push_neg at hcon
    apply hxc
    funext i
    fin_cases i
    · exact hcon.1
    · exact hcon.2
  have hxq : x ≠ q := by
    intro h
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    simp only [hqdef, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    rcases hcoord with h' | h'
    · exact h' (by linarith)
    · exact h' (by linarith)
  have hyq : y ≠ q := by
    intro h
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    simp only [hqdef, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    rw [hy0] at h0
    rw [hy1] at h1
    have e0 : (l + 1) * (x 0 - c 0) = 0 := by linarith
    have e1 : (l + 1) * (x 1 - c 1) = 0 := by linarith
    have hl1 : l + 1 ≠ 0 := by linarith
    rcases hcoord with h' | h'
    · exact h' (sub_eq_zero.1 ((mul_eq_zero.1 e0).resolve_left hl1))
    · exact h' (sub_eq_zero.1 ((mul_eq_zero.1 e1).resolve_left hl1))
  have h0 : orient x y q = 0 := by
    simp only [orient, hqdef, Matrix.cons_val_zero, Matrix.cons_val_one]
    rw [hy0, hy1]
    ring
  exact (generalPosition_iff_orient_ne_zero S).1 hgp x hx y hy q hq hxy hxq hyq h0

theorem rotAbout_polar (c : Point) (r θ φ : ℝ) :
    rotAbout c φ (polar c r θ) = polar c r (θ + φ) := by
  funext i
  fin_cases i <;> simp [rotAbout, polar, Real.cos_add, Real.sin_add] <;> ring

/-- **Phases, natural form.** For even `m`, if two points `x = c + r e^{iα}` and
`y = c + r' e^{iβ}` (`r, r' > 0`) of an invariant set in general position satisfy
`β = α + k · 2π/m`, then `y = ρ^k x`: the two points are in one orbit (one layer). -/
theorem eq_iterate_of_phase_eq {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r') (hx : polar c r α ∈ S) (hy : polar c r' β ∈ S)
    {k : ℕ} (hk : β = α + k * (2 * Real.pi / m)) :
    polar c r' β = (rotAbout c (2 * Real.pi / m))^[k] (polar c r α) := by
  have hx' : (rotAbout c (2 * Real.pi / m))^[k] (polar c r α) ∈ S := iterate_mem hinv hx k
  have hval : (rotAbout c (2 * Real.pi / m))^[k] (polar c r α) = polar c r β := by
    rw [rotAbout_iterate, rotAbout_polar, hk]
  rw [hval] at hx' ⊢
  by_contra hne
  refine same_ray_false heven hm hinv hgp hx' hy (Ne.symm hne) (l := r' / r) (by positivity) ?_
  funext i
  fin_cases i
  · show c 0 + r' * Real.cos β - c 0 = r' / r * (c 0 + r * Real.cos β - c 0)
    rw [div_mul_eq_mul_div, eq_div_iff hr.ne']
    ring
  · show c 1 + r' * Real.sin β - c 1 = r' / r * (c 1 + r * Real.sin β - c 1)
    rw [div_mul_eq_mul_div, eq_div_iff hr.ne']
    ring

theorem polar_add_int (c : Point) (r θ : ℝ) (n : ℤ) :
    polar c r (θ + n * (2 * Real.pi)) = polar c r θ := by
  simp only [polar, Real.cos_add_int_mul_two_pi, Real.sin_add_int_mul_two_pi]

/-- **Phases, integer form.** Same as `eq_iterate_of_phase_eq` with `β = α + k · 2π/m`, `k ∈ ℤ`:
then `y = ρ^j x` for `j = k mod m`. -/
theorem eq_iterate_of_phase_eq_int {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r') (hx : polar c r α ∈ S) (hy : polar c r' β ∈ S)
    {k : ℤ} (hk : β = α + k * (2 * Real.pi / m)) :
    ∃ j : ℕ, polar c r' β = (rotAbout c (2 * Real.pi / m))^[j] (polar c r α) := by
  have hmz : (0 : ℤ) < m := by exact_mod_cast hm
  set j : ℕ := (k % (m : ℤ)).toNat with hjdef
  have hmod_nonneg : 0 ≤ k % (m : ℤ) := Int.emod_nonneg k hmz.ne'
  have hj : (j : ℤ) = k % (m : ℤ) := Int.toNat_of_nonneg hmod_nonneg
  have hdecomp : k = (j : ℤ) + (m : ℤ) * (k / (m : ℤ)) := by
    rw [hj]
    exact (Int.emod_add_mul_ediv k m).symm
  have hmR : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  have hβ : β = (α + (j : ℝ) * (2 * Real.pi / m)) + ((k / (m : ℤ) : ℤ) : ℝ) * (2 * Real.pi) := by
    rw [hk]
    have hkR : (k : ℝ) = (j : ℝ) + (m : ℝ) * ((k / (m : ℤ) : ℤ) : ℝ) := by
      exact_mod_cast hdecomp
    rw [hkR]
    field_simp
    ring
  have hy' : polar c r' (α + (j : ℝ) * (2 * Real.pi / m)) ∈ S := by
    rw [hβ, polar_add_int] at hy
    exact hy
  refine ⟨j, ?_⟩
  rw [hβ, polar_add_int]
  exact eq_iterate_of_phase_eq heven hm hinv hgp hr hr' hx hy' rfl

/-- **Phases of distinct layers differ (even `m`).** If `y` is not in the `ρ`-orbit of `x`, then
the directions of `x` and `y` are not congruent modulo `2π/m`.  With the labelling of the encoder
(layer `0` has a point of direction `0`), this gives `ψ_i ≠ ψ_j` for distinct layers and
`ψ_i ≠ 0` for `i ≥ 1`, with no perturbation. -/
theorem phase_ne_of_not_mem_orbit {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r') (hx : polar c r α ∈ S) (hy : polar c r' β ∈ S)
    (horb : ∀ j : ℕ, polar c r' β ≠ (rotAbout c (2 * Real.pi / m))^[j] (polar c r α)) :
    ∀ k : ℤ, β ≠ α + k * (2 * Real.pi / m) := by
  intro k hk
  obtain ⟨j, hj⟩ := eq_iterate_of_phase_eq_int heven hm hinv hgp hr hr' hx hy hk
  exact horb j hj

end ErdosSzekeres.OrbitConsistency
