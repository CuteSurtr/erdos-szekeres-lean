# Two fixed realizations: 4,499 uniform Deltas, minimum three

**COMPLETE — COMPUTED exact finite enumeration, 14 November 2026.** The
original and balanced 15-point realizations have identical families of
4,499 uniform Deltas. Each has exactly four minimum witnesses of size three.
All indices below are zero-based.

## Statement

| Fixed realization | Ordinary Deltas | Uniform Deltas | Minimum uniform size | Number attaining minimum |
|---|---:|---:|---:|---:|
| Original `realize15-a/witness.json` | 4,805 | 4,499 | 3 | 4 |
| Balanced `balance15-a/witness.json` | 4,805 | 4,499 | 3 | 4 |

This compares exactly two coordinate sets. It does not establish constancy
of uniform counts or minima throughout their common orientation cell, nor
exhibit variation of either quantity. No coordinate search was run.

## Model and soundness

An ordinary Delta contains no four-cap and meets every convex six-subset.
For each cap triple `(a,b,c)`, compare its terminal line with the upper
envelope of terminal lines of all ambient four-caps, on every `X > max_x(U)`.
The Delta is uniform precisely when it contains no exposed cap triple.
This is the fixed-coordinate characterization in
[boundary/envelope/theory.md](../../../../boundary/envelope/theory.md),
Theorem 3. Its necessary quantifiers and the retained four-cap constraints
are unchanged.

Exposures are decided by intersecting exact rational strict inequalities.
A separate implementation checks every pair against all nonnegative
ambient-line intersections, the value at zero, and the largest ambient
slope. Between consecutive intersections the upper envelope is affine;
the endpoint values and final slope therefore give a complete half-line
test. This is a within-track second implementation, not a parent audit.

## Method

`tools/count_uniform.py` loads the cached exact families: 145 cap triples,
48 four-caps and 187 convex six-subsets. It checks general position,
increasing x, all 455 orientation signs, and the no-five-cap/no-seven-gon
premises in both realizations before reusing these families. Both have
maximum cap size four and maximum convex-polygon size six.

All 32,768 subset masks are tested for ordinary Delta membership once.
The resulting 4,805 masks are filtered separately by the two exact exposure
families. Every minimum witness is replayed using separate geometric code,
including its complement and its supporting four-caps. The complete ordinary
mask list, both uniform mask lists, coordinates, exposure intervals, minimum
models and both 15-variable, 237-clause membership CNFs are retained.

## Results

In both realizations the only exposed triples are `(7,9,10)` and `(7,9,14)`.
Exactly 306 ordinary Deltas contain at least one of them. The two surviving
families agree mask for mask; their CNFs are byte-identical.

| Selected size | Ordinary count | Uniform count, in either realization |
|---:|---:|---:|
| 3 | 4 | 4 |
| 4 | 59 | 59 |
| 5 | 351 | 346 |
| 6 | 1,047 | 1,009 |
| 7 | 1,578 | 1,474 |
| 8 | 1,216 | 1,105 |
| 9 | 463 | 420 |
| 10 | 81 | 76 |
| 11 | 6 | 6 |

The four ordinary size-three Deltas are all caps, and all four are uniform
in both realizations. The following single ambient lines dominate their
terminal lines in slope and height at `max_x(U)` in each fixed realization:

| Minimum Delta | Supporting ambient four-cap | Its terminal pair |
|---|---|---|
| `{2,3,7}` | `(4,7,12,13)` | `(12,13)` |
| `{2,3,11}` | `(4,7,12,13)` | `(12,13)` |
| `{4,11,12}` | `(7,9,10,14)` | `(10,14)` |
| `{4,11,13}` | `(7,9,10,14)` | `(10,14)` |

Thus the earlier cup-protected minimum of four is strictly above the exact
uniform minimum in both tested realizations. These are exact coordinate
certificates; this addendum makes no orientation-only claim about these
four particular minimum witnesses.

## Controls and resources

The four ordinary triples exactly match the parent's retained list in
`model15_audit/data/weak-witnesses.json`. All 50 distinct cap-terminal pairs
per realization agree between interval and rational breakpoint checks.
The original minimum absolute determinant is 3,321,082; the balanced one
is 45. All 455 orientation signs agree.

The computation exited zero in 0.10 seconds wall time, using 19,692 KiB
maximum RSS. Limits: one CPU (affinity 3), AS 300 MiB, CPU 18 seconds,
external timeout 20 seconds. No long allocation, solver, hillclimb, new
UNKNOWN or memory failure occurred. Per-case output cache release remains
in the driver. The earlier reports, unknowns and manifests are unchanged.

## Files and hashes

- [data/run/summary.json](data/run/summary.json): counts, histograms and controls.
- [data/run/differences.json](data/run/differences.json): exact family equality.
- `data/run/{original,balanced}/`: coordinates, all uniform masks, exposures,
  minimum certificates, individual size-three checks and complete CNFs.
- `data/run/ordinary_masks.json`: all 4,805 ordinary masks.
- `data/run/source/`: executed source snapshot and its imported modules.
- `data/inputs/`: frozen input snapshots, including cached geometry and the
  parent's weak-witness list; paths and input hashes are in
  `data/run/input_manifest.json`.
- `data/external_manifest.json`: hashes for all 23 external run files
  (213,515 bytes) under
  `/home/jay/research/data/delta3-codex-20261113/extension/envelope/cup_dominance/metric15-v1`.
- [data/resource.txt](data/resource.txt): command, resource limits and exit receipt.
- `SHA256SUMS`: scoped hashes for this append-only addendum.

Both uniform CNFs have SHA-256
`47e0cdabc88a0afd407c129090c38977774b5e20beb776b5c9a7761c6be6b8cb`.

## What remains

Nothing remains in the requested two-realization task. Independent parent
replay is separate. Neither these two positive coordinate checks nor the
stored CNFs assert a universal existence theorem.

## Reproduction

From the repository root, choose a fresh output directory. The command
below uses frozen inputs in this addendum and does not modify earlier runs.

```bash
metric_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/envelope/cup_dominance/metric15
metric_out=/home/jay/research/data/delta3-codex-20261113/extension/envelope/cup_dominance/metric15-replay-v1
timeout -k 1 20 prlimit --as=314572800 --cpu=18 taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$metric_record/tools/count_uniform.py" \
  --original "$metric_record/data/inputs/original.json" \
  --balanced "$metric_record/data/inputs/balanced.json" \
  --cached-case "$metric_record/data/inputs/cached_case" \
  --weak-witnesses "$metric_record/data/inputs/parent_weak_witnesses.json" \
  --out "$metric_out"
```
