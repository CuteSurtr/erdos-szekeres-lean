# Review sr, round 1, lens: adversarial

Section: `sections/sr.tex` (Reduction of symmetric sets to case classes), map `sections/sr.map.tsv`.
Sources compared: `SYMLEAN/SymmetricReduction.lean` (all 72 declarations), `SYMLEAN/README.md`, `SYMLEAN/logs/*`,
`ErdosSzekeres/{Definitions,Basic,Orientation,OrientationGeometry,Suk/SupportingLines}.lean`, the inventory
`inventory/SYMLEAN-core.json`, `WRITEUP/note/symmetric_es7.tex` (lines 50-110), `WRITEUP/SYMMETRIC.md`,
`WRITEUP/MIRROR.md`, `C2ENC/class_table.md`, `C2FINAL/README.md`, `C3FINAL/README.md`, `C3SPOT/README.md`,
`C4CUT/README.md`, `H3/README.md`, `H3/MirrorEncoding/Line.lean`, `V2-L/README.md`, `AUDIT3/reports/A1_reduction.md`.
(Paths relative to `cloud/es7-2026-10-19/results` or to the repository root.)

**Verdict: pass.** No blocker and no major finding. Seven minor findings below.

## What was checked, and how

1. **Fidelity of every Lean-tagged statement.** Each statement head was compared with its declaration in
   `SymmetricReduction.lean`, hypothesis by hypothesis (order, `Finset` vs set, maps-into `Invariant`, `0 < p`,
   `p.Prime`, `7 ≤ p`, `w ≠ 1`, `normSq w = 1`, `1 < S.card` vs `2 ≤ S.card`, `33 ≤ S.card`, exact class sizes
   34/33/35/33/34/32, `c ∉ S`, `u 0 ^ 2 + u 1 ^ 2 = 1`, the fixed-point formulations, the angles `2 * Real.pi / n`,
   `k * p` vs `2k`, the conclusion `∃ c, g = halfTurn c ∧ c ∉ S ∧ 2 ∣ S.card ∧ 34 ≤ S.card`). The six classes were also
   compared with the fully qualified `#print` output in `SYMLEAN/logs/ReviewSanity.out`, and the two theorems with the
   `#check` output in `SYMLEAN/logs/AffineReductionAxioms.out`/`ReviewSanity.out`. No mismatch.
2. **References.** All 73 `\leanref` file:line pairs and all rows of the map were checked by script against the
   sources: every line holds the named declaration. Prose references `ErdosSzekeres/Basic.lean:31`,
   `H3/MirrorEncoding/Line.lean:18` and `:94`, `SYMLEAN/review/ReviewSanity.lean:1593` and `:1629`,
   `SYMLEAN/review/VariantChecks.lean` (`group_form`, line 1168) are correct. All 72 declarations of the file appear in a
   statement head and in the Coverage list.
3. **Sources and rigor paragraph.** SHA-256 prefixes of the six named Lean files recomputed: all match
   (`6d5ec90a4215`, `7bf809cbdc77`, `2425500eefd1`, `13667aa2d3dc`, `f67955ac7091`, `c7db9bbbb65e`, `6a8e12677685`).
   Byte identity checked with `cmp`: `SymmetricReductionAxioms.lean` lines 1-1059, `review/ReviewSanity.lean` and
   `review/VariantChecks.lean` lines 1-1059 equal the main file; `AffineReduction.lean` agrees on lines 1-1058 (line
   1059 differs), as the Coverage paragraph says. `logs/SymmetricReduction.out` is empty and `runs.tsv` shows exit 0;
   `SymmetricReductionAxioms.out` lists exactly `[propext, Classical.choice, Quot.sound]` for both theorems. The
   transitive import closure inside the repository (`Definitions`, `Basic`, `Orientation`, `OrientationGeometry`,
   `Suk/TriangleOrder`, `Suk/BaseChart`, `Suk/BaseOrder`, `Suk/SupportingLines`) and the main file contain no
   `axiom` declaration (only a docstring mentions the word), no `sorry`, `admit`, `decide`, `native_decide`,
   `ofReduceBool`. `IsEucIsometry.injective` is indeed unused.
4. **Identities (symbolic algebra).** Checked with sympy: `toC_reflLine` (difference is `(p−a)(|u|²−1)` componentwise),
   `cross_of_reflLine_fixed` (cross = −(u1/2)e0 + (u0/2)e1), the identity of `orient_eq_zero_of_cross`,
   `reflLine` with `u = 0` is the half-turn about `a`, the tangent identity of the concyclic lemma (both equalities),
   `orient(q, c, 2c − q) = 0`, `rotAbout = crot(exp(iθ))`, and the orientation-reversing case of the structure
   theorem (`b/2 + a·conj(z − b/2) = a·conj(z) + b` given `a·conj(b) = −b`). Numerical value of the sup-metric example
   (√3/2) checked.
5. **Compile check.** Own wrapper `build/sr_r1adv_wrapper.tex`, two `nice -n 15 pdflatex` runs, exit 0 both times.
   Undefined references only to `fd:`, `mb:thm:classes`, `mb:thm:main3`, `ar:thm:main` (all allowed and all defined in
   their sections). No duplicate labels, all labels prefixed `sr:`, all 8 export labels defined on the right
   statements, map rows match the 46 statement environments one to one. No machine path, no tool name.

## Attacks on the main statements (all survive)

- **Classes (Definition sr:def:classes).** Verbatim, including exact sizes and every side condition. The note that the
  fixed points of `reflLine` are exactly the mirror points for unit `u` is correct (uses `u ≠ 0`).
- **Orbit selection (sr:lem:orbit, via the written core sr:lem:orbit-core).** Attacked with `S = ∅` (`p ∣ 0`, `kp ≤ 0`
  forces `T = ∅`), `k = 0`, `kp = |S|`, `p = 1`, the wrap-around case `i = 0` of the injectivity step (uses
  `f^[p](x) = x` and `p − 1 < p`, no underflow since `p ≥ 1`), and `d = 0` in (MP1)/(MP4). The induction hypothesis
  is applied to `S \ O` with all pointwise hypotheses inherited. The redundancy remark on injectivity is correct.
- **Isometries (sr:thm:structure).** (a) The self-contained proof is valid: polarization gives preservation of the
  real inner product for `H = G − G(0)`; `a = H(1)`, `e = H(i)` are orthonormal, `e·ā` has modulus 1 and real part 0,
  so `e = ±ia`; the orthonormal expansion gives `H(z) = xa + ye`. No continuity or surjectivity is used. (b) Tested on
  `|S| = 2` (swap reflection, half-turn about the midpoint, reflection fixing both points, rotations about one point):
  the conclusion holds. Translation exclusion needs only `S ≠ ∅`; the rotation case uses a point `q ≠ ofC c`, which
  needs `|S| ≥ 2`; the orientation-reversing case does not need `g ≠ id`, as stated. Glide reflections are excluded
  by pigeonhole on `g∘g`.
- **Concyclic (sr:lem:concyclic) and supports (sr:lem:supports).** `r < 0` (empty set), `r = 0` (at most one point),
  non-general-position inputs (e.g. many points on a circle with collinear triples: impossible, but the lemma does not
  need it), `s = {p}` (empty hull): all fine.
- **Centre lemma (sr:lem:center).** With `|S| = 2` and `c ∈ S` the invariance already forces a third point; the proof
  finds three distinct collinear points. Only `|S| ≥ 2` is needed, as in Lean.
- **Roots of unity.** Orders 2, 4, 6, 8, 12, 9, 15, 25 run through `root_cases` and `root_cases2`; (P1)-(P6) proofs
  are correct (with the notational caveat of finding 4).
- **Case lemmas.** Size arithmetic: `3 ∣ n ≥ 32 ⇒ n ≥ 33`, `5 ∣ n ≥ 32 ⇒ n ≥ 35`, even `n ≥ 33 ⇒ n ≥ 34`, mirror
  `|F| ≤ 2` and `|M|` even give 17 pairs or 16 pairs plus one axis point; the truncated subtraction `|S| − 1` is
  harmless since `|S| ≥ 33`. Odd prime with the centre in `S`: handled by `rot_erase_facts`. Fourfold: `d ∣ 4`
  excludes `d = 0`; `d = 1, 2` force the centre. `p ≥ 7` needs no general position, and the lemma correctly does not
  assume it.
- **Main theorem and variant (sr:thm:main, sr:thm:variant).** Every branch of `isometry_structure`, `root_cases`,
  `root_cases2` is handled; invariance under `crot c (a^k)` is derived for every `k`; `g = halfTurn (ofC c)` is an
  equality of maps of the plane. The status remarks keep the five (resp. five) classes as hypotheses and do not
  present the theorems as unconditional.
- **Bridge (sr:lem:mirror-line) and Remark sr:rem:redundant.** Correct; `3 ∤ 32`, `5 ∤ 34`, `|F|` odd and `≤ 2` gives
  `|F| = 1` for 33 points.

## Findings

### F1 (minor) Remark sr:rem:variant mischaracterizes Corollary 3 of `WRITEUP/SYMMETRIC.md`

Location: `sr.tex` lines 958-960.
The remark says that Corollary 3 of `WRITEUP/SYMMETRIC.md` "speaks about the whole symmetry group and also about
affine symmetries". Corollary 3 (`WRITEUP/SYMMETRIC.md:46-49`) is itself per symmetry: "every symmetry of a 7-gon-free
set of at least 33 points ... is a half-turn about a point outside the set". The group form ("symmetry group exactly
the half-turn group") is Corollary `cor:only` of `WRITEUP/note/symmetric_es7.tex:95-104`, which is also what the
inventory risk item refers to. The real difference between the Lean theorem (universally quantified over `g`) and
Corollary 3 is only the affine symmetries.
Suggested fix: "It is the isometry case of Corollary 3 of `WRITEUP/SYMMETRIC.md`, whose symmetries also include affine
bijections; the group form of Corollary `cor:only` of the note is the review theorem `group_form`."

### F2 (minor) Provenance of the H3 chain in Remarks sr:rem:mirror-line and sr:rem:records

Location: `sr.tex` lines 225-227, 245-246, 983-988.
- The remark says that `Mir.MirrorExclusionLine` "is derived [in H3] from hypotheses saying that certain CNF formulas
  are unsatisfiable (`Mir.mirrorExclusionLine_of_unsat`, `Mir.mirrorExclusionLine_of_cubes`), whose verdicts were
  recorded outside Lean." `H3/README.md` says that in H3 sub-case (ii) is open and that there is "no claim about the
  whole mirror class"; the hypothesis `¬DimacsSatisfiable (interiorCnf 33 7)` of `mirrorExclusionLine_of_unsat` has
  no recorded verdict as such. The conditional whole-class theorem whose hypotheses all carry recorded cake_lpr
  verdicts is `V2L.mirrorExclusionLine_final` (`V2-L/README.md` §9.1 and §9.6: 1 + 121 + 1,198 + 74,000 CNF facts;
  `SYMLEAN/README.md` §5 table row "`H3` and `V2-L`"; `WRITEUP/MIRROR.md:48-60`).
- Remark sr:rem:records says that for every class the step from a SAT certificate to the Lean class "rests on written
  soundness proofs of the encoders". For the H3/V2-L route to `MirrorOneAxis33` the encoder soundness is Lean-checked
  (`WRITEUP/MIRROR.md:53-56`); only the identification of a file's verdict with a Lean `¬DimacsSatisfiable` term is
  outside Lean.
- "over the same `reflLine`": `Mir.reflLine` and this file's `reflLine` are distinct constants with the same text; their
  equality by `rfl` was shown by a separate check whose file is not in the directory (`SYMLEAN/README.md` §5).
None of this affects a statement or proof of the section (the remarks are informational), hence minor.
Suggested fix: cite `V2L.mirrorExclusionLine_final` as the conditional theorem, say its hypotheses are recorded cake_lpr
verdicts whose proofs were not retained, and restrict "written soundness proofs" to the certificate routes of
`HalfTurn34`, `Threefold33`, `Fivefold35`, `Fourfold32` and `SYMZ`.

### F3 (minor) Remark sr:rem:records omits some written ingredients

Location: `sr.tex` lines 229-241.
- `Threefold33`: `C3FINAL/README.md` ("What this closes") says the reduced cut rests on Lemma H6M (`C3AUDIT2`); the
  class table (`C2ENC/class_table.md` §1) lists it in the normal-form column. The remark lists `C3-S/soundness.md`,
  `C3a` and `C2ENC/perturbation.md` but not Lemma H6M.
- `HalfTurn34`: reductions A and B (written, reviewed in `C2P/review`, checked at the CNF level in `AUDIT3` A5) are
  part of the chain (`C2FINAL/README.md` §1 item 4) and are not named.
- `Fivefold35`: "two encodings" may suggest independence; the class table and `AUDIT3` (A4-3) say they are two normal
  forms of one encoder, not independent encodings.
The remark points to the class table for the full evidence, so this is minor.

### F4 (minor) Notation clash in Lemma sr:lem:prim (P1)

Location: `sr.tex` lines 655-658.
The lemma opens with "Let ζ, ξ ∈ ℂ and n, k, d ∈ ℕ", so `n` is an arbitrary natural number; (P1) then says "then
n = ord(ζ) > 0", using `n` as a definition. Read literally (n arbitrary), (P1) is false for any n ≠ ord(ζ). Every use
("Let n = ord(a). By (P1) ...") has the intended reading, so there is no effect on correctness.
Suggested fix: "then ord(ζ) > 0, ζ is a primitive ord(ζ)-th root of unity, and ord(ζ) = 1 iff ζ = 1."

### F5 (minor) Coverage paragraph: "mentioned only in Remarks ..."

Location: `sr.tex` lines 1054-1056.
`SYMLEAN/review/ReviewSanity.lean` is also cited in the "Axioms and rigor" paragraph (lines 54-57), not only in the
three listed remarks.

### F6 (minor) Overfull boxes

The compile log shows 39 overfull `\hbox` warnings, most from the long multi-`\leanref` heads (e.g. lines 142, 167,
192, 255, 318, 394, 439 of the source). Style only.

### F7 (minor) Wording "is proved" for a Lean-checked review theorem

Location: `sr.tex` line 960: "A group form is proved in the review file ...". Under the contract's rigor labels this
should read "is Lean-checked in the review file".

## Points examined and not reported

- The blanket rigor sentence ("Every statement below whose head carries a Lean reference is Lean-checked in this
  sense") is supported: every Lean-tagged declaration is either a dependency of the two printed theorems, covered by
  the `ReviewSanity` print (bridge lemma), or covered by the empty compile log with no axioms in the file. The main
  library lemma `Suk.convexPosition_of_strict_supports` is a dependency of `case_rot_big`.
- Remark sr:rem:records says SYM5 and C4CUT certificates were accepted by "both" checkers. `LRATCHECK20261105` records
  that unpatched lrat-check builds are unsound on the empty-clause path; the project anchors these results on
  cake_lpr, which accepted them, so the statement is accurate. A brief caveat would be harmless but is not required.
- The logs are recorded outputs of 1 November 2026 and were not re-run (by rule); the section reports them as logs.
- The section re-proves `Suk.convexPosition_of_strict_supports` although `fd.tex` also proves it (as
  `fd:lem:strict-supports`); that label is not in the contract's list of foundation labels, so re-proving it here is
  consistent with the referencing rules.
