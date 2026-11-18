# Independent review of the compact weak-Delta encoder

**Written encoding equivalence confirmed; implementation controls COMPUTED.**
No soundness gap was found in the reviewed final source. Both delivered
m16 CNFs and variable maps were reproduced byte-for-byte from an independent
build. This is an encoder audit, not a certificate of either frontier
instance or a proof of the all-size conjecture.

Reviewed source: `../compact/compact_cnf.cpp`, SHA-256
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.
The arguments below were derived from the clauses and independently checked;
the parent/author's conclusions and their control scripts were not used as
proof or executed by this audit. Coordinate files were used only as inputs.

## Orientation, full convexity flags and the n-gon exclusion

For an ordered four-set write its packet as (a,b,c,d). The eight ternary
clauses forbid both alternating patterns in every three-entry subsequence.
A binary sequence with two changes has an alternating three-subsequence;
one with at most one change has none. Thus these clauses exactly impose the
intended packet condition.

The four forward Q4 clauses force a=b and c=d. The four reverse clauses
force Q4 whenever a=d or b differs from c. Under the packet condition,
a=d forces all four signs equal; b differing from c forces a=b and c=d.
Conversely, if a=b and c=d, either the two pairs agree (a=d), or they differ
(b differs from c). Hence Q4 is equivalent, not merely an implication, to
the four-point convexity predicate. In particular a convex set cannot be
hidden by assigning its Q flag false. All 32 assignments of the four signs
and Q were independently checked against the emitted clause patterns.

The consecutive-sign no-five-cap clause is exact. Equal consecutive triple
signs propagate through an ordered four-vertex packet, since its first and
last entries agree. Deleting an internal vertex therefore preserves the
consecutive-sign property. Repeated deletion gives the same sign on every
triple. This establishes the all-size chain fact used at sizes four and
five. Independently, all 1,024 sign assignments on five points were checked;
the 62 valid signotopes satisfy the claimed equivalence.

For larger S, convexity means every four-subset is convex. Choose any five
distinct vertices E in S. Every four-subset T omits at least one vertex
v in E, hence T lies in S minus v. Therefore

`Q(S) <=> AND_{v in E} Q(S minus v)`.

Both directions follow directly: convexity descends to subsets, and the
children cover every four-subset. The code's `children` retains the original
mask s and deletes a single different bit for each child. Each child has
smaller size; all required child flags have already been allocated.
The five binary forward clauses and one reverse clause implement the full
conjunction. By induction every Q flag is exact.

An n-set is convex iff all five selected (n-1)-children are convex, so the
single clause of their negated Q flags excludes exactly that n-gon. Its
soundness depends on the reverse Q implications just verified. The `direct`
alternative uses all Q4 subsets and is equivalent by the same definition.
For n=5 the children are Q4 directly. If m<n, there is no n-subset and no
n-gon clause. These boundary cases cause no missing-child access.

For actual general-position points, the four-point equalities characterize
convex quadrilaterals. A finite set with a point inside its convex hull has
a point inside a triangle of other points, hence a nonconvex four-subset.
Thus the four-subset definition agrees with ordinary convex position.

## Containment DAGs and canonical assignments

A four-cap flag implies the two negative consecutive signs, which force
all four triple signs negative. For a larger S, a true A(S) requires a true
child obtained by deleting one of five selected vertices. Descending in
cardinality eventually reaches a genuine four-cap. Conversely, any actual
four-cap avoids one of those five vertices. Setting A to actual cap
containment satisfies every implication simultaneously.

B at size n-1 is the exact Q flag. At larger sizes a true B selects one of
n deletion children. An actual (n-1)-target avoids at least one of those
n vertices, so the same decreasing-cardinality proof gives soundness and
a canonical containment assignment. The optional `exact` mode adds child
implies parent clauses, which actual containment also satisfies. Neither
mode changes the existential projection onto the orientation variables.

Every needed cap child has size at least four and is within its parent's
upper bound. Every needed target child has size at least n-1 and is within
its parent's upper bound. Smaller masks are literal false constants, never
unconstrained variables. Integer mask deletion strictly decreases the mask,
so allocation by increasing mask works for A/B. No cycle or missing leaf
was found. All masks fit the uint32 type in the accepted m<=16 range.

## Why the reduced size interval is sufficient

Let a working Delta be four-cap-free and intersect every target. With a
nonempty retained interval `3 <= |Delta| <= m-n+2`:

- If its size is below three, enlarge it to three. The enlarged set is
  still four-cap-free because it has only three vertices, and it still
  intersects every target because it contains the original Delta.
- If its size exceeds m-n+2, shrink it to that size. Four-cap-freeness is
  hereditary. The complement now has size n-2 and cannot contain a target
  of size n-1, so the smaller set still works.

Thus any working Delta yields one in the retained interval. Conversely,
a working retained Delta is already a working Delta. The existence
properties are equivalent, and their negations are equivalent too.

If the interval is empty, m<n+1. Since m>=4, choose any three points; they
are cap-free and their complement has fewer than n-1 vertices. A working
Delta always exists, so an empty clause in the counterexample CNF is
correct. At m=n+1 the interval consists of size three and its pool clauses
are empty for the same reason. No minimum-counterexample assumption is used.

Only A sizes up to m-n+2 and B sizes up to m-3 are needed. Complementary
retained masks lie within these bounds, and every descendant remains within
them. At m16 these are A<=11 for n7, A<=10 for n8, and B<=13 in both cases.

A full CNF model supplies real failure witnesses for all retained Delta,
and the range argument excludes all working Delta. Conversely, a valid
signotope with no working Delta has the canonical assignment: exact Q,
actual A/B containment, and its orientation signs. Every premise,
definition and retained pool clause then holds. This proves equivalence
for each accepted m,n. `--base` omits the counterexample requirement, and
`--fix-signs` produces a conditional instance; neither should be presented
as the unconditioned full formula.

## Independent implementation evidence

[`audit_compact.py`](audit_compact.py) compiled the reviewed source with the
system C++ compiler, entirely under the audit scratch directory. Its
geometric reference uses this audit's Python-integer hulls and direct scans,
not the parent checker or subset transforms. It checks variable-map domains,
evaluates every emitted clause under exact semantic values, and compares
each retained failure clause with that mask's direct geometric outcome.

| Coordinate control | Clauses checked | Four-caps | Targets | All working Delta | False retained pool clauses |
|---|---:|---:|---:|---:|---:|
| Actual real15, n6 | 140,621 | 80 | 216 | 353 | 353 |
| Real16, n7 | 296,714 | 71 | 279 | 7,835 | 7,835 |
| Real16 targeted fixture, n8 | 346,608 | 280 | 168 | 8,439 | 8,404 |

All three have no five-cap and no forbidden n-gon. Every non-pool clause
is true. Precisely the failure clauses of genuinely working retained
Delta are false. In the n8 control, the 35 working masks outside the
interval were independently converted to working masks inside it. This
exercises the range reduction rather than merely checking total counts.

The independent binary produced exactly the delivered n7/m16 and n8/m16
CNFs and maps. Full CNF hashes:

- n7: `642c2e5d94dc2c98a1bc72a49e0976207762cb0a2e952167ff8135846a64ca07`
- n8: `37e8a9ba5ddec0907580ec0f846ba7dd65846d1ef71c9573db824880d3b18a07`

The matching variable counts are 127,584 and 123,216. Their paths are
`/home/jay/research/data/delta3-codex-20261113/resume/compact/n{7,8}m16-final.cnf`.
This binds the actual scheduled inputs to the reviewed source; it says
nothing about the outcome of the parent's active solver jobs.

A separate nine-point real control exercised all eight combinations of
recurrence/direct convexity, reduced/all pools, and witness/exact
containment. For each individual retained failure clause, with coordinates'
orientation signs fixed and other pool clauses omitted, an existential
auxiliary-variable query agreed with direct subset geometry: **3,392
queries, zero mismatches**. These small finder results are COMPUTED only.
Four small m<n controls also passed: (4,5),(4,8),(5,8),(6,7).

The Boolean/cover controls additionally checked 32 Q4 assignments, all 62
five-point signotopes, and 3,906 four-subset/deletion-cover incidences. Finite
controls support the source implementation; they are not substitutes for
the written arguments above.

Files: [algebra](results/compact-algebra.json), [tiny cases](results/compact-tiny.json),
[real15](results/compact-real15.json), [real n7](results/compact-real7.json),
[real n8](results/compact-real8.json), and [build](results/compact-build.json).
Each records source/checker hashes and limits. The largest checker RSS was
39,956 KiB; individual checks took at most 1.526 seconds. Every invocation
had AS400 MiB, one CPU and numerical-library thread, an 18-second CPU limit
and a 20-second external SIGKILL limit. No long job, unit, proof checker,
parent-file edit or installation was performed.

Reproduce with the research venv Python and `-B`, separately running
`audit_compact.py build`, `algebra`, `tiny`, `real7`, `real8`, and `real15`,
each under `timeout -s KILL 20s`. Large generated files stay in
`/home/jay/research/data/delta3-codex-20261113/resume/audit/compact`.

Remaining claim boundary: a finder UNSAT still needs the parent's fresh
CaDiCaL LRAT and the exact cake acceptance line for that matching formula.
A SAT candidate still needs independent orientation checking and exact
realization before it can refute the real-point statement.
