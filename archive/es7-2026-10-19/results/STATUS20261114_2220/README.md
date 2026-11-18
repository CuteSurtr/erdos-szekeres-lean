# STATUS20261114_2220: slice 20 excluded; ES(8) ≤ 308 candidate (14 November 2026, 22:20 KST)

Read [the budget34 record](../LO33N20261113/budget34/README.md) first; its headline and last section carry the details.

## Established tonight (21:11-22:17 KST)

- **EXACT TREE:** budget-34 slice 20 (h(F) ≥ 20, h(Lo) ≥ 14) is excluded over rows `s20-v13` (3,672 rows). Checked
  twice by the committed `scripts/omission_tree.check_tree`: incremental replay `audit/incremental-v10` and a fresh
  full replay `audit/fresh-v13` with no receipt reused. 4,289 contexts, 15,479,542 leaves, minimum margin 1, only
  state 0 missing pending.
- **CERTIFIED:** 49 new coupled rows in eight rounds (v6-v13), each killing a finder witness; every batch passed the
  independent audit (own encoder + fresh cake_lpr). All 1,020 coupled rows have a fresh `s VERIFIED UNSAT` line.
- **Consequence:** with slice 19 (this morning), the written bridge gives **ES(8) ≤ 308**. Computer-assisted, not
  Lean-checked, unrefereed, and **not yet independently audited**. It uses N5 ≤ 65, whose LRATs were deleted
  (recorded verdicts).
- Tool changes, all copies with exact asserted diffs (originals untouched): `run_tree_v2.py` (`--bb`, `--split-open`),
  `prepare_successor.py`, `continue34_v2/v3.py`, `incremental_audit_v2/v3/v4.py`, `replay34_v2.py` (context labels may
  skip numbers after a split; self-check `test_replay34_v2.py`), `audit_followup_rows_v2.py`, `fresh_replay.py`.
  One replay run (`incremental-v8`) failed closed on the old label rule before the fix; nothing was replayed by it.

## Next useful work

1. Independent audit `VERIFY308` with own code (bridge, the 49 evening rows, an independently written leaf checker).
2. Optional slice (h(F) ≥ 18, h(Lo) ≥ 16) at budget 34: removes the N5 dependency.
3. Owner decisions: whether and when to commit the 13-14 November records (they still need the path and tool-name
   scrub before publication); the paused repository cleanup (folder categories, README).

## Machine state

All research units stopped at 22:18 (finders, replays, memory guard). No commit, push or branch change tonight
after the 21:01 snapshot push. Evidence is retained under `/home/jay/research/data/es308-20261114` (7.2 G).
