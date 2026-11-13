# Review of section `lg` (Geometry of the layers: nesting, chains and polar rules): round 1, lens: rigor

Verdict: **pass**. I found no blocker and no major finding. There are five minor findings, listed at the end.

Paths are relative to STAGE (`sections/`, `build/`) or to RES (`LAYERLEAN/...`, `LEANEXT/...`), or to the repository
root for `ErdosSzekeres/...`, as the contract requires.

## What was checked, and how

### 1. Statement fidelity (all 27 in-scope declarations)

I compared each statement in `sections/lg.tex` with `LAYERLEAN/LayerLemma.lean` line by line. For each one I checked
the hypotheses, implicit and explicit binders, the conclusion, strict versus weak inequalities, and natural-number
subtraction and casts. All 27 are faithful:

- **Rotation and trigonometry.**
  - `rotAbout_iterate`: `(rotAbout c α)^[j] = rotAbout c (j * α)`, with `j` cast to ℝ.
  - `orient_rotAbout` and `trig_layer`: the exact polynomial and trigonometric forms.
  - `orient_regular_nonneg`: `0 < m` and **`j ≤ m`**, conclusion `0 ≤ …`.
  - `lin_rotAbout`.
  - `lin_orbit_pos`: `p ≠ c`, `0 < m`, `0 < j`, `j < m`.
  - `orient_next_prev_pos`: `p ≠ c`, `3 ≤ m`, with `m - 1` a natural subtraction. The text notes that it is the
    ordinary difference.
- **Convexity.**
  - `convex_orient_nonneg`: `{q | 0 ≤ orient a b q}`.
  - `convex_disk`: every `R`.
  - `dist2` is defined by its coordinate formula.
- **Layers.**
  - `strict_nesting`: `2 ≤ m`, `K ≤ 2m`, `c ∉ S`, invariance, `¬HasConvexNGon K S`, general position, `n < n'`,
    `x ∈ hullVerts (peel S n)`, `y ∈ peel S n'`, and `0 < orient x (ρ x) y`.
  - `centre_not_mem_of_even`: `0 < m`, `Even m`, invariance, general position, `p ∈ S`, `p ≠ c`, conclusion `c ∉ S`.
    There is no K-freeness hypothesis and no `c ∉ S` hypothesis.
  - `dist2_le_of_later`: `0 < m`, **`n ≤ n'`**, no general position, weak conclusion.
- **Chains.**
  - `lin`.
  - `orient_trans_halfplane`: the five hypotheses in Lean's order, with `c` generic.
  - `fan_step`: hypotheses `h1`–`h5` exactly.
  - `orient_eq_lin`: `lin ![-(x 1 - p 1), x 0 - p 0] x y`.
  - `fan_positive`: index ranges `s < n`, `s+1 < n`, `s+2 < n`; conclusions `j<k<n` and `i<j<k<n`.
  - `fanPt`: `Fin (n+1)`, with `n` implicit; `i = 0 ↦ p`, otherwise `q (i-1)`.
  - `hasConvexNGon_of_fan`: `3 ≤ n`, `p ∈ S`, `q s ∈ S` for `s < n`, (H), (F), (T), conclusion
    `HasConvexNGon (n+1) S`.
  - `lin_pos_of_peel`: `3 ≤ m`, `K ≤ 2m`, …, `y ∈ peel S i`, `y ≠ p`, conclusion `0 < lin (c - p) p y`.
  - `chain_clauses_sound`: `3 ≤ m`, `4 ≤ K`, `K ≤ 2m`, ranges `s < K-1`, `s+1 < K-1`, `s+2 < K-1`, conclusion
    `False`.
- **Polar rules.**
  - `polar`: no sign condition on `r`.
  - `orient_polar`.
  - `orient_polar_centre_inside`: all nine hypotheses, including `0 < rb`.
  - `sin_add_lt`.
  - `orient_polar_halfplane`: weak `ra ≤ rb`, `rd ≤ rb`, no hypothesis on the sign of `rb`, and `δ - α < π`.

There is no ∀/∃ alternation anywhere, and the order of binders matches Lean. No statement is silently strengthened or
weakened.

### 2. File and line references

- Every `\leanref` line matches the declaration line in `LAYERLEAN/LayerLemma.lean`. I checked all 27 with `grep -n`:
  465, 472, 480, 488, 516, 529, 582, 625, 629, 641, 653, 658, 694, 700, 794, 801, 830, 864, 914, 932, 935, 943, 956,
  974, 999, 1002, 1012.
- Other line numbers in the text also hold:
  - `orbitFS` is at :48.
  - `peel_antitone` is at :460.
  - `card_peel` is at :1037, with its docstring at :1036.
  - The cited range 465–1032 ends with `dist2_le_of_later`'s last line.
  - In the main library: `ErdosSzekeres/Orientation.lean:9`, `ErdosSzekeres/OrientationGeometry.lean:66` and
    `ErdosSzekeres/Suk/OrientationClique.lean:9`.
- `sections/lg.map.tsv` has 31 rows. A script matched them one-to-one against the 31 statement environments of the tex
  (label, kind, Lean name and file:line), with no mismatch.

### 3. Hashes and provenance

I recomputed these SHA-256 prefixes and all match:

| File | Prefix |
|---|---|
| `LayerLemma.lean` (1148 lines) | `afb8542dceb0` |
| `LAYERLEAN/README.md` | `9eaec241a1d2` |
| `LAYERLEAN/logs/axioms.log` | `3c4b7aac502e` |
| `LEANEXT/review/axioms.log` | `386c4f578725` |
| `axioms_recheck_20261106/out.txt` | `a59c3816cbe7` |
| `Definitions.lean` | `2425500eefd1` |
| `Orientation.lean` | `f67955ac7091` |
| `OrientationGeometry.lean` | `c7db9bbbb65e` |
| `Suk/OrientationClique.lean` | `cf63d5219b47` |

The other provenance claims also hold:

- `grep` finds no `sorry`, `admit`, `axiom` or `native_decide` in the file.
- `logs/build.log` records exit 0 with 0 message lines.
- `lakefile.toml` has the single default target `ErdosSzekeres`.
- The toolchain is `v4.24.0`.
- A script confirmed that lines 11–1147 of `LayerLemma.lean` occur verbatim in each of `LEANEXT/capstone/Capstone2.lean`,
  `LEANEXT/merged/Merged.lean`, `LEANEXT/es7corr/ES7Corollaries.lean` and `ENCBLEAN/geo/ES8Geo/Capstone2.lean`, as the
  Coverage paragraph says.

### 4. Axioms evidence

I checked each of the 23 in-scope theorems against the three logs with `grep`:

- **`LAYERLEAN/logs/axioms.log`** lists exactly 16 of them. The 7 it lacks are exactly the ones named in the text:
  `rotAbout_iterate`, `orient_rotAbout`, `convex_orient_nonneg`, `orient_eq_lin`, `lin_rotAbout`, `lin_orbit_pos` and
  `orient_next_prev_pos`.
- **`LEANEXT/review/axioms.log`** lists all 23.
- **The re-check `out.txt`** lists exactly 11 of them: `strict_nesting`, `centre_not_mem_of_even`, `fan_positive`,
  `hasConvexNGon_of_fan`, `lin_pos_of_peel`, `chain_clauses_sound`, the four polar results and `dist2_le_of_later`.

Every listed theorem uses only `[propext, Classical.choice, Quot.sound]`.

The map's per-row note on which log covers which theorem agrees with these counts.

### 5. Every identity, checked with sympy

The script is `build/lg_r1rigor_sympy.py`, run under `nice -n 15`. All 65 checks print OK and none print FAIL. The
checks cover:

- **Notation.** The relations in (lg:eq:J), `det(X,Y) = ⟨JX,Y⟩`, and `R_θX = cos θ X + sin θ JX`.
- **Rotation facts.** Lemma `lg:lem:rotfacts`(b), both as the matrix product and as composition of `rotAbout` with a
  general centre, and (d).
- **`orient_rotAbout`.** Checked as a polynomial identity with `cos` and `sin` as free symbols, so no Pythagoras is
  needed, as the text says. The intermediate `b − x = (cos α − 1)u + sin α Ju` is checked too.
- **`trig_layer`,** with both displayed intermediate steps.
- **The value formula of the remark after Lemma `lg:lem:regular`,** `F = 4 sin(π/m) sin(jπ/m) sin((j−1)π/m)`. Also
  checked numerically:
  - `F ≥ 0` for `1 ≤ m ≤ 9` and `0 ≤ j ≤ m`;
  - the zero set is exactly `{1, m}` for `2 ≤ m ≤ 9`.
- **Lemma `lg:lem:next-prev`.** The identity `F = 4 sin t sin(π−t) sin(π−2t)` with `t = π/m`, and `F > 0` for
  `3 ≤ m < 30`.
- **`lin_rotAbout`** (the identity behind `lin_orbit_pos`), as a polynomial identity.
- **(O4),** the affinity of `orient` in its third argument.
- **`convex_disk`:**
  - `u|A|² + v|B|² − |uA+vB|² = uv|A−B|²`, together with the displayed middle expression;
  - `(uy₁+vy₂) − c = uA + vB` when `u + v = 1`.
- **`centre_not_mem_of_even`:**
  - `rotAbout(c,π)(p) = 2c − p`;
  - `orient(p, c, 2c−p) = 0`;
  - `2πk/(2k) = π`.
- **The Cramer identity** in both coordinates, plus:
  - the vanishing of the 3×3 determinant with a repeated row;
  - the cofactor expansion exactly as written;
  - the second and third consequences.
- **`orient_trans_halfplane`.** Identity (lg:eq:trans), and the dictionary `orient(a,·,·) = det(·−a, ·−a)` used in the
  proof.
- **`fan_step`.** Identity (lg:eq:fanstep), the six translations to `det(P,B)`, …, `det(E,B)` via cyclic invariance,
  and the third Cramer instance with `(X,Y,Z,V) = (P,B,A,E)`.
- **`orient_eq_lin`.**
- **The key identity (lg:eq:key) of `lin_pos_of_peel`,** for arbitrary points and also for arbitrary `w`, with
  `orient(p',p,y) = det(E,C)`.
- **`orient_polar`,** with both intermediate `det` expansions and `det(r e(φ), s e(ψ)) = rs sin(ψ−φ)`.
- **Rule A** (`sin z = sin(z+2π)`), the sine addition formula, the **rule B** decomposition
  `r_a r_b sin x + r_b r_d sin y − r_d r_a sin(x+y) = r_a(r_b−r_d) sin x + r_d(r_b−r_a) sin y + r_a r_d(sin x + sin y − sin(x+y))`,
  and `orient_polar` specialised to `β = α + x`, `δ = α + x + y`.

### 6. Step-by-step referee check of every proof

- **Lemma `lg:lem:layer`.** Each use of (L2)–(L4) meets its hypotheses:
  - `c ∉ peel(S,n)` and the K-freeness of `peel(S,n)` are inherited correctly;
  - (L3) needs only `0 < m`, `c ∉ S` and invariance;
  - (L4) is applied to `peel(S,n)` with `x ∈ hv(peel(S,n))`;
  - (d) uses `n+1 ≤ n'` and `peel(S,n+1) = peel(S,n) \ L`.

  I compared (L1)–(L4) with the statements of `ll:lem:hv`(c), `ll:lem:antitone`, `ll:lem:inv-peel` and
  `ll:thm:core-rot` in `sections/ll.tex`, and they match.
- **Lemma `lg:lem:rot-iter`.** The induction uses `f^{j+1} = f ∘ f^j` and the cast `(j+1 : ℝ) = j + 1`; it is fine.
  Corollary `lg:cor:period` uses `(m:ℝ) ≠ 0`.
- **Lemma `lg:lem:regular`.** The case split `j = 0` or `1 ≤ j ≤ m` is exhaustive. The ranges `0 < t ≤ π`,
  `0 ≤ jt ≤ π` and `0 ≤ (j−1)t ≤ jt ≤ π` are correct, and so is `sin ≥ 0` on `[0, π]`. The remark's refinement is
  correct for `m ≥ 2`, `x ≠ c` and `1 ≤ j ≤ m`.
- **Lemma `lg:lem:lin-orbit`.** `|p−c|² > 0` because some coordinate differs, and `0 < 2πj/m < 2π`, so `cos < 1`.
- **Lemma `lg:lem:next-prev`.** `(m−1)t = π − t`. For `m ≥ 3`: `t ∈ (0, π/3]`, `π−t ∈ [2π/3, π)` and
  `π−2t ∈ [π/3, π)`.
- **Theorem `lg:thm:nesting`.**
  - The weak half: `L ⊆ H` because `j < m ⇒ j ≤ m` (the `j ≤ m` range of `orient_regular_nonneg`), `H` is convex, and
    hence `conv L ⊆ H`.
  - The strict half: `ρ(x) = ρ¹(x) ∈ L` because `1 < m`. `x ≠ ρ(x)` comes from Lemma `lg:lem:lin-orbit` with `j = 1`
    and `lin(c−x, x, x) = 0`. This is a valid alternative to Lean's minimal-period argument, and it is not circular:
    `lg:lem:lin-orbit` does not depend on nesting. `y ∉ L` gives the other two distinctness facts, and general
    position (fd:lem:collinear(b)) finishes the proof.
  - Remark (2), on `m = 2`: the argument derives `orient = 0` from `y ∈ conv{x, ρx}` via (O4)/(O3) and combines it
    with the already-proved theorem. It is valid and not circular.
- **Lemma `lg:lem:centre`.** `Even m ⇒ m = k + k`, `k ≥ 1`, `m/2 = k`, `q ∈ S` by iterated invariance, `q = 2c − p`,
  and the three distinctness facts are each proved. The remark's example `S = {c}` is correct.
- **Theorem `lg:thm:radius`.** Lemma `lg:lem:rotfacts`(d), plus `lg:lem:disk` with `R = dist2(c,x)`, plus
  `lg:lem:layer`(c) with `n' ≥ n`. No general position is needed, and none is used.
- **Lemma `lg:lem:fan-pos`.** I checked each of the three inductions.
  - **(a)** The base `k = j+1` is (F). In the step, all three (H) indices are `< n`, and Lemma `lg:lem:trans` is
    applied with `(a,b,c,e) = (p, q_j, q_k, q_{k+1})`.
  - **(b₀)** The base is (T) at `s = i`, using `i+2 < n`. The five hypotheses of `fan_step` are (T) at `s`, (F) at
    `s+1`, (F) at `s`, the induction hypothesis (which needs `s+1 < n`), and (a) at `(i, s+1)`. They match the Lean
    proof (`hturn s`, `hfan (s+1)`, `hfan s`, `ih`, `hP i (s+1)`).
  - **(b)** The base is (b₀) at `s = j`. For the step, `w' = J(q_i − p)` gives `lin(w', q_i, ·) = orient(p, q_i, ·)`,
    which is positive at every `q_t` with `i < t < n` by (a). The induction hypothesis and (b₀) at `s = k` complete it.

  All three inductions are well founded, being on `k ≥ j+1`, `s ≥ i+1` and `k ≥ j+1`.
- **Theorem `lg:thm:fan`.**
  - Step 1: in both cases the index shift `i−1 < j−1 < k−1 < n` is correct.
  - Step 2: a third index exists because `n+1 ≥ 4 > 2`, and (O3) covers every coincidence pattern.
  - Step 3: the hypotheses of `fd:lem:pos-triples` are met exactly, namely a linear order, injectivity,
    `|s| = n+1 ≥ 4`, and positivity on every increasing triple. I compared these with the statement in
    `sections/fd.tex`.
  - Step 4: the cardinality follows from injectivity.
- **Lemma `lg:lem:halfplane`.**
  - The case split `y ∈ L` or `y ∉ L` is exhaustive. In the first case `j ≠ 0` because `ρ⁰p = p ≠ y`.
  - `p' = ρ^{m−1}(p) ∈ L`, and `ρ(p') = ρ^m(p) = p` by Corollary `lg:cor:period`.
  - (e1) and (e2): every hypothesis of Theorem `lg:thm:nesting` is listed and holds, including `p' ∈ hv(peel(S,i))`.
  - (w1) and (w2) use `0 < 1 < m` and `0 < m−1 < m`; (o) uses `m ≥ 3`.
  - The signs in (lg:eq:key) match the derivation from the Cramer identity, which sympy confirms.
- **Theorem `lg:thm:chain`.**
  - `K−1 ≥ 3` is the ordinary difference.
  - The hypotheses of `lg:lem:halfplane` hold for each `q_s`, namely (i), (ii), `m ≥ 3` and `K ≤ 2m`.
  - Theorem `lg:thm:fan` is applied to `peel(S,i)` with `n = K−1` and `w = c − p`.
  - `(K−1)+1 = K` because `K ≥ 1`.
  - `fd:lem:mono`(c) lifts the result to `S`.
- **Polar part.**
  - `lg:lem:polar`: `b − a = B − A`, and the `det` expansion is correct.
  - Rule A: all three sines are positive.
  - `lg:lem:sinadd`: from `cos < 1`, which holds because `cos x = 1` only on `2πℤ`.
  - Rule B: `x, y < π` follows from `x + y < π` with `x, y > 0`, and the three-term decomposition is correct.

**Summary of the checks.**

- Every inequality direction is correct.
- Every case split is exhaustive.
- No step is delegated to Lean. Each parenthetical about Lean (`ring`, `nlinarith`, the complex form, `cos 2t =
  2cos² t − 1`) only describes the Lean route; the written argument is complete without it.

### 7. Numeric sanity (not part of the proof)

The script is `build/lg_r1rigor_numeric.py`. I checked strict nesting, the tangent half-plane, the radius order and
next/previous positivity on two kinds of configuration:

- the review instance S4 = {(±2,0), (0,±2), (±½,±½)}, with `c = 0` and `m = 4`, in exact rational arithmetic;
- 300 random nested regular m-gons, with `3 ≤ m ≤ 9` and 2–4 layers (39 436 nesting pairs).

All of them hold.

### 8. Compile, labels, contract hygiene

- `build/lg_r1rigor_wrapper.tex` is the contract wrapper. Two `nice -n 15 pdflatex` passes both exit 0. The only
  undefined references are `fd:` and `ll:` labels. There is no error, no "Missing $" and no overfull box.
- **Labels.** All 13 required export labels are defined on the named statements: `lg:lem:orient-rot`,
  `lg:lem:regular`, `lg:thm:nesting`, `lg:lem:centre`, `lg:thm:fan`, `lg:lem:halfplane`, `lg:thm:chain`,
  `lg:def:polar`, `lg:lem:polar`, `lg:lem:ruleA`, `lg:lem:sinadd`, `lg:lem:ruleB` and `lg:thm:radius`.
- **References.**
  - Every `\ref` points to an `lg:` label, to an `fd:` label from the contract list, or to an `ll:` export label.
  - Every cited `fd:` and `ll:` label exists in `sections/fd.tex` or `sections/ll.tex`.
- **Text.**
  - There are no machine paths and no tool names.
  - Nothing is overclaimed: no "verified" or "certified", only "Lean-checked" for Lean theorems and "written proofs
    (not refereed)" for the proofs.
  - The Coverage paragraph lists all 27 scope declarations, and its exclusions (`peel_antitone`, `card_peel`, the
    verbatim copies) are justified.

## Findings (all minor)

### m1 (minor): the "non-simp" qualifier is attributed to the review report

- **Location:** `sections/lg.tex:46–48` (Axioms paragraph).
- **Issue:** The text says the review log "according to LEANEXT/review/REPORT.md covers all 59 non-simp theorems of the
  reviewed file". The report does not say "non-simp".
- **Evidence:**
  - `LEANEXT/review/REPORT.md:16` reads "All 59 theorem declarations were checked".
  - F6 there reads "the file has 59 theorems in all".
  - The file actually has 59 `theorem` declarations plus 7 `@[simp] theorem` declarations (`LayerLemma.lean:236–254`),
    66 in total.
  - The qualifier "non-simp" is therefore correct as a fact, but the report itself does not say it, and the report's
    own count "59 in all" is inaccurate.
- **Suggested fix:** "…covers the 59 theorems of the reviewed file that are not tagged `@[simp]` (the report says 'All
  59 theorem declarations were checked'; the file has 7 further `@[simp]` theorems)…".

### m2 (minor): the provenance wording for the written steps is slightly inaccurate

- **Location:** `sections/lg.tex:57–58` (Rigor paragraph) and `:841–842` (Coverage).
- **Issue:** Both passages say the written steps "collect facts that the Lean proofs establish inline". Two of them do
  not fit that description.
- **Evidence:**
  - Lean never states the general Cramer identity of Lemma `lg:lem:cramer`. It proves each of the three instances,
    (lg:eq:trans), (lg:eq:fanstep) and (lg:eq:key), directly by `ring` (`LayerLemma.lean:632–634, 644–646, 901–904`).
  - Lean never proves the second half of Corollary `lg:cor:period`, `ρ^m = id` for every point. It obtains
    `ρ^[m] y = y` only for `y ≠ c`, from `minimalPeriod_rotAbout` (`:886–890`, `:392–395`).
  - The text does note both deviations locally: Remark (2) after Lemma `lg:lem:halfplane`, Remark (1) after it on
    `ring`, and the map notes. The general sentence, however, still describes them as inline Lean facts. Likewise, "They
    follow the Lean proofs, except where a remark says otherwise" (`:56`) is not accompanied by a remark at Lemmas
    `lg:lem:trans` and `lg:lem:fan-step`, where the key identity is derived from Lemma `lg:lem:cramer` instead of
    Lean's `ring`.
- **Effect:** None on correctness. Both written proofs are complete.
- **Suggested fix:** "…are not Lean declarations; they are proved here. Lemma `lg:lem:cramer` derives the identities
  that Lean checks by `ring`, and Corollary `lg:cor:period` replaces Lean's minimal-period argument."

### m3 (minor): the title of Lemma `lg:lem:halfplane-convex` is too strong when `a = b`

- **Location:** `sections/lg.tex:346`, the title "closed half-planes are convex"; also the overview line 12.
- **Issue:** The statement is for all points `a, b`. When `a = b`, `orient(a,a,q) = 0` for every `q`, so the set is
  all of ℝ², not a half-plane.
- **Effect:** None. The statement and proof are correct, and the paragraph after Definition `lg:def:lin` and the one
  after Lemma `lg:lem:orient-lin` are correctly qualified ("for w ≠ 0", "for x ≠ p").
- **Suggested fix:** Add "(for a = b the set is the whole plane)".

### m4 (minor): standard facts are cited without a reference

- **Location:** `sections/lg.tex:273`, `:321–322`, `:341`, `:413`, `:760`, `:773–774` and `:795`.
- **Issue:** Contract rule 5 asks that cited textbook facts come with "a precise statement and a reference". The
  section uses the following facts without a source:
  - "cos θ = 1 only for θ ∈ 2πℤ";
  - "sine is ≥ 0 on [0, π]" and "> 0 on (0, π)";
  - in Remark (2) after Theorem `lg:thm:nesting`, the convex hull of two points is the segment.
- **Evidence:** The statements are precise and correct; only the reference is missing. The contract explicitly allows
  basic trigonometric identities.
- **Suggested fix:** One sentence near the Rotations paragraph citing a standard calculus or analysis text for the
  basic properties of sin and cos.

### m5 (minor): the letter `c` changes meaning in Lemma `lg:lem:fan-step`

- **Location:** `sections/lg.tex:519–544`.
- **Issue:** Lemma `lg:lem:trans` warns explicitly "(here c is an arbitrary point, not a centre)". Lemma
  `lg:lem:fan-step` also uses `c` as a generic point and even translates by it (`P = p − c`, …), but has no such
  warning.
- **Evidence:** The Rotations paragraph fixes `c` as the centre whenever `m` is given. No `m` is in scope in
  `lg:lem:fan-step`, so there is no actual ambiguity.
- **Suggested fix:** For clarity, add the same parenthetical as in Lemma `lg:lem:trans`.

## Things I was unsure about

None that affect correctness.

I considered whether Remark (2) after Theorem `lg:thm:nesting` is circular, since it uses the theorem's own conclusion
to show that the hypotheses cannot all hold when `m = 2`. It is not circular, because the theorem is proved
independently of the remark.

I also considered whether the alternative proof of `x ≠ ρ(x)` creates a dependency loop. It does not: Lemma
`lg:lem:lin-orbit` depends only on Lemmas `lg:lem:rot-iter` and `lg:lem:lin-rot`.
