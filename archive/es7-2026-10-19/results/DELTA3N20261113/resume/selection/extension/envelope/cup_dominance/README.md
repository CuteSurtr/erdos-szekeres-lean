# Cup protection: all315 baseline sets and both terminal-obstruction fixtures pass

**PROVED (written):** cup-chain protection is sufficient for uniform envelope
domination. **COMPUTED:** every retained baseline set, the old18-point fixture
and the new15-point realization has an exactly checked cup-protected weak
Delta. No negative, unknown or failed check occurred. Completed14Nov2026.
No universal existence theorem, CERTIFIED claim or ES bound is asserted.

## Statement and soundness

For every selected cap triple(a,b,c), require an ambient four-cap ending in
(u,v) such that either(u,v)=(b,c), or u>=b,v>=c and the distinct union of the
pairs is a cup. Also forbid old four-caps and hit every whole(n-1)-gon.
[SOUNDNESS.md](SOUNDNESS.md) proves that the ambient terminal line then
exceeds the query line everywhere to the right of U. The criterion uses only
ordered triple orientations. Consequently any checked witness persists in
all realizations of the same ordered orientation data.

SAT finds membership assignments. Every assignment is checked against its
complete CNF; every selected cap triple receives an explicit four-cap support,
its cup union, and exact line slope/height inequalities. A separate positive
checker verifies all premises, the weak Delta and rational line certificates.
The parent's independent cup replay is separate and was pending at freeze.

## Method

Reused the frozen full-pool geometry, with fresh exact premise checks, and
added the complete bad-triple family for cup protection. All coordinate CNFs,
models, support rows and outputs remain retained. The generic signotope
encoder and terminal obstruction certification belong to the parent.

The known18-point fixture and four real positive controls were checked first.
Then all315 baseline records were tested (with the known18 fixture repeated
as a control). The newly supplied15-point realization was immediately tested
with both the original uniform-envelope finder and the cup-protection finder.
There was no further hillclimb.

## Results

| Cases | Count | Outcome | Selected cup-triple certificates |
|---|---:|---|---:|
|n7 baseline pool|121|all positive|8,424|
|n8 baseline pool|194|all positive|20,608|
|old18-point fixture|1|positive|77 in finder model|
|new15-point realization|1|positive under both finders|see retained packets|
|small real controls|4|all positive|exact checks passed|

The largest cup CNF has42 variables,245,950 clauses and1,688,723 literals.
The baseline certificate count is29,032. The pool run completed in20.17s.

Exact enumeration of all2^18 and2^15 colorings gives smaller explanations:

| Fixture | Ordinary weak Deltas | Cup-protected Deltas | Minimum size | One minimum A |
|---|---:|---:|---:|---|
|old18|8,149|1,639|5|{0,2,3,14,15}|
|new15|4,805|1,842|4|{2,3,6,9}|

The old18 witness uses ambient four-caps(0,8,14,16) and(0,8,15,16), with
three-point cup unions for its six cap triples. The new15 witness has just
two cap triples,(2,3,6) and(2,3,9), both supported by the four-cap(4,7,12,13).
Their cup unions are(3,6,12,13) and(3,9,12,13). Coordinates, every support and
positive replay are in [known18_minimum.json](data/known18_minimum.json) and
[real15_minimum.json](data/real15_minimum.json).

These1,639 and1,842 masks remain uniformly safe throughout their respective
ordered orientation cells, by the written sufficient condition. Thus a
uniform failure cannot be obtained by coordinate variation in either cell.
This later result supersedes the possibility left open in the frozen
adversarial record; it does not prove selection for arbitrary order types.

## Structural correction and four-point classification

The previously known A={0,5,6,7,8} is uniformly safe at its coordinates but
not cup protected. Its only cap triples are(0,5,6),(0,5,7). The quadruples
(5,6,14,17),(5,7,14,17) have pattern++--, not++++; determinant(5,14,17) is
-10,300,875,882. This corrected an exploratory parent command with an
incorrect determinant term; the parent's core checkers were unaffected.

No actual dominating ambient pair shares an endpoint with either query pair.
For q(5,6), ambient pair(12,13), witnessed by four-cap(0,9,12,13), is forced
to dominate by the four-point pattern-+++ although the union is not a cup.
Its four other actual supports, and all four supports for q(5,7), have
pattern++--; their slope comparison is not forced by those four-point signs.
See [old_known_A.json](data/old_known_A.json).

For two disjoint endpoint pairs, let d be ambient line minus query line.
Its endpoint signs are determined by triple orientations. If d at the
leftmost endpoint is negative and at the rightmost is positive, domination
of the whole rightward ray is forced. Positive signs at both ends leave the
slope undetermined. A negative rightmost value rules out domination from
that endpoint, though a later ray may differ. The complete48-case table has
18 forced cases,6 undetermined cases and24 cases failing the whole ray.
[The table](data/four_point_classes.json) includes opposite exact realizations
for all six ambiguous cases and exact controls covering all48 rows. This
comparison is not a change to the cup criterion used in the completed CNFs.

## Controls

Three earlier boundary fixtures at n6,n7,n8 passed. A seven-point integer
control has no five-cap or six-gon. Its A={0,1,2} contains the cap triple
(0,1,2), protected by ambient four-cap(3,4,5,6) through the cup union
(1,2,5,6). Pair(1,2) itself cannot end a four-cap. This proves the sufficient
rule is strictly weaker than terminal safety on real valid data.
[proper_cup_control.json](data/proper_cup_control.json) and the source script
retain the coordinates and certificate. No negative result was rounded up.

## Files and hashes

Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/envelope/cup_dominance/`.

- `known-v1/`: four controls, known18 formula/model and executed source snapshot.
- `pool-v1/cases/`:315 baseline packets plus the repeated known18 control.
- `real15-v1/{uniform,cup}/`: both fresh coordinate formulas and exact models;
  `source_input.json` freezes the parent's realization.
- `structure-v1/`: exact enumerations and full support/classification packets.
- [coverage.json](data/coverage.json), [pool_summary.json](data/pool_summary.json),
  [real15_summary.json](data/real15_summary.json), [run_plan.json](data/run_plan.json).
- [external_manifest.json](data/external_manifest.json) hashes3,264 retained
  files totaling253,512,976 bytes. [SHA256SUMS](SHA256SUMS) covers this record's
  README,SOUNDNESS,tools,data only. Later `comparison/` work is separate.

## Resources and remaining work

The parent received the plan before the pool run. Unit
`nov13c-vfy-delta6-cup-pool` ran05:27:00–05:27:20KST, one CPU(affinity3),
AS700MiB, MemoryMax1000M, MemorySwapMax0, RuntimeMaxSec600, driver500s.
It used16.669 CPU seconds, exited0, and peaked at214.9M including file cache.
Per-case cache release was active. No guard stop, OOM or nominal-limit
violation occurred. All other probes/controls were bounded short checks.

The long allocation is released. Further checks are one CPU/AS300MiB/20s
unless newly coordinated. No new long job is planned. Universal cup-protected
selection and the broader orientation-only criteria remain open. Independent
cup-certificate replay is the parent's next check. No shared or older record,
installed software, git history, proof directory or external service was changed.

## Resume

Fresh output directories are required. Read repository rules and coordinate
resources before any long rerun. `tools/probe.py` accepts `--out`, `--binary`,
`--known`, optional `--controls`, and optional `--full-run` pointing to the
completed uniform `full-v1/` batch. `tools/fixture.py` accepts a new coordinate
JSON via `--input`, an explicit `--n`, `--name`, `--binary` and fresh `--out`.
`tools/structure.py` accepts `--known-case`, `--case15` and fresh `--out`.
Exact commands/paths are pinned in [run_plan.json](data/run_plan.json).
