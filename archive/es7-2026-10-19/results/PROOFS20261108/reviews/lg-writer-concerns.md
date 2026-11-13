# Writer report for section `lg` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- The preamble has a layout problem that affects every section. amsthm typesets the theorem head inside \sbox\@labels, a box, so the \nolinkurl break points inside \leanref names are lost and a head can only break at spaces. Heads therefore overflow, by up to about 100pt (beyond the page edge), unless the first head line happens to be nearly full. I chose this section's short names empirically so that every head breaks cleanly; the final build has no overfull or underfull boxes. This tuning depends on the width of the 'Lemma N.M' prefix (a two-digit section number adds about 6pt). A preamble-level fix would be more robust, e.g. letting \leanref start with \hfil\penalty0\hfilneg or putting the Lean reference on its own line. Requesting this as a macro change.
- \lean{} (url-based) drops spaces, so multi-word Lean expressions (e.g. 'Invariant (rotAbout c (2 * Real.pi / m)) S', 'HasConvexNGon (n + 1) S', 'Fin (n + 1)') are written with \texttt instead. Other sections may hit the same problem.
- Axioms evidence: 16 of the 23 theorems are in LAYERLEAN/logs/axioms.log. The other 7 (rotAbout_iterate, orient_rotAbout, convex_orient_nonneg, orient_eq_lin, lin_rotAbout, lin_orbit_pos, orient_next_prev_pos) appear only in LEANEXT/review/axioms.log. Its 59 names match exactly the 59 non-simp theorems of LayerLemma.lean (checked by a name diff); the section says this explicitly.
- Two proof steps differ from Lean, and remarks say so. (1) x != rho(x) in strict_nesting is derived from lin_orbit_pos with j=1, where Lean uses the minimal period. (2) rho(p') = rho^m(p) = p in lin_pos_of_peel is derived from rotAbout_iterate plus rotation by 2pi = id, where Lean uses minimalPeriod_rotAbout. rotAbout_iterate is proved by the matrix composition rule instead of Lean's complex form.
- The section depends on the ll export statements as described in the contract: ll:thm:core-rot (hullVerts_eq_orbitFS_rotAbout), ll:lem:inv-peel, ll:lem:hv (subset_convexHull_hullVerts), ll:lem:antitone, plus ll:lem:minperiod and ll:thm:card-peel in remarks and coverage. These are recalled as (L1)-(L4) in the notation subsection; if the ll writer phrases them differently, check that the recall still matches.
- Every identity used was checked with sympy (all residuals 0): orient_rotAbout (as a polynomial identity with free cos/sin symbols), trig_layer, the rotation composition rule and R_a R_b = R_{a+b}, the orient_trans_halfplane, fan_step and lin_pos_of_peel key identities, the Cramer identity, orient_eq_lin, lin_rotAbout, orient_polar, the rule-B decomposition, convex_disk, the centre computation and the angle bookkeeping. Script: reviews/checks/lg_sympy_check.py
- Output files: STAGE/sections/lg.tex and STAGE/sections/lg.map.tsv. The compile check is build/lg_wrapper.tex: two pdflatex passes, both exit 0, no errors, no box warnings. The only undefined references are the allowed fd:/ll: export labels.

## contract_discrepancies
- The contract pairs export label lg:lem:regular with 'orient_regular_nonneg (with trig_layer)'. lg:lem:regular is defined on orient_regular_nonneg, and trig_layer has its own lemma (lg:lem:trig, LayerLemma.lean:480), which the proof of lg:lem:regular uses. This keeps one Lean name per map row.
- The map has one row per theorem/lemma/corollary/definition environment (31 rows). The section's remarks are unlabeled and have no Lean counterpart, so they are not listed in the map.

## not_covered
- peel_antitone (LayerLemma.lean:460) and card_peel (:1037, docstring :1036): inside the given line range but owned by section ll (ll:lem:antitone, ll:thm:card-peel); \ref'd, not restated
- Verbatim duplicates of these declarations in LEANEXT/capstone/Capstone2.lean, LEANEXT/merged/Merged.lean, LEANEXT/es7corr/ES7Corollaries.lean, ENCBLEAN/geo/ES8Geo/Capstone2.lean (each contains LayerLemma.lean lines 11-1147 verbatim; checked by substring test)

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/lg.tex as of the snapshot)
- none
