# Formula augmentation confirmed; certificate replay pending

**PROVED:** canonical exact repair preserves orientation projection and
admits every real counterexample with no extra geometric premise.
**COMPUTED:** all 15,822 map entries and 55,556 added reverse clauses match
independent reconstruction. The 59,815-clause original body is byte-for-byte
unchanged; total 115,371 clauses, no new variables or fixed signs.
Added rows: 26,884 bad-family + 28,672 target-family.

Reviewed output hash:
`3ec4b75d9076b6f257fed83f3cbb17b8372a43f53f1c0fc8d30730e4c5d35b87`.
All old containment/failure interfaces pass, as do two exact real controls
and 111,104 Boolean lattice assignments. Full proof and results:
[VERIFY_EXACT.md](VERIFY_EXACT.md), [README.md](README.md).

The parent's `finite13-b/` binary proof is still growing. No accepted
certificate or independent replay is claimed. Replay needs a completed
retained proof plus explicit resources beyond the current short AS300 MiB
allocation if necessary; see [REPLAY_HANDOFF.md](REPLAY_HANDOFF.md).

Structure 0.42 s / 80,664 KiB RSS; controls 0.38 s / 80,140 KiB. Sequential
one-CPU jobs, AS300, wall20/CPU19. No job left running. Frozen subset audit
is untouched; no m15 model/coordinate audit or full base audit was duplicated.
