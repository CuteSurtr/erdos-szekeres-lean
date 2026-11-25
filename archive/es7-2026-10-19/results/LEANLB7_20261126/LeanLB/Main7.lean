import LeanLB.Statement7
import LeanLB.Check.C3N31
import LeanLB.Check.C6N30
import LeanLB.Check.C4N28
import LeanLB.Check.C2N32
import LeanLB.Check.MirN32
import LeanLB.Check.C5N31

/-!
# Lean-checked symmetric lower-bound sets for k = 7 (RESULTS.md row C7)

Each theorem says: the explicit set (`LeanLB/Statement7.lean`, from the rows of the repository's file)
has the stated number of points, is in general position, is invariant under the stated rotation about
the origin (or the reflection in `x = 0`), and has no 7 points in convex position. The checker and its
soundness proof are those of LEANLB20261111, with the chain bound `B = 5` instead of `6`
(`lowerBound_of_check` and `G.lowerBound` give `¬ HasConvexNGon (B + 2)`).
-/

namespace LeanLB

open ErdosSzekeres Real

/-- **3-fold, 31 points with the centre** (`SYMMAX/c3_31points.txt`). -/
theorem threefold31 :
    setC3N31.card = 31 ∧ GeneralPosition setC3N31 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 3)) setC3N31 ∧ ¬ HasConvexNGon 7 setC3N31 := by
  have hlink : c3N31Rows.map (cycPoint 3) =
      c3N31Nat.map (embed (1, 0) (-1 / 2, Real.sqrt 3 / 2) c3N31Shift) :=
    map_eq_of_link (lat := lat3) (g := unshift c3N31Shift) _ _ cycPoint_three (fun _ => rfl)
      c3N31_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 5) (by norm_num) (by rw [c3N31_len]; norm_num)
    c3N31_gp c3N31_dp (embed_scaling (1, 0) (-1 / 2, Real.sqrt 3 / 2) c3N31Shift
      (by simp only [one_mul, zero_mul, sub_zero]; positivity))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 3)) (P := cycPoint 3) (R := mulOmega) c3N31Rows
    (fun w => by rw [cycPoint_three, cycPoint_three, rot_three, lat3_mulOmega]) c3N31_closed
  unfold setC3N31
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c3N31_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **6-fold, 30 points** (`SYMMAX/c6_30points.txt`, Eisenstein coordinates). -/
theorem sixfold30 :
    setC6N30.card = 30 ∧ GeneralPosition setC6N30 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 6)) setC6N30 ∧ ¬ HasConvexNGon 7 setC6N30 := by
  have hlink : c6N30Rows.map (cycPoint 3) =
      c6N30Nat.map (embed (1, 0) (-1 / 2, Real.sqrt 3 / 2) c6N30Shift) :=
    map_eq_of_link (lat := lat3) (g := unshift c6N30Shift) _ _ cycPoint_three (fun _ => rfl)
      c6N30_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 5) (by norm_num) (by rw [c6N30_len]; norm_num)
    c6N30_gp c6N30_dp (embed_scaling (1, 0) (-1 / 2, Real.sqrt 3 / 2) c6N30Shift
      (by simp only [one_mul, zero_mul, sub_zero]; positivity))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 6)) (P := cycPoint 3) (R := mulZeta3) c6N30Rows
    (fun w => by rw [cycPoint_three, cycPoint_three, rot_six_eis, lat3_mulZeta3]) c6N30_closed
  unfold setC6N30
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c6N30_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **4-fold, 28 points** (`SYMMAX/c4_28points.txt`). -/
theorem fourfold28 :
    setC4N28.card = 28 ∧ GeneralPosition setC4N28 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 4)) setC4N28 ∧ ¬ HasConvexNGon 7 setC4N28 := by
  have hlink : c4N28Rows.map intPoint = c4N28Nat.map (embed (1, 0) (0, 1) c4N28Shift) :=
    map_eq_of_link (lat := latXY) (g := unshift c4N28Shift) _ _ intPoint_eq (fun _ => rfl)
      c4N28_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 5) (by norm_num) (by rw [c4N28_len]; norm_num)
    c4N28_gp c4N28_dp (embed_scaling (1, 0) (0, 1) c4N28Shift (by norm_num))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 4)) (P := intPoint) (R := rot90XY) c4N28Rows
    (fun w => by rw [intPoint_eq, intPoint_eq, rot_four, latXY_rot90XY]) c4N28_closed
  unfold setC4N28
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c4N28_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **Half-turn, 32 points** (`SYM2/sym7_32points.txt`): 32 is the largest size of a heptagon-free set
if ES(7) = 33. -/
theorem halfturn32 :
    setC2N32.card = 32 ∧ GeneralPosition setC2N32 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 2)) setC2N32 ∧ ¬ HasConvexNGon 7 setC2N32 := by
  have hlink : c2N32Rows.map intPoint = c2N32Nat.map (embed (1, 0) (0, 1) c2N32Shift) :=
    map_eq_of_link (lat := latXY) (g := unshift c2N32Shift) _ _ intPoint_eq (fun _ => rfl)
      c2N32_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 5) (by norm_num) (by rw [c2N32_len]; norm_num)
    c2N32_gp c2N32_dp (embed_scaling (1, 0) (0, 1) c2N32Shift (by norm_num))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 2)) (P := intPoint) (R := negXY) c2N32Rows
    (fun w => by rw [intPoint_eq, intPoint_eq, rot_two, latXY_negXY]) c2N32_closed
  unfold setC2N32
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c2N32_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **Mirror, 32 points** (`SYMMAX/mirror_32points.txt`), symmetric in the line `x = 0`. -/
theorem mirror32 :
    setMirN32.card = 32 ∧ GeneralPosition setMirN32 ∧
      Invariant (lineRefl 1 0 0) setMirN32 ∧ ¬ HasConvexNGon 7 setMirN32 := by
  have hlink : mirN32Rows.map intPoint = mirN32Nat.map (embed (1, 0) (0, 1) mirN32Shift) :=
    map_eq_of_link (lat := latXY) (g := unshift mirN32Shift) _ _ intPoint_eq (fun _ => rfl)
      mirN32_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 5) (by norm_num) (by rw [mirN32_len]; norm_num)
    mirN32_gp mirN32_dp (embed_scaling (1, 0) (0, 1) mirN32Shift (by norm_num))
  have hinv := invariant_of_rows (f := lineRefl 1 0 0) (P := intPoint) (R := reflXY) mirN32Rows
    (fun w => by rw [intPoint_eq, intPoint_eq, refl_x, latXY_reflXY]) mirN32_closed
  unfold setMirN32
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, mirN32_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **5-fold, 31 points with the centre** (`SYMMAX/c5_31points.txt`). -/
theorem fivefold31 :
    setC5N31.card = 31 ∧ GeneralPosition setC5N31 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 5)) setC5N31 ∧ ¬ HasConvexNGon 7 setC5N31 := by
  have hlink : c5N31Rows.map (cycPoint 5) = c5N31L.map (fun p => G.embT G.t5 G.s5 p.1) := by
    have e : c5N31L.map (fun p => G.embT G.t5 G.s5 p.1) =
        (c5N31L.map Prod.fst).map (G.embT G.t5 G.s5) := by
      rw [List.map_map]; rfl
    rw [e, G.c5N31_link, List.map_map]
    exact List.map_congr_left (fun w _ => G.cycPoint_five w)
  have hcert := List.all_eq_true.mp G.c5N31_cert
  have hD : (0 : ℤ) < G.D5 := by unfold G.D5; norm_num
  have hlo : (0 : ℤ) < G.lo5 := by unfold G.lo5; norm_num
  have hsc : (0 : ℤ) < c5N31Sc := by unfold c5N31Sc; norm_num
  have hop : ∀ a ∈ c5N31L, ∀ b ∈ c5N31L, ∀ c ∈ c5N31L, G.opA (8 * c5N31Mx + 8) a b c = true →
      0 < orient (G.embT G.t5 G.s5 a.1) (G.embT G.t5 G.s5 b.1) (G.embT G.t5 G.s5 c.1) :=
    fun a ha b hb c hc h => G.opA_sound hD hlo hsc G.s5_pos G.t5_bounds.1 G.t5_bounds.2
      (hcert a ha) (hcert b hb) (hcert c hc) h
  have hab : ∀ p ∈ c5N31L, ∀ q ∈ c5N31L, G.abA 1 (2 + 2 * 1) p q = true →
      G.evT G.t5 p.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t5 p.1.1 <
        G.evT G.t5 q.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t5 q.1.1 :=
    fun p hp q hq h => G.abA_sound hD hlo hsc G.t5_bounds.1 G.t5_bounds.2 1 (hcert p hp)
      (hcert q hq) h
  have h3 : 3 ≤ c5N31L.length := by rw [G.c5N31_len]; norm_num
  obtain ⟨hc, hg, hn⟩ := G.lowerBound (op := G.opA (8 * c5N31Mx + 8)) (ab := G.abA 1 (2 + 2 * 1))
    (B := 5) (L := c5N31L) (φ := fun p => G.embT G.t5 G.s5 p.1)
    (hgt := fun p => G.evT G.t5 p.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t5 p.1.1)
    hop (G.opA_cyc _) hab (by norm_num) h3 G.c5N31_gp G.c5N31_dp
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 5)) (P := cycPoint 5)
    (R := G.mulZ5) c5N31Rows G.rot_cycPoint_mulZ5 G.c5N31_closed
  unfold setC5N31
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, G.c5N31_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-! ## Existential forms -/

theorem exists_threefold31 : ∃ S : Finset Point, S.card = 31 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 3)) S ∧ ¬ HasConvexNGon 7 S := ⟨setC3N31, threefold31⟩

theorem exists_sixfold30 : ∃ S : Finset Point, S.card = 30 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 6)) S ∧ ¬ HasConvexNGon 7 S := ⟨setC6N30, sixfold30⟩

theorem exists_fourfold28 : ∃ S : Finset Point, S.card = 28 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 4)) S ∧ ¬ HasConvexNGon 7 S := ⟨setC4N28, fourfold28⟩

theorem exists_halfturn32 : ∃ S : Finset Point, S.card = 32 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 2)) S ∧ ¬ HasConvexNGon 7 S := ⟨setC2N32, halfturn32⟩

theorem exists_mirror32 : ∃ S : Finset Point, S.card = 32 ∧ GeneralPosition S ∧
    Invariant (lineRefl 1 0 0) S ∧ ¬ HasConvexNGon 7 S := ⟨setMirN32, mirror32⟩

theorem exists_fivefold31 : ∃ S : Finset Point, S.card = 31 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 5)) S ∧ ¬ HasConvexNGon 7 S := ⟨setC5N31, fivefold31⟩

/-! ## ES(7) ≥ 33 from an explicit set

The library has this for every `n` (`ErdosSzekeres.not_forcesConvexNGon_two_pow`); here it follows from
the 32-point half-turn set. -/

/-- 32 points do not force a convex 7-gon. -/
theorem not_forcesConvexNGon_32_7 : ¬ ForcesConvexNGon 32 7 := fun h =>
  halfturn32.2.2.2 (h setC2N32 halfturn32.2.1 halfturn32.1.ge)

/-- Any number of points that forces a convex 7-gon is at least 33: ES(7) ≥ 33. -/
theorem heptagon_lower_bound {N : ℕ} (h : ForcesConvexNGon N 7) : 33 ≤ N := by
  by_contra hN
  exact not_forcesConvexNGon_32_7 (h.mono (by omega))

end LeanLB
