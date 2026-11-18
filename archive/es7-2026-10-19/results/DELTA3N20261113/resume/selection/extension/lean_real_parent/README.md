# Fresh parent replay of the real fifteen-point obstruction

**PROVED, Lean; fresh parent replay PASS.** All six frozen real-geometry
bridge modules were rebuilt sequentially. The31 axiom reports match the
frozen record exactly and use only `propext`, `Classical.choice`, and
`Quot.sound`. No error, warning, resource stop or changed source was found.

The main theorem is
`Delta3.Balanced15.RealBridge.balanced15_real_obstruction` in
[RealBalanced15.lean](../lean_geometry/real_bridge/RealBalanced15.lean).
It states that the actual real finite set has15 points, distinct x
coordinates, general position, no five-cap, no convex heptagon, and no
terminal-safe subset hitting every actual convex six-subset. Its precise
real-set predicates and existential form are in the frozen bridge packet.
This is not a counterexample to ordinary weak Delta or uniform selection.

The parent independently checked all source and prerequisite hashes,
the pinned project source/olean pairs, every expected axiom declaration,
and every run's clean exit. Earlier finite prerequisites had separately
passed the35-job parent replay; they were not assumed from a solver result.
The frozen worker packet was left unchanged.

The six checks took **7.526 seconds**, with maximum RSS **1,973,880 KiB**,
below the2000MiB guard. The unit `nov13c-vfy-delta6-real15-parent` used
CPU100%, MemoryMax2600M, Swap0, Runtime300s, AS4GiB, and affinity4.
Per-module deadlines and the independent RSS watcher were active.

[data/result.json](data/result.json), [data/DONE.json](data/DONE.json),
and the twelve fresh logs/receipts retain all outcomes and source hashes.
The worker manifest SHA-256 is
`58a8efa09a6a35633fbc8c31bd51678e3b7186b130bc3148e07af2b9d5d7c44d`;
the main source SHA-256 is
`4e8f648678aae017c8356d0ed33cccffe891c9ee5f0ee9230448d8fb4b95cbfc`.
Reproduction uses the frozen packet's `replay.py` with a fresh prefix;
allocate the2000MiB slot before doing so.
