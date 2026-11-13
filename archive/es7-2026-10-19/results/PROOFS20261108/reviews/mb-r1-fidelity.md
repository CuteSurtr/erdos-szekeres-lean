# Review mb, round 1, lens: fidelity

Section: `sections/mb.tex` (1113 lines) with `sections/mb.map.tsv` (42 rows).
Paths below are relative to the results directory `RES` (e.g. `MIRRORETV/...`, `SYMLEAN/...`) or to the repository
root (`ErdosSzekeres/...`), as in the contract.

## Verdict: PASS (no blocker, no major; 8 minor findings)

Every statement and definition that cites a Lean declaration matches it: hypotheses, conclusions, quantifier order,
Finset vs set, maps-into vs equality, strict vs weak inequalities. All 78 distinct `\leanref` (name, file:line) pairs
resolve to the named declaration at exactly the cited line. All 7 export labels are defined on the right statements.
Every headline declaration in the scope is covered. All of this was checked against the Lean source; I did not rely on
the inventory alone.

## What was checked, and how

1. **Every `\leanref` pair.** A short script (`build/mb-fid-r1/check_refs.py`) opened each cited file and looked for a
   declaration of the named identifier within 3 lines of the cited line. 78 of 78 are OK, and every one is at the
   exact line (offset 0).
2. **Map vs tex.** Script `build/mb-fid-r1/mapcmp.py`:
   - the header is correct;
   - there are 42 statement environments and 42 map rows, with no missing or extra rows;
   - the kinds agree, and the Lean names and file:line lists agree row by row.
3. **Statement-by-statement comparison with the Lean source.** Every item below was read in Lean and compared.
   - **Vendored definitions.** `Config`, `Cap3` (Defs.lean:30), `Cap`, `Cup`, `Gon`, `NGon`, `HasNCap`, `HasNCup`,
     `HasNGon` (ErdosSzekeres/Vendor/ETV/Config/Defs.lean:20–66), plus `List.Chain3'` and `List.In` (Lib/List/Defs.lean:46, 22).
     - The consecutive-triple semantics of `Chain3'`/`Chain3` match Definition mb:def:config(a).
     - "Gon" requires two lists of length ≥ 2, a cap and a cup, with the same `head?` and the same `getLast?`.
     - "NGon" requires lengths summing to n+2.
   - **Lemma mb:lem:config-mono.** `hasNCap_supset`, `hasNGon_supset` and `ncup_is_ngon` (2 ≤ n) at Config/Lemmas.lean:293, 305, 275, all in the root namespace.
   - **Theorem mb:thm:baek.** `main (n) (C : Config γ) (S : Finset γ) (hS : choose (n+2) 2 + 2 ≤ S.card) : C.HasNCap 4 S ∨ C.HasNGon (n+3) S` (Main/Main.lean:87). The section's statement is exact.
   - **Theorem mb:thm:capcup.** `Config.cap_cup (a b) (S) (hS : choose (a+b) a < S.card) : HasNCap (a+2) S ∨ HasNCup (b+2) S` (CapCup.lean:46). Exact; strict inequality.
   - **Lemma mb:lem:baek8.** `four_cap_or_eight_gon` (23 ≤ card) and `capacity22` (Omission/Baek.lean:12, 16).
   - **Bridges.**
     - `Configuration` and `HasCap` (all-triples): Realization.lean:9, 64.
     - `cup`: Realization.lean:33; it is true iff all three indices are < n and orient > 0.
     - `colorConfig c.cup true` (ActualRanks.lean:28) and `pointAt`, with value 0 off range (ListGeometry.lean:13).
     - `cup_true_iff`, `cup_false_iff` (which needs i<j<k), `cup_sign`, `cap_sign` (which needs a<b<d).
     - `four_point_identity_left/right`, `positive_four`, `negative_four`, `chain3_all`, whose ambient set is `S : Set α` with the transitivity hypothesis on S, a pairwise-sorted list and `Chain3'`.
     - `cup_list_all`, `cap_list_all`, `hasCap_of_list`.
     - `Boundary`/`CupArc` (BoundaryGeometry.lean:120, 56), `reflect` (69), `Boundary.card` (k+l+2), `boundary_convex_position`, and `boundary_polygon` (`b.points ⊆ ↑S`).
     - `boundaryOfGon` and `boundaryOfGon_inside` (BaekGeometry.lean:62, 77). The orientation `Boundary l k`, with the lower arc = the cup `ys` and the upper arc = the reflected cap `xs`, matches the section's s = |l′|−2 (Lean `l`) and t = |l|−2 (Lean `k`).
     - Remark mb:rem:boundary's change of variables is correct.
   - **Proposition mb:prop:gon.** `hasNGon_heptagon` (MirrorMain.lean:1512), `hasNGon_octagon` (BaekGeometry.lean:94) and `hasNGon_nonagon` (MirrorNine_append.lean:99). After normalising the number, a diff of the three proofs is empty, confirming "identical up to m".
   - **Capacity results.**
     - `capacity16`: `¬c.HasCap 4` and `¬HasConvexNGon 7 (univ.image c.point)` give n ≤ 16.
     - `geometric_capacity22`: S ⊆ range n.
     - `capacity22g`.
     - `config_capacity113`: on any `Config`, ¬HasNCap 5 and ¬HasNGon 9 give card ≤ 113.
     - `capacity113`.
     - The section's proof of (a) follows the Lean proof step by step. The Lean proof uses `main 6` with C(8,2)=28, `cap_cup 3 6` with C(9,3)=84, and splits by T = first entries of 4-caps in S. It then joins with `Cup3 p q r` via `ncup_is_ngon`, or with a 5-cap.
   - **Reduction lemmas.**
     - `mir`, `Rset` (0 < p 1), `Aset` (p 1 = 0).
     - `card_split`, which needs symmetry only.
     - `card_A_le`, which needs general position (GP) only.
     - `injOn_x`, with hypotheses gp, sym, T ⊆ S, y ≥ 0 on T, and at most one axis point.
     - `cfg` together with `sortPt_image`.
   - **Polygon lemmas and mirror_seven_of.**
     - The four generated lemmas (MirrorMain.lean:212, 392, 639, 816) were compared hypothesis by hypothesis with Lemma mb:lem:polygons(a)–(d): the x-order chain, the y-signs, the four orientations and the seven or eight membership facts.
     - The `Hcap`, `HL` and `HR` binders of `mirror_seven_of` (1676–1691) have the same statements, with ∀P after the point hypotheses. This order is logically equivalent to the section's "universally quantified over the points and over all finite P".
     - The case split in the written proof of Lemma mb:lem:seven-of matches lines 1721–1756 exactly.
     - The counting step matches lines 1763–1795: |R| ≤ 15 when A ≠ ∅.
   - **Arbitrary lines.**
     - `lineRefl`, `frame`, `unframeLin` and `unframe`: the formulas agree coordinate by coordinate with Definition mb:def:frame.
     - `frame_lineRefl`, `orient_frame`, `unframe_frame`, `frame_unframe`, `frame_injective` and `unframe_injective` all carry the hypothesis n0²+n1²=1.
     - `hasConvexNGon_affineMap` (`Point →ᵃ[ℝ] Point`, injective; image Finset).
     - `transport`, a fourfold conjunction.
   - **Main theorems.** `mirror_seven`, `mirror_seven_line`, `mirror_eight`, `mirror_eight_line`, `mirror_nine` and `mirror_nine_line`. The `_line` versions have the hypotheses {n0 n1 c}, hn and `∀ p ∈ S, lineRefl n0 n1 c p ∈ S`.
   - **Part C of RTC.**
     - `reflLine` (RTC:449).
     - `reflLine_eq_lineRefl`, with (−u1, u0, −u1·a0+u0·a1).
     - `card_le_32_of_reflLine`: `Invariant (reflLine a u) S`, with no condition on axis points.
     - `MirrorOneAxis33` and `MirrorNoAxis34` (RTC:508, 514), which match Theorem mb:thm:classes(a), (b) and Definition sr:def:classes of the sr section.
     - `mirrorOneAxis33_proved` and `mirrorNoAxis34_proved`: the axis binder `_` is unused.
     - `heptagon_of_nontrivial_isometry_3`: binders h2, h3, h5, S, g : Point → Point, GP, 33 ≤ card, `IsEucIsometry g`, g ≠ id, `Invariant g S`.
     - `heptagon_of_nontrivial_affineEquiv_3`: g : Point ≃ᵃ[ℝ] Point, `g ≠ AffineEquiv.refl ℝ Point`.
     - The conditional status is stated in the theorem, in the map and in Remark mb:rem:main3.
   - **Statements of other sections' theorems paraphrased inside proofs.** All agree with Lean:
     - `cap_mirror_polygon` (2233, m ≥ 2);
     - `axis_left_polygon` and `axis_right_polygon` (2309, 2403, m ≥ 3; `hPm` for every i, including the axis point);
     - `mirror_odd_general` (2498);
     - `mirror_odd_general_line` (2641);
     - `mirror_seven'` (2631), `mirror_eight'` (2636).
4. **Copy and line-offset claims.** All checked with `diff`:
   - RTC 1562–4236 is identical to MirrorMain.lean 3–2677;
   - RTC 38–1559 is identical to AffineReduction.lean 12–1533;
   - RTC 38–1084 is identical to SymmetricReduction.lean 12–1058, so the offset is +26;
   - SymmetricReduction.lean:997 is `heptagon_of_nontrivial_isometry`, AffineReduction.lean:1501 is `heptagon_of_nontrivial_affineEquiv`, and SymmetricReduction.lean:423 is `reflLine`;
   - RTC 1050, 1078, 1503, 1515, 1536 and 1547 carry the names given in Remarks mb:rem:main3 and mb:rem:axis;
   - MirrorExclusionLineCopy agrees textually with `Mir.MirrorExclusionLine` (H3/MirrorEncoding/Line.lean:94), including `reflLine` (Line.lean:18).
5. **Hashes and logs.**
   - All 18 SHA-256 prefixes in the Sources paragraph and the axioms paragraph match.
   - MirrorMain.out lines 848–863 hold the 16 axiom lines, all standard, and there is no "error".
   - MirrorNine.out lines 879–882 hold the 4 axiom lines.
   - The line shift of 2677 is confirmed by the warnings at 2740 and 2746, which correspond to append lines 63 and 69.
   - axioms.out contents are as described (but see F5).
   - Lean 4.24.0 / Mathlib f897ebcf match `lean-toolchain` and `lake-manifest.json`.
   - In MirrorMain.lean, MirrorNine_append.lean and RTC, `decide` is used only on Fin-index comparisons and on C(6,2), C(8,2) and C(9,3).
   - There is no `native_decide`, `sorry`, `axiom` or `ofReduceBool` in the three files, in the cited vendored and bridge files, or anywhere under `ErdosSzekeres/Vendor/ETV`.
6. **Polynomial identities stated in the text.** Checked with sympy (`build/mb-fid-r1/sym_check.py`); all hold:
   - the four-point identities;
   - the chord identity;
   - the interior-point formula;
   - the four ν-identities of the frame (the stated right-hand sides exactly);
   - the two reflLine/lineRefl coordinate differences 2w_i(u0²+u1²−1).
7. **Compilation and references.**
   - A standalone compile (wrapper in `build/mb-fid-r1/`) passes twice with exit 0.
   - The only undefined references are permitted `fd:`, `mm:`, `sr:` and `ar:` labels. Each of them exists in its own section on the statement mb claims for it: mm:thm:line(a) is `transport`, mm:thm:odd is `mirror_odd_general`, sr:thm:main is `heptagon_of_nontrivial_isometry`, ar:thm:main(a) is `heptagon_of_nontrivial_affineEquiv`, and sr:def:classes(4), (5) match mb:thm:classes.
   - Neither the section nor the map contains a machine path or a tool name.
8. **Baek citation.** Remark mb:rem:baek's paraphrase of Theorem 1.6 ("for every N ≥ 3 … binom(N−1,2)+2 … x-distinct … 4-cap or N points in convex position") agrees with the verbatim quotation in MIRRORETV/PROOFS.md:365–367 ("For any n ≥ 3 …"). The index shift N = n+3 and the thresholds 17, 23 and 30 (bounds 16, 22, 29) are correct. The note WRITEUP/note/symmetric_es7.tex:156–159 states n ≥ 4; that is weaker and does not contradict the quotation.

## Export labels (contract)

| label | required declaration(s) | status |
|---|---|---|
| mb:thm:baek | the cited vendored statement(s) as used | defined on `main` (Main.lean:87); `Config.cap_cup` separately as mb:thm:capcup; OK |
| mb:thm:seven | mirror_seven, mirror_seven_line | (a), (b); OK |
| mb:thm:eight | mirror_eight, mirror_eight_line | (a), (b); OK |
| mb:thm:nine | mirror_nine, mirror_nine_line (with config_capacity113) | (a) config_capacity113, (b), (c); OK |
| mb:thm:refl32 | card_le_32_of_reflLine (with reflLine_eq_lineRefl) | (a), (b); OK |
| mb:thm:classes | mirrorOneAxis33_proved, mirrorNoAxis34_proved | (a), (b); OK |
| mb:thm:main3 | heptagon_of_nontrivial_isometry_3, heptagon_of_nontrivial_affineEquiv_3 | (a), (b), marked conditional; OK |

## Coverage of the scope

Every declaration named in the scope is stated with its Lean name:
- **Baek and bridges:** `main`, the bridge lemmas, `hasNGon_heptagon`, `capacity16`;
- **k = 7 and 8:** `mirror_seven_of`, `mirror_seven`, `mirror_seven_line`, `capacity22g`, `mirror_eight`, `mirror_eight_line`;
- **k = 9:** `hasNGon_nonagon`, `capacity113`, `config_capacity113`, `mirror_nine`, `mirror_nine_line`;
- **Part C:** the six theorems.

Every headline result in the two inventories that belongs to this scope is covered. The others are assigned in Coverage to mm, sr or ar, or listed as duplicates (`mirror_seven'`, `mirror_eight'`, the Part A copies including `case_mirror`).

## Findings (all minor)

**F1 (minor). Remark mb:rem:capcup, tex lines 204–206: off-by-one in the description of the classical split.**

- *Issue.* The remark says the classical proof splits S "into the first entries of (a+2)-caps and the rest". For the
  statement it comments on (conclusion HasNCap(a+2) ∨ HasNCup(b+2)), the split is by first entries of caps one shorter
  than the target, i.e. (a+1)-caps.
- *Evidence.* In the vendored proof, ErdosSzekeres/Vendor/ETV/Main/CapCup.lean:55–69: after `intro a b … intro hab1 ha1b S hS` the goal is
  `HasNCap (a+1+2) S ∨ HasNCup (b+1+2) S`, while `is_start_of_cap` uses `c.length = a + 2`. So "(a+2)" is correct only
  for the shifted induction variable. As written it is ambiguous or off by one.
- *Suggested fix.* Write "the first entries of caps one shorter than the target cap" (in the Lean step to (a+1,b+1):
  the (a+2)-caps).

**F2 (minor). Sources paragraph, tex lines 39–48: `Realization.lean` is listed as adapted from M. Schroeder's archive.**

- *Issue.* `ErdosSzekeres/Omission/Realization.lean` appears among "the bridge files (adapted from M. Schroeder's archive, MIT licence)".
- *Evidence.*
  - The file has no adaptation header. The other six bridge files do: PlanarChains, ListGeometry, BoundaryGeometry,
    BaekGeometry, Baek and ActualRanks.
  - docs/THIRD_PARTY.md:111–118 describes it as project code: "`Realization.lean` connects attained paths to this
    project's all-triples cups, caps … These connections … were added here, using the archive's balanced-state/cycle
    strategy."
- *Suggested fix.* List Realization.lean separately, as project code.

**F3 (minor). Remark mb:rem:baek(3), tex lines 191–193: the cited proposition is narrower than the claim.**

- *Issue.* The remark says "every N-gon of C_c yields N points in convex position (Proposition mb:prop:gon)". Proposition
  mb:prop:gon is stated only for m ∈ {7, 8, 9}.
- *Evidence.* The general claim is true by the same proof, because Lemma mb:lem:boundary has no restriction on s and t.
  Still, the cited statement does not say it.
- *Suggested fix.* Write "(Proposition mb:prop:gon for N = 7, 8, 9; its proof works for every N)".

**F4 (minor). Axioms paragraph, tex lines 71–73 and 92–93: `cup_false_iff` is not covered by the cited axioms logs.**

- *Issue.* The paragraph says the axioms lines "also cover … the bridge lemmas" and that "Every Lean declaration stated
  below is Lean-checked (axioms evidence above)". `ErdosSzekeres.Omission.Configuration.cup_false_iff`, cited in Lemma
  mb:lem:signs, is not in the dependency cone of any printed theorem.
- *Evidence.*
  - Its only uses are ErdosSzekeres/Omission/Realization.lean:114 (an `EndingPath` lemma) and ListGeometry.lean:156
    (`listCap_of_hasCap`). Neither is used by capacity16, geometric_capacity22 or capacity113.
  - It is compiled as part of the imported library, and the file has no sorry or axiom, so it is kernel-checked. But the
    cited `#print axioms` logs do not cover it.
- *Suggested fix.* Either drop `cup_false_iff` from the leanref (`cap_sign` already gives the stated equivalence), or add
  "(compiled with the library; not in the printed cones)".

**F5 (minor). Axioms paragraph, tex lines 67–69: imprecise description of the `#check` output in axioms.out.**

- *Issue.* The paragraph says "its two `#check` outputs are truncated".
- *Evidence.*
  - SYMLEAN/mirror/axioms.out contains three truncated `#check` fragments: lines 17–18 (isometry_3), 19–20
    (affineEquiv_3) and 39–40 (isometry_3 again).
  - RTC issues five `#check` commands (RTC:4312–4316). Those for reflLine_eq_lineRefl, mirrorOneAxis33_proved and
    mirrorNoAxis34_proved have no output in the excerpt.
- *Suggested fix.* Write "it shows truncated `#check` output only for the two `_3` theorems (one of them twice); the
  other three `#check` commands of RTC have no output in it".

**F6 (minor; uncertain). Remark mb:rem:baek(1), tex lines 181–183: the "Theorem 2.7" attribution is not fully supported by the README.**

- *Issue.* The remark says "according to MIRRORETV/README.md, §8, this is Theorem 2.7 in the arXiv numbering".
- *Evidence.* README §8, under Corrections, only says "Baek's Theorem 2.7 holds for all colourings with weak gons; only
  the strong-gon version fails". It states neither the numbering scheme for 2.7 nor that Theorem 2.7 has exactly the
  threshold C(n+2,2)+2 and the (n+3)-gon of `main`. I could not check the paper (no network access); the hedge
  "according to" mitigates this.
- *Suggested fix.* Write "README §8 refers to the weak-gon colouring form as Baek's Theorem 2.7 (its reviews read arXiv
  v2)". Or drop "in the arXiv numbering" unless it is checked against the paper.

**F7 (minor; borderline claims lens). Remark mb:rem:main3, tex lines 1042–1049: one supporting record is not named.**

- *Issue.* The remark names C2FINAL/C2C34, C3FINAL/C3LEAN, SYM5 and the encoder-soundness proofs. This matches
  SYMLEAN/mirror/README.md §4.
- *Evidence.* Threefold33 and Fivefold35 also rest on the written centre-perturbation lemma (C2ENC/perturbation.md).
  The sr section's Remark sr:rem:records and the SYMLEAN-mirror inventory list it.
- *Suggested fix.* Add "and the centre-perturbation lemma C2ENC/perturbation.md", for consistency with sr.

**F8 (minor). Coverage paragraph, tex lines 1111–1113: the list of skipped bridge-file declarations reads as exhaustive.**

- *Issue.* The paragraph lists "declarations of the bridge files not on these paths (hasCup_of_list, hasNCup_octagon,
  listCup_of_hasCup, listCap_of_hasCap, PlanarChains.cup_all)", which reads as a complete list.
- *Evidence.* Many other off-path declarations of the listed files are not named:
  - Realization.lean: ofGeneralPosition, HasCup, endingPath_embedding/hasCup/hasCap, avoids_of_noCup/noCap,
    balancedOwner, balanced_universe_bound;
  - ActualRanks.lean: EndingPath, list_witness, rank_*, false_cup_iff_cap, avoids_of_*;
  - small BoundaryGeometry helpers: affine, affine_mix, affine_positive_convex, supporting_edges_expose, first, last,
    point_x_bounds, first_x_strict, last_x_strict, reflect, reflect_reflect, orient_reflect, reflect_mem_flip,
    Boundary.points, Boundary.finite_coe.

  None of them is a headline declaration of this scope.
- *Suggested fix.* Add "for example", or "and the remaining declarations of Realization.lean and ActualRanks.lean, which
  serve the omission experiments".

## Items checked with no finding

- **Definitions with a mathematical role.** Definitions mb:def:config, mb:def:color, mb:def:mir, mb:def:frame and
  mb:def:reflline, as well as the restatements of `Configuration` and `HasCap`, are exact.
- **Statements with a Lean name.** All statements with a Lean name are exact:
  - Lemmas mb:lem:config-mono, baek8, signs, four, chain, lists, boundary, gc22, split, sort, polygons, seven-of,
    frame, affine and transport;
  - Propositions mb:prop:gon, cap16, cap22 and cap113;
  - Theorems mb:thm:baek, capcup, seven, eight, nine, refl32, classes and main3.
- **Written step.** Lemma mb:lem:interior is correctly tagged as a written step: it is the local `have interior`, not a
  declaration.
- **Conditional status.** Theorem mb:thm:main3 is stated as conditional, with the three classes as hypotheses. The map
  note says "takes hypotheses". Remark mb:rem:main3 names the records and their rigour.
- **Docstring overclaims.** None is copied: "Corollary 3 exactly as …" and "Lean-verified there from CNF facts" do not
  appear.
