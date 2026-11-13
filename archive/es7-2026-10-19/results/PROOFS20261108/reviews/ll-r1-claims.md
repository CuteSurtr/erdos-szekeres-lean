# Review ll, round 1, lens: claims, labels and LaTeX

Section: `sections/ll.tex` (760 lines) and `sections/ll.map.tsv` (31 rows).
Verdict: **pass**. There are no blocker or major findings and six minor ones (m1 to m6 below).

Paths below are relative to the staging directory (`sections/`, `build/`), to the results directory RES
(`LAYERLEAN/...`, `C6UPPER/...`), or to the repository root (`ErdosSzekeres/...`, `lakefile.toml`).

## What was checked, and the result

1. **Compile.** `build/ll_wrapper.tex` was compiled twice with `nice -n 15 pdflatex -interaction=nonstopmode
   -halt-on-error -output-directory=claims-ll-r1`.
   - Both passes exit 0 and the PDF has 9 pages (`build/claims-ll-r1/ll_wrapper.log`, `pass1.stdout`, `pass2.stdout`).
   - There are no `!` errors, no "Missing", no undefined control sequence and no "Label(s) may have changed".
   - Undefined references:
     - ten `fd:` labels: `fd:def:point`, `gp`, `cp`, `ngon`, `inv`, `rot`, and `fd:lem:cp-hull`, `mono`, `collinear`,
       `affine-cp`;
     - `lg:thm:nesting` and `lg:lem:centre`, both export labels of section lg in the contract.
   - Nothing else is undefined.
   - Warnings: 35 overfull hboxes (see m1) and 2 hyperref "Token not allowed in a PDF string" warnings from the `$mt$`
     in the section title (see m6).
2. **Machine paths and tool names.** I grepped `ll.tex` and `ll.map.tsv` for every absolute machine-path prefix the
   contract forbids (the private temporary prefix, the user and home directories, the system temporary directory), for
   sandbox and placeholder paths, for the scratch directory, for the user name and for tool names. There are no hits. I also grepped for leaked meta-text (inventory, contract, writer, TODO, `??`): no hits.
3. **Cited paths.** Every `\dirn{...}` path exists in RES or the repository root:
   - `LAYERLEAN/LayerLemma.lean`, `LAYERLEAN/logs/build.log`, `LAYERLEAN/logs/axioms.log`,
     `LAYERLEAN/logs/axioms_recheck_20261106/out.txt`;
   - `LEANEXT/review/axioms.log`, `WRITEUP/note/k8_soundness.tex`, `C6UPPER`, `C7UPPER`, `ENCBLEAN`;
   - `ErdosSzekeres/Definitions.lean`.

   All are relative, as the contract requires.
4. **SHA-256** (recomputed with `shasum -a 256`).
   - `LAYERLEAN/LayerLemma.lean` = `afb8542dceb0c17005b4eccec1b79abbb57099c0768e1a4bbb1cf52ad797257f`. Both quoted
     prefixes are correct (`afb8542dceb0` at ll.tex:20, `afb8542d` at :33). The file has 1148 lines, as stated.
   - `ErdosSzekeres/Definitions.lean` = `2425500eefd181ad...`. The quoted prefix `2425500eefd1` (:23) is correct, and the
     file does define Point, GeneralPosition, ConvexPosition and HasConvexNGon (lines 9-22).
5. **Axiom-log citations** (I opened each log).
   - `LAYERLEAN/logs/axioms.log` has 28 lines, each `[propext, Classical.choice, Quot.sound]`. This matches "28
     theorems".
   - `axioms_recheck_20261106/out.txt` has 19 lines with the same three axioms, `Exit status: 0` and `exit 0`. The run
     started 2026-11-05T19:59:23Z, which `README.txt` dates 6 Nov 2026, 04:59 KST, so this matches "19 theorems; re-check
     of 6 November 2026, exit status 0".
   - `LayerLemmaAxioms.lean`: by `cmp`, its first 1148 lines are byte-identical to `LayerLemma.lean`, followed by 19
     `#print axioms` lines. This matches the claim.
   - `LEANEXT/review/axioms.log` has 59 axiom lines. Sorted, the names are exactly the 59 theorems of the file not marked
     `@[simp]` (the diff against a grep of `^theorem` is empty; the file has 66 theorems, 7 of them `@[simp]`).
     `iterate_mem` is `[propext, Quot.sound]`; the other 58 have the three axioms. `LEANEXT/review/REPORT.md` dates the
     review 4 Nov 2026 and names `LayerLemma.lean` with SHA-256 `afb8542d…`. This matches the claim at ll.tex:33-37.
   - `LAYERLEAN/logs/build.log` reads: `lake env lean`, from the repository root, exit code 0, 0 message lines. This
     matches.
   - Pins: `lean-toolchain` is v4.24.0 and `lake-manifest.json` pins mathlib `f897ebcf72cd...`. This matches "the
     repository's pins".
   - `lakefile.toml` has `defaultTargets = ["ErdosSzekeres"]`, so the claim that `lake build` does not re-check the
     file is correct.
6. **Source scan of the Lean file.** The only `decide` is at line 1125 (`Even 6`, an argument of
   `centre_not_mem_of_even`). There is no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern`,
   `unsafe`, `opaque` or `set_option`. This matches ll.tex:38-40. Nothing in the scope is a finite computation, so no
   "computer-assisted" label is needed, and none is used.
7. **Lean names and line numbers.** I listed all 55 declarations in lines 1-470 and 1034-1147.
   - Each one is cited in a statement head.
   - Every `file:line` equals the line of the `def` or `theorem` keyword: 48, 52, 59, 62, 68, 80, 91, 105, 111, 114,
     118, 121, 130, 146, 139, 162, 189, 217, 231, 234, 252, 236-287, 298, 302, 311, 319, 465, 325, 336, 364, 374, 378,
     381, 460, 386, 402, 419, 1037, 1066, 1102, 1107, 1113, 1136.
   - Every name exists in the file.
   - The Mathlib names cited (`Complex.isPrimitiveRoot_exp`, `Set.extremePoints`, `convexHull`,
     `Function.minimalPeriod`) are the ones the Lean proofs use.
8. **Labels.**
   - Section labels: there are 32 labels, all starting with `ll:`, and each is defined once.
   - Foreign references: every `\ref` to a label outside the section is one of the ten `fd:` labels in the contract or
     an `lg:` export label. All twelve are defined in `fd.tex` and `lg.tex`, and their environment types match the
     words used before them ("Definition", "Lemma", "Theorem").
   - Export labels: all 15 are defined on the named statements:
     - `ll:def:hv` hullVerts;
     - `ll:def:peel` peel;
     - `ll:lem:hv`: convexPosition_hullVerts, extreme_mem_hullVerts, subset_convexHull_hullVerts, hullVerts_nonempty;
     - `ll:lem:minperiod`, `ll:thm:core`, `ll:thm:core-rot`, `ll:lem:inv-peel`, `ll:thm:layers`,
       `ll:lem:exists-layer`, `ll:lem:antitone`, `ll:thm:card-peel`, `ll:thm:reduction`;
     - `ll:def:66-70` Sixfold66 and Sevenfold70;
     - `ll:thm:sixfold`, `ll:thm:sevenfold`.
9. **Map TSV.**
   - The header is correct.
   - There are 31 rows for 31 statement environments (7 definitions, 21 lemma/theorem/corollary, 3 remarks).
   - Label, kind, Lean names and file:line agree with every head (checked by script).
   - The written step `ll:cor:decomp` and the remarks have `-`.
   - The notes say "takes hypotheses: Sixfold66 / Sevenfold70" and "takes the premise H".
   - The 21 lemma, theorem and corollary environments each have a proof (21 proof environments).
10. **Hypotheses presented as hypotheses.**
    - Sixfold66 and Sevenfold70 appear as assumptions in the statements of Theorems `ll:thm:sixfold` and
      `ll:thm:sevenfold` ("a hypothesis, not proved in Lean") and in the heads ("conditional on ..."). They are defined as
      propositions in Definition `ll:def:66-70`. The introduction and Remark `ll:rem:hyp` say that the octagon
      statements are established only conditionally.
    - Premise (H) of `ll:thm:reduction` is stated inside the theorem, and the text after it says it is an explicit
      hypothesis.
    - Supplying records: Remark `ll:rem:hyp` names C6UPPER and C7UPPER with the rigor label *certificate* (cake_lpr
      verdicts, cube cover checked), plus the written soundness proof in `WRITEUP/note/k8_soundness.tex` (written proof,
      not refereed). This is consistent with `C6UPPER/README.md` (§§3, 6, 7), `C7UPPER/README.md` (§3) and with
      k8_soundness Corollary `k8s:cor:geom` (a) and (b) and its trust table.
    - The ENCBLEAN sentence matches `ENCBLEAN/geo/ES8Geo/Main.lean:87-92` (`sixfold66_of_unsat`,
      `sixfold66_of_cubes64 (h : EncB.CubesUnsat64) : Sixfold66`). I found no unconditional Lean proof of Sixfold66,
      Sevenfold70 or any instance of (H): every use of `convexNGon_of_layers` in the repository passes a hypothesis
      through (`LEANEXT/es7corr/ES7Corollaries.lean:1174,1207`).
11. **Real-cast numerals.** Remark `ll:rem:numerals` matches Lean lines 1126-1130 and 1141-1143: `exact_mod_cast` for
    the angle and `simpa using h4` for `6*11` to `66`.
12. **Overclaiming.** I grepped for verif/certif/fully/formally/unconditional/guarantee/establish/confirm and found
    nothing beyond the rigor labels. The docstring wording "the sixfold case of ES(8)=65" is not repeated.
13. **Fidelity spot-check** (not my lens, done anyway). I compared every statement with its Lean declaration: hypotheses,
    their order, `c ∉ S`, `0 < m`, `K ≤ 2*m`, `m*(t-1) < (S.erase c).card`, maps-into invariance, real numerals and the
    `Finset` vs `Set` coercion in `layers_are_orbits` (c). I found no mismatch.

## Findings

### m1 (minor, LaTeX): long statement heads run past the right margin, and Lean names and line numbers are clipped in the PDF

- **Evidence.** `build/claims-ll-r1/ll_wrapper.log` has 35 overfull hboxes. The text width is 6.7in and the margin
  0.9in ≈ 65pt, so any overflow above 65pt runs off the paper. Overflows beyond the paper edge:

  | ll.tex lines | overflow | statement head |
  |---|---|---|
  | 110-111 | 149.3pt | `ll:lem:orbit` |
  | 175-176 | 74.8pt | `ll:lem:hv` |
  | 336-337 | up to 144.1pt | `ll:lem:complex` |
  | 387-388 | 123.1pt | `ll:lem:rot` |
  | 495-497 | 73.0pt | `ll:lem:inv-peel` |
  | 509-512 | 97.8pt | `ll:thm:layers` |
  | 677-680 | 79.9pt | `ll:thm:sevenfold` |

  More overflows lie inside the margin (for example 62.3pt at `ll:def:66-70` and 51.9pt at `ll:lem:antitone`).
- **Rendered PDF** (`build/claims-ll-r1/pg-*.png`, `full6-6.png`, `full7-7.png`, `crop5-5.png`):
  - the Theorem 1.22 head ends `LAYERLEAN/LayerLemma.lea`, so line 402 is invisible;
  - the Theorem 1.29 head shows `ErdosSzekeres.LayerLemma.sevenfold_octag`;
  - the Lemma 1.21 head ends `...lean:38`, for 386;
  - in the Lemma 1.6 head, line 121 shows as `:12`;
  - the Lemma 1.12 head lines end `ofC_ze`, `ofC_t`, `crot_`, `:28`;
  - Lemmas 1.2 and 1.14 are clipped the same way.

  The source and the map are correct; only the rendering loses the information.
- **Fix.** Put `\sloppy` right after the `\label{...}` of these statements, as `fd.tex` does in its long heads.

  I tested this in `build/claims-ll-r1/sloppytest/` (a copy, with `\sloppy` inserted after every statement label).
  The overfull boxes fall from 35 to 3, all within the margin (50.3pt at `ll:lem:inv-sdiff`, 18.7pt and 15.5pt).

  Another option is to split the multi-declaration heads, for example by moving the per-item Lean references into the
  items.

### m2 (minor, claim about axiom coverage): "the seven @[simp] lemmas ..., which are used inside printed theorems" (ll.tex:35-36)

- **Claim.** The section says the seven `@[simp]` lemmas are used inside printed theorems.
- **Evidence.** That is plausible for `toC_re`, `toC_im` (the `simp` in `rotAbout_eq_crot`), `toC_ofC` (the term proof
  of `toC_crot`), `ofC_toC` (`toC_injective`) and `toC_crot`. For `ofC_zero` and `ofC_one` I find no use.
  - `ofC` occurs only in the definition of `crot` and in the simp lemmas (lines 234-255).
  - After line 360, the only use of `crot` is the rewrite chain in `rotAbout_iterate` (line 467).
  - No proof goal in the file contains `ofC z 0` or `ofC z 1`.

  I cannot confirm this without running Lean (not allowed), but the claim is at best unverified for these two.
- **Impact.** None on correctness: both are `rfl` lemmas checked by the build (exit 0).
- **Suggested wording.** "... except the seven `@[simp]` lemmas of Lemma ll:lem:complex(a)-(b), which are proved by
  `rfl` or by extensionality and are covered by the build log only (most of them are also used inside printed
  theorems)".

  A related nit: in the same sentence, "each depends only on these three axioms" follows a clause about the simp lemmas
  and can be misread as referring to them. Say "each printed theorem".

### m3 (minor, supplying records not fully qualified): Remark `ll:rem:hyp`, ll.tex:699-706

- **Claim.** The remark says Sixfold66 is "supplied by the record C6UPPER ... together with the written soundness proof
  of the encodings in `WRITEUP/note/k8_soundness.tex` (a written proof, not refereed)". The labels are correct and
  nothing is presented as proved.
- **Missing qualification 1: gaps.** k8_soundness itself lists open gaps (G1)-(G4) (`k8_soundness.tex`, "Gaps that
  remain", lines 959-1030):
  - (G1): the code-to-clause correspondence is established by reading the Python source;
  - (G3): encoder A uses binary64 arithmetic;
  - (G4): several steps, among them Corollary `k8s:cor:geom` (the passage to Sixfold66/Sevenfold70) and the assembly in
    `k8s:lem:layer`, "have had no internal review".

  `C6UPPER/README.md` §§6-7 also cites "gaps (G1)–(G4)". Add a clause such as "(not refereed; its section on the trust
  base lists the remaining gaps (G1)–(G4))".
- **Missing qualification 2: ENCBLEAN.** The ENCBLEAN sentence ("a Lean derivation of Sixfold66 that takes the
  unsatisfiability of the cube formulas as a hypothesis") is accurate for `EncB.Geo.sixfold66_of_cubes64`. But the
  cube formulas are those of ENCBLEAN's Lean definition `EncB.encB` of encoder B's formula, and ENCBLEAN states Sixfold66
  in a verbatim copy of `LayerLemma.lean` (`ENCBLEAN/geo/ES8Geo/Capstone2.lean`). Tying those formulas to the certified
  files and the cake_lpr verdicts rests on the trust items (E1)-(E6) of k8_soundness gap (G2). Saying so in half a
  sentence would avoid suggesting that this route needs only the SAT verdicts.

### m4 (minor, imprecise description of the Lean proofs): Coverage (ll.tex:733-734) and map note of `ll:lem:hv`

- **Claim.** Both say the Lean proofs of (b)-(d) "use Krein–Milman".
- **Evidence.**
  - The Lean proof of (b) (`extreme_mem_hullVerts`, lines 130-137) uses `Convex.mem_extremePoints_iff_convex_diff`
    and `extremePoints_convexHull_subset`, not Krein–Milman.
  - (d) uses `IsCompact.extremePoints_nonempty` and (c) uses `closure_convexHull_extremePoints`.

  The proof text at ll.tex:185-188 describes this correctly; only the Coverage paragraph and the TSV note
  over-generalise.
- **Suggested wording.** "the Lean proofs of (c) and (d) use Krein–Milman".

### m5 (minor, precision of the blanket rigor sentence): ll.tex:40-43

- **Claim 1.** "Every statement below whose head names a Lean declaration is *Lean-checked* in this sense".
- **Problem.** This also covers the definitions, among them Definition `ll:def:66-70`, whose head names Sixfold66 and
  Sevenfold70. A hurried reader could take "Lean-checked" to apply to these propositions. The definition text corrects
  this at once ("neither is proved in Lean"), so this is wording only.
- **Suggested wording.** Restrict the sentence to "every lemma and theorem whose head names a Lean declaration", or add
  "(definitions are Lean definitions, not claims; in particular Sixfold66 and Sevenfold70 are not proved)".
- **Claim 2.** "for each we say whether it follows the Lean proof".
- **Problem.** The proofs of Lemmas `ll:lem:hv-basic` and `ll:lem:peel-basic` do not say so (both are trivial).

### m6 (minor, cosmetic): hyperref warning from the title

- **Evidence.** `\section{... exactly $mt$ points}` produces two "Token not allowed in a PDF string" warnings, and the
  bookmark drops the math.
- **Fix (optional).** `\texorpdfstring{$mt$}{mt}` is a hyperref command, not a new macro, so it is allowed.

## Not findings (checked and correct)

- No `\ref` points to a label outside the allowed set. Every export label is defined.
- No machine path or tool name appears in either file.
- The SHA-256 prefixes, line counts, axiom-log counts, dates and exit statuses all match the records.
- The intro, the statements and the remarks never present Theorems `ll:thm:sixfold`/`ll:thm:sevenfold` or
  `ll:thm:reduction` as unconditional.
- The written step `ll:cor:decomp` is labelled as such in the head, in the text before it, in Coverage and in the map.
