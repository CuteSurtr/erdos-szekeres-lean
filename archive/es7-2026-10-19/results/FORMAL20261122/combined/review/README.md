# Review of item `combined` (part 1): independent reviewer (slot rv5, track ag)

Reviewer work directory (the only place written): `/home/jay/research/data/formalize-20261122/combined/review`.
Worker directory (read-only for me): `/home/jay/research/data/formalize-20261122/combined`.
Units: `esr-ag-rv5-<job>` (CPUQuota 100 %, MemorySwapMax 0, nice 10, one at a time; gates: no YIELD, Tctl < 86 C,
`cpu_free.sh esr` >= 1, ag-track anon + expected peak <= 6,800 MB). No lake, no lean-lsp, no git writes, no olean output.

## Milestones (plan, written 22 Nov 22:02 KST before any unit)

| M | content | state |
|---|---|---|
| R0 | orientation: SKILL.md, FORMAL20261122, LEAN_STATUS, worker README/REMAINS/sources/tools, sibling records | done 22:01 |
| R1 | own review tools: `lean/RV5Review.lean` (ONE compile: stored statements, own restatements re-elaborated from the pieces, type equality, declaring modules, axioms, olean module list with resolved paths, row dumps, one interpreter rowText), `tools/rv5_audit.py` (one provider per module, sha256 vs original pins, mtimes), `tools/rv5_bind.py` (sample of rowprint prints vs certified CNFs, cake_lpr lines, fresh cake_lpr) | done 22:16 |
| R2 | the ONE compile (`esr-ag-rv5-ax`, MemoryMax 6G) | done 22:17:53-22:31:11: lean_rc 0, 13:18 wall, anon+shmem peak 532 MB, no oom; every check passed (logs/RV5Review.log) |
| R3+R4 | import audit + CNF binding sample (`esr-ag-rv5-ab` 22:32:04-22:32:43: audit passed, bind crashed on a `.zst` LRAT path; `esr-ag-rv5-bind` 22:33:19-22:33:31 after the fix: 20/20 bound, 20 fresh cake_lpr VERIFIED) | done |
| R5 | REMAINS.md labels against the records; `VERIFY_combined.md` | done 22:40: theorems CONFIRMED, audit CONFIRMED, REMAINS confirmed with 2 nits, Switch3519 not confirmed (untested) |

## Status
- 22:02 R0 done; cpu_free.sh esr = 0 at 22:01 (waits expected).
- 22:40 review finished; nothing of this slot running. Result: `VERIFY_combined.md`.
- 22:31 R2 done (the one compile). Stray: 8 small `rowprint list` outputs were first written to /tmp/claude-1000 by mistake at ~22:05 and moved into data/rowprint_list/ at once.
