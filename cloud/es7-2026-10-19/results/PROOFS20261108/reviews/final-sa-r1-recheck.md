# Final pass, round 1: independent re-check of section sa

Verdict: **pass**. All six findings are resolved correctly. The edit adds no blocker or major finding. Two minor
points are listed at the end. Neither needs a change in this pass.

Files compared: `snapshots/final-r1-pre/sa.tex` and `.map.tsv` against `sections/sa.tex` and `.map.tsv`. I used
`diff -u`. The sa.tex diff has six hunks, each belonging to one finding. In the map, the notes of two rows changed
(sa:prop:table and sa:prop:assembled). Nothing else changed. The list of `\label{...}` is identical before and after.
No theorem, proposition or lemma environment changed; the only environment touched is the written-step Remark
sa:rem:use (items (1) and (5)), which findings 2 and 3 asked for.

Sources re-read (paths relative to RES): `AUDIT3/A1_reduction/SizeArith.lean` (whole file),
`AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean` and its log (whole files),
`SYMLEAN/SymmetricReduction.lean` lines 466-498 (the six classes), 763 and 1042 (`case_fourfold` and its only use),
`SYMLEAN/review/VariantChecks.lean` lines 1055-1306, `SYMLEAN/logs/VariantChecks.out`, `LAYERLEAN/LayerLemma.lean`
lines 1037-1099, and `LEANEXT/es7corr/ES7Corollaries.lean` lines 1-40 and 1148-1233. I also diffed lines 1-1147 of
the last two files.

## Findings of the fix round

1. **[minor] hypotheses of the table statements (sa.tex 231-237, map row sa:prop:table): resolved.** Checked
   against SizeArith.lean 61-80. `table_c3` (`hk : k ≤ 10`), `table_c4` (`k ≤ 7`) and `table_c2` (`k ≤ 16`) are
   parts (a), (e) and (h). `table_c4_only_c2` (`2 * k ≤ 16`) and `table_c6` (`2 * k ≤ 10`) are parts (f) and (g).
   `table_c5` (`5 * k + e < 35`) is part (c). `table_mirror` (`b = 0 → k ≤ 16`, `1 ≤ b → k ≤ 15`) is part (i). The
   only hypothesis of `c3_no32` and of `c5_gap` is `he : e ≤ 1`, which is what parts (b) and (d) state.
   - "The bound that the theorem gives" on 5k+e in part (c) is also right. The case theorem T_C5 of the records
     gives n < 35, as the comment of `table_c5` says ("if not excluded (n < 35)"). The Lean class `Fivefold35`
     gives k ≤ 6, hence 5k+e < 35, and item (5) says exactly that.
   - The map note says the same as the text. It renders correctly in a scratch appendix (see the notes at the end).
2. **[minor] item (5) of Remark sa:rem:use drops n ≥ 33 (sa.tex 578-582): resolved.** I checked every clause of
   the added sentence.
   - The counts: k for `Threefold33`, `Fivefold35`, `Fourfold32`, for `HalfTurn34` on half-turn sets and for the
     mirror classes; 2k for ρ^[2] when s = 4 (`HalfTurn34`) and when s = 6 (`Threefold33`). Lemma sa:lem:model(a)
     applied to ρ^[2] gives n = 4k+e = 2k'+e, respectively n = 6k+e = 3k'+e, with the same e, so k' = 2k.
   - The subsets T of items (1) and (2) never use 33 ≤ n, only the count. Each has the exact size of its class, is
     in general position, is invariant and avoids c. In the mirror case it has no fixed point, or exactly one,
     since the pairs avoid L. These are exactly the hypotheses of the classes at SymmetricReduction.lean 466-498:
     `HalfTurn34` with `halfTurn c` = ρ_{c,π}, `Threefold33` with ρ_{c,2π/3} = ρ_{c,2π/6}^[2], and `Fourfold32` with
     `rotAbout c (2π/4)`. HasConvexNGon 7 T then gives 7 points of S in convex position.
   - For even s, k ≥ 1 gives a point of S other than c, so e = 0 by the last clause of Lemma sa:lem:model(a).
     General position of S is still a standing hypothesis; only 33 ≤ n is dropped. And k = 0 gives n = e ≤ 1.
   - This is enough for parts (e)-(h), which bound sk: there n = sk, or n ≤ 1 when k = 0.
   - The deviation from the suggested wording ("$k$, or $2k$ for $\rho^{[2]}$ ...") makes the sentence correct for
     the sixfold row and the HalfTurn34 fourfold row, where the class is applied to 2k orbits or pairs. The
     suggested "if $k$ reached" would have been inexact there.
3. **[minor] uses of Fourfold32 (sa.tex 521-525): resolved.**
   - `group_form` is at VariantChecks.lean:1168 with `(h4 : Fourfold32)` at 1169. It is declared in namespace
     `ErdosSzekeres.SymReduction.VariantChecks` (line 1076), and its axioms are printed at line 15 of
     `VariantChecks.out`. Its proof calls `halfTurn_of_symmetric_counterexample` three times, so "a check of that
     theorem" is accurate.
   - The other uses in that file are `fourfold36_of_fourfold32` (1220, `h4 : Fourfold32`) and `variant_unfolded`
     (1116, with the class unfolded). So "some checks ..., among them its group form" is true and does not claim
     that the list is complete.
   - The short name `VariantChecks.group_form` is the one that sr.tex uses (sr.tex 114-116, 1024, 1164). It sits in
     the same sentence as the file path.
4. **[minor] big_order_orbit (sa.tex 23-24): resolved.** AssembledSizes.lean:24 concludes `1 ≤ k`. The comment at
   line 23 reads "at least one non-central orbit". The new text, "at least one orbit other than the centre",
   matches it.
5. **[minor] "restates six of the statements" (sa.tex 283-285, map row sa:prop:assembled): resolved.**
   - Four declarations restate a whole statement: `halfturn_pairs` restates `c2_reduce` (conjuncts swapped),
     `threefold_orbits` restates `c3_reduce`, and `mirror_b0` and `mirror_b12` restate the two mirror statements.
   - Two restate a part: `fivefold_size` gives only the first conclusion of `c5_reduce`, and
     `fourfold_via_halfturn` only the third conclusion of `c4_reduce`.
   - The map row was changed to match the text. That is within the finding, which is about the same claim.
6. **[minor] the ec proofs use copies of the layer results (sa.tex 44-48): resolved.**
   - ES7Corollaries.lean imports only `ErdosSzekeres.*` and Mathlib modules (lines 1-9). `diff` shows that its
     lines 1-1147 are identical to lines 1-1147 of LayerLemma.lean. Line 1148 differs: the section-11 banner in one
     file, `end ErdosSzekeres.LayerLemma` in the other.
   - `fivefold_heptagon` (1183) goes through `fivefold_heptagon_of_erase` (1170). `fourfold_heptagon` (1216) goes
     through `fourfold_heptagon_of_erase` (1203). Both call the copy of `convexNGon_of_layers` (1066) with t = 7 or
     t = 8.
   - That copy builds `T = S' \ peel S' t` with `T.card = m * t`, that is 35 or 32, through the copy of `card_peel`
     (1037). That copy calls the copy of `layers_are_orbits` (402).
   - The new sentence is grammatical and true. It agrees with ec.tex 79-85 and 911-912. `ll:thm:reduction` is an
     export label of section ll, so the new `\ref` is allowed.

## Referee check of the diff

- Mathematics: every new claim checked as above. No statement environment changed. Propositions sa:prop:table and
  sa:prop:assembled and Lemma sa:lem:big-order still match the Lean statements exactly. I re-read them against
  SizeArith.lean 61-80 and AssembledSizes.lean 6-27.
- Rigor labels: no new label, none raised or lowered. The new text uses no "verified", "certified" or "proved", and
  no hypothesis is presented as proved: the classes remain hypotheses in item (5).
- Hygiene: sa.tex and sa.map.tsv contain no machine path, no tool name, and no
  `\newcommand`/`\def`/`\usepackage`. All 14 map rows have 5 tab-separated fields. `\lean` and `\dirn` are used only
  on names and paths without spaces.
- Compile: `build/sa_final_recheck_r1_wrapper.tex` (same content as the contract wrapper) was run twice from
  `build` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
  - Both runs exit 0, with no `!` errors, no "Missing" and no undefined control sequence. There are no overfull
    boxes.
  - The log has two notices "Underfull \vbox ... while \output is active" (badness 10000 and 2318). They come from
    page breaks in the standalone wrapper. On page 1 the source table moves to page 2. These are not overfull
    boxes.
  - The output has 9 pages. The undefined references are only fd: labels and export labels of other sections
    (ar, ec, lg, ll including ll:thm:reduction, mb, mm, sr).
  - I extracted the text of the changed passages from the PDF: they read correctly.

## Remaining points (minor; no change needed in this pass)

1. **[minor] sa.tex 521-523: Lemma sr:lem:fourfold also takes Fourfold32 (in substance, the wording predates this
   edit).** The sentence reads "Among the reduction theorems stated in this document, only Theorem sr:thm:variant
   uses this class". Lemma sr:lem:fourfold (`ErdosSzekeres.SymReduction.case_fourfold`,
   SYMLEAN/SymmetricReduction.lean:763) is also stated in this document, and it takes `(h4 : Fourfold32)`.
   - Its only use is in the Lean proof of the variant (line 1042). Section sr uses the same convention: sr.tex 298
     says "Fourfold32 (used only by Theorem sr:thm:variant)". So the sentence is defensible if "reduction theorems"
     means the main theorems, not their case lemmas.
   - Optional wording: "only Theorem~\ref{sr:thm:variant}, through its case lemma \lean{case_fourfold}, uses this
     class". sr:lem:fourfold is not an export label, so it cannot be cited with `\ref`.
2. **[minor] appendix_map.tex is older than the edited maps.** It was generated at 21:39. sa.map.tsv changed at
   21:52, and the maps of pc, ec, mb and cb changed in this pass as well. The generated appendix still has the old
   notes of sa:prop:table and sa:prop:assembled.
   - Regenerate it with `python3 tools/make_appendix.py` before the full build. This is outside the section files.
   - I regenerated it on a scratch copy (`build/sa_final_recheck_r1_app`; the real appendix is untouched). The run
     gives 470 rows and no error. Compiled alone twice (`build/sa_final_recheck_r1_appwrap.tex`), it exits 0 with no
     errors and no overfull boxes.
   - The two new sa notes render as plain text with typewriter identifiers and `$b=0$`, `$1\le b$`, `$e\le1$`.

## Note on the fix log

The log says "No statement environment was changed". That is true of theorems, propositions and lemmas. The remark
sa:rem:use did change, as findings 2 and 3 required. This affects only the log, not the document.
