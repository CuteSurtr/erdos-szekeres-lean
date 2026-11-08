# Section `ll`, polish round 1: diff audit

Inputs: `snapshots/sections-r1pass/ll.tex` and `.map.tsv` (the version that passed the four-lens review, 760 lines)
against `sections/ll.tex` and `.map.tsv` (current, 792 lines); fixer log `reviews/ll-polish-r1-fix.md`; the round-1
reports `reviews/ll-r1-{fidelity,rigor,adversarial,claims}.md` and `reviews/ll-writer-concerns.md`. There are no
earlier polish audit reports for `ll`. Paths below are relative to the staging directory (`sections/`, `build/`),
to RES (`LAYERLEAN/...`, `C6UPPER/...`) or to the repository root (`ErdosSzekeres/...`).

**Verdict: PASS.** No blocker and no major finding; one minor finding (m1). Every hunk of both diffs was checked;
every touched statement was re-read against its Lean declaration; every new claim about records was checked against
the files under RES; every finding marked "fixed" is fixed correctly; every "declined" and "duplicate" is acceptable.

## 1. Method

- `diff -u` of both file pairs: 18 hunks in `ll.tex`, 2 changed rows in `ll.map.tsv` (notes only).
- Lean source: `LAYERLEAN/LayerLemma.lean` (SHA-256 `afb8542dceb0c170...` recomputed, 1148 lines), lines 1-470 and
  1020-1148 re-read.
- Records opened: `LEANEXT/review/{axioms.log, REPORT.md, tests_tail.lean, VacuityTest.lean, vacuity.log}`,
  `LAYERLEAN/logs/axioms.log`, `LAYERLEAN/logs/axioms_recheck_20261106/out.txt`, `C6UPPER/README.md` (head, status,
  addenda), `C7UPPER/README.md` (statement, encoders, certificate table), `WRITEUP/note/k8_soundness.tex` (head,
  soundness theorem, Corollary `k8s:cor:geom`, trust table, gaps (G1)-(G4) and trust items (E1)-(E6)),
  `ENCBLEAN/geo/ES8Geo/{Main,Capstone2,Audit}.lean` and the imports of every `ES8Geo` file, `ENCBLEAN/EncB/Cover.lean`,
  `ENCBLEAN/EncB/Coded.lean`, `ENCBLEAN/geo/{lean-toolchain, lake-manifest.json}`.
- Mathlib: a local checkout whose git HEAD is the pinned revision `f897ebcf72cd16f8...` (`Set.extremePoints`,
  `Convex.mem_extremePoints_iff_convex_diff`, `extremePoints_convexHull_subset`, `IsCompact.extremePoints_nonempty`,
  `closure_convexHull_extremePoints`, `Nat.iterate`, `Function.iterate_succ'`, `Function.iterate_add`).
- Scripted checks: theorem names of the Lean file against the names in `LEANEXT/review/axioms.log`; the seven
  `@[simp]` names against all three axiom logs; `Sixfold66`/`Sevenfold70` over every `.lean` file of the repository;
  `diff` of `LayerLemma.lean` lines 37-1147 against `ENCBLEAN/geo/ES8Geo/Capstone2.lean` lines 45-1155; SHA-256 of both
  copies of `ErdosSzekeres/Definitions.lean`; label, `\ref` and `\leanref` sets of old against new file; map columns;
  forbidden strings.
- Compile: own wrapper `build/ll_p1diff_wrapper.tex` (contract content), `nice -n 15 pdflatex` twice; pages 1-2, 4-6
  and 9-10 of the PDF inspected.

## 2. Hunk by hunk (line numbers of the current `sections/ll.tex`)

| # | lines | change | result |
|---|---|---|---|
| 1 | 1 | `\texorpdfstring{$mt$}{mt}` in the section title | correct; hyperref is loaded by the preamble (line 11), not a new macro; no "Token not allowed" warning remains |
| 2 | 8-12 | intro: "for every hull vertex x the hull vertices are exactly x, f(x), ..., f^{m-1}(x), so that, if S is nonempty, they form a single f-orbit" | matches `hullVerts_eq_orbitFS` (189): `hullVerts S = orbitFS f m x` for every `x ∈ hullVerts S`; for S nonempty hv(S) is nonempty (139) and f^m x = x, so the set is the whole orbit of x. Correct |
| 3 | 22 | treated lines "1--469 and 1034--1148" | correct: `rotAbout_iterate` occupies 465-469, 470 is blank, 471 opens the docstring of `orient_rotAbout`, 1032 ends `dist2_le_of_later`, 1034 is the header of section 12, 1148 is `end ErdosSzekeres.LayerLemma` |
| 4 | 34-53 | Lean-evidence paragraph rewritten | every claim checked, see section 3 |
| 5 | 68-72 | (C2): Lean's `Nat.iterate` uses f^{i+1} = f^i ∘ f; same maps (`Function.iterate_succ'`); f^{i+j} = f^i ∘ f^j (`Function.iterate_add`) | correct at the pin: `Nat.iterate` is `succ k, a => iterate op k (op a)`; `iterate_succ' : f^[n.succ] = f ∘ f^[n]`; `iterate_add : f^[m + n] = f^[m] ∘ f^[n]` |
| 6 | 87-90 | (C4) is Mathlib's definition at the pin; the swap gives x_2 = x | correct: at f897ebcf `Set.extremePoints A = {x ∈ A \| ∀ x₁ ∈ A, ∀ x₂ ∈ A, x ∈ openSegment 𝕜 x₁ x₂ → x₁ = x}`; the open segment is symmetric, so applying the condition to (x_2, x_1) gives x_2 = x |
| 7 | 105 | "For t ∈ N" (typo) | correct |
| 8 | 182 | "As in Lean:" for `mem_hullVerts`/`hullVerts_subset` | correct (114: `simp only [hullVerts, Finset.mem_filter]`; 118: `(mem_hullVerts.1 hx).1`) |
| 9 | 199-203 | how Lean proves (b), (c), (d) | correct: (b) uses `extremePoints_convexHull_subset` and `Convex.mem_extremePoints_iff_convex_diff` (`x ∈ A.extremePoints ↔ x ∈ A ∧ Convex (A \ {x})`, quoted with "x ∈ C" now); (d) uses (b) and `IsCompact.extremePoints_nonempty` (Mathlib docstring "Krein-Milman lemma"); (c) uses (b) and `closure_convexHull_extremePoints` ("Krein-Milman theorem") |
| 10-12 | 303, 430, 464 | short names "invariance of S∖hv(S)", "invariance of S∖{c}", "layer lemma, rotations" | heads only; Lean names, lines, labels and statement bodies unchanged; statements re-read against lines 217, 325, 364: faithful (0<m, maps-into, f^[m] y = y; any real θ; 0<m, K≤2m, c∉S, invariance, K-free, ∀ x ∈ hv S). The names describe the statements correctly |
| 13 | 495-496 | "As in Lean:" for `peel_succ`/`peel_subset` | correct (378: `rfl`; 381: the same recursion with `sdiff_subset`) |
| 14 | 609 | `\texorpdfstring` in the subsection title | correct |
| 15 | 622-625 | "(H) ... no theorem of LayerLemma.lean proves it; in the two applications it is supplied by Sixfold66 and Sevenfold70, themselves hypotheses" | correct: the only theorems of the file concluding `HasConvexNGon` are `hasConvexNGon_of_fan` (700, conclusion at 704, a fan configuration), `convexNGon_of_layers` (takes H) and the two octagon theorems (take Sixfold66/Sevenfold70); the Lean proofs at 1129-1130 and 1142-1143 instantiate H from the hypothesis exactly so |
| 16 | 709-737 | Remark `ll:rem:hyp`, first two paragraphs | all claims checked, see section 3; one minor imprecision (m1) |
| 17 | 764-766 | Coverage: Lean uses two Mathlib facts for (b), Krein-Milman theorem for (c), lemma for (d) | correct, consistent with hunk 9 |
| 18 | 791-792 | "Step 2 of our proof of Theorem ll:thm:sixfold uses it" | correct: Step 2 cites Lemma `ll:lem:rot`(d); the Lean proof of `sixfold_octagon` calls `centre_not_mem_of_even`, not `rotAbout_iterate` |
| tsv | rows 7, 31 | notes of `ll:lem:hv` and `ll:rem:hyp` | consistent with hunks 9, 16, 17; 31 rows, 5 tab-separated fields each, labels/kinds/names/lines unchanged |

## 3. Record claims of the new text (all confirmed)

Lean-evidence paragraph:
- `LEANEXT/review/axioms.log` has 59 axiom lines; the sorted names equal the sorted names of the 59 unindented
  `theorem` declarations of `LayerLemma.lean` that are not `@[simp]` (empty diff; 66 theorems, 7 of them `@[simp]` at
  lines 236, 237, 238, 239, 241, 244, 254). 58 lines report `[propext, Classical.choice, Quot.sound]`, `iterate_mem`
  reports `[propext, Quot.sound]`.
- The seven `@[simp]` lemmas (`toC_re`, `toC_im`, `ofC_zero`, `ofC_one`, `toC_ofC`, `ofC_toC`, `toC_crot`) are all in
  Lemma `ll:lem:complex`(a)-(b) and occur in none of the three logs (fixed-string count 0 in each).
- Their proofs (236-255): four `rfl`; `toC_ofC` is `apply Complex.ext <;> rfl`; `ofC_toC` is
  `funext i; fin_cases i <;> rfl`; `toC_crot` is `toC_ofC _`. The summary in the text is accurate.
- `REPORT.md`: review dated 4 November 2026 (KST), reviewed file `LayerLemma.lean` with SHA-256 `afb8542d…`, 1148
  lines. It lists `AxiomsCheck.lean` among the hand-back files, but no file of that name exists anywhere in the
  repository, and the kept `tests_tail.lean` and `VacuityTest.lean` print axioms only for the five `Review.*` tests.
  So "the check file from which the axioms were printed is not kept in the record" is correct.
- No `sorry`, `admit`, `axiom`, `native_decide` in the file; the only `decide` is at line 1125 (`Even 6`).
- `rotAff` (311) is a `def` whose `map_vadd'` field is a tactic proof, as stated.

Remark `ll:rem:hyp`:
- `Sevenfold70` occurs in `.lean` files only as `def Sevenfold70 : Prop` (in the copies of the layer file) and as the
  hypothesis of `sevenfold_octagon`: no theorem concludes it.
- The only theorems whose conclusion is `Sixfold66` are `sixfold66_of_no_model` (78), `sixfold66_of_unsat` (87) and
  `sixfold66_of_cubes64` (91) of `ENCBLEAN/geo/ES8Geo/Main.lean`, each with a hypothesis. The `Audit.lean` hits are
  `#guard_msgs` texts.
- `EncB.Geo.sixfold66_of_cubes64 (h : EncB.CubesUnsat64) : Sixfold66` exists under this full name (namespace
  `EncB.Geo`; `Audit.lean:99` prints `EncB.CubesUnsat64 → ErdosSzekeres.LayerLemma.Sixfold66`).
- `EncB.CubesUnsat64` (`ENCBLEAN/EncB/Cover.lean:110`) is
  `∀ c ∈ cubes64, ¬DimacsSatisfiable (cubeCnf (encB 6 8 11) c)`, with `length cubes64 = 64`; `EncB.encB` is a Lean
  definition (`ENCBLEAN/EncB/Coded.lean:330`, namespace `EncB`). The description is accurate.
- `def Sixfold66` occurs in `ENCBLEAN/geo` only at `ES8Geo/Capstone2.lean:1110`; import chain Main → ModelOfLabelling →
  Labelling → Interface → Capstone2. Lines 45-1155 of Capstone2 are byte-identical to `LayerLemma.lean` lines 37-1147
  (namespace line to the last declaration; empty diff). `ENCBLEAN/geo/ErdosSzekeres/Definitions.lean` and the
  repository's `ErdosSzekeres/Definitions.lean` both have SHA-256 `2425500eefd181ad...`; Definitions.lean imports Mathlib
  only, and `ENCBLEAN/geo` pins Lean v4.24.0 and Mathlib `f897ebcf`. So the identification of the two `Sixfold66`
  propositions is sound.
- C6UPPER: "Every configuration of 11 nested regular hexagons about a common centre, in general position, contains 8
  points in convex position"; cake_lpr verdicts on cube formulas; the cover checked by `tools/verify_cover.py` and
  `verify_final64` (README status and addenda).
- C7UPPER: two separately implemented encoders, "encoder A + H(1)" and "encoder B", each `VERIFIED UNSAT` by
  cake_lpr (README §2-3). The parenthetical "one of them with an added symmetry-breaking unit clause" is correct.
- Rigor label `certificate` for the unsatisfiability of the formulas: k8_soundness trust table, row "Unsatisfiability
  of the formulas & certificate".
- k8_soundness covers the symmetry breaking (subsection "The reflection unit", Lemma `k8s:lem:refl`) and the cube cover
  (subsection "The cube cover and the passage to geometry", Lemma `k8s:lem:cube`).
- (G1)-(G4) are summarised faithfully: (G1) code-to-clause correspondence by reading the code; (G2) passage from a
  DIMACS file to Sixfold66/Sevenfold70 is a written proof (Corollary `k8s:cor:geom`); (G3) encoder A's angular part
  rests on binary64 arithmetic; (G4) several written proofs have had no internal review.
- (E1)-(E6) are listed under (G2). (E1) is the identity of the printed texts with the certified cube files; (E2)-(E3)
  are the verdicts and their reading as unsatisfiability. The sentence "Neither ... nor ... is Lean-checked; both
  rest on the trust items (E1)-(E6)" is accurate. The link between the texts and `CubesUnsat64`
  (`texts_iff_cubesUnsat64`) is Lean-checked, and the text does not say otherwise.

Rigor vocabulary: "proved" occurs only as "not proved" (lines 18, 52, 658, 664, 694). No "verified" or "certified".
No hypothesis is presented as proved. The new text says the unsatisfiability results are *certificate*, the soundness
step is a written proof (not refereed) with open gaps, and ENCBLEAN is "a Lean derivation" that assumes
`EncB.CubesUnsat64`. Nothing is rounded up.

## 4. Fixer log: fixed, declined, duplicate

Fixed, and confirmed fixed correctly: F M1 (hunk 15); F M2 (hunk 4; the usage claim is gone, the unprinted lemmas
and their proofs are described); F M3 = R M2 first part = A m3 = C m4 = W 6 (hunks 9, 17, tsv row 7); F M4 = R M6 =
A m6 (hunk 2); F M5 = R M7 = A §5 (hunk 4); F M6 = R M1 = A m1 = C m1 = W 1 = W overfull list (0 overfull boxes, and
the three heads were shortened); R M2 second part ("x ∈ C and", hunk 9); R M3 (hunk 5); R M4 = C m3 gaps (hunk 16);
R M8 = A m8 = C m5 claim 1 (hunk 4: only lemmas and theorems are Lean-checked; `rotAff` explained; definitions are
not claims); A m2 (hunk 7); A m5(ii) = C m3 ENCBLEAN (hunk 16); A m7 (hunk 6). The adversarial reviewer's premise that
Mathlib asks "x_1 = x and x_2 = x" is not true at the pin, and the fixer's clarification states the pinned definition
correctly. C m2 nit ("for each printed theorem", hunk 4); C m5 claim 2 (hunks 8, 13; every other lemma or theorem
proof already says whether it follows Lean); C m6 (hunks 1, 14); W 7 (every claim of the remark checked, section 3).
The fixer's "other changes" 1-7 are all correct (hunks 3, 10-12, 18, 16, 4, tsv).

Duplicates: R M5, A m4 (to F M1); R M6, A m6 (to F M4); R M7, A §5 (to F M5); C m1, R M1, A m1, W 1, W overfull (to
F M6); and the others listed above. Each points to a finding that is fixed, and the fix also meets the duplicate's
own suggestion (for R M5: the remark now states that no Lean theorem proves Sixfold66 unconditionally and none
concludes Sevenfold70). Acceptable.

Declined, all acceptable:
- W 2. `\lean{}` with spaces: `ll.tex` has no `\lean{...}` argument containing a space, so nothing prints run
  together.
- W 3. `rotAbout_iterate` is in range and covered.
- W 4. The export list is fixed by the contract, and `ll:cor:decomp` is labelled a written step.
- W 5. `lg:lem:centre` in the current `sections/lg.tex:485-488` takes 0 < m, m even, invariance under
  rotAbout(c, 2π/m), general position, p ∈ S and p ≠ c, and concludes c ∉ S. That is exactly what Step 2 supplies.

## 5. Compile check

`build/ll_p1diff_wrapper.tex` (contract content), from `build/`,
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice:
- Both passes exit 0 (10 pages).
- No `!` error, no "Missing", no undefined control sequence, no "Label(s) may have changed", no hyperref
  "Token not allowed".
- Undefined references: only the ten allowed `fd:` labels, plus `lg:lem:centre` and `lg:thm:nesting`.
- Overfull boxes: 0 of any size, so none above 1pt.
- The 51 underfull boxes are all in statement heads with long `\leanref` lists. They are the intended effect of the
  preamble's statement tolerance. The rendered heads are within the margins: the three shortened heads take two lines
  each on pages 4-6, and no Lean name or line number is clipped.

Label set, `\ref` set and `\leanref` list are identical to the passed snapshot. There are 31 statement environments
for 31 map rows, and 21 proofs. No machine path, tool name, `\newcommand` or `\usepackage` appears in
`ll.tex` or `ll.map.tsv`.

## 6. Findings

**m1 (minor, small imprecision in the new provenance text): `sections/ll.tex:719-723` (Remark `ll:rem:hyp`, second
paragraph).**
- *What the text says.* C6UPPER "gives the unsatisfiability of SAT encodings ... by cake_lpr verdicts on cube
  formulas whose cover is checked there". No qualification follows. For C7UPPER, the next clause says that one of
  the two encodings carries "an added symmetry-breaking unit clause".
- *Why it is imprecise.* The same holds at m = 6:
  - Encoder A's certificate is for F_A(6,8,11) plus the unit Y(1,2), through 32 cubes.
  - Only encoder B's base formula is certified on its own, through 64 cubes.
  - Sources: `C6UPPER/README.md`, addendum of 6 November ("Encoder A, the cross-check, still uses the unit Y(1,2)");
    `WRITEUP/note/k8_soundness.tex:702-704` ("At (6,8,11) the certificate for B is also for F_B alone, through 64
    cubes, and the one for A is for F_A plus Y(1,2), through 32 cubes").
- *Effect.* Because the qualification is given for C7UPPER and omitted for C6UPPER, a reader may conclude that no
  C6UPPER certificate uses symmetry breaking. Nothing false is asserted about the section's own results, which are
  conditional, and the next sentence says the note covers the symmetry breaking.
- *Fix.* Add, e.g., "(for encoder B the formula itself, by 64 cubes; for encoder A the formula with the added
  symmetry-breaking unit Y(1,2), by 32 cubes)" after "whose cover is checked there".

## 7. Checked and not findings

- The new phrase "(over a byte-identical copy of `ErdosSzekeres/Definitions.lean`)" is correct (SHA-256 identical).
  It refers to a repository-root path, as the contract requires.
- "The seven `@[simp]` lemmas are printed in none of the three logs", followed by "So no statement of this section
  depends on `sorryAx`, ...": the conclusion now follows from stated premises, namely the logs for the 59 printed
  theorems, the described `rfl`/extensionality proofs for the seven unprinted lemmas, and the source scan.
- The map note "(b)-(d) proved by elementary arguments" (row 7) was already in the passed version. It describes this
  document's written proofs and claims no stronger label.
