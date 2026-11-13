import LeanLB.Check.C4N52
import LeanLB.Check.C6N60
import LeanLB.Check.C2N64
import LeanLB.Check.MirN46
import LeanLB.Check.C3N61
import LeanLB.Check.C5N56
import LeanLB.Check.C7N64

/-!
# Lean-checked symmetric lower-bound sets for k = 8

Each theorem says: the explicit set (defined in `LeanLB/Statement.lean` from the rows of the
repository's file, `LeanLB/Data/*.lean`) has the stated number of points, is in general position, is
invariant under the stated rotation about the origin (or the reflection in `x = 0`), and has no 8
points in convex position. Definitions: `ErdosSzekeres.GeneralPosition`, `ErdosSzekeres.HasConvexNGon`
(`ErdosSzekeres/Definitions.lean`), `LeanLB.Invariant`, `LeanLB.rotAbout`, `LeanLB.lineRefl`.
-/

namespace LeanLB

open ErdosSzekeres Real

/-- **4-fold, 52 points** (`ES8SYM/sets/c4_52pts_13layers.pts`). -/
theorem fourfold52 :
    setC4N52.card = 52 ∧ GeneralPosition setC4N52 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 4)) setC4N52 ∧ ¬ HasConvexNGon 8 setC4N52 := by
  have hlink : c4N52Rows.map (cycPoint 4) = c4N52Nat.map (embed (1, 0) (0, 1) c4N52Shift) :=
    map_eq_of_link (lat := lat4) (g := unshift c4N52Shift) _ _ cycPoint_four (fun _ => rfl)
      c4N52_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 6) (by norm_num) (by rw [c4N52_len]; norm_num)
    c4N52_gp c4N52_dp (embed_scaling (1, 0) (0, 1) c4N52Shift (by norm_num))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 4)) (P := cycPoint 4) (R := shift4) c4N52Rows
    (fun w => by rw [cycPoint_four, cycPoint_four, rot_four, lat4_shift4]) c4N52_closed
  unfold setC4N52
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c4N52_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **6-fold, 60 points** (`SIX60/sets/c6_60pts_D.pts`): the lower bound of "the 6-fold maximum is
exactly 60". -/
theorem sixfold60 :
    setC6N60.card = 60 ∧ GeneralPosition setC6N60 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 6)) setC6N60 ∧ ¬ HasConvexNGon 8 setC6N60 := by
  have hlink : c6N60Rows.map (cycPoint 6) =
      c6N60Nat.map (embed (1, 0) (1 / 2, Real.sqrt 3 / 2) c6N60Shift) :=
    map_eq_of_link (lat := lat6) (g := unshift c6N60Shift) _ _ cycPoint_six (fun _ => rfl)
      c6N60_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 6) (by norm_num) (by rw [c6N60_len]; norm_num)
    c6N60_gp c6N60_dp (embed_scaling (1, 0) (1 / 2, Real.sqrt 3 / 2) c6N60Shift
      (by simp only [one_mul, zero_mul, sub_zero]; positivity))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 6)) (P := cycPoint 6) (R := shift6) c6N60Rows
    (fun w => by rw [cycPoint_six, cycPoint_six, rot_six, lat6_shift6]) c6N60_closed
  unfold setC6N60
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c6N60_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **Half-turn, 64 points** (`ES8SYM/sets/c2_64points_k8.txt`). -/
theorem halfturn64 :
    setC2N64.card = 64 ∧ GeneralPosition setC2N64 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 2)) setC2N64 ∧ ¬ HasConvexNGon 8 setC2N64 := by
  have hlink : c2N64Rows.map intPoint = c2N64Nat.map (embed (1, 0) (0, 1) c2N64Shift) :=
    map_eq_of_link (lat := latXY) (g := unshift c2N64Shift) _ _ intPoint_eq (fun _ => rfl)
      c2N64_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 6) (by norm_num) (by rw [c2N64_len]; norm_num)
    c2N64_gp c2N64_dp (embed_scaling (1, 0) (0, 1) c2N64Shift (by norm_num))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 2)) (P := intPoint) (R := negXY) c2N64Rows
    (fun w => by rw [intPoint_eq, intPoint_eq, rot_two, latXY_negXY]) c2N64_closed
  unfold setC2N64
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c2N64_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **Mirror, 46 points** (`ES8SYM/sets/mirror_46points_k8.txt`), symmetric in the line `x = 0`:
the lower bound of "the mirror maximum is exactly 46". -/
theorem mirror46 :
    setMirN46.card = 46 ∧ GeneralPosition setMirN46 ∧
      Invariant (lineRefl 1 0 0) setMirN46 ∧ ¬ HasConvexNGon 8 setMirN46 := by
  have hlink : mirN46Rows.map intPoint = mirN46Nat.map (embed (1, 0) (0, 1) mirN46Shift) :=
    map_eq_of_link (lat := latXY) (g := unshift mirN46Shift) _ _ intPoint_eq (fun _ => rfl)
      mirN46_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 6) (by norm_num) (by rw [mirN46_len]; norm_num)
    mirN46_gp mirN46_dp (embed_scaling (1, 0) (0, 1) mirN46Shift (by norm_num))
  have hinv := invariant_of_rows (f := lineRefl 1 0 0) (P := intPoint) (R := reflXY) mirN46Rows
    (fun w => by rw [intPoint_eq, intPoint_eq, refl_x, latXY_reflXY]) mirN46_closed
  unfold setMirN46
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, mirN46_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **3-fold, 61 points with the centre** (`ES8SYM/sets4/c3_61pts_centre.txt`). -/
theorem threefold61 :
    setC3N61.card = 61 ∧ GeneralPosition setC3N61 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 3)) setC3N61 ∧ ¬ HasConvexNGon 8 setC3N61 := by
  have hlink : c3N61Rows.map (cycPoint 3) =
      c3N61Nat.map (embed (1, 0) (-1 / 2, Real.sqrt 3 / 2) c3N61Shift) :=
    map_eq_of_link (lat := lat3) (g := unshift c3N61Shift) _ _ cycPoint_three (fun _ => rfl)
      c3N61_link
  obtain ⟨hc, hg, hn⟩ := lowerBound_of_check (B := 6) (by norm_num) (by rw [c3N61_len]; norm_num)
    c3N61_gp c3N61_dp (embed_scaling (1, 0) (-1 / 2, Real.sqrt 3 / 2) c3N61Shift
      (by simp only [one_mul, zero_mul, sub_zero]; positivity))
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 3)) (P := cycPoint 3) (R := mulOmega) c3N61Rows
    (fun w => by rw [cycPoint_three, cycPoint_three, rot_three, lat3_mulOmega]) c3N61_closed
  unfold setC3N61
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, c3N61_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **7-fold, 64 points with the centre** (`ES8SYM/sets/c7_64pts_small.pts`): the lower bound of
"the 7-fold maximum is exactly 64". -/
theorem sevenfold64 :
    setC7N64.card = 64 ∧ GeneralPosition setC7N64 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 7)) setC7N64 ∧ ¬ HasConvexNGon 8 setC7N64 := by
  have hlink : c7N64Rows.map (cycPoint 7) = c7N64L.map (fun p => G.embT G.t7 G.s7 p.1) := by
    have e : c7N64L.map (fun p => G.embT G.t7 G.s7 p.1) =
        (c7N64L.map Prod.fst).map (G.embT G.t7 G.s7) := by
      rw [List.map_map]; rfl
    rw [e, G.c7N64_link, List.map_map]
    exact List.map_congr_left (fun w _ => G.cycPoint_seven w)
  have hcert := List.all_eq_true.mp G.c7N64_cert
  have hD : (0 : ℤ) < G.D7 := by unfold G.D7; norm_num
  have hlo : (0 : ℤ) < G.lo7 := by unfold G.lo7; norm_num
  have hsc : (0 : ℤ) < c7N64Sc := by unfold c7N64Sc; norm_num
  have hop : ∀ a ∈ c7N64L, ∀ b ∈ c7N64L, ∀ c ∈ c7N64L, G.opA (8 * c7N64Mx + 8) a b c = true →
      0 < orient (G.embT G.t7 G.s7 a.1) (G.embT G.t7 G.s7 b.1) (G.embT G.t7 G.s7 c.1) :=
    fun a ha b hb c hc h => G.opA_sound hD hlo hsc G.s7_pos G.t7_bounds.1 G.t7_bounds.2
      (hcert a ha) (hcert b hb) (hcert c hc) h
  have hab : ∀ p ∈ c7N64L, ∀ q ∈ c7N64L, G.abA 1 (2 + 2 * 1) p q = true →
      G.evT G.t7 p.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t7 p.1.1 <
        G.evT G.t7 q.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t7 q.1.1 :=
    fun p hp q hq h => G.abA_sound hD hlo hsc G.t7_bounds.1 G.t7_bounds.2 1 (hcert p hp)
      (hcert q hq) h
  have h3 : 3 ≤ c7N64L.length := by rw [G.c7N64_len]; norm_num
  obtain ⟨hc, hg, hn⟩ := G.lowerBound (op := G.opA (8 * c7N64Mx + 8)) (ab := G.abA 1 (2 + 2 * 1))
    (B := 6) (L := c7N64L) (φ := fun p => G.embT G.t7 G.s7 p.1)
    (hgt := fun p => G.evT G.t7 p.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t7 p.1.1)
    hop (G.opA_cyc _) hab (by norm_num) h3 G.c7N64_gp G.c7N64_dp
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 7)) (P := cycPoint 7)
    (R := cycShift 7) c7N64Rows
    (fun w => by have := rot_cycPoint 7 (by norm_num) w; push_cast at this; exact this)
    G.c7N64_closed
  unfold setC7N64
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, G.c7N64_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-- **5-fold, 56 points with the centre** (`ES8SYM/sets3/c5_56pts_11layers_centre.pts`). -/
theorem fivefold56 :
    setC5N56.card = 56 ∧ GeneralPosition setC5N56 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 5)) setC5N56 ∧ ¬ HasConvexNGon 8 setC5N56 := by
  have hlink : c5N56Rows.map (cycPoint 5) = c5N56L.map (fun p => G.embT G.t5 G.s5 p.1) := by
    have e : c5N56L.map (fun p => G.embT G.t5 G.s5 p.1) =
        (c5N56L.map Prod.fst).map (G.embT G.t5 G.s5) := by
      rw [List.map_map]; rfl
    rw [e, G.c5N56_link, List.map_map]
    exact List.map_congr_left (fun w _ => G.cycPoint_five w)
  have hcert := List.all_eq_true.mp G.c5N56_cert
  have hD : (0 : ℤ) < G.D5 := by unfold G.D5; norm_num
  have hlo : (0 : ℤ) < G.lo5 := by unfold G.lo5; norm_num
  have hsc : (0 : ℤ) < c5N56Sc := by unfold c5N56Sc; norm_num
  have hop : ∀ a ∈ c5N56L, ∀ b ∈ c5N56L, ∀ c ∈ c5N56L, G.opA (8 * c5N56Mx + 8) a b c = true →
      0 < orient (G.embT G.t5 G.s5 a.1) (G.embT G.t5 G.s5 b.1) (G.embT G.t5 G.s5 c.1) :=
    fun a ha b hb c hc h => G.opA_sound hD hlo hsc G.s5_pos G.t5_bounds.1 G.t5_bounds.2
      (hcert a ha) (hcert b hb) (hcert c hc) h
  have hab : ∀ p ∈ c5N56L, ∀ q ∈ c5N56L, G.abA 1 (2 + 2 * 1) p q = true →
      G.evT G.t5 p.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t5 p.1.1 <
        G.evT G.t5 q.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t5 q.1.1 :=
    fun p hp q hq h => G.abA_sound hD hlo hsc G.t5_bounds.1 G.t5_bounds.2 1 (hcert p hp)
      (hcert q hq) h
  have h3 : 3 ≤ c5N56L.length := by rw [G.c5N56_len]; norm_num
  obtain ⟨hc, hg, hn⟩ := G.lowerBound (op := G.opA (8 * c5N56Mx + 8)) (ab := G.abA 1 (2 + 2 * 1))
    (B := 6) (L := c5N56L) (φ := fun p => G.embT G.t5 G.s5 p.1)
    (hgt := fun p => G.evT G.t5 p.1.2 + ((1 : ℕ) : ℝ) * G.evT G.t5 p.1.1)
    hop (G.opA_cyc _) hab (by norm_num) h3 G.c5N56_gp G.c5N56_dp
  have hinv := invariant_of_rows (f := rotAbout 0 (2 * π / 5)) (P := cycPoint 5)
    (R := cycShift 5) c5N56Rows
    (fun w => by have := rot_cycPoint 5 (by norm_num) w; push_cast at this; exact this)
    G.c5N56_closed
  unfold setC5N56
  refine ⟨?_, ?_, hinv, ?_⟩
  · rw [hlink, hc, G.c5N56_len]
  · rw [hlink]; exact hg
  · rw [hlink]; exact hn

/-! ## Existential forms -/

theorem exists_sixfold60 : ∃ S : Finset Point, S.card = 60 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 6)) S ∧ ¬ HasConvexNGon 8 S := ⟨setC6N60, sixfold60⟩

theorem exists_fourfold52 : ∃ S : Finset Point, S.card = 52 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 4)) S ∧ ¬ HasConvexNGon 8 S := ⟨setC4N52, fourfold52⟩

theorem exists_halfturn64 : ∃ S : Finset Point, S.card = 64 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 2)) S ∧ ¬ HasConvexNGon 8 S := ⟨setC2N64, halfturn64⟩

theorem exists_mirror46 : ∃ S : Finset Point, S.card = 46 ∧ GeneralPosition S ∧
    Invariant (lineRefl 1 0 0) S ∧ ¬ HasConvexNGon 8 S := ⟨setMirN46, mirror46⟩

theorem exists_threefold61 : ∃ S : Finset Point, S.card = 61 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 3)) S ∧ ¬ HasConvexNGon 8 S := ⟨setC3N61, threefold61⟩

theorem exists_sevenfold64 : ∃ S : Finset Point, S.card = 64 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 7)) S ∧ ¬ HasConvexNGon 8 S := ⟨setC7N64, sevenfold64⟩

theorem exists_fivefold56 : ∃ S : Finset Point, S.card = 56 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 5)) S ∧ ¬ HasConvexNGon 8 S := ⟨setC5N56, fivefold56⟩

end LeanLB
