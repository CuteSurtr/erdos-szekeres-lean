# Delta3 exact integer search instrument

Status: **COMPUTED** implementation and controls, 13 November 2026. **HEURISTIC** search.
No new Delta counterexample or universal theorem is claimed. No UNSAT result from
this implementation has yet been certified with cake_lpr.

This directory is the assigned `DELTA3N20261113/search/` area. New scratch files are
under `/home/jay/research/data/delta3-codex-20261113/search/` (abbreviated `W` below).
Old research records, the main README/math files, branches, and commits were not
changed. No email or web request was made. No long job or systemd unit was launched
by this implementation agent.

The parent reports launching the frozen binary in `nov13c-vfy-delta3-search-n7`,
with output `W/scheduled-n7-701`, for 600 seconds. That run's results belong to the
parent; this file records only the short implementation controls completed before
the launch. The parent requested no additional jobs, and none were started after
that instruction.

## Delivered files

- `delta_search.cpp`: standalone C++20 engine, one thread, no external libraries.
- `runner.py`: compiler, JSON/JSONL importer, resource-limited runner, independent
  packet audit, optional CaDiCaL/cake_lpr certificate pipeline.
- `controls.py`: hull/subset oracle, fixture controls, malformed-input and limit
  tests, and packet corruption test.
- `fixtures.json`: six coordinate fixtures, with local provenance and source
  hashes where applicable. Includes the parent's new 16-point example.
- `CONTROL_RESULTS.json`, `CONTROL_CHECKS.jsonl`: copied final control results.
- `SMOKE_RESULT.json`: copied three-second search counters and configuration.
- `ARTIFACTS.json`, `SHA256SUMS`: executable, input-pool, control, and source hashes.

Read to establish semantics: `DELTA2N20261113/README.md`, `VERIFY_D1.md`,
`tools/lower_lib.py`, `tools/lower_walk.py`, `tools/control_lower.py`, the relevant
Delta/saturated-pair sections of `ETVTHY20261113/README.md`, and the E4 coordinates
in `NOVELTY20261113B/README.md`. An existing FASTBB C++ engine was inspected; its
LP/omission problem was different, so no code was imported. Production geometry
and the DPLL solver are new and do not load `esgeo` or the old Python tools.

## Mathematical contract and exactness

Input is a real integer point set with distinct x coordinates and no collinear
triple, sorted internally by x. All output indices refer to that sorted order.
The supported range is 0..64 points, `4 <= a <= 8`, `a <= n <= 12`.
The main targets are `a=5`, `n=7,8`, `mode=lower`.

Coordinates satisfy `|x|, |y| <= 10^15`. Inputs outside that bound are rejected.
Subtractions are promoted before arithmetic. The determinant has absolute value
at most `8*10^30 < 2^103`, well inside signed `__int128`. Structured mutations use
128-bit intermediate arithmetic and check the coordinate bound before narrowing.
Floating-point arithmetic occurs only in heuristic scores and wall-clock limits.

**PROVED (algorithmic argument, not a proof of the conjecture):** for real points,
a cap and a cup with the same extreme endpoints meet only at those endpoints;
their union is in convex position. Conversely, each convex polygon splits into
such chains. Thus the largest polygon size is
`max_(u<v) (capB(u,v)+cupB(u,v)-2)`. A valid set satisfies
`capB+cupB <= n+1`, and its convex `(n-1)`-gons correspond exactly to pairs attaining
`n+1` and their longest cap/cup chains. Consequently the desired cup-side condition
is exactly

```
capB_S(u,v) + cupB_(S\Delta)(u,v) <= n
for every pair u<v outside Delta,
and Delta contains no (a-1)-cap.
```

Both endpoints are included in the cup to be hit. This condition is stronger than
weak D(a,n); a cup-side failure alone would not refute weak D(a,n).

The production DP works backwards from each right endpoint, extending edges
through cached cap/cup successor bit masks. A second implementation works forwards
from each left endpoint and uses raw integer determinants. On valid inputs the
entire original pair-length tables must agree before any exact solver verdict.
Every returned Delta is checked again with the forward implementation. Invalid
premise candidates are rejected using the production geometry; small controls
independently check those rejections too.

All `(a-1)`-caps are enumerated as negative monotone clauses. One genuine hit
clause per saturated pair initializes the positive clauses. Complete bit-mask
DPLL uses unit propagation and branches on a variable in a shortest unsatisfied
positive clause. A SAT model is checked geometrically. Any missing cup adds its
positive clause, with a cap/cup polygon witness, and DPLL repeats.

**PROVED (encoding argument):** every generated clause is necessary for a valid
Delta. A model is accepted only after the complete geometric oracle succeeds.
An exhaustive contradiction in even a subset of the necessary clauses implies
no Delta exists. The lazy formula therefore need not enumerate every cup before
an UNSAT conclusion. Finite limits may stop either phase; they yield `UNKNOWN`.
No limit is interpreted as failure of the conjecture.

The native unbounded negative verdict is **COMPUTED**, not **CERTIFIED**.
`runner.py audit` independently checks each clause from the coordinates, checks
the premises with arbitrary-precision Python arithmetic, and checks actual hull
convexity of every polygon witness. The optional `certify` command first performs
that audit, then runs CaDiCaL with text LRAT and cake_lpr. It assigns **CERTIFIED**
only when the checker stdout contains the exact line `s VERIFIED UNSAT`.
Exit codes alone never certify UNSAT. This external pipeline was implemented but
not run during this task; its exact-line gate and geometric audit were controlled.

## Hardness and structured search

The seven mutation families are cycled, with random choices inside each family:

1. Move a selected vertex vertically across the nearest orientation wall. The
   rational line height is calculated with exact integer division.
2. Scale and split a vertex into a small local cluster, allowing growth.
3. Translate an entire contiguous block across a wall.
4. Change the sweep direction by a positive-determinant integer shear of x.
5. Apply a quadratic vertical bend.
6. Delete a point near the current Delta, allowing subsequent cluster regrowth.
7. Graft an affine image of a block from another bank entry.

All resulting sets are rechecked for general position and both premises. Mutation
names describe proposals, not guarantees that the order type or validity survives.
Failed proposals never enter the bank. Integer rounding in wall/graft operations
can cross multiple walls or create degeneracy; exact checks handle this.

A bounded cache stores the complete packed orientation string, including point
count. Hash collisions cannot identify different order types. `novel_tested`
means absent from this recent cache, **not globally distinct**: evicted types may
reappear. It includes candidates later rejected for violating the premises.
`move_OK` counts successful existence tests, including tests not accepted as the
current state. There is no equivalence reduction across different sweep orders.

`--min-delta` binary-searches the minimum cardinality of a **cap-free cup-side**
Delta using complete cardinality-bounded DPLL plus the same geometric oracle.
This is not the minimum of a bare cup transversal. Only a completed bounded
contradiction raises the proven lower bound. Timeout retains the previously
verified working Delta, with `tau_lower <= tau <= tau_upper`, `tau_exact=false`,
and `optimization_unknown=true`. It does not produce a conjecture failure.

`--private-witnesses` seeks for each selected vertex p a polygon whose lower cup
meets the current Delta exactly at p. It records the vertex and both chains.
Mutations favor these vertices. `private_complete` means the extraction loop
finished; it does not mean every vertex has a private witness in a nonminimal
Delta. If the loop times out, the working Delta remains valid.

The bank score is

```
30*m + 100*tau_lower + 2*private_count + 0.6*saturated_pairs
     + 3*doubly_hard_pairs + 5*log(1+DPLL_nodes) + 3*log(1+hit_clauses).
```

Three quarters of a full bank preserve high scores; the remaining slots provide
diversity. Restarts default to every 128 proposals. Some worse moves are accepted
to allow deletion/regrowth. Scores are heuristic, and are not minimum-cardinality
proofs unless the separate `tau_exact` flag is true.

On an unbounded exhaustive failure, `failure.{json,cnf,points}` is saved before
minimization. Greedy deletion recomputes all geometry and constraints at every
trial; it does not assume saturated-pair sets are inherited. It writes
`minimized.*` after each successful reduction. `one_deletion_minimal=true` requires
a full final pass without an inconclusive deletion test. A global search deadline
can leave only the raw failure or a partially minimized failure.

## Controls actually completed

**COMPUTED:** the final suite ran 60 native invocations in 0.249 seconds, with
maximum child RSS 21,424 KiB (the child inherits the Python harness before exec).
The frozen production binary passed this suite after its final build.

- E4, the known 15-point `(5,6)` fixture: strong fails; weak and cup-side succeed.
- Known 11-point cap-side failure: upper fails and lower succeeds.
- Known 9-point endpoint failure: endpoints fail and lower succeeds.
- ETV 26-point and 42-point fixtures: lower succeeds; the 42-point set has 191
  saturated pairs.
- Parent's new 16-point `(5,7)` seed: **minimum cap-free cup-side Delta size 5**;
  one returned Delta is `{0,1,3,6,7}`. Each of these five vertices has a checked
  private cup witness. An initial standalone check took 0.326 ms; the final
  suite repeated the result and audited its exported packet.
- 36 small real point sets, 17 satisfying their chosen premises: exhaustive
  subset enumeration and monotone-chain hulls agree with both pair-length tables,
  premise decisions, solver answers, returned models, and exact minima. Parameters
  include a=4,5,6 and n=5..8; the five supported modes all occur.
- Coordinate arithmetic near both +/-10^15 boundaries, a 64-point cup exercising
  bit 63, empty/singleton/two-point inputs, duplicate x, collinearity, and a
  coordinate exceeding the bound.
- Forced time/node/round/clause limits all return `UNKNOWN`, never a failure.
  A cardinality bound of zero returns `NO_DELTA_WITHIN_BOUND` separately.
- Endpoint failure minimization completes; independent brute force finds a Delta
  after each remaining single-point deletion.
- Geometry audits accept the actual fixture packets and reject a corrupted hit
  clause. Certificate-verdict parsing rejects empty output, ordinary UNSAT,
  leading-space variants, and appended text.

**HEURISTIC:** one three-second smoke search from the 16-point seed, `seed=701`,
completed 30,913 proposals, 21,228 cache-miss geometry tests, and 7,282 successful
existence tests across the seven mutation families. It accepted 3,002 moves,
reported 9,140 cache hits and 14,491 invalid proposals, and found no Delta failure.
There were zero incomplete existence tests and one incomplete cardinality
optimization. These correlated tests are not exhaustive evidence. The saved best
configuration in that short run had 20 points and computed minimum Delta size 7;
that exploratory record is `W/smoke-parent16/best.json` and was not independently
minimized or certified.

A separate two-second cardinality probe on the 42-point fixture found a verified
16-point Delta and established only `13 <= tau <= 16` before its budget expired.
It did **not** establish tau=16. Its native maximum RSS was 7,804 KiB. Do not use
the parent's separate tau=16 result to relabel this probe as complete.

No head-to-head timing against `lower_walk.py` was run. The differences are compiled
geometry/solving, exact status handling, recent-order-type deduplication, structured
proposals, and the cardinality/private-witness objective.

## Commands and scheduling

Use the specified interpreter:

```bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
S=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/search
W=/home/jay/research/data/delta3-codex-20261113/search
```

The frozen executable used by the parent is `W/delta_search_v1`, SHA-256
`7cdf13a7d1a99be7a48fadcea2931342489079edc0ace21637c30a664f4dea9d`.
Do not rebuild this path while the parent is using it. Builds can target a new
filename; the runner installs a completed build atomically. No build is needed
for the currently scheduled run.

The exact scheduled configuration, already launched by the parent, is:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" search \
  --binary "$W/delta_search_v1" --pool "$W/n7-diverse.pool" \
  --out "$W/scheduled-n7-701" --a 5 --n 7 --seconds 600 --seed 701 \
  --min-delta --private-witnesses --time-ms 100 --memory-mb 512 \
  --clause-limit 200000 --cache 10000 --bank 24 --min-size 14
```

The pool has 14 sets: the new 16-point seed, ETV's 26-point set, and six selected
rows from each of `pool_hept.jsonl` and `pool_hep.jsonl`. Sizes are 16..29. Seeds
are individually validated before use; input-pool membership is not a claim of
validity. Its exact SHA-256 is in `ARTIFACTS.json`. `n7-diverse.jsonl` preserves
the source paths and row indices. Startup considers larger seeds first; all 14
fit below the configured bank capacity of 24.

Resource estimate for this configuration: one thread, approximately 600 seconds
of wall time, usually tens of MB and expected under 150 MB for the configured
cache/clauses. The child has a 512 MiB address-space limit and the Python wrapper
adds roughly 20–30 MB. The parent's `MemoryMax=700M` covers both. Actual test RSS
is reported above; this is not a measured 600-second peak. No threads, child SAT
processes, systemd calls, or background jobs are created by native search.

The runner refuses an existing output directory. `stdout.jsonl` contains periodic
and final counters; the native stream is flushed, even though the wrapper prints
its captured stdout to its own caller only at termination. Follow the file while
running. Other files: `manifest.json`, `stderr.log`, `improvements.jsonl`,
`best.*`, `elite.jsonl`, and, when needed, `pending.jsonl`, `failure.*`,
`minimized.*`. Every incomplete existence test is saved to `pending.jsonl`.
Cardinality-only uncertainty is recorded separately because existence was checked.

Future commands below are ready instruments, **not requests to launch more jobs**:

```bash
# Build a new executable and run the short control suite.
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" build --binary "$W/delta_search_next"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" controls --binary "$W/delta_search_next"

# Check one .json / .points file; JSONL is accepted only if it has one record.
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" check \
  --binary "$W/delta_search_v1" --input "$W/parent16-check/input.points" \
  --a 5 --n 7 --min-delta --private-witnesses

# Prepare a future n=8 pool from real coordinates, then let the parent schedule it.
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" prepare --out "$W/n8-future.pool" \
  /home/jay/research/data/etvthy-20261113/etv858.json \
  /home/jay/research/data/etvthy-20261113/pool_main.jsonl
# Same search command as above with --n 8, another output path, and this pool.

# On a future unbounded failure packet: audit, certify, or resume minimization.
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" audit "$W/RUN/failure.json"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" certify "$W/RUN/failure.json" \
  --seconds 60 --heap-mb 512 --memory-mb 1536
PYTHONDONTWRITEBYTECODE=1 "$PY" "$S/runner.py" minimize \
  --binary "$W/delta_search_v1" --input "$W/RUN/failure.points" --a 5 --n 7
```

Certificate jobs are separate, sequential solver/checker processes and must be
scheduled against the shared verifier budget; the default checker heap is explicit.
The stored native CNF for a cardinality-bounded check omits that extra bound and
is marked accordingly. `certify` rejects bounded and inconclusive packets. Minimum
cardinality claims therefore remain COMPUTED in this version.

Native exit codes: 0 checked Delta / completed search; 10 unbounded computed
failure; 11 no Delta within an explicit cardinality bound; 20 inconclusive
existence, no usable seed, or incomplete minimization precondition; 30 failed
premises; 31 degenerate/out-of-bound geometry; 2 parser/internal/I/O error.
A completed search with any incomplete existence test returns 20; cardinality-only
uncertainty does not change a checked existence verdict into an unknown one.

Limits and trust boundary: 64-point masks, bounded coordinates, pure DPLL rather
than a learning SAT solver, bounded per-case work, and a bounded recent cache.
Large or hard sets can be inconclusive. Source, compiler, geometry and solver
controls have been exercised; no proof-assistant verification, sanitizer run,
external LRAT run, or universal conjecture certification was performed here.
