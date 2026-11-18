# PROVED: exact finite integer-orientation obstruction on 15 points

Finite packet frozen at 06:45 KST, 14 November 2026. All 34 finished Lean modules
pass, with 47 axiom audits containing only standard axioms or no axioms. A fresh
parent replay is pending at this checkpoint. The older `../lean/` packet is unchanged.

## Statement

The main declaration is
`Delta3.Balanced15.balanced15_finite_obstruction` in `Balanced15.lean`. For the exact
15 integer points in `data/balanced-witness.json`, it proves:

- strictly increasing horizontal coordinates;
- nonzero determinant for every increasing triple;
- every five-element subsequence fails the all-negative-triples cap predicate;
- every seven-element subsequence fails the all-four-point orientation criterion;
- no chosen set of indices satisfies both `TerminalSafe` and `HitsSix`.

Additional checked declarations give all 455 exact determinant values, absolute
determinant margin at least 45, counts of 3,003 five-subsets and 6,435 seven-subsets,
and a Boolean-selection version of the terminal obstruction.

`TerminalSafe A` says that each selected increasing negative-determinant triple
has an ambient four-cap ending in its last two indices. `HitsSix A` says that every
increasing six-tuple passing all its four-point orientation tests contains a
selected index. `terminalPair_iff` proves that the implemented terminal test is
exactly the stated existential four-cap condition. No separate condition forbidding
selected four-caps is needed for this finite obstruction.

## Model and soundness

The index type is `Fin 15`. Coordinates are integer pairs. CNF variable `i+1`
corresponds to zero-based point index `i`. The source coordinate syntax was checked
against the copied JSON; no optimizer verdict enters the Lean proof.

`cap` tests every three-element subsequence for negative determinant.
`quadConvex` uses exactly the four-sign formula in the repository's
`ErdosSzekeres.QuadConvexSigns`. `signConvex` requires that formula on every
four-element subsequence. These are explicit finite integer predicates.

**This packet does not prove a theorem about real `ConvexPosition`, real convex
hulls, or the entire geometric counterexample.** The precise remaining connections
and available repository lemmas are recorded in `REAL_BRIDGE_NOT_CHECKED.md`.
The no-five/no-seven conclusions here quantify over all appropriate subsequences;
`mem_choose_of_sublist` formally proves enumeration completeness.

No finished source uses `sorry`, custom axioms, `native_decide`, or `Lean.ofReduceBool`.
The computations use ordinary `decide` or `decide +kernel`; the latter requests
kernel reduction, not native evaluation. The terminal contradiction uses ordinary
proof terms and the previously frozen Boolean theorem.

## Method

`FiniteModel.lean` defines the fixture and predicates. `Determinants.lean` verifies
the entire exact table. `FiniteFacts.lean` verifies the determinant margin and
the five-cap exclusion.

Seven-subset checking is split into 13 explicit blocks of at most 512 subsets.
Each `SevenBlockNN.lean` checks its predicate, and each `SevenCoverNN.lean` checks
its exact position in the recursive subset enumeration. `SevenAggregate.lean`
assembles the blocks with a generic take/drop lemma. `SubsequenceFacts.lean` turns
the enumeration results into statements about arbitrary subsequences of the
required length.

`TerminalBridge.lean` derives all 98 hypotheses of the frozen propositional core
from the coordinate predicates: 36 negative triple clauses use an exactly checked
negative determinant and absent terminal pair; 62 positive six-clauses use exactly
checked four-point tests. The frozen `core_unsat` then yields the contradiction.
Every arithmetic side condition is checked by Lean, not assumed from the external
CNF encoder. `Balanced15.lean` packages the finite conclusions.

## Results

All 34 finished source checks exited zero with no warnings or guard stop. Their
recorded durations sum to 40.484 seconds. The largest kernel-reported maximum RSS
was 1,026,556 KiB. Exporting the unchanged Boolean dependency took an additional
13.806 seconds at 583,864 KiB. Every invocation was shorter than 27 seconds.

The final aggregate finite theorem checks in 0.115 seconds at 373,744 KiB RSS.
The terminal bridge checks in 3.394 seconds at 459,592 KiB RSS. All sampled swap
values in the successful records are zero. Logs and exact hashes are in
`data/checks/` and `data/manifest.json`.

## Controls

The task stayed on one CPU (core 4), Lean `-j1 -M1000`, AS 4 GiB, RSS guard 1300 MiB,
and nominal allocation 1800M. No unmanaged LSP, new installation, full repository
build, branch change, or commit was used.

Three failed controls are retained in `data/controls/`, including their exact
source bytes and run records: a Lean recursion-depth failure and two clean RSS
guard stops. The memory failures used repeated drop/take evaluation and a single
large coverage equality. Both were replaced with smaller checked blocks and
proof-term assembly. The peak sampled RSS at the larger guard stop was 1,336,892
KiB, an approximately 5.6 MiB polling overshoot, still below the nominal allocation.
Both processes were stopped by the watcher with SIGTERM, not a kernel OOM kill.

The unused `NoSeven0.lean` through `NoSeven3.lean` are **excluded development
prototypes**, not finished results. Replay only the manifest's listed sources.

## Files and hashes

Main theorem source SHA-256:
`6e94328f462c4c0f9ba7a98262a053dcebf12b94e5d6780f40bb6eb095548eee`.

Terminal bridge SHA-256:
`c8b99bb4ecdd16d21d047db1ace03263e9963ea12756101f87e175f1d42ad54a`.

Coordinate input SHA-256:
`7da027c4f6c800245a9f715e684872358fea36cab0d0133aa15e0a0b199eed9b`.

Manifest SHA-256:
`e6d39e997435758346d0233aa416bb7f66371d6c3494bba309c4cab57bd73313`.

The manifest lists all 34 finished sources, 47 axiom audits, exact resources,
generator hashes, retained controls, and a dependency-ordered replay list.
`generate_fixture.py` reproduces 27 generated table/block/coverage sources;
`generate_terminal_bridge.py` reproduces the bridge. They write only into the
authorized scratch staging directory and check byte equality with this packet.

## What remains

The exact finite statement is complete. A fresh parent replay is pending. The
real-coordinate, convexity, and hull connection has not been compiled in this
packet. Any subsequent attempt belongs in a separate `real_bridge/` subdirectory;
it must not modify these frozen sources or evidence. The current 1300 MiB cap
must not be raised without the parent's explicit resource reallocation.

## Resume commands

After reserving the Lean slot and notifying the parent, a full sequential replay
can run under the required bounded user unit:

```bash
systemd-run --user --unit=nov13c-vfy-delta6-lean \
  -p CPUQuota=100% -p MemoryMax=1800M -p MemorySwapMax=0 -p RuntimeMaxSec=600 \
  --working-directory=/home/jay/research/lean/erdos-szekeres-lean \
  /usr/bin/prlimit --as=4294967296 --core=0 /usr/bin/taskset -c 4 \
  python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean_geometry/replay.py \
  --prefix geometry-parent-fresh
```

The driver runs one bounded child at a time using the unchanged `../lean/check.py`.
It stops on the first failure, verifies each source hash, and saves all logs and
a completion JSON to the authorized scratch directory. It checks 34 new modules
plus one unchanged Boolean dependency, whose three axiom reports are additional
to the 47 reports belonging to this packet. No such long replay unit was launched
by the producer; its individual incremental checks already pass.
