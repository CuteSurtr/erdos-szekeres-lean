# Independent four-cut formula and projection audit — PASS

**COMPUTED:** streamed independent reconstruction matches every byte and
all48 added clauses. **PROVED (written):** real n7/m14 terminal failure
projects to the strengthened formula with the dependencies below. This
does not assert equivalence on arbitrary Boolean assignments. This packet
contains no solver result or accepted proof for the fourcuts formula.

## Rows and base

Let t(a,b,c) mean that the increasing-x triple is a cup. For a cut k use
L=[0,k), R=[k,14). The required signs are:

| Family | LLR | LRR |
|---|---|---|
| high | cup | cap |
| low | cap | cup |
| all_cup | cup | cup |
| all_cap | cap | cap |

The clause contains exactly the negation of every required mixed sign.
It is false iff the entire cut pattern holds; it is true iff some mixed
sign violates that pattern. Pure triples are absent. Our row builder
counts how many vertices are left of the cut. A separate truth evaluator
quantifies over LL times R and L times RR. Neither imports the producer.

The full map hash is pinned to the earlier independent exact-base audit;
all32086 sequential map IDs and364 orientation IDs are read here. Every
one of231613 base rows,623240 literals and4104153 body bytes is retained
unchanged. There are no new variables or geometric premises hidden in
the base. The rebuilt full SHA256 equals the actual output SHA256:
`3c6c1f83e2cf426ca13eb2e9ba7e363a1da42f1138cc3b9503c57601678e5788`.

Each family has13 provenance entries and2730 literals before deduplication.
Each cut width is6k(14-k). The only repeated patterns are all_cup cut1=
low cut1, all_cup cut13=high cut13, all_cap cut1=high cut1, all_cap cut13=
low cut13. Thus52 entries produce48 clauses and10608 literals. The first37
rows are byte-identical to the frozen three-family formula; the new rows
are the11 interior all-cap cuts, with2574 literals. Final totals:
32086 variables,231661 clauses,633848 literals. Every producer receipt
entry, repeated index, count and input/output/source hash agrees.

Base SHA256: `5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4`.
Map SHA256: `b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e`.
Producer SHA256: `964b349651920e44bafd66ea478a44e77d53bd1a8e2d616375c7c1061570114b`.

## Independent all-cap argument

Let U=L disjoint-union R be x-separated, GP, without a five-cap or convex
n-gon, n>=5, and all mixed triples caps. Suppose both blocks have at least
two points. An internal cap triple in either block, together with any two
points of the other, would be a five-cap: every triple of those five points
is either that internal cap or a mixed cap. Thus both blocks are cups and
each has size at most n-1.

For every l in L choose A={l} union R. There is no four-cap in A: any four
selected points contain three R points, whose triple is a cup. Every
selected cap triple is l,b,c with b,c in R. Any two ambient L points u<v
together with b,c form a four-cap, all four triples crossing the cut.
Its final pair is b,c, as required for terminal protection. The ambient
support need not lie in A or contain l.

Every target meeting R is hit. A remaining (n-1)-point target lies in L;
since |L|<=n-1, it equals L and contains l. This proves terminal selection
without a smaller-size or capacity premise. In the particular n7,m14
case, two nontrivial cup blocks would total at most12 points, so these11
interior patterns are already impossible under the ambient hypotheses.
The constructive proof also confirms their intended general meaning.

If L is a singleton, choose all of R. R has no four-cap (otherwise the
left point completes a five-cap), and each R cap triple is protected by
prefixing that left point. Every target has at least4 points and meets R.
This is directly positive and agrees with the repeated high cut1 row.

If R={r}, L has no four-cap. T_n(L) suffices. For Option1 choose B union
{r}; B is a cup, hits every internal target, and every selected pair a<b
in B has End3_L(b), giving u<v<b<r as a protecting four-cap for a,b,r.
For Option2 L=B union D into cups, |D|<=n-2, choose B. D has no internal
(n-1)-target. D union {r} has no mixed convex subset of size>=4: an
internal D triple is a cup while all three triples with r are caps, so
its middle D point is inside the other three. This covers n>=5. For m14
only T7 at left13 is needed, already independently audited and freshly
certified before this work. This agrees with the repeated low cut13 row.

## Earlier families and canonical projection

The frozen [three-family audit](../allcuts14_audit/VERIFY_ALLCUTS14.md)
provides the full high, low and all-mixed-cup reductions for14, including
the critical singleton cases. Its explicit dependencies are terminal
existence through11, separately at12, separately exact13; T7 through
left10 by standard low joins with a three-cup; and individual certified
left11,12,13 formulas. No ambient-size monotonicity is used. This audit
checks the exact old37-row prefix and pins that frozen manifest.

For any alleged real14 terminal counterexample, use the independently
audited exact base's canonical orientation, convexity, terminal-cap and
containment flags. The earlier reductions rule out its high/low/all-cup
patterns. The all-cap proof above rules out its all-cap patterns. Hence
every appended clause is true. This is precisely the real-counterexample
projection needed if a matching accepted proof later arrives. It does
not require the newly closed all-left T7 theorem, only its earlier left13
instance. It does not use the separate rooted lemma.

## Controls and limits

Boolean controls cover52 canonical patterns,10920 mixed flips,8008 pure
flips,16576 exhaustive assignment/cut pairs at m4/5, and52 each of omitted-
literal and wrong-polarity mutants. Exact integer controls construct50
two-cup all-cap joins for n5,6,7, and two admissible14-point singleton-end
joins from coordinates of our earlier no-four-cap left13 control. Every
fixture is checked for GP/no5cap/no n-gon. Every possible choice of l in
the50 nontrivial fixtures gives a checked selector; together with the two
singleton constructions,185 selectors pass. All52 actual cut predicates
are checked on each14-point fixture, for104 comparisons. Data retain each
coordinate, selected set and ambient protecting four-cap.

Only our frozen independent integer determinant/strict triangle-containment
geometry is reused read-only, with its source hash checked against its
frozen manifest. Parent expected selectors and control outputs are not
imported. These are exact controls, not order-type exhaustion. The all-cap
and rooted notes are snapshotted, with the rooted note not used as a premise.

The first control run reached CPU19 in the frozen helper's thinning loop
on m4,n7 (negative m-n+2 bound). Its source and logs remain in data/attemptA.
The independent final driver directly checks the requested selectors and
all ambient supports, omitting unrelated thinning. The complete final run
passes in0.504s, AS300MiB, one CPU, wall20/CPU19, no compile or cake. Input
hashes are stable. No finite14, weak-Delta, ES or minimality conclusion is
asserted merely from these clause audits.
