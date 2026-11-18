# Structured low-split selection — universal T6 and T7 closed

**PROVED written reduction and independently reviewed encoders; CERTIFIED
finite formula results with the independent replays listed below.** This record keeps
the new restricted search separate from the unrestricted n7/m14 search.
**T6(L) and T7(L) are now proved for every admissible left set**, by their finite
certificates and checked geometric capacity. No general Delta theorem or
unconditional statement about every low join is claimed.
The final [closure record](CLOSURE.md) gives the complete size coverage,
independent replays, final left16 hashes and precise consequences.

## The smaller problem

Fix n in {6,7,8}. Let L be a real x-ordered general-position set with no
four-cap and no convex n-gon. A low split U=L union R has every LLR triple
a cap and every LRR triple a cup. First take R to be an (n-4)-point cup.
Such a split is always realizable: place a small upward-curving right block
strictly below every continued L secant and below all L heights, sufficiently
far to the right. Exact coordinates must be checked if a SAT model is used.

The mixed convex subsets are exactly an L cap plus an R cup. Thus U has no
five-cap and no n-gon: its mixed cap size is at most four and its mixed
convex size at most 3+(n-4)=n-1. Internal exclusions also hold.

Write End3(b) when some L three-cap ends at b. There are exactly two ways
for a terminal-safe weak Delta in U to exist:

1. **A selected R point.** There is a cup B in L meeting every internal
   (n-1)-gon, and every selected vertex b after the first has End3(b).
2. **No selected R point.** L has a partition into a cup B and a cup C,
   where |C|<=n-2. Absence of an n-gon already gives |B|<=n-1.

Here is the equivalence. Every cap triple inside L lacks an ambient
four-cap on its terminal pair, since no four-cap lies in L and R is later.
Therefore the selected L part B must be a cup. A selected mixed cap is
a<b<r with a,b in L; its terminal pair (b,r) has an ambient four-cap
exactly when End3(b) holds. Mixed triples with two R points are cups.
Every mixed target uses an L three-cap and all n-4 R points, so any
selected R point hits it. If no R point is selected, the complement of B
must have no L three-cap, hence must be a cup; it must also have at most
n-2 points to avoid an internal target. These conditions are sufficient
as well, including absence of selected four-caps.

For n=7, R has only three points. At |L|=11, option 2 is a six-cup/five-cup
partition. At |L|>=12 it is impossible by cardinality. This reduces a
structured 14-point search to only 11 unknown geometric vertices.

## Why the same left lemma would handle larger right blocks

Suppose instead R is arbitrary with maximum cup length d<=n-4, while U
still satisfies the low-split signs, no five-cap and no n-gon. There is
no internal R target, since its maximum polygon size is at most d+2<=n-2.

If option 1 holds in L, take B together with the cup-ending-rank-d level
in R. The rank level is terminal-safe internally and meets every maximum
R cup. All possible mixed targets are hit; selected mixed cap triples
are protected by End3 in L. If option 2 holds, take B alone: the remaining
L cup contains no three-cap and at most n-2 points, so neither an internal
L target nor a mixed target can avoid B. Thus either left alternative
gives a terminal-safe Delta for every such R.

The earlier written [low-split partial reduction](../structure2/low_split.md)
handles the other cup-length cases and explains the remaining assumptions.
The completed universal T6/T7 statements close this hard branch for those
parameters. The other cup-length cases retain their stated hypotheses.

## Direct CNF

[low_split_cnf.cpp](../low_split_cnf.cpp) uses the audited compact geometric
base, adds no-four-cap clauses, and defines every End3 vertex flag by an
exact OR of negative triple orientations ending there.

For every B with 0<=|B|<=m-n+2, it states failure of option 1 as one clause:
some triple of B is a cap, or some nonfirst selected vertex lacks End3,
or the complement contains an exact convex (n-1)-set. This range is
complete: a larger working B can be thinned to size m-n+2, preserving
its cup and End3 conditions while leaving a complement of size n-2.

For every partition with |B|<=n-1 and |L minus B|<=n-2, one clause states
that some triple of one part is a cap. These are precisely the failures
of option 2. When no partition meets the size bounds, there are no such
clauses; an empty family is not replaced by an empty clause.

Every real failure of both alternatives has a canonical satisfying
assignment. Therefore an accepted UNSAT certificate, after encoder audit,
establishes the left lemma at the encoded size. An abstract SAT model
still needs exact realization and a separate fixed-instance audit.

## Compact CNF

[low_split_compact.cpp](../low_split_compact.cpp) expresses exactly the same
predicate using exact containment flags. For a two-set {a,b}, its bad flag
is the literal NOT End3(b). For a triple a<b<c it is the OR of Cap(a,b,c),
NOT End3(b), and NOT End3(c). Larger sets use four deletion children:
each forbidden witness has size at most three and misses one of those
four vertices. All reverse child implications are included.

Target containment similarly uses exact (n-1)-gon leaves and n deletion
children. The failure row is then just Bad(B) OR Target(L minus B). The
End3 and two-cup-partition clauses are unchanged in meaning. The direct
and compact formulas need independent row and semantic comparisons;
sharing their intended predicate is not by itself a successful audit.

## Current formula results

| n | Left size | Standard full size | Encoding | Current status |
|---|---:|---:|---|---|
| 7 | 11 | 14 | direct | CERTIFIED; independent audit and fresh replay PASS |
| 7 | 12 | 15 | direct | CERTIFIED; independent audit and fresh replay PASS |
| 7 | 13 | 16 | direct | CERTIFIED; independent audit and fresh replay PASS |
| 7 | 14 | 17 | compact exact | CERTIFIED at cake450; independent audit and fresh replay PASS |
| 7 | 15 | 18 | compact exact | CERTIFIED at cake1400; independent audit and fresh replay PASS |
| 7 | 16 | 19 | compact exact | CERTIFIED at cake2800; full independent instance audit and clean fresh replay PASS |
| 6 | 8 | 10 | direct | CERTIFIED formula UNSAT; audit pending |
| 6 | 10 | 12 | direct | CERTIFIED; independent audit and fresh replay PASS |
| 6 | 11 | 13 | direct | CERTIFIED; independent audit and fresh replay PASS |

Receipts and retained raw/compressed proofs are in scratch directories
`low11-n7-a`, `low12-n7-a`, `low13-n7-a`, `low14-n7-b`, `low15-n7-a`,
`low15-replay-b`, `low16-n7-a`, `low16-replay-a`, `low8-n6-a`,
`low10-n6-a`, and `low11-n6-a`.
Only cake_lpr's exact `s VERIFIED UNSAT` line is accepted. Full commands,
binary hashes, file hashes, time and compression roundtrips are in each
`result.json`. A finite certificate at one left size does not establish
all smaller sizes by monotonicity.

## Resources and retained verification history

The direct controls used one CPU and AS300 MiB or AS150 MiB for the tiny
n6 case. The compact m14 estimate used 593,588 literals, approximately
85–142 MiB by the memory policy, plus buffers under AS300 MiB.
`nov13c-vfy-delta6-low14` has CPUQuota100%, MemoryMax500M, no swap and
RuntimeMaxSec2400. It replaces the parent's short-check reservation;
other parent probes are temporarily capped at AS150 MiB. Large proof
cache is released periodically by the binary-LRAT driver.

The independent [formula audit](../low_split_audit/VERIFY_LOW_SPLIT.md)
is complete. It reconstructed all four supplied formulas and maps, and
checked over one million Boolean cases and248448 full selectors on real
low joins. The written [theory review](../structure2/low_split.md) is also
complete. Both records are frozen; fresh proof replays have their own
[append-only packet](../low_split_audit/replay/README.md).

The initial compact14 proof check exhausted its128MiB CakeML heap. The
same624474740-byte proof passed the separately bounded450MiB check in
27.155 seconds, with stable input/proof hashes; both outcomes are retained.
Scratch `low14-replay-a/result.json` records the accepted verdict.

Through-left10 coverage follows from a valid standard low join to a
three-cup, of total size at most13, the explicit through13 terminal
theorem, and the exact classification. Separate accepted formulas handle
left11–16. Ambient-size monotonicity is not used. The checked capacity
excludes larger left sets; left15 and left16 audits/replays are complete.
The14-point full-set cut search lists its
own dependencies in [allcuts14/README.md](../allcuts14/README.md).

The left15 solver returned UNSAT after1122.796s. Its2,526,967,446-byte
binary LRAT exhausted cake heaps550 and900; those clean checker failures
remain recorded. The unchanged proof passed heap1400 in133.683s under
AS1650 and MemoryMax2200M. Input SHA-256:
`793063f5c7c5208c16ce038c63659878adee4eb049546d775d65c5a18ed60418`;
proof SHA-256:
`f86789033376814b7a36ea4bbc26e5a6007e66168a1fef4e38d09a5f6cca2f7c`.
The independent [left15 packet](../low_split_audit/left15/VERIFY_LEFT15.md)
now passes the full new instance reconstruction and a fresh73.805s proof
replay. Its separate frozen record extends the explicit coverage to left15.

The independent [n6 packet](../low_split_audit/n6/VERIFY_LOW6.md) closes
T6(L) through left11: left<=9 follows by a standard two-cup join to a
set of at most11 points; left10 and11 have individual certificates.
Its12288 full-selector controls and fresh proofs pass. The old left8
formula is redundant for this deduction and does not replace its explicit
smaller-size coverage. Removing the left-size bound needs the separately
checked capacity no-four-cap/no-six-gon => size<=11. Both specializations, [Capacity11.lean](Capacity11.lean) and
[Capacity16.lean](Capacity16.lean), have now passed their
[bounded kernel checks](capacity_checks/README.md) with five standard-only
axiom reports. Thus universal T6(L) is closed. The written transfer gives
terminal selection for every admissible low join with at least two left
points; the singleton-left critical case still uses a selector on R.
Consequently a cardinality-minimal n6 terminal counterexample has no low
cut. This composition is a written proof using certified finite inputs
and a Lean capacity theorem, not a fully formalized selector theorem.

The original left16 proof has now passed both parent and clean independent
heap2800 replays, closing universal T7 in the same manner. Its complete
instance audit is in `../low_split_audit/left16_longcup/`; the proof uses
the original base, without its separate long-cup augmentation. The clean
independent receipt is `../low_split_audit/left16_replay/data/retryB/result.json`.
The first wrapper's telemetry failure is preserved and superseded by
that successful retry. See [CLOSURE.md](CLOSURE.md) for the full chain.
