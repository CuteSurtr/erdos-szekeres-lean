# Review of section `ar` (Affine symmetries), round 1, lens: claims, labels and LaTeX

**Verdict: pass.** I found no blocker and no major finding. There are nine minor findings, F1 to F9.

Files reviewed: `sections/ar.tex` (752 lines) and `sections/ar.map.tsv` (30 rows plus a header). Paths below are
relative to STAGE (`sections/`, `build/`), to RES (`SYMLEAN/...`, `C2FINAL/...`, `WRITEUP/...`) or to the repository
root (`ErdosSzekeres/...`, `lean-toolchain`, `lake-manifest.json`).

## Checks performed, with evidence

1. **Compilation.** I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=claims-ar-r1
   ar_wrapper.tex` twice from `build/`.
   - Both passes exit 0. The log has no `!` error, no "Missing $", no overfull box and no multiply-defined label. It
     has 68 underfull boxes, which come from the section's `\sloppy` (see F8).
   - After pass 2 every undefined reference is an allowed one:
     - `fd:def:{point,orient,gp,cp,ngon,inv}` and `fd:lem:{collinear,cp-hull,affine-orient,affine-cp}` (foundations
       labels);
     - `sr:def:iso`, `sr:def:classes`, `sr:thm:main`, `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes` and
       `mb:thm:main3`, all of them export labels in the contract table.
   - Each of these 17 labels is defined in the current `sections/fd.tex`, `sr.tex` or `mb.tex`, so the full document
     will resolve them.
   - The output is in `build/claims-ar-r1/`.

2. **Labels.**
   - The section defines 31 labels, each once, all with the prefix `ar:`.
   - Every `\ref` to an own label resolves.
   - The export label `ar:thm:transfer` sits on `hasConvexNGon_of_affine_symmetry`.
   - The export label `ar:thm:main` sits on `heptagon_of_nontrivial_affineEquiv` together with the variants
     `_affineEquiv_image`, `_affineMap`, `_affine` and `_affine_coords`, as the contract requires.
   - No `\ref` goes to a non-export label of another section.

3. **Map.**
   - The section has 30 statement environments and the map has 30 rows.
   - A script compared label, kind, `lean_name` and `file_line` of every row with its `\begin{...}[...\leanref...]` head.
     All 30 match.
   - The file is ASCII, every line has 5 tab-separated fields, there are no CR characters and the file ends with a
     newline.
   - The notes state hE and the five classes as hypotheses.

4. **Lean names and line numbers.**
   - All 45 (name, file:line) pairs in the statement heads are exact declaration lines of
     `SYMLEAN/AffineReduction.lean`.
   - The 45 declarations of lines 1059–1533 are exactly the names in the Coverage paragraph: none is missing and none
     is extra.
   - The citations into the duplicated prefix are exact, in both `AffineReduction.lean` and
     `SymmetricReduction.lean`: `iterate_mem` :69, `eDist2` :265, `IsEucIsometry` :268, `Invariant` :271,
     `point_ext` :502 and `heptagon_of_nontrivial_isometry` :997.
   - The repository citations are exact: `ErdosSzekeres/Orientation.lean:9` (`orient`), `ErdosSzekeres/Basic.lean:15`
     (`convexPosition_iff`) and `ErdosSzekeres/OrientationGeometry.lean:66` (`generalPosition_iff_orient_ne_zero`).
   - The mirror citations are exact: `SYMLEAN/mirror/ReductionThreeClasses.lean` :4274 (`mirrorOneAxis33_proved`),
     :4282 (`mirrorNoAxis34_proved`) and :4303 (`heptagon_of_nontrivial_affineEquiv_3`, whose binders are only
     `HalfTurn34`, `Threefold33` and `Fivefold35`).
   - Lines 38–1559 of that mirror file equal lines 12–1533 of `AffineReduction.lean` (checked with `diff`), so the
     "+26" offset is right.
   - The cited Mathlib names exist at `f897ebcf`. I grepped the source tree of that revision:
     - `Matrix.det_fin_two`, `Matrix.det_fin_two_of`, `LinearMap.toMatrix'`, `LinearMap.toMatrix'_mulVec` and
       `LinearMap.det_toMatrix'`;
     - `LinearEquiv.isUnit_det'`, `AffineMap.image_convexHull` and `AffineMap.decomp`;
     - `AffineEquiv.ext`, `AffineEquiv.refl`, `AffineEquiv.toAffineMap` and `LinearMap.toAffineMap`.
   - The proof-step and binder names `hLm`, `hTiT`, `hTTi`, `hnT`, `hiso`, `hinv'`, `hne'`, `Ti`, `hg`, `hE`, `h2`,
     `h3`, `h5`, `hm1` and `hm0` all occur in the Lean proofs.

5. **SHA-256 prefixes.** I recomputed all eight with `shasum -a 256`, and all match:

   | file | cited prefix | computed |
   |---|---|---|
   | `SYMLEAN/AffineReduction.lean` | `41cfc0b60aec` | `41cfc0b60aec15c7…` |
   | `SYMLEAN/SymmetricReduction.lean` | `6d5ec90a4215` | `6d5ec90a421586e6…` |
   | `SYMLEAN/AffineReductionAxioms.lean` | `f6cb9372b174` | `f6cb9372b1745ada…` |
   | `SYMLEAN/logs/AffineReductionAxioms.out` | `38d0b6f59398` | `38d0b6f59398ad75…` |
   | `ErdosSzekeres/Definitions.lean` | `2425500eefd1` | `2425500eefd181ad…` |
   | `ErdosSzekeres/Orientation.lean` | `f67955ac7091` | `f67955ac70916031…` |
   | `ErdosSzekeres/Basic.lean` | `13667aa2d3dc` | `13667aa2d3dc83ef…` |
   | `ErdosSzekeres/OrientationGeometry.lean` | `c7db9bbbb65e` | `c7db9bbbb65eb4cd…` |

   A read-only `git diff --stat 9cf4949a5 7e32ee259` shows the four `ErdosSzekeres/` files unchanged since 9cf4949a5,
   the commit at which README §8 says the Lean runs used them. So the hashes are those of the files that were compiled.

6. **Axioms and compilation evidence.**
   - `SYMLEAN/logs/AffineReductionAxioms.out` lists exactly the nine theorems the section names. Each depends on
     `[propext, Classical.choice, Quot.sound]`.
   - Its `#check` block (lines 18–27) shows the five classes as premises of `heptagon_of_nontrivial_affineEquiv`.
   - `SYMLEAN/logs/AffineReduction.out` is 0 bytes.
   - `SYMLEAN/logs/runs.tsv` records exit 0 for both files on 2026-11-01. `AffineReductionAxioms.lean` consists of
     lines 1–1533 of `AffineReduction.lean` (checked with `diff`), a blank line, nine `#print axioms` lines and one
     `#check` line.
   - The bullet "every other declaration … is used … in the proof of one of these nine theorems" is true. A textual
     dependency closure from the eight in-scope printed theorems reaches all 45 declarations.
   - The whole file contains no `decide`, `native_decide`, `sorry`, `admit` or `axiom`.
   - The toolchain is `leanprover/lean4:v4.24.0`, and Mathlib rev `f897ebcf72cd…` (`lake-manifest.json`).
   - `SYMLEAN/mirror/axioms.out` gives only the three standard axioms for `mirrorOneAxis33_proved`,
     `mirrorNoAxis34_proved` and `heptagon_of_nontrivial_affineEquiv_3`.

7. **Hypotheses and status claims.**
   - The five classes appear as hypotheses in the head ("conditional on the five case classes"), in the statement and in
     the Coverage paragraph.
   - Remark `ar:rem:classes` names the supplying records and rigor labels. This agrees with `SYMLEAN/README.md` §5 and
     §9, `SYMLEAN/mirror/README.md`, `SYMZ/README.md` (Theorems 2a and 2b), `C2FINAL/README.md`, `C3FINAL/README.md`,
     `C3SPOT/README.md` and `SYM5/README.md`.
   - "The unconditional form … is computer-assisted, and it is not Lean-checked as a whole" repeats README §9.
   - The hypothesis hE is stated precisely: same binder order as Lean, `AffineReduction.lean:1331–1332`. It is called
     a parameter for the same N and n, as the task notes require.
   - Remark `ar:rem:hE`(2) about P1 is accurate: `WRITEUP/P1/p1.tex:173–183` says that an order-preserving version
     is needed and not formalized.
   - I found no other Lean development of an affine conjugation in the checkout. The affine declarations exist only in
     the three copies named in Coverage; `AffineEquiv` occurs elsewhere only as coordinate frames in
     `ErdosSzekeres/Suk/Base*.lean`.
   - The prefix declarations that Sources says "are treated in the section of Theorem sr:thm:main" are treated there.
     `Invariant`, `iterate_mem`, `point_ext`, `eDist2`, `IsEucIsometry` and `heptagon_of_nontrivial_isometry` all
     appear in `sections/sr.map.tsv` or `sr.tex`.
   - The docstring phrase "Corollary 3" is not repeated.

8. **Machine paths and tool names.** I grepped `ar.tex` and `ar.map.tsv` for absolute machine-path prefixes (the
   system temporary directory, the user home directories and the session's scratch directory) and for tool names. There are no hits.
   - All file references are relative to RES or to the repository root, as the contract requires.

9. **Displayed identities** (a quick symbolic check, beyond the lens). All of these hold:
   - the four identities in the proof of `ar:lem:fix` and the two in `ar:lem:inj`;
   - the orientation factor in `ar:lem:lin2`(b);
   - `ar:lem:chol` (a)–(c);
   - the evaluation at (−β, α) in `ar:lem:avgq-pos`(c);
   - β²/α + (αγ−β²)/α = γ.

## Findings

All findings are minor. None affects correctness.

**F1 (minor), `ar.tex:665–666`, last paragraph of the proof of Theorem `ar:thm:main`.**
- The text says: "The Lean proofs are the same one-line applications. They pass `heptagon_of_nontrivial_isometry`,
  applied to the five hypotheses …, as `hE`."
- This is not true of `heptagon_of_nontrivial_affineEquiv_image`. Its Lean proof (`SYMLEAN/AffineReduction.lean:1516–1517`)
  applies `heptagon_of_nontrivial_affineEquiv h2 h3 h5 hm1 hm0` and turns `g '' S ⊆ S` into `Invariant`. The
  isometry theorem reaches it only through (a).
- The written proof of (b), "Now apply (a)", is correct.
- Fix: write "In Lean, (a), (c), (d) and (e) pass … as `hE`; (b) applies (a)."

**F2 (minor), `ar.tex:8–9`, introduction.**
- The text says: "The Euclidean statement is a hypothesis of the transfer (a parameter), not a claim of the project."
- This can be misread. For N = 33 and n = 7 the Euclidean statement is the project's Theorem `sr:thm:main`
  (Lean-checked, conditional on the classes), and Theorem `ar:thm:main` uses it.
- The intended meaning is stated precisely in Remark `ar:rem:hE`(1): "It involves no unproved claim of the project."
- Fix: write "(a parameter of the theorem, not an unproved assumption)".

**F3 (minor), `ar.tex:456`, Definition `ar:def:E`.**
- The text says: "This is, word for word, the type of the hypothesis `hE`."
- The Lean binder (`AffineReduction.lean:1331–1332`) uses the named predicates `IsEucIsometry g` and `Invariant g S`,
  the variables `S` and `g`, and curried premises. The definition renames the variables to S′ and h and unfolds both
  predicates.
- The content is faithful (checked), but "word for word" overstates it.
- Fix: write "This is the type of the hypothesis `hE`, with `IsEucIsometry` and `Invariant` unfolded and the bound
  variables renamed."

**F4 (minor), `ar.tex:39–43` and `52–53`, Rigor and axioms.**
- The run date ("run of 1 November 2026") and the exit codes ("exit code 0") are not in the cited `.out` files. They
  come from `SYMLEAN/logs/runs.tsv`:
  - `AffineReduction.lean`: 2026-11-01T14:54:56Z, exit 0;
  - `AffineReductionAxioms.lean`: 2026-11-01T14:55:01Z, exit 0.
  README §8 records the same.
- The facts are correct, but the source of the exit codes is not named.
- Fix: cite `SYMLEAN/logs/runs.tsv` for the date and the exit codes.
- Trivial, no action needed: `AffineReductionAxioms.lean` has a blank separator line (line 1534) before the ten
  appended lines, which is why it has 1544 lines and not 1543.

**F5 (minor; I am unsure whether it is an error), `ar.tex:690–691`, Remark `ar:rem:classes`.**
- The text says: "written soundness proofs of the encoders (not refereed)".
- The records use other words:
  - `SYMLEAN/README.md` §5 says "written proofs (reviewed, …)";
  - `C2FINAL/README.md:16,24,37` says the `C2ENC` encoder proof was "refereed on 1 November" (an internal referee pass);
  - P1 (`WRITEUP/P1/p1.tex:70,137`) uses "written soundness proof …, not refereed".
- So the section follows P1's convention. It is an understatement, not an overclaim. I am unsure whether the contract
  intends external records to be relabelled this way.
- Suggestion: write "(reviewed within the project, not refereed; `SYMLEAN/README.md` §5)" so that the label matches
  the records.

**F6 (minor, optional), `ar.tex:689–690`, Remark `ar:rem:classes`.**
- The supplying records are named only as `C2FINAL`, `C3FINAL` and `SYM5`.
- `SYMLEAN/README.md` §5 gives the certificate chains:
  - `HalfTurn34`: `C2C34` (encoder, hull cover, hexagonal hulls), `C2P`–`C2P5` (parallelogram subcases) and `C2FINAL`
    (composition);
  - `Threefold33`: `C3FINAL`, with the normal form `C3-S` and the encoding `C3a`.
- `SYMLEAN/mirror/README.md` §4 says "C2FINAL with C2C34, C3FINAL with C3LEAN, SYM5".
- The remark already points to README §5 and §9, so this is acceptable. Naming the chain records would make the remark
  self-contained.

**F7 (minor), `ar.map.tsv`, rows with several names** (`ar:lem:mulvec`, `ar:lem:nsq`, `ar:def:gram`, `ar:def:avgq`,
`ar:lem:avgq-pos`, `ar:lem:lin2`, `ar:lem:chol`, `ar:lem:gp-affine`, `ar:cor:transfer-forms` and `ar:thm:main`).
- These rows separate the Lean names and the file:line entries with ", ".
- The maps of fd, ll, mb, mm, oc, pc and sr use "; "; only ec also uses ", ".
- The contract does not fix the separator. This is a consistency point that matters if the appendix map is generated by
  splitting on ";". Coordinate with whoever builds `appendix_map`.

**F8 (minor, cosmetic), `ar.tex:2`.**
- `\begingroup\sloppy\emergencystretch=\linewidth` gives 68 underfull-box warnings and visibly stretched lines. Two
  examples:
  - the Sources paragraph after "`ErdosSzekeres/Orientation.lean:9` (SHA-256 f67955ac7091…)";
  - the heads with several `\leanref`s (Lemma `ar:lem:avgq-pos`, Corollary `ar:cor:transfer-forms`, Theorem
    `ar:thm:main`).
- This is not an error: there are no overfull boxes, and the contract does not forbid the group.
- Optional: break the long heads or move the Lean references into the first line of the statement body.

**F9 (minor, clarity), `ar.tex:642–644`, Theorem `ar:thm:main`(e).**
- Here "f" is a real number, while item (c) of the same theorem uses f for an affine map.
- Corollary `ar:cor:transfer-forms`(c) adds "(here f is a real number)", but the theorem does not.
- Fix: add the same parenthesis.

## Not findings (checked and fine)

- "No proof uses `decide` or `native_decide`. Nothing in this section is a computation." This is true: the proofs use
  `ring`, `field_simp`, `linarith`, `nlinarith`, `linear_combination`, `positivity`, `omega`, `norm_num`, `simp` and
  `fin_cases`, and none of them is a data computation.
- The description of the mirror classes is correct:
  - they are Lean-checked theorems with no SAT input, obtained from the repository's formalization of Baek's theorem;
  - their axioms log is clean;
  - they also have SAT certificates in `SYMZ`.
- "For most of them only recorded verdicts remain" matches `C2FINAL` §§4–5 and §9 (sampled re-solves) and
  `C3SPOT`/`C3PIECES` (2,120 random pieces and the 204 indispensable σ-cube pieces were re-solved).
- The perturbation caveat for `Threefold33` and `Fivefold35` matches `SYMLEAN/README.md` §6.5, item 3.
- Remark `ar:rem:scope`(3) is right that the variant has no affine version (README §9), and no such Lean file exists.
