# Review sr, round 1, lens: claims, labels and LaTeX

Section: `sections/sr.tex` (1056 lines), map `sections/sr.map.tsv` (46 rows).
Paths below: research records relative to `cloud/es7-2026-10-19/results` (RES); main library relative to the
repository root; build files relative to the staging directory.

**Verdict: pass.** No blocker or major finding. Seven minor findings, listed below with evidence. The first one
(statement heads running off the page in the PDF) should be fixed before assembly; a tested one-line fix is given.

## What was checked, with results

1. **Compile** (`build/claims-sr-r1`, two passes of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
   -output-directory=claims-sr-r1 sr_wrapper.tex` from `build/`): both passes exit 0. No `!` error, no "Missing $",
   no multiply defined label. Undefined references after pass 2: only `fd:def:{point,orient,gp,cp,ngon,inv,rot}`,
   `fd:lem:{collinear,cp-hull,mono}`, `ar:thm:main`, `mb:thm:classes`, `mb:thm:main3`, all allowed. 29 overfull
   hboxes (see M1).
2. **References.** 56 labels defined, no duplicates, all start with `sr:`. Every `\ref` target is an own label, an
   `fd:` label listed in the contract, or a contract export label (`ar:thm:main`, `mb:thm:classes`,
   `mb:thm:main3`); these three exist in `sections/ar.tex:625`, `sections/mb.tex:985`, `sections/mb.tex:1008` on the
   intended statements. Other sections reference `sr:def:classes`, `sr:def:iso`, `sr:thm:main`, `sr:thm:variant`;
   all defined here.
3. **Export labels.** All eight are defined on the statements the contract names: `sr:def:iso` (eDist2,
   IsEucIsometry), `sr:def:classes` (the six classes), `sr:thm:structure` (isometry_complex_cases,
   isometry_structure), `sr:lem:concyclic`, `sr:lem:orbit` (both orbit selections), `sr:thm:main`, `sr:thm:variant`,
   `sr:lem:mirror-line`.
4. **Map.** 46 statement environments, 46 map rows; label and kind identical and in the same order. The Lean-name and
   file:line columns are identical to the `\leanref` heads (script diff, no difference).
5. **Lean names and line numbers.** All 72 `ErdosSzekeres.SymReduction.*` names in the heads exist at the cited lines
   of `SYMLEAN/SymmetricReduction.lean`, and `ErdosSzekeres.Suk.convexPosition_of_strict_supports` is at
   `ErdosSzekeres/Suk/SupportingLines.lean:28`. The file has exactly 72 declarations (lines 65 ... 1056), so the
   claim "All 72 declarations ... are covered" holds. Other cited locations checked: `ErdosSzekeres/Basic.lean:31`
   (ConvexPosition.hasConvexNGon), `H3/MirrorEncoding/Line.lean:18` (Mir.reflLine, text identical to
   SymReduction.reflLine) and `:94` (Mir.MirrorExclusionLine, text identical to MirrorExclusionLineCopy),
   `Mir.mirrorExclusionLine_of_unsat` (:139) and `Mir.mirrorExclusionLine_of_cubes` (:147) both conditional on
   `¬DimacsSatisfiable` hypotheses, `SYMLEAN/review/ReviewSanity.lean:1593` and `:1629`.
6. **Statements against Lean** (read side by side): the six classes (exact sizes 34/33/35/33/34/32, `c ∉ S`, unit
   `u`, the fixed-point conditions, angles `2 * Real.pi / n`), the main theorem, the variant, all case lemmas and
   coordinate lemmas match their declarations, including hypothesis order and `33 ≤ S.card`.
7. **SHA-256 prefixes** recomputed: SymmetricReduction.lean `6d5ec90a4215`, SymmetricReductionAxioms.lean
   `7bf809cbdc77`, Definitions `2425500eefd1`, Basic `13667aa2d3dc`, Orientation `f67955ac7091`, OrientationGeometry
   `c7db9bbbb65e`, Suk/SupportingLines `6a8e12677685`: all as stated. Line counts 1059 and 1062 (two `#print axioms`
   lines after a blank line). Lines 1-1059 of SymmetricReductionAxioms.lean and of review/ReviewSanity.lean are
   byte-identical to the main file (cmp). Lines 1-1058 of AffineReduction.lean are identical (line 1059 starts §9),
   as the Coverage paragraph says. `runs.tsv` prefixes match the current files (6d5ec90a, 7bf809cb, ec251368).
8. **Axioms logs.** `SYMLEAN/logs/SymmetricReduction.out` is empty, exit 0 in `runs.tsv`.
   `SymmetricReductionAxioms.out` lists exactly `[propext, Classical.choice, Quot.sound]` for
   heptagon_of_nontrivial_isometry and halfTurn_of_symmetric_counterexample. `ReviewSanity.out` lists the same for
   `Review.mirrorOneAxis33_iff_exclusionLine`, whose proof uses mirrorOneAxis33_of_exclusionLine (line 1630).
   `SYMLEAN/mirror/axioms.out` lists the same for mirrorOneAxis33_proved, mirrorNoAxis34_proved and the `_3`
   theorems.
9. **No computation, no axiom.** No `sorry`, `admit`, `axiom`, `decide`, `native_decide`, `implemented_by`,
   `extern`, `unsafe` or `set_option` in the main file, nor in its full transitive closure of repository imports
   (Definitions, Basic, Orientation, OrientationGeometry, Suk/{TriangleOrder, BaseChart, BaseOrder, SupportingLines};
   the only hit is the word "axiom" in a comment at Definitions.lean:30). So "No statement of this section is a
   finite computation" is correct and no computer-assisted label is needed for Lean statements. Pins:
   `lean-toolchain` v4.24.0, Mathlib rev f897ebcf72cd.
10. **Hypotheses as hypotheses.** Theorems sr:thm:main and sr:thm:variant and the case lemmas state their classes as
    assumptions ("hypotheses; none is proved in this section"); Remark sr:rem:main says the theorem is Lean-checked
    only as an implication and computer-assisted as an unconditional statement; the map notes say "takes
    hypotheses: ...". No docstring overclaim is repeated ("exactly as written", "Lean-verified there from CNF
    facts", "fully proved" do not occur). No "verified" or "certified" anywhere.
11. **Records (Remark sr:rem:records)** checked against `C2ENC/class_table.md` §1-2, `SYMLEAN/README.md` §5-6,
    `WRITEUP/SYMMETRIC.md` (Theorems 1, 2a, 2b, 4, 5, Corollary 3), `C4CUT/README.md`, `C3FINAL/README.md` (116,883
    records), `C3SPOT` (2,120 of 2,120), the C2 directories (C2C34 hull cover and 120 hexagonal hulls retained;
    C2P-C2P5 parallelogram waves; C2RECHECK; C2FINAL claim), `SYMLEAN/mirror/axioms.out`. All directories and files
    named exist. Rigor labels are right: computer-assisted for HalfTurn34, Threefold33, Fivefold35, Fourfold32;
    Lean-checked (no SAT input) for the two mirror classes; recorded verdicts of deleted proofs named for C2P* and
    C3FINAL; the H3 route named as conditional on CNF facts. The Fourfold32 credit (Subercaseaux, Mackey, Qian and
    Heule, arXiv:2506.00224, §6.2) matches `C4CUT/README.md` and `SYMLEAN/README.md` §5. "Accepted by both
    checkers" (SYM5, C4CUT) stays correct in view of `LRATCHECK20261105/README.md`, since cake_lpr also accepted
    those proofs.
12. **Paths and names.** No absolute machine path (system temp, home or user directories) and no name of a software
    tool that wrote text in `sr.tex` or `sr.map.tsv` (case-insensitive grep for the contract's forbidden prefixes and
    names). All 39 `\dirn{}` paths resolve, relative to RES or to the
    repository root as the Sources paragraph says. No `\newcommand`, `\def`, `\usepackage` or other preamble
    material; only the allowed environments; first line `\section{...}\label{sr:sec}`.

## Findings

### M1 (minor, LaTeX): statement heads run off the right edge of the page; Lean names and line numbers are cut off

- Evidence: `build/claims-sr-r1/sr_wrapper.log` has 29 `Overfull \hbox` warnings, the largest 190.1pt (Lemma
  sr:lem:crot head, source lines 394-396), others 169.1pt (lines 319-320), 159.8pt (193-195), 156.8pt (482-483),
  153.4pt (143-144), 151.5pt (256-257, 423-424), 135.8pt (106-108). With a 0.9in right margin (65pt) anything over
  about 65pt leaves the page. Rendered pages confirm it: page 2, Definition 1.1 head ends "SYMLEAN/SymmetricReduct"
  (the line number 268 of IsEucIsometry is invisible), Lemma 1.5 head is cut in four lines; page 6, Lemma 1.16 ends
  "SYMLEAN/SymmetricReducti", Lemma 1.17 ends "ErdosSzekeres.SymReduc" twice, Lemma 1.18 loses the line of
  halfTurn_eq_crot. About 17 statement heads are affected.
- This is local to this section: `ar_wrapper.log`, `cb_wrapper.log` and `lg_r1adv_wrapper.log` have 0 overfull
  boxes, because `sections/ar.tex` wraps its body in `\begingroup\sloppy\emergencystretch=\linewidth` (line 2) ...
  `\endgroup` (line 752).
- Fix (tested on a scratch copy, `build/claims-sr-r1/sloppytest/`): insert
  `\begingroup\sloppy\emergencystretch=\linewidth` after line 1 and `\endgroup` at the end. Result: exit 0,
  0 overfull hboxes.

### M2 (minor, claims): Remark sr:rem:variant describes the review group form as "proved" and Corollary 3 inexactly

- Lines 960-961: "A group form is proved in the review file `SYMLEAN/review/VariantChecks.lean` (`group_form`)".
  `group_form` (VariantChecks.lean:1168) takes Threefold33, Fourfold32, Fivefold35, MirrorOneAxis33 and
  MirrorNoAxis34 as hypotheses. Per contract rules 7-8, say "Lean-checked, with the same five classes as
  hypotheses".
- Lines 958-960: "that corollary speaks about the whole symmetry group and also about affine symmetries".
  `WRITEUP/SYMMETRIC.md` Corollary 3 (lines 46-49) says "every symmetry of a 7-gon-free set ... is a half-turn about a
  point outside the set", with "symmetry" covering affine bijections (lines 8-9). That is a per-symmetry statement
  over all symmetries, and SYMMETRIC.md itself says "Lean-checked for isometries". The group form ("symmetry group
  exactly the half-turn group") is the note's Corollary cor:only (`WRITEUP/note/symmetric_es7.tex:95-104`). The
  real gap between the Lean theorem and SYMMETRIC.md's Corollary 3 is the affine symmetries. Suggested wording:
  "...; that corollary also covers affine symmetries, and the note's Corollary cor:only states a group form."

### M3 (minor, names): short names that do not expand to existing declarations under the section's namespace convention

- Lines 101-103 state: "All Lean names of this section are in the namespace `ErdosSzekeres.SymReduction` unless
  stated otherwise". Three review names are in sub-namespaces, and nothing says so:
  `mirrorOneAxis33_iff_exclusionLine` (line 55) and `exclusionLine_of_mirrorOneAxis33` (line 989) are
  `ErdosSzekeres.SymReduction.Review.*` (ReviewSanity.lean:1073), and `group_form` (line 961) is
  `ErdosSzekeres.SymReduction.VariantChecks.group_form` (VariantChecks.lean:1076, 1168). Read with the convention,
  they name nonexistent declarations. File paths are given, so a reader can find them; this is why the finding is
  minor and not a blocker.
- The Mathlib names in Lemma sr:lem:minper (lines 291-294) lack the `Function.` prefix:
  `Function.IsPeriodicPt.minimalPeriod_dvd`, `Function.minimalPeriod_eq_one_iff_isFixedPt`,
  `Function.iterate_minimalPeriod` and `Function.iterate_injOn_Iio_minimalPeriod`. The Lean file has
  `open Function`.
- Fix: write the full names.

### M4 (minor, claims): the first sentence of Remark sr:rem:records does not fit the H3 route

- Lines 225-227: "For no class is the step from a SAT certificate to the Lean class Lean-checked: that step rests on
  written soundness proofs of the encoders and on the review of the class definitions ...". This is right for the
  SAT routes of the five classes. For the H3 route to MirrorOneAxis33 (named at line 246), the step from CNF
  unsatisfiability to `Mir.MirrorExclusionLine` is Lean-checked (`Mir.mirrorExclusionLine_of_unsat`,
  `H3/MirrorEncoding/Line.lean:139`). Outside Lean are only the recorded verdicts and the identification of
  `Mir.MirrorExclusionLine` with `MirrorExclusionLineCopy`. That identification is by text; `SYMLEAN/README.md` §5
  reports a `rfl` check that is not retained in the repository.
- The sentence understates rather than overclaims. Suggest: "except the H3 route (Remark sr:rem:mirror-line), where
  the encoder step is Lean-checked and only the CNF verdicts, recorded outside Lean, and the textual identification
  of the two propositions remain".

### M5 (minor, claims): Fivefold35's "two encodings" can be read as independent

- Lines 239-241: "SYM5 (two encodings, proofs retained and accepted by both ...)". `C2ENC/class_table.md` §1
  (Fivefold35 row) and `WRITEUP/SYMMETRIC.md` Theorem 5 say they are "two normal forms of one encoder, not
  independent encodings (AUDIT3, A4-3)".
- The section does not claim independence, but adding "(two normal forms of one encoder, not independent)" removes
  the ambiguity. Optionally note that the layer lemma behind form (b) is Lean-checked in LAYERLEAN.

### M6 (minor, accuracy): the Coverage paragraph says the review files are mentioned "only in Remarks ..."

- Lines 1054-1056 list Remarks sr:rem:sup, sr:rem:variant and sr:rem:mirror-line. `SYMLEAN/review/ReviewSanity.lean`
  and its log are also cited in the "Axioms and rigor" paragraph (lines 54-57), as the axiom evidence for
  mirrorOneAxis33_of_exclusionLine. Fix the wording.

### M7 (minor, accuracy): "the Mathlib facts used are restated and proved in Lemmas sr:lem:minper and sr:lem:prim"

- Lines 1050-1051. That is true only of the minimal-period and root-of-unity facts. The other Mathlib results used
  by the Lean proofs are handled elsewhere:
  - `Isometry.affineIsometryOfStrictConvexSpace` and `linear_isometry_complex`, replaced by the self-contained proof
    of sr:thm:structure(a);
  - `Set.Finite.exists_lt_map_eq_of_forall_mem`, in sr:lem:pigeon;
  - `Complex.cpow_nat_inv_pow`, replaced by "every complex number has a square root";
  - `Nat.minFac_prime`, used inline in the proof of sr:lem:root-cases.
- Suggest "the Mathlib facts on minimal periods and roots of unity are restated and proved in ...; the others are
  proved or replaced in place (sr:lem:pigeon, sr:thm:structure(a))".

## Not findings (checked and correct)

- Remark sr:rem:sup: the sup-metric example (rotation by 2π/3 sends c + (1,0) to c + (-1/2, √3/2), sup distance
  √3/2 < 1) is correct, and `review/SupMetric.lean` contains `not_isometry_rot_threefold` (log: standard axioms).
- "reflLine with u = 0 is the half-turn about a": d = 0 gives (2a0 - p0, 2a1 - p1). For other non-unit u the linear
  part 2uu^T - I has eigenvalue 2|u|^2 - 1 ≠ ±1, so the map is not an isometry.
- Remark sr:rem:redundant: 3 ∤ 32 and 5 ∤ 34. For 34 mirror points |F| ∈ {0, 2}. Its last sentence matches
  `SYMLEAN/README.md` §6.3.
- Remark sr:rem:main: the binder names h2 h3 h5 hm1 hm0 are as in the source (lines 998-999). Theorem mb:thm:main3
  indeed keeps only HalfTurn34, Threefold33 and Fivefold35 (`SYMLEAN/mirror/axioms.out`, #check lines).
