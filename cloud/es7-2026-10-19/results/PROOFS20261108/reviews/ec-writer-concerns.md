# Writer report for section `ec` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Layout and preamble: amsthm typesets a statement head in a box, so the url-style \lean/\dirn strings inside \leanref cannot break there. Heads overflowed, by up to about 1100pt when the body began with a list. I fixed that case by putting a sentence before each list. I also wrapped the section body in a local group (a \begingroup\sloppy line right after \section/\label, and \endgroup at the end of the file); this sets a layout parameter and defines no macro. Five overfull boxes remain, all in heads and all under 31pt (inside the margin). Suggested global fix: make \leanref breakable in theorem heads, for example with explicit penalties after . / _ or \sloppy for theorem notes. The other sections will have the same problem.
- The ES8SYM Lean files do not match the recorded hashes. Present SHA-256 are 92f15b5cc907 (C6check.lean) and 6e54f5f83a19 (PolarOrient.lean). ES8SYM/README.md:259-260 records 8c090168 and 4d42e2fb for the compiled files and says only four comment lines differ. This could not be checked without recompiling (not allowed), so the section says the .out logs refer to the compiled versions. The ES7Corollaries.lean and PRIMEFOLD hashes match their records.
- The ES(7) corollaries are conditional on Fivefold35 and Fourfold32, which are hypotheses here; the project supports them with the computer-assisted SAT results in SYM5 and C4CUT (cake_lpr accepted). They are different Lean constants from SYMLEAN's same-text propositions, and no Lean bridge exists. The copied Fourfold32 docstring is inaccurate in this file. All of this is stated in Remark ec:rem:cases.
- Export-label layout: ec:thm:fivefold is on fivefold_heptagon, and its two variants are separate theorems (ec:thm:fivefold-erase, ec:thm:fivefold-nc). ec:thm:fourfold is on fourfold_heptagon, with variant ec:thm:fourfold-erase. ec:thm:compat is one combined theorem with parts (a) dvd_card, (b) card_mod, (c) exists_iff, (d) classification. ec:thm:l0 combines L0 and L0_rot.
- Hypotheses kept visible: PCompat.exists_iff and exists_card0/1 take hr0 and hdisj on r, which Lean never discharges for C. The remark gives a written-step instance (r_i = i+1) and notes that general position and Fermat's little theorem are not formalized. L0 excludes the centre by parity, not by general position. part_a has no planar link in Lean; Corollary ec:cor:planar supplies a written one, labelled written step.
- RefuteC6.m4_with_centre_counter has no #print axioms line; it is covered by the file's clean compile log only. ex341 is labelled computer-assisted; its arithmetic is also done by hand in the proof.
- Self-review done: all 49 \leanref name/line pairs were checked mechanically against the source lines. Every identity and the arithmetic were checked with sympy: determinant/cross expansions, det_mul_eq, the centre case, scaling, ngonPt, the strict-convexity norm identity, the complex form of rotAbout, the half-turn, the radius vs inverse-radius polar forms, the thresholds, the ex341 numerals, and the classification for m <= 3000. Two clean pdflatex passes exit 0; the only undefined references are fd:, ll:, lg: and sr: export labels, which exist in the other section files.

## contract_discrepancies
- Section body is wrapped in \begingroup\sloppy ... \endgroup (local layout setting, no new macro) to limit head overflows caused by the shared preamble; remove if the preamble gets a global fix.
- No other deviations: the section starts with \section{...}\label{ec:sec}, all labels start with ec:, \ref targets are only own labels, fd: labels and allowed export labels (ll:thm:reduction, ll:lem:minperiod, ll:thm:card-peel, ll:thm:layers, lg:lem:centre, lg:lem:polar, sr:def:classes).

## not_covered
- LEANEXT/es7corr/ES7Corollaries.lean lines 1-1147: verbatim copy of LAYERLEAN/LayerLemma.lean lines 1-1147 (checked with diff); belongs to the ll/lg sections. Used here only via ll:thm:reduction (convexNGon_of_layers, :1066) and lg:lem:centre (centre_not_mem_of_even, :582), recalled in prose as (R) and (C).
- #print axioms commands (C6check.lean:119-123, PolarOrient.lean:127-132, PCompatCore.lean:285-291, L0Check.lean:152): evidence, not results.
- ES8SLACK (EarlyVertex.lean, Identity.lean, and the never-compiled Composition311.lean and TemplateRowsC3.lean): out of scope for this section, as instructed; mentioned in the Coverage paragraph with a pointer to ES8SLACK/proofs.md.

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/ec.tex as of the snapshot)
- 1.1pt in paragraph at lines 668--669
- 10.6pt in paragraph at lines 645--646
- 30.8pt in paragraph at lines 780--781
- 4.4pt in paragraph at lines 640--642
- 5.1pt in paragraph at lines 602--603
