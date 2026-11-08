# Diff audit of section `sr`, polish round 1

Compared: `snapshots/sections-r1pass/sr.tex` and `sr.map.tsv` (the version that passed the four-lens review;
byte-identical to `snapshots/polish-r1-pre/`) against `sections/sr.tex` (1,116 lines; 1,056 before) and
`sections/sr.map.tsv` (46 rows plus header in both). `diff -u` gives 22 hunks in the `.tex` and one hunk (two rows) in
the map. Fixer log: `reviews/sr-polish-r1-fix.md`. Round-1 reports read in full: `reviews/sr-r1-fidelity.md`,
`sr-r1-rigor.md`, `sr-r1-adversarial.md`, `sr-r1-claims.md` and `sr-writer-concerns.md`. No earlier polish audit of
`sr` (`sr-p*-diff.md`, `sr-p*-referee.md`) exists. Paths below are relative to the staging area, to the results
directory `RES`, or to the repository root (main library); Mathlib means the pinned checkout at rev `f897ebcf72cd`.

**Verdict: PASS.** No blocker and no major finding; two minor findings (§5). Every hunk was checked against the Lean
source and the cited records. Every fix the fixer marked "fixed" is correct; the duplicates point to correct fixes;
the one declined item (an optional addition) is acceptable. My own wrapper compiles with exit 0 and has no overfull
box.

## 1. The `.tex` hunks (all 22, grouped by topic; line numbers of the current file)

1. **Sources** (lines 36-48). The import closure of `SYMLEAN/SymmetricReduction.lean` inside the repository was
   recomputed from the import lines: the file imports `Basic`, `OrientationGeometry`, `Suk/SupportingLines`;
   `Basic` imports `Definitions`; `OrientationGeometry` imports `Definitions`, `Orientation`; `Suk/SupportingLines`
   imports `Suk/BaseOrder`, `Basic`; `BaseOrder` → `BaseChart` → `TriangleOrder` → `OrientationGeometry`. So exactly
   eight modules, and the last three are reached only through `Suk/SupportingLines`. SHA-256 prefixes recomputed:
   `d21becd29e84` (BaseOrder), `08d0e856f005` (BaseChart), `6447cd4833d4` (TriangleOrder), and the five old ones
   unchanged. The section cites nothing from the three new modules (its only `Suk.` name is at
   `Suk/SupportingLines.lean:28`). Correct.
2. **Axioms and rigor** (lines 59-67). `Review.mirrorOneAxis33_iff_exclusionLine` is at
   `SYMLEAN/review/ReviewSanity.lean:1629`, inside `namespace ErdosSzekeres.SymReduction.Review` (lines 1073-1632);
   `logs/ReviewSanity.out` line 32 shows the three standard axioms for this full name. The scan of the file and the
   eight modules (grep): no `axiom` declaration, no `sorry`/`admit`, no `decide`/`native_decide`/`ofReduceBool`; the
   word "axiom" occurs only in the docstring `ErdosSzekeres/Definitions.lean:30` and in the module docstring of the
   main file (lines 16 and 50). The sentence about unused declarations now rests on the compile log and this scan,
   which together support it. Correct.
3. **Dependencies** (lines 78-81). `cb:thm:c2` (`Central34.all_cases_closed`) and `cb:thm:c3`
   (`C3Cover.all_roots_covered`) are contract export labels of section `cb`, both theorem environments; they are
   cited only in Remark `sr:rem:records`, as stated. "Lean-checked bookkeeping" matches their status in `cb` (kernel
   evaluation; the `cb` section adds the label computer-assisted, which is not contradicted). "Which gives written
   proofs of the two mirror classes" replaces "where … are proved", in line with the rigor vocabulary. Correct.
4. **Conventions** (lines 105, 110-115). `starRingEnd` is Mathlib's. The new name rule was tested on every `\lean`
   name of the section (script extraction): every short name resolves to the intended declaration under "the first
   of `ErdosSzekeres.SymReduction.n`, `ErdosSzekeres.n`, `n` that exists". `Review` and `VariantChecks` are
   sub-namespaces of `ErdosSzekeres.SymReduction` (`ReviewSanity.lean:1073`, `VariantChecks.lean:1076`); `Point` is
   `ErdosSzekeres.Point`; `Suk.` is `ErdosSzekeres.Suk`. No Mathlib name used in the text (`Isometry`, `Collinear`,
   `ConvexIndependent`, `IsPrimitiveRoot…`, `orderOf…`, `starRingEnd`, `Function.…`, `Complex.…`, `Set.Finite…`) has
   a namesake in `ErdosSzekeres` (grep of the main library for such declarations and namespaces: none). Correct.
5. **Form of g** (lines 125-127). Lemma `sr:lem:toC-iso`(b) gives an isometry G of ℂ, Theorem `sr:thm:structure`(a)
   gives `G z = a z + b` or `a z̄ + b` with `|a| = 1`. Correct.
6. **reflLine paragraph** (lines 199-206). Checked with sympy (`build/sr_p1diff/sr_p1diff_sympy.py`, all OK): the
   complex form differs from `â + û² conj(z − â)` by `(z − â)(s − 1)`, so it holds for `s = u0²+u1² = 1` as Lemma
   `sr:lem:refl`(a) states; `a + tu` is fixed when `s = 1`; `a + itu ↦ a − itu` (for every u, since d = 0); `u = 0`
   gives `2a − p`; `a` is fixed and `a + u ↦ a + (2s−1)u`; `eDist2 = (2s−1)² s`, and `(2s−1)² s = s` has exactly the
   solutions `s ∈ {0, 1}`, so for every other u the map is not a Euclidean isometry. "Same text as `Mir.reflLine`":
   the bodies at `H3/MirrorEncoding/Line.lean:18-20` and `SymmetricReduction.lean:423-425` are byte-identical.
   Correct.
7. **Fixed points of a unit reflLine** (lines 230-234). `reflLine(p) − p = 2du − 2(p − a)` (sympy), so a fixed point
   is `a + du`; `d(a + tu) = t s = t`. Correct, and now proved directly from Definition `sr:def:maps`(d).
8. **Remark `sr:rem:records`** (lines 241-287). Every claim was compared with the records:
   - Trust sentence: `WRITEUP/SYMMETRIC.md` §3 (lines 229-235, revised 6 November): only cake_lpr is trusted,
     lrat-check is a secondary check, and "both checkers" means the cake_lpr verdict. Correct.
   - "No step from a SAT certificate to a Lean class is Lean-checked": `SYMMETRIC.md` line 35 and §4. The restriction
     of "written proofs … and the review of SYMLEAN/README.md §6" to the certificate routes of the four rotation
     classes and to SYMZ matches `C2ENC/class_table.md` §1-§3 and `SYMLEAN/README.md` §6 (all six classes reviewed).
     For the H3/V2-L route, `WRITEUP/MIRROR.md` §1 (lines 53-56) says the kernel checked the soundness of the two
     encodings, the normal forms and the case split. Correct.
   - HalfTurn34: "verdicts of both checkers recorded at solve time" (`class_table.md` §1; `SYMMETRIC.md` lines
     244-245); reductions A (P_a ↔ P_{17−a}) and B (subcase pairing into 287 orbits), written, reviewed in
     `C2P/review`, checked at the CNF level in `AUDIT3` A5 (`C2FINAL/README.md` lines 27-30; `SYMMETRIC.md` lines
     121-124); the orbit bookkeeping is Lean-checked (`C2FINAL/README.md` §6), which is Theorem `cb:thm:c2`. Correct.
   - Threefold33: 2,120 pieces re-solved in `C3SPOT` from a random draw (`C3SPOT/README.md` lines 1-24); the 204
     indispensable σ-cube pieces re-solved with retained proofs, both checkers (`C3PIECES/README.md`, Status and §3);
     the Lean-checked cover of the 910 roots, with the leaf-to-record step checked in Python (`SYMMETRIC.md` lines
     206-209; `class_table.md` §1), which is Theorem `cb:thm:c3`; Lemma H6M (`C3FINAL/README.md` line 36,
     `C3AUDIT2/REPORT.md`). Correct.
   - Fivefold35: two normal forms of one encoder, not independent, each with a retained proof accepted by both
     checkers and each settling the class alone (`SYM5/README.md` lines 26, 84-91; `class_table.md` §1);
     B. C. Dumitru, arXiv:2512.24061 §7, priority, no public proof files (`SYM5/README.md` lines 13-25). Correct.
   - Mirror classes: `SYMLEAN/mirror/ReductionThreeClasses.lean` imports only library and Mathlib modules (lines
     1-13), and `diff` of its lines 38-1084 with lines 12-1058 of `SymmetricReduction.lean` is empty; the copied text
     contains `namespace ErdosSzekeres.SymReduction` (its line 80), so the full names agree; `mirrorOneAxis33_proved`
     (4274) and `mirrorNoAxis34_proved` (4282) are in that namespace (4249-4310). SYMZ = Theorems 2a/2b of
     `SYMMETRIC.md`. Correct; see minor finding m2 for one wording.
   - Fourfold32: `SYMLEAN/README.md` §5 row and `SYMMETRIC.md` §2 table. Correct.
9. **Lemma `sr:lem:minper`** (lines 327-330). In Mathlib `Mathlib/Dynamics/PeriodicPts/Defs.lean` the four theorems
   are inside `namespace Function` (lines 49-503): `iterate_minimalPeriod` 258, `iterate_injOn_Iio_minimalPeriod`
   327, `minimalPeriod_eq_one_iff_isFixedPt` 340, `IsPeriodicPt.minimalPeriod_dvd` 364. Full names correct.
10. **Head of Lemma `sr:lem:orbitFS`** (line 354). Only the order of the references changed. Lean re-read
    (`SymmetricReduction.lean:76-118`): items (a)-(e) still match `mem_orbitFS_self` 90, `orbitFS_subset` 93,
    `orbitFS_invariant` 99, `card_orbitFS` 76, `card_orbitFS_of_minimalPeriod` 111 exactly (hypotheses `0 < p`,
    none, `0 < p ∧ f^[p] x = x`, `p.Prime ∧ f^[p] x = x ∧ f x ≠ x`, `minimalPeriod f x = p`). Correct.
11. **Titles** of `sr:lem:toC-iso`, `sr:lem:concyclic`, `sr:thm:main`, `sr:thm:variant`, `sr:lem:mirror-line`
    (old lines 481, 601, 893, 928, 971; new lines 517, 637, 932, 969, 1016). Only the short names changed; the Lean
    declarations were re-read
    (lines 301, 313, 509, 997, 1024, 1052-1057) and the statements still match.
12. **Proof of Theorem `sr:thm:structure`(a)** (lines 556-559). Mathlib's `Isometry.affineIsometryOfStrictConvexSpace`
    (`Mathlib/Analysis/Convex/StrictConvexBetween.lean:138`) needs `StrictConvexSpace` only for the codomain and its
    docstring says it does not need surjectivity; `linear_isometry_complex` (`Mathlib/Analysis/Complex/Isometry.lean:130`)
    takes `f : ℂ ≃ₗᵢ[ℝ] ℂ`. Both descriptions are now right; see minor finding m1 (the first is a `def`).
13. **Lemma `sr:lem:prim`(P1)** (lines 693-695, 708-711). The statement no longer uses the fixed letter n; it is
    true (Mathlib `IsPrimitiveRoot.orderOf`, `orderOf_eq_one_iff`). The proof is complete: s > 0 from the definition,
    division with remainder gives `s ∣ l`, and `s = 1 ⇔ ζ = 1`. The two uses (proofs of `sr:lem:root-cases`, line
    746, and `sr:lem:root-cases2`, line 769) read `n = ord(a)` and then use exactly what (P1) gives. Correct.
14. **Remark `sr:rem:main`** (lines 961-964). `heptagon_of_nontrivial_isometry_3`
    (`ReductionThreeClasses.lean:4292`) takes exactly `HalfTurn34`, `Threefold33`, `Fivefold35`, for the copied
    definitions (item 8). Correct.
15. **Remark `sr:rem:variant`** (lines 999-1007). Corollary 3 (`SYMMETRIC.md` lines 46-49) is per symmetry, assumes
    Theorems 1, 2, 5 and `C4CUT`, and "symmetry" includes affine bijections (lines 8-9): as stated. `cor:only` is at
    `WRITEUP/note/symmetric_es7.tex:95-99`. `VariantChecks.group_form` (`VariantChecks.lean:1168`) takes
    `Threefold33`, `Fourfold32`, `Fivefold35`, `MirrorOneAxis33`, `MirrorNoAxis34`, and S in general position,
    `33 ≤ |S|`, `¬HasConvexNGon 7 S`, and concludes: every invariant Euclidean isometry is `id`, or there is `c ∉ S`
    (with `2 ∣ |S|`, `34 ≤ |S|`, `halfTurn c` invariant) such that every invariant Euclidean isometry is `id` or
    `halfTurn c`. The paraphrase "the identity and at most one half-turn, whose centre is not in S" is accurate
    (it omits the size conjuncts, which is harmless). `logs/VariantChecks.out` line 15 gives the three standard axioms;
    `runs.tsv` hash `4b823bb6` equals the current file. "Lean-checked … with the same five classes as hypotheses":
    correct, not rounded up.
16. **Remark `sr:rem:mirror-line`** (lines 1028-1045). Byte identity of the bodies of `MirrorExclusionLineCopy`
    (1053-1054) and `Mir.MirrorExclusionLine` (`Line.lean:95-96`), and of the two `reflLine`s (item 6). Every
    mention of `Mir.` in `SYMLEAN/**/*.lean` is in a comment, so no Lean theorem in SYMLEAN identifies them. The `rfl`
    check whose file is not kept: `SYMLEAN/README.md` lines 178-180. `Line.lean:139` and `:147` are the two `Mir.`
    theorems. `V2L.mirrorExclusionLine_final` is at `V2-L/V2L/FinalTree.lean:28`; `V2-L/README.md` §9.6 gives the
    counts 1,198 (h1), 1 (hroot), 121 (hup), 74,000 (hleaves), each a cake_lpr verdict on a file; `WRITEUP/MIRROR.md`
    §1 (lines 47-50) uses the same "1 + 121 + 1,198 + 74,000 statements" wording, and `WRITEUP/CERTIFICATES.md` line
    359 says the proof files were not retained; `MIRROR.md` lines 98-101 and §6 items 2-4 say the file-to-term step
    is outside Lean. `Review.exclusionLine_of_mirrorOneAxis33` is at `ReviewSanity.lean:1593`. Correct.
17. **Remark `sr:rem:redundant`** (lines 1066-1067). An implied hypothesis can be dropped without changing the class;
    adding a hypothesis makes `∀S, H → C` weaker. Correct.
18. **Coverage** (lines 1105-1116). Pigeonhole (proof of `sr:lem:pigeon`), least prime factor (proof of
    `sr:lem:root-cases`) and complex square roots (proof of `sr:thm:structure`(b)) are indeed stated where used. The
    review files are cited only in the "Axioms and rigor" paragraph and in Remarks `sr:rem:sup`, `sr:rem:variant`,
    `sr:rem:mirror-line` (grep of "review/"; the Conventions paragraph names the namespaces `Review.` and
    `VariantChecks.`, not the files). Correct.

## 2. The map hunk

- Row `sr:lem:orbitFS`: Lean names and file:line reordered to match the new head.
- Row `sr:rem:mirror-line`: the new note agrees with the remark.
- Script check (`build/sr_p1diff/mapcheck.py`): 46 statement environments and 46 rows, labels, kinds, Lean names and
  file:line columns identical to the heads and in the same order; each of the 73 `\leanref`s points at the declaration
  line of the named declaration. Labels: the same 55 as in the snapshot, all prefixed `sr:`, no duplicates; all eight
  export labels still on their statements. `\ref` targets outside `sr:`: the ten allowed `fd:` labels and
  `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes`, `mb:thm:main3` (all contract export labels).

## 3. The fixer's log

| row | finding | fixer | audit |
|---|---|---|---|
| 1 | fidelity F1 (distinct `reflLine` constants) | fixed | confirmed (hunks 6, 16) |
| 2 | fidelity F2 (written proofs vs the H3 route) | fixed | confirmed (hunk 8) |
| 3 | fidelity F3 (namespaces of review names) | fixed | confirmed (hunks 2, 4, 15, 16) |
| 4 | fidelity F4 (Coverage "only in Remarks") | fixed | confirmed (hunk 18) |
| 5 | fidelity F5 ((P1) notation) | fixed | confirmed (hunk 13) |
| 6 | fidelity F6 (form of g) | fixed | confirmed (hunk 5) |
| 7 | fidelity F7 (copies in SYMLEAN/mirror) | fixed | confirmed by `diff` (hunks 8, 14); wording, see m2 |
| 8 | fidelity F8 (codomain strictly convex) | fixed | confirmed (hunk 12); see m1 |
| 9 | rigor m1 (Corollary 3) | fixed | confirmed (hunk 15) |
| 10 | rigor m2 (redundant hypotheses) | fixed | confirmed (hunk 17) |
| 11 | rigor m3 (overfull boxes) | fixed | confirmed: 0 overfull boxes (§4) |
| 12 | rigor m4 (reflection; fixed points) | fixed | confirmed with sympy (hunks 6, 7) |
| 13, 15, 18, 19, 20, 23, 24, 26, 28, 30 | duplicates | duplicate | each points to a fix confirmed above |
| 14 | rigor m6 (unpinned modules) | fixed | confirmed: hashes and closure (hunks 1, 2) |
| 16 | adversarial F2 (V2L theorem; H3 provenance) | fixed | confirmed (hunks 8, 16) |
| 17 | adversarial F3 (H6M; reductions A, B; normal forms) | fixed | confirmed (hunk 8) |
| 21 | adversarial F7 ("proved" → Lean-checked) | fixed | confirmed (hunk 15) |
| 22 | adversarial note (lrat-check caveat) | fixed | confirmed (hunk 8) |
| 25 | claims M3 (b) (`Function.` names) | fixed | confirmed (hunk 9) |
| 27 | claims M5 (two normal forms; optional LAYERLEAN pointer) | main point fixed, option declined | fix confirmed; declining the optional pointer is acceptable: the text stays true (the layer lemma has a written proof, `class_table.md` §1), and the reason given is sound |
| 29 | claims M7 (which Mathlib facts are restated) | fixed | confirmed (hunk 18) |
| 31 | writer concern (records not re-verified) | fixed | confirmed: I re-checked every record claim (hunk 8) |
| 32 | writer concern (formatting traps) | no action needed | agreed |

The "Other changes" 1-7 of the log were checked as part of the hunks above.

## 4. Compile check

`build/sr_p1diff_wrapper.tex` (same content as the contract's wrapper), two runs of
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error sr_p1diff_wrapper.tex` from `build/`: exit 0 both
times; no `!` error, no "Missing $", no multiply defined label, no hyperref warning; 15 pages. **Overfull boxes:
none.** Undefined references after the second run: only `fd:def:{point,orient,gp,cp,ngon,inv,rot}`,
`fd:lem:{collinear,cp-hull,mono}`, `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes`, `mb:thm:main3` (all
allowed). There are 65 underfull lines, all in statement heads and long name lists (the effect of the preamble's high
tolerance), none in the new remark text; not a finding. No machine path and no tool name in `sr.tex` or
`sr.map.tsv` (grep). No `\newcommand`, `\def`, `\usepackage` or section-local `\sloppy`.

## 5. Findings

**m1 (minor).** Proof of Theorem `sr:thm:structure`(a), lines 556-558 (also the map note of `sr:thm:structure`, "the
Mathlib theorems used in Lean", and Coverage line 1107, "Mathlib's theorems on isometries"). The text calls
`Isometry.affineIsometryOfStrictConvexSpace` "Mathlib's theorem … a theorem of Mazur–Ulam type". In Mathlib it is a
`noncomputable def` (`Mathlib/Analysis/Convex/StrictConvexBetween.lean:138`) that turns an isometry into an affine
isometry with the same underlying map (`coe_affineIsometryOfStrictConvexSpace`, line 149, by `rfl`). The described
content is right; only the kind of declaration is misnamed. Suggested wording: "applies Mathlib's construction of an
affine isometry from an isometry into a strictly convex space (\lean{Isometry.affineIsometryOfStrictConvexSpace}, a
result of Mazur–Ulam type that does not need surjectivity)".

**m2 (minor).** Remark `sr:rem:records`, mirror bullet, lines 276-279: "The file
SYMLEAN/mirror/ReductionThreeClasses.lean does not import SYMLEAN/SymmetricReduction.lean; its lines 38--1084 are
byte-identical to lines 12--1058 of that file, so the classes of that file are copies of those of
Definition sr:def:classes". The first "that file" is `SymmetricReduction.lean`; the second is meant to be
`ReductionThreeClasses.lean`, but read literally it is again `SymmetricReduction.lean`, whose classes are those of
the definition themselves. Suggested wording: "so the classes defined in ReductionThreeClasses.lean are copies …".

## 6. Checked and not reported

- `Mir.mirrorExclusionLine_of_cubes` (`Line.lean:147`) also has two `coverCheck … = true` hypotheses, so "derive …
  from hypotheses saying that certain CNF formulas are unsatisfiable" (line 1032-1034) is not the full list. The
  sentence does not say "only", it was in the passed version, and those hypotheses are decidable checks; not
  reported.
- `SYMLEAN/README.md` §9 (line 316) still says lrat-check and cake_lpr are both trusted, while `SYMMETRIC.md` §3 (revised
  6 November) trusts only cake_lpr. The remark cites §3 of `SYMMETRIC.md` for its trust sentence, so it follows the
  later record; the inconsistency is in the records, not in the section.
- "Lean-checked bookkeeping" for `cb:thm:c2` and `cb:thm:c3`: both are kernel evaluations that section `cb` also
  labels computer-assisted; calling them Lean-checked is accurate and does not round a label up.
- "Verdicts of both checkers recorded at solve time" (C2P–C2P5) and "recorded checker verdicts" (C3FINAL) agree with
  `SYMMETRIC.md` §3 ("each accepted by both checkers at solve time"), so the new general trust sentence (cake_lpr
  accepted it) applies to them.
- No new statement of the section corresponds to a changed Lean declaration; the only statement whose text changed
  is the written step (P1), which is correct.
