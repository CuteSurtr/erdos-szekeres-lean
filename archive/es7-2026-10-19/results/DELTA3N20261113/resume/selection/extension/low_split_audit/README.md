# Critical low-split encoder audit — PASS

**PROVED:** direct/compact projection and the critical low-split two-option
classification are sound. **COMPUTED:** all supplied map/row bytes and
independent Boolean/real controls PASS. See
[VERIFY_LOW_SPLIT.md](VERIFY_LOW_SPLIT.md) for proof and exact scope.

Direct left11/12/13 have respectively1,430/2,443/4,017 variables and
14,070/23,829/40,574 clauses. Compact left14 has31,099 variables and220,707
clauses. Fourteen native instances are checked, with more than one million
Boolean comparisons and248,448 whole-selector checks on seven real joins.

Exact End3, its first-point exemption, no-four-cap, both selection options,
negative pair aliases and exact four-child D/seven-child T all pass.
Parent direct11–13 accepted proofs are pinned by streaming hashes/logs.
The original compact14 heap128 failure is preserved; the separate parent
heap450 replay is now CERTIFIED. No fresh LRAT replay is claimed here.

For left<=10 the full join has size<=13, covered by separate through11,
size12 and size13 results. Left11–13 use their individual certificates.
This confirms the required bounded left coverage without ambient-selection
monotonicity. No unrestricted all-size low-cut theorem is asserted.

All jobs use one CPU, AS300 MiB, wall20/CPU19; compilation may use the
previously authorized AS500 MiB/20-second bound. No extra heap or long unit.
Writes only here and scratch
`/home/jay/research/data/delta3-codex-20261113/extension/low-split-audit/`.
Earlier m14 and n5 packets are frozen.
