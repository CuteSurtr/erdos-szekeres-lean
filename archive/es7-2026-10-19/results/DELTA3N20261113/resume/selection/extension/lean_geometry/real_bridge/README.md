# Balanced fifteen: checked real terminal-membership obstruction

**PROVED.** Six new Lean modules pass, with 31 explicit axiom audits. The final
theorem is
`Delta3.Balanced15.RealBridge.balanced15_real_obstruction` in
[RealBalanced15.lean](RealBalanced15.lean). Its existential form is
`exists_real_terminal_obstruction`.

For the exact fifteen integer-coordinate points in the frozen
[FiniteModel.lean](../FiniteModel.lean), interpreted as points of the real plane,
the kernel-checked conjunction states:

- the real finite set has cardinality 15 and distinct horizontal coordinates;
- it satisfies the repository's `ErdosSzekeres.GeneralPosition`;
- it has no five-cap;
- it satisfies `¬ErdosSzekeres.HasConvexNGon 7 realSet`;
- there is no real finite subset A that satisfies terminal-pair membership and
  meets every six-element subset in the repository's real `ConvexPosition).

The precise additional definitions are in
[PointSetBridge.lean](PointSetBridge.lean).
`XOrderedCap T` says that every triple a,b,c in T with a.x < b.x < c.x has
negative real orientation. `HasXOrderedCap k S` asks for a k-element subset
with this property. The theorem also proves distinct x-coordinates, so this
is the usual all-triples cap condition on this configuration. It does not
import `Omission.Configuration.HasCap`.

`SetTerminalSafe S A` says that every increasing cap triple a,b,c in A has
u,v in S with u.x < v.x < b.x < c.x and {u,v,b,c} a cap. Thus the last pair
b,c belongs to an ambient four-cap. `HitsConvexSix S A` quantifies over
**all** real six-element subsets T of S in convex position and requires
T to meet A. The conclusion quantifies over arbitrary real finite subsets A;
it is not restricted to a Boolean encoding or an index-level predicate.

This is a terminal-membership obstruction. The packet makes no claim about
universal envelope safety, the original Delta existence statement, minimality,
or a twelve-point configuration.

The real convex-hull connection is proved in
[ConvexBridge.lean](ConvexBridge.lean): the frozen four-point sign test is
equivalent to the repository's `ConvexPosition` on distinct real points.
Convex-position heredity gives the direction needed for no seven-gon;
`Suk.convexPosition_of_four_subsets` gives the direction needed for hitting
six-gons. The real determinant cast is proved through `integerToReal` and
`orient_integerToReal`. Cap and terminal conditions are then transferred
by explicit proofs. No geometric step in the stated conjunction remains
external.

## Proof and axiom record

| Replay order | Source | Axiom reports |
| --- | --- | ---: |
| 1 | IndexHelpers.lean | 4 |
| 2 | BridgeBase.lean | 7 |
| 3 | ConvexBridge.lean | 6 |
| 4 | TerminalReal.lean | 5 |
| 5 | PointSetBridge.lean | 6 |
| 6 | RealBalanced15.lean | 3 |

[data/manifest.json](data/manifest.json) records every audited declaration,
its exact axiom list, source/log/record hashes, input and prerequisite hashes,
cached project-module hashes, resource measurements, and replay order.
All reported axioms are among `propext`, `Classical.choice`, and `Quot.sound`;
the three final declarations use exactly those three standard axioms.
The finished sources contain no `sorry`, custom axiom, `native_decide`, or
`Lean.ofReduceBool`.

The frozen algebra/Boolean and finite-geometry packets were not changed.
The finite prerequisite packet already passed the parent's independent
35-job / 50-audit replay; a copy of that result is
[data/finite-parent-result.json](data/finite-parent-result.json). The old
finite packet's “real bridge external” text is its historical freeze state,
superseded by this separately frozen extension.

Successful checks took 7.520 seconds in total. Maximum observed kernel
RSS was 1,973,904 KiB (1927.641 MiB), below the allocated 2000 MiB guard.
Maximum sampled VmPeak was 2,819,488 KiB; maximum sampled RssAnon across
these checks was 336,320 KiB. Sampled swap was zero. These are per-process
peaks, not simultaneous sums. Lean used `-j1 -M1000`, AS 4 GiB and CPU
affinity core 4; no LSP or long job was launched.

The earlier sole-`IntegerCertificates` import probe under the 1300 MiB guard
was cleanly stopped and is retained as
[data/real-import-integer-1300.json](data/real-import-integer-1300.json) with
its log and original wrapper. It is not counted as a successful check.
The successful 2000 MiB import probe is retained separately. Root
`ImportInteger.lean` and `ImportReal.lean` are excluded probes.

## Parent replay

Prerequisite: the frozen finite packet's independently replayed modules and
`Terminal15Boolean.olean` are available in the authorized scratch directory.
The replay script rechecks all prerequisite source hashes, recompiles all six
new modules sequentially, checks every expected axiom report, rejects errors
or warnings, and requires clean resource exits. Logs and `-DONE.json` go only
to `/home/jay/research/data/delta3-codex-20261113/extension/lean/`.

After taking the released 2000 MiB reservation, run:

```bash
real_bridge_dir=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/lean_geometry/real_bridge
systemd-run --user --unit=nov13c-vfy-delta6-real15-parent \
  -p CPUQuota=100% -p MemoryMax=2600M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=300 -p LimitAS=4G -p TasksMax=32 \
  -p WorkingDirectory=/home/jay/research/lean/erdos-szekeres-lean \
  /usr/bin/taskset -c 4 /usr/bin/python3 -B "$real_bridge_dir/replay.py" \
  --prefix parent-real15-fresh-a
```

The 300-second runtime must end before 08:20 KST on 14 November 2026.
The local runner still imposes its 27-second per-module deadline and RSS
watcher. This command has not been launched by this side task. Parent fresh
real replay is pending at this freeze. Put its evidence in a separate
parent record; do not edit this frozen packet.

