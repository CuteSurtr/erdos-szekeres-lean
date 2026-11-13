# Writer report for section `oc` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Layout workaround: section body is wrapped in \begingroup\sloppy\emergencystretch=15em ... \endgroup (balanced, no new macros). Without it, amsthm theorem heads with several \leanref entries overflow the margin by up to ~160pt, because URL line breaks inside the boxed head are unavailable. Heads with many references are now loose but within the margin.
- Multi-word Lean terms are typeset with \texttt (e.g. \texttt{Invariant f S}, \texttt{(k \% m).toNat}, \texttt{\#print axioms}) because \lean/\nolinkurl drops spaces and breaks on % and #.
- PreservesOrient.iterate has no recorded axiom output (no printed theorem depends on it); stated in the intro.
- KeyOrder axiom output exists only for the byte-identical ENCBLEAN copy (ENCBLEAN/logs/m4_build.log:3-10), not inside LEANEXT; stated in the intro.
- Remark oc:rem:layers(3) gives my own counterexample (S4-type set with m=4, K=8) showing 2pi/m cannot be replaced by pi/m in phase_ne_of_distinct_layers; full written argument given, checked by exact arithmetic.
- Remark oc:rem:parity cites encoder code lines C7UPPER/gen.py:108 (sortpar) and C6UPPER/encb/gen_b2.py:56 (perm_sign) and gives a hand six-case table sign = (-1)^inv; the code-to-statement correspondence remains outside Lean (Python evidence only).
- Statements with OrbitConsistency and Merged (LayerLemma) copies are stated once with both Lean names; identity of the duplicated constants is explained in Remark oc:rem:copies.
- Proof routes differing from Lean are flagged: rotAbout_iterate (addition formulas), orient3_swap (orient symmetries), iterate_mem_hullVerts_peel (rho^[m]=id directly instead of minimalPeriod_rotAbout).

## contract_discrepancies
- Mandated head format \begin{lemma}[name; \leanref{...}{...}] produces overfull lines under amsthm: the head is boxed, so URL breaks inside long Lean names and paths do not occur. Suggest a preamble-level remedy (e.g. a global \emergencystretch or a breakable \leanref) so sections do not need local \sloppy groups.
- \lean (\nolinkurl) silently drops spaces and cannot take % or #; a separate macro for multi-word Lean code would help.
- No export labels exist for whole sections (fd:sec, ll:sec, lg:sec are not in the allowed list), so other sections are referred to by name only.

## not_covered
- OrbitConsistency.lean lines 49-103 complex-coordinate helpers (toC, ofC, toC_re, toC_im, ofC_zero, ofC_one, toC_ofC, ofC_toC, toC_injective, crot, toC_crot, crot_one, crot_comp, crot_iterate, rotAbout_eq_crot): verbatim copies of LAYERLEAN/LayerLemma.lean:231-308, not needed (rotAbout_iterate proved via addition formulas)
- Merged.lean lines 1-1147: copy of LAYERLEAN/LayerLemma.lean (sections ll/lg)
- KeyOrder.lean:151-158: #print axioms commands, not results
- Verbatim copies in LEANEXT/capstone/Capstone2.lean (lines 1156-1391) and ENCBLEAN/geo/ES8Geo (byte-identical OrbitConsistency.lean, KeyOrder.lean)
- Python evidence (orbit/check_literals.py and logs) and mutant logs: cited as evidence only, not Lean results

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/oc.tex as of the snapshot)
- none
