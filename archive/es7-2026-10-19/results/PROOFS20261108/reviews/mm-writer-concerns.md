# Writer report for section `mm` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Shared-preamble issue: \leanref inside theorem heads cannot break inside long names, because amsthm builds the head in a box and the url break penalties are lost in restricted horizontal mode. Heads overflowed the page by up to about 120pt, and by 1900pt when a statement began with a list. Workaround in mm.tex: \begingroup\setlength{\emergencystretch}{0.5\linewidth} ... \endgroup around the section body, plus a lead-in sentence before lists that open a statement. Now 0 overfull boxes. A preamble-level fix would help all sections.
- Section mb cannot \ref the counting lemma (mm:lem:count), injOn_x (mm:lem:injx) or the generated heptagon/octagon lemmas (mm:prop:small-polygons), because they are not export labels. mb can still prove mirror_seven/mirror_eight from mm:thm:odd/mm:thm:even with its capacity lemmas (the route of mirror_seven'/mirror_eight'), or the contract could add these labels to the export list.
- The nine generated small-polygon lemmas are proved in writing as instances or sub-polygons of mm:thm:mirror-polygon and mm:thm:axis-polygon. This differs from their machine-generated Lean proofs (linarith certificates), and the text says so.
- Axioms evidence comes from the recorded logs MIRRORETV/lean/MirrorMain.out (848-863) and MirrorNine.out (881); Lean was not re-run, per the hard rules.
- No section in the contract table covers the FarFlat.lean lemmas; the orchestrator may want to assign them.

## contract_discrepancies
- Transport is part (a) of the export-labelled Theorem mm:thm:line (head lists transport, mirror_odd_general_line, mirror_even_general_line), following the contract's '(with transport)', so Section mb can cite it; there is no separate transport label.
- mm:lem:slope (export) holds cap_below_lines as part (a) and, as part (b), the interior-axis-point fact. Part (b) is a written step (inline in the Lean proofs, not a separate declaration) and is labelled as such in the text and in the map.
- The section file uses \begingroup/\endgroup and \setlength{\emergencystretch} (no new macros or packages) to stop statement heads running into the margin; the contract does not mention this kind of local typesetting setting.

## not_covered
- MIRRORETV/lean/FarFlat.lean: root-namespace orient (12), orient_wzq_neg (15), orient_uqz_neg (34), orient_cyclic (55), orient_sum (60), inside_triangle (67), line_misses (89). No declaration in scope uses them (FarFlat imports only Mathlib and MirrorMain does not import it); they belong to the far-flat lower-bound construction (Theorem B). Listed in Coverage.
- MirrorOdd.hasNGon_heptagon, capacity16, mirror_seven_of, mirror_seven, capacity22g, mirror_eight, mirror_seven_line, mirror_eight_line: Baek-based, Section mb (mb:thm:seven, mb:thm:eight)
- MirrorOdd.mirror_seven', MirrorOdd.mirror_eight': consistency duplicates (mm:thm:odd with (3,16) and mm:thm:even with (4,22), with hM from mb's capacity lemmas); explained in Coverage
- #print axioms lines 2662-2677 of MirrorMain.lean (audit commands)
- MirrorNine_append.lean (C12Check namespace, Section mb) and the MIRRORETV/review re-formalizations (out of scope)

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/mm.tex as of the snapshot)
- none
