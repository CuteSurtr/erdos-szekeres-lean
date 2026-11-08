# Writer report for section `cb` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- C2FINAL/Central34Orbits.lean has no committed compile or axioms log; its Lean-checked label rests on C2FINAL/README.md section 6 (propext only). This is stated in the intro and in the map notes.
- The amsthm theorem head is set in an unbreakable box (amsthm.sty, \sbox\@labels). One \leanref fits a head line of 484pt; two need about 600-640pt, and multi-ref heads overflowed by up to 1700pt in a first draft. I therefore gave each Lean declaration its own statement environment (100 environments). For the export lemma cb:lem:run, which must carry both run_sound and checkRoot_sound, I stacked the two \leanref inside a bottom-aligned tabular in the head (no new macro). Other sections with several \leanref in one head (e.g. sr.tex:192, sr:def:classes) will run off the page in the PDF.
- \lean{...} (\nolinkurl) drops spaces, so code fragments with spaces (Elab.async false, x == y, Nat.testBit n i, Covered S) are set with \texttt instead.
- Scope honesty: the leaf predicate of all_roots_covered is the certificates' own key list. 554 of the 910 roots are their own single leaf (ds = 0, checked by grep on the data). Certification and hash matching are Python audits outside Lean, and lrat-check verdicts alone carry no weight. All of this is stated in Remark cb:rem:use.
- Self-checks (not cited in the text): a scratch Python transcription of the C3Cover definitions and checker reproduced reflectionFacts, strata, 910 roots, root order = certificate order, and the 910/76,256/73,567/1,747/942 counts. The Central34 transcription reproduced 560/287/14 per case, 287 or 288 closed entries, uncovered = [] for all 8 cases, and the closedP6 double orbit {[1,7],[5,16]}. All arithmetic identities were checked with sympy. All 81 \leanref name/line pairs were checked against the source lines.
- Compile: two passes exit 0, no overfull boxes. The only undefined reference is the allowed export label sr:def:classes, which exists in sections/sr.tex and is used for context only.

## contract_discrepancies
- The contract's head format allows several \leanref in one head, but amsthm heads cannot break lines. I used one declaration per statement instead, and the stacked-tabular head for cb:lem:run.
- For uniform generated families (batch0..batch126, certs0..certs126, reflection_facts_H6_1_0..H6_5_1, closedP1..closedP8), the head carries the \leanref of the first member. The statement body names the whole family with exact line numbers (e.g. 1740+4N; 370+3(2a+s-2)). The map TSV records the family in the note column.

## not_covered
- The seven negative controls in C3LEAN/C3Cover.lean (control_missing_record 2266, control_missing_sigma_child 2270, control_swapped_keys 2274, control_missing_layer_child 2278, control_wrong_root 2282, control_strict_reduction 2286, control_phi_mutant 2292): tests, listed and described in Coverage (control_strict_reduction's 810 is cross-checked against cb:prop:refl)
- #print axioms lines (C3Cover.lean 2301-2327, Central34Orbits.lean 296-298)
- C3LEAN/tools/prelude.lean: verbatim source of C3Cover.lean lines 29-329 (covered through C3Cover.lean)
- C3LEAN/Control_record.lean, C3LEAN/Control_sibling.lean: must-fail files (prelude copy + one mutated-certificate theorem at line 305)
- C3LEAN/review/RevCtrl_mut.lean (nine rejection controls), C3LEAN/review/RevCtrl_pass.lean (two acceptance controls + rev_parent_decodes, cited in remarks only), C3LEAN/review/RevDiff.lean (#eval harness, no theorems)
- Inventory C3-C2-misc also lists AUDIT3/A1_reduction SizeArith/AssembledSizes lemmas and ES7SPLIT baek_seven; these are outside the scope assigned to section cb and are not covered here

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/cb.tex as of the snapshot)
- none
