# Verification records

The [publication audit](PUBLICATION_AUDIT.md#disposition-sanitized-history)
documents the removal of local machine paths from Git history. Proof sources
and certificate data are unchanged; path-bearing records and their dependent
hashes are normalized. Earlier GitHub run/commit links refer to the original
private repository and may not resolve in the public replacement. New hosted
results are available in the [CI workflow](https://github.com/CuteSurtr/erdos-szekeres-lean/actions/workflows/ci.yml).

## ES(8) ≤ 313 — 12 October 2026

The [313 record](../experiments/omission-final313-2026-10-11/README.md) closes
the conditional bridge. Its 437,580-leaf certificate was replayed exactly in
Python and exported to 10,325 Lean parts plus catalog and root; every module
passed the kernel with an audited axiom report and a recorded object hash.
`forces_convex_octagon_313 : ForcesConvexNGon 313 8` and
`convex_octagon_of_card_ge_313` depend only on `propext`, `Classical.choice`
and `Quot.sound`. The check took about 120 CPU-hours on one machine and is not
part of the hosted CI workflow; the maintained library build and its 587-root
audit are unchanged.

## Erdős–Szekeres lower bound — 11 October 2026

Seven new modules in [ErdosSzekeres/LowerBound](../ErdosSzekeres/LowerBound)
prove the 1961 construction: for every $`n\ge3`$ there are $`2^{n-2}`$ real
points in general position with no $`n`$ points in convex position. The
principal roots are `ErdosSzekeres.not_forcesConvexNGon_two_pow`,
`conjecturedBound_le_of_forces`, `octagon_lower_bound` and
`sixtyFive_le_esNumber_eight`, so $`65\le\mathrm{ES}(8)`$. Except for the new
`esNumber n := sInf {N | ForcesConvexNGon N n}`, whose defining set is nonempty
for $`n\ge3`$ by `Suk.classical_upper_bound`, the statements use only the
unchanged definitions `GeneralPosition`, `HasConvexNGon`, `ForcesConvexNGon`
and `conjecturedBound`. The proof contains no finite certificate, `decide` or
native evaluation.

The maintained library builds all **3,308 jobs** with `--wfail`. Sixteen new
roots extend the audit to **587 theorems**; the
[saved audit](validation/axiom-audit-lower-bound-2026-10-11.txt) uses only
`propext`, `Classical.choice` and `Quot.sound`. The ordinary Python suite now
reports 125 tests: 99 pass and 26 optional tests skip. Its three new tests
check the exact integer witnesses of
[es_lower_bound_witness.py](../scripts/es_lower_bound_witness.py) for
$`n=3,\ldots,8`$, including general position and a largest convex subset of
exactly $`n-1`$ points, and compare its convex-subset dynamic program with
brute force. These numerical controls are independent of the Lean proof.

## Rank-aware search, four rows and normalization — 10 October 2026

The [four-core certificate bundle](../experiments/omission-residual32-rank-certificates-2026-10-10/README.md)
checks eight new Lean modules and sixteen theorem roots. Supports have sizes
13, 13, 13 and 12. Their literal refutations contain 503, 726, 582 and 795
clauses, with 419, 605, 450 and 659 RUP steps. The second and fourth proofs
use 16 and 3 source-cup clauses. The [kernel record](../experiments/omission-residual32-rank-certificates-2026-10-10/kernel-check.json)
and [complete axiom audit](../experiments/omission-residual32-rank-certificates-2026-10-10/axioms.txt)
bind the actual geometric `hole_bound` theorems. Twelve corruption controls
independently test the proof replay; the source exporter has seven controls,
including fresh Lean rejection of altered direction and threshold literals.

The [normalization bundle](../experiments/omission-residual-rank-normalization-2026-10-10/README.md)
checks two further modules and twelve roots. Its exact-catalog theorem proves
that source-height clipping preserves abstract coupled-model satisfiability.
Its [axiom audit](../experiments/omission-residual-rank-normalization-2026-10-10/axioms.txt)
uses only the standard axioms. Five controls check source identity and a
nontrivial clipped assignment with fifteen changed labels. This theorem
explicitly excludes additional equations for exact attained ranks.

The portable continuation gate now checks **41 modules and 87 theorem roots**
from source. It runs both new bundles' finite preflights and rejection controls
before compiling, and rejects warnings, proof placeholders, custom axioms and
native evaluation. The hosted workflow also enables all source-cup exporter
kernel controls and the new standard-library discovery/catalog replays.

The maintained library still builds all 3,301 jobs with `--wfail`; its 571-root
audit is unchanged. The ordinary Python suite now reports 122 tests: 96 pass
and 26 optional tests skip. Enabling the new source-cup integration suite
passes all seven controls, including its three optional Lean checks.

The [2,650-row catalog replay](../experiments/omission-residual32-rank-global-2026-10-10/README.md)
binds the unchanged 2,646-row prefix and all four new supports. Its
uncompressed SHA-256 is
`e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6`.
Exact integer replays verify four successive 33-hole strictness witnesses and
elimination of the saved 306-vertex single-swap component. The component does
not exhaust all 33-hole assignments. Neither it nor a timed-out global solver
run supplies a 32-hole exclusion. **The completed planar bound remains 314.**

## Attained source-cup rank — 10 October 2026

The [attained-rank bundle](../experiments/omission-residual-rank-attainment-2026-10-10/README.md)
proves the source-height bound and its catalog, configuration and coupled-clause
forms. Its [kernel record](../experiments/omission-residual-rank-attainment-2026-10-10/kernel-check.json)
records fresh serial builds of two modules; the [six-root axiom audit](../experiments/omission-residual-rank-attainment-2026-10-10/axioms.txt)
uses only `propext`, `Classical.choice` and `Quot.sound`. Source and dependency
hashes are bound by the manifest. Two negative controls reject changed inputs.

At the attained-rank checkpoint, the portable continuation gate included **31 modules and 59 audit roots**.
The preceding 29-module build and this two-module build are separately recorded;
the hosted workflow rebuilds all 31 from source and rejects warnings, proof
placeholders, custom axioms and native evaluation. The maintained library and
its 571-root audit are unchanged.

The [finite replay](../experiments/omission-residual-rank-attainment-2026-10-10/assessment/replay.py)
reproduces all 23,562 directed domains and 596,904 unordered triple comparisons.
The new bound removes 13,832 labels from 4,555 domains, with no newly incompatible
pairs or changed forced-sign triples. This finite assessment is separate from
the Lean proof. Neither supplies a global hole bound or the 313-point theorem.
CI replays the assessment without an external solver.

## Relaxed Sixth template and resumed 313 search — 10 October 2026

The [new geometric bundle](../experiments/omission-residual32-sixth-relaxed-2026-10-10/README.md)
proves a 41-condition template and 48 concrete necessary omission rows for
actual residual configurations. Its [kernel record](../experiments/omission-residual32-sixth-relaxed-2026-10-10/kernel-check.json)
checks nine modules and ten audited declarations; its
[axiom output](../experiments/omission-residual32-sixth-relaxed-2026-10-10/axioms.txt)
contains only the standard Lean axioms. The independent finite checker
replays 1,032 RUP steps, all literal maps and the exact 2,646-row catalog
extension; two negative controls reject corrupted certificates or maps.

At this checkpoint, the portable continuation gate included **29 modules and 53 audit roots**.
The [fresh combined build record](validation/residual32-2646-checks-2026-10-10.json)
and [complete axiom output](validation/residual32-2646-axioms-2026-10-10.txt)
identify this checkpoint. This rebuild uses fresh objects and rejects compiler
warnings, proof placeholders, custom axioms and native evaluation in every
compiled source. The maintained library and its 571-root audit are unchanged.

The [local-search checker](../experiments/omission-residual32-primal-resume-2026-10-10/check.py)
independently proves by integer replay that the saved 306-vertex, 3,650-edge
33-hole graph is one entire connected component under single swaps with
state zero occupied. It starts from one seed and checks closure and
reachability. No vertex permits removal of a hole. Seven negative controls
include a disconnected union that must not be mistaken for one component.
The three additional 32-hole near-models each fail one row. The search over
five million 34-hole assignments was capped and is not exhaustive. These
are Python checks of finite search evidence, not Lean population bounds.

The [SAT/PB bundle](../experiments/omission-residual32-sat-resume-2026-10-10/README.md)
records two timed-out SAT runs and one timed-out native pseudo-Boolean run.
Three local counter-encoding tests and one integer-serialization test pass;
the OPB generator reproduces the saved input hash. CI also replays the local
component, the serialization test, and the exact OPB input without installing
a solver. The ordinary Python suite reports 115 tests: 92 pass and 23 optional
tests are skipped. No global 32-hole exclusion, geometric realization, or 313-point
theorem is claimed by any of these search diagnostics.

## Residual32 witness and geometric strengthening — 10 October 2026

The old 2,469-row relaxation now has a Lean-checked 32-hole witness, so no
universal 33-hole bound follows from those rows. The
[case-4 record](../experiments/omission-residual32-case4-2026-10-10/kernel-check.json)
checks two modules and fifteen conclusions. Cases 2 and 7 remain partial
integer searches; no complete exclusions are claimed for them.

The [new coupled core](../experiments/omission-residual32-witness-coupled-2026-10-10/kernel-check.json)
checks three modules and eleven conclusions, including a valid geometric
row, strict strengthening, and nonrealizability of that exact old witness.
The independent checker replays all 258 RUP steps and thirteen deletion
models; seven corruption/replay controls pass. These deletion models are
necessary-constraint assignments, not real-point realizations.

The [generic Sixth template](../experiments/omission-residual32-sixth-variants-2026-10-10/kernel-check.json)
checks three modules and four conclusions. Its 29 additional literal supports
are only Python diagnostics and all follow from individual old rows. The
[Fourth128 family](../experiments/omission-residual32-fourth-global-variants-2026-10-10/kernel-check.json)
checks ten modules and ten audited roots in 352.453 seconds. All 128 rows are
valid for actual configurations. None passes the single-old-row implication
test; full independence is not claimed. An independent review checked the
ordered maps, support bindings, eight proof chunks and complete assembly.

The [ordered129 bridge](../experiments/omission-residual32-added-rows-2026-10-10/kernel-check.json)
checks `Residual32AddedRows.literal_binding` and `all_rows` in 13.979 seconds.
Its preflight binds the unchanged old prefix and the exact new suffix of
the 2,598-row search source. A changed tail index is rejected before Lean.
The strengthened arithmetic search remains inconclusive; its best 32-hole
near-model violates original row 205 by one.

These are **19 new standalone Lean modules and 42 audited conclusions**.
The portable gate additionally rebuilds the old literal Catalog, for 20
modules and 43 audited conclusions in total. Only `propext`,
`Classical.choice`, and `Quot.sound` occur in the local proof audits.
The [combined local audit](validation/residual32-strengthening-axioms-2026-10-10.txt)
and [source-bound record](validation/residual32-strengthening-checks-2026-10-10.json)
identify this checkpoint. The gate scans every compiled source for proof
placeholders, custom axiom
declarations and native-evaluation tokens. It regenerates the coupled core,
checks exact finite diagnostics, and builds fresh experiment objects on Linux
or macOS without relying on platform-specific saved object hashes.

```sh
lake env python3 scripts/check_residual32_continuation.py
```

This command is now an explicit hosted CI step. Local results above do not
assert that a hosted run has completed; the exact pushed commit's Actions
result must be checked separately. All 3,929 inputs of the completed 314-point
assembly were rehashed unchanged during this continuation. That bound remains
the completed global result. See [MATH.md](MATH.md) for the mathematical scope.

Earlier sections below are historical checkpoints. Their unresolved-old-model
status is superseded by the exact witness described above.

## Residual32 catalog transfer and contextual proofs — 10 October 2026 continuation

The [transfer gate](../experiments/omission-residual32-transfer-2026-10-10/kernel-check.json)
passes six fresh modules and audits 17 named roots. It proves every one of the
2,469 frozen literal inequalities for the same actual residual configuration,
including all twelve final rounded consequences and the exact population
complement. Five actual-configuration exclusions and two merged-parent
exclusions also pass. All reported axioms are `propext`, `Classical.choice`,
and `Quot.sound`. The checker rehashes 747 prerequisite objects/configurations
and 72 external Lean sources; a corrupted original catalog is rejected before
compilation. See its [complete validation](../experiments/omission-residual32-transfer-2026-10-10/validation.json).

The [five original contextual certificates](../experiments/omission-residual32-context-certificates-2026-10-10/kernel-check.json)
pass seven fresh modules with explicit row-validity premises. Their checker
validates archived source, decompressed source, diagnostic, frozen contexts,
generator, exporter and generated-file identities before compiling. The
negative preflight test rejects a mismatched source. The separate
[zero-state check](../experiments/omission-residual32-context-certificates-2026-10-10/zero-state-check.json)
proves actual occupancy of state zero for every nonempty residual configuration.

The [six resumed subtree proofs](../experiments/omission-residual32-resume-lean-2026-10-10/kernel-check.json)
pass seven fresh modules and audit twelve conclusions: six conditional
arithmetic exclusions and six actual geometric corollaries. Their 94 nodes,
44 binary splits and 50 weighted leaves were independently reviewed against
the inherited contexts and frozen source. All 853 recorded prerequisite/source
identities match; an altered subtree archive is rejected before compilation.
Only the same three standard axioms occur. The fresh check took 58.595 seconds.

The [resumed arithmetic tree](../experiments/omission-residual32-resume-2026-10-10/README.md)
and sixteen closed conditional subtrees pass independent unbounded-integer
replay, with six corruption controls. This evidence is separate from Lean:
eight leaves remain open, within three original contexts, and the full tree
is not a checked 32-hole exclusion. Six of the sixteen new conditional
subtrees additionally have the Lean proofs above; ten remain integer-only.
The [balanced SAT run](../experiments/omission-balanced62-sat-2026-10-10/README.md)
ended `UNKNOWN` at 600 seconds. It is not an infeasibility certificate.

All 3,929 input identities of the completed 314-point gate were rehashed during
this continuation and remained unchanged. These new standalone bundles are
checked separately; the maintained library's CI does not implicitly build them.
The [final packaging record](validation/residual32-continuation-checks-2026-10-10.json)
binds all 21 new Lean sources and the bundle records. It records eight passing
negative controls, matching artifact identities, and no proof placeholders or
custom axiom declarations in those sources.

## Hosted CI repair — 10 October 2026

GitHub [run 38011126753](https://github.com/CuteSurtr/erdos-szekeres-lean/actions/runs/38011126753)
succeeded on commit `2359347ecc880b8b932b1e78dd5d02ab0166fff3` in 1h18m57s.
It passed the full 3,301-job library build, the 571-theorem standard-axiom audit,
92 Python tests (23 conditional skips), and all 26 opted-in Lean integration
checks. No proof checks were removed. The workflow limits compiler/build
parallelism, provisions extra swap, cancels superseded runs, and saves the
project build cache only after all checks pass. The cold full-library stage
took 43m03s, including 2,324 seconds in `GeneralResidualBlocks`; the verified
build cache was successfully saved. This hosted result is distinct from the
standalone final 314-point gate and the new standalone transfer checks.

## Closed 314-point theorem — 10 October 2026

The [complete final gate](../experiments/omission-global-assembly-2026-10-10/global-cover-314-check.json)
passes all eight assembly modules and rehashes **3,929 unchanged inputs**.
Its SHA-256 is `a16dea3164f6269ebb985595a513c886ff73993b6d381e626d704b80fee1d016`.
The [full final axiom output](../experiments/omission-global-assembly-2026-10-10/global-cover-314-axioms.txt)
checks `ErdosSzekeres.Omission.forces_convex_octagon_314` and its explicit
real-point form, with only `propext`, `Classical.choice` and `Quot.sound`.
The theorem has no undischarged row, arithmetic or coordinate hypotheses.

The residual31 arithmetic proof passes all **1,218 modules**: 1,216 parts,
catalog and root, covering 50,945 leaves. The balanced61 proof has 22,318
leaves in 504 modules. Both source-only archives were independently checked
against every exported source hash and scanned for proof placeholders and
native-evaluation tokens. The 264 loose source files in the 571-root library
audit below remain byte-for-byte unchanged. No additional library build or
test-suite run is claimed for this certificate-only completion.

The [additional validation record](validation/octagon-314-checks-2026-10-10.json)
binds these independent checks. The observed final gate took 444.789 seconds
and reached 31,645,417,472 bytes of child-process resident memory (about 29.47
GiB). These are measurements from this Mac, not portable resource guarantees.
The current GitHub build remains separate from these completed local checks.

## Structural geometry and uniform finite saving — 10 October 2026

The complete library passes `lake build --wfail` (**3,301 jobs**). The
[saved audit](validation/axiom-audit-structural-2026-10-10.txt) checks **571
named roots**, using only `propext`, `Classical.choice`, and `Quot.sound`.
The [source-bound record](validation/structural-checks-2026-10-10.json)
includes every maintained/standalone Lean source and confirms the old 316/317
global proof inputs remain unchanged.

New results are the second nine-state omission row, its generic template,
two supporting-edge insertion theorems, six uniform factorial-saving
declarations, and structural proofs of three nine-state rows. The latter
include two new supports beyond the original CNF compatibility template.
All new Lean passed the kernel. The sized template
exporter also reproduced the prior fifth thirteen-state template byte-for-byte.
The unchanged 115-test checkpoint below remains the Python-suite evidence;
no unrelated test rerun is counted as a new result.

The earlier records below describe their respective checkpoints.

The separate [315-point final gate](../experiments/omission-global-assembly-2026-10-10/global-cover-315-check.json)
is now complete: all eight assembly modules passed, and all 1,795 bound inputs
were rehashed unchanged. The final ordinary real-point theorem has only the
three standard axioms. The balanced arithmetic proof contains 22,318 leaves in
502 parts, plus catalog and root. Full source archives, cut transfers, audits
and resource measurements are preserved in the global/cover artifacts.

## Smaller obstructions and finite HMPT refinement — 10 October 2026

The complete library passes `lake build --wfail` (**3,293 jobs**). The
[current saved audit](validation/axiom-audit-recovery-2026-10-10.txt) checks
**544 named roots**, with only `propext`, `Classical.choice`, and `Quot.sound`.
The [115-test run](validation/recovery-tests-2026-10-10.txt) has 92 passes and
23 optional skips. All 21 coupled certificate replay and corruption controls
pass. The [source-bound record](validation/recovery-checks-2026-10-10.json)
contains source hashes and the clean placeholder scan.

New checked results comprise 28 fifth-template maps; eleven- and nine-state
geometric obstructions; nine finite binomial/factorial HMPT refinement theorems;
and five endpoint-budget analysis theorems. Their separate proof bundles retain
full audits and exact claims. A standalone kernel example proves strictness of
the new exponent formula. The published asymptotic coefficient is unchanged.

All 972 inputs of the completed 316-point gate and 822 inputs of the earlier
317-point gate still match after this build. The unfinished 315/314 certificate
runs are not counted as completed theorems here. GitHub run `37991641955` was
cancelled after a runner shutdown signal, with build exit 143; the remote build
did not complete. Local proof checks and audits succeeded. The workflow now builds the
large coupled proof families sequentially, then runs the full build and existing
checks. This reduces simultaneous memory demand; it does not identify the cause
of the earlier shutdowns. Mathlib download caching remains enabled.

Some comments in the frozen conditional-interface sources still call their
numerical premises targets. Those comments describe their original checkpoint;
the separate completed global assemblies discharge those premises. Their source
bytes remain unchanged to preserve the checked certificate bindings.



## Closed 316-point theorem and expanded geometry — 10 October 2026

The library passes `lake build --wfail` (**3,283 jobs**). The
[full current audit](validation/axiom-audit-extensions-2026-10-10.txt) checks
**517 roots**, accepting only `propext`, `Classical.choice`, and `Quot.sound`.
The [109-test run](validation/extensions-tests-2026-10-10.txt) has 86 passes
and 23 optional integration/solver skips; all 15 coupled replay and damage
controls pass. The [source-bound record](validation/extensions-checks-2026-10-10.json)
identifies this exact checkpoint.

The separate [316-point gate](../experiments/omission-global-assembly-2026-10-10/global-cover-316-check.json)
is complete, including the final real-point theorem and standard-axiom audit.
All 972 inputs of that gate and 822 inputs of the earlier 317-point gate were
rehashed after the library rebuild: none changed. The new balanced arithmetic
archive contains only 94 regular Lean source files. A scan of all 241 loose
project Lean sources, including vendored prerequisites and standalone research
files, finds no proof placeholders, custom axiom declarations or native proofs.

Five coupled core obstructions, the first/second template families, three third
template variants, 24 fourth template variants, and the 14-state two-hole theorem
are checked. Separately, all twelve modules of the frozen 57-row union proof
pass with 203 unchanged inputs. They prove the scoped nine/48 independence and
redundancy classification; they do not establish a new global bound by themselves.

Remote run `37988107276` was cancelled with build exit code 143; its later checks
were skipped. The cause is not established. This is distinct from the successful
local build, audit, finite certificate gate and test run.

The records below are historical checkpoints. Their old statements about
unfinished 316-point work do not describe the completed theorem above.


## Coupled geometric obstructions — 10 October 2026

The default library passes `lake build --wfail` (**3,259 jobs**) with both
`CoupledCore13.hole_bound` and `CoupledCoreSecond.hole_bound` included. The
[complete axiom report](validation/axiom-audit-coupled-2026-10-10.txt) checks
**483 named roots** and accepts only `propext`, `Classical.choice` and
`Quot.sound`. The six added library modules and standalone first strictness
proof contain no proof placeholders, custom axioms or native-evaluation axioms.
The [source-bound record](validation/coupled-checks-2026-10-10.json) states the
exact scope; compatible-template experiments are not counted in this snapshot.

The [Python run](validation/coupled-tests-2026-10-10.txt) has 100 tests:
77 pass and 23 optional integration/solver controls skip in the standard-library
environment. All six new coupled-proof controls pass, including exact replay
of both derivations, all 26 deletion witnesses, formula-damage rejection and
rejection of an invalid final derivation even after its hash is updated.
Earlier full integration checks remain recorded below.

The two proof bundles preserve their own direct Lean audits and exact source
formula identities. All 822 inputs of the completed 317-point proof were
rehashed after this library build and still matched. GitHub run `37984305688`
was cancelled on both attempts, with the build process returning 143; those
remote attempts did not complete, despite the successful local build.

## Closed 317-point theorem — 10 October 2026

The default library passes `lake build --wfail` (**3,253 jobs**). The
[complete current axiom audit](validation/axiom-audit-cover-2026-10-10.txt)
passes for **475 named roots**, including Suk 2016, HMPT 2020, the new cut
soundness, dyadic counting, block constraints and orientation helpers. Only
`propext`, `Classical.choice` and `Quot.sound` occur. All **90 Python tests**
pass with optional solvers and Lean integration controls enabled, with no skips;
the [full output](validation/cover-tests-2026-10-10.txt) is preserved.

Separately, the [complete global certificate gate](../experiments/omission-global-assembly-2026-10-10/global-cover-317-check.json)
passes for `ErdosSzekeres.Omission.forces_convex_octagon_317` and its explicit
real-point form `convex_octagon_of_card_ge_317`. The
[unabridged final axiom output](../experiments/omission-global-assembly-2026-10-10/global-cover-317-axioms.txt)
contains only the standard three axioms. The theorem has no unproved geometry,
arithmetic or literal-row assumptions. It is checked through the separate
certificate workflow, not silently included in default-library CI.

The new route checks 17 balanced arithmetic parts and 149 residual arithmetic
parts, both complete roots, 622 derived cuts, all catalog bridges and the
existing geometric prerequisites. The large older partial trees are not
needed. Source-only archives, exact check records, and reproduction instructions
are in the [cover artifact](../experiments/omission-cover-certificates-2026-10-10/README.md)
and [assembly artifact](../experiments/omission-global-assembly-2026-10-10/README.md).
After the library rebuild, every library object bound by the successful final
317 record still had its recorded hash.

A separate six-root audit verifies an abstract 32-hole residual witness against
all original rows and all 45 additional geometric rows. It is not a real-point
realization. Stronger 316/315/314 draft assemblies are explicitly unproved.

The [source manifest](validation/source-manifest-cover-2026-10-10.json) records
the current source inventory and checks. No proof placeholders, native-evaluation
axioms or custom axioms occur in these maintained finished sources or new
source archives. Git tracks no cache directories or compiled build artifacts.
Third-party attribution remains in [THIRD_PARTY.md](THIRD_PARTY.md).

All dated records below are historical checkpoints. Statements there that a
317-point proof was unfinished describe the earlier state, not the current one.

## Additional rows and parameter barrier — 2026-10-10

The library builds with warnings treated as errors (**3,247 jobs**). The
[new full axiom audit](validation/axiom-audit-research-2026-10-10.txt) passes
for **453 named roots**, including all nine new maintained results. Only
`propext`, `Classical.choice` and `Quot.sound` occur. All **70 tests** pass
with optional solvers and Lean controls enabled; see the
[test output](validation/research-tests-2026-10-10.txt) and
[source-bound validation record](validation/research-checks-2026-10-10.json).
The scan of **163 loose Lean sources** finds no placeholders, custom axioms
or `native_decide`. Git tracks no cache directories or compiled outputs.

The [separate additional-row artifact](../experiments/omission-additional-rows-2026-10-10/README.md)
was rebuilt from the preserved catalog and all three source modules. Its
10 audited roots include the reused catalog, the individual cycle and block
witness checks, and the combined irredundancy theorem. The maintained geometry
proves every new row for actual residual configurations; the standalone
witnesses prove independence as Boolean constraints. Neither asserts a
stronger cardinality bound. Literal-alignment tests verify the candidate
data, and negative controls confirm that Lean rejects a reversed cycle and
collapsed block thresholds.

The [latest residual batch](../experiments/omission-residual-progress-2026-10-10.json)
adds **40 parts and 1,765 leaves**, with matching source/object hashes and
standard-axiom reports. Cumulative progress is **470/3,411 parts** and
**20,028/145,474 leaves**. The record inherits earlier checks through the
hashed previous checkpoint. The residual root remains unchecked.

The [research report](RESEARCH_2026-10-10.md) records the literature assessment,
the exact fixed-scale HMPT optimization barrier, and unsuccessful numerical
and certificate-pruning experiments. No global improvement is claimed.

## Certificate linking and parallel checks — 2026-10-09

All **67 tests** pass with optional solvers and Lean controls enabled; the
[saved test output](validation/omission-assembly-tests-2026-10-09.txt) and
[validation record](validation/omission-assembly-checks-2026-10-09.json)
identify the checked tooling sources. GitHub validation passed for tooling
commit `b7c189b`, including the main library build, 444-root audit and Lean
integration controls. A fresh local audit also passed for all **444 named
roots**. The scan of **158 loose Lean sources** found no placeholders or
custom axioms. The additional source is a standalone import control, not a new
global theorem in the default library.

The parallel arithmetic checker builds the catalog first, checks independent
parts with one coordinating record writer, and builds the root only after all
parts succeed. A selected parallel run stays incomplete; resuming a complete
control tree preserves its existing records and checks the root. A corrupted
part is rejected and prevents root checking.

The balanced geometry exporter and checker now support a distinct arithmetic
module prefix, including the occupancy bridge. All **900 arithmetic sources**
and **86 geometry/occupancy sources** match their historical versions after
reversing only import-name changes. The
[fresh balanced rebuild record](../experiments/omission-linked-balanced-2026-10-09.json)
records the catalog and **72 of 898 parts** checked under their new names;
it does not relabel historical
compiled objects as fresh checks. Its root and renamed geometry remain pending.

The [production import control](../experiments/omission-linked-control-2026-10-09.json)
successfully loads actual balanced `Part00000` and residual `Part00380` in one
Lean process. Both catalog theorems and both subtree theorems pass their axiom
audits. This checks coexistence of production proof chunks, not a closed global
bound. See the [assembly guide](OMISSION_ASSEMBLY.md) for reproduction and the
remaining full-root composition.

The [fifth residual batch](../experiments/omission-residual-progress-2026-10-09-batch5.json)
adds **50 parts and 2,211 leaves**. The cumulative documented frontier is now
**430 of 3,411 parts**, covering **18,263 of 145,474 leaves**. Every new source
and compiled-output hash matches its successful check record; the earlier
progress is inherited through the explicitly hashed fourth-batch record.
The full residual root and the global bound remain unproved.

## Complete residual geometric transfer — 2026-10-09

The main `lake build --wfail` passes with **3,245 jobs**. The
[current full audit](validation/axiom-audit-residual-2026-10-09.txt) covers
**444 named roots**, including 94 added roots for the residual geometry and
Baek prerequisite. Only `propext`, `Classical.choice` and `Quot.sound` occur.
All **63 Python tests** pass with optional solvers and Lean controls enabled.

The separate [residual artifact](../experiments/omission-residual-geometry-2026-10-09/README.md)
checks **39 cycle modules and 24 block/composition modules**, covering every
one of the 1,187 residual rows. Three additional reduction theorems are audited.
`all_geometric_rows` has only actual geometric restrictions as premises;
`feasible_holes` constructs the complete Boolean hole vector and proves its
exact cardinality complement. The population bound and global numerical
conclusion remain conditional on `ExcludesThirtyHoles`.

The artifact manifest verifies all successful prerequisite bindings, generated
source hashes, compiled output hashes and archived source contents. All 63
geometric sources reproduce byte for byte. The scan covers **157 loose Lean
files**, plus the generated archives, with no placeholders or custom axioms.
Git tracks no cache directories or compiled artifacts. The 13 new geometry
modules contain 1,433 lines; 16 separately attributed Apache-2.0 modules supply
the remaining Baek proof dependencies. Earlier immutable artifact records are
preserved.

The [third residual batch](../experiments/omission-residual-progress-2026-10-09-batch3.json)
adds 30 parts and 1,304 leaves, bringing the checked frontier to **360 parts
and 15,131 leaves**. This is a partial arithmetic result, not a root exclusion. The
[fourth batch](../experiments/omission-residual-progress-2026-10-09-batch4.json)
adds another 20 parts and 921 leaves, including eight independently checked
parts whose identical prerequisite bindings and output hashes were verified
before merging their records. That checkpoint reached **380 of 3,411 parts**
and **16,052 of 145,474 leaves**. Across the 45-minute session, 50 parts and
2,225 leaves were added; the full residual root remains unchecked.

Lean accepts the literal residual cycle and block controls and rejects a
corrupted cyclic order and collapsed compression thresholds. A further control
builds two complete small arithmetic trees with distinct module prefixes and
imports them together. This addresses the exporter's historical module-name
collision; it does not pretend that production certificates were rebuilt under
new imports. See the [updated remaining-work estimate](ES8_REMAINING.md).

## Complete geometric partition — 2026-10-09

The main `lake build --wfail` passes with **3,216 jobs**. The
[current full audit](validation/axiom-audit-partition-2026-10-09.txt) covers
**350 named roots**, including all 73 public theorems in the eight new partition
modules. Only `propext`, `Classical.choice` and `Quot.sound` occur. All **55 Python
tests** pass with the optional solvers and Lean integration controls enabled.
The separate
[composition artifact](../experiments/omission-partition-2026-10-09/README.md)
checks four more theorems against the previously verified balanced certificate.

The complete partition includes actual induced configurations, an exact
disjoint cover, the three-chain argument, and every avoidance and junction
restriction. The resulting `OmissionBalanced.forces_317_of_residual_123` still
has the unproved `Partition.ResidualBound 123` hypothesis. The unconditional
structural conclusion extracts at least 124 residual chart points from any
putative octagon-free set of at least 317 real points. Neither theorem proves
the global bound without the residual population argument.

The validation manifest records the full source inventory, checks the saved
balanced prerequisite bindings and stores the exact standalone axiom output.
The large certificate trees are not rebuilt at this checkpoint; their compiled
objects match the earlier successful check records. Earlier records below
remain historical and are not overwritten.

The scan covers **127 loose maintained Lean files** with no proof placeholders
or custom axioms. Git tracks no caches or compiled outputs. The source bindings
of all 86 balanced geometry checks and their 114 prerequisite inputs match the
previous successful records; the new manifest also records the adapted
upstream source hashes.

## Projective/root transfer — 2026-10-09

The main `lake build --wfail` passes with **3,208 jobs**. The
[saved audit](validation/axiom-audit-projective-2026-10-09.txt) passes for
**277 named roots**, including the eight new projective-transfer theorems.
Only `propext`, `Classical.choice` and `Quot.sound` occur. All **55 Python tests**
pass with the optional solvers and Lean integration controls enabled.

`ErdosSzekeres.Omission.forces_317_of_asymmetric_315` is conditional on
`AsymmetricBound 315`, which remains unproved. Its audit certifies that
conditional statement, not ES(8) ≤ 317. The actual normalization and root-deleted
chart, cap exclusion, polygon pullback and threshold accounting are complete.

The [separate composition artifact](../experiments/omission-projective-transfer-2026-10-09/README.md)
also passes Lean and its axiom check:

```text
'OmissionBalanced.large_avoiding_set_has_chart_cup' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This proves the 194-point structural consequence in the [projective proof map](OMISSION_PROJECTIVE.md).
It uses the previously checked balanced arithmetic and geometry objects;
this checkpoint does not rebuild their large proof trees. Its validation
manifest records source and object hashes and verifies the saved prerequisite
bindings. The source scan covers **118 loose maintained Lean files**, with no
proof placeholders or custom axioms. Git tracks no caches or compiled outputs.
The earlier records below are preserved as historical checkpoints.

## Balanced geometry library — 2026-10-09

The main library now includes twelve modules for attained ranks, exact balanced
state indexing, the actual real-point connection, computed boxes, geometric
cycle soundness and the first literal row. The main `lake build --wfail` passes
with **3,207 jobs**. The [saved audit](validation/axiom-audit-geometry-2026-10-09.txt)
passes for **269 named roots**, including 68 new geometry roots. Every transitive
axiom is among `propext`, `Classical.choice`, and `Quot.sound`; some finite and
structural results are axiom-free. The audit parser now accepts Lean's explicit
axiom-free report while still rejecting missing, duplicate and nonstandard
reports, with tests for each case.

All **55 Python tests** pass in the existing solver environment with the Lean
integration controls enabled. The standard-library-only run passes 39 and
skips 16 optional tests. A new Lean control accepts the source's first cycle and
rejects a deliberately corrupted cyclic order, with the same support. CI runs
that control separately, in addition to the existing arithmetic exporter
controls. A literal-data test verifies that the geometric catalog has exactly
the same 252 profiles in the same order as the archived arithmetic row source.

The [second residual batch](../experiments/omission-residual-progress-2026-10-09-batch2.json)
adds twenty successful part checks (862 leaves), bringing the checkpoint to
**330 parts and 13,827 leaves**. The residual root is still unchecked. The
historical record below is retained rather than overwritten.

The [standalone geometric certificate](../experiments/omission-balanced-geometry-2026-10-09/README.md)
also passed all **86 module checks**: the occupancy prerequisite, 84 row blocks,
and the final assembly. The 85 generated geometry sources reproduce byte for
byte and contain no placeholders or custom axioms. The final two reports are:

```text
'OmissionBalanced.all_geometric_rows' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalanced.real_configuration_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
```

All 2,685 row supports and demands are equated with the arithmetic catalog
inside Lean. The standalone theorem concludes the actual-point bound 192 under
the explicit balanced avoidance hypotheses. It is not part of the default
269-root audit or a global ES(8) theorem. The [artifact validation manifest](../experiments/omission-balanced-geometry-2026-10-09/validation.json)
records all sources, prerequisite bindings, output hashes and test-log hashes.
The final source scan covers 116 loose Lean files, plus the 900 archived
arithmetic and 85 archived geometry sources; no placeholders, custom axioms or
compiled artifacts occur in those source archives. Git tracks no cache or
compiled build outputs.

## Earlier arithmetic-only checkpoint — 2026-10-09

The [complete balanced artifact](../experiments/omission-balanced-lean-2026-10-09/README.md)
records the successful October 7 build of all 898 parts and the final root,
covering 9,862 leaves. On October 9, every one of its 900 generated Lean sources
was regenerated byte for byte and checked against the archived hashes. The
catalog and root were rechecked, and the new `OmissionBalanced.occupied_card_le`
corollary passed Lean. All three current axiom reports contain only the standard
axioms. This was not a second full-tree rebuild.

The source archive contains no compiled objects and no proof placeholders or
custom axiom declarations. Its complete build reports, source manifest and
fresh axiom output are saved alongside it. The main geometric library is
unchanged; this separate result is not included in its 201-root audit. The main
`lake build --wfail` was rerun successfully (3,194 jobs), and a fresh 201-root
axiom audit exactly matches the saved October 5 output. A scan of all 103 loose
maintained Lean files also finds no placeholders or custom axioms.

The Python suite reports 48 tests: 46 passed and two optional Lean integration
tests skipped. A separate Lean-enabled run passes all seven exporter tests,
including both kinds of leaf, branch composition, resume, source tampering,
and a corrupted-column control that Lean rejects. CI now runs those small
Lean controls; it does not silently claim to check the full large certificate.
The residual tree and the geometric transfer remain unfinished. Its
[partial-build record](../experiments/omission-residual-progress-2026-10-09.json)
records 310 of 3,411 parts checked, including ten fresh successful retries or
completions; no residual root theorem is claimed.

## Historical library checkpoint — 2026-10-05

Proof checkpoint: `0407d69d70b12eae6c66fe8808de464264330984`.
The subsequent cleanup changes documentation, ignore rules and audit-output
recording; it does not change the finished geometric proofs.

## Main library

- `lake build --wfail`: **passed**, 3,194 build jobs (including dependencies).
- `python3 scripts/check_axioms.py`: **passed**, 201 named theorem roots.
- Python suite with the existing optional Z3/HiGHS environment: **41 tests passed**.
  The standard-library-only CI run skips 13 solver-dependent tests.
- Lean successfully resolved all **75 declarations** checked from the paper map
  (74 project-qualified names and Mathlib's `convexHull_mono`).

The [complete, unabridged axiom output](validation/axiom-audit-2026-10-05.txt)
contains these main results:

```text
'ErdosSzekeres.Suk.theorem2016' depends on axioms: [propext, Classical.choice, Quot.sound]
'ErdosSzekeres.HMPT.theorem2020' depends on axioms: [propext, Classical.choice, Quot.sound]
Axiom audit passed for 201 theorems: only standard Lean axioms.
```

`#print axioms` reports transitive axiom dependencies of each named result.
The allowlist is exactly `propext`, `Classical.choice`, and `Quot.sound`.
It excludes `sorryAx`, custom theorem assumptions declared as axioms, and
native-evaluation axioms. This records Lean verification of the stated
propositions; it does not expand them to the unformalized parts of the papers.
See [PAPER_MAP.md](PAPER_MAP.md) for those scope distinctions.

## Placeholder and repository checks

A source scan covered **all 102 tracked `.lean` files**, including finished
Suk/HMPT modules, adapted prerequisites, the audit, and standalone experiments.
There were **zero occurrences** of the tokens `sorry`, `admit`, `sorryAx` and
`native_decide`, and zero lines declaring an `axiom` or `constant`. Thus there
is no `sorry` anywhere in the maintained finished results. Failed local probes
inside the ignored cache are not maintained results and are not included in
this statement. The transitive axiom check independently covers the dependencies
of both completed final theorems.

The Git index contained **zero** files under `.cache/`, `.lake/`, or `.elan/`,
and zero compiled Lean objects, native objects/libraries, trace files or Python
bytecode. `git check-ignore` confirmed that representative toolchain and build
outputs are ignored. The committed generated `.lean` catalog is proof input,
not a compiled build artifact. Third-party licenses and modifications are
identified in [THIRD_PARTY.md](THIRD_PARTY.md).

[Source manifest](validation/source-manifest-2026-10-05.json) records SHA-256
hashes of every maintained Lean source, the toolchain/dependency pins, the audit
script, the audit output and validation logs. Its combined source digest is
`d73423332422742791949c5dc190e90ce7a0a181a62d839c88df9211db3b65cf`.
Logs of the full build and Python run remain in the ignored cache; their hashes
are recorded, while the requested full axiom output is committed above.

To reproduce the main audit, after building:

```sh
python3 scripts/check_axioms.py --output /tmp/erdos-axiom-audit.txt
```

For this Mac's workspace-local toolchain:

```sh
ELAN_HOME="$PWD/.elan" .elan/bin/lake build --wfail
ELAN_HOME="$PWD/.elan" python3 scripts/check_axioms.py \
  --lake "$PWD/.elan/bin/lake" --output /tmp/erdos-axiom-audit.txt
```

## Separate certificate checkpoint

The [chunked catalog and leaf](../experiments/omission-chunked-2026-10-05/README.md)
were checked separately, with both Lean processes exiting zero. Their saved
profiler and axiom output are in the directory's `validation.json`. They are
not part of the default-library build or its 201-root audit. Their conclusions
certify the 2,685 balanced row encodings and a single conditional leaf only.
At that historical checkpoint, both complete omission trees and their geometric
transfer remained unproved in Lean. Certificate work stopped after it was pushed;
the October 9 section above records the subsequent resumed work.
