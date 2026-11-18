# Independent verification of the Delta results

**CONFIRMED**, at the scopes stated below. This is a written/computational
verification record, not a Lean proof or a refereed result. The general weak
conjectures for n=7 and n=8 are not confirmed by this work.

## Terminal-safe boundary follow-up, 14 November, 04:10 KST

[The boundary record](resume/selection/boundary/README.md) adds three
cake_lpr-certified terminal-safe failure formulas at n6/m9, n7/m11, n8/m13.
The independent worker reconstructed the new clause families, checked
real canonical assignments and independently replayed all three LRATs.
Combined with the written cup-rank/localization argument, every old valid
set through these sizes admits one terminal-safe Delta that extends with
every rightmost point preserving five-cap-freeness. The extension itself
need not avoid an n-gon. This does not increase the prior finite rooted
frontier under the full no-n-gon premise.

A separate written integer family refutes the cup/complement shortcut for
all n>=6 while retaining two-point terminal-safe Deltas. Parent and track
controls agree at n6/7/8. The weaker envelope route has written exact
characterizations and eight positive fixed-instance controls; the parent
checked those witnesses and 364 rational domination certificates. No
all-size Delta claim, Lean formalization or ES-bound improvement follows.
See [the boundary audit](resume/selection/boundary/audit/VERIFY_BOUNDARY.md).

## Favorable-selection follow-up, 14 November

[The new selection record](resume/selection/README.md) proves a written
rooted-existence theorem for five-cap-free S, rightmost root, n≥6 and
|S|≤2n−3, without an n-gon-free premise. Its cup-rank argument and the
one-old-blue small-size repair theorem were reviewed by the parent; exact
controls are separate from those written proofs. Neither is Lean-checked.

Ten finite rooted CNFs (n7/m9–13 and n8/m10–14) received fresh LRAT proofs.
The separate auditor independently regenerated all 15 filtered formulas,
checked real canonical models and mask coverage, and replayed **all ten
accepted proofs with cake_lpr**. Smaller sizes have a direct cardinality
proof. Thus rooted weak Delta holds through 13 points for n7 and 14 for n8
under the stated signotope/real premises. Larger trials remain UNKNOWN.
See [VERIFY_ROOTED.md](resume/selection/audit/VERIFY_ROOTED.md).

Three fixed real obstructions were independently checked by the parent
using new coordinate/whole-subset code, then freshly certified: terminal-rank
selection fails at n7/m18; one-old-blue repair fails for specific old Deltas
at n7/m14 and n8/m16, even with the deleted point rightmost. All three still
have ordinary weak Deltas. The terminal example even has a Delta satisfying
the weaker envelope condition on the entire right half-line. Parent exact
checks, CNF/proof hashes and accepted logs are in
`resume/selection/data/parent_obstructions.json` and `data/certificates/`
relative to that selection directory.

The alternative specialized rooted encoder produced only UNKNOWN searches.
None of the finite accepted claims depends on it. No arbitrary-size Delta
theorem, weak-Delta counterexample, numerical ES improvement, or priority
claim follows from this pass.

## Continuation completed 14 November

[The continuation record](resume/README.md) preserves the completed parallel
tracks. Its [independent audit](resume/audit/README.md) confirms the written
compact-encoder equivalence, all-gap embedding equivalence, exact pool
exports, and the real 12-point counterexample to arbitrary maximality.
The compact m16/n7 and m16/n8 formulas independently regenerate to the
scheduled hashes; both completed solver runs are UNKNOWN. The two batched
pool m16 runs also ended UNKNOWN. None extends a universal frontier.

The parent's fresh all-gap one-insertion cup-n7 proof was accepted by cake;
the independent reviewer checked source, regenerated CNF, proof hashes and
the literal success log. This rules out a counterexample containing the
fixed old15 order type plus one point, not arbitrary 16-point sets or larger
extensions. The reviewer did not perform an additional cake invocation.

The five-insertion weak-n8 lemma has an independent written review. The
extreme-point envelope theorem and sharp n+2 deletion-repair obstructions
have written proofs, two separately implemented exact checks and parent
review; their second checker is not attributed to a separate author.
The 9-, 10- and 12-point real strategy obstructions all have working weak
Deltas. No weak conjecture is refuted by them.

The late five-point-hexagon-transversal probe has a separate parent checker,
which validates all 241,748 CNF clauses and the exact abstract witness. Its
minimum hexagon transversal has size six, but it has 16,794 weak Deltas.
Real realizability remains unresolved. That probe lies outside the separate
agent audit and does not refute a real-point statement.

The continuation's archived result JSON files and parent SHA256SUMS bind
these completed outcomes to the inputs, commands, logs and retained external
proofs/traces. No new Lean checking or refereeing is claimed.

## Real cup-side counterexample at (5,6)

The 15 integer coordinates in `coordinator/data/cup15/realized.json` were first
found by a numerical realization search. Neither numerical optimizer statuses
nor the universal SAT model are needed for the final counterexample check.

Two separately written coordinate programs agree:

1. `coordinator/audit_cup15.py`: arbitrary-precision determinants, all-subset
   monotone hulls, and a direct scan of all 32,768 Delta masks. It constructs
   the final small coloring CNF from actual cap and lower-chain lists.
2. `encoder_audit/coordinate_audit.py`: no imports from the encoder, model
   checker, or coordinator audit. It separately uses integer hulls and
   homogeneous cap/cup chain pairs; these two constructions yield the same
   target families. It scans all Delta masks directly, without SAT or a
   subset-lattice transform.

Both find 455 matching, nonzero determinant signs; no 5-cap; no convex hexagon;
80 four-caps; 216 pentagons; 103 distinct lower chains; zero cup-side Delta;
and 353 weak Delta choices. The second audit explicitly accounts for every
mask: 23,586 contain a four-cap, and the other 9,182 miss a lower chain.
Its full report and witness-family hashes are in
`encoder_audit/candidate_geometry.json`.

The final coloring CNF has 15 variables and 183 clauses. Its negative clauses
are the actual 80 four-caps. Each of its 103 positive clauses has an explicit
pentagon carrier in `coordinator/data/cup15/independent_geometry.json`.
Its LRAT proof was freshly generated with CaDiCaL 2.1.3 and accepted by
cake_lpr with the exact line `s VERIFIED UNSAT`. The CNF hash is
`739c18a2261ba90acabd74c88f7b461485d4f1153f960d776995aef901760c71`;
the LRAT hash is
`f44d9ca8f512b4ee51df1d17991f67403e29e742b6f50d1246abd3baca1d889d`.

Thus the real-point cup-side strengthening of D(5,6) is **refuted**. This
finite counterexample does not depend on soundness of the large discovery
encoder. It does not refute weak D(5,6), D(5,7), or D(5,8). Explicit witnesses
for all one-point deletions are in `coordinator/data/cup15/deletions.json`;
they establish deletion-minimality, not global minimality.

## The universal encoder and the 14-point octagon statement

The new encoder's author supplied `encoder/DESIGN.md`, with exact semantics
for every clause family and both directions of the canonical-assignment
argument. A separate reviewer examined the code, the absent-witness and alias
cases, the reduced subset lattice, cap/cup interior disjointness, flat pools,
and optional restrictions. See `encoder_audit/AUDIT.md`.

The all-size proof that a cap/cup union satisfies the four-subset convexity
criterion was independently checked. It closes the written proof gap noted
in DELTA2's earlier audit: on such a union, every triple has the chord sign
of its middle vertex. This is a mathematical argument, not an extrapolation
from small enumeration.

The independent canonical evaluator reconstructs intended semantic values
without using the solver's auxiliary values. For the discovered candidate it
satisfied all 181,556 clauses and 781,297 literals of the actual universal
CNF; it also checked zero nodes and aliases. Small positive and negative
controls are recorded separately. None of those finite controls substitutes
for the written soundness argument.

The **unconditioned flat cup-side (5,8), m=14** CNF was accepted by cake_lpr.
No mirror constraint, cube, fixed orientation, or extra geometric assumption
was used. The statement confirmed is:

> Every 14-point signotope with no 5-cap and no convex octagon has a 4-cap-free
> subset meeting the lower chain, including endpoints, of every convex heptagon.

In particular it holds for real point sets. This extends the previous
cup-side frontier from 13 to 14 points when combined with the earlier
size-by-size certificates; it does not prove the unrestricted conjecture.

CNF SHA-256:
`a0e37105f825fc655ea76faef691c92b3748d99e654fb86cd101545afc1a1dbc`.
LRAT SHA-256:
`03e6d69917731b55a4fd2d70255668c4caf8a5c52b9343cf99662ac9c2d8344c`.
The parent independently recomputed both file hashes and inspected the exact
checker line. Timings were 53.564 seconds for CaDiCaL and 8.429 seconds for
cake_lpr. Full files remain in the encoder scratch directory
`fallback-flat-n8-m14/`; small evidence is in `coordinator/data/frontier/`.
The proof has not been independently regenerated a second time.

## Auxiliary results

- The 16-point failure of minimum-cardinality optimization was independently
  checked by `coordinator/audit_minimum.py`, including every actual saved
  clause family, a separate hull enumeration, and all 65,536 subsets. Both
  cardinality exclusion CNFs have accepted LRAT proofs. The correct optimum
  is four unrestricted versus five 4-cap-free; this is not a Delta failure.
- The a=4 restricted human theorem was reviewed independently in
  `encoder/A4_REVIEW.md`, including the k=3 case and the reflected noncanonical
  edge labels. The extra extreme-point hypothesis is essential to the proof.
- Hypergraph hole-exchange obstructions and descent fan-coverage obstructions
  have separate exact-coordinate checkers. They refute the specified repair
  rules; they do not refute weak Delta.
- The bounded lifting follow-up in `hypergraph/LIFT.md` includes two accepted
  LRAT proofs and separate exact geometry controls. The parent reviewed the
  projection argument and required an explicit per-fiber bound for arbitrary
  convex subsets, including endpoints; the final argument supplies it. The
  exclusions apply only to the stated generic cluster models. The control
  driver imports the formula under test and is not a second independent CNF
  encoder, and the LRAT proofs have not had a second independent replay.

## Limits of verification

Unknown solver outcomes remain unknown. In particular, neither a time limit
nor the existence of a large partial LRAT trace counts as a certificate.
No new Delta theorem here is Lean-checked. The trusted computational boundary
includes the exact-integer audit programs and cake_lpr. All original proof
artifacts are retained; compressed copies are verified by decompressed hash.
No claim about literature priority is made.
