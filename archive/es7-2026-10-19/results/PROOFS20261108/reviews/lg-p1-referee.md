# lg, polish round 1: independent referee report

Section: `sections/lg.tex` (940 lines) and `sections/lg.map.tsv` (31 rows). Lean source: `LAYERLEAN/LayerLemma.lean`
(RES-relative; SHA-256 `afb8542dceb0…`, 1148 lines, recomputed). Paths below are relative to STAGE (`sections/`,
`build/`, `reviews/`), to RES (`LAYERLEAN/…`, `LEANEXT/…`, `WRITEUP/…`) or to the repository root (`ErdosSzekeres/…`).

**Verdict: PASS.** I found no blocker and no major finding. All 27 in-scope declarations are stated faithfully, every
proof step holds, and every cross-reference says what the section claims. There is one minor finding (F1), about rigor
vocabulary in the paragraph *Encoders*. I formed this view before reading the earlier reports, then compared it with
them (see the end).

## What I checked, and how

### 1. Every statement against its Lean declaration (27 of 27)

I read lines 1–1148 of `LayerLemma.lean` (definitions at 48, 105, 111, 298, 374; the scope 465–1032; 1037). For each
headed statement I compared hypotheses, binder order, conclusion, natural-number subtraction, casts, Finset vs Set and
maps-into vs equality. All 27 match:

- **Rotations and the regular polygon.** `rotAbout_iterate` (465): the cast of `j` is stated. `orient_rotAbout` (472)
  and `trig_layer` (480). `orient_regular_nonneg` (488): `0 < m`, `j ≤ m`, no `x ≠ c`. `lin` (625) and
  `lin_rotAbout` (794): `c - p` is coordinatewise. `lin_orbit_pos` (801): `p ≠ c`, `0 < m`, `0 < j`, `j < m`.
  `orient_next_prev_pos` (830): `3 ≤ m` and `m - 1` as a natural number. The section says the cast is legitimate.
- **Convexity.** `convex_orient_nonneg` (516) is a Set. `dist2` (999). `convex_disk` (1002): any real `R`.
- **Layers.**
  - `strict_nesting` (529): `2 ≤ m`, `K ≤ 2m`, `c ∉ S`, Invariant, `¬HasConvexNGon K S`, GeneralPosition, `n < n'`.
  - `centre_not_mem_of_even` (582): `0 < m`, `Even m`, `p ∈ S`, `p ≠ c`. No `c ∉ S` and no K-freeness.
  - `dist2_le_of_later` (1012): `n ≤ n'`, no general position, weak inequality.
- **Fans and chains.**
  - The three statements `orient_trans_halfplane` (629), `fan_step` (641) and `orient_eq_lin` (653): every hypothesis
    is in the Lean order and has the Lean argument order.
  - `fan_positive` (658): (H), (F) and (T) with the exact index bounds. `fanPt` (694): `Fin (n+1)`, `q(i-1)` only for
    `i ≠ 0`.
  - `hasConvexNGon_of_fan` (700): `3 ≤ n`, conclusion `HasConvexNGon (n+1) S`.
  - `lin_pos_of_peel` (864): `3 ≤ m`, `y ∈ peel S i`, `y ≠ p`.
  - `chain_clauses_sound` (914): `3 ≤ m`, `4 ≤ K`, `K ≤ 2m`, the bounds of (C1)–(C4) in terms of `K - 1`, and
    conclusion `False`.
- **Polar rules.** `polar` (932), `orient_polar` (935), `orient_polar_centre_inside` (943) with its six angle bounds,
  `sin_add_lt` (956), and `orient_polar_halfplane` (974) with weak radius bounds and no `0 < rb`.

The map has 31 rows, in the same order as the 31 non-remark statement environments of the tex. Its 27 Lean line numbers
match the file, checked by script. There are exactly 27 declarations in lines 465–1032, 23 theorems and 4 definitions;
I listed them by grep.

### 2. Every proof, step by step

Each step meets the hypotheses of what it uses.

- Lemma `lg:lem:layer` (a)–(d) through (L1)–(L4).
- The induction in `lg:lem:rot-iter` uses `f^{j+1} = f∘f^j` and `(j+1:ℝ) = j+1`.
- In `lg:cor:period`, `(m:ℝ) ≠ 0`.
- `lg:lem:regular` splits into `j = 0` and `1 ≤ j ≤ m`; the ranges `0 < t ≤ π`, `0 ≤ jt ≤ π` and `0 ≤ (j-1)t ≤ π` are
  right.
- In `lg:lem:next-prev`: `(m-1)t = π - t`, and for `m ≥ 3`, `t ∈ (0, π/3]`, `π - t ∈ [2π/3, π)` and
  `π - 2t ∈ [π/3, π)`.
- `lg:thm:nesting`: weak side by convexity; `x ≠ ρx` through `lin_orbit_pos`, `j = 1`; `y ∉ L` through (d); then
  general position.
- `lg:lem:centre`: `m = k + k`, `ρ^k = rotAbout(c, π)`, `q = 2c - p`, and the three distinctness cases.
- `lg:thm:radius`: the layer lies in the disk, and the disk is convex.
- `lg:lem:fan-pos`:
  - (a) the induction on `k`, with the half-plane hypothesis at `t ∈ {j, k, k+1}`;
  - (b₀) the five `fan_step` premises at `(p, q_i, q_s, q_{s+1}, q_{s+2})`;
  - (b) the induction with `w' = J(q_i - p)`.
- `lg:thm:fan`: in Step 1 the shifted indices satisfy `< n`; in Step 2 a third index exists since `n+1 ≥ 4`.
- `lg:lem:halfplane`, both cases:
  - (e1) and (e2) through `strict_nesting` at `(i, i+1)`;
  - `ρ(p') = ρ^m(p) = p` through `lg:cor:period`;
  - (w2) uses `0 < m-1 < m`.
- `lg:thm:chain`: `n = K-1 ≥ 3` and `(K-1)+1 = K`.
- Rule B: `x, y < π` follows from `x + y < π`.

There is no circularity. Every result is used only after it is proved, and the order of the tex is a valid
dependency order.

### 3. Every identity, by sympy 1.13.3

Script `build/lg_p1_referee_sympy.py`, 51 checks, all residuals 0:

- (lg:eq:J), `det(X,Y) = ⟨JX,Y⟩`, `R_θX = cosθ X + sinθ JX`, and (O1), (O2), (O4);
- rotfacts (a)–(d), including the matrix product `R_α R_β = R_{α+β}`;
- `orient_rotAbout`, `trig_layer` and `lin_rotAbout`;
- the Cramer identity in both coordinates, its two corollaries, and the 3×3 cofactor expansion used in its proof;
- the key identities (lg:eq:trans), (lg:eq:fanstep) and (lg:eq:key), for arbitrary points, with the six `fan_step`
  translations to `det(·,·)` and `orient(p',p,y) = det(E,C)`;
- `orient_eq_lin`;
- `orient_polar`, with the `det(A,B) + det(B,D) + det(D,A)` step and `det(r e(φ), s e(ψ)) = rs sin(ψ−φ)`;
- the rule-B decomposition and the `convex_disk` identity (`u + v = 1`);
- `rotAbout(c,π)(p) = 2c − p` and `orient(p, c, 2c−p) = 0`;
- `(m−1)t = π − t`;
- the value formula of the remark after `lg:lem:regular`.

A second script, `build/lg_p1_referee_sympy_poly.py`, confirms that `orient_rotAbout` and `lin_rotAbout` are pure
polynomial identities in free symbols for `cos` and `sin`. So the claim "no relation between cos and sin is used" is
true.

### 4. Cross-references

The fd labels used are `fd:def:{point,orient,gp,cp,ngon,inv,rot}` and `fd:lem:{orient,collinear,mono,pos-triples}`. The
ll labels used are `ll:def:{hv,peel}`, `ll:lem:{hv,antitone,inv-peel,minperiod}` and `ll:thm:{core-rot,card-peel}`. All
are in the contract's export lists. I opened each one in `sections/fd.tex` or `sections/ll.tex`, and each says what lg
claims:

- (L1) = `ll:lem:hv`(c), `S ⊆ conv(hv S)`.
- (L2) = `ll:lem:antitone`.
- (L3) = `ll:lem:inv-peel`, with `0 < m` and `c ∉ S`.
- (L4) = `ll:thm:core-rot`, with `0 < m`, `K ≤ 2m`, `c ∉ S`, invariance and K-freeness.
- `fd:lem:orient`(b) is cyclic invariance.
- `fd:lem:collinear`(b) is general position iff `orient ≠ 0`.
- `fd:lem:mono`(c) is upward monotonicity of `HasConvexNGon`.
- `fd:lem:pos-triples` is the Lean statement, with a linear order, injectivity and `|s| ≥ 4`.

The environment words are consistent with the label kinds: every "Lemma\ref" points to a lemma, and so on. All lg
labels that are `\ref`d are defined in lg. All 13 lg export labels sit on the named declarations. The contract's
"(with trig_layer)" for `lg:lem:regular` is handled by the separate `lg:lem:trig`; the polish fix log adjudicated this
(declined to add a second `\leanref`), and I do not re-raise it.

### 5. Records, hashes and logs

I recomputed every file fact with `shasum`, `wc`, `diff` and `grep`. All are correct:

- **SHA-256 prefixes.** All ten match: LayerLemma.lean, README.md, Definitions, Orientation, OrientationGeometry,
  OrientationClique, the two `axioms.log` files and `out.txt` (nine distinct files). The tenth, the review report's
  `afb8542d…` for the reviewed file, is the LayerLemma.lean hash again.
- **Line numbers.** `orient` is at :9 and `orient_cycle` at :15. Also :66, OrientationClique :9, `Basic.lean:20`
  (`HasConvexNGon.mono`), `orbitFS` :48, `rotAbout_eq_crot` :302, `crot_iterate` :267, `peel_antitone` :460, and
  `card_peel` :1037 with its docstring at :1036.
- **`LAYERLEAN/logs/axioms.log`.** It prints 16 of the 23 scope theorems, and the 7 missing are exactly the ones named.
- **`LEANEXT/review/axioms.log`.** It prints 59 names, equal as a set to the 66 theorem declarations minus the 7
  `@[simp]` ones (checked by set difference). All 23 scope theorems use `[propext, Classical.choice, Quot.sound]`.
- **`out.txt`.** It covers 11 scope theorems.
- **REPORT.md.** It says "All 59 theorem declarations", has build exit 0, and its findings F2 and F5 read as cited.
- **`build.log`.** It has exit 0, 0 message lines and no hash.
- **The re-check file.** `LayerLemmaAxioms.lean`: `head -1148` is identical to LayerLemma.lean.
- **Forbidden words.** There is no `sorry`, `admit`, `axiom` or `native_decide` in the file.
- **Toolchain and target.** The toolchain is v4.24.0 and Mathlib is pinned at `f897ebcf72…`. `defaultTargets` is
  `["ErdosSzekeres"]` only, so the file is not in the default target.
- **README.** "What is not in Lean" and the status "(written proof, review and tests)" are as quoted.
- **The k = 8 note.** In `WRITEUP/note/k8_soundness.tex`, (G1) is the code-reading gap, it records the ENCBLEAN second
  route, and (E1) is "evidence from running compiled code, not a Lean theorem".
- **Mathlib names.** `Real.sin_pos_of_pos_of_lt_pi`, `Real.cos_le_one` and `Real.cos_eq_one_iff` exist at the pinned
  revision.
- **Main-library list.** Grepping lines 465–1032 for the main-library declaration names gives exactly the ones listed
  under *Sources*; the other hits are words in comments.

### 6. Coverage claims

- **The eight copies.** I diffed lines 11–1147 of LayerLemma.lean against the matching block of each of the eight
  files: all are identical, with start lines 19/19/11/11/11/11/19/11.
- **No further copy.** A grep for `theorem lin_pos_of_peel` over the whole checkout finds exactly these nine files
  (`.lake` excluded), and no non-`.lean` file has it.
- **Same short names elsewhere.**
  - `ErdosSzekeres.OrbitConsistency` (two files): `rotAbout_iterate` and `polar`.
  - `ErdosSzekeres.SymReduction.Review`: `orient_rotAbout`.
  - `PhaseClassification`: the five names the section lists.
  - `C7`: `orient_polar`.
- **pc.** `sections/pc.tex` does treat the PhaseClassification five.

### 7. Compile and hygiene

`build/lg_refp1_wrapper.tex` (contract wrapper, my own copy) was compiled with two runs of
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:

- both runs exit 0, with 12 pages;
- there are 0 overfull boxes, and the one underfull box is a page-level `\vbox`;
- the undefined references are only `fd:` and `ll:` export labels;
- there is no "Missing" and no error.

The tex and the tsv contain no machine path and no tool name. The section has no `\newcommand`, `\def` or
`\usepackage`. The tsv has 5 columns on every row.

## Findings

### F1 (minor): rigor vocabulary and an incomplete trust picture in the paragraph *Encoders*

- **Location.** `sections/lg.tex:95–97`.
- **Text.** "For encoder B at m=6 that note also records a second route on which the step is Lean-checked for a Lean
  definition of the formula (ENCBLEAN); on that route, that the texts printed from this definition are the
  **certified files** is trust item (E1), evidence from running compiled code and not a Lean theorem."
- **What is wrong.**
  1. "Certified" is one of the words the binding rules reserve. The task says never write "verified", "certified" or
     "proved" beyond *Lean-checked* or *written proof*, and never present a CNF verdict as proved. Calling the CNF files
     "the certified files" implicitly asserts their certification, that is, the cake_lpr verdicts. The k = 8 note's
     trust item (E2) lists exactly those verdicts as *trusted, not Lean-checked*. The phrase is copied from the note's
     (E1) ("the certified cube files"); rule 8 of the contract says not to repeat such wording.
  2. The sentence names only (E1). On that route the note assumes the 64 cake_lpr verdicts and all of (E1)–(E6),
     including (E3), cake_lpr's parser, and (E4), the Lean compiler and runtime for the printer. A reader could take
     (E1) to be the only thing trusted there.
  3. Not wrong, but it could be stated: (G1) also trusts the Python interpreter to run the generators as written.

  None of this affects any statement or proof of the section.
- **Fix.** Replace the sentence after "(ENCBLEAN);" with, for example:
  "on that route, that the texts printed from this definition are the CNF files on which the recorded cake_lpr
  verdicts were obtained is trust item (E1) of that note, evidence from running compiled code and not a Lean theorem;
  the route also assumes those 64 verdicts and the trust items (E2)–(E6)."
  Optionally, after "by reading the code", add "(with the Python interpreter trusted to run the programs as written)".

## Attacks that did not succeed (checked, not findings)

- **Remark (2) after `lg:thm:nesting`** (m = 2 is vacuous). It is sound: `y` lies in the segment from `x` to `ρx` and
  outside `{x, ρx}`, and `x ≠ ρx`, so general position fails. The segment-convexity argument is complete.
- **The remark after `lg:lem:centre`** (`S = {c}`) is correct.
- **The refinement "value 0 exactly for j ∈ {1, m}"** after `lg:lem:regular` holds for `x ≠ c` and `m ≥ 2`. It fails
  for `m = 1`, which the remark excludes.
- **Natural-number subtraction.** It appears in `m - 1` (with `m ≥ 3`), `K - 1` (with `K ≥ 4`) and `i - 1`, `j - 1`,
  `k - 1` in `fanPt` and Step 1 (with indices `≥ 1`). Every use is an ordinary difference, as the section says.
- **The convention 2π/m with m = 0.** Every statement containing `2π/m` assumes `m ≥ 1`. I checked all ten statements
  and written steps where it occurs.
- **(S1) and (S2), the trigonometric facts.** The section uses no other trigonometric fact than those listed in
  "Sine and cosine". This includes `sin(α−δ) = sin(α−δ+2π)` (periodicity) and `sin(−z) = −sin z` (oddness).
- **The claim in *Rigor* that every difference from the Lean proof is stated.** I compared each written proof with the
  Lean proof. The remaining differences are either automatic-tactic steps derived by hand, which that paragraph covers,
  or are flagged in a remark or parenthetical:
  - `rotAbout_iterate`;
  - `x ≠ ρx`;
  - `ρ(p') = p`;
  - the Cramer instances;
  - fan Step 2;
  - the `HasConvexNGon.mono` use in the chain proof;
  - `orient_polar`.

  One difference is a different but equivalent standard fact: `lin_orbit_pos` and `sin_add_lt` use (S2) where Lean
  uses `cos_eq_one_iff_of_lt_of_lt`. It is not a structural difference.
- **Hypotheses presented as proved; computations presented as hand proofs.** There are none. No statement of this
  scope takes an unproved proposition or a SAT verdict as a hypothesis, and none is a finite computation.

## Comparison with the earlier reports (read after forming the view above)

The round-1 reports (`reviews/lg-r1-{fidelity,rigor,adversarial,claims}.md`) and the polish fix log
(`reviews/lg-polish-r1-fix.md`) raised only minor points, and the fix log resolved or adjudicated all of them. I
re-checked the text added in that round:

- the paragraphs *Encoders* and *Sine and cosine*;
- the new segment argument;
- the eight-copy list;
- the other-namespaces item;
- the reworded *Sources* and *Axioms* paragraphs.

All of it is accurate, apart from F1. The F1 wording ("certified files", only (E1) named) was introduced in the polish
round, so the earlier reports could not have seen it.
