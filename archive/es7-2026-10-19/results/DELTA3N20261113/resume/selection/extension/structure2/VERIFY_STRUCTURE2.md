# Verification scope for the rank-five subclass work

**Separate exact arithmetic code within this track: PASS.** This is not
an independent outside review, a Lean formalization or a CERTIFIED LRAT
result. No SAT solver was used. Written arguments and fixed-instance
computations have separate scopes.

## Separated theorem

The proof uses four elementary steps: the split determines mixed cups and
caps; a mixed convex subset is precisely a cup from L plus a cap from R;
this classifies six-gons by the maximum cup length c of L; and one global
rank level then hits them all. Single-rank terminal safety is the prior
written lemma. The no-seven-gon hypothesis is used to exclude a three-cap
in R when c=4. The c=3 case additionally uses that a top cup-rank level in
a four-cap-free R is itself a cup.

`separator_controls.py` generates three exact integer sets and uses
translated determinants, edge DP for ranks, and exhaustive monotone hulls
for all six- and seven-subsets. Outputs are `separator_c2.json`,
`separator_c3.json`, `separator_c4.json`. Their sizes are 19,25,25;
maxima are (cap,cup,gon)=(4,5,6); every asserted selector is terminal-safe.
The two 25-point controls share the same labeled six-gon family, but have
different four-cap counts, so they are not independent sampling evidence.

`verify_structure2.py` imports none of the finder, generator or prior
checker code. It reconstructs signed 3x3 determinants, enumerates cups of
sizes 2 through 6 to recover ranks, and exhausts four- and five-caps. It
checks the split and the exact rank identity on R afresh.

For polygon maxima it uses cup/cap chains with prescribed common left and
right endpoints. Their interiors lie strictly on opposite sides of the
endpoint chord, so a longest lower cup and upper cap together give a
convex polygon of size their lengths minus two. Conversely every convex
polygon has such two chains. DP transitions extend only reachable states;
unreachable zero states are never extended. This implementation agrees
with an independent triangle-containment enumeration on 24 deterministic
general-position controls of sizes 3 through 8.

The replay finds full maximum gon six and selected-complement maximum gon
five for each separator control. It directly checks all 92 selected cap
triples in the two 25-point examples against actual ambient terminal pairs;
the 19-point selector is a cup. Thus target coverage and cap safety are
confirmed without the generator's hull code. Runtime was about 0.197 s,
peak RSS 18,832 KiB for the complete replay.

## Failed candidate and pair replacement

The same independent checker reconstructs terminal18 ranks and premises,
checks each hexagon used in `failed_steps.md` by triangle containment,
checks each claimed four-cap, and verifies exposure of triple (12,16,17)
at X=max_x(U)+1 against every ambient four-cap line. Thus both displayed
finite contradictions are arithmetic proofs, without solver certification.

`check_candidate_hypothesis.py` uses that independent DP on the frozen
coordinates. The complement of L5 has maximum gon six, while the complement
of L5 union {10} has maximum gon five. Therefore the attempted lemma's
common-representative hypothesis truly holds, nonvacuously, for p=10.
The four-target contradiction then refutes its conclusion.

The checker also confirms A={3,4,7,10,14,16} as a uniform selector using
direct rational line certificates and complement polygon DP. It does not
independently re-enumerate all 4,096 subsets: the counts 28 ordinary / 16
uniform / 0 terminal / 0 graph-independent are the restricted finder's
exact computations. They are not needed for either written contradiction.

## Parent cup-domination rule and corrected fixture claim

The componentwise cup-shift line implication is proved in
`cup_domination.md`, with attribution to the parent. Four-cap avoidance
remains a separate premise. The independent replay confirms that the two
withdrawn terminal18 quadruples have signs ++--, not all positive, and
retains their integer determinants. The parent later reported other
cup-protected terminal18 selections; this track also checked explicit
positive selections in its restricted top-two-level test. It does not
duplicate the parent's whole-set counts.

A separate seven-point integer control exercises the strict four-cup,
shared-intermediate-endpoint, and shared-final-endpoint branches. All three
target triples are caps, the common ambient four-cap is real, no five-cap
exists, and exact slopes/heights give domination.

## General split reductions and closure replay

The n>=5 cup-bounded generalization has ten small named controls and a
completed n5 grid with 65 valid splits. The stronger no-cup-bound
high-split reduction has its own frozen packet, `VERIFY_HIGHSPLIT.md` and
`HIGHSPLIT_SHA256SUMS`. That packet includes 90 n5 splits, 344 conditional
lifts, eighteen named controls, the last-cut negative control and its
separate source/invariant replay. The parent reviewed its written proof.

`closure_controls.py` compares actual pair-graph transitive closure with
the two-triangle formula on eight fixed fixtures and 48 deterministic
small configurations. The separate `verify_closure_examples.py` checks
the real nine-point strictness example and the cup-protected four-cap
inside terminal18's top two rank levels. Both pass; no global existence
invariance claim follows from the specified-selection examples.

## Low-split and all-mixed-cup follow-up

`low_split.md` proves the absent-long-cup low-split case and the exact
two-option elimination of the right block for every n>=5. It explicitly
leaves universal existence of the left predicate unresolved. The previous
a4 terminal-polygon proof is used only with its absent-cup hypothesis;
no extra outer root is needed for that lemma.

The low-left probes test only a bounded n5 grid, ten old a4 real controls
plus the trimming example and their reflections, and four predesignated
old n7 left blocks. Every tested remaining-branch set has an Option 1
cup. Several simple rank shortcuts fail and have explicit coordinates.
These positive tests are not promoted to a theorem. `low_split_controls.py`
checks eleven full geometric joins, including R blocks with cap triples.

`verify_low_classification.py` is a separate implementation with no
imports from the finder, generator, previous geometry checker or SAT code.
It computes actual terminal membership constraints from exact real
coordinates, closes them upward over all subsets, and compares all
532,608 full-set assignments in three controls with the classification.
Every assignment agrees; counts are 36,60,616 at n5,n6,n7. This audits the
geometric classification on those inputs, not the parent's CNF encoder.

`cup_join.md` proves the all-mixed-cup cut reduction. Its five exact
controls cover interior cuts at n5,n6,n8 and both singleton-end lifts at
n7. The n5 selector has two genuinely selected cap triples; both n7 lifts
retain 46. Internal ranks, cross signs, full/complement polygon maxima
and ambient terminal certificates all pass. These controls reuse the
frozen exact helper and are not called an outside independent audit.

## Limits and retained incidents

The known terminal18 and the boundary three-block n7 family were checked
at every x cut and have no split of the theorem's type. The theorem makes
no claim about them. General maximum-cup-five selection remains open here.

No timeout, OOM, solver UNKNOWN or proof deletion occurred. Failed candidate
claims, the overly strong first-pair graph, a diagnostic tuple/list counting
mistake, two atomic patch-context failures and the withdrawn parent fixture
claim are preserved in the record. No stored geometry used the diagnostic
zero counts. No long job was started or reserved.
