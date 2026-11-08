# Review: section `ec` (Small corollaries for k = 7 and k = 8), round 1, lens FIDELITY

Verdict: **PASS** (no blocker, no major finding; 6 minor findings).

Files reviewed: `sections/ec.tex` (851 lines) and `sections/ec.map.tsv` (41 rows), against
`LEANEXT/es7corr/ES7Corollaries.lean` 1148-1233 (and the copied LAYERLEAN prefix), `ES8SYM/lean/C6check.lean`,
`ES8SYM/lean/PolarOrient.lean`, `PRIMEFOLD/compat/lean/PCompatCore.lean`, `PRIMEFOLD/compat/lean/L0Check.lean`, their
`.out`/axioms logs, the inventories `LEANEXT.json` and `ES8-small.json`, and the Mathlib sources at the pinned commit
`f897ebcf` for every Mathlib notion the section paraphrases. Paths are relative to `cloud/es7-2026-10-19/results`
unless they start with `sections/` (staging area) or `Mathlib/` (pinned Mathlib).

## Findings (most significant first; all minor)

### F1 (minor). Overview item (2) states the threshold arithmetic with an unquantified `e`; read literally, it is false for m = 4
- Location: `sections/ec.tex:13` ("Also the threshold arithmetic $65\le mt+e\iff t\ge17,13,11,10$ for $m=4,5,6,7$").
- Issue: `e` is not quantified. If it ranges over {0,1} for every m (as in `thr_m5`/`thr_m7`), the m = 4 case is
  false: t = 16, e = 1 gives 65 <= 65 but not 17 <= 16. This is exactly item (v) of Proposition `ec:prop:thr`
  (`RefuteC6.m4_with_centre_counter`). The Lean statements `thr_m4` and `thr_m6` have no `e`
  (`C6check.lean:108,110`).
- Status: the formal Proposition `ec:prop:thr` (lines 374-384) is exact, and Remark `ec:rem:thr` explains e = 0 for
  even m. So only the introductory summary is wrong.
- Fix: "... $65\le mt+e\iff t\ge17,13,11,10$ for $m=4,5,6,7$, where $e\le1$ for $m=5,7$ and $e=0$ for $m=4,6$".

### F2 (minor). Overview item (1) drops finiteness
- Location: `sections/ec.tex:8-10` ("every set in general position that is invariant under a rotation by $2\pi/5$ and
  has at least $32$ points ...").
- Issue: the Lean theorems are about `Finset Point`. The theorem statements (lines 133-182) correctly say "finite set".
- Fix: "every finite set in general position ...".

### F3 (minor). The paraphrase of Mathlib's `CommGroupWithZero` and of the role of `DecidableEq` is slightly incomplete
- Location: `sections/ec.tex:586-588`.
- Issue 1: Mathlib's `GroupWithZero` (`Mathlib/Algebra/GroupWithZero/Defs.lean:203-207`) also has the field
  `inv_zero : 0⁻¹ = 0` and a division operation (`DivInvMonoid`). This is harmless: every structure as described
  extends uniquely by setting 0⁻¹ := 0, and no statement involves ⁻¹ or /.
- Issue 2: decidable equality is also needed for `insert 0 S` (`exists_card1`, `PCompatCore.lean:164`) and for the
  decidable test `if (0 : K) ∈ S` inside the statement of `card_mod` (`PCompatCore.lean:114`). It is not needed
  "only to form finite sets by image, difference and erasure".
- No effect on correctness.

### F4 (minor; uncertain, more a claims point). "No step ... is checked in Lean" may be slightly too strong for Fourfold32
- Location: `sections/ec.tex:105-106` (Remark `ec:rem:cases`: "no step from a formula or a certificate to these
  propositions is checked in Lean").
- For `Fivefold35` the sentence is accurate: SYM5 run P1 uses the angle normal form and no layer lemma.
- For `Fourfold32`, the C4CUT formula is the layered encoding. It relies on the layer lemma (C4CUT/README.md section 1:
  "Each layer is one rotation orbit, by the layer lemma ..."), and the layer lemma is Lean-checked in LAYERLEAN
  (`layers_are_orbits`), although nothing in Lean links it to the CNF.
- The encoder-soundness link is indeed not in Lean, so the sentence is defensible if "step" means that link. I am
  unsure whether other reviewers will read it that way.
- Suggested wording: "the link from a formula or certificate to these propositions (the encoder's soundness) is not
  checked in Lean; the layer lemma used by the layered encodings is Lean-checked in LAYERLEAN but not connected to
  the formula".

### F5 (minor). Unused notation that clashes with another use
- Location: `sections/ec.tex:226`.
- `C_r = {z : |z| = r}` is defined but never used afterwards. Lemma `ec:lem:sphere` says "every x with |x| = r".
- `C_4` and `C_5` denote cyclic symmetry groups at line 196 (`N(C_5) <= 31`).
- Fix: drop `C_r`, or rename it.

### F6 (minor, cosmetic). Overfull boxes in statement heads
- My separate compile check (see below) reports 5 overfull hboxes, all in `\leanref` heads.
- Sizes and lines: 5.1pt (602-603), 4.4pt (640-642), 10.6pt (645-646), 1.1pt (668-669), and 30.8pt at lines 780-781
  (head of Theorem `ec:thm:l0`).

No other issue found. Details of what was checked follow.

## 1. Statement-by-statement comparison with Lean

Every `\leanref` name exists, in the stated namespace, exactly at the cited line. An automated scan matched all 49
`\leanref` pairs, each with offset 0. For each statement I compared hypotheses, conclusion, quantifier order, types,
casts and natural subtraction.

| label | Lean declaration (file:line) | result |
|---|---|---|
| ec:def:cases | `ErdosSzekeres.LayerLemma.Fivefold35` (ES7Corollaries.lean:1157), `Fourfold32` (:1164) | exact. Finset, GP, card = 35/32, c ∉ S, Invariant (maps into) of `rotAbout c (2*π/5)` / `(2*π/4)` with real numerals, conclusion HasConvexNGon 7; hypothesis order also kept. |
| ec:thm:fivefold-erase | `fivefold_heptagon_of_erase` (:1170) | exact: H : Fivefold35, S, c, GP, Invariant(2π/5), `30 < (S.erase c).card`. |
| ec:thm:fivefold | `fivefold_heptagon` (:1183) | exact: `32 ≤ S.card`. |
| ec:thm:fivefold-nc | `fivefold_heptagon_of_centre_not_mem` (:1193) | exact: adds `c ∉ S`, `31 ≤ S.card`. |
| ec:thm:fourfold-erase | `fourfold_heptagon_of_erase` (:1203) | exact: `28 < (S.erase c).card`, 2π/4. |
| ec:thm:fourfold | `fourfold_heptagon` (:1216) | exact: `29 ≤ S.card`. |
| (R), (C) restated | `convexNGon_of_layers` (LAYERLEAN/LayerLemma.lean:1066), `centre_not_mem_of_even` (:582) | exact: 0 < m, K ≤ 2m, premise H with the same hypothesis order, `m*(t-1) < (S.erase c).card` with natural subtraction noted; even m, p ∈ S, p ≠ c. Consistent with how sections ll and lg state `ll:thm:reduction` and `lg:lem:centre`. |
| ec:lem:sphere | `RefuteC6.sphere_subset_extremePoints` (C6check.lean:24) | exact (∀ r : ℝ, sphere 0 r ⊆ extremePoints of closedBall 0 r). The definition of extreme point given in the section ("x₁ = x" only) is exactly Mathlib's definition at f897ebcf (`Mathlib/Analysis/Convex/Extreme.lean:64-65`; `mem_extremePoints_iff_left` is `.rfl`). |
| ec:lem:ci-circle | `RefuteC6.convexIndependent_of_norm_eq` (:43) | exact (any ι, injective f, ‖f i‖ = r). ConvexIndependent paraphrase = Mathlib def (`Mathlib/Analysis/Convex/Independent.lean:53`). |
| ec:def:zeta | `RefuteC6.zeta` (:60) | exact; cast of m to ℂ and m = 0 behaviour stated. |
| ec:lem:zeta | `RefuteC6.zeta_prim` (:62) | exact (m ≠ 0). IsPrimitiveRoot paraphrase = Mathlib structure. |
| ec:lem:orbit8 | `orbit_injective` (:66), `orbit_convexIndependent` (:75) | exact (8 ≤ m, p ≠ 0, k ↦ p·ζ_m^k on Fin 8). |
| ec:thm:big-order | `RefuteC6.part_a` (:85) | exact: Set ℂ (no finiteness, no general position), forward invariance under exp(2πi/m), the hypothesis "every injective Fin 8 → ℂ family with values in S is not convex independent" in the same quantifier order, conclusion S ⊆ {0}. |
| ec:prop:thr | `thr_m4`..`thr_m7` (:108-111), `m4_with_centre_counter` (:115) | exact, including `c ≤ 1` only for m = 5, 7 (renamed e and declared). |
| ec:def:polar | `C7.cross` (:45), `pt` (:48), `coef` (:63), `phase` (:94), `ngonPt` (:97) | exact. `phase` = θ_o + (2π k)/m with casts as in Lean. Pi.single is the unit vector; coefficients add on coinciding layers. |
| ec:lem:det-mul | `C7.det_mul_eq` (PolarOrient.lean:24) | exact (u_k ≠ 0; D·(u₁u₂u₃) = Σ; matrix rows as in `!![...]`). |
| ec:lem:polar-u | `C7.orient_polar` (:37) | exact (u_k > 0; sign D = sign Σ). |
| ec:lem:polar-cross | `C7.orient_polar_cross` (:50) | exact. |
| ec:prop:layered | `C7.orient_layered` (:68) | exact (any ι, L, φ, u > 0, i, j, k not necessarily distinct; sum over Fin t). |
| ec:cor:scale | `C7.orient_layered_scale` (:80) | exact (λ > 0, λ·u(L i)). |
| ec:lem:ngon-pt | `C7.ngonPt_eq_pt` (:100) | exact (u = 1 / r p.1). |
| ec:thm:nested | `C7.nested_regular_orient` (:108) | exact (only r_o > 0; coef Prod.fst (phase m θ); weight 1/r_o). |
| ec:lem:centre-u | `C7.orient_centre` (:116) | exact. |
| ec:lem:pc-basic | `ne_zero_of_order` (PCompatCore.lean:36), `pow_inj_of_order` (:43), `pow_mul_mem` (:58) | exact. (O), (R0), (RD) transcribe hm/hζm/hprim, hr0, hdisj literally. |
| ec:lem:pc-exist | `exists_card0` (:129), `exists_card1` (:160) | exact (hypotheses hr0, hdisj stated; conclusions invariant ∧ 0 ∉ S ∧ card = m t, resp. card = m t + 1). |
| ec:def:compat | `PCompat.Compat` (:205) | exact (N % m = 0 ∨ N % m = 1 % m; m = 0 and m = 1 remarks correct). |
| ec:prop:parity | `compat_even` (:208), `compat_odd` (:235) | exact (2 ≤ m even; 3 ≤ m odd). |
| ec:thm:compat | `dvd_card` (:67), `card_mod` (:112), `exists_iff` (:174), `classification` (:253) | exact. (b) `(if 0 ∈ S then 1 else 0) % m`; (c) RHS is the unfolded Compat; (d) 1 ≤ m with the three alternatives. |
| ec:prop:ex341 | `PCompat.ex341` (:277) | exact (six conjuncts). Labelled computer-assisted. The description of the Lean check is accurate: five `decide`s, `exponentiation.threshold 400`, and `Nat.not_prime_mul`, whose pinned signature takes `a ≠ 1`, `b ≠ 1` (`Mathlib/Data/Nat/Prime/Basic.lean:24`), as the section says. The hand arithmetic 1024 = 93·11+1 = 33·31+1 = 3·341+1 is correct. |
| ec:lem:arith | `L0Check.arith` (L0Check.lean:21) | exact. The FermatPsp paraphrase = Mathlib (`Mathlib/NumberTheory/FermatPsp.lean:51-60`: n ∣ b^(n-1) - 1 ∧ ¬prime ∧ 1 < n), natural subtraction noted. |
| ec:lem:orbit-dvd | `L0Check.orbit_dvd` (:60) | exact. |
| ec:thm:l0 | `L0Check.L0` (:122), `L0_rot` (:144) | exact (2 ≤ m; primitive root, resp. exp(2πi/m); forward invariance; card = 2^(m-1); same disjunction). |

Written steps (`ec:fact:prim`, `ec:cor:planar`) are tagged "written step" and have `-` in the map. I checked the
unfolding of ConvexPosition/HasConvexNGon in `ec:cor:planar` against `ErdosSzekeres/Definitions.lean:17-22` and
against `fd:def:cp`/`fd:def:ngon`. The rotation identity φ(rotAbout(c,θ)p) = e^{iθ}φ(p) follows from the fd formula.

Hypotheses as hypotheses (contract rule 7):
- The five ES(7) theorems say "Assume Fivefold35/Fourfold32" in the statement.
- Remark `ec:rem:cases` names SYM5 and C4CUT, with the label "computer-assisted" and cake_lpr acceptance (checked
  against SYM5/README.md, table rows P1 and L1, and C4CUT/README.md).
- hr0 and hdisj are stated as hypotheses. Remark `ec:rem:compat`(ii) correctly says they are not discharged in Lean.

Mathlib paraphrases checked at f897ebcf: Set.extremePoints, openSegment, ConvexIndependent, IsPrimitiveRoot,
Complex.isPrimitiveRoot_exp, IsPrimitiveRoot.{ne_zero, norm'_eq_one, pow_inj, pow_ne_one_of_pos_of_lt},
Nat.dvd_prime_pow, Nat.not_prime_mul, Nat.FermatPsp/ProbablePrime, GroupWithZero (see F3), and SignType.sign (values
-1/0/1). All match.

## 2. Other factual claims checked (all correct)
- Lines 1-1147 of ES7Corollaries.lean = lines 1-1147 of LAYERLEAN/LayerLemma.lean (re-run diff: identical).
  LayerLemma.lean has 1148 lines; its last line is `end ErdosSzekeres.LayerLemma`. Invariant :105, rotAbout :298,
  centre_not_mem_of_even :582 and convexNGon_of_layers :1066 are correct.
- SHA-256 prefixes: all five match (5883c8ebac55, 92f15b5cc907, 6e54f5f83a19, ebc6aacefadb, 05a67c3b8b16). The
  recorded prefixes agree in es7corr/REPORT.md:3 and PRIMEFOLD/README.md:35,38. ES8SYM/README.md:258-260 records
  8c090168/4d42e2fb and the "four comment lines" remark, as the section says.
- Line ranges in the sources table: 1233, 123, 132, 291, 152.
- Pins: lean-toolchain v4.24.0 and the Mathlib rev f897ebcf in lake-manifest.json. The records state the compile
  environment.
- Axioms paragraph: every listed theorem and axiom set matches `es7corr/axioms.log`, `C6check.out`,
  `PolarOrient.out`, `PCompatCore.out` (ex341: [propext] only) and `L0Check.out`.
  - `m4_with_centre_counter` has no axiom line.
  - Every other covered declaration is used, transitively, by a printed theorem.
  - A grep finds no sorry, admit, native_decide or axiom in the five files, and no `#print` in ES7Corollaries.lean.
- Mutant logs: the failures are at the final `omega` lines 1189 (fivefold_heptagon) and 1231 (fourfold_heptagon).
- SYMLEAN/SymmetricReduction.lean:477/:496 have the same text, in namespace ErdosSzekeres.SymReduction, with their own
  Invariant (:271) and rotAbout (:400). No Lean file mentions both namespaces' constants. The copied Fourfold32
  docstring is as described.
- LAYERLEAN/LayerLemma.lean:935 `orient_polar` (radius form, polar at :932) matches Remark `ec:rem:polar`(ii). The
  identity "right side × u₁u₂u₃ = Σ" with r = 1/u checks term by term. p1.tex:380 and k8_soundness.tex:449,480 cite
  the radius form.
- ES8SYM/proofs/layers.md: Lemma 1 at lines 15-29, Lemma 2 at 31-43, the general-position remark at 41-42.
  symmetric_es7.tex prop:C (:326) and lem:sizes (:58), and symmetric_extremal.tex prop:compat (:355) and prop:k8sizes
  (:520) say what the remarks attribute to them. PRIMEFOLD/cluster/PROOFS.md Lemma 0 excludes the centre by general
  position (:62).
- Cited files exist: SYMMAX/c5_31points.txt, SYMMAX/c4_28points.txt, ES8SLACK/proofs.md and the four ES8SLACK Lean
  files.

## 3. Coverage and export labels
- All declarations of the scope are covered:
  - every declaration of ES7Corollaries 1148-1233;
  - all of C6check (including m4_with_centre_counter as an arithmetic fact);
  - all 13 of PolarOrient;
  - all 13 of PCompatCore;
  - all 4 of L0Check.
- Coverage lists the `#print axioms` lines with correct line ranges (C6check 119-123, PolarOrient 127-132,
  PCompatCore 285-291, L0Check 152), the copied prefix 1-1147, and ES8SLACK as out of scope, with a pointer to
  ES8SLACK/proofs.md and the two uncompiled files named.
- Export labels: all are defined on the named statements.
  - `ec:thm:fivefold` → fivefold_heptagon; the variants carry their own labels.
  - `ec:thm:fourfold` → fourfold_heptagon.
  - `ec:thm:big-order` → part_a.
  - `ec:lem:polar-u` → C7.orient_polar.
  - `ec:thm:nested` → nested_regular_orient.
  - `ec:thm:compat` → dvd_card, card_mod, exists_iff, classification.
  - `ec:thm:l0` → L0, L0_rot.
- `\ref`s: only to ec labels (all defined) and to allowed export labels: fd:def:{point,orient,gp,cp,ngon,inv,rot},
  ll:thm:reduction, ll:lem:minperiod, ll:thm:layers, ll:thm:card-peel, lg:lem:centre, lg:lem:polar and sr:def:classes.
  These labels exist in the other sections on the expected declarations.
- Map: 41 rows. They agree one to one with the 41 statement environments (label and kind), and the lean_name and
  file_line columns match the `\leanref` heads exactly.

## 4. Mechanical checks
- Compile: a separate wrapper (`build/ecfid/ecfid_wrapper.tex`), `nice -n 15 pdflatex` run twice, exit 0 both times.
  The only undefined references are to fd/ll/lg/sr export labels; there are no errors and no "Missing $". See F6 for
  the overfull boxes.
- No `\newcommand`, `\usepackage` or preamble material. The file starts with `\section{...}\label{ec:sec}`.
- No machine paths and no tool names in `ec.tex` or `ec.map.tsv`.
- Restricted rigor wording: none. "proves" is used only for Lean proofs and for "we prove it here" (a written step).
