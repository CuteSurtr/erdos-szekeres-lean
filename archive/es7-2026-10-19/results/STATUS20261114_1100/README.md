# Handoff: budget34 research, 14 November2026, about11:00 KST

The owner requested roughly one hour from10:00:22. Read
[the main result record](../LO33N20261113/budget34/README.md) and
[the final independent audit](../LO33N20261113/budget34/audit/final-audit.json).
All work remains uncommitted on es7-night-2026-11-01. No push, branch
change, root README.md/math.md edit or external communication occurred.

## Established this pass

- **EXACT TREE:** budget34 slice19, capacities F19/Lo15, is excluded.
  All3,643 contexts replay;1,658,483 nodes,829,242 leaves,minmargin1.
  The sole pending branch is state0missing, impossible for actual residuals.
- **PROVED structural lemma:** no residual configuration simultaneously
  has at least65 F owners and55 Lo owners. Equivalently F<=64 or Lo<=54.
  Pad its Boolean hole set to19/15 and use the completed tree. The padding
  need not be geometrically realizable. This lemma uses neither N5 nor
  N66. See [the proof](../LO33N20261113/budget34/tradeoff/README.md) and
  [independent review](../LO33N20261113/budget34/bridge-followup/README.md).
- **CERTIFIED:** all971 coupled rows in the final pool were independently
  CNF-reconstructed and freshly accepted by cake_lpr. The812 initial rows
  were supplemented by batches7+128+9+10+5; all raw evidence is retained.
- **PARTIAL EXACT REPLAY:** slice20 final version5 has1,222 checked
  contexts out of4,064;2,842 remain open. The final partial tree counts
  11,366,003 nodes and5,683,002 leaves including its pending frontier,
  min checked margin1. The2,843 pending branches include state0missing.
  This is not a finite exclusion.

The existing project bound remains ES(8)<=309. ES(8)<=308 is unproved.
With the inherited N5<=65 result, N66<=55 would now suffice for308; the
established N66 bound is56. The historical N5 arithmetic LRATs were deleted
in their earlier session, as its audit records explicitly say; this pass
does not claim a fresh retained-proof N5 replay. The standalone tradeoff
and the preferred existing309 chain avoid that dependency.

The new result combines existing Lean components, written geometric
soundness, fresh LRAT checks and exact integer tree replay. It is not a
complete Lean theorem and nothing is refereed. No literature novelty claim
is made. The independent [SAT record](../LO33N20261113/budget34/sat/VERIFY_FINITE_SAT.md)
documents its bounded searches, semantic controls and earlier witnesses.
Witness4 also satisfies every one of6,829 additional provisional nine-state
rows from the supplied discovery files: adding that entire supplied family
to v4 is insufficient. The final five13-state cuts exclude it. This is a
finite-model observation, not a claim that every possible nine-state
constraint is insufficient. Final v5's encoding audit and214 exact
real-point controls passed; bounded solver searches ended UNKNOWN.

## Preserved live state

W=/home/jay/research/data/es308-20261114.

- Complete slice19: W/runs/s19/bb. Portable archive
  W/archive/s19-exact.tar; SHA-256
  `586793624172691d00a4c5f364ab29f6b4e4e3cb9e1e21458a93ab4232f3aeee`.
  Every archive member was round-trip checked against the original.
- Resumable slice20: W/runs/s20/bb, with1,222 immutable closed context
  files and its4,064-context master. Two independent tail probes supplied
  76+115 of those files; all imports passed independent exact replay.
- Final inputs: W/inputs/s20-v5,3,623 rows=2,650 base+2 capacities+971
  coupled. Extra SHA-256
  `e6601e5edcddfcc653a0891eef63d8010a6dd303431d312515fa8e8e03618126`;
  rows SHA-256
  `8d8c970f37b99309e94a7a8b06537024fe7264abfe8c2af501c6f0cf6b463fb0`.
- All prior input versions and four earlier Boolean witnesses are
  snapshotted. Each earlier witness was ruled out by later certified cuts;
  none is a real point configuration. No SAT or UNSAT claim is made for
  final version5.
- W/continuation/events.json records the sequential discovery/certificate
  loop. It finished before10:45. W/cuts-* retain the added CNFs, LRATs,
  exact cake stdout, source hashes and receipts. Large evidence occupies
  about4.1GiB; no large proof was deleted.
- Small input copies, receipts, hashes, tools, independent reviews and
  audit packets are in R/LO33N20261113/budget34. The final hash manifest
  belongs to that record. Prior Delta packets remain untouched.

## Next useful work

Finish slice20 with sound constraints, or prove N66<=55. The last short
v5 search hit the50,000-node per-context cap and closed no additional
contexts. Repeating the identical short retry wastes work on these hard
contexts. Consider refining the open frontier in a preserved successor
packet using native fastbb's `--split-open`; the current Python runner
does not expose that option. A higher per-context cap requires a fresh
memory estimate within the existing limits. Completed context files
should be retained and their row-prefix provenance preserved.

The runner tools/run_tree.py can resume the current packet with
`20 --input-folder=s20-v5 --tag=<new-exclusive-tag>`, bounded seconds and
threads. A new task must inspect live units before launching anything.
Use nov13c-vfy-* systemd units, total<=16 CPU threads, global research
memory<=24GB, verifier track<=6000MiB, no swap, finite runtime and clean
stops below each nominal memory cap. Read MEMORY_POLICY.txt and the
current guard script; restart memguard5 before long research work.
Do not use the old budget33 witness helper unchanged. Only an exact
cake_lpr `s VERIFIED UNSAT` line certifies an LRAT. Do not infer exclusion
from a finder/HiGHS status, partial tree, or absence of a new witness.

All search and audit jobs were stopped during this pass. Monitor shutdown
is recorded in [shutdown.json](../LO33N20261113/budget34/data/shutdown.json).
All research units were inactive at10:51:37; memguard5 was stopped and
p2-watch-d1b was already not loaded. The three sidecar agents were closed.
Check for newly launched external jobs before the next session; this
handoff is a snapshot, not a promise about future machine state.
