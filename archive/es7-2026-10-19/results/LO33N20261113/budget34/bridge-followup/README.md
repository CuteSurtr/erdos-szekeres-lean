# PROVED: residual population tradeoff from slice 19 alone

14 November 2026, bounded adversarial follow-up, completed before 10:40 KST.
**Verdict: the padding argument is sound.** Written deduction from existing
Lean geometric components, CERTIFIED coupled rows and an EXACT TREE;
not fully Lean-checked and unrefereed. The finalized `../bridge/` is unchanged.

## Statement

For every actual residual configuration R, let nF and nLo count its owners
in the frozen state families F and Lo. Then

    nF <= 64  OR  nLo <= 54.

Equivalently, `nF>=65` implies `nLo<=54`, and `nLo>=55` implies `nF<=64`.
**No N5 or N66 bound is used.** Neither the balanced population 187 nor
the baseline ES(8)<=309 chain is needed for this structural statement.

## Model, hypotheses and proof

An actual residual configuration consists of real points in general
position with distinct x-coordinates, no 6-cap, no convex octagon and no
incoming-6-cup/outgoing-5-cap junction. Its injective owner map has image O
in the 154-state catalog C. The families `F={f1>=5}` and `Lo={f1<=4}`
partition C, with sizes 84 and 70. For nonempty R, state 0 belongs to O
and lies in Lo. Its Boolean hole vector h satisfies every one of the
2,650 base inequalities and 812 frozen coupled inequalities.

Suppose for contradiction that `nF>=65` and `nLo>=55`. In particular R is
nonempty. Write `a=h(F)=84-nF<=19` and `b=h(Lo)=70-nLo<=15`. Select

- `19-a` currently occupied indices in F;
- `15-b` currently occupied indices in `Lo\{0}`.

These selections exist: respectively there are `84-a>=19-a` and
`69-b>=15-b` eligible indices, since `h_0=0`. Change just these entries
from 0 to 1 to obtain h'. Then h' is Boolean, `h'>=h` coordinatewise,
`h'_0=0`, `h'(F)=19`, `h'(Lo)=15` and `h'(C)=34`.

Every base/coupled row has the form `sum_(i in S_r) h_i >= d_r` with
positive unit coefficients. Thus its left side cannot decrease when h is
replaced by h'. The two slice capacity rows hold with equality. Hence h'
satisfies exactly the finite system excluded by the independently checked
budget-34 slice-19 tree. Its only pending branch, state 0 missing, is
inapplicable. This is a contradiction. Empty R satisfies the statement
trivially. **QED.**

**Realizability boundary.** No new point set, new owner map or reassignment
of ranks is claimed for h'. The actual geometric configuration supplies
the initial row-satisfying h. The subsequent argument takes place entirely
in the Boolean covering system. The tree excludes every Boolean vector
satisfying that system, including unrealizable vectors. We do not pad a
geometric CNF assignment or assume that its auxiliary variables are monotone.

## Dependencies and method

1. **PROVED, existing Lean components:** actual residual owner injectivity,
   catalog cardinality, population/holes complement, validity of all 2,650
   rows, and nonempty state-0 occupancy. Sources are listed in
   [the preserved bridge](../bridge/README.md), sections 2 and 4.
2. **PROVED written geometric soundness plus CERTIFIED finite inputs:**
   the 812 coupled rows. The [pool receipt](../audit/pool_summary.json)
   records 812 independent encoder reconstructions and 812 fresh retained
   LRAT acceptances, completed 10:12:14 KST. Geometric soundness is inherited
   from [VERIFY309, link (c)](../../../VERIFY309N20261113/README.md).
3. **EXACT TREE:** [slice-19 receipt](../audit/s19-summary.json), budget 34,
   capacities F19/Lo15, all 3,643 contexts, 1,658,483 nodes, 829,242 leaves,
   minimum margin 1, sole pending branch state 0 missing; completed
   10:16:01 KST. Its inputs are exactly the 2,650 base rows, two capacity
   rows and 812 coupled rows. Their extra-row SHA-256 is
   `770d276db7b51d369e9a6fa1b9f36abb15d2539d224a71b19bf5fa738cbd9983`.

Read these receipts and independently inspected the small frozen row
files, using one CPU and AS150MiB. No solver, Lean build, certificate
audit or tree replay was run. The deduction does not inherit the deleted
N5 arithmetic proofs, because N5 is absent from its dependencies.

## Consequences and limits

Given **additional independently justified** capacities `nF<=c5` and
`nLo<=c66`, the disjunction yields

    |R| <= max(64+c66, 54+c5).

Indeed its first case bounds the sum by `64+c66`, and its second by
`c5+54`. With N5<=65 and a future N66<=55, this is 119, and the existing
balanced 187/composition gives ES(8)<=308. That numerical corollary still
uses N5 and its historical proof-retention caveat, as well as the
unproved antecedent N66<=55. Current 65/56 only gives residual 120.
**No unconditional N66<=55 or ES(8)<=308 result follows here.**

## Controls, files and hashes

[check_inputs.py](tools/check_inputs.py) independently checks the row
directions, nonnegative integer demands, valid distinct support indices,
exact family partition, state-0 location, capacities and receipt/input
hash agreement. It does not check certificates or replay the tree.
[input-check.json](data/input-check.json) records the results and input
hashes; `SHA256SUMS` pins this follow-up. Nonnegative demands were checked;
monotonicity itself follows from the positive coefficients.

## What remains and resume

No mathematical gap was found in this standalone deduction. The stated
computer-assisted dependencies retain their existing trust boundaries.
The parent can cite this tradeoff without a N5/N66 hypothesis; a numerical
ES improvement needs the additional capacity or slice-20 work already
identified. No follow-up compute is needed.
