# Real cardinality-three obstruction — COMPLETE

**COMPUTED exact independent checks:** an explicit eleven-point real (5,7)
set has minimum weak-Delta and terminal-safe weak-Delta size **three**.
The written finite certificate and non-affine one-parameter family are in
[VERIFY_CARDINALITY.md](VERIFY_CARDINALITY.md). Started 14 November 2026,
05:05 KST; completed around 05:17 KST.
The completed `../audit/` is frozen and is not edited by this track.

## Statement

The x-ordered points are

```
(0,0), (2,-1), (9,2), (24,9), (25,-13), (48,1),
(71,-29), (85,-11), (86,-11), (140,59), (141,0).
```

They have no five-cap or seven-gon. **A={0,1,3}** is a cup and meets every
convex six-subset. Every pair misses at least one convex six-subset, so
ordinary weak Deltas also require at least three points. No global
minimality in ambient size or new ES bound is asserted.

## Model and soundness

The independent replay checks all 165 determinants, 462 possible five-caps,
330 possible seven-gons, 22 actual six-targets, all 55 pairs and all 2,048
selections. A twelve-row pair-cover certificate explains the lower bound.
A={0,1,3} has determinant 42 and is terminal-safe because it has no cap
triple. Replacing only (48,1) by (48,1+t) preserves all facts whenever
**-1<t<8/61**; an independent exact endpoint certificate proves the interval.

## Method and results

Exhaustive deletion scans of terminal18, compact16 and star12 found no
candidate: all 36,204 eleven-subsets have a hitting pair. The retained
abstract n7/m11/k2 orientation model was then realized on the eighth
bounded numerical proposal, accepted only after exact sign checks.
Exact rounding and coordinate compression gave the small integer witness.
HiGHS statuses are never used as evidence. No parent uniform-envelope or
terminal-safe CNF scan was duplicated.

Independent replay finds twelve four-caps, no five-cap, 22 convex six-sets
and no seven-gon. Maximum cap/cup/convex sizes are (4,5,6). There are 65
ordinary weak and 46 terminal-safe Deltas of size three. All four concrete
coordinate replays and seven negative controls pass.

## Controls, files and what remains

`find.py`, `realize.py`, `simplify.py` and `family.py` retain discovery and
exact simplification. `verify.py`, `verify_family.py` and `controls.py`
provide independent replay and controls. No parent checker is imported.
The final [witness](data/witness.json), [point data](data/witness.points),
complete receipts, unsuccessful attempt traces, `data/inputs.json` and
scoped `SHA256SUMS` pin the evidence.
Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/cardinality/`.
The bounded task is complete; no work remains running or queued.
The family has eleven points throughout. Larger-n generalization and
ambient-size minimality were not established or claimed.

## Resources and resume

One CPU, AS400 MiB, external 20 seconds per invocation; largest RSS was
75,572 KiB. No long allocation was needed. The prior audit's manifest still
verifies. No git mutation, installation, external action, proof deletion,
frozen audit edit or shared manifest change occurred.

From the repository root, after checking resources:

```sh
card=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/cardinality
py=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  prlimit --as=419430400 --cpu=18 "$py" -B "$card/verify.py" \
  "$card/data/witness.json" witness-recheck
```

Use a fresh receipt tag: all output scripts refuse to overwrite retained
attempts. Re-running numerical discovery is unnecessary for verification;
all final claims use frozen integer coordinates and exact arithmetic.
