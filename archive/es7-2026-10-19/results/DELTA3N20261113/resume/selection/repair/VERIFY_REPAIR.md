# Verification of the frozen repair cases

**Confirmed by independent implementations; full one-blue formulas CERTIFIED
by the parent.** This note distinguishes the track's second implementation
from the parent's separate audit. It is not a claim that this track reran
the parent's proof checker.

`repair.cpp` supplied the finder, exact geometric family counts, complete
full-Delta families and min-plus repair costs. The track's `verify.py` uses
different geometry algorithms and Python unbounded integers, scans every
full B once, and reproduces the following:

| Case | Four-caps | Targets | Old targets | Five-caps | Convex n-gons | Full Deltas | Minimum cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| Rightmost n7/m14 | 59 | 109 | 79 | 0 | 0 | 2,669 | 2 |
| Rightmost n8/m16 | 90 | 121 | 85 | 0 | 0 | 15,356 | 2 |

Every coordinate is an integer, x is strictly increasing, and every triple
determinant is nonzero. The given A contains no four-cap and hits all old
targets. The cost calculation permits every subset B, both colors of r,
arbitrary deletion of A and all old-blue points.

The supplemental `controls.py` 0-1 BFS computes all directed distances from
the full-Delta family. It reproduces the C++ repair-cost histograms for every
root and every old Delta: 32,293 n7 and 166,896 n8 pairs. It also checks the
one-blue positive fixtures and all clauses of ordinary and r-selected
two-blue controls.

The ordinary n7 positive is {1,5,9}; its r-selected counterpart is
{1,5,9,13}. The ordinary n8 positive is {2,3}; its r-selected counterpart
is {2,3,15}. Exactly 1,091 n7 full Deltas and 6,164 n8 full Deltas select r.
The minimum cost remains two even when r is required selected, because
the general lower bound applies and these positives attain it.

`proof_core.py` checks that T is one of the enumerated four-caps, each
displayed private polygon belongs to the complete target family, its
intersection with T is exactly the stated singleton, and the listed blue
supports have empty intersection. It also verifies every core clause is
literally present in the corresponding full formula. The written
private-polygon contradiction covers every possible one-blue repair.

The parent separately checked all coordinate predicates, complete clause
families, old-Delta validity, full-Delta counts and exact minimum cost in
`../check_obstructions.py`. Its repair7 and repair8 records in
`../data/parent_obstructions.json` say INDEPENDENTLY CONFIRMED. The parent
then generated fresh LRAT proofs of the full formulas. This track read
the literal `s VERIFIED UNSAT` line in each cake log and matched hashes of
both frozen CNFs, plain LRATs and zstd LRATs with the completed result files.
No local cake replay is claimed. The parent verified compressed round trips.

The main finite-coordinate claims are therefore COMPUTED and independently
confirmed; the full propositional no-one-blue formulas are CERTIFIED; the
small-size positive lemma and general exact criteria are PROVED in written
form. Nothing is Lean-checked, and neither weak Delta existence conjecture
is refuted. No global size-minimality or universal two-blue sufficiency is
claimed.
