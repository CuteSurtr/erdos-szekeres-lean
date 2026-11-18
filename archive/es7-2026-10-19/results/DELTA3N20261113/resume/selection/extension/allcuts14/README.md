# Conditional terminal n7/m14 search with three cut families

**COMPUTED formula construction; bounded search ended UNKNOWN.**
This experiment adds exclusions for high splits, low splits, and splits
with every crossing triple a cup. The base is the already audited exact
containment formula. It is a conditional search, not an unconditional
propositional equivalence or a new symmetry assumption.

For a 14-point real failure, high cuts are impossible by the written
high-split reduction and the established size-13 terminal theorem.
All-mixed-cup cuts are similarly impossible by the written cup-join
reduction; its two singleton-end cases use the same size-13 theorem.

For a low split, write d=maxcup(R). The easy d=5 and d=4 cases are handled
by the written reduction; d=5 reduces to the 13-point right block.
For d<=3 the left set has no four-cap and at most13 points. The exact
T7(L) equivalence supplies a terminal-safe Delta provided T7(L) holds.
For left sizes<=10, join L to a sufficiently low three-cup: the resulting
valid set has at most13 points, so the known terminal theorem and the
equivalence give T7(L). Left sizes11,12,13 have separate accepted direct
formula proofs. Their encoder soundness/instance audit and fresh proof
replays are complete in `../low_split_audit/`.

Each excluded cut contributes the disjunction of negations of all its
crossing orientation signs. All three families and all13 cuts are
generated. Two endpoint clauses coincide, leaving37 distinct clauses
and8,034 added literals. No fixed coordinate signs are imposed.

`../augment_allcuts14.py` records the full row provenance, source hashes,
and explicit dependencies. The separate
[row and soundness audit](../allcuts14_audit/README.md) is complete: it
reconstructs all37 rows, checks their39 provenance entries and8034
literals, and verifies the unchanged base formula. The search itself
ended without a conclusive result. Any later UNSAT outcome requires cake_lpr's exact
acceptance line and independent row/proof review before a geometric
theorem follows. Any SAT outcome requires full semantic checks and exact
realization before it becomes a geometric counterexample.

This record does not alter the earlier high-split-only search or its
frozen audit. General Delta, uniform selection, and ES bounds stay open
at their prior statuses.

The2700-second solver budget ended UNKNOWN. Total retained run time,
including streamed hashes and verified compression roundtrip, was2725.590s.
Its3,912,087,705-byte search trace is not an accepted UNSAT proof.
[data/allcuts14-a/result.json](data/allcuts14-a/result.json) retains the
commands and hashes. The separate earlier high-cut-only search likewise
ended UNKNOWN at its5400-second budget; its receipt is preserved separately
as [data/indecomp14-a/result.json](data/indecomp14-a/result.json).
Neither outcome establishes existence or nonexistence of a14-point failure.
