# Universal T6 and T7: completed certificate-backed chains

**PROVED, written composition using CERTIFIED finite statements and
Lean-checked capacity bounds. Independent audits and fresh proof replays
are complete.** This is not an end-to-end Lean selector theorem.

For n=6 or n=7, let L be any finite real set in general position, with
distinct x coordinates, no four-cap and no convex n-gon. Then T_n(L)
holds: at least one of the following exists.

1. A cup B meeting every convex (n-1)-subset of L, such that each selected
   vertex after the first ends a three-cap in L.
2. A partition L=B disjoint-union D into cups with |D|<=n-2.

The empty set is included. These are the precise predicates of the
[written equivalence](../structure2/low_split.md), the reviewed direct
encoder and its exact-containment implementation. All endpoint and
containment flags used negatively are defined in both directions.

## Complete size coverage

| Parameter | Sizes | Evidence |
|---|---|---|
| n=6 | left<=9 | Standard low join to a two-cup, total size<=11; explicit terminal coverage through11; exact equivalence |
| n=6 | left10,11 | Individual accepted formulas, complete independent reconstruction and fresh cake replays |
| n=6 | no larger L | Lean geometric capacity11 |
| n=7 | left<=10 | Standard low join to a three-cup, total size<=13; explicit terminal coverage through13; exact equivalence |
| n=7 | left11,12,13 | Individual direct formulas, complete independent reconstruction and fresh cake replays |
| n=7 | left14,15 | Individual compact formulas, complete independent reconstruction and fresh cake replays |
| n=7 | left16 | Original compact formula, complete independent reconstruction and fresh clean cake replay |
| n=7 | no larger L | Lean geometric capacity16 |

The canonical low joins are actual real configurations: a small right
cup can be placed strictly below all continued left secants. They have
no five-cap or n-gon. The explicit lower terminal theorems and exact
classification then give the left predicates. No claim at a single size
is extended to smaller ambient sets by monotonicity.

The n6 dependencies are [terminal12_audit](../terminal12_audit/VERIFY_TERMINAL12.md)
and [the independent left10/11 packet](../low_split_audit/n6/VERIFY_LOW6.md).
The n7 dependencies include [the through13 terminal replay](../exact_audit/replay13/README.md),
[the first four left-size replays](../low_split_audit/replay/README.md),
[left15](../low_split_audit/left15/VERIFY_LEFT15.md), and
[the original left16 replay](../low_split_audit/left16_replay/README.md).
The [left16 instance audit](../low_split_audit/left16_longcup/VERIFY_LONGCUP16.md)
reconstructs every original base row before separately studying its
augmentation. The accepted original proof does not use that augmentation.

Both [geometric capacity bounds](capacity_checks/README.md) are checked
specializations of the existing Baek theorem. They concern actual ordered
real configurations and the repository's convex-position predicate.
The five reported axiom sets contain only standard Lean axioms. The
finite encoders and their geometric soundness are independently reviewed
code and written proofs; they are not all formalized in Lean.

## The final left16 certificate

The original formula has128297 variables and903593 clauses. CaDiCaL2.1.3
returned UNSAT after2648.668s. Its4724116807-byte binary LRAT has:

* CNF SHA-256: `2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8`.
* LRAT SHA-256: `247f64c822609e878be490e059fb7e0c96e5e71fde0e265de74c7be36cd8dd42`.

The first heap550 check exhausted its heap. The unchanged proof passed
the parent's separately bounded heap2800 check in205.490s with stable
hashes. The first independent attempt printed acceptance but its optional
exit-time telemetry failed before the final receipt. That complete attempt
and recovered hashes are retained. The clean independent retry finished
at08:17:29 KST: exact `s VERIFIED UNSAT`, exit0, stable pre/post input,
proof, compressed-proof and checker hashes. Cake took134.537s, with
2870348KiB peak process RSS and zero swap.

The clean [retry receipt](../low_split_audit/left16_replay/data/retryB/result.json)
is the independent completion evidence. Wrapper failure is not silently
promoted to a clean pass. Large proofs remain in the recorded scratch
directories; no proof was deleted.

## Geometric consequences and their limits

For n=6 and n=7, every admissible low split with at least two left points
has a terminal-safe weak Delta. The hard branch maxcup(R)<=n-4 follows
from universal T_n and the arbitrary-right-block transfer. The branch
maxcup(R)=n-3 has the previously proved rank-level construction. The
critical maxcup(R)=n-2 branch forces singleton L and uses a selector on R.
Thus **a cardinality-minimal terminal counterexample has no low cut**;
an unconditional assertion about every low join is not inferred.

The [all-cap lemma](consequences/all_cap.md) gives a stronger conclusion
for that particular sign pattern: every admissible n6 or n7 set with an
all-cap cut is positive, with no minimality or size restriction. Its
non-singleton blocks and singleton-left case are directly constructive;
the singleton-right case uses the now-complete T_n theorem.

Combined with the older high/all-cup reductions, a minimal terminal
counterexample at n6 or n7 has none of the four constant crossing-sign
patterns. The exact12-point n6 and15-point n7 examples have no such cut
in the parent's independent fixed-coordinate check. This consistency
check is not a premise of the general reductions.

The frozen consequences packet predates the clean independent retry and
therefore records that review as pending. This closure record supersedes
that status without changing the historical packet. General weak Delta,
uniform-selection existence, the full14-point n7 terminal case and ES
bounds are not settled by the structured theorem.
