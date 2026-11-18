# Delta continuation, 13–14 November 2026

The later pass requested at 00:55 KST is complete in
[selection/README.md](selection/README.md). It adds stronger written
selection results, independently replayed finite rooted certificates, and
certified counterexamples to stronger repair/selection rules. This page
retains the preceding pass's findings and resource snapshot.

**This pass is complete. Weak D(5,7) and D(5,8) remain open.** There are new
written extension theorems, exact obstructions to proposed proof strategies,
and one conditional cup-side certificate. Both 16-point search methods
reached their time limits UNKNOWN. No larger universal Delta frontier or
new numerical ES bound follows from this continuation.

Here weak D(5,n) asks: if S has no five-cap and no convex n-gon, does S have a
four-cap-free subset meeting every convex (n−1)-gon? Real sets have distinct
x-coordinates and no collinear triples. The cup-side strengthening requires
meeting the lower chain, including endpoints, of each target polygon. The
parent record already refutes that strengthening at n=6; it is not assumed
in the new weak-Delta arguments.

PROVED below means a written mathematical argument, CERTIFIED requires the
literal cake_lpr line `s VERIFIED UNSAT` for the stated CNF/LRAT pair, and
COMPUTED means an exact finite calculation. Numerical realization searches
are HEURISTIC until all integer determinants pass. Nothing new here is
Lean-checked or refereed, and no literature-priority claim is made.

## Findings and exact scope

| Finding | Label and outcome | Evidence |
|---|---|---|
| Extend a chosen weak Delta at a rightmost point when its three-cap terminal-line envelope is dominated by the ambient four-cap envelope | PROVED sufficient condition; favorable Delta existence remains open | [Weak theory](weak_theory/theory.md) |
| Repair an arbitrary deletion solution only by dropping its selected points and optionally adding the new point | Refuted by COMPUTED real examples at 9 points for n7 and 10 for n8; PROVED sharp size n+2 and a lift to every n≥7 | [Theory and exact checks](weak_theory/README.md) |
| Every inclusion-maximal four-cap-free subset is a weak Delta | Refuted by a COMPUTED real 12-point example at n7 | [Independent audit](audit/VERIFY_MAXIMAL.md) |
| Weak n8 for a five-cap-free extension of a hexagon-free set by at most five points | PROVED, independently reviewed; no octagon-free premise needed | [Lift lemma](lift/MODEL.md), [review](audit/VERIFY_EMBEDDING.md) |
| One-point cup-side n7 counterexample extending the fixed old 15-point order type, in any x-order gap | CERTIFIED impossible, all 16 insertion gaps covered | [Lift record](lift/README.md) |
| Every valid 16-point abstract configuration has a five-point transversal of its hexagons | Refuted by an exact COMPUTED abstract witness; real realizability unresolved | [Limited sufficient-condition probe](pool/TRANSVERSAL.md) |

The real 12-point example has no five-cap or heptagon, 25 four-caps and
54 hexagons. Its specified red set is maximal but misses a hexagon; the
singleton {8} meets every hexagon. There are 1,526 working weak Deltas.
Likewise, both sharp repair examples have a working full Delta {0}. These
are failures of universal choice/repair rules, not counterexamples to weak
Delta. Global minimality is not asserted for the 12-point example.

For the positive extension theorem, write U=S−r and r=(X,Y) rightmost, and
let F_j(V;X) be the greatest height at X of a line through the terminal pair
of a j-cap in V, with empty maximum −infinity. If A is a weak Delta in U,
S has no five-cap, and F_3(A;X)≤F_4(U;X), then A∪{r} is a weak Delta in S.
Five-cap-freeness gives Y>F_4(U;X), so no new four-cap appears. Existing
polygons retain their hits; every new polygon contains r. The remaining
inductive gap is selecting such a favorable A, or allowing a more general
repair that also selects previously unselected old points.

## Completed searches and certificates

| Instance / method | Solver limit | Outcome |
|---|---:|---|
| Weak n7, m16, batched subset pool | 900 s | COMPUTED UNKNOWN; 3 intermediate models, 767 subset clauses |
| Weak n8, m16, batched subset pool | 900 s | COMPUTED UNKNOWN; 2 intermediate models, 511 subset clauses |
| Weak n7, m16, compact universal CNF | 900 s | COMPUTED UNKNOWN |
| Weak n8, m16, compact universal CNF | 900 s | COMPUTED UNKNOWN |
| Cup n7, fixed old15 + one point, all gaps | 20 s allowance | CERTIFIED; solve 0.364 s, cake 0.564 s |
| Cup n7, fixed old15 + two points, all gaps | 4 s probe | COMPUTED UNKNOWN; no long run launched |
| Weak n6, m8, tiny pool control | 12 s allowance | CERTIFIED after fresh proof and explicit-stack checker |

The compact CNFs use exact recursive convexity flags, a justified reduced
Delta-size range and one-way containment witnesses. Independent review
reproduced both scheduled CNFs byte-for-byte and checked canonical real
assignments plus 3,392 projected clause queries. See
[VERIFY_COMPACT.md](audit/VERIFY_COMPACT.md). The pool formulas are literal
subformulas of the earlier audited universal encoder. Their final exported
formulas and masks passed [independent review](audit/VERIFY_POOL.md).

| Certified one-insertion artifact | SHA-256 |
|---|---|
| Full CNF, 453,999 clauses / 142,767 variables | `9138cb5807ca6d208e2cb3f1519b0060026d495e295e9388c1f45bc35284d233` |
| Fresh parent LRAT, 2,338,806 bytes | `41978f2d53df04787a34aba49a119675079d95b63bb5f5350cef7541289467f1` |

The new embedding family was independently reviewed and its complete CNF
regenerated. The parent performed the fresh solve and cake check; the separate
reviewer checked the proof hashes and log rather than replaying cake again.
This is a conditional statement about a fixed old order type, not universal
cup-side n7 on 16 points. It does not exclude two or more insertions.

Compact input hashes and full results are retained in
[n7](data/compact-n7m16/result.json) and [n8](data/compact-n8m16/result.json).
UNKNOWN traces of 3,650,642,732 and 3,451,029,679 bytes are retained externally,
alongside compressed copies whose decompressed SHA-256 hashes were checked.
They are incomplete traces, not certificates. No identical timed-out run
was restarted.

## Independent audit and preserved failures

[The audit index](audit/README.md) records the separate reviews of the pool,
maximal-set clauses, compact encoder, embedding family and five-insertion
lemma. The weak-theory track has two distinct integer implementations and
parent review, but does not describe its second implementation as a separate
person's review. The final parent transversal probe is outside that audit;
its independent-from-encoder checker is `pool/check_transversal.py`.

The original frozen pool driver has two small-instance bugs: empty-array
dimensions and acceptance of batch=0. Neither is exercised by the completed
m16 runs. `pool/batch_pool_v2.py` fixes them and snapshots source bytes at
startup. Six edge controls pass; the independent reviewer checked the diff.
The original executed source and its hashes remain unchanged.

The repository proof helper initially omitted a CakeML stack bound and
failed safely to allocate under the tiny control's address-space cap.
Explicit heap128/stack32 accepted the same proof. The failed log is retained;
`pool/run_cnf.py` bounds both heap and stack for parent-run checks.
This was not an OOM kill. Rejected geometric constructions, collinear
controls, UNKNOWN probes and unsuccessful realization attempts are retained
and described in their respective subdirectories.

## Separate N66 follow-up and ES309 consequence

The background N66≤56 certificate arrived at 23:43 KST. The
[independent follow-up](../../VERIFY309N20261113/followup56/README.md) now
confirms it: all 319,611 trimmed clauses and all 6,775 rows were justified,
the retained main proof passed a fresh cake replay, and all four additional
supporting CNFs were independently regenerated and freshly certified.
The extra 600-second attempt to generate another main proof ended UNKNOWN;
it is not part of the evidence for the confirmed bound.

[ES309](../../ES309N20261113/README.md) now gives a simpler preferred chain:
Lemma A yields h(Lo)≥14; at total 33 holes only slices 18 and 19 remain, and
both use the 2,650 Lean rows with their slice capacities. This eliminates
slice 20 and its residual coupled-owner encoder from that chain. The bound
remains ES(8)≤309, with written soundness, certified propositional components
and exact tree replays outside Lean. The fully Lean-checked bound remains 310.

## Resources, artifacts and continuation

All new scheduled units finished by 00:32:02 KST. Each used one CPU, no swap,
a finite systemd deadline and an address-space limit below 80% of its launch
MemoryMax. The largest simultaneous AS reservation for long units was
5700 MiB, below the 6000-MiB verifier budget; unrelated jobs counted toward
the 16-thread / 24-GB research caps. No new unit was stopped by the guard.
The guard remains active because unrelated research jobs are still running.

| Unit suffix after nov13c-vfy- | AS MiB | Launch MemoryMax | RuntimeMaxSec |
|---|---:|---:|---:|
| delta3r-pool-n7m16 / n8m16 | 900 / 1200 | 1200M / 1600M | 1000 |
| delta3r-compact-n7m16 / n8m16 | 1000 each | 1400M each | 1500 |
| delta3r-lift-n7add1 | 500 | 700M | finite; exact unit value not retained |
| n66-56-replay | 3600 | 4600M | 600 |
| n66-56-newrows | 700 | 1000M | 2200 |
| n66-56-fresh | 3400 | 4400M | 1400 |

The existing v5 guard removes kernel memory.max while enforcing anonymous
memory plus swap against the launch ceiling and track budget. Consequently
systemd's reported peak includes file cache; it is not the anonymous-memory
budget measure. Cake replay RSS was 3,286,916 KiB, with zero swaps.
No guard setting or research cap was raised.

`data/summary.json`, `data/units.log`, `data/memory_guard.log` and
`data/archive_manifest.json` preserve outcomes, executed commands and external
artifact hashes. Pool small evidence is under `pool/data/`.
All large CNFs, plain proofs and unsuccessful traces remain under
`/home/jay/research/data/delta3-codex-20261113/resume/`; N66 evidence is under
`/home/jay/research/data/verify309-codex-20261113/followup56/`.
No proof directory was deleted. The parent record's refreshed SHA256SUMS
covers this continuation; subrecords retain their own scoped manifests.

To recollect completed-run metadata, from the repository root:

```sh
timeout --kill-after=2 25 prlimit --as=419430400 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/collect_resume.py
```

This rewrites collection timestamps and requires refreshing the manifests.
Encoder-specific reproduction commands are in `compact/`, `lift/COMMANDS.md`,
`weak_theory/README.md` and the audit reports. A useful next target is a
favorable-Delta selection theorem or a repair permitting recoloring of old
blue points. Cup n7 +2 is another explicitly unresolved finite target; it
would need a new resource reservation, not an unchanged universal m16 retry.
No agent or new verification job is left running. No commit, push, branch
change, repository-root README edit or math.md edit was made.
