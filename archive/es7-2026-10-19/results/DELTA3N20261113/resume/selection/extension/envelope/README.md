# Full-pool uniform-envelope search: 945 positive exact models

**COMPUTED, exact positive models checked and independently replayed:** all 315 retained coordinate sets
and 630 orientation-preserving variations admit a uniform-envelope weak Delta.
No negative, timeout, invalid premise or failed check occurred in the completed
batch. Started 14 November 2026, 04:50 KST; unit completed 04:56 KST. Universal
uniform-envelope selection and weak D(5,7), D(5,8) remain open. No CERTIFIED
claim, ES bound or novelty claim is made.

## Statement

For each tested fixed U, the retained A hits every convex (n-1)-subset,
contains no four-cap, and its cap-triple envelope stays below the ambient
four-cap envelope for **every X>max_x(U)**. The same A works for all X.
All sets were freshly checked for general position, increasing x, no five-cap
and no convex n-gon.

## Model and soundness

[SOUNDNESS.md](SOUNDNESS.md) explains exact integer geometry, endpoint chain
enumeration, rational exposure calculation, CNF clauses and positive replay.
The characterization is the prior [written theorem](../../boundary/envelope/theory.md).
The CNF hits every target polygon and forbids every old four-cap and exposed
cap triple. Old four-cap clauses are retained.

C++ uses bounded signed128-bit determinants; Python uses unbounded integers
and Fraction for line inequalities. CaDiCaL is only a finder: every assignment
is checked against its complete CNF. A second Python implementation checks
all premises, the weak Delta, and rational domination of every selected cap
triple. The parent's separate implementation subsequently passed all945
witnesses:85,313 one-support and2 two-support certificates, grouped into306
orientation classes, in4.762s. See [the independent receipt](data/parent_positive_replay.json).
Its scope is positive witnesses and certificates, not a complete CNF audit.

## Method

Every record in the full pools (121 n7, 194 n8) receives a complete coordinate
CNF and checked model. Two deterministic single-vertex y perturbations then
move 7/8 toward an exact orientation boundary on a once-scaled integer grid.
Every triple sign is compared with the baseline before a fresh full check.
All 630 coordinate moves are nonzero; they preserve their315 baseline
orientation assignments (306 distinct groups in the parent's audit), rather
than introducing630 new order types.

Every case also emits `terminalsafe.cnf`, using all rank-three terminal triples.
This track neither solves nor minimizes those formulas. No generic signotope
formula was generated here.

## Results

| n | Input kind | Cases | Points | Selected cap-triple certificates | Exposure families changed |
|---|---|---:|---:|---:|---:|
|7|Original pool|121|21–26|8,588|—|
|8|Original pool|194|24–42|19,889|—|
|7|Coordinate variations|242|21–26|17,142|5|
|8|Coordinate variations|388|24–42|39,696|2|

All 945 are positive, with 85,315 selected cap-triple certificates. Seven
variations changed the exposure family while preserving all triple signs;
[summary.json](data/summary.json) lists them. The largest uniform CNF has
42 variables, 245,724 clauses and 1,688,045 literals. No model minimality is claimed.

The pool also supplies a geometric fact absent from the prior eight-fixture
record: a safe cap triple can **require two ambient lines** for its domination
certificate. From `n8-i107` we retain an 11-point subset with no five-cap or
eight-gon, a safe triple, two rationally weighted four-cap supports, and no
single dominating ambient line. Direct enumeration checks all 19 four-caps
and 12 ambient lines. See [the fixture](data/two_line_fixture.json) and
[its separate checker](tools/two_line_fixture.py). This is not a uniform
selection obstruction.

## Controls and preserved development outcomes

The small suite passed 55 geometry cases (41 valid, 14 invalid), comparing
all cap/target families and maximum chain/polygon sizes with exhaustive
subsets and hulls. Algebra controls cover two-line necessity, interior
exposure, equality endpoints, equal slopes and empty envelopes. The old
four-cap control confirms that envelope safety alone is insufficient.
See [controls.json](data/controls.json).

The first 42-point preflight returned `UNKNOWN_SOLVER_MEMORY_ESTIMATE`:
1,688,045 literals exceeded its initial one-million-literal guard. Its CNF
and source remain in scratch `profile-v1/`; [the outcome](data/development/initial_preflight_unknown.json)
is preserved separately. **This was not a memory failure.** Two smaller
positive profiles passed. The full batch used the authorized two-million-
literal guard and solved the 42-point case successfully.

After the cache correction below, two 42-point profiles passed with the
updated driver. Those are regression checks, not additional coverage.
The exact executed source remains frozen in `full-v1/source/`.

## Files and hashes

Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/envelope/`.

- [inputs.json](data/inputs.json) retains baseline coordinates and pool identities;
  [run_plan.json](data/run_plan.json) pins executed sources.
- [coverage.json](data/coverage.json) lists all models, counts and packet paths.
- [external_manifest.json](data/external_manifest.json) hashes 11,353 retained
  files; all hashes were reread and checked during collection.
- `full-v1/cases/<name>/` retains `input.json`, `points.txt`, `geometry.json`,
  `envelope.json`, `envelope.cnf`, `terminalsafe.cnf`, `finder.log`, `model.json`,
  `certificates.json`, `positive_replay.json`, `result.json`, and geometry stderr.
  The 945 packets total 1,114,303,545 bytes. Nothing was deleted.
- [SHA256SUMS](SHA256SUMS) covers this batch's README, SOUNDNESS, tools and data.
  The separate `adversarial/` continuation is outside that manifest.
  No shared manifest or old record was edited.

## Resources, deviation and remaining work

The parent received the plan before launch. Unit `nov13c-vfy-delta6-envelope`
used one CPU (affinity3), AS700MiB, MemoryMax1000M, MemorySwapMax0,
RuntimeMaxSec2400 and driver cutoff2200s. It completed in69.88s (64.52 CPU
seconds), exit0. Largest reported process RSS was72,600KiB. No OOM, swap
event or guard stop was observed.

**Resource estimate deviation:** accumulating retained-output page cache was
omitted. Systemd reported a **1000.2M cache-inclusive peak, reaching/slightly
exceeding nominal MemoryMax1000M**. The existing guard had lifted the kernel
limit. One high observation was anonymous52.5MB, file cache892.9MB and
kernel42.6MB. We do not claim the nominal limit was respected. The parent
was notified. Completed files were fsynced and advised POSIX_FADV_DONTNEED,
without deletion. The current reproduction driver releases each completed
packet's cache; two 42-point short controls passed. See the
[resource receipt](data/resource_receipt.json) and [unit log](data/unit_receipt.txt).

The bounded full-pool task is complete and its unit inactive. The parent
independently confirmed all945 witnesses. Universal existence, new order types
and adversarial coordinates remain outside this coverage statement. The newly
assigned 18-point adversarial continuation has its own `adversarial/` record.

## Reproduction

Read AGENTS.md and the research skill; check resources and coordinate the
one-CPU reservation before a long rerun. Use fresh output directories.
Compile `tools/geometry.cpp` with `g++ -std=c++17 -O2` under the short-check
500MiB/20s limit. Inside a fresh systemd unit with the limits above:

```sh
E=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/envelope
W=/home/jay/research/data/delta3-codex-20261113/extension/envelope
/usr/bin/prlimit --as=734003200 /usr/bin/taskset -c 3 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$E/tools/search.py" --pool-dir "$E/../../data/real_pool" \
  --binary "$W/geometry" --out "$W/fresh-rerun" --seconds 2200 --variations 2
```

Replay one packet with `tools/verify.py CASE_DIRECTORY` under the usual one-CPU
AS400MiB external20s limit. `tools/collect.py` verifies retained hashes and
creates a fresh evidence directory. `tools/controls.py` and
`tools/two_line_fixture.py` reproduce the separate exact controls.
