# Review fd, round 2, lens: claims, labels and LaTeX

Section: `sections/fd.tex` (1189 lines) and `sections/fd.map.tsv` (header + 40 rows).

**Verdict: pass.** No blocker and no major finding; there are four minor findings (m1 to m4). Both round-1 major
findings are fixed. All 20 contract statements of fd are true and match their Lean declarations, so there is no
contract discrepancy.

Path conventions in this report:
- Paths starting with `sections/`, `build/` or `reviews/` are relative to the staging directory.
- `LAYERLEAN/...`, `SYMLEAN/...`, `LEANEXT/...` and `MIRRORETV/...` are relative to RES.
- `ErdosSzekeres/...`, `docs/...`, `lean-toolchain` and `lake-manifest.json` are relative to the repository root.

Mathlib was read from a checkout at `f897ebcf72cd16f89ab4577d0c826cd14afaafc7` and Lean core from the 4.24.0
toolchain, both read only. Nothing under REPO was modified. Lean, lake and solvers were not run. Only read-only git
commands were used.

## 1. Round-1 major findings

Both round-1 majors (fidelity F1 and claims M1) concerned the same issue, and both are **fixed**:

- **fd:lem:affine-orient is now tagged with `ErdosSzekeres.SymReduction.orient_affine`** at
  `SYMLEAN/AffineReduction.lean:1241`.
  - The declaration sits at that exact line, in namespace `ErdosSzekeres.SymReduction`, opened at :54.
  - The statement now matches the Lean hypothesis, "g is a map with g(x)=Ax+v for every x".
  - The Lean form is spelled out in the lemma, and (i) and (ii) are marked as written steps.
  - The verbatim copy at `SYMLEAN/mirror/ReductionThreeClasses.lean:1267` is named. A diff of the 8 lines,
    docstring included, is empty.
- **fd:lem:affine-cp now carries the general Lean forms (b′)–(e′)**, with five `\leanref`s at
  `SYMLEAN/AffineReduction.lean:1263/1278/1290/1298/1305`. Each statement was compared with the source:
  - (b′) `convexPosition_image_affine`: injective Mathlib `AffineMap`.
  - (c′) `generalPosition_image_affine` (`g p = L *ᵥ p + b`, `L.det ≠ 0`) and
    `generalPosition_image_affineEquiv` (`Point ≃ᵃ[ℝ] Point`).
  - (d′) `hasConvexNGon_image_affine`.
  - (e′) `injective_of_affine`.

  All five match. Part (a) is correctly identified as Mathlib `AffineMap.image_convexHull`. Its Mathlib proof, read
  in the checkout, is the same two-inclusion argument the section gives.
- **The false sentences are gone.**
  - "Lean proves the special cases it needs separately" and "Written steps without a single Lean counterpart" no
    longer occur (grep).
  - The new Remark fd:rem:orient-lean correctly identifies `OrbitConsistency.orient3_perm`
    (`LEANEXT/orbit/OrbitConsistency.lean:178`, `∀ t, orient3 (t ∘ σ) = sign σ * orient3 t`) as the case R = ℝ of
    (d). The index translation σ = s⁻¹πs was checked.
- **The new evidence was checked in the logs.**
  - `SYMLEAN/logs/runs.tsv`:
    - line 4: `AffineReduction.lean`, prefix `41cfc0b6`, exit 0, 0 output lines.
    - line 5: `AffineReductionAxioms.lean`, prefix `f6cb9372`, exit 0. This prefix equals the current file's
      SHA-256.
  - The first 1533 lines of `AffineReductionAxioms.lean` are byte-identical to the current `AffineReduction.lean`.
  - `SYMLEAN/logs/AffineReductionAxioms.out` lists, each with `[propext, Classical.choice, Quot.sound]`:
    - lines 9–11: `heptagon_of_nontrivial_affine_coords`;
    - lines 13–15: `generalPosition_image_affineEquiv`;
    - line 16: `hasConvexNGon_image_affine`.
  - Each claimed use site lies inside the claimed proof:
    - :1528 is in `heptagon_of_nontrivial_affine_coords`;
    - :1462 is in `hasConvexNGon_of_affine_coords_symmetry`;
    - :1295 is in `generalPosition_image_affineEquiv`;
    - :1281 is in `generalPosition_image_affine`;
    - :1303 is in `hasConvexNGon_image_affine`.

## 2. Fresh pass: what was checked, and the result

1. **Compile.**
   - Command, from `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error
     -output-directory=claims-fd-r2 fd_wrapper.tex`, run twice.
   - Both passes exit 0, and the PDF has 15 pages.
   - The log has no `!` error, no "Missing $", no hyperref or font warning, no multiply-defined label and
     0 overfull boxes. There are many underfull boxes, which are cosmetic and come from `\sloppy`/`\raggedright`.
   - The only undefined references are `ll:def:hv`, `ll:def:peel` (input line 92), `ll:def:66-70` (369),
     `oc:lem:perm` (492) and `oc:lem:rot-inv` (554). All five are export labels of ll and oc in the contract, and
     nothing else is undefined.
   - The environment words fd uses for them match the target environments: "Definitions" for `ll:def:hv` and
     `ll:def:peel`, "Definition" for `ll:def:66-70`, and "Lemma" for `oc:lem:perm` and `oc:lem:rot-inv`.
2. **LaTeX rules.**
   - The file starts with `\section{Conventions and foundations}\label{fd:sec}`.
   - It contains no `\newcommand`, `\def`, `\let`, `\usepackage`, `\input` or `\documentclass`.
   - The environments used are definition (9), lemma (23), remark (8), proof (23), and enumerate, itemize,
     equation*, pmatrix, center and tabular.
   - Every label starts with `fd:`, and there are no duplicate labels.
3. **Machine paths and tool names.**
   - `fd.tex` and `fd.map.tsv` were grepped for `/private`, `/Users`, `/home`, `/tmp`, the scratch directory, the user name,
     and the names of tools, solvers and checkers. There are no hits.
   - Both files are pure ASCII.
4. **Overclaiming words.**
   - Grep for verif*, certif*, proved/proven, establish, confirm, rigorous, guarantee, "exactly as written" and
     "formally" finds only allowed uses:
     - "not proved in Lean";
     - the label definitions;
     - "(such as ``verified'' or ``certified'')" in the sentence that says these words are not used;
     - "certificate" for exact rational and integer checks and for the `linear_combination` coefficient;
     - "proved here" for the written proofs.
   - See m2 for one framing sentence.
5. **Export labels.** All 20 contract labels are defined once each, on the named statements. Their line order
   (227 … 1079) follows the contract order exactly:
   - `fd:def:{point,orient,gp,cp,ngon,forces,inv,rot}`;
   - `fd:lem:{orient,affine-orient,collinear,cp-hull,mono,affine-cp,caratheodory,four-subsets,four-positive,
     pos-triples,pos-cycle,separation}`.
6. **`\ref` targets.**
   - Every `\ref` in fd is an fd label or one of the five ll/oc export labels above.
   - In the other sections, every `\ref{fd:...}` points to a label that fd defines. All of them are contract export
     labels; no section refers to a non-exported fd label.
7. **Statement map.**
   - The header is as required, there are 41 lines of 5 tab-separated fields each, and the line endings are LF.
   - A script compared the 40 statement environments of the section (9 definitions, 23 lemmas, 8 remarks) with the
     40 rows: they match in order, label and kind.
   - Every row with Lean names was checked against the source: each name is declared at the cited line, in the
     stated namespace, with a declaration keyword. There are 0 mismatches.
8. **Lean names and lines.**
   - All 49 `\leanref`s were checked by script. Each declaration keyword sits exactly at the cited line, and the
     namespace-qualified name equals the cited name. There are 0 mismatches.
   - Every in-text `\dirn{file:line}` was opened and lands on the stated declaration or step (42 citations). These
     include `Reflection.lean:6/34/42/43/44/47/52/55/64`, `LayerLemma.lean:162/165/325/330/368`,
     `OrbitConsistency.lean:117/168/178` and `ConvexCycleCuts.lean:8/31`.
   - The use sites cited as evidence were confirmed to lie inside the claimed enclosing theorems, using a scan for
     the enclosing declaration:
     - `Construction.lean:54` is in `exists_cupCapFree` and :118 is in `conjecturedBound_le_of_forces`;
     - `OrientationObstructions.lean:64/68` are in `Omission.Configuration.orient_ne_of_distinct`;
     - `SpikeChain.lean:140` is in `AdjacentCapFrames.glue_chain_caps`;
     - `VisibleEdgeInsertion.lean:77` is in `convexPosition_insert_of_one_visible_edge`, with `open Suk`, and the
       name is unique in the library;
     - `FiniteDensityBound.lean:66` is in `horizontal_finite_density_bound`;
     - `MirrorMain.lean:2520` and `ReductionThreeClasses.lean:4079` are in `mirror_odd_general`.
   - The Mathlib names exist in the pinned checkout: `Collinear` (`Module.rank k (vectorSpan k s) ≤ 1`),
     `ConvexIndependent` (`∀ s x, p x ∈ convexHull (p '' s) → x ∈ s`),
     `convexIndependent_set_iff_notMem_convexHull_diff`, `collinear_iff_of_mem`, `AffineMap.image_convexHull`,
     `Caratheodory.minCardFinsetOfMemConvexHull`, `Function.iterate_succ_apply'`, `Function.minimalPeriod` (0 for a
     non-periodic point), `ConvexIndependent.mono`, `vectorSpan` and `AffineIndependent`. Each is restated
     faithfully.
9. **Fidelity of the contract statements.**
   - Each Lean-tagged statement was compared with its declaration: Definitions.lean, Orientation.lean,
     OrientationGeometry.lean (1–91), Basic.lean, FourPoint.lean, SupportingLines.lean, OrientationClique.lean
     (1–47), ConvexCycleCuts.lean, Reflection.lean, the three `Invariant` and `rotAbout` copies,
     `iterate_mem`, `rotAbout_eq_crot`, `rotAff`, `rotAbout_iterate`, `rotAbout_injective`,
     `MirrorOdd.hasConvexNGon_of_le` and the AffineReduction theorems.
   - Hypotheses, strictness, Finset/Set and quantifier order all match. In particular:
     - `convexPosition_of_positive_triples`: `4 ≤ s.card` and p injective on all of ι;
     - `hasConvexNGon_of_positive_cycle`: all increasing triples of the embedding e;
     - `convexPosition_of_strict_supports`;
     - `orient_support_sum` (`orient p (p + b - a) r`).
   - The key identities were rechecked with a short sympy script (`build/claims-fd-r2/sym_check.py`, all True):
     - orient (a)–(d), including all six permutations;
     - the affine formula, rotation invariance, and (e) and (f) of fd:lem:rot;
     - det F_φ = −1, F_φu = u and F_φu⊥ = −u⊥;
     - the `orient_affine_combination` identity with the coefficient (p₁q₀−p₀q₁)(u+v−1);
     - `orient_support_sum`;
     - all twelve support values of fd:lem:four-positive.

   No fd contract statement is false or mismatched.
10. **SHA-256.** All 15 prefixes in the sources table were recomputed with `shasum -a 256`, and all are correct.
    This includes the new `SYMLEAN/AffineReduction.lean` `41cfc0b60aec`. The short prefixes `6d5ec90a` and
    `41cfc0b6` in the axioms paragraph are also correct.
11. **Axioms and build logs.** Each cited log was opened and the cited lines read:
    - `docs/validation/axiom-audit-lower-bound-2026-10-11.txt`:
      - lines 87, 88, 103, 113, 114, 119, 132, 175, 176, 178, 624, 720, 725 and 732 name the stated declarations,
        each with the three standard axioms;
      - line 49 starts the three-line entry of `convexPosition_insert_of_one_visible_edge`.
    - Read-only git checks:
      - HEAD is `7e32ee25931883f2…` on branch `es7-night-2026-11-01`;
      - `7f0868fdb` (11 Oct 2026) added the audit;
      - `git diff 7f0868fdb HEAD` is empty for every main-library file named in the paragraph, for the four
        Vendor/ErdosSzekeresConvex files, and for `lean-toolchain` and `lake-manifest.json`.
    - `docs/VALIDATION.md:73` reads "The maintained library builds all 3,308 jobs with `--wfail`", under the
      heading dated 11 October 2026.
    - The main-library import closure of Basic, Suk/OrientationClique and Suk/Reflection is exactly the table files
      plus BaseOrder, BaseChart, TriangleOrder, CupsCaps and the four Vendor files, as stated. A grep of all of them
      finds no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by` or `unsafe`.
    - `LAYERLEAN/logs/build.log`: exit code 0, 0 message lines.
    - `LEANEXT/review/axioms.log`: line 1 `iterate_mem` with [propext, Quot.sound]; lines 22, 23, 26 and 33 as
      stated. `LEANEXT/review/REPORT.md` ties this log to `LayerLemma.lean` SHA `afb8542d…` (1148 lines), the
      current file.
    - `LEANEXT/orbit/logs/build.log` reads `exit=0`. `LEANEXT/orbit/logs/axioms.log` has `orient_rotAbout_inv` on
      line 1 and `orient3_perm` on line 5, with the three standard axioms. `REPORT.md` there names SHA `9b843180…`,
      429 lines, the current file.
    - `MIRRORETV/lean/MirrorMain.out` line 858 is `mirror_odd_general`. The file has 0 errors and 121 warnings,
      and `MIRRORETV/SHA256SUMS` lists `ca623e55…` for `MirrorMain.lean`.
    - `SYMLEAN/mirror/axioms.out` line 11 is `mirror_odd_general`, and `SYMLEAN/mirror/README.md:49-50` records
      exit 0 and no errors.
    - A grep of the six cited research files finds no `sorry`, `admit`, `axiom` or `native_decide`.
12. **Reading conventions required by the scope.** All are present:
    - the purpose paragraph (:3–14): human-readable proofs, the Lean checks remain the primary evidence, not
      refereed;
    - the commit `7e32ee259`, matching HEAD;
    - Lean 4.24.0 (`lean-toolchain`: `leanprover/lean4:v4.24.0`) and Mathlib `f897ebcf`, whose full hash matches
      `lake-manifest.json`;
    - the package name `erdos_szekeres`, matching `lakefile.toml`;
    - the three rigor labels;
    - explicit casts `(m:ℝ)`, `x/0 = 0` and truncated subtraction (:74–84).

    The `native_decide` axioms were checked in Lean 4.24.0 `Init/Core.lean`: :2340 `axiom trustCompiler`,
    :2363/2375 `have := trustCompiler` in `reduceBool`, and :2392 `axiom ofReduceBool`. Naming both axioms is
    therefore accurate. No Stage-1 file actually uses `native_decide`: the hits in C3LEAN, V1-L, V2-L and
    ENCBLEAN/EncB are comments saying it is not used.
13. **Path convention, tested on the whole document.**
    - All 267 distinct (section, path) pairs cited by all 11 sections were resolved under fd's rule: root-relative
      for `ErdosSzekeres/`, `docs/`, `experiments/`, `scripts/` and the three root files, RES-relative otherwise.
    - Every path resolves except bare file names after a full citation (allowed by fd), `.../` placeholders, and the
      RES directory name itself.
    - Every research directory with its own `lean-toolchain` pins v4.24.0, and every manifest pins Mathlib
      `f897ebcf`.
14. **Hypotheses.**
    - `Sixfold66` and `Sevenfold70` appear only as "propositions" in Remark fd:rem:angles, and their definitions use
      real numerals `2 * Real.pi / 6` and `/ 7` (`LAYERLEAN/LayerLemma.lean:1104,1109`).
    - SAT verdicts appear only as an example of unproved hypotheses (:13).
    - No fd statement depends on a hypothesis or on a computation. The use of `decide` in
      `convexPosition_of_positive_triples` (Fin 4 order facts and `univ = {0,1,2,3}`, OrientationClique.lean:23,
      28–31) is described correctly, and the statement is correctly not labelled computer-assisted.
15. **Other factual claims.**
    - "19 definitions of `rotAbout`, all with this same body": the grep count in RES is 19, and all bodies are
      identical.
    - The three `Invariant` copies are textually identical.
    - `convexIndependent_of_affineIndependent` is used only at Basic.lean:64.
    - The "Deliberately not covered" list is complete for the nine main-library files in the table: every
      declaration is covered, named in a remark or proof, or listed.
    - `docs/SAT.md:168–233` is the vertical and full-plane coordinate-repair passage, which mentions the
      linear-arithmetic and nonlinear solver cuts and `convexCycleCut_of_avoids`.
    - The `orient` over ℤ claim holds (`ErdosSzekeres/IntegerCertificates.lean`).
    - Rudin, *Principles of Mathematical Analysis*, 3rd ed.: Theorem 2.41 is Heine–Borel in ℝᵏ and Theorem 4.16 is
      the extreme value theorem. Both are correctly cited.

## 3. Findings (all minor)

### m1 (minor): fd:lem:affine-orient(i) has an exact Lean counterpart, but the head and Coverage call it a written step or a "special case"

- **Where.**
  - fd.tex:504, the head "(i), (ii) written step".
  - fd.tex:1149–1154, Coverage: "No Lean declaration states the following statements or parts in the form given
    here; … parts (i) and (ii) of \ref{fd:lem:affine-orient} (Lean special cases
    \lean{OrbitConsistency.orient_rotAbout_inv} and \lean{Suk.orient_reflectY}, …)".
  - Map rows `fd:lem:affine-orient` (note "(i),(ii) written step") and `fd:rem:affine-orient-lean` (note "Lean
    special cases: (i) rotations …").
- **Evidence.**
  - (i) reads: for all o,a,b,d ∈ ℝ² and θ ∈ ℝ, orient(ρ_{o,θ}a, ρ_{o,θ}b, ρ_{o,θ}d) = orient(a,b,d).
  - `ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv (c : Point) (θ : ℝ) (a b d : Point) : orient (rotAbout c θ
    a) (rotAbout c θ b) (rotAbout c θ d) = orient a b d` (`LEANEXT/orbit/OrbitConsistency.lean:117`, axioms.log
    line 1) states exactly this. fd:def:rot makes the three `rotAbout` copies the same ρ.
  - fd's own Remark fd:rem:affine-orient-lean (:551–555) says "Invariance of orient under rotAbout, that is, (i),
    is …orient_rotAbout_inv". Section oc states the same theorem as Lean-checked `oc:lem:rot-inv`.
  - By fd's rule at :67–69, "written step" means "not Lean-checked". The document therefore labels one statement
    two ways.
  - This is an under-claim, not an overclaim. It is minor because the remark names the theorem correctly and the
    contract export label carries its own exact tag (`orient_affine`).
- **Fix.**
  - Tag (i) in the head: `…; (i) \leanref{ErdosSzekeres.OrbitConsistency.orient_rotAbout_inv}{LEANEXT/orbit/
    OrbitConsistency.lean:117}; (ii) written step`.
  - Update the map rows to match.
  - In Coverage, move (i) to "Covered", or at least replace "Lean special cases" with "exact counterpart of (i);
    special case of (ii)".
  - Small related point: Coverage (:1157–1158) lists "the composition law of (c)" as a written step, while the
    body (:391–392) also marks "ρ₀ = id" as one. This is harmless, since ρ₀ = id is `rotAbout_iterate` at j = 0,
    but the two lists should match.

### m2 (minor): the purpose paragraph's universal claim omits cited published theorems

- **Where.** fd.tex:7–11: "every statement that corresponds to a Lean declaration is stated exactly as in Lean, …
  and it receives a complete proof that can be checked without Lean, except that for a statement labelled
  computer-assisted …".
- **Evidence.**
  - Contract rule 5 lets sections cite published theorems used by the Lean code as black boxes.
  - Section mb does so: `mb:thm:baek` ("Baek's theorem, cited", `\leanref{main}{ErdosSzekeres/Vendor/ETV/Main/
    Main.lean:87}`) and `mb:thm:capcup`. mb.tex:184 says "In this document Theorem~\ref{mb:thm:baek} is cited, not
    reproved".
  - These statements correspond to Lean declarations but receive no proof in this document, so the sentence is
    not true as written.
  - A smaller instance of the same imprecision: fd:lem:inv-image(c) is stated for ℝ², whereas Lean states it for an
    arbitrary type. This is disclosed at :330–331, so it is not stated "exactly as in Lean".
  - This is minor because mb and fd:lem:inv-image are explicit where it matters, and no rigor label is affected.
- **Fix.** Add one clause, for example: "…except that for a statement labelled computer-assisted …, and that a few
  published theorems used by the Lean code (for example Baek's theorem) are cited in the exact form used and not
  reproved; where a statement is given in a different generality from Lean, the text says so."

### m3 (minor): "followed by #print axioms commands" omits one #check line

- **Where.** fd.tex:196–198: "The file SYMLEAN/AffineReductionAxioms.lean is SYMLEAN/AffineReduction.lean followed
  by #print axioms commands".
- **Evidence.** After the 1533 identical lines, the file adds 9 `#print axioms` lines and one
  `#check @ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv`; the check output is
  AffineReductionAxioms.out:18–27. This does not affect the evidence.
- **Fix.** "followed by #print axioms commands (and one #check)", or "followed by printing commands".

### m4 (minor): the bare ":N" shorthand is used but not defined in the conventions

- **Where.** fd.tex:27–31 defines ":N" as a line-number suffix and allows bare file names after a full citation. fd
  itself writes bare `\dirn{:N}` meaning "line N of the file just named" 7 times (:155, 161, 203, 205, 206, 208,
  855), ar once and oc twice.
- **Evidence.** For example, "(\dirn{ErdosSzekeres/Basic.lean:73} and \dirn{:75})" and "(\dirn{:1295})". The
  meaning is clear from context, but the conventions paragraph, which all sections rely on, does not state it.
- **Fix.** Add: "a bare :N after a file citation refers to line N of that file."

## 4. Notes (no action needed)

- The axioms paragraph conservatively lists `Suk.reflectY_x`, `reflectY_y` and `reflectY_reflectY` as not covered
  by a printed line. `reflectY_reflectY` is probably covered by audit line 178: the `simpa` in
  `hasConvexNGon_of_reflectY` (Reflection.lean:67) must simplify `reflectY (reflectY x)`. `reflectY_x` and
  `reflectY_y` may be covered by line 176 through `orient_reflectY`'s `simp only`. Rfl-lemmas need not appear in
  the proof term, so I did not claim coverage. The stated alternative evidence (build record plus text search) is
  accurate.
- fd:lem:rot(b) is tagged with the `def` `rotAff`. The parenthetical says precisely what Lean checks: the
  `map_vadd'` identity ρ(p+v) = ρ(p) + R_θv. The first displayed formula of (b) is the definition unfolded. This
  is acceptable.

## 5. Summary for the fixer

Nothing is required for a pass. Recommended edits, all one or two lines:
- m1: tag (i) of fd:lem:affine-orient with `orient_rotAbout_inv`, and fix the Coverage wording and map notes.
- m2: add the cited-theorem clause to the purpose paragraph.
- m3: one-word fix.
- m4: one-sentence convention.
