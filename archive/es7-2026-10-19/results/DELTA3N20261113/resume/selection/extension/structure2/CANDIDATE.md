# Candidate and adversarial plan before any long computation

**Candidate, not proved.** Let U be a real (5,7)-valid set with maximum cup
length five. Write L_i={v: beta(v)=i}, where beta is longest cup ending rank.
Suppose every convex six-gon disjoint from L_5 contains one common vertex
p in L_4. Is there B subset L_5 such that B union {p} is a uniform-envelope
weak Delta?

This is a restricted existence claim with fixed p, not merely the generic
envelope or deletion criterion. It includes the case with no missed target
by taking L_5 alone. The nonvacuous hypothesis holds for the known 18-point
terminal-safe obstruction: L_5 misses exactly two hexagons, both containing
the rank-4 vertex p=10. A terminal-safe version cannot hold there.

## Exact finite tests

1. Use the frozen terminal18 coordinates and the explicit n7 three-block
   family. Recompute cup ranks, polygons, cap quadruples and exposure
   intervals with integers/Fraction. No floating-point statuses are evidence.
2. For each eligible p, enumerate only subsets of L_5. This tests the
   restricted candidate, not arbitrary selections or coordinate hillclimbs.
   On terminal18 there are only 128 such subsets for p=10.
3. Inspect coverage requirements on B and the forbidden pairs/triples that
   involve p. Any failure must retain all exact rows and a checkable finite
   contradiction, not only a finder result. A positive case is a control,
   not a proof of the candidate.
4. If useful, add the small frozen prior structure controls whose maximum
   cup is five. Do not sweep the retained pools or duplicate the envelope
   worker's search. Deliberate deletions are bounded controls only, and
   ranks/envelopes must be recomputed.
5. Try to prove a clear restriction of the candidate from its actual
   obstruction structure. If it stalls, record the precise conditional
   lemma and the missing geometric implication.

Only one-CPU, AS400MiB, external-20-second probes are authorized here. No
long job is reserved; no request for one has been made.

## Recorded outcome

**Refuted by terminal18**, already at the ordinary-Delta level. The exact
four-target/four-cap contradiction is in `failed_steps.md`. The candidate
and original test plan above are retained. The positive theorem proved in
`separated_theorem.md` uses a geometric split hypothesis; no repair of the
candidate's common-vertex hypothesis is silently assumed.

## Second narrow candidate, recorded before its fixed-fixture test

**Candidate, not proved (06:08 KST 14 November).** Under the same n=7
maximum-cup-five hypotheses, can one retain all of L_4 and choose B subset
L_5 so that L_4 union B is a uniform-envelope weak Delta? The previous
terminal18 enumeration supplies positive controls of this form; this is
not an inference of a universal statement from those controls.

Test only the already frozen terminal18, three-block n7, closure9 and
parent's real15 fixtures. Recompute ranks and full geometric hypotheses
first. Enumerate only the at-most-2^|L_5| choices for B, keeping four-cap
exclusion separate and comparing terminal, one-step cup, two-triangle
closure and exact uniform-envelope protection. On failure, extract an
explicit obstruction rather than merely recording a zero count. No pool
sweep, coordinate hillclimb, generic selection CNF or long job is involved.

**Bounded outcome:** terminal18, three-block n7 and closure9 all have
selections of this form. On terminal18, two pass the direct cup criterion
and the exact uniform criterion; none passes the terminal criterion.
The real15 input has maximum cup six and is outside this candidate's
hypotheses. The initial assertion failure and corrected premise result
are both retained. This second candidate remains unproved; no broader
pool search was undertaken.
