# Review of item `combined-2` (part 2): independent reviewer (slot rv5, track ag)

Reviewer work directory (the only place written): `/home/jay/research/data/formalize-20261122/combined/review/part2`,
plus the result file `/home/jay/research/data/formalize-20261122/combined/review/VERIFY_combined-2.md`.
Part 1's review files in `combined/review/` (README.md, VERIFY_combined.md, lean/, tools/, logs/, data/) are not touched.
Worker directory (read-only for me): `/home/jay/research/data/formalize-20261122/combined`.

Units: `esr-ag-rv5-p2<job>` (CPUQuota 100 %, MemorySwapMax 0, nice 10, one at a time). Gates before each start: no
YIELD file, Tctl < 86 C, `cpu_free.sh esr` >= 1, no other `esr-ag-rv5-*` unit, ag-track anon + expected peak <= 6,800 MB
(85 % of the ag budget 8,000 MB in `esr-memguard-1122f`). No lake, no lean-lsp, no git writes, no olean output (no `-o`).
Lean: bare `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1`, LEAN_PATH = the worker's
`tools/env2.sh` (copied to `tools/env.sh`, expansion compared with `diff`).

Memory rule: compile MemoryMax 6G (the import of `E304Z.Final` maps about 25 GB of oleans; anon+shmem expected about
0.6 GB, HEURISTIC from part 1 and its review: 520-533 MB); a 0.2 s sampler of the cgroup's anon+shmem sends SIGTERM to
lean at 80 % of MemoryMax (4,915 MB). Hash/print units: MemoryMax 2G-5G as sized below, measured with `/usr/bin/time -v`.

## Milestones (plan, written 23 Nov 00:20 KST before any unit)

| M | content | state |
|---|---|---|
| R0 | orientation: SKILL.md, FORMAL20261122 README, LEAN_STATUS, worker README/REMAINS/sources/tools/logs, part-1 review, n66-l15-rows README + review | done 00:20 |
| R1 | own tools: `lean/RV5P2Review.lean` (THE ONE compile: worker axioms; own re-elaboration by another route, N66 via `n66_bound_54_of_rows`+`rowsValid_R15`, rb118 via blocks+RS slices, 304 via `composition_304_z`+`excludes_67`; type equality; hand-unfolded explicit statements accepted by defeq; verdict-shaped (text) composite; declaring modules; module list with `findOLean`; interpreter dumps of `R1_15`/`leaves105`); `tools/rv5p2_audit.py` (one provider per module under env2, sha256 O_DIRECT vs part-1 review closure + worker closure2 + N66 records; ctime/mtime vs the review compiles; resolution equal in the component envs); `tools/rv5p2_bind.py` (sample re-print with the frozen exes `n66r15print`, `r15rowprint`, `rowprint` vs certified files; fresh cake_lpr on a few printed texts) | done 00:24 |
| R2 | the ONE compile (`esr-ag-rv5-p2ax`, MemoryMax 6G) | done 00:24:51-00:34:28: lean_rc 0, 9:37 wall, anon+shmem peak 611 MB, no oom; every check passed (`logs/RV5P2Review.log`) |
| R3 | audit + binding sample units | done: `esr-ag-rv5-p2aud` 00:35:09-00:35:50 rc 0, 0 problems; `esr-ag-rv5-p2bind` 00:36:19-00:37:08 rc 0, 14/14 bound, fresh cake 5/5 + negative control rejected |
| R4 | REMAINS.md/README claims vs records; `VERIFY_combined-2.md` | done 00:45 |

## Status
- 23 Nov 00:20 R0 done. s35_19 not finished at 00:10 (the driver `esr-fvr-drv` is compiling `esr-fvr-c3519-C0119xx`
  chunks). cpu_free.sh esr = 3, Tctl 84 C at 00:10.
- 00:24:51 R2 started: unit `esr-ag-rv5-p2ax`, `lean/RV5P2Review.lean` sha256 `c441ce98…` (B9 moved last, B3 per-pair try/catch, per the advisor). Tools `tools/rv5p2_audit.py` and `tools/rv5p2_bind.py` written while it runs.
- 00:34:28 R2 done. Axioms of all four worker theorems and of the reviewer's re-elaborations exactly [propext, Classical.choice, Quot.sound]; TYPEEQ alpha=true defeq=true for the four end theorems and both N66 bounds; binders 8/8/9/9, none intermediate; RS.s35_19 MISSING; interpreter dumps equal rows_used15.txt (f45e25f1) and the l15 reviewer's leaves dump (5f188424).
- 00:37 R3 done (audit: 13,786 modules, one provider, all hashes equal earlier records, 0 component-env mismatches, ctime bounds hold, 4 N66 manifests clean; bind: 5 trims, 3 templates + 1 core, T208 sub-list, 4 rows byte-identical; fresh cake_lpr 5/5 ACCEPT, 1/1 negative rejected).
- 00:37:29 status.json read once (read-only): s35_19 still not done (3519 at 651 modules, no root/final).
- 00:45 review finished; nothing of this slot running. Result: `../VERIFY_combined-2.md` (four theorems CONFIRMED; H-T69 non-vacuity and Switch3519L15 NOT CONFIRMED; no required fixes).
