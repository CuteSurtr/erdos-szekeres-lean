# Section sr, polish round 1: independent referee report

Lens: referee (full independent read). Files: `STAGE/sections/sr.tex` (1116 lines), `STAGE/sections/sr.map.tsv`
(46 rows). Lean source: `RES/SYMLEAN/SymmetricReduction.lean` (all 1059 lines read), the eight imported repository
modules, `ErdosSzekeres/Suk/SupportingLines.lean:28`, and the files cited in the remarks. Earlier reports were read
only after the checks below were done.

**Verdict: pass.** No blocker and no major finding. Four minor findings, all in the record remarks; none affects a
statement, a proof or a rigor label of a statement of this section.

## What was checked

1. **Fidelity of every Lean-referenced statement (72 declarations).** Each statement was compared with its Lean
   declaration: hypotheses, conclusion, quantifier order, implicit/explicit binders, `Finset` vs set, maps-into
   (`Invariant`) vs equality, natural-number subtraction (`|S'| >= |S| - 1`, `j - i`, `d - j + i`, `p - 1`,
   `k'p <= |S| - p`, all with the needed order hypotheses), division (`c = b/(1-a)` with `a != 1`; `n/p`, `n/4` with
   divisibility), casts (`(j:C) - i != 0`; angles `2 * Real.pi / 3` etc. with real numerals). All 72 match, including
   `orbit_select` (prime `p`, injectivity, `f^[p] y = y`, no fixed point), `rot_erase_facts` (`T ⊆ S`, not `T ⊆ S'`),
   `case_rot_big` (no general position), `isometry_complex_cases` (two disjuncts each with its own `∀ z`),
   `halfTurn_of_symmetric_counterexample` (`g = halfTurn c` as functions), the six classes and
   `MirrorExclusionLineCopy`. Line numbers in heads and map: all 72 exact (script check: map rows equal heads in
   names, file:line and order; 46 environments = 46 map rows; kinds match).
2. **Library citations.** `Suk.convexPosition_of_strict_supports` (SupportingLines.lean:28) and
   `ConvexPosition.hasConvexNGon` (Basic.lean:31) match. Mathlib names in the written steps were checked in the pinned
   Mathlib sources (rev f897ebcf): `Function.iterate_minimalPeriod`, `Function.iterate_injOn_Iio_minimalPeriod`,
   `Function.minimalPeriod_eq_one_iff_isFixedPt`, `Function.IsPeriodicPt.minimalPeriod_dvd`,
   `IsPrimitiveRoot.eq_pow_of_pow_eq_one` (has `[NeZero k]`, consistent with the `k > 0` of (P5)),
   `IsPrimitiveRoot.eq_neg_one_of_two_right`, `Complex.isPrimitiveRoot_exp` (`n != 0`), `linear_isometry_complex`
   (argument `ℂ ≃ₗᵢ[ℝ] ℂ`), `Isometry.affineIsometryOfStrictConvexSpace` (only the codomain strictly convex; docstring
   "does not require the isometry to be surjective"), `Complex.cpow_nat_inv_pow`,
   `Set.Finite.exists_lt_map_eq_of_forall_mem`.
3. **Every proof step**, including the self-contained proof of `isometry_complex_cases` (inner-product preservation,
   frame `a = H(1)`, `e = H(i) = ±ia`, decomposition `ξ = <ξ,a>a + <ξ,e>e`), the shared induction
   `sr:lem:orbit-core` (both injectivity sub-cases `i = 0` and `i >= 1`), (MP1)–(MP4), (P1)–(P6), `root_cases2`, the
   three rotation sub-cases, the mirror counting (`|F| <= 2`, `|M|` even, `|M| >= 31 -> 32`, `33 -> 34`), and the
   redundancy remark (`3 ∤ 32`, `5 ∤ 34`; `c ∉ S` for `Fourfold32` via the half-turn). No gap found.
4. **Identities, checked with sympy** (script in the referee's scratch directory, all OK): `toC_reflLine` (real and
   imaginary parts of the difference are `x(s-1)`, `y(s-1)`), `reflLine` involution (difference
   `4u_i(s-1)d`), `û² conj(û² ζ̄) = (ûū)² ζ`, the cross-product identity of `sr:lem:refl`(d),
   `orient(p,q,r) = (q-p)×(r-p)`, both equalities of the concyclic identity, `orient(q,c,2c-q) = 0`, Euler form of
   `rotAbout`, `halfTurn = crot(-1)`, `c + a(z-c) = az + b` for `c = b/(1-a)`, `g(g(p)) = p + a b̄ + b` and the
   reflection formula of case (C), `reflLine(a+u) = a + (2s-1)u`, `s(2s-1)² = s` iff `s ∈ {0,1}`, `u = 0` gives the
   half-turn, fixed points `a + tu`, the sup-metric example, and the polarization/decomposition identities of
   Theorem `sr:thm:structure`(a).
5. **Sources and axioms paragraphs.** SHA-256 prefixes of the main file, the Axioms copy and all eight modules of the
   import closure recomputed: all match; closure recomputed from the import lines (8 modules; BaseOrder, BaseChart,
   TriangleOrder only through SupportingLines). `SymmetricReductionAxioms.lean` lines 1–1059, `ReviewSanity.lean`
   lines 1–1059, `VariantChecks.lean` lines 1–1059 and `AffineReduction.lean` lines 1–1058 are byte-identical to the
   main file (diff). RTC lines 38–1084 = main file lines 12–1058 (diff); RTC does not import the main file. Logs:
   `SymmetricReduction.out` empty, exit 0 in `runs.tsv`; axioms of both printed theorems and of
   `Review.mirrorOneAxis33_iff_exclusionLine` (ReviewSanity.lean:1629; converse at :1593) and of
   `VariantChecks.group_form` are the standard three. Textual scan (`-w` and case-insensitive): no `axiom`
   declaration, `sorry`, `decide`, `native_decide`, `admit`, `implemented_by`, `extern`, `unsafe`; "axiom" only in
   comments (main file :16, :50; Definitions.lean:30).
6. **Cross-section references.** All 15 external labels are allowed (fd foundation labels; export labels of cb, mb,
   ar) and say what is claimed: fd:def:inv (maps into), fd:def:rot (formula), fd:lem:collinear (b), fd:lem:cp-hull,
   fd:lem:mono (a)–(c); mb:thm:classes (written proofs of both mirror classes, Lean-checked), mb:thm:main3 (three
   hypotheses remain), ar:thm:main (affine symmetries), cb:thm:c2/cb:thm:c3 (see m3). Uses of sr labels in ar, cb, ec,
   mb are consistent with the sr statements.
7. **Record claims** in Remarks sr:rem:records, sr:rem:main, sr:rem:variant, sr:rem:mirror-line against
   `SYMLEAN/README.md` §5, §6, §8, §9; `WRITEUP/SYMMETRIC.md` §0, §1, §3; `C2ENC/class_table.md` §1–§2;
   `C2FINAL/README.md`; `C3LEAN/README.md` §1, §6; `AUDIT3/reports/A2_threefold.md`; `C4CUT/README.md`;
   `H3/MirrorEncoding/Line.lean` (:18, :94, :139, :147); `V2-L/V2L/FinalTree.lean` (:28);
   `V2-L/README.md` §9.1, §9.6; `WRITEUP/MIRROR.md` §6; `WRITEUP/note/symmetric_es7.tex` (`cor:only`, :95);
   `SYMLEAN/mirror/axioms.out`. Numbers (120, 116,883, 2,120, 204, 910, 1+121+1,198+74,000) and attributions match.
   Every cited path exists. The cake_lpr-only trust statement matches the 6 November revision of SYMMETRIC.md §3.
8. **Compile and hygiene.** Standalone build with the current preamble (two `nice -n 15 pdflatex` runs, private
   wrapper): exit 0, no error, no "Missing $", no overfull box; only the 15 expected foreign references undefined.
   No machine path, no tool name in `sr.tex` or `sr.map.tsv`. No `\newcommand`, `\def`, `\usepackage`,
   `\makeatletter` or `\sloppy` in the section. "proved" occurs only for the written proofs of this section or in
   "none is proved in this section".

## Findings

### m1 (minor). The H3/V2-L route: "the case split [is] Lean-checked" and the hypothesis count

*Location.* `sr.tex` lines 247–249 (Remark sr:rem:records: "On the route through \dirn{H3} and \dirn{V2-L} to
\lean{MirrorOneAxis33} the soundness of the encodings and the case split are Lean-checked; what remains outside Lean
there is described in Remark~\ref{sr:rem:mirror-line}") and lines 1035–1039 (Remark sr:rem:mirror-line: "it is
Lean-checked with $1+121+1{,}198+74{,}000$ hypotheses of the form ...").

*Evidence.* `V2L.mirrorExclusionLine_final` (`RES/V2-L/V2L/FinalTree.lean:28`) has four hypotheses: `h1` (a family
over the 1,198 V1-L leaves), `hroot : RootCertificate` (one CNF), `hup : UpCertificates` (a family over 121 CNFs) and
`hleaves` (a family over 74,000 leaves). Its docstring (lines 26–27) and `V2-L/README.md` §9.6 call `hroot` and `hup`
"the 122 cover-obligation facts"; `WRITEUP/MIRROR.md` §6 defines
`RootCertificate := ¬DimacsSatisfiable (interiorCnf 33 7 ++ upCubes.map negClause)`. So the exhaustiveness of the
top two levels of that case split is itself among the CNF hypotheses (recorded cake_lpr verdicts); only the tree
covers below the cases (`treeOf_check`, kernel evaluation) and the logical reduction are Lean-checked. The sentence at
l. 248–249 reads as if the whole case split were Lean-checked, and l. 1036 counts instances, not Lean hypotheses. No
statement is affected and the route is correctly called conditional, so this is an imprecision, not an overclaim of a
statement's label.

*Fix.* l. 247–249: "... the soundness of the encodings and the reduction of the class to its CNF facts are
Lean-checked (the tree covers below the cases by kernel evaluation); the cover of the top two levels of the split is
itself among those CNF facts; what remains outside Lean ...". l. 1036–1038: "it is Lean-checked with four hypotheses
(\texttt{h1}, \texttt{hroot}, \texttt{hup}, \texttt{hleaves}) which together assert $1{,}198+1+121+74{,}000$ facts of the
form ``this CNF formula is unsatisfiable'' (the $1+121$ are the cover obligations of the case split), each with a
recorded \texttt{cake\_lpr} verdict ...".

### m2 (minor). Threefold33 bullet omits the written exhaustiveness of the splits; H6M pointer

*Location.* `sr.tex` lines 261–268 (Remark sr:rem:records, \lean{Threefold33} bullet).

*Evidence.* `C3LEAN/README.md` §1 ("That the splits are exhaustive, and that the reflection maps of Lemma 5 and Lemma
H6M are the right maps, are written proofs, reviewed, not Lean-checked") and §6 (layer and σ-splits: Lemmas 1–4 and
the cover theorem of `C3-S/soundness.md`, its reduced-cut version `C3H6M/soundness_h6m.md`, rules 2 and 3 of
`C3U2/sigma_split.md`). The bullet names the normal form, Lemma H6M, the encoding and the perturbation lemma, but not
the σ-split rules of `C3U2/sigma_split.md`. Section mb's Remark mb:rem:main3 does list "the exhaustiveness of the
splits" for the same class, so the two sections describe the same class differently. Also, "the written Lemma H6M
(\dirn{C3AUDIT2})" points to the adversarial check; the written lemma is in `C3H6M/soundness_h6m.md` (statement also in
`C3PLAN/PLAN.md`, lines 175–218, which C3AUDIT2 reviewed). The class table uses the same pointer, so this is a record
pointer, not an error.

*Fix.* Add after "the written Lemma H6M": "(\dirn{C3H6M/soundness\_h6m.md}, checked in \dirn{C3AUDIT2}); on the
written exhaustiveness of the layer splits and $\sigma$-splits (\dirn{C3-S/soundness.md}, rules 2 and 3 of
\dirn{C3U2/sigma\_split.md})".

### m3 (minor). cb:thm:c2 and cb:thm:c3 called "Lean-checked bookkeeping" without "computer-assisted"

*Location.* `sr.tex` line 79 ("Theorems~\ref{cb:thm:c2} and~\ref{cb:thm:c3} (Lean-checked bookkeeping of two case
splits)"), line 258 ("the Lean-checked bookkeeping of the subcase orbits"), line 264 ("the Lean-checked cover of the
$910$ roots").

*Evidence.* Section cb labels both statements "(Computer-assisted.)" (cb.tex:1116 for cb:thm:c3, cb.tex:1366 for
cb:thm:c2): both are kernel evaluations over explicit lists (`decide +kernel`; `WRITEUP/SYMMETRIC.md` §3). Contract
rule 6 labels such statements computer-assisted. "Lean-checked" is true, so nothing is rounded up, but the sr text and
the cb heads use different labels for the same theorems.

*Fix.* l. 79: "(Lean-checked by kernel evaluation, computer-assisted bookkeeping of two case splits)"; at l. 258 and
l. 264 add "computer-assisted," before "Lean-checked", or append "(kernel evaluation)".

### m4 (minor). The remark follows sources that disagree on the trusted checkers

*Location.* `sr.tex` lines 242–243 ("it follows ... \S5 and \S9 of \dirn{SYMLEAN/README.md}, \S3 of
\dirn{WRITEUP/SYMMETRIC.md} ...") and lines 249–251 ("The project trusts one proof checker, \texttt{cake\_lpr} ...").

*Evidence.* `SYMLEAN/README.md` §9, line 316: "The SAT solver is not trusted; the checkers lrat-check and cake_lpr
are (`WRITEUP/SYMMETRIC.md` §3)". `WRITEUP/SYMMETRIC.md` §3 (line 231, "Revised 6 November 2026") makes lrat-check a
secondary check only. The section correctly follows the later revision, but a reader who opens README §9 as directed
finds the opposite statement.

*Fix.* After "(\dirn{WRITEUP/SYMMETRIC.md} \S3)" add: "; \dirn{SYMLEAN/README.md} \S9 predates this revision and still
lists both checkers as trusted".

## Points examined and not reported

- The written (P5) adds `k > 0`; the pinned Mathlib lemma carries `[NeZero k]`, so the restatement is faithful to
  what the Lean proof uses. In Lemma sr:lem:odd-prime the letters of (P5) are used with swapped roles ("by (P5)
  ζ = w^e"); the application is correct.
- Theorem sr:thm:structure(a) states the hypothesis as `|G(z)-G(w)| = |z-w|`; the equivalence with Mathlib's
  `Isometry G` is stated in Lemma sr:lem:toC-iso(b). Adequate.
- The C3a encoding is called "computational evidence ... tested, not proved" in `C3LEAN/README.md` §6 (citing
  C3AUDIT), but `AUDIT3/reports/A2_threefold.md` row 2 records a written soundness proof re-derived by the auditor,
  and `WRITEUP/SYMMETRIC.md` §3 lists it among written proofs; the section's grouping under written proofs is
  supported by the later record.
- The mirror classes of `SYMLEAN/mirror` are different constants from those of the main file; the section says the
  file does not import the main file and that the classes are byte-identical copies with the same full names, and
  Remark sr:rem:main says Theorem mb:thm:main3 is "for the byte-identical copies". Adequate.
- `IsEucIsometry.injective` lies outside the dependency cone of every printed theorem; the empty compile log plus the
  scan supports "Lean-checked in this sense", as the section says.
