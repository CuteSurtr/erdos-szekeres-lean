# Writer report for section `pc` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Axioms evidence is uneven. phase/logs/axioms.log covers the 16 main PhaseClassification theorems, and every other PhaseClassification declaration feeds one of them. For the Linked/Capstone/Capstone2 additions there is no saved axiom output in LEANEXT. dist2_polar, polar_eq, exists_angle, sqrt_dist2_pos, ne_of_mem (and polar_zero) are covered transitively by the #guard_msgs pins at ENCBLEAN/geo/ES8Geo/Audit.lean:31-70; I traced that usage chain myself. orient_pos_of_layers, the six Capstone layer rules and orient_pos_of_alternating_polar have no recorded axiom check. Their only evidence is the REPORT claims plus ENCBLEAN/logs/m4_build.log, a clean build that imports the byte-identical Capstone2 module. The intro states all of this.
- Layout: the preamble's url breaking left theorem heads with long Lean names running off the page (38 overfull boxes). I wrapped the section body in \begingroup\sloppy ... \par\endgroup, which is balanced inside pc.tex and does not touch the preamble. 8 overfull boxes remain, all within the margin (the largest is 59pt, in the pc:thm:layers head). A preamble-level fix (e.g. \Urlmuskip=0mu plus 1mu) would help every section; that is a request for the preamble owner.
- pc:thm:layers bundles 7 Lean declarations in one environment so that the export label sits on 'orient_pos_of_layers and the Capstone layer rules'. The common hypotheses are factored out as (L), (P) and (P-sqrt). A verifier may prefer to split the intrinsic versions into a separate corollary.
- pc:lem:polar-facts repeats short proofs of the PhaseClassification copies of LayerLemma's polar formula, rule A, sin_add_lt and rule B. This keeps the section self-contained but duplicates section lg (which it cites).
- Several remarks contain written observations that are not Lean-checked, each labelled as such and proved in place: the four gap_classification disjuncts are mutually exclusive; the three runs are mutually exclusive, so exactly one pattern holds under genericity; gap_classification fails without genericity (example (0, pi, 3pi/2)).
- Checks run: every trig/orient identity in sympy; every linear inequality step (lift indices of all six emptiness lemmas, alternation memberships, arc12 cases, gap cases, relabelling orders, halfplane bound) by an exact Fourier-Motzkin script, which correctly fails on 3 false claims; the 64 Boolean words by enumeration; a 200000-sample numeric test of the pattern definitions, relabelling equivalences and rule signs. The check scripts are in the scratch directory/pc_checks/ (outside STAGE).

## contract_discrepancies
- Documentation inaccuracies, noted in the text where relevant: phase/REPORT.md says 540 lines but PhaseClassification.lean has 545 (the hash prefix matches); the gap_classification docstring says 'exactly one' but Lean proves only the disjunction; LEANEXT/README.md says the files are standalone, not importable modules, but Capstone2.lean is imported as a module by ENCBLEAN (hash pinned in ENCBLEAN/geo/SOURCES.sha256).
- The contract's `\leanref` takes one file:line per name. Where a declaration has several copies (PhaseClassification at +1420 in Capstone(2); Linked at +8), I cite the first occurrence and state the offset rule once in the intro.
- Capstone.lean also has an extra blank line 1425 between the Linked copy and the PhaseClassification copy, which the inventory's description omits; the intro mentions it.

## not_covered
- Capstone.lean/Capstone2.lean lines 1426-1965: verbatim copies of PhaseClassification.lean at line offset +1420, already covered
- Linked.lean lines 1-1384 and the matching lines of Capstone(2): copies of LAYERLEAN/LayerLemma.lean and merged/Merged.lean, which belong to sections ll, lg and oc
- LayerLemma.dist2_le_of_later, peel_subset, hullVerts_subset: quoted with \ref to lg:thm:radius, ll:def:peel and ll:def:hv, not restated as statement environments

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/pc.tex as of the snapshot)
- 1.2pt in paragraph at lines 816--818
- 11.7pt in paragraph at lines 131--132
- 42.1pt in paragraph at lines 893--898
- 5.8pt in paragraph at lines 419--420
- 59.0pt in paragraph at lines 816--818
- 6.5pt in paragraph at lines 816--818
