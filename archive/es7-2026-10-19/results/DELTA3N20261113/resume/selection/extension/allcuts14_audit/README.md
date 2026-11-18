# Combined n7/m14 cut audit — PASS

**COMPUTED:** all37 rows /8,034 literals and39 provenance entries rebuilt;
the231,613-row exact base is byte-identical. **PROVED (written):** real
counterexamples project to the strengthened formula using the explicit
prior-size and low-predicate dependencies in
[VERIFY_ALLCUTS14.md](VERIFY_ALLCUTS14.md). No combined14 UNSAT certificate
is supplied; this is not unconditional abstract-formula equivalence.

The independent truth controls and12 exact real fixtures pass, including
eight size14 controls,1,158 selectors/lifts and92,592 mixed-subset tests.
Both singleton ends and all low branches have explicit coverage. The fresh
[low11–14 replays](../low_split_audit/replay/README.md) establish T7 through
left14 with separate lower coverage; this14-point cut audit only needs
left<=13. No left15/16 or all-size claim follows.

Combined CNF SHA-256:
`01de4ba0c9831690f5e64a3592fd335ef701c100224060733e9734d55ac65554`.
Full hashes, outputs and row provenance are under data/. The independently
rebuilt CNF stays in the disjoint allcuts14-audit scratch directory.
All jobs used one CPU, AS300MiB, wall20/CPU19, affinity5,nice10, below23MiB
RSS and one second. No own check overlapped cake; no compile or solver ran.

The parent matching search was SOLVING when checked at07:26KST. A finite14
theorem still needs an accepted matching proof. Frozen records are unchanged.
tools/check_rows.py and data/controls.command.sh preserve the independent
workflow; output paths are exclusive, so any rerun needs a new record.
