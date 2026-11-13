# Writer report for section `mb` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Theorem-head typesetting: amsthm boxes the head, so \nolinkurl break points inside \lean/\dirn are lost and long \leanref items cannot break (overflows up to ~150pt, i.e. text off the page). I mitigated this locally by inserting \\ before every \leanref in heads and \raggedright after the label in 12 statements; the compile now has 0 overfull boxes. A preamble-level fix (e.g. a breakable \leanref or a theorem style that does not box the note) would be cleaner for the whole document (macro request).
- Lemma mb:lem:polygons (the four generated heptagon/octagon lemmas used by mirror_seven and mirror_eight) is proved by instantiating mm:thm:mirror-polygon and mm:thm:axis-polygon with m=4 (plus a one-point deletion for cap_mirror_heptagon); I checked that mm.tex states these exactly as the Lean declarations I restate in the proof.
- Baek: the published geometric Theorem 1.6 (arXiv numbering) differs from the vendored combinatorial statement (arbitrary ternary relation, weak gons); the attribution of the combinatorial form to Baek's Theorem 2.7 is taken from MIRRORETV/README.md section 8 and was not checked against the paper by me.
- Some lemmas are restated with full proofs here although section mm also proves them (card_split, card_A_le, injOn_x, sorting, transport = mm:thm:line(a)); statements are Lean-faithful in both places, so there is duplication but no conflict.
- Axioms evidence is from recorded logs (not re-run): MirrorMain.out 848-863, MirrorNine.out 879-882 (log of MirrorMain.lean ++ MirrorNine_append.lean, lines shifted by 2677), SYMLEAN/mirror/axioms.out (filtered excerpt with repeated lines and truncated #check output).
- mb:thm:main3 is conditional; Remark mb:rem:main3 names the records C2FINAL/C2C34, C3FINAL/C3LEAN, SYM5 and notes, per the records, that part of the case split rests on recorded checker verdicts and sampled re-checks rather than retained proof files.
- Map file has 42 rows: 33 statements (5 definitions, 8 theorems, 16 lemmas, 4 propositions) plus 9 remarks listed with lean_name '-'. All 78 \leanref name/file:line pairs were checked against the sources (0 mismatches). All algebraic identities (four-point, chord, frame/lineRefl, reflLine_eq_lineRefl, interior, injOn_x, binomials) checked with sympy (scratch script outside STAGE).

## contract_discrepancies
- Contract lists mb:thm:nine as 'mirror_nine and mirror_nine_line (with config_capacity113)': I made config_capacity113 part (a) of Theorem mb:thm:nine, with mirror_nine/mirror_nine_line as (b)/(c); capacity113 is Proposition mb:prop:cap113, stated between the proof of (a) and the proof of (b),(c).
- Head format: heads contain forced line breaks (\\) between the short name and each \leanref, and some statements start with \raggedright after the label, to stop overlong \leanref items running off the page; the \leanref{...}{...} content is exactly as the contract specifies.
- The contract calls the fd items 'Facts' but labels them fd:lem:*; fd.tex uses lemma environments, and I refer to them as 'Lemma~\ref{fd:lem:...}', which matches.

## not_covered
- Lean proofs of main and Config.cap_cup: cited published theorems (Baek 2025; Erdos-Szekeres 1935), not reproved, per the task notes
- Generated certificate proofs of cap_mirror_heptagon/octagon, axis_left/right_heptagon and wrappers cyc4-cyc8: statements covered by a different proof (from mm:thm:mirror-polygon, mm:thm:axis-polygon); Remark mb:rem:generated describes the Lean route
- MirrorOdd.mirror_seven' and mirror_eight': consistency duplicates (Remarks mb:rem:seven, mb:rem:eight)
- cap_mirror_polygon, axis_left/right_polygon, cap_below_lines, mirror_odd/even_general(_line), mirror_four/five/six(_line): subject of section mm (referenced via mm:thm:* labels)
- Part A of RTC (five-class reduction, affine extension): subject of sections sr and ar; used via sr:thm:main and ar:thm:main
- Helpers absorbed into proofs: mir_mir, xset, emb, sortPt, sortPt_mem, sortPt_x, sortPt_strictMono, sortPt_injective, unframeLin, unframe_apply, pointAt_eq, pointAt_order, arcOfList, cupArc, capArc, same_first, same_last, CupArc, Boundary, Boundary.flip, Boundary.finite
- Bridge-file declarations not on these proof paths: hasCup_of_list, hasNCup_octagon, listCup_of_hasCup, listCap_of_hasCap, PlanarChains.cup_all
- #print axioms and #check lines (audit output)

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/mb.tex as of the snapshot)
- none
