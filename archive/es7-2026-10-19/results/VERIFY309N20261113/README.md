# VERIFY309N20261113 — independent audit of the proposed ES(8) ≤ 309 chain

Started 13 November 2026, 22:09 KST; completed 22:38 KST. **All three required links confirmed.**
ES(8) ≤ 309 may be stated as a computer-assisted result with the trust boundary below; it is not a
fully Lean-checked theorem. The complete chain is in `../ES309N20261113/README.md`.
Repository branch unchanged: `es7-night-2026-11-01`. No commit, push, root README or `math.md` change.

**14 November follow-up:** [N66 ≤ 56 is independently confirmed](followup56/VERIFY_N66_56.md).
The retained LRAT passed a new cake_lpr replay, all 319,611 clauses and 6,775 row
justifications were checked, and four additional supporting CNFs received fresh
certificates. This permits the simpler ES309 chain using only slices 18 and 19
over the 2,650 Lean rows. The original three-link audit below remains valid.

Labels: PROVED = written mathematical argument; CERTIFIED = exact `s VERIFIED UNSAT` from cake_lpr for
the specified CNF; EXACT TREE = integer replay; COMPUTED = finite controls, not a mathematical proof;
HEURISTIC = search information. None of the new conclusions is refereed.

## Live state on entry

`systemctl --user list-units 'nov13c-*' 'p2-*' 'memguard*' --no-pager` showed the N66 level-13 driver and
three searches, the slice-21 chain, E2, the D1b watcher and memguard5 running. The certified-status JSON
still gave N66 ≤ 57. Slice 21 had neither DONE nor STUCK. E2's only status entry was its CNF hash;
D1b had not started and had no status file. The thread helper reported six free threads.

The live guard script is version 5: 6,000 MiB verifier track, 24,000 MiB global research total, and a
95% clean-stop threshold. It replaces the kernel limit with `memory.high`, retaining the launch limit
as its stop threshold. `MEMORY_POLICY.txt` describes an older guard version. New jobs are sized below
80% of their launch limit, with swap disabled; no cap was raised.

## (a) N66 ≤ 57: CONFIRMED — CERTIFIED

`tools/rows66.py` reconstructs all 70 Young diagrams, cell sets, refined domains, the six-order test,
and transposition without importing the record's code. All 7,913 used row justifications pass:
3,769 transported, 3,891 mirror, 203 core, 50 cycle. The recursive justifications use 417 templates and
204 core CNFs. Support/demand multisets and the used-row SHA agree. Transport maps are injective,
all tests hold both on the template and its image, and mirror supports are exact transposes.
This check alone is **COMPUTED**, not certification of the underlying templates.

`tools/audit_mono.py` independently enumerates the valid monolithic clause families, including guards
and chain-variable numbering. It imports neither mono66 nor coupled5 nor their checkers. It recognizes
all 206,705 clauses (206,703 distinct; two duplicates):

| family | distinct used clauses |
|---|---:|
| empty domain | 1,465 |
| excluded label | 28,419 |
| threshold | 903 |
| forced sign | 5,528 |
| growth | 34,678 |
| chain start | 5,089 |
| order transitivity | 3,342 |
| common-endpoint exclusion | 524 |
| chain-to-end implication | 6,079 |
| signotope packet | 85,888 |
| chain extension | 25,732 |
| fixed occupancy | 2 |
| justified row | 7,913 |
| sequential counter | 1,141 |

The original-clause IDs independently reconstruct the trimmed CNF byte-for-byte:
`80b55b0c2c2ef445f485901e69fda3fdbb994fc1d882b5828d9227a85a695ee7`.
This is a reconstruction from the untrimmed CNF plus independent recognition of every resulting clause,
not a fresh execution of the original trimming program. PySAT's sequential-counter encoder is a shared
dependency; the geometry enumeration is separate code. The layout has all 70 states, budget 12,
no cube and no symmetry-breaking assumptions.

Soundness (PROVED, written): assign the selectors to actual occupancy; before to x-order; thresholds to
the exact ending cap/cup labels; orientation to determinants. Assign each chain atom to existence of
its specified cap/cup and each endpoint atom to existence of a 5-cap/5-cup between those endpoints.
Every guard on a missing owner satisfies its clause. For present owners, state separation and rank
attainment give the domain clauses; monotonicity and growth follow from extending attaining chains;
chain extension follows from consecutive slopes. A 5-cap and 5-cup with common endpoints lie above and
below their chord and form a convex octagon, so the endpoint exclusion is valid. Packets are the
four-point signotope property. Fixed states are the first two points. A hole vector of weight at most
12 extends to the sequential counter's prefix-count assignment. Once all row certificates and the
fresh UNSAT proof pass, this rules out 58 points and establishes N66 ≤ 57.

`tools/recert57.sh` runs CaDiCaL 2.1.3 anew on the trimmed CNF, retaining its new LRAT, then cake_lpr.
Work directory: `/home/jay/research/data/verify309-codex-20261113`.
The fresh run returned exit 20 after 549.96 CPU seconds (550.44 wall seconds; maximum RSS 377.94 MB).
Its LRAT SHA-256 is `46305acfef8d9f3961a5f7b94f1f96a2550e995611441ae16be4562e015956cc`.
**cake_lpr returned exactly `s VERIFIED UNSAT` with a 1,000 MB heap.** No larger-heap retry was needed.
This certifies the propositional CNF. The row-certificate coverage subsequently finished successfully.
`tools/certify_new_rows.py` explicitly inherits 349 identical CNFs covered by the previous independent
`N66N20261113/VERIFY_N66.md` audit, cross-checking its per-item successful outputs. The remaining 272
are regenerated by the new streaming encoder `tools/coupled66_independent.py`; their full hashes must
match. Fresh CaDiCaL proofs select sub-CNFs, which are re-solved and accepted only on the exact cake_lpr
verdict line. This selection is not trusted as a proof checker: every selected clause is a clause of
the independently generated full CNF and cake_lpr must certify the new subproof.

**Final row result: all 621 distinct template/core CNFs covered: 272 freshly CERTIFIED, 349 inherited
from the earlier independent audit.** All 272 freshly generated full CNFs matched their recorded hashes;
all fresh subproofs produced the exact cake_lpr acceptance line. No hash, clause, transport, or certificate
failure occurred. Together with the row checks, geometric-family audit and fresh main proof, this
independently confirms **N66 ≤ 57**. N66 ≤ 58 follows immediately, without separately replaying its older
certificate. Level 13 (N66 ≤ 56) remains outside this completed result.

## (b) Slice 20: CONFIRMED — EXACT TREE

`tools/replay20.py` is a new wrapper around `scripts/omission_tree.check_tree`. It reconstructs the row
system from the pinned 2,650-row source, derives F and Lo from the actual catalog, and verifies that
the only two capacity rows are **(F,20)** and **(Lo,13)**. Every other extra row has demand one and an
exact `s VERIFIED UNSAT` entry in the certificate inventory. All 578 such supports are covered.

The wrapper traverses the master independently, derives each context's complete branch path, rejects
duplicates or missing contexts, compares stored missing/occupied sets with that path, and replays each
subtree under its path. It does not trust stored context paths or finder statistics. Artificial pending
siblings used for piecewise replay are counted and removed; the only global pending branch is state 0
missing. Residual state 0 is occupied, so this branch is impossible.

Result: **2,048 contexts; 3,468,657 nodes; 1,734,329 leaves; minimum integer margin 1; one pending leaf**.

| artifact | SHA-256 |
|---|---|
| extra rows | `d12f624f1858e8670988df864686accf1d35f4e02c7127b8c355bc918055ecee` |
| master file bytes | `ba14e314a4b86cccf7f626db055fde2f6cbced777696415cc6b052aa6d9d0c78` |
| normalized master nodes (record convention) | `15cd5892e5b11ae103902ee8beb874962562f6cc9f19cc2c304641e8f88cd9b0` |
| context hashes concatenated in numeric order | `709a345e47be19866a452ca9268644648d62c0df5b982fa5c1a78d78b4966567` |
| coupled certificate inventory | `2f065615bc44a3c5d86693f0d57b29a1b2501df68439f4e210fd1bf15661682f` |

The two master hashes differ only because their definitions differ; the normalized hash matches the
handoff. `logs/s20.jsonl` retains all 2,048 individual context hashes; `logs/s20-summary.json` summarizes.

Additional linkage check: `tools/recert_residual.py` regenerates all 578 full CNFs with the audited
RES33N encoder and compares their SHA-256 with the inventory. It inherits the 130 identical CNFs
independently replayed in VERIFY_LO and freshly re-solves/re-certifies the other 448. CNFs (compressed),
fresh LRATs and checker logs are retained under the work directory's `residual/` subdirectory.
**Final result: all 578 CNF hashes match; 448 fresh cake_lpr acceptances and 130 inherited independent
acceptances.** All 448 fresh LRAT SHA-256 hashes also match the original inventory. The row soundness
and the actual certified CNFs are therefore linked, rather than inferred from inventory wording alone.

## Composition check and an important distinction

The nine F-rows were independently re-counted: each has 28 states and demand 6; each of the 84 F-states
occurs exactly three times. Thus 3h(F) ≥ 54, hence h(F) ≥ 18 (`logs/f18.json`). With h(Lo) ≥ 13 and
the previously Lean-checked exclusion of budgets ≤32, a putative actual residual set with at most
33 holes has exactly 33 holes and h(F) ∈ {18,19,20}. Slices 18 and 19 over the Lean rows alone were
already independently replayed in VERIFY_LO; slice 20 is replayed above. This gives at least 34 holes
for every actual residual configuration and hence residual population ≤120 (empty configurations
are immediate). N5 is not used.

**Do not infer `Excludes2650Zero 33`.** That assertion for arbitrary Boolean vectors over only the
2,650 rows is false: those rows admit 33-hole vectors. The new conclusion applies to actual residual
configurations using the additional geometric capacity/coupled rows. A Lean export must carry those
extra hypotheses or prove their transfer; it cannot simply reuse the bridge with an unproved
`Excludes2650Zero 33` argument.

The inspected existing composition theorem is
`ErdosSzekeres.Omission.Partition.forces_of_population_bounds` in `PopulationBounds.lean`, with an
explicit positivity premise. The balanced theorem is
`ErdosSzekeres.Omission.Compact310.balanced_population_187` in
`experiments/omission-compact-checker-2026-11-05/assembly/Final310Compact.lean`.
It combines balanced 187 and residual 120 into the forcing threshold 187+120+2=309.
These existing components were previously Lean-checked; this audit inspected their source signatures
but did not rerun a Lean build. The new residual-120 proof and its attachment to that theorem are not
Lean-checked here.

## (c) Residual coupled encoder: soundness CONFIRMED — PROVED (written), with COMPUTED controls

Audited `RES33N20261113/tools/coupled.py` and its `common.py`, including the source-bound clauses,
the excluded label (1,6), the plain-domain triple table, and constant-literal simplification.
For an actual residual configuration use pair labels
`d(u,v) = (6 − longest cap starting with (u,v), longest cup ending with (u,v) − 1)` for u < v.
The first coordinate is in 1..4 (no 6-cap), and the second is in 1..6 (no 8-cup).

| clause family | reason it holds for every real residual configuration |
|---|---|
| threshold monotonicity | thresholds of a single integer label |
| source cup bound | remove v from an attaining cup ending with (u,v); its prefix ends at u, hence d₂(u,v) ≤ f₁(u)+1 |
| empty direction and domain | state separation gives d(u,v) ∈ I(v) \\ I(u); (1,6) would give a 5-cap starting at u and a 6-cup ending at u, a forbidden junction |
| transitivity | before is the actual strict x-order |
| cap growth | a cap triple u,v,w extends a longest cap starting with (v,w) to one starting with (u,v), so d₁(v,w) > d₁(u,v) |
| cup growth | extend a longest cup ending with (u,v), giving d₂(v,w) > d₂(u,v) |
| forced sign | inspect every possible x-order; nonempty incoming-domain differences are necessary; a coordinate's non-growth rules out the corresponding cap/cup sign; permutation parity restores the requested orientation |
| signotope packets | the four triple signs of four x-ordered real points change at most once |
| convex-four equivalence | for four points in general position the circuit has a 2–2 sign split exactly when the points form a convex quadrilateral; the implemented orientation truth table is this test in arbitrary owner order |
| no octagon | if eight points are not all extreme, an interior point lies inside a triangle of three others (triangulate their hull; general position excludes triangle edges), giving a nonconvex four-subset; thus no octagon implies at least one nonconvex quadruple in every eight-subset |

Unordered threshold variables are assigned the label of the earlier-to-later pair. Orientation variables
use increasing owner index, with permutation signs for other orders. True literals remove a clause;
false literals are removed from it; duplicate/tautological simplifications preserve validity.
The plain cell differences used for the sign test are supersets of the refined admissible domains, so
their bounding-box forcing is conservative. No CNF family assumes a fact stronger than the residual
hypotheses. Thus an UNSAT support CNF proves that at least one support state is missing.

## Real-set controls (COMPUTED, not proofs)

`tools/real_geometry.py` computes all geometry and assignments with exact integers. It uses its own
random-insertion generator, rejects collinear/non-distinct-x sets, computes cap/cup ranks and maximum
convex polygon size by endpoint-chain DP, and checks the residual no-junction condition. Archived ETV
50-point sets and a 57-point residual chart are additional input fixtures, with hypotheses recomputed;
the chart's rational coordinates are scaled to integers.

- N66: **74 sets, 585,562 row evaluations, zero violations**, 69 of 70 states seen, 2,326 tight row evaluations.
- Residual: **91 sets, 273 CNFs, 6,490,402 clause evaluations, zero violations**, including arbitrary
  permutations of owner indices and complete octagon clauses on supports of size 8 or 9.

The imported residual encoder is the object under test; determinants, hull tests, labels, states and
truth assignments are independent. These controls are finite evidence and do not replace the written
soundness arguments.

## Commands and resource accounting

All longer runs use `systemd-run --user`, `CPUQuota=100%`, `MemorySwapMax=0`, and nice 15:

| unit | MemoryMax | RuntimeMaxSec | action |
|---|---:|---:|---|
| nov13c-vfy-codex-s20 | 900M | 1800 | `python -u tools/replay20.py` |
| nov13c-vfy-codex-cert57 | 1400M | 7200 | `bash tools/recert57.sh` |
| nov13c-vfy-codex-mono | 700M | 1800 | `python -u tools/audit_mono.py` |
| nov13c-vfy-codex-real | 600M | 1800 | `python -u tools/real_geometry.py` |
| nov13c-vfy-codex-suite | 3000M | 18000 | `bash tools/remaining_suite.sh` |

Python is `/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python`.
The suite waits for the fresh-proof unit, and if a 2,000 MB checker heap is necessary it waits for E2,
the D1b watcher and D1b itself before using it. New row subproofs use a 700 MB heap. The largest simultaneous
new compute allocation before the suite was four threads; the entry helper counted ten already allocated.
No research unit was stopped by this audit or by the memory guard during these checks. The suite was
invoked a second time after successful completion to add the residual-row checks; completed N66
certificates were skipped. There was no memory-failure retry. Sampled total research anonymous memory
plus swap stayed around 7.4–8.5 GiB; sampled research swap was zero. The main solver's recorded maximum
RSS was 377.94 MB, and the main proof checker used approximately 1,006 MiB with its 1,000 MB heap.
These are logs/snapshots, not a continuously sampled peak guarantee. Caps remained unchanged.

## Final status, limitations and artifacts

`logs/final-summary.json` aggregates the required verdicts; `tools/final_receipts.py` refuses incomplete
coverage and checks each fresh cake_lpr log for the exact acceptance line. No required check failed.
`logs/n66-row-certificates.jsonl` and `logs/residual-row-certificates.jsonl` contain the per-CNF receipts.
`logs/input-hashes.json` pins source and inherited-verifier artifacts; `logs/binary-hashes.json` pins
CaDiCaL and cake_lpr. Fresh proof objects are in the work directory above, not committed or copied into
Git. The slice-20 context files and the slice-19 archive also remain in their original external work
directories. Do not delete those directories without arranging archival preservation.

Historical live-state snapshot at 22:38 KST on 13 November (superseded by
the follow-up for N66):

- All `nov13c-vfy-codex-*` units completed successfully and no longer appear as running or failed.
- The best certified N66 bound remains 57; level 13 (≤56) is still running.
- Slice 21's driver produced DONE at 22:22:36, reporting 19,333,541 nodes and minimum margin 1.
  This audit did not independently replay slice 21 and does not use it. A new background chain7 unit
  is running. The DONE receipt is archived as `logs/background-s21-DONE.json`.
- E2 remains running with only its initial CNF-hash status entry; D1b remains queued, with no verdict.
- Since research jobs remain, memguard5 and the D1b watcher were intentionally left running.

The fully Lean-checked upgrade, ES(8) ≤308 and the optional robustness/side problems remain
open or outside this audit. N66 ≤56 was outside the original audit and is now
confirmed in the linked follow-up; its extra fresh 600-second main solve was
UNKNOWN, while the retained proof passed independent cake replay. No fresh
literature search was performed; the comparison in the ES309
record is explicitly attributed to `NOVELTY20261113B`, including its unread-source caveats.
No web request, commit, push, branch change, root README edit, `math.md` edit, or FASTBB README edit was made.
