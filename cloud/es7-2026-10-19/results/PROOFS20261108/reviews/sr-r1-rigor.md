# Review of section `sr` (Reduction of symmetric sets to case classes), round 1, lens: rigor

**Verdict: PASS.** No blocker or major finding. Six minor findings (wording, layout and documentation) are listed below.

Files reviewed: `sections/sr.tex` (1056 lines) and `sections/sr.map.tsv` (46 rows), checked against
`SYMLEAN/SymmetricReduction.lean` (all 1059 lines read), the inventory `inventory/SYMLEAN-core.json`,
`SYMLEAN/README.md`, `SYMLEAN/logs/*`, `C2ENC/class_table.md`, `WRITEUP/SYMMETRIC.md`,
`WRITEUP/note/symmetric_es7.tex` (lines 50-110), `AUDIT3/reports/A1_reduction.md`, `H3/MirrorEncoding/Line.lean`,
`LRATCHECK20261105/README.md`, and the repository modules `ErdosSzekeres/{Definitions,Basic,Orientation,
OrientationGeometry}.lean` and `ErdosSzekeres/Suk/{SupportingLines,BaseOrder,BaseChart,TriangleOrder}.lean`.

## 1. Step-by-step check of the proofs

Every proof was read line by line. I checked each step, the direction of each inequality, that each case split is
exhaustive, that each induction is well founded, and that each use of an earlier result meets its hypotheses. Results:

| statement | result |
|---|---|
| Lemma `sr:lem:complex` (a)-(e) | correct; (e) uses (c) and (d) properly |
| Lemma `sr:lem:iterate`, `sr:lem:pigeon` | correct; pigeonhole on the `|S|+1` iterates `f^[k](q)`, `0 ≤ k ≤ |S|` |
| Lemma `sr:lem:minper` (MP1)-(MP4) | correct. (MP3) is proved first and then used in (MP1). In (MP4), `0 < d-j+i < d` holds because `i < j < d` |
| Lemma `sr:lem:orbitFS` (a)-(e) | correct; (d) routed through (MP1), (MP2) and (e) |
| Lemma `sr:lem:orbit-core` | correct. Strong induction on `|S|` with `|S \ O| = |S| - p < |S|` (`p > 0`). Invariance of `S \ O` is proved in both cases `i = 0` (via `f^[p](x) = f(f^[p-1](x))`) and `i ≥ 1`, using injectivity on `S` and `f^[i-1](x), f^[p-1](x) ∈ S`. The union `T' ∪ O` is disjoint |
| Lemma `sr:lem:orbit` (a), (b) | hypotheses of the common form are checked exactly: (MP3) and (e) for (a); `p > 0` and (d) for (b). The remark that injectivity is redundant in (b) is correct (apply `f^[p-1]`) |
| Lemma `sr:lem:crot` (a)-(g) | correct; (d) by induction using (c) and the convention `f^[k+1] = f ∘ f^[k]` |
| Lemma `sr:lem:rot-half` | correct (Euler's formula; checked with sympy) |
| Lemma `sr:lem:refl` (a)-(d) | correct. The real and imaginary residuals `x(u0²+u1²-1)` and `y(u0²+u1²-1)` are exact; the involution follows from `(u ū)² = 1`; the cross-product identity in (d) is exact (sympy) |
| Lemma `sr:lem:toC-iso` | correct |
| Theorem `sr:thm:structure` (a) | **self-contained proof, correct and complete.** Polarization gives inner-product preservation; `v = e ā` with `|v| = 1` and `Re v = 0` gives `e = ±ia`; the expansion `ξ = ⟨ξ,a⟩a + ⟨ξ,e⟩e` holds for both signs; `H(z) = xa + ye`. No linearity or surjectivity is assumed. Each sign and each identity was checked with sympy |
| Theorem `sr:thm:structure` (b) | correct. The case split (R, `a = 1`), (R, `a ≠ 1`), (C) is exhaustive by (a). Pigeonhole is applied to `g` and to `g∘g` with `Invariant` checked. `q̂ - c ≠ 0` comes from choosing `q ≠ ofC(c)`, which needs `|S| ≥ 2`. `a^i ≠ 0` because `|a| = 1`. `t = a b̄ + b = 0`. With `u² = a` (any square root) and `A = ofC(b/2)`, the identity `b/2 + a conj(p̂ - b/2) = a p̂̄ + b` uses `a b̄ = -b` (sympy) |
| Lemma `sr:lem:supports` | correct. `orient(p,q,·)` is affine (sympy); the open half-plane is convex; `conv(s\{p}) ⊆ H` and `p ∉ H` |
| Lemma `sr:lem:concyclic`, Corollary `sr:cor:concyclic` | correct. Both equalities in the display were checked with sympy; `q` matches the Lean witness `![p 0 - (p 1 - c 1), p 1 + (p 0 - c 0)]` |
| Lemma `sr:lem:center` | correct; `q, c, 2c-q` are pairwise distinct and `orient(q,c,2c-q) = 0` (sympy) |
| Definition `sr:def:prim`, Lemma `sr:lem:prim` (P1)-(P6) | correct. In (P5), the `k` distinct powers are all the roots of `X^k - 1`. (P6) uses `exp(w) = 1 ⟺ w ∈ 2πiℤ`, a standard fact that is stated correctly |
| Lemma `sr:lem:rot345` | correct |
| Lemmas `sr:lem:root-cases`, `sr:lem:prime-cases`, `sr:lem:root-cases2` | correct and exhaustive. In `root_cases2` the "only prime factor is 2" branch is handled through `n = 2m'`, then `m' = 1` |
| Lemmas `sr:lem:halfturn-facts`, `sr:lem:case-halfturn` | correct; `|S| ≥ 33`, even, gives `≥ 34 = 17·2` |
| Lemma `sr:lem:rot-erase` | correct; `w ≠ 0` from `w^p = 1`, `p > 0`; the centre is fixed; `S'` is invariant by injectivity |
| Lemma `sr:lem:rot-big` | correct; `normSq(w) = 1` from `t ↦ t^p` strictly increasing on `[0,∞)`; the orbit is concyclic with `p ≥ 7` points |
| Lemma `sr:lem:odd-prime` | correct; `3 | n ≥ 32 ⇒ n ≥ 33`, `5 | n ≥ 32 ⇒ n ≥ 35`; `exp(2πi/p) = w^e` by (P5); `rotAbout = (crot_{c,w})^[e]` |
| Lemma `sr:lem:fourfold` | correct; `w² = -1`; the centre is excluded through the half-turn; minimal period 4 (`d ∈ {1,2,4}`, with 1 and 2 excluded); `8·4 = 32 ≤ |S|` |
| Lemma `sr:lem:mirror` | correct; `|F| ≤ 2`; `M` invariant; `|F| = 0 ⇒ |M| ≥ 34`; `|F| ≥ 1 ⇒ |M| ≥ 31`, even, so `≥ 32`; `T' = T ∪ {x}` has exactly one fixed point |
| Theorems `sr:thm:main`, `sr:thm:variant` | correct; each case meets the hypotheses of the lemma it invokes exactly; in the variant, the contradictions give the existential conclusion |
| Definition `sr:def:exclusion-line`, Lemma `sr:lem:mirror-line`, Remarks `sr:rem:mirror-line`, `sr:rem:redundant` | correct mathematics (`|F| ≤ 2`, `|M|` even, `|F| + |M| = 33 ⇒ |F| = 1`; `3 ∤ 32`, `5 ∤ 34`) |

Nothing is delegated to Lean. Every reference to Lean inside a proof is parenthetical: `pigeon`, the Mathlib route in
Theorem `sr:thm:structure`(a), and the principal square root. The standard facts cited are stated correctly: pigeonhole,
Euler's formula, the root count of `X^k - 1`, `exp(w) = 1 ⟺ w ∈ 2πiℤ`, the existence of complex square roots, and the
convex hull lying in any convex superset.

## 2. Identities checked with sympy

Script: `build/sr_r1rigor_sympy.py`, output `build/sr_r1rigor_sympy.out`: 61 checks, 0 failures. Covered:
- the inner product `Re(z w̄) = x1x2 + y1y2` and the polarization identity;
- the sup-metric example (`cos(2π/3) = -1/2`, `sin(2π/3) = √3/2`, sup distance `√3/2 ≠ 1`);
- `eDist2 = normSq`, `crot_comp`, `crot_eq_self` and `eDist2_crot_center`;
- `rotAbout = crot` and `halfTurn = crot(-1)`;
- every expansion in Lemma `refl` (a), checked both as written and modulo `u0²+u1² = 1` by polynomial reduction;
- the involution (coordinates and complex form);
- the fixed-point equations and the Lean linear combination;
- that `a + tu` is fixed, and that `u = 0` gives the half-turn;
- the identity `(v×w)|u|² = (w·u)(v×u) - (v·u)(w×u)`;
- every step of Theorem `structure` (a) and (b): `⟨ξ,ia⟩ = Re(-iξā)`, the decomposition for `e = ±ia`, `c = b/(1-a)`, `g∘g` and the reflection formula;
- both concyclic equalities, the affinity of `orient(p,q,·)` and `orient(q,c,2c-q) = 0`;
- the powers of `exp(2πi/n)` for `n = 3, 4, 5`;
- the size arithmetic (33, 35, 34, 32, 36; `32 mod 3`, `34 mod 5`).

## 3. Records, logs and labels checked

- SHA-256 prefixes: all seven stated values match (`6d5ec90a4215`, `7bf809cbdc77`, `2425500eefd1`, `13667aa2d3dc`,
  `f67955ac7091`, `c7db9bbbb65e`, `6a8e12677685`). Lines 1-1059 of `SymmetricReductionAxioms.lean` and of
  `review/ReviewSanity.lean` are byte-identical to the main file (cmp). Lines 1-1058 of `AffineReduction.lean` are
  identical too. `runs.tsv` hashes equal the current files, so the logs belong to these files.
- `logs/SymmetricReduction.out` is empty and exits 0. `SymmetricReductionAxioms.out` lists exactly the three standard
  axioms for both theorems. `ReviewSanity.out` lists the same three for `mirrorOneAxis33_iff_exclusionLine`, which is
  proved from the bridge lemma at `review/ReviewSanity.lean:1630`.
- No `decide`, `native_decide`, `axiom`, `sorry`, `admit` or `ofReduceBool` occurs in the main file or in the whole
  repository import closure (the five listed modules plus `Suk/BaseOrder`, `Suk/BaseChart` and `Suk/TriangleOrder`).
  The only hit is the word "axiom" in a docstring at `ErdosSzekeres/Definitions.lean:30`.
- All 72 declarations of the file are listed in the Coverage paragraph. Every `\leanref` line number is exact,
  including `ErdosSzekeres/Suk/SupportingLines.lean:28`, `ErdosSzekeres/Basic.lean:31`,
  `H3/MirrorEncoding/Line.lean:18` and `:94`, and `ReviewSanity.lean:1593` and `:1629`.
- The map has 46 rows, matching the 46 statement environments one to one. Kinds match, and the Lean names and lines in
  the map equal those in the heads (script check).
- All eight export labels are defined on the named statements. Refs go only to `sr:`, `fd:` and the allowed export
  labels `mb:thm:classes`, `mb:thm:main3` and `ar:thm:main`. There are no duplicate labels, no machine paths and no
  tool names.
- Remark `sr:rem:records` agrees with `C2ENC/class_table.md` and `SYMLEAN/README.md` §5, §6 and §9: the 120 hexagonal
  hulls, 116,883 pieces, 2,120 re-solved in `C3SPOT`, the perturbation lemma for `Threefold33` and `Fivefold35` only,
  `C4CUT`, and the credit to arXiv:2506.00224 §6.2. `mirrorOneAxis33_proved` and `mirrorNoAxis34_proved` exist
  (`SYMLEAN/mirror`, lines 4274 and 4282), with standard axioms in `SYMLEAN/mirror/axioms.out`. Per
  `LRATCHECK20261105/README.md`, every class certificate cited here is also accepted by cake_lpr, so the wording
  "accepted by both checkers" is not affected by the lrat-check defect.
- Compile check: `build/sr_rigorcheck_wrapper.tex`, two `pdflatex` runs, exit 0. The only undefined references are the
  allowed `fd:`, `mb:` and `ar:` labels. There are 39 overfull boxes (finding m3).

## 4. Findings

### m1 (minor): Remark `sr:rem:variant` mischaracterizes Corollary 3 of `WRITEUP/SYMMETRIC.md`
- **Location:** `sections/sr.tex` lines 957-962.
- **Issue:** The remark contrasts the Lean theorem ("per-symmetry") with Corollary 3, which it says "speaks about the
  whole symmetry group". In fact Corollary 3 (`WRITEUP/SYMMETRIC.md:46-49`) says "every symmetry of a 7-gon-free
  set ... is a half-turn about a point outside the set". That is the same per-symmetry, universally quantified form as
  the Lean theorem. The real differences are two. First, "symmetry" there includes affine bijections
  (`SYMMETRIC.md:8-9`). Second, Corollary 3 assumes Theorems 1, 2, 5 and `C4CUT` as established, whereas Lean takes
  the classes as `Prop` hypotheses. The group statement ("symmetry group exactly the half-turn group") is in the note's
  `cor:only` (`WRITEUP/note/symmetric_es7.tex`, lines 95-99), not in `SYMMETRIC.md`.
- **Fix:** For example: "It is Corollary 3 of `WRITEUP/SYMMETRIC.md` restricted to Euclidean isometries; that
  corollary also covers affine bijections. A group form ... is Lean-checked in the review file ...".

### m2 (minor): the last sentence of Remark `sr:rem:redundant` is imprecise
- **Location:** line 1012.
- **Issue:** "Such hypotheses only make a class weaker, that is, easier to supply." For the hypotheses listed in the
  first three bullets, which are implied by the others, the class is logically equivalent to the version without them.
  They make it neither weaker nor stronger. The sentence is true only of extra hypotheses in general, such as the
  non-redundant one in `MirrorNoAxis34`.
- **Fix:** For example: "A redundant hypothesis leaves a class equivalent; an extra hypothesis can only make a class
  weaker, never stronger."

### m3 (minor): 39 overfull boxes, up to about 151 pt
- **Location:** mostly statement heads with long `\leanref` lists. Examples: lines 255-257 (Lemma `sr:lem:iterate`,
  151.5 pt), 422-424 (`sr:lem:rot-half`, 151.5 pt), 105-108 (`sr:def:iso`, 135.8 pt), 369-371 (`sr:lem:orbit`,
  130.5 pt), 167-169 (`sr:def:maps`, up to 133.6 pt), 739-743 (120.8 pt), 701-704 (116.3 pt).
- **Issue:** The text runs into and past the right margin in the PDF. The amsthm head is set in an unbreakable box, so
  long names cannot wrap. This is layout only; the compile exits 0.
- **Fix:** Shorten the heads, for example by moving some `\leanref` entries into the first sentence of the statement
  or putting at most one or two names in a head. Alternatively, ask for a preamble-level change.

### m4 (minor): two informal geometric claims cite lemmas that do not state them
- **Location:** lines 187-188 and 215-217.
- **Issue:** (i) "For `u0²+u1²=1`, `reflLine_{a,u}` is the reflection in the line `a+ℝu` (Lemma `sr:lem:refl`)":
  Lemma `refl` gives the complex form, the involution and the fixed-point equation, but never states that the map is
  the reflection in that line. (ii) "fixed points lie on it by Lemma `refl`(c) (since `u≠0`)": the one-line step from
  `(p-a)×u = 0` and `u ≠ 0` to `p ∈ a+ℝu` is not written. Neither claim is used in any proof, so correctness is
  unaffected.
- **Fix:** Add one sentence, for example: "In complex form `z ↦ â + û² conj(z-â)` fixes `a+tu` and sends `a+itu` to
  `a-itu`, so it is the reflection in `a+ℝu`." For (ii): "if `u0 ≠ 0` put `t = (p0-a0)/u0`; then `p1-a1 = t u1`;
  symmetrically if `u1 ≠ 0`."

### m5 (minor): the Coverage paragraph understates where `ReviewSanity.lean` is used
- **Location:** lines 1054-1056.
- **Issue:** The paragraph says the review files are "mentioned only in Remarks `sr:rem:sup`, `sr:rem:variant` and
  `sr:rem:mirror-line`". But `SYMLEAN/review/ReviewSanity.lean` and its log are also cited in the paragraph "Axioms and
  rigor" (lines 54-57). There they are the axioms evidence for `mirrorOneAxis33_of_exclusionLine`, which the printed
  theorems of the main file do not use.
- **Fix:** Add "and, for `ReviewSanity.lean`, the paragraph Axioms and rigor".

### m6 (minor): the "no axiom, no decide" claim covers modules whose hashes are not pinned
- **Location:** lines 36-43 and 58-61.
- **Issue:** Line 58 says the imported repository modules contain no `axiom`, `decide` or `native_decide`. The import
  closure includes `ErdosSzekeres/Suk/BaseOrder.lean`, `BaseChart.lean` and `TriangleOrder.lean`, which
  `Suk/SupportingLines.lean` imports. Their hashes are not listed among the sources. I checked that the claim is true
  for all eight modules. The pinned list is labelled "used here", which is accurate, but a reader cannot pin the full
  closure.
- **Fix:** Add one clause naming the three transitively imported `Suk` modules (with hashes) as part of the closure the
  claim covers.

## 5. Things checked and found correct that a reader might question

- Theorem `sr:thm:structure`(a) replaces the Mathlib route (Mazur-Ulam type plus `linear_isometry_complex`) with an
  inner-product argument. The argument needs neither continuity nor surjectivity, and it is complete.
- Lemma `sr:lem:center` needs only `|S| ≥ 2`, as in Lean. The note's version needed `|S| ≥ 3`.
- `case_rot_big` and `convexPosition_of_concyclic` use no general position; the section says so.
- In `root_cases` the least prime factor is used, and every even order goes to the half-turn; the section says so.
- In Theorem `sr:thm:structure`(b), case (C), any square root of `a` works. The section notes that Lean takes the
  principal value.
- The rigor labels are correct. The classes are hypotheses in every statement that uses them. Remark `sr:rem:records`
  names the supplying records with labels: computer-assisted for `HalfTurn34`, `Threefold33`, `Fivefold35` and
  `Fourfold32`; Lean-checked from the vendored Baek formalization for the mirror classes. Remark `sr:rem:main` states
  the conditional status. The docstring wording "Corollary 3 exactly as written" is not repeated.
