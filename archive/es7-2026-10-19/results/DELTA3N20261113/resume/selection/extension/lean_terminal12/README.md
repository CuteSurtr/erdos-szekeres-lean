# Twelve-point real terminal obstruction at n=6

**PROVED in Lean.** The complete packet has 19 unique T12 modules and 59
standard-only axiom audits: 14 finite/Boolean modules with 32 audits, followed
by five real-geometry modules with 27 audits. The parent has independently
replayed the finite stage successfully. Fresh parent real-stage replay is
pending at this freeze.

The main theorem is
`Delta3.Terminal12.RealBridge.terminal12_real_obstruction` in
[T12Real.lean](T12Real.lean); `exists_real_terminal_obstruction` is its
existential form. It proves for the exact real finite set:

- cardinality 12, distinct horizontal coordinates, and the repository's
  `ErdosSzekeres.GeneralPosition`;
- no five-cap and `¬ErdosSzekeres.HasConvexNGon 6 realSet`;
- no real finite subset A satisfying terminal-pair membership while meeting
  every real convex pentagon contained in the set.

The points are
`(0,0), (37,-35), (38,-248), (84,-270), (472,-427), (653,-757),
(665,-793), (666,-717), (683,-718), (736,-567), (926,-895), (1000,0)`.
They match the audited input
[coordinates](data/T12-coordinates.json) exactly. Lean checks all 220
increasing-triple determinants, a determinant magnitude bound of 45,
all 792 five-subsets and all 924 six-subsets.

This is an existence obstruction for terminal membership. It makes no
Lean claim about the global minimum or any lower bound. It does not refute
ordinary weak-Delta or uniform-Delta existence, and makes no envelope
domination claim.

## Statement and geometric connection

[T12PointSetBridge.lean](T12PointSetBridge.lean) gives the precise real predicates.
`XOrderedCap T` requires negative orientation for every a,b,c in T with
a.x < b.x < c.x; `HasXOrderedCap k S` asks for a k-element subset of S
with that property. Distinct horizontal coordinates are proved separately.
This is an explicit all-triples real cap formulation; the packet does not
import `Omission.Configuration.HasCap`.

`SetTerminalSafe S A` requires, for every increasing cap triple a,b,c in A,
points u,v in S with u.x < v.x < b.x < c.x and {u,v,b,c} a cap.
Thus b,c is the last pair of an ambient four-cap.
`HitsConvexFive S A` requires A to meet every five-element T contained in S
with the repository's real `ConvexPosition T`.
The contradiction quantifies over arbitrary real finite subsets A.
It needs no additional four-cap exclusion assumption on A.

[T12ConvexBridge.lean](T12ConvexBridge.lean) proves the correspondence between
the finite orientation predicate and genuine real convex position, using
the repository's four-point sign criterion, convex-position heredity,
and `Suk.convexPosition_of_four_subsets`.
[T12BridgeBase.lean](T12BridgeBase.lean) proves determinant compatibility
through `integerToReal`, injectivity, cardinality and general position.
[T12TerminalReal.lean](T12TerminalReal.lean) transfers the cap and hitting
conditions. No geometric connection in the stated conjunction remains
external.

## Boolean and finite proof

[T12Boolean.lean](T12Boolean.lean) encodes all 192 original clauses and
refutes the 65-clause subset by ordinary Lean proof terms. The supplied
DPLL tree has 47 nodes, 24 leaves and 84 unit steps.
[T12TerminalBridge.lean](T12TerminalBridge.lean) derives each of the 65
clauses from the exact coordinate predicates, with the arithmetic premises
checked by kernel reduction. The tree and Python generators are not
trusted proof checkers.

The original CNF SHA-256 is
`25ca75a9eee359ca03ae7f96657128ab03693c03421b1e7e83627f529841890a`;
the core hash is
`450bb17403af22a2253a03b4610b14caefab73253d883ddcbd65f780bac95d3a`;
the tree hash is
`f14ab9466f3110b3daf3e0ba5c1d6857b575475e6f267d6fb38f4ae57e318add`.
Input paths and hashes are in [input-hashes.json](data/input-hashes.json).
The parent's separate cake acceptance, irredundancy witnesses and global
lower bound are not assumptions in these Lean proofs.

## Checks and resources

[finite-manifest.json](data/finite-manifest.json) lists all 14 finite sources,
32 exact axiom reports and logs. Its hashes remain fixed by
[FROZEN_FINITE.json](FROZEN_FINITE.json).
[real-manifest.json](data/real-manifest.json) lists the five real sources,
27 reports, prerequisite hashes, cached project-module hashes and logs.

| Real replay order | Module | Axiom reports |
| --- | --- | ---: |
| 1 | T12BridgeBase | 7 |
| 2 | T12ConvexBridge | 6 |
| 3 | T12TerminalReal | 5 |
| 4 | T12PointSetBridge | 6 |
| 5 | T12Real | 3 |

Every reported axiom is among `propext`, `Classical.choice`, and `Quot.sound`.
Both final obstruction theorems use exactly these three standard axioms.
There are no finished proofs using sorry, custom axioms, native_decide
or Lean.ofReduceBool.

All 19 bounded checks passed without errors, warnings, guard stops or swap.
Finite checks took 9.302 seconds total, peaking at 623,448 KiB RSS.
Real checks took 7.061 seconds total, peaking at 1,959,532 KiB RSS
(1913.606 MiB), under the explicitly allocated 2000 MiB guard.
The total recorded check time is 16.363 seconds.
Each process used one CPU, AS 4 GiB, Lean -j1 -M1000 and a 27-second deadline.
No long job or LSP was launched. All generated module names and exported
oleans start with T12, and all exports/logs are confined to
`/home/jay/research/data/delta3-codex-20261113/extension/lean-terminal12/`.
Earlier fifteen-point and algebra packets remain unchanged.

## Fresh parent real replay

After claiming the released 2000 MiB reservation, run:

```bash
t12_dir=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean_terminal12
systemd-run --user --unit=nov13c-vfy-delta6-t12-real-parent \
  -p CPUQuota=100% -p MemoryMax=2600M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=300 -p LimitAS=4G -p TasksMax=32 \
  -p WorkingDirectory=/home/jay/research/lean/erdos-szekeres-lean \
  /usr/bin/taskset -c 4 /usr/bin/python3 -B "$t12_dir/T12replay_real.py" \
  --prefix parent-t12-real-a
```

The runtime must end before 08:20 KST on 14 November 2026. The script validates
the 14 finite prerequisite source hashes and project cache hashes, rebuilds
the five new real modules sequentially, compares all 27 axiom reports, and
rejects warnings, errors or resource stops. It uses the independently
replayed T12 finite oleans already in the dedicated scratch directory.
Its log/JSON files and `parent-t12-real-a-DONE.json` are written there.

The separate finite replay is `T12replay_finite.py --prefix <unique-tag>`,
using the 1300 MiB runner; the parent has already completed it successfully.
Do not run the real-stage runner under that smaller reservation.
Parent fresh real evidence should be archived separately, leaving this
packet frozen.

