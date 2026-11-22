# verify/: independent review of item n66enc-recheck (22 Nov 2026)

Reviewer slot rv4 (lens REBUILD + SOUNDNESS). Units `esr-ag-rv4-<job>`: 1 thread, MemoryMax 3000M, MemorySwapMax 0.
Writes only in `/home/jay/research/data/formalize-20261122/n66enc-recheck/verify/`. No git writes, no Lean builds,
none of the worker's scripts (`../tools/recheck.py`, `../tools/cu_check.sh`) is run. Deliverable:
`VERIFY_n66enc-recheck.md` (this directory).

## 1. Status

- 17:20 KST: plan written. `cpu_free.sh` showed 0 free threads at 17:17 (27.7 of 28), so `tools/launch.sh` waited
  outside any unit (bounded 45 min) for a free thread.
- 17:30:12: unit `esr-ag-rv4-n66v1` started (driver: prep -> run -> post). Prep done 17:31:30.
- 17:31-17:32: **leaves MATCH, eager MATCH, full:131 MATCH** with the frozen exe (details in
  `VERIFY_n66enc-recheck.md`).
- 17:40:27: **trims 132/132 MATCH** (125 distinct, 8 UP leaves share one 112-byte text, 1,183,383,419 bytes);
  negfull and negtrim reproduce the worker's SHA-256 exactly.
- 17:45:46: **own FULL leaves 0-26: 27/27 MATCH.** The worker's `esr-ag-n66r-full2` ended 17:34:08 (131/131 MATCH);
  its files were read only after that. VERIFY file written with all eight verdicts.
- 18:07:45: unit done, 268/268 pieces, exe frozen at start and end. **Own FULL 132/132 MATCH** (leaf 131 plus
  0-130). For all 267 pieces both ran with a printed hash, the printed SHA-256 and byte count equal the worker's.
  No unit of this review is running. **Final: all eight claims confirmed; two wording fixes** (run count 270;
  the 79.1 % memory figure is an estimate, HEURISTIC).

## 2. What is checked (claims of the recheck worker)

frozen-exe-identity, leaf-map, eager-match-frozen, full131-match-frozen, trims-132-match-frozen, controls,
memory-measured, fullall-extension-partial. Labels: all COMPUTED claims (deterministic program runs compared with
files and recorded hashes). No claim rests on a cake_lpr proof, so cake_lpr re-runs are out of scope.

## 3. Plan (own code)

- `tools/prep.py` (Python, own): hashes of inputs; expected values per leaf from campaign_status.json, cert.json,
  verify.json, layout.json, STATUS_campaign.md; FULL inputs re-derived (act from the state file `activated`, rows
  from `mono/rows_1832.json` filtered d = 1 and sorted, cross-checked with layout `row_list`); eager byte range from
  layout `eager` and the file itself; negative-control inputs.
- `tools/run.sh` (bash + coreutils, own): one exe at a time; before each start: YIELD absent, Tctl < 86 C,
  ag-track anon + 2400 MB <= 8000 MB, exe SHA-256 = frozen `98d121ba…aa46`. Output streamed through `tee` into
  `sha256sum` and `wc`, and into `cmp` against the reference (with byte offsets for the eager segment). Exe
  maxrss and exit code from `/usr/bin/time`. Resumable: a piece with a result line is skipped.
- `tools/post.py` (Python, own): verdicts per claim, distinct texts, sizes, clause counts, memory.

## 4. Results

See `VERIFY_n66enc-recheck.md` (verdicts, numbers, hashes) and `out/summary.json` (machine summary by post.py).

## 9. Resume

```bash
V=/home/jay/research/data/formalize-20261122/n66enc-recheck/verify
bash $V/tools/launch.sh esr-ag-rv4-<new name>     # waits for a free thread, then starts tools/driver.sh in a unit
# driver: prep (skipped when out/expected.json and out/plan.tsv exist) -> run.sh (skips pieces in out/runs.tsv) -> post.py
cat $V/out/status.json; python3 -I $V/tools/post.py   # progress and verdicts
```
