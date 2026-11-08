# Diff audit of section `sr`, round doc-r0

Compared: `snapshots/doc-r0-pre/sr.tex` (1,116 lines) and `snapshots/doc-r0-pre/sr.map.tsv` against `sections/sr.tex`
(1,131 lines) and `sections/sr.map.tsv` (46 rows plus header in both), with `diff -u`. The `.tex` has 6 hunks and the
map has 1 hunk (one row). Fixer log: `reviews/sr-doc-r0-fix.md`. The notes it addressed: `reviews/sr-p1-diff.md` m1, m2
and `reviews/sr-p1-referee.md` m1-m4. Paths below are relative to the staging area, to `RES`, or to the repository
root. "Mathlib" means the pinned checkout at rev `f897ebcf72cd` (the rev in `lake-manifest.json`). Line numbers are
those of the current `sections/sr.tex`.

**Verdict: PASS.** No blocker and no major finding. One minor finding (m1, wording). The fixer marked all six notes
fixed and declined none. All six are fixed, and the one extra change is correct. No statement, label, `\leanref`,
`\ref` or environment changed: the label list, the `\leanref` list, the set of `\ref` targets and the environment
count (46) hash to the same values in the snapshot and in the current file. My wrapper compiles with exit 0 and has no
overfull box.

## 1. The `.tex` hunks

1. **Dependencies (l. 79-80).** The text now reads "bookkeeping of two case splits, Lean-checked by kernel evaluation
   and so computer-assisted" for `cb:thm:c2` and `cb:thm:c3`.
   - `C2FINAL/Central34Orbits.lean:291`: `all_cases_closed ... := by decide +kernel`.
   - `C3LEAN/C3Cover.lean:2251`: `all_roots_covered`. Its proof combines `checkRoot_sound` with facts proved by
     `decide +kernel` (151 occurrences in the file; its header says "by kernel evaluation (`decide +kernel`, no
     `native_decide`)"; `C3LEAN/README.md` Status gives the same).
   - Section `cb` heads: `cb.tex:1119-1120` "(Computer-assisted: ...)" and `cb.tex:1370-1371` "(Computer-assisted.)".
   - The label matches contract rule 6. Nothing is rounded up. Correct.
2. **Remark `sr:rem:records`, H3/V2-L route (l. 249-252).** New claims: (a) the soundness of the encodings and the
   reduction of `Mir.MirrorExclusionLine` to CNF facts are Lean-checked; (b) the cube covers in that reduction are
   checked by kernel evaluation; (c) the exception is the cover of the top two levels of the case split, which is
   itself given by 1+121 of the CNF facts.
   - `V2-L/V2L/FinalTree.lean:28-34`: `mirrorExclusionLine_final` takes exactly `h1`, `hroot : RootCertificate`,
     `hup : UpCertificates` and `hleaves`. It applies `mirrorExclusionLine_of_certificatesT` to `treeOf_check`.
   - The covers below the top two levels are proved by kernel evaluation:
     - sub-case (i): `V1-L/V1L/Cover.lean:17`, `hullLeaves_coverCheck : coverCheck hullLeaves = true := by decide +kernel`;
     - sub-case (ii): `treeOf_check`, one `decide +kernel` per sibling list, and the 310 leaf cases in `CheckLeaf`
       (`V2-L/README.md` §9.5).
   - `V2-L/README.md` §9.2 and `WRITEUP/MIRROR.md` §6: no `native_decide` in V2-L, H, H3 or V1-L.
   - `V2-L/V2L/Main.lean:27-32`: `RootCertificate := ¬DimacsSatisfiable (interiorCnf 33 7 ++ upCubes.map negClause)`,
     and `UpCertificates` ranges over `upTable` (`Facts.lean:19, 47, 49`: 121 entries).
   - `WRITEUP/MIRROR.md` §4 ("the 122 obligations"): root covers the upper chains U, and up:U covers the cases (U, L).
     These are the top two levels.
   - Correct, not rounded up. MIRROR.md §1 says loosely that "the case split" was kernel-checked. The new text is more
     precise than that record and agrees with §4 and §6. Wording: see m1.
3. **Remark `sr:rem:records`, trust sentence (l. 252-256).**
   - `WRITEUP/SYMMETRIC.md:231`: "*Revised 6 November 2026:* lrat-check ... is a secondary check only and not part of
     the trust base". This is inside §3 (l. 202-264).
   - `SYMLEAN/README.md:316` (§9): "the checkers lrat-check and cake_lpr are (`WRITEUP/SYMMETRIC.md` §3)".
   - `git log`: the README was last changed in f353ac364 (2026-11-02). The lrat-check sentence of SYMMETRIC.md entered
     in ad1edc4ca (2026-11-06 +0900). So "predates that revision and still lists both checkers as trusted" is true.
   - The remark's opening sentence does cite "§5 and §9 of SYMLEAN/README.md", so "which this remark follows on other
     points" is consistent. Correct.
4. **HalfTurn34 bullet (l. 263-265).** The only change is "bookkeeping of the subcase orbits, Lean-checked by kernel
   evaluation and so computer-assisted". It is correct by item 1.
5. **Threefold33 bullet (l. 269-276).**
   - "Cover of the 910 roots, Lean-checked by kernel evaluation and so computer-assisted": item 1.
   - "The written Lemma H6M (C3H6M/soundness_h6m.md, checked adversarially in C3AUDIT2)":
     - `C3AUDIT2/REPORT.md` title: "adversarial check of Lemma H6M".
     - `C3H6M/soundness_h6m.md:1-26` is the written lemma. Its φ_{a,s} is the same as in `C3PLAN/PLAN.md:177-182`,
       the text C3AUDIT2 checked.
     - `C3LEAN/README.md` §6 lists "C3AUDIT2 and C3H6M (Lemma H6M)" as the reviews.
   - "Written exhaustiveness of the layer splits and σ-splits (Lemmas 1--4 and the cover theorem of
     C3-S/soundness.md, its version for the reduced cut in C3H6M/soundness_h6m.md, and rules 2 and 3 of
     C3U2/sigma_split.md)":
     - `C3LEAN/README.md` §6 has the same list, nearly word for word.
     - The parts exist: `C3-S/soundness.md` has Lemmas 1-4 (l. 12, 19, 39, 54) and "Theorem (cover)" (l. 81).
       `soundness_h6m.md:80` has "Theorem (cover, with the reduced cut)". `C3U2/sigma_split.md` has Rule 2 (l. 31)
       and Rule 3 (l. 59).
   - The bullet is now consistent with Remark `mb:rem:main3` (`mb.tex:1099-1104`). Correct.
6. **Mirror bullet (l. 285-288).** Both files are now named in full.
   - I re-ran the check: `diff` of RTC l. 38-1084 against `SymmetricReduction.lean` l. 12-1058 is empty.
   - The RTC imports (l. 1-13) do not include the main file.
   - `namespace ErdosSzekeres.SymReduction` is at RTC l. 80, inside the copied range, so the classes at RTC l. 493-522
     have the same full names.
   - Correct.
7. **Proof of Theorem `sr:thm:structure`(a) (l. 565-569).**
   - Mathlib `Mathlib/Analysis/Convex/StrictConvexBetween.lean:138` is a `noncomputable def affineIsometryOfStrictConvexSpace (hi : Isometry f) : PF →ᵃⁱ[ℝ] PE`.
   - Strict convexity is required only of `E`, the space of the codomain `PE` (variables, l. 106-108).
   - Its docstring: "Unlike Mazur-Ulam, this does not require the isometry to be surjective".
   - `coe_affineIsometryOfStrictConvexSpace` (l. 149-150) is `rfl`, so the underlying map is the given isometry.
   - `linear_isometry_complex` (`Mathlib/Analysis/Complex/Isometry.lean:130`) is a theorem about `ℂ ≃ₗᵢ[ℝ] ℂ`.
   - The Lean proof (`SYMLEAN/SymmetricReduction.lean:323-335`) does exactly this, with
     `toLinearIsometryEquiv` in between.
   - The statement of the theorem did not change. I re-read it against `:321-322` and `:869-872` and it still matches:
     two disjuncts, each with its own `∀ z`; `1 < S.card`; `g ≠ id`; `Invariant`; `∃ m, 0 < m ∧ a ^ m = 1`;
     `u 0 ^ 2 + u 1 ^ 2 = 1`.
   - Correct.
8. **Remark `sr:rem:mirror-line` (l. 1044-1052).**
   - The `coverCheck` parenthetical: `H3/MirrorEncoding/Line.lean:147-150` takes `hc1 : coverCheck C1 = true` and
     `hc2 : coverCheck C2 = true`. `coverCheck : List (List Int) → Bool` (`H3/MirrorEncoding/CoverCore.lean:28`).
   - The four hypotheses are named and counted correctly: h1 = 1,198 (`V1-L/V1L/Cover.lean:19`); hroot = 1;
     hup = 121; hleaves = 74,000 = 172 + 138 + 73,690 (`V2-L/README.md` §9.6; `WRITEUP/MIRROR.md` §6).
   - The FinalTree docstring (l. 16, 26-27) calls hroot and hup "the 122 cover-obligation facts".
   - The rest is reworded from the passed version: recorded cake_lpr verdicts, proofs not retained
     (`WRITEUP/CERTIFICATES.md`, "Not in the archive"), file-to-term step outside Lean (`MIRROR.md` §6, trust items
     2-4).
   - Correct. Wording: see m1.
9. **Coverage (l. 1120-1124).** The text now says "the construction `Isometry.affineIsometryOfStrictConvexSpace` and
   the theorem `linear_isometry_complex`". This is correct by item 7.

## 2. The map hunk

Only the note of `sr:thm:structure` changed: "written proof of part (a) by an elementary argument instead of the
Mathlib results used in Lean (a construction and a theorem)". It is accurate. All 47 lines have 5 columns. Labels,
kinds, Lean names and file:line columns are unchanged.

## 3. The fixer's log

| note | fixer | audit |
|---|---|---|
| diff m1 (`def` called a theorem) | fixed | confirmed (items 7, 9, map) |
| diff m2 ("that file") | fixed | confirmed (item 6) |
| referee m1 (H3/V2-L case split; count of hypotheses) | fixed | confirmed (items 2, 8); wording nit m1 |
| referee m2 (Threefold33: exhaustiveness of splits; H6M pointer) | fixed | confirmed (item 5) |
| referee m3 (cb theorems not labelled computer-assisted) | fixed | confirmed (items 1, 4, 5) |
| referee m4 (README §9 vs SYMMETRIC.md §3) | fixed | confirmed (item 3) |
| other change 1 (`coverCheck` hypotheses of `_of_cubes`) | made | confirmed (item 8) |
| other change 2 (re-wrapping) | made | confirmed: no text change |

No note was declined.

## 4. Compile check

- Wrapper `build/sr_docr0audit_wrapper.tex`, with the contract's content. Two runs of
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from `build/`: exit 0 both times, 15 pages.
- No `!` error, no "Missing $", no multiply defined label, no warning other than undefined references.
- **Overfull boxes: none.**
- Undefined references, all allowed: `fd:def:{point,orient,gp,cp,ngon,inv,rot}`, `fd:lem:{collinear,cp-hull,mono}`,
  `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes`, `mb:thm:main3`.
- 64 underfull lines, none in the changed line ranges.
- `pdftotext`: the new `\dirn` paths with underscores (`C3H6M/soundness_h6m.md`, `C3U2/sigma_split.md`) render
  correctly.
- Hygiene (grep):
  - no machine path and no tool name in `sr.tex` or `sr.map.tsv`;
  - no `\newcommand`, `\def`, `\usepackage`, `\makeatletter` or `\sloppy`;
  - no "verified" or "certified";
  - the added lines contain no "proved".

## 5. Findings

**m1 (minor).** Remark `sr:rem:records` l. 251 ("the cover of the top two levels of the case split") and Remark
`sr:rem:mirror-line` l. 1049-1050 ("the cover obligations of the top two levels of the case split").
- The problem: "the case split" has no antecedent in the section. The H3/V2-L route has two cube splits:
  - the 1,198-leaf binary partition of sub-case (i), whose cover is kernel-checked;
  - the hull-pair split of sub-case (ii) (`WRITEUP/MIRROR.md` §4, "The case split of sub-case (ii)").
- Only the second is meant. The numbers 1+121 and the record pointers disambiguate, and the claims are correct.
- Suggested wording: "the top two levels of the hull-pair case split of sub-case (ii) (\dirn{WRITEUP/MIRROR.md} \S4)"
  at its first use, l. 251.

## 6. Checked and not reported

- "Four hypotheses ... which together assert ... facts": "CNF facts" is the records' term (`MIRROR.md`,
  `SYMMETRIC.md` §3). The same sentence calls them hypotheses, and the remark ends "only conditionally on those CNF
  facts". No hypothesis is presented as proved.
- C3AUDIT2 (REPORT.md first committed 2026-10-21 04:46 UTC) predates `C3H6M/soundness_h6m.md` (05:35 UTC the same day).
  It checked Lemma H6M as stated in `C3PLAN/PLAN.md` §3a, which has the same statement, and the addendum's proof follows
  that check. "Checked adversarially in C3AUDIT2" therefore describes the lemma correctly.
- The Threefold33 bullet does not name Lemma 5 of `C3-S/soundness.md` or "Containment" of `C3U2/sigma_split.md`
  separately. The bullet does not claim to be a complete list, and both are covered by "the written normal form
  C3-S/soundness.md" and the cited records. This omission predates this round.
