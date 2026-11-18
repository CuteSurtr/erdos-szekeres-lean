# Adversarial coordinates: no improvement in the sampled 18-point cell

**HEURISTIC search completed; exact finite scores:** 474,988 proposals and
256 restarts all retained exactly 4,057 uniform-envelope Deltas. No strict
improvement, zero-survivor case, unknown or failed check occurred. The
ordinary weak Delta family has exactly 8,149 members throughout this cell.
This does not prove fixed-x exposure invariance or universal selection.

## Statement and model

The target was uniform-envelope failure within the orientation cell of the
retained 18-point n7 terminal obstruction. Ordinary weak Delta failure is
impossible in this cell. A fixed ordinary Delta is eliminated exactly when
it contains a cap triple whose terminal line is exposed somewhere rightward.
Each cap-terminal pair has a bitset marking the ordinary Deltas containing
one of its triples. The union over exposed pairs gives the exact eliminated
family; the objective is the number of surviving Deltas, not exposed-edge count.

[SOUNDNESS.md](SOUNDNESS.md) explains the truth-table enumeration, pair coverage,
integer exposure predicates, strict movement bounds and limits of the search.

## Method

Initial coordinates were scaled once by4096. All x coordinates then stayed
fixed; one integer y at a time moved inside the exact strict orientation
interval and the box [-B,B], B=16 times the largest initial absolute y.
Each visit tested integer endpoints, near-boundary fractions, a midpoint and
four random integers. The heuristic favored lower survivor counts, allowed
neutral moves, and used warmup/rare escape moves plus restarts. Seed2026111405,
256 restarts,128 moves per restart,500,000-proposal ceiling and3300s deadline.

Every accepted state and every newly sampled exposure family had all816
triple signs and full exact exposure/certificate data rechecked. A strict
best also receives a direct test of all8,149 ordinary masks and a complete
coordinate CNF with a checked geometric model. No further hillclimb was run.

## Results

| Quantity | Result |
|---|---:|
| Proposals scored |474,988|
| Restarts completed |256|
| Accepted moves |32,575|
| Distinct sampled exposure families |1|
| Initial / best / every proposal survivor count |4,057|
| Strict score improvements |0|
| Ordinary weak Deltas |8,149|

The exposure pairs were always (7,14),(7,15),(7,17),(10,16),(10,17),(14,15),
(16,17), with zero-based indices. The best trajectory is therefore flat:
only `best-000` at the baseline. The full7.1MiB accepted-move/restart trajectory
is retained, including all neutral movement. No sample establishes a theorem
about unvisited coordinates. The parent's separate structural follow-up is
recorded under the neighboring `cup_dominance/` task.

## Controls and replay

[controls.json](data/controls.json) records a direct check of all262,144
colorings against the same full geometric families, agreeing with exactly
8,149 ordinary masks. Direct exposed-triple checks give4,057 baseline
survivors. Both strict integer interval endpoints for all18 vertices and
1,000 rational line-family tests passed.

The preflight retained1,005 proposals and68 accepted moves, also with no
improvement. Its initial outer-loop bound could overshoot by a small batch;
the final driver enforces the proposal limit within the inner loop. The
original preflight source and result are preserved, not overwritten.

A separate [trajectory replay](tools/replay.py), importing no search code,
verified every32,575 accepted move by the affected triple orientations and
all256 restart geometries:4,639,096 exact orientation tests. It independently
recomputed the score at127 specified states, including the retained best,
using Fraction line intersections and all8,149 masks. All returned4,057.
See [the replay receipt](data/trajectory_replay.json). This is a second
within-track implementation, not the parent's independent audit, and does
not independently recompute the score of every proposal.

## Files and hashes

Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/envelope/adversarial/`.

- [summary.json](data/summary.json), [best.json](data/best.json) and
  [exposure_patterns.json](data/exposure_patterns.json) retain the exact results.
- [run_plan.json](data/run_plan.json) pins executed sources and parameters.
- `run-v1/family.json` retains all8,149 masks and every pair coverage bitset.
- `run-v1/trajectory.jsonl` retains accepted moves and restart coordinates.
- `run-v1/baseline/`, `run-v1/best/best-000/`, and `run-v1/patterns/` retain
  coordinates, the full coordinate CNF/model/certificates, and pattern example.
- [external_manifest.json](data/external_manifest.json) hashes every file in
  the completed run and the preserved preflight, with source snapshots.
- [SHA256SUMS](SHA256SUMS) covers only this adversarial subrecord.

## Resources and remaining work

Parent received and accepted the measured plan before the bounded job.
`nov13c-vfy-delta6-env-adversarial` ran05:10:32–05:12:03KST14Nov2026, one CPU
(affinity3), AS700MiB, MemoryMax1000M, MemorySwapMax0, RuntimeMaxSec3600.
It completed at the restart limit in91.15s, with90.395 CPU seconds, exit0.
Journal peak was11.8M; process peak RSS21,604KiB includes shared pages.
Per-packet fsync/fadvise and trajectory cache release were used. No nominal
MemoryMax deviation, guard stop, OOM or observed swap occurred in this run.
[unit_receipt.txt](data/unit_receipt.txt) retains the journal evidence.

The unit is inactive. A uniform failure elsewhere in the same orientation
cell or outside the bounded grid remains possible. No universal theorem,
CERTIFIED result, new ES bound, installation, external action, git mutation,
proof deletion or old-record edit was made.

## Resume

Read repository rules and check live reservations first. A fresh long run
needs the stated one-CPU systemd limits and a fresh output directory. The
executed parameters are in `data/run_plan.json`; the command's core is:

```sh
E=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/envelope
W=/home/jay/research/data/delta3-codex-20261113/extension/envelope
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$E/adversarial/tools/adversarial.py" \
  --input "$E/../../terminal/data/witness.json" --binary "$W/geometry" \
  --out "$W/adversarial/fresh-run" --seconds 3300 --max-evals 500000 \
  --restarts 256 --steps 128 --scale 4096 --seed 2026111405
```

`tools/controls.py` and `tools/replay.py` accept `--run` and a fresh `--out`; both completed under
the one-CPU AS400MiB external20s short-check limits.
