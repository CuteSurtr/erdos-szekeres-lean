# Review of res118-rowblocks: statement fidelity (slot lrv3, 22 Nov 2026)

Independent statement-fidelity review of the worker result `res118-rowblocks`. This directory is the only place
the reviewer writes. No `lake`, no lean-lsp, no git writes, nothing written into any olean store.

Units of slot lrv3 are shared with other reviewers (`esr-ag-lrv3-e1`, `esr-ag-lrv3-v182a`). My units are named
`esr-ag-lrv3-rbx-*` and start only when no `esr-ag-lrv3-*` unit is active (plus the YIELD / Tctl / pool gates).

## Plan

| step | content | state |
|---|---|---|
| R0 | orientation: worker README/DESIGN, Lean sources, Res118 definitions, ENCBLEAN DIMACS semantics, M9 script, T4 runner | done |
| R1 | own checks outside Lean: module-shadow check over the LEAN_PATH roots, source scan | done 18:42: 9,677 modules, 0 duplicates; scan clean (`data/lrv_static.json`) |
| R2 | own binding (unit `esr-ag-lrv3-rbx-bind`): `rowprint row B I` hashed in Python for all 2,025 rows vs `cnf_sha_actual` of ACCEPTED T4 jobs (exact line in `cake/<job>.out`); exe frozen check; CaDiCaL controls | done 18:48:20-19:00:45, rc 0: 2,025/2,025 BOUND, equal to the worker's M9 row by row (`data/lrv_bind.*`, `data/lrv_post.json`) |
| R3 | ONE Lean compile (unit `esr-ag-lrv3-rbx-ax1`): axioms, stored statements, unfolded restatements, olean row dumps, kernel row checksums, interpreter-vs-exe text of one row | ran 19:03:30-19:03:45, rc 134 (stack overflow, most likely my `Lrv.ck` kernel fold). Sections 1-3 complete: axioms (38 lines, all standard), stored statements, olean dumps. Lost: fingerprints, my restatements' axiom lines, U0 text. Not recompiled (one compile) |
| R4 | olean row dump vs exe `list` (the link M9 lacks), interpreter text vs exe text | done: dumps equal the exe lists for all four blocks (`data/lrv_cmp.json`); U0 text lost in the abort |
| R5 | `VERIFY_res118-rowblocks_fidelity.md` | done 19:10: CONFIRMED for all five theorems (statement fidelity); fixes in its §8 |

Resume: `tools/start_unit.sh <job> <max_wait_min> <command...>`; `tools/lrv_bind.py`, `tools/run_audit.sh`.
