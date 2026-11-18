# Fresh parent replay of the finite geometry packet — PASS

**PROVED Lean finite statement, freshly replayed.** All 35 source checks
passed: the 34 finished coordinate modules and the previously frozen
Boolean dependency. Every source hash matched the producer's manifest.
The 50 declaration audits contain only standard axioms or no axioms;
there were no errors, warnings, resource-guard stops, `sorryAx`, or
`ofReduceBool` dependencies.

Total individual check time was 51.844 seconds; the largest reported RSS
was 1,093,836 KiB. The sequential unit was
`nov13c-vfy-delta6-geometry-replay`, with CPUQuota100%, MemoryMax1800M,
MemorySwapMax=0, RuntimeMaxSec600, AS4 GiB, and core4 affinity. Each child
used the unchanged 27-second/RSS1300 MiB wrapper. The slot was released
after completion before the separate real-bridge work resumed.

[data/result.json](data/result.json) lists each exact source, hash, runtime
and peak. All logs and individual run receipts are retained alongside it.
The replayed producer manifest SHA-256 is
`e6d39e997435758346d0233aa416bb7f66371d6c3494bba309c4cab57bd73313`.

The theorem and its precise finite semantics are described in
[the frozen packet](../lean_geometry/README.md). This confirms exact
integer-coordinate predicates, complete subset coverage, and the terminal
contradiction. At this checkpoint, interpretation as real convex hulls
remains a separate unfinished bridge. No full real-geometry theorem is
claimed solely from this replay.
