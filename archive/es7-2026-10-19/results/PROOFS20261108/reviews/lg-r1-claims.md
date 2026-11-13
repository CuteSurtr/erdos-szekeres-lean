# Review of section `lg`, round 1, lens: claims, labels and LaTeX

Section: `sections/lg.tex` (855 lines) and `sections/lg.map.tsv` (31 rows plus header).
Verdict: **pass**. No blocker or major findings. 8 minor findings, listed below.

## What was checked, with evidence

### Compile (as instructed)
- Command, run from `STAGE/build`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=claims-lg-r1 lg_wrapper.tex`, run twice.
- Both passes exit 0. Output: 10 pages. Logs are in `build/claims-lg-r1/`.
- The final log has no errors, no "Missing $", and no overfull or underfull boxes.
- The only warning is "There were undefined references". All of them are allowed labels:
  - fd labels: `fd:def:cp`, `fd:def:gp`, `fd:def:inv`, `fd:def:ngon`, `fd:def:orient`, `fd:def:point`, `fd:def:rot`, `fd:lem:collinear`, `fd:lem:mono`, `fd:lem:orient`, `fd:lem:pos-triples`.
  - ll export labels: `ll:def:hv`, `ll:def:peel`, `ll:lem:antitone`, `ll:lem:hv`, `ll:lem:inv-peel`, `ll:lem:minperiod`, `ll:thm:card-peel`, `ll:thm:core-rot`.
- No `lg:` label is undefined. Every referenced fd/ll label is defined in `fd.tex` or `ll.tex` (checked by grep).
- The PDF was rendered to PNG and pages 1, 2, 7 and 10 were inspected. The layout is fine apart from minor finding M7.

### LaTeX rules
- The file starts with `\section{...}\label{lg:sec}`.
- It contains no `\newcommand`, `\def`, `\usepackage`, `\begin{document}` or `\input`.
- Only the allowed environments are used (plus amsmath displays, `itemize`, `enumerate` and `cases`).
- Every label starts with `lg:`. Each of the 42 labels is defined exactly once.
- There are no non-ASCII characters in the `.tex` or the `.tsv`.

### Labels and references
- Every `\ref`/`\eqref` target is either an own `lg:` label, an fd label from the contract list, or an ll export label from the contract table. No other target is used.
- All 13 export labels are defined, each on the statement the contract names:
  - `lg:lem:orient-rot` → orient_rotAbout
  - `lg:lem:regular` → orient_regular_nonneg
  - `lg:thm:nesting` → strict_nesting
  - `lg:lem:centre` → centre_not_mem_of_even
  - `lg:thm:fan` → hasConvexNGon_of_fan
  - `lg:lem:halfplane` → lin_pos_of_peel
  - `lg:thm:chain` → chain_clauses_sound
  - `lg:def:polar` → polar
  - `lg:lem:polar` → orient_polar
  - `lg:lem:ruleA` → orient_polar_centre_inside
  - `lg:lem:sinadd` → sin_add_lt
  - `lg:lem:ruleB` → orient_polar_halfplane
  - `lg:thm:radius` → dist2_le_of_later
- Other sections reference only export labels of `lg` (ec, ll, oc, pc: centre, nesting, def:polar, lem:polar, ruleA, ruleB, sinadd, radius). All of these exist.

### Map TSV
- The header is correct.
- There are 31 rows, one for each of the 31 non-remark statement environments (22 lemmas, 4 theorems, 1 corollary, 4 definitions). They are in the same order as in the file, and each row has 5 columns.
- For every row, the kind, the Lean name and the `file:line` match the `\leanref` in the statement head.
- The written steps (`lg:lem:layer`, `lg:lem:rotfacts`, `lg:cor:period`, `lg:lem:cramer`) have `-` in both Lean columns and are tagged "written step" in their heads.
- The axioms-log note of each row is consistent with the logs: rows marked "LEANEXT only" are exactly the 7 theorems missing from `LAYERLEAN/logs/axioms.log`.

### Lean names, files and line numbers
- Every declaration line cited in the heads and the map matches `LAYERLEAN/LayerLemma.lean` exactly:
  - 465 rotAbout_iterate, 472 orient_rotAbout, 480 trig_layer, 488 orient_regular_nonneg, 516 convex_orient_nonneg
  - 529 strict_nesting, 582 centre_not_mem_of_even, 625 lin, 629 orient_trans_halfplane, 641 fan_step
  - 653 orient_eq_lin, 658 fan_positive, 694 fanPt, 700 hasConvexNGon_of_fan, 794 lin_rotAbout
  - 801 lin_orbit_pos, 830 orient_next_prev_pos, 864 lin_pos_of_peel, 914 chain_clauses_sound, 932 polar
  - 935 orient_polar, 943 orient_polar_centre_inside, 956 sin_add_lt, 974 orient_polar_halfplane, 999 dist2
  - 1002 convex_disk, 1012 dist2_le_of_later
- Other line citations are also correct:
  - "lines 465–1032": dist2_le_of_later ends at line 1032.
  - orbitFS is defined at :48.
  - peel_antitone is at line 460, and card_peel at line 1037 with its docstring at line 1036.
- Main-library citations are correct: `ErdosSzekeres/Orientation.lean:9` (orient), `ErdosSzekeres/OrientationGeometry.lean:66` (generalPosition_iff_orient_ne_zero) and `ErdosSzekeres/Suk/OrientationClique.lean:9` (convexPosition_of_positive_triples).
- Every `\lean{}`/`\leanref{}` name exists. LayerLemma names were checked by grep for their declarations. The rest are main-library names, Mathlib names (`Convex`, `convexHull_min`, `Even`) or keywords.
- All scope declarations are in `namespace ErdosSzekeres.LayerLemma`, so the full names in the heads are right. The file's only other namespace commands are `section Orbits`, which does not change names, and `end ErdosSzekeres.LayerLemma` at line 1148.

### SHA-256 prefixes (recomputed with `shasum -a 256`)
All prefixes are correct:

| File | Prefix |
|---|---|
| `LAYERLEAN/LayerLemma.lean` | `afb8542dceb0` (1148 lines) |
| `LAYERLEAN/README.md` | `9eaec241a1d2` |
| `ErdosSzekeres/Definitions.lean` | `2425500eefd1` |
| `ErdosSzekeres/Orientation.lean` | `f67955ac7091` |
| `ErdosSzekeres/OrientationGeometry.lean` | `c7db9bbbb65e` |
| `ErdosSzekeres/Suk/OrientationClique.lean` | `cf63d5219b47` |
| `LAYERLEAN/logs/axioms.log` | `3c4b7aac502e` |
| `LEANEXT/review/axioms.log` | `386c4f578725` |
| `LAYERLEAN/logs/axioms_recheck_20261106/out.txt` | `a59c3816cbe7` |

The reviewed-file hash `afb8542d…` matches `LEANEXT/review/REPORT.md`.

### Axioms-log claims (logs opened)
- **`LAYERLEAN/logs/axioms.log`** has 28 lines, 16 of them for theorems of this scope. The 7 scope theorems missing from it are exactly the ones the text lists: rotAbout_iterate, orient_rotAbout, convex_orient_nonneg, orient_eq_lin, lin_rotAbout, lin_orbit_pos and orient_next_prev_pos.
- **`LEANEXT/review/axioms.log`** has 59 lines and contains all 23 scope theorems. The 59 are exactly the 66 theorem declarations of the file minus its 7 `@[simp]` lemmas (toC_re, toC_im, ofC_zero, ofC_one, toC_ofC, ofC_toC, toC_crot), checked by set difference.
- **The re-check `out.txt`** has 19 lines, 11 of them in scope (strict_nesting, centre_not_mem_of_even, dist2_le_of_later, orient_polar, orient_polar_centre_inside, orient_polar_halfplane, sin_add_lt, chain_clauses_sound, hasConvexNGon_of_fan, lin_pos_of_peel, fan_positive). This matches "the 11 of them that it lists".
- Every scope entry in all three logs is `[propext, Classical.choice, Quot.sound]`.
- `logs/build.log` records `lake env lean`, exit code 0 and 0 message lines, with Lean 4.24.0 and Mathlib f897ebcf72. This matches `lean-toolchain` and `lake-manifest.json`.
- `lakefile.toml` has `defaultTargets = ["ErdosSzekeres"]`, so the statement "not part of the default lake build target" is correct.
- grep finds no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `unsafe`, `opaque` or `extern` in the file. Its only `decide` is at line 1125, outside the scope.

### Hypotheses, computations and rigor labels
- No statement in scope takes Sixfold66, Sevenfold70, a case class or a SAT verdict as a hypothesis, and none is a finite computation. The Rigor paragraph says exactly this, and it is accurate.
- "Lean-checked" appears once, in the Rigor paragraph, with the logs cited.
- The written proofs are labelled "written proofs (not refereed)".
- Definitions are "restated", not called Lean-checked.
- There is no "verified", "certified", "exactly as written", "omitted" or "see the Lean file".
- The code-to-clause step is explicitly disclaimed in Remark (3) after Theorem 1.16 and in the remark after Theorem 1.32. The missing polar-coordinate link (review F2) is disclaimed in the remark after Lemma 1.38. Strict radii are disclaimed after Theorem 1.20.

### Machine paths and tool names
- grep finds no `/private`, `/Users`, `/home`, `/tmp`, `/sandbox`, the scratch-directory name or user name in `lg.tex` or `lg.map.tsv`.
- grep finds no tool name (a list of product names).
- Paths are relative to RES (`LAYERLEAN/…`, `LEANEXT/…`, `ENCBLEAN/…`) or to the repository root (`ErdosSzekeres/…`).

### Coverage claims
- All 27 scope declarations are listed with `\ref`s: 23 theorems and the 4 definitions lin, dist2, fanPt and polar.
- The claim that `LEANEXT/capstone/Capstone2.lean`, `LEANEXT/merged/Merged.lean`, `LEANEXT/es7corr/ES7Corollaries.lean` and `ENCBLEAN/geo/ES8Geo/Capstone2.lean` each contain lines 11–1147 of `LayerLemma.lean` verbatim is true. Substring checks place the block at lines 19, 11, 11 and 19 respectively. See M3 for the copies that are not listed.

### Statements against Lean (cross-check for this lens)
- All 27 heads were compared with the Lean source.
- Hypotheses and their order, strict and weak inequalities, `j ≤ m`, `0 < j < m`, `3 ≤ m`, `4 ≤ K`, `K − 1`, `n < n'` against `n ≤ n'`, and the conclusion `False` all match.
- Comments about how Lean proves things are accurate: complex form for rotAbout_iterate; `ring` for orient_rotAbout and the key identity; cos_two_mul with sin²+cos² for trig_layer; nlinarith for convex_disk and rule B; minimal period for x ≠ ρx and for ρ(p′) = p.

### Identities (sympy 1.13.3; script `build/claims-lg-r1/sympy_identities.py`)
109 checks were run, all symbolic unless noted:
- (1) and det(X,Y) = ⟨JX,Y⟩; (O1)–(O4); R_θX = cosθ X + sinθ JX; rotAbout = c + R_θ(p−c); rotation facts (a)–(d).
- orient_rotAbout and its b−x decomposition; trig_layer and both intermediate lines.
- The remark formula 4|x−c|² sin(π/m) sin(jπ/m) sin((j−1)π/m), for m ∈ {2,3,5,6,7} and all 0 ≤ j ≤ m.
  - For m = 5, j = 2 and 3, sympy could not simplify the nested radicals. A 60-digit numeric check gives zero for m ∈ {5,8,10,11,12} and all j.
- lin_rotAbout and its intermediate step; the next/prev rewriting F = 4 sin t sin(π−t) sin(π−2t), with F > 0 for m = 3,…,9.
- The convex_disk algebra; rotAbout(c,π)p = 2c−p and orient(p,c,2c−p) = 0; the m = 2 remark.
- The Cramer identity (vector, ⟨w,·⟩ and det(V,·) forms) and its 3×3 expansion.
- (eq:trans) and its Cramer instance; (eq:fanstep) with all six det translations and its Cramer instance; orient_eq_lin.
- (eq:key) and orient(p′,p,y) = det(E,C); orient_polar, the det decomposition and det(re(φ),se(ψ)) = rs sin(ψ−φ).
- The rule B decomposition, the rule A sine shift, and the sine addition formula.

All identities hold.

## Findings (all minor)

**M1 (minor, attribution). Axioms paragraph, lg.tex:46–48.**
- The text says the review log "according to `LEANEXT/review/REPORT.md` covers all 59 non-simp theorems of the reviewed file".
- REPORT.md does not say "non-simp". It says "All 59 theorem declarations were checked", and F6 says "the file has 59 theorems in all". The file has 66 theorem declarations, 7 of them `@[simp]`.
- The section's statement is factually right (I verified that the 59 are exactly the non-simp theorems), but the qualifier is the section's own correction and is attributed to REPORT.md.
- Suggested fix: "which covers all 59 theorems of the reviewed file other than its 7 `@[simp]` lemmas (REPORT.md speaks of 'all 59 theorem declarations')".

**M2 (minor, incomplete source list). Sources, lg.tex:28–38.**
- The list of main-library declarations that "the section uses" omits `ErdosSzekeres.orient_cycle` (`ErdosSzekeres/Orientation.lean:15`). The Lean proof of hasConvexNGon_of_fan uses it at LayerLemma.lean:742, 747, 767 and 772.
- The list also omits `HasConvexNGon.mono` (via `fd:lem:mono`(c)), which the written proofs use: Notation, and the proof of Theorem `lg:thm:chain`.
- Both are reachable through the Dependencies paragraph (`fd:lem:orient`, `fd:lem:mono`), so correctness is not affected.
- Suggested fix: add orient_cycle to the list, or say "uses, among others".

**M3 (minor, coverage list of copies is not exhaustive). Coverage, lg.tex:848–853.**
- The text lists four files as "the verbatim copies of these declarations in other units".
- Four more files also contain lines 11–1147 of `LayerLemma.lean` verbatim (substring check):
  - `LEANEXT/capstone/Capstone.lean`
  - `LEANEXT/linked/Linked.lean`
  - `LEANEXT/review/VacuityTest.lean`
  - `LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean`
- `LEANEXT/phase/PhaseClassification.lean` also has statement-identical copies of polar, orient_polar, orient_polar_centre_inside, sin_add_lt and orient_polar_halfplane, in `namespace PhaseClassification`. Section `pc` covers these.
- These copies are outside this section's scope (LAYERLEAN lines 460–1036, which is fully covered), so the coverage claim for the scope is not affected.
- Suggested fix: "among them" or list all of them.

**M4 (minor, wording about how the proofs relate to Lean). lg.tex:56–58 and 841–842.**
- The text says "They follow the Lean proofs, except where a remark says otherwise" and that the written steps "collect facts that the Lean proofs establish inline". This is looser than the content.
- **Lemma `lg:lem:cramer`.** Lean never establishes the general identity; it checks each instance by `ring`.
- **Corollary `lg:cor:period`.** ρ^m = id for every point is not what Lean proves; Lean uses the minimal period for p ≠ c. The map note and remark (2) after Lemma 1.30 say this.
- **Deviations marked only by parentheticals inside proofs, not remarks:** rotAbout_iterate, trig_layer, convex_disk and rule B.
- **Deviations not marked at all:** orient_trans_halfplane and fan_step are proved through the Cramer identity, where Lean uses `ring`; orient_polar is proved through the det decomposition, where Lean uses `simp`/`sin_sub`/`ring`.
- These deviations are harmless; the issue is the sentence describing them.
- Suggested fix: "They follow the structure of the Lean proofs; where the argument differs, a remark or a parenthetical in the proof says so. The written steps collect or replace facts that the Lean proofs establish inline."

**M5 (minor, possible overclaim in the summary). lg.tex:20–21.**
- The text says "hence the chain clauses are sound (Theorem~\ref{lg:thm:chain})".
- The theorem is the geometric statement behind the chain clauses. That the encoders emit exactly these clauses is not in Lean, as the remark at lg.tex:711–715 says correctly.
- Suggested fix: "hence the geometric statement behind the chain clauses holds" or "hence the chain clauses are satisfied by the true orientations".

**M6 (minor, map practice; I am unsure this is required). lg.map.tsv.**
- The map has no rows for the 8 remark environments, which are unlabelled.
- The contract asks for "one row per statement environment", and remarks are arguably not statements. Sections `fd` and `mm` also omit them, but `ar`, `ec`, `ll`, `mb`, `oc`, `pc` and `sr` include remark rows.
- I flag this only so that sections are consistent. If remark rows are required, the remarks need labels such as `lg:rem:...`.

**M7 (minor, cosmetic). Equation (1), `lg:eq:J`, lg.tex:77–79.**
- The display is too wide for the line, so amsart puts its number "(1)" on a line of its own above the display (page 2 of the PDF).
- There is no overfull warning.
- Suggested fix: split the display into two lines, or drop one item.

**M8 (minor, informational; I am unsure this is a defect). Contract row "`lg:lem:regular` orient_regular_nonneg (with trig_layer)".**
- trig_layer is stated as a separate Lemma `lg:lem:trig`, which is not an export label. The export statement `lg:lem:regular` carries only orient_regular_nonneg.
- No other section references trig_layer, so no reference is broken.
- I flag this only in case the contract meant trig_layer to appear in the head of the export statement.

## Not findings (checked and correct)
- **The m = 2 remark.** It is logically sound: the hypotheses cannot all hold, so for m = 2 the theorem forces the later peels to be empty.
- **The S = {c} counterexample remark for centre_not_mem_of_even.** It is correct.
- **The "value 0 exactly for j ∈ {1, m}" refinement in the remark after Lemma 1.7.** It is correct for x ≠ c and m ≥ 2.
- **README version.** `LAYERLEAN/README.md` is cited at its current hash `9eaec241…`. REPORT.md reviewed an older README (`555f10d3…`), but the section does not claim otherwise.
