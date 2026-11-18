# m14 exact/conditional high-split audit — PASS

**PROVED:** exact reverse containment preserves the orientation projection;
the real high-split reduction justifies cuts1–12 directly and cut13 using
terminal-safe existence at exactly size13. **COMPUTED:** all map entries,
added rows, body-byte preservation and independent integer controls PASS.
No m14 UNSAT certificate or finite m14 theorem is claimed here.

Inputs: `n7m14-exact.cnf` (32,086 variables, 231,613 clauses) and
`n7m14-indecomp.cnf` (231,626 clauses), compared against the existing
`terminal7-a/m14/input.cnf` and map. Prior generic geometry and exact
augmentation proofs remain explicit dependencies, not full re-audits.

The 32,086 map entries,127,128 reverses and13 cut clauses (2,730 literals)
match independent streaming reconstruction. The original104,485 body rows
are unchanged. Both conditional files are byte-identical. Exact hash:
`5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4`.
Conditional hash:
`ba43ca6ecbaeb6bc05854271a27f1204e3a690240a5c525bf1b2a9223dbd1819`.

[VERIFY_HIGHSPLIT.md](VERIFY_HIGHSPLIT.md) gives the independent proof,
controls and source-version provenance. Fifteen small real fixtures give
222 selectors/lifts and21,599 mixed-subset checks. Canonical real14 flags
satisfy all216,700 non-failure rows. A real19 extension of the cited old18
obstruction demonstrates why the last-cut premise is essential. The revised
exact-size13 dependency is sufficient; no size monotonicity is assumed.

The exact-size13 result includes the fresh independent replay in
`../exact_audit/replay13/`. A future real m14 conclusion still requires a
matching accepted certificate for the conditional CNF. The parent run was
SOLVING at handoff; no unconditional propositional equivalence is claimed.

Commands, stdout/stderr, time, source and receipt snapshots are retained.
The first header-parser failure and its partial output remain; the corrected
parser accepts standard padded DIMACS headers while all body checks remain
byte-exact. Every successful job was below0.6s/32MiB RSS. All checks used
one CPU, AS300 MiB, wall20/CPU19; no proof replay or long job was used.
Writes only here and scratch
`/home/jay/research/data/delta3-codex-20261113/extension/highsplit-audit/`.
Original frozen audit files are unchanged. No owned job remains active.

To reproduce rows, check CPU availability and run the command from
`data/rows02.command.sh` with a fresh run suffix and log paths; the checker
refuses to overwrite an existing run. The controls and exact limits are in
`data/controls.command.sh`; likewise use fresh output names for any rerun.
