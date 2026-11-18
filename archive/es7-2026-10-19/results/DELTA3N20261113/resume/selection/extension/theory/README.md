# Geometric necessity of two envelope supports

**PROVED (written counterexample): two ambient supports are geometrically
necessary; triple orientations do not determine exposure.** Exact replay
passed in a separate implementation within this track. **COMPUTED exact:**
both endpoint sets and the displayed insertion have cap/cup/gon maxima
(4,4,6); the parent independently reported the same geometry. Started
14 November 2026, 04:47 KST; completed and frozen the same morning.
Assigned scope: `selection/extension/theory/` only. No Delta selection
failure, universal selection theorem, or numerical ES bound is claimed.

## Statement

For a real five-cap-free set U in general position with distinct x values,
a cap-triple terminal line can lie below the four-cap upper envelope on the
whole rightward half-line without lying below any single ambient line.
Moreover, keeping all triple orientations and all x coordinates fixed can
change exposure of the same terminal line, and uniform extension-safety of
the same specified weak Delta. It need not change existence of some Delta.

## Model and soundness

Use the definitions and written two-support proof in
`../../boundary/envelope/theory.md`. For M=max_x(U), a line is represented
by (slope, height at M). One support dominates iff both coordinates are at
least those of q. Two supports can dominate by a convex combination.
Only exact integer determinants and rational inequalities support a result.

## Method and results

The finder used bounded small random point sets and exact rational line
profiles. A found example was simplified by hand. No existing-pool sweep,
uniform-selection search, SAT solver, floating-point optimization or long
job was used.

Index the eight points from zero:

    (0,0), (1,1), (2,0), (3,4), (4,-3), (5,10), (6,-2), (7,5).

The only four-caps are 0124, 2356, 2357; there is no five-cap. For X=7+t,
the cap triple 036 has terminal line q=-2t-4. The ambient lines are

    L24=-3t/2-15/2,  L56=-12t-14,  L57=-5t/2+5.

Their half-weight certificate is `(L24+L57)/2=q+11/4`. Neither of these
lines, nor L56, dominates q on all t>0. Hence one support does not suffice.

Change only the last point to (7,3). All 56 triple orientations remain the
same; the set is still five-cap-free with exactly the same three four-caps.
Now L57=-7t/2+3, and q is exposed exactly on `14/3<t<7`.
At t=6, q=-16 exceeds the entire ambient envelope, whose value is -33/2.

The stronger family `(7,h)`, 3<=h<=5, stays in one order type and changes
exposure precisely at h=34/9. Equality is safe. See [theory.md](theory.md).
Thus exact fixed-realization exposure cannot be a predicate of triple
orientation signs alone, even with the x coordinates fixed.

A={0,3,6} is a weak Delta on both eight-point sets: its size is three and
its five-point complement cannot contain a six-gon. Both sets have no
seven-gon. For h=5, A+r is a weak Delta for every five-cap-free rightmost
insertion. For h=3, r=(13,-65/4) preserves both no-five-cap and no-seven-gon,
but A+r is the four-cap 036r. **Keeping A unchanged still gives a weak
Delta after that insertion.** No new six-gon contains r. This is a change
in one prescribed selection's uniform A+r property, not monotone failure
or a counterexample to global existence invariance.

## Controls

[tools/verify_examples.py](tools/verify_examples.py) imports no finder or
prior envelope code. It checks all determinants, every four- and five-subset,
the convex-combination identity, the exact exposure inequalities and a
five-cap-free insertion witnessing the exposed triple. The result in
[data/exact_replay.json](data/exact_replay.json) is PASS. This is independent
code within this track, not outside independent verification or CERTIFIED.

[tools/verify_delta_scope.py](tools/verify_delta_scope.py) exhaustively checks
convex hulls and target coverage without importing any other local code.
[data/delta_scope_replay.json](data/delta_scope_replay.json) is PASS and
agrees with the parent's separately reported endpoint-chain DP results.
See [VERIFY_THEORY.md](VERIFY_THEORY.md) for exact scopes and resources.

Two bounded random searches had no hit (3,000 eight-point attempts and
200,000 seven-point attempts); the successful eight-point batch stopped
at attempt 3,999. These are not exhaustion or minimality claims. Two
collinear development variants and a failed checker assertion about
nonempty new targets are preserved. No timeout, OOM or solver UNKNOWN
occurred.

## Files and hashes

- [theory.md](theory.md): full determinant table, written line proof,
  continuous family and precise Delta/encoding scope.
- [data/examples.json](data/examples.json): integer coordinates, weights,
  interval and insertion. SHA-256:
  `ad3a9be95b01e85f94bb415af9c513f55c177be96587f665b3c2fd8bb93fb05d`.
- [data/exact_replay.json](data/exact_replay.json) and
  [data/delta_scope_replay.json](data/delta_scope_replay.json): exact replay
  outputs with checker hashes and timing/RSS.
- [data/search/](data/search/): all three bounded finder outputs, including
  the original larger-coordinate example and both no-hit runs.
- [data/development_variants.json](data/development_variants.json) and
  [data/development/](data/development/): valid/invalid variants and the
  preserved initial checker failure.
- [SHA256SUMS](SHA256SUMS): this directory only, excluding itself.

Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/theory/`.
No shared manifest or older record was edited.

## What remains

The assigned questions are settled by the explicit examples. Minimality
of eight points is unknown. Global existence invariance, general uniform
selection, and general weak Delta questions are unchanged. The parent may
add its independent arithmetic/proof review in its own scope. This track
is frozen; no job remains active.

## Resume and resources

All checks used affinity CPU 3, address-space limit 400 MiB, CPU limit
18 seconds and external deadline 20 seconds. The longest finder took
6.713 seconds; final checkers used under 17 MiB RSS. The resource helper
reported twelve free CPUs under the global cap before the probes. Global
caps stayed 16 research CPUs and 24 GB, verifier track 6000 MiB. No compile,
long job, proof, installation, git mutation or external action occurred.

From the repository root, choose fresh scratch output names:

```sh
T=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/theory
W=/home/jay/research/data/delta3-codex-20261113/extension/theory
timeout -k 1 20 prlimit --as=419430400 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$T/tools/verify_examples.py" "$T/data/examples.json" --out "$W/replay-lines.json"
timeout -k 1 20 prlimit --as=419430400 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$T/tools/verify_delta_scope.py" "$T/data/examples.json" --out "$W/replay-scope.json"
```

Read the research rules and recheck live resources before resuming. Both
checkers refuse to overwrite output. Coordinate any long job with the parent.
