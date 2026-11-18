# Next cup-rank subclass for n=7

**PROVED (written): high-split and all-mixed-cup cut reductions, an exact
low-split left-predicate reduction, and a two-triangle formula for cup-
comparison closure.** All are stated for every n>=5 where n is relevant.
Several stronger rank shortcuts fail explicitly. Exact controls passed;
the universal low-split left predicate remains unresolved in this track.

**FROZEN, bounded task complete** on 14 November 2026, before the assigned
08:15 KST deadline; started about 05:02 KST. The parent reviewed the
high-split proof, whose earlier packet remains unchanged under
`HIGHSPLIT_SHA256SUMS`. The full track is covered by `SHA256SUMS`.
Scope is this directory only; `extension/theory/` remains untouched.

## Statement

Seek a useful restricted uniform-envelope selection theorem for real sets
with no five-cap, no convex seven-gon, and maximum cup length exactly five.
Weak Delta means four-cap-free and meeting every whole convex six-gon.
Uniform safety additionally means every selected cap-triple terminal line
lies below the ambient four-cap envelope on the whole rightward half-line.

The first proved subclass has a nonempty x-separated split L,R with all LLR
triples cups and all LRR triples caps. For n>=5, no five-cap, no (n-1)-cup
and no convex n-gon imply a terminal-safe selector in one global cup-rank
level. With c=maxcup(L), choose level n-3 for c=n-3 or n-4, and level n-2
for c<=n-5. See [separated_general.md](separated_general.md); the original
[n7 proof](separated_theorem.md) and fixtures are retained as an instance.

The stronger [high-split reduction](highsplit_reduction.md) removes the cup
bound: every such split with |R|>=2 has a terminal-safe Delta. If |R|=1,
the only unresolved branch inherits a protected Delta from L by adding
the singleton. Thus a size-minimal counterexample has no high-split cut,
and recursively high-split-decomposable sets always have terminal-safe
Deltas. For a size-m SAT search, all cuts except the last are excluded
unconditionally; the last needs the same property at size m-1. The
parent's size-13 terminal certificate audit is outside this track.

The [low-split note](low_split.md) proves the hard case when L has no
(n-1)-cup, using the prior a4 endpoint lemma without an outer root. For
arbitrary L, it gives an exact two-option predicate T_n(L), equivalent to
terminal selection after joining an (n-4)-cup on the right and sufficient
for every low-split right block with cup maximum at most n-4. The parent
owns the specialized CNFs and their audits; no universal T_n theorem is
claimed from this track's positive controls.

The [all-mixed-cup reduction](cup_join.md) proves terminal-safe selection
when every crossing triple is a cup and both blocks have size at least
two. Singleton ends reduce to the same property at size m-1. No new SAT
encoder or solver run was made for these cut clauses.

## Model and known constraints

Read `../../structure/theory.md`, `../../boundary/theory/theory.md`, and
`../../terminal/README.md`. In the original maximum-cup-five class, if
beta is the longest cup ending rank, every hexagon's right endpoint has
beta 4 or 5. A cap triple a<b<c with an exposed
terminal line necessarily has beta(a)<beta(b). Individual rank levels and
unions with nonincreasing ranks in x order are terminal-safe.

The 18-point terminal-safe obstruction has maximum cup five and already
rules out a universal terminal-safe theorem in this subclass. The three-
block boundary family has a convex complement to every maximum cup, yet
has two-point safe selectors. Neither fact may be ignored by a proposed
selection argument.

## Method and results

The original [candidate and adversarial plan](CANDIDATE.md) were recorded
before any long computation. Its single-common-rank-four representative
claim fails on terminal18 even for ordinary weak Deltas: four targets force
a four-cap. Replacing each mixed triple/quadruple blocker by its first
pair also fails, via a ten-row contradiction, although the original
constraints have uniform selectors. See [failed_steps.md](failed_steps.md).

The parent's cup-union line criterion is sound, with old four-cap exclusion
kept separate. Its proposed terminal18 certificate was withdrawn and is
retained as a negative control; other positive terminal18 selections were
later reported by the parent. This track does not duplicate the parent's
generic CNFs or another worker's pool/selection search.

**Closure simplification:** over all ordered point pairs, reachability
from (b,c) to (u,v) under componentwise-right cup-union comparisons is
equivalent to b<=u, c<=v and the two cup tests (b,c,v), (b,u,v), omitting
repeated-endpoint tests. The path has length at most two, via (b,v).
Thus closure protection is an existential test of two cup flags and End4,
without recursive path variables. [closure.md](closure.md) proves this.

An explicit nine-point (5,7) set with maximum cup five shows closure is
strictly stronger than the original cup-union rule for a cap triple and
a specified weak Delta. It does not change global existence there: another
singleton Delta passes both rules. On terminal18, closure protects 23
additional cap triples, including three of rank pattern (4,5,5); the
16 known uniform selectors inside the top two levels all pass the original
cup criterion already. No general rank-five existence conclusion follows.

## Controls

Exact separated controls at n=7 have 19,25,25 points and maxima (4,5,6).
A separate implementation rechecks ranks, no-five-cap, full and complement
polygon maxima, terminal certificates, and both finite contradictions.
Its polygon DP agrees with triangle-containment enumeration on 24 small
controls. See [VERIFY_STRUCTURE2.md](VERIFY_STRUCTURE2.md).

For the n>=5 extension, ten named small cases cover both n5 branches,
vacuous edge cases and every branch at n6/n8. A bounded n5 grid completed
19,608 configurations, with 65 valid separated splits (five c=1, sixty
c=2), all passing. This is not exhaustion over real order types. An empty-L
negative control confirms why the nonempty hypothesis is explicit.

Closure reachability agrees exactly with the two-triangle formula on eight
fixed fixtures and 48 deterministic small random configurations. The frozen
two-support-only eight-point line remains unprotected by this stronger
one-line criterion. Mathematical failures and development incidents are
retained; no solver UNKNOWN, timeout or OOM has occurred.

Without a cup bound, the n5 grid has 90 valid splits and checks 344
conditional critical-case lifts, all passing. Eighteen named controls
cover n5,6,7,8. One is the essential negative control: terminal18 plus a
high singleton inherits terminal nonexistence, showing why the last-cut
clause needs its lower-size premise.

The low-left probes check a 109-set remaining-branch n5 grid, 22 fixed
a4 controls including reflections, and four predesignated n7 left blocks.
Eleven full low-split controls pass, including a 25-point set with 46
selected cap triples. A separate implementation importing no finder,
generator, prior checker or encoder compares every full-set selection
against the two-option predicate: all 532,608 assignments in n5/n6/n7
controls agree. Five all-mixed-cup controls also pass.

These finite positives are not universal theorems. Both top cup-rank
levels can individually miss targets, and their union can contain a cap.
The first retain-rank-four probe also preserved a premise assertion
failure on real15; that input has maximum cup six and is outside the
candidate's maximum-cup-five hypotheses. Its corrected replay records
that exclusion explicitly.

## Files and hashes

Proofs are linked above. `tools/` contains the profilers and separate exact
checks; `data/` contains frozen coordinates, all outputs and source/input
hashes. `SHA256SUMS` covers this directory, excluding itself. The earlier
eleven-file `HIGHSPLIT_SHA256SUMS` remains byte-for-byte unchanged.
Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/structure2/`.
No shared manifests or other records have been edited.

## What remains

The full unseparated maximum-cup-five uniform-selection problem and a
general written proof of T_n(L) remain unresolved. Parent finite CNF
runs and semantic/proof audits are separate dependencies; their changing
status is not incorporated into this frozen theorem record. No weak-
Delta failure, global existence-invariance result, novelty claim, Lean
formalization or numerical ES improvement follows from this work.

## Resume and resource limits

Check the frozen record with `sha256sum -c SHA256SUMS` from this directory.
The tools accept fresh output paths in the assigned scratch directory;
do not overwrite retained results. Short probes only: one CPU, 400 MiB
address space, 20-second external deadline. No long job was reserved or
launched; no job from this track remains running. Global and
verifier budgets are unchanged. No git mutation, installation, external
action, proof deletion or old-record edit.
