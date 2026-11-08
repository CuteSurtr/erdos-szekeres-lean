# Review sr, round 1, lens: fidelity

Section: `STAGE/sections/sr.tex` (1057 lines), map: `STAGE/sections/sr.map.tsv` (46 rows).
Lean source: `SYMLEAN/SymmetricReduction.lean`, lines 1-1059 (paths relative to RES; main library relative to the
repository root).

**Verdict: pass.** No blocker and no major finding. Eight minor findings (F1-F8). None of them changes a statement
that corresponds to a Lean declaration; all 46 statement environments, all 73 `\leanref` entries and all 72
declarations of the file were checked against the Lean source.

## 1. What was checked

### 1.1 Names and line numbers

A script read every `\leanref{Name}{File:Line}` in the section (73 entries) and searched for
`def|theorem|lemma Name` within 3 lines of the cited line of the cited file. Result: 73 of 73 found, all at offset 0
(the cited line is the declaration line). This includes `ErdosSzekeres.Suk.convexPosition_of_strict_supports` at
`ErdosSzekeres/Suk/SupportingLines.lean:28`.

Line numbers cited in prose were checked by hand:
- `ConvexPosition.hasConvexNGon`, `ErdosSzekeres/Basic.lean:31`: correct.
- `Mir.reflLine`, `H3/MirrorEncoding/Line.lean:18`: correct, body byte-for-byte the same as `reflLine` (line 423).
- `Mir.MirrorExclusionLine`, `H3/MirrorEncoding/Line.lean:94`: correct, same text as `MirrorExclusionLineCopy`
  (line 1052).
- `Mir.mirrorExclusionLine_of_unsat` (Line.lean:139) and `Mir.mirrorExclusionLine_of_cubes` (Line.lean:147): exist;
  both take `¬DimacsSatisfiable ...` hypotheses, as the section says.
- `mirrorOneAxis33_iff_exclusionLine`, `SYMLEAN/review/ReviewSanity.lean:1629`, and
  `exclusionLine_of_mirrorOneAxis33`, line 1593: correct (namespace `ErdosSzekeres.SymReduction.Review`, see F3).
- `group_form`, `SYMLEAN/review/VariantChecks.lean:1168`: exists (namespace `...SymReduction.VariantChecks`).
- `mirrorOneAxis33_proved` (4274), `mirrorNoAxis34_proved` (4282), `heptagon_of_nontrivial_isometry_3` (4292) in
  `SYMLEAN/mirror/ReductionThreeClasses.lean`: exist; `_3` takes exactly `HalfTurn34`, `Threefold33`, `Fivefold35`.
- Mathlib names quoted in written steps (checked in the pinned Mathlib source, rev f897ebcf):
  `Function.minimalPeriod`, `IsPeriodicPt.minimalPeriod_dvd`, `minimalPeriod_eq_one_iff_isFixedPt`,
  `iterate_minimalPeriod`, `iterate_injOn_Iio_minimalPeriod`, `Set.Finite.exists_lt_map_eq_of_forall_mem`,
  `IsPrimitiveRoot` (fields `pow_eq_one`, `dvd_of_pow_eq_one`), `IsPrimitiveRoot.orderOf`, `orderOf_eq_one_iff`,
  `IsPrimitiveRoot.pow` (`0 < n`, `n = a * b`), `eq_neg_one_of_two_right`, `ne_one` (`1 < k`), `ne_zero` (`k ≠ 0`),
  `eq_pow_of_pow_eq_one` (`[NeZero k]`, matching the "k>0" of (P5)), `Complex.isPrimitiveRoot_exp` (`n ≠ 0`),
  `Isometry.affineIsometryOfStrictConvexSpace`, `linear_isometry_complex`, `Complex.cpow_nat_inv_pow`. All exist with
  the hypotheses the section states.

### 1.2 Statements against Lean, one by one

For each statement environment with a Lean reference I compared hypotheses, conclusion, binder order, types (Finset vs
Set, ℕ vs ℝ vs ℂ, casts), strict vs weak inequalities, maps-into vs equality, and implicit arguments.

| label | Lean declaration(s), line | result |
|---|---|---|
| sr:def:iso | eDist2 265, IsEucIsometry 268 | matches: `(p0-q0)^2+(p1-q1)^2`; `∀ p q`, whole plane, nothing else assumed |
| sr:def:inv | Invariant 271 | matches: `∀ p ∈ S, f p ∈ S` (maps into), `S : Finset Point` |
| sr:def:complex | toC 274, ofC 277 | matches: `⟨p 0, p 1⟩`, `![z.re, z.im]` |
| sr:lem:complex | toC_re 279, toC_im 280, ofC_zero 281, ofC_one 282, toC_ofC 284, ofC_toC 287, toC_injective 291, eDist2_eq_normSq 294, eDist2_pos_of_ne 297, point_ext 502 | matches item by item; (e) has `p ≠ q`, strict `0 <` |
| sr:def:maps | crot 349, rotAbout 400, halfTurn 413, reflLine 423 | matches; rotAbout coordinates and signs exact; reflLine `d = (p0-a0)u0+(p1-a1)u1`, no unit hypothesis in the definition (the section says so) |
| sr:def:classes | HalfTurn34 467, Threefold33 472, Fivefold35 477, MirrorOneAxis33 482, MirrorNoAxis34 488, Fourfold32 496 | all six verbatim: exact sizes 34/33/35/33/34/32 (`=`), `c ∉ S`, angles `2*π/3`, `2*π/5`, `2*π/4` (not simplified), `u0^2+u1^2=1` first, fixed-point clause `∃ x ∈ S, σ x = x ∧ ∀ y ∈ S, σ y = y → y = x`, `∀ p ∈ S, σ p ≠ p`; same hypothesis order |
| sr:lem:iterate | iterate_mem 69, Invariant.iterate 309 | matches (general type for (a); `∀ i`) |
| sr:def:orbitFS | orbitFS 65 | matches: image of `range p`; DecidableEq noted |
| sr:lem:orbitFS | mem_orbitFS_self 90, orbitFS_subset 93, orbitFS_invariant 99, card_orbitFS 76, card_orbitFS_of_minimalPeriod 111 | matches: (a) `0<p`; (b) any p; (c) `0<p`, `f^[p] x = x`; (d) prime, `f^[p] x = x`, `f x ≠ x`; (e) `minimalPeriod f x = p` only |
| sr:lem:orbit | orbit_select_minimalPeriod 123, orbit_select 194 | matches: `0 < p` (resp. prime) before `∀ S`; invariance, `Set.InjOn`, per-point hypotheses; conclusion `p ∣ card ∧ ∀ k, k*p ≤ card → ∃ T ⊆ S, invariant ∧ card = k*p` |
| sr:lem:crot | toC_crot 351, crot_one 354, crot_comp 359, crot_iterate 364, crot_eq_self_iff 370, crot_injective 384, eDist2_crot_center 394 | matches; (e) `w ≠ 1`, iff with `toC p = c`; (f) `w ≠ 0`; (g) `normSq w = 1`, centre `ofC c` |
| sr:lem:rot-half | rotAbout_eq_crot 404, halfTurn_eq_crot 415 | matches: `crot (toC c) (exp (θ * I))`, `crot (toC c) (-1)`; equality of maps |
| sr:lem:refl | toC_reflLine 427, reflLine_involutive 435, cross_of_reflLine_fixed 447, orient_eq_zero_of_cross 455 | matches; (c) has no hypothesis on u (stated); (d) no distinctness |
| sr:lem:toC-iso | IsEucIsometry.injective 301, isometry_toC_conj 313 | matches; Mathlib `Isometry` on ℂ correctly identified with `|G z - G w| = |z - w|` |
| sr:thm:structure | isometry_complex_cases 321, isometry_structure 869 | matches: (a) `∃ a b, ‖a‖ = 1 ∧ (∀ z, G z = a z + b) ∨ (∀ z, G z = a·conj z + b)`; (b) `1 < S.card`, `IsEucIsometry g`, `g ≠ id`, `Invariant g S`; (i) `∃ c a : ℂ, g = crot c a ∧ a ≠ 1 ∧ ∃ m, 0 < m ∧ a^m = 1`; (ii) `∃ A u, u0^2+u1^2 = 1 ∧ g = reflLine A u` |
| sr:lem:supports | Suk.convexPosition_of_strict_supports (SupportingLines.lean:28) | matches: `∀ p ∈ s, ∃ q, ∀ r ∈ s, r ≠ p → 0 < orient p q r` |
| sr:lem:concyclic | convexPosition_of_concyclic 509 | matches: any `r : ℝ`, no general position |
| sr:cor:concyclic | hasConvexNGon_of_concyclic 522 | matches: `T ⊆ S`, concyclic on T, `n ≤ T.card` ⇒ `HasConvexNGon n S` |
| sr:lem:center | center_not_mem_of_halfTurn 528 | matches: `2 ≤ S.card` (not 3) |
| sr:lem:rot345 | isPrimitiveRoot_rot3 584, _rot5 591, _rot4 598 | matches: `exp (↑(2*π/n) * I)` with the real angle cast |
| sr:lem:root-cases | root_cases 552 | matches: `0 < m`, `a^m = 1`, `a ≠ 1`; `(∃ k, a^k = -1) ∨ ∃ p k, p.Prime ∧ p ≠ 2 ∧ IsPrimitiveRoot (a^k) p` |
| sr:lem:prime-cases | prime_cases 572 | matches: `p = 3 ∨ p = 5 ∨ 7 ≤ p` |
| sr:lem:root-cases2 | root_cases2 607 | matches: `a = -1 ∨ (∃ k, IsPrimitiveRoot (a^k) 4) ∨ ∃ p k, ...` |
| sr:lem:halfturn-facts | halfTurn_facts 647 | matches (`k*2` written `2k`) |
| sr:lem:case-halfturn | case_halfTurn 670 | matches; `HalfTurn34` stated as a hypothesis |
| sr:lem:rot-erase | rot_erase_facts 676 | matches: `S.erase (ofC c)`; `T ⊆ S`, `ofC c ∉ T`, invariant, `card = k*p` |
| sr:lem:rot-big | case_rot_big 711 | matches: prime, `7 ≤ p`, `w^p = 1`, `w ≠ 1`, invariant, `2 ≤ S.card`; no general position (stated) |
| sr:lem:odd-prime | case_odd_prime 736 | matches; classes stated as hypotheses; `IsPrimitiveRoot w p`, `p ≠ 2` |
| sr:lem:fourfold | case_fourfold 763 | matches; `IsPrimitiveRoot w 4` |
| sr:lem:mirror | case_mirror 811 | matches; unit u; `33 ≤ S.card` |
| sr:thm:main | heptagon_of_nontrivial_isometry 997 | matches; the five classes are hypotheses (binders h2 h3 h5 hm1 hm0); binder order S, g, hgp, hcard, hg, hne, hinv |
| sr:thm:variant | halfTurn_of_symmetric_counterexample 1024 | matches; conclusion `∃ c, g = halfTurn c ∧ c ∉ S ∧ 2 ∣ S.card ∧ 34 ≤ S.card` |
| sr:def:exclusion-line | MirrorExclusionLineCopy 1052 | matches; no axis-point clause; invariance written out as `∀ q ∈ S, reflLine a u q ∈ S` |
| sr:lem:mirror-line | mirrorOneAxis33_of_exclusionLine 1056 | matches |

The written steps (sr:lem:pigeon, sr:def:minper, sr:lem:minper, sr:lem:orbit-core, sr:def:prim, sr:lem:prim) agree
with the Lean local statement `pigeon` (isometry_structure, line 875) and with the Mathlib facts they name.

The algebraic identities used in the proofs of sr:lem:refl(a), sr:lem:refl(d) and sr:lem:concyclic were re-checked
with sympy (all differences reduce to 0, resp. to `x(u0²+u1²−1)`, `y(u0²+u1²−1)` as stated).

### 1.3 Export labels and coverage

- Every export label of the contract for `sr` is defined on the named statement: `sr:def:iso` (eDist2, IsEucIsometry),
  `sr:def:classes` (all six classes), `sr:thm:structure` (isometry_structure with isometry_complex_cases),
  `sr:lem:concyclic`, `sr:lem:orbit` (both orbit-selection lemmas), `sr:thm:main`, `sr:thm:variant`,
  `sr:lem:mirror-line`.
- The file has exactly 72 declarations (17 definitions, 55 theorems; counted from the source). The Coverage paragraph
  lists all 72, and each is attached to a statement with the correct line. The claim "All 72 declarations ... are
  covered" is correct.
- Every scope item of the task (pigeonhole periodicity, orbit_select, orbit_select_minimalPeriod, eDist2,
  IsEucIsometry with the sup-metric remark, Invariant, rotAbout, halfTurn, reflLine and their lemmas,
  isometry_complex_cases, isometry_structure, convexPosition_of_concyclic and its HasConvexNGon corollary,
  center_not_mem_of_halfTurn, halfTurn_facts, root_cases, root_cases2, prime_cases, the six case lemmas, the six class
  Props, the two main theorems, the bridge) is covered.
- Map: 46 rows, one per statement environment; label, kind, Lean names and file:line columns agree with the statement
  heads exactly (checked by script). Notes "takes hypotheses: ..." are present on every row whose Lean declaration
  takes a class.

### 1.4 Sources, logs, rigor statements

- SHA-256 prefixes recomputed: SymmetricReduction.lean `6d5ec90a4215`, SymmetricReductionAxioms.lean `7bf809cbdc77`,
  Definitions `2425500eefd1`, Basic `13667aa2d3dc`, Orientation `f67955ac7091`, OrientationGeometry `c7db9bbbb65e`,
  Suk/SupportingLines `6a8e12677685`: all as stated. 1059 lines: correct.
- SymmetricReductionAxioms.lean: lines 1-1059 byte-identical to the main file (cmp), then a blank line and two
  `#print axioms` lines: as stated. ReviewSanity.lean and VariantChecks.lean: lines 1-1059 byte-identical (cmp).
  AffineReduction.lean: lines 1-1058 identical (line 1059 starts §9): as stated in Coverage.
- `logs/SymmetricReduction.out` is empty; `logs/runs.tsv` has exit 0 with sha256 prefix `6d5ec90a`, matching the file.
  `logs/SymmetricReductionAxioms.out` shows `[propext, Classical.choice, Quot.sound]` for both theorems.
  `logs/ReviewSanity.out` shows the same three axioms for `mirrorOneAxis33_iff_exclusionLine`.
- No `axiom`, `decide`, `native_decide`, `sorry`, `admit` in the file or in the transitively imported repository
  modules (Definitions, Basic, Orientation, OrientationGeometry, Suk/TriangleOrder, Suk/BaseChart, Suk/BaseOrder,
  Suk/SupportingLines); the only hit is the word "axiom" in a comment of Definitions.lean.
- Toolchain: `lean-toolchain` = v4.24.0, `lake-manifest.json` Mathlib rev `f897ebcf72cd...`: as stated.
- Rigor labels: classes are presented as hypotheses everywhere (statements of sr:lem:case-halfturn, sr:lem:odd-prime,
  sr:lem:fourfold, sr:lem:mirror, sr:thm:main, sr:thm:variant, sr:lem:mirror-line); Remark sr:rem:records gives the
  label of each class (computer-assisted for HalfTurn34, Threefold33, Fivefold35, Fourfold32; Lean-checked in
  `SYMLEAN/mirror` for the two mirror classes). The docstring wordings "Corollary 3 exactly as written" and
  "Lean-verified there from CNF facts" are not repeated. Record paths named in Remark sr:rem:records (C2FINAL, C2C34,
  C2P-C2P5, C2RECHECK, C2ENC/proof.md, C2ENC/class_table.md, C2ENC/perturbation.md, C3FINAL, C3SPOT,
  C3-S/soundness.md, C3a, SYM5, SYMLEAN/mirror, SYMZ, WRITEUP/SYMMETRIC.md, H3, C4CUT) all exist; the numbers 120,
  116,883 and 2,120 agree with the records.

### 1.5 LaTeX

Compiled twice with a separate job name (`nice -n 15 pdflatex ... -jobname=...`, files removed afterwards): exit 0
both times. Undefined references only to `fd:` labels, `mb:thm:classes`, `mb:thm:main3`, `ar:thm:main` (all export
labels of other sections; all defined there). No `\newcommand`, no `\usepackage`, no machine path, no tool name. All
labels start with `sr:`.

## 2. Findings

### F1 (minor). "over the same reflLine" in Remark sr:rem:mirror-line

Location: sr.tex line 983 (Remark sr:rem:mirror-line), also lines 986-988.

`MirrorExclusionLineCopy` (line 1052) is stated over `ErdosSzekeres.SymReduction.reflLine` (line 423), while
`Mir.MirrorExclusionLine` (H3/MirrorEncoding/Line.lean:94) is stated over `Mir.reflLine` (Line.lean:18). These are two
different Lean constants with byte-identical bodies, in two separately compiled developments. No Lean theorem of this
unit identifies the two Props; `SYMLEAN/README.md` §5 mentions an `rfl` check in a file that is not in the repository.
So the sentence "Lemma sr:lem:mirror-line supplies MirrorOneAxis33 only conditionally on those CNF facts" also rests
on this textual identification.

Suggested fix: "over a textually identical \lean{reflLine} (\lean{Mir.reflLine}, \dirn{H3/MirrorEncoding/Line.lean:18});
the two Props are identified by their text, not by a Lean theorem of this unit", and add "and on this identification"
after "conditionally on those CNF facts".

### F2 (minor). The first sentence of Remark sr:rem:records is not accurate for the H3 route

Location: sr.tex lines 225-227.

"For no class is the step from a SAT certificate to the Lean class Lean-checked: that step rests on written soundness
proofs of the encoders and on the review of the class definitions". For the H3 route to `MirrorOneAxis33` (named in
the same remark, line 245-246), the step from the CNF facts to the class is Lean-checked:
`Mir.mirrorExclusionLine_of_unsat (h1 : ¬DimacsSatisfiable (hullCnf 33 7)) (h2 : ¬DimacsSatisfiable (interiorCnf 33 7))
: MirrorExclusionLine` (Line.lean:139). What lies outside Lean there is the certificate check (recorded cake_lpr
verdicts, proofs not retained) and the textual identification of F1, not a written encoder proof. The first clause
("not Lean-checked") stays true; the second clause is wrong for this route. The status of the class is not affected
(it is also Lean-checked from Baek's theorem).

Suggested fix: restrict the sentence to the certificate records of `C2*`, `C3*`, `SYM5`, `SYMZ` and `C4CUT`, or add
"except for the H3 chain, whose encoder is Lean-checked and whose CNF facts are recorded verdicts
(Remark sr:rem:mirror-line)".

### F3 (minor). Namespaces of review-file names

Location: sr.tex lines 101-103 (convention), 54-55, 961, 989.

The convention says "All Lean names of this section are in the namespace ErdosSzekeres.SymReduction unless stated
otherwise". The review names used are in sub-namespaces: `ErdosSzekeres.SymReduction.Review.mirrorOneAxis33_iff_exclusionLine`,
`ErdosSzekeres.SymReduction.Review.exclusionLine_of_mirrorOneAxis33`, `ErdosSzekeres.SymReduction.VariantChecks.group_form`.
Read with the convention, `ErdosSzekeres.SymReduction.group_form` etc. do not exist.

Suggested fix: write `Review.mirrorOneAxis33_iff_exclusionLine`, `Review.exclusionLine_of_mirrorOneAxis33`,
`VariantChecks.group_form`, or say "unless stated otherwise; the review files use the sub-namespaces Review and
VariantChecks".

### F4 (minor). Coverage says the review files are mentioned "only in Remarks ..."

Location: sr.tex lines 1054-1056.

`SYMLEAN/review/ReviewSanity.lean` and its log are also used in the paragraph "Axioms and rigor" (lines 54-57) as the
axiom evidence for `mirrorOneAxis33_of_exclusionLine`. The word "only" is inaccurate.

Suggested fix: "(audit files, mentioned only in the paragraph on axioms and in Remarks ...)".

### F5 (minor). Lemma sr:lem:prim (P1): the letter n is both fixed and defined

Location: sr.tex lines 655-658.

The lemma fixes "n,k,d∈N" and (P1) then says "If ζ^m=1 for some m>0, then n=ord(ζ)>0, ...". Read literally, this
asserts that the arbitrary fixed n equals ord(ζ), which is false. The intended reading (and the use in the proofs of
sr:lem:root-cases and sr:lem:root-cases2) is "with n=ord(ζ): n>0, ...". Written step; no Lean statement is affected.

Suggested fix: "(P1) If ζ^m=1 for some m>0, then ord(ζ)>0, ζ is a primitive ord(ζ)-th root of unity, and ord(ζ)=1 if
and only if ζ=1."

### F6 (minor). Where the form of g is proved

Location: sr.tex lines 113-115.

"That g has the form z↦az+b or z↦a z̄+b is proved in Theorem sr:thm:structure(a)." Part (a) is about an isometry G of
ℂ; for g one needs first Lemma sr:lem:toC-iso(b) (G = toC∘g∘ofC is an isometry of ℂ). The proof of (b) does exactly
this, so it is only a wording issue.

Suggested fix: "... in complex coordinates, by Lemma sr:lem:toC-iso(b) and Theorem sr:thm:structure(a)."

### F7 (minor, precision). The mirror classes proved in SYMLEAN/mirror are byte-identical copies

Location: sr.tex lines 242-244 (Remark sr:rem:records) and 922-923 (Remark sr:rem:main).

`SYMLEAN/mirror/ReductionThreeClasses.lean` cannot import this file; its lines 38-1559 are a verbatim copy of
`SYMLEAN/AffineReduction.lean` lines 12-1533 (checked with diff), which contains lines 12-1058 of this file. So
`mirrorOneAxis33_proved`, `mirrorNoAxis34_proved` and `heptagon_of_nontrivial_isometry_3` are about the copies of
`MirrorOneAxis33`, `MirrorNoAxis34` and `heptagon_of_nontrivial_isometry` in that file (same full names, same text).
The section's claims are right in substance; one clause would make the identification explicit (unless section mb
already says it).

Suggested fix: add "(for the byte-identical copies of these definitions in that file)".

### F8 (minor, precision). Description of the Mathlib theorem used for part (a)

Location: sr.tex lines 520-522.

"an isometry between strictly convex real normed spaces is affine": Mathlib's
`Isometry.affineIsometryOfStrictConvexSpace` needs only the codomain to be strictly convex
(`[StrictConvexSpace ℝ E]` for `f : PF → PE`). The sentence describes a correct special case (ℂ is both), so nothing
is wrong; optional precision: "an isometry of a real normed space into a strictly convex one is affine".

## 3. Things checked and found correct that a reader might doubt

- The classes are exactly as in Lean, including the unsimplified angle `2π/4` of `Fourfold32` and the order of the
  hypotheses (unit `u` first in the mirror classes).
- `center_not_mem_of_halfTurn` needs `2 ≤ |S|` (not 3); `case_rot_big` assumes no general position;
  `convexPosition_of_concyclic` allows any real `r`; `orbit_select` keeps its (redundant) injectivity hypothesis; the
  section states all four faithfully and remarks on them.
- `isometry_structure`: `g ≠ id` is an inequality of maps of the whole plane, and `IsEucIsometry` assumes nothing but
  distance preservation on the whole plane; both are stated so.
- `halfTurn_of_symmetric_counterexample`: `g = halfTurn c` is an equality of maps; `c ∉ S`, `2 ∣ |S|`, `34 ≤ |S|`; the
  section neither drops nor adds a conjunct, and Remark sr:rem:variant correctly limits it to one isometric symmetry at a
  time.
- `MirrorExclusionLineCopy` has no axis-point clause; the bridge does not use the fixed-point hypothesis; the converse
  is correctly located (review file, line 1593) and its arithmetic (|F| ≤ 2, |M| even, |F|+|M| = 33 ⇒ |F| = 1) is right.
