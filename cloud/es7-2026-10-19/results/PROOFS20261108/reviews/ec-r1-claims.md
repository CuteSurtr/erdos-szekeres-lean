# Review ec, round 1, lens: claims, labels and LaTeX

Section: `sections/ec.tex` (850 lines), map `sections/ec.map.tsv` (41 rows).
Paths below are relative to `STAGE` (staging area) or to `RES = cloud/es7-2026-10-19/results`.

**Verdict: pass.** No blocker or major finding. Eight minor findings (wording, layout, scope nits).

## What was checked, with results

### Compile check
- `build/ec_wrapper.tex` compiled from `STAGE/build` with
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=claims-ec-r1 ec_wrapper.tex` twice.
  Both passes exit 0. Logs are in `build/claims-ec-r1/` (`pass1.txt`, `pass2.txt`, `ec_wrapper.log`).
- No `!` errors, no undefined control sequences, no "Missing", no multiply-defined labels, no hyperref
  PDF-string warnings. The bookmarks are fine.
- There are 34 undefined-reference warnings, all to export labels of other sections:
  - `fd:def:{point,orient,gp,cp,ngon,inv,rot}`;
  - `ll:thm:reduction`, `ll:lem:minperiod`, `ll:thm:layers`, `ll:thm:card-peel`;
  - `lg:lem:centre`, `lg:lem:polar`;
  - `sr:def:classes`.
- Each of these labels is in the contract's export lists and is defined in its own section file (`fd.tex`, `ll.tex`,
  `lg.tex`, `sr.tex`). The environment types match the words used (Theorem, Lemma, Definition).
- The task note says the section "may \ref ll:, lg:, fd: export labels". The section also refs `sr:def:classes`
  (Remark ec:rem:cases, line 108, and the Rigor paragraph, line 66). The contract allows any export label of another
  section, so this is compliant.
- Overfull boxes: see finding m6.

### Labels and references
- 47 labels are defined. All start with `ec:` and none is duplicated. Every `\ref{ec:...}` resolves.
- All seven export labels of `ec` are defined on the named statements:

  | label | number | declaration |
  |---|---|---|
  | `ec:thm:fivefold` | Thm 1.4 | `fivefold_heptagon` |
  | `ec:thm:fourfold` | Thm 1.7 | `fourfold_heptagon` |
  | `ec:thm:big-order` | Thm 1.16 | `RefuteC6.part_a` |
  | `ec:lem:polar-u` | Lemma 1.23 | `C7.orient_polar` |
  | `ec:thm:nested` | Thm 1.28 | `C7.nested_regular_orient` |
  | `ec:thm:compat` | Thm 1.35 | `dvd_card`, `card_mod`, `exists_iff`, `classification` |
  | `ec:thm:l0` | Thm 1.40 | `L0`, `L0_rot` |

  The variants of the fivefold and fourfold theorems have their own labels (`ec:thm:fivefold-erase`,
  `ec:thm:fivefold-nc`, `ec:thm:fourfold-erase`).
- The range `Theorems~\ref{ec:thm:fivefold-erase}--\ref{ec:thm:fourfold}` (Axioms paragraph) is 1.3–1.7. These are
  exactly the five consecutive corollaries.

### Map TSV
- The header is correct. There are 41 data rows for the 41 statement environments, in order.
- A script compared label, kind, Lean names and `file:line` against each environment's `\leanref` head
  (`build/claims-ec-r1/tools/mapcheck.py`). It found no mismatch.
- Every row has 5 tab-separated fields. There are no CR characters and no duplicate labels.
- The notes do not overclaim:
  - "takes hypotheses: Fivefold35/Fourfold32";
  - "takes hypotheses hr0, hdisj on r (not discharged for C in Lean)";
  - "computer-assisted (kernel decide; axioms propext only)".

### Machine paths, tool names, overclaiming words
- A grep of `ec.tex` and `ec.map.tsv` for the machine-path prefixes of contract rule 3 (and the temporary-directory
  prefix) and for tool names finds nothing.
- "verified", "certified" and "proved" do not occur in the tex. The map has only "never proved in Lean".
- The docstring wording "certified in results/C4CUT" and "The fivefold case of ES(7)" is not repeated.

### SHA-256 prefixes (recomputed with `shasum -a 256` in RES)
| file | computed | in section |
|---|---|---|
| LEANEXT/es7corr/ES7Corollaries.lean | 5883c8ebac55… | 5883c8ebac55 ✓ |
| ES8SYM/lean/C6check.lean | 92f15b5cc907… | 92f15b5cc907 ✓ |
| ES8SYM/lean/PolarOrient.lean | 6e54f5f83a19… | 6e54f5f83a19 ✓ |
| PRIMEFOLD/compat/lean/PCompatCore.lean | ebc6aacefadb… | ebc6aacefadb ✓ |
| PRIMEFOLD/compat/lean/L0Check.lean | 05a67c3b8b16… | 05a67c3b8b16 ✓ |

Other hash and record claims:
- The recorded prefixes are quoted correctly:
  - `LEANEXT/es7corr/REPORT.md` has `5883c8eb…`;
  - `PRIMEFOLD/README.md:35,38` has `ebc6aace…` and `05a67c3b…`;
  - `ES8SYM/README.md:258-260` has `8c090168…` and `4d42e2fb…` for the compiled files, with the "four comment lines"
    statement. The section discloses that this could not be checked.
- Line counts match the table: 123, 132, 291 and 152.
- Pins:
  - The repository's `lean-toolchain` is v4.24.0 and `lake-manifest.json` has Mathlib `f897ebcf…`.
  - A read-only `git log` shows no change to either file since the first commit (2026-10-04).
  - `PRIMEFOLD/README.md:33` names Lean 4.24.0 and Mathlib `f897ebcf`.
  - `ES8SYM/README.md:258` says "the repository's Lean 4.24.0 and Mathlib".
  - So "according to the records … the repository's pins" is accurate.

### Axioms logs (opened)
- `LEANEXT/es7corr/axioms.log`: the five corollaries, each with [propext, Classical.choice, Quot.sound] ✓.
- `ES8SYM/lean/C6check.out`: `part_a` and `thr_m4`…`thr_m7`, with the three standard axioms ✓. There is no line for
  `m4_with_centre_counter` (C6check.lean:119-123 prints only these five), as the section says ✓. The log shows no
  error ✓.
- `ES8SYM/lean/PolarOrient.out`: the six C7 theorems the section names ✓.
- `PRIMEFOLD/compat/lean/PCompatCore.out`: `dvd_card`, `card_mod`, `exists_iff`, `compat_even`, `compat_odd` and
  `classification` with the standard three; `ex341` with [propext] only ✓.
- `PRIMEFOLD/compat/lean/L0Check.out`: `L0Check.L0_rot` ✓.
- "Every other declaration covered here occurs in the statement or the proof of one of these": checked for each one.
  - C6check: `zeta`, `zeta_prim`, `orbit_*`, `sphere_subset_extremePoints` and `convexIndependent_of_norm_eq` all
    feed `part_a`.
  - PolarOrient: `det_mul_eq` feeds `orient_polar`; `ngonPt_eq_pt` feeds `nested_regular_orient`; the definitions
    occur in statements.
  - PCompatCore: `ne_zero_of_order`, `pow_inj_of_order` and `pow_mul_mem` feed `dvd_card`; `exists_card0/1` feed
    `exists_iff`.
  - L0Check: `arith` and `orbit_dvd` feed `L0`, which feeds `L0_rot`.
  - ES7Corollaries: `Fivefold35` and `Fourfold32` occur in the statements.
- A grep of the five files finds no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by` or `extern` ✓.
  `decide` occurs only in `ex341` (lines 279-281), `classification` (line 266, the m = 1 branch) and `Even 4/6`
  (ES7Corollaries:1125, 1227).

### Computations and how Lean checks them
- `PCompat.ex341` is labelled "computer-assisted" in its head and in the map ✓. The proof describes the Lean check
  correctly:
  - five `by decide` (Compat via `Or.inr`, `341 = 11*31`, and the three remainders), under
    `set_option exponentiation.threshold 400` (line 275);
  - non-primality via `Nat.not_prime_mul (by decide) (by decide)`. At Mathlib f897ebcf the signature is
    `(a1 : a ≠ 1) (b1 : b ≠ 1)`, matching "11 ≠ 1 and 31 ≠ 1" ✓;
  - no `native_decide`, log [propext] ✓.
- The hand computation is correct: 1024 = 93·11+1 = 33·31+1 = 3·341+1, and 2^340 = (2^10)^34.
- `thr_m4`…`thr_m7` and `m4_with_centre_counter` use `omega`. The section says so ("decision procedure … proof term
  checked by the kernel") and gives a hand proof. It is not labelled computer-assisted, which is appropriate: these
  are not enumerations.

### Hypotheses presented as hypotheses
- Each of the five ES(7) theorems begins "Assume Fivefold35/Fourfold32" ✓. The sentence before them repeats that the
  case statement is a hypothesis ✓. Overview item (1) says "they are hypotheses of the Lean theorems" ✓.
- Remark ec:rem:cases:
  - It says no Lean theorem proves the case statements.
  - It names `SYM5` and `C4CUT` with their rigor (computer-assisted; LRAT accepted by cake_lpr; exact rational
    Grassmann–Plücker certificates; a written encoder-soundness argument).
  - It says no formula-to-proposition step is in Lean.
  - It notes that the SYMLEAN constants (SymmetricReduction.lean:477, :496, verified) are different Lean constants.
  - It corrects the misleading copied docstring of `Fourfold32` (an inventory risk).
- The records confirm all of this:
  - `SYM5/chk_P1_cake_lpr_heap30000.out` and `chk_L1_cake_lpr.out` contain `s VERIFIED UNSAT`;
  - `C4CUT/final.json` has `"cake_lpr": "s VERIFIED UNSAT"`;
  - `C4CUT/README.md` §2 describes the six cuts with exact certificates.
- `exists_iff`, `exists_card0` and `exists_card1` take (R0) and (RD) as hypotheses ✓. Remark ec:rem:compat(ii) says
  they are not discharged in Lean for ℂ ✓.

### Other record claims (all verified)
- Line numbers:
  - Every `\leanref` file:line is exact.
  - ES7Corollaries: 1157, 1164, 1170, 1183, 1193, 1203, 1216; section header at 1148; `end` at 1233.
  - C6check: 24, 43, 60, 62, 66, 75, 85, 108–111, 115; prints at 119–123.
  - PolarOrient: 24, 37, 45, 48, 50, 63, 68, 80, 94, 97, 100, 108, 116; prints at 127–132.
  - PCompatCore: 36, 43, 58, 67, 112, 129, 160, 174, 205, 208, 235, 253, 277; prints at 285–291.
  - L0Check: 21, 60, 122, 144; print at 152.
- Lines 1–1147 of ES7Corollaries.lean are identical to lines 1–1147 of LAYERLEAN/LayerLemma.lean (`diff`, exit 0).
  LayerLemma.lean has 1148 lines, the last being `end ErdosSzekeres.LayerLemma`.
- LayerLemma.lean declaration lines: 105 `Invariant`, 298 `rotAbout`, 582 `centre_not_mem_of_even`, 935
  `orient_polar` (radius form, formula as quoted), 1066 `convexNGon_of_layers`.
- (R) and (C) match the Lean statements and `ll.tex`/`lg.tex`.
- `ES8SYM/proofs/layers.md`:
  - Lemma 1 is at lines 15–29.
  - Lemma 2: (a) and the arithmetic of (b) are the Lean part; the layer step is not formalized (lines 42–43).
  - The general-position remark is at lines 41–42.
- `WRITEUP/P1/p1.tex:380` and `WRITEUP/note/k8_soundness.tex:449,480` use the radius-form `orient_polar` ✓.
- `symmetric_es7.tex` prop:C (line 326) gives N(C4) = 28 and N(C5) = 31, derived via lem:sizes ✓.
- `symmetric_extremal.tex` prop:compat (line 355) claims general-position existence; the section says this is not
  formalized ✓.
- `PRIMEFOLD/cluster/PROOFS.md` Lemma 0 (line 58) excludes the centre by general position ✓.
- The mutant logs fail at ES7Corollaries lines 1189 and 1231, which are the final `omega` of `fivefold_heptagon` and
  `fourfold_heptagon` ✓.
- `SYMMAX/c5_31points.txt` and `c4_28points.txt` exist.
- The ES8SLACK paths in Coverage exist, and `ES8SLACK/README.md:402-404` says the two named files were not compiled ✓.
- The Mathlib names cited exist at f897ebcf:
  - `Complex.isPrimitiveRoot_exp`;
  - `IsPrimitiveRoot.{ne_zero, norm'_eq_one, pow_inj, pow_ne_one_of_pos_of_lt}`;
  - `Nat.dvd_prime_pow`, `Nat.not_prime_mul`;
  - `Nat.FermatPsp`/`ProbablePrime` (definition as displayed);
  - `Set.extremePoints` and `ConvexIndependent` (definitions as paraphrased);
  - `norm_combo_lt_of_ne`, `convexIndependent_iff_notMem_convexHull_diff`, `Matrix.det_fin_three`.
- Scope and Coverage:
  - Every declaration of the five files in scope is covered by label.
  - The LayerLemma copy (lines 1–1147) and the `#print axioms` lines are excluded with reasons.
  - ES8SLACK is mentioned as out of scope with a pointer to `ES8SLACK/proofs.md`, as the task requires.
  - Every written step is listed (Fact ec:fact:prim, Corollary ec:cor:planar, the example in Remark ec:rem:compat(ii)).

## Findings (all minor)

**m1 (minor). The overview states the threshold arithmetic without the condition on e, and it is false for m = 4 with
e = 1.**
- Location: `ec.tex:12-13`, overview item (2).
- The overview says "the threshold arithmetic 65 ≤ mt+e ⟺ t ≥ 17,13,11,10 for m = 4,5,6,7". The letter e is not
  defined there. If it ranges over {0, 1} as in items (ii) and (iv) of Proposition ec:prop:thr, the equivalence fails
  for m = 4: 65 ≤ 4·16+1 but 16 < 17. That is exactly `RefuteC6.m4_with_centre_counter`.
- Lean's `thr_m4` and `thr_m6` have no e. The precise Proposition ec:prop:thr is correct.
- Suggested fix: "65 ≤ 4t, 5t+e, 6t, 7t+e (with e ≤ 1) ⟺ t ≥ 17, 13, 11, 10".

**m2 (minor). Remark ec:rem:cases lists the outside-Lean dependencies of SYM5 and C4CUT incompletely.**
- Location: `ec.tex:105`.
- The remark says "Both results also rest on the written soundness argument for the encoder". The SYM5 result also
  rests on the centre-perturbation lemma, which makes the auxiliary centre generic: a written proof in
  `C2ENC/perturbation.md`, cited in `SYM5/README.md` §1 and as `lem:perturb` in `symmetric_es7.tex:107,315`.
- The layer normal forms (SYM5 L1 and C4CUT) also use the layer lemma, which is Lean-checked in LAYERLEAN.
- C4CUT's sector-unit step was noted as "not written down" (`C4CUT/README.md` §1, AUDIT3 A4-1), although the README
  gives the one-line argument.
- This is not an overclaim, only an incomplete list.
- Suggested fix: "rest on written arguments outside Lean (encoder soundness; for SYM5 also the centre-perturbation
  lemma, `C2ENC/perturbation.md`)".

**m3 (minor). "It is the Lean check of part (a)" is loose without the qualifier that Lean checks the ℂ form.**
- Location: `ec.tex:220-222`.
- `part_a` is a complex-plane statement: an arbitrary `Set ℂ`, centre 0, convex-independent families. Lemma 2(a) of
  `layers.md` is planar, and the link is the written step Corollary ec:cor:planar.
- Remark ec:rem:big-order says this, so the claim is clarified a page later.
- Suggested fix: "the Lean check of a complex-number form of part (a) (the planar form is Corollary ec:cor:planar, a
  written step)".

**m4 (minor). Remark ec:rem:thr says e = 0 for even m without the side condition S ≠ {c}.**
- Location: `ec.tex:396-398`.
- The remark says "c ∉ S for even m (Lemma lg:lem:centre); so … e = 0 for m = 4, 6". Lemma lg:lem:centre needs a point
  p ∈ S with p ≠ c.
- S = {c} satisfies all the stated assumptions, and there e = 1 with m even.
- This is harmless, since the remark then assumes |S| ≥ 65. The imprecision is inherited from `layers.md` line 11.
- Suggested fix: add "(for S ≠ {c})".

**m5 (minor). The Sources table's "lines covered" column contradicts the Coverage paragraph.**
- Location: `ec.tex:28-34` against `ec.tex:842-844`.
- The column "Lean file (lines covered)" gives 1–123, 1–132, 1–291 and 1–152. Coverage says the `#print axioms`
  lines (119–123, 127–132, 285–291, 152) are deliberately not covered.
- Suggested fix: rename the column to "lines considered" or end the ranges at 118, 126, 284 and 151.

**m6 (minor, layout). Five statement heads with long `\leanref` lists overflow the margin.**
- Overfull boxes:
  - 30.8pt: Theorem ec:thm:l0 head, input lines 779–781. It visibly runs into the right margin on PDF p. 10.
  - 10.6pt: Proposition ec:prop:parity head, lines 644–646.
  - 5.1pt: Lemma ec:lem:pc-basic head, lines 601–603.
  - 4.4pt: Definition ec:def:compat head, lines 639–642.
  - 1.1pt: Theorem ec:thm:compat head, lines 667–669.
- Many underfull boxes come from `\sloppy`.
- Possible fixes: shorter heads; or put the second `\leanref` of Theorem ec:thm:l0 in a remark-free form the
  preamble supports, if the preamble has a line-break-friendly variant. A new macro is not allowed in the section, so
  any such variant would have to be requested.

**m7 (minor, style). Theorem ec:thm:compat(d) quantifies m a second time.**
- Location: `ec.tex:668, 677`.
- The theorem's preamble fixes "m ∈ ℕ and ζ ∈ K". Part (d) then says "For every m ∈ ℕ with 1 ≤ m", which shadows the
  outer m.
- The text flags that (d) does not involve K and ζ, so it is not ambiguous in practice.
- Suggested fix: move (d) out of the theorem, or drop the outer quantifier for (d).

**m8 (minor). Some file mentions are bare file names rather than RES-relative paths.**
- Locations: `ec.tex:39, 111, 400, 840-844`.
- Bare names such as `\dirn{ES7Corollaries.lean}`, `\dirn{C6check.lean}`, `\dirn{PolarOrient.lean}`,
  `\dirn{PCompatCore.lean}` and `\dirn{L0Check.lean}` appear after the full RES-relative path has been given.
- They are unambiguous within the section. Contract rule 3 asks for paths relative to RES.
- Suggested fix, optional: use the full relative path, or write "the file" in place of the bare name.

## Things I was unsure about (reported, judged not errors)
- **Lean-checked status of the ES8SYM theorems.** The compiled ES8SYM files have different hashes from the present
  copies. The section says this openly (`ec.tex:41-44`), and the Rigor paragraph still calls the ES8SYM theorems
  Lean-checked. Under contract rule 8 this is acceptable, but a fixer may want to repeat the caveat in the Rigor
  paragraph.
- **"Bridge them by a cast lemma" (`ec.tex:86`).** Lean uses `exact_mod_cast`/`simpa`, which applies the cast lemmas
  (`Nat.cast_ofNat`). The wording is accurate enough.
- **"Never compiled" for Composition311.lean.** A compile was attempted and killed at 1.63 GB. `ES8SLACK/README.md:403`
  itself says "It has not been compiled", so the wording matches the records.
