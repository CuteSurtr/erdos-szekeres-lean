# V12 review: highcap_v1.py, run_tree_v7.py, continue34_v12.py (track R, 18 Nov 2026)

## Verdict: READY WITH NOTES

Scope of the verdict:
- **`highcap_v1.py`** may be launched now against the live v11 loop `esr-lo-b35s20v11c`, with the exact command of §6.
  That command wraps it in a shell loop, because the tool exits as soon as nothing is selectable (note N1).
- **`run_tree_v7.py` + `continue34_v12.py`** (the inbox) may replace v11 at the loop's next restart. They are not needed
  to launch the side pass; they are needed before any side-pass witness can reach a round (§6.2).

Reasons:
1. **Soundness.** No new code path can make the loop accept a wrong row or close a context wrongly.
   - Rows still enter only through `cut34_v4 certify` and `append_cuts_v2` (literal `s VERIFIED UNSAT`); v12 changes
     neither.
   - An imported ctx file is a byte copy of what the unchanged fastbb2 wrote in a side packet. Its `master.txt` is
     byte-identical to the target's and its header equals the target's `contexts.json` entry. The rows it was solved
     with are a line prefix of the target's rows.
   - The final replay rechecks every file from scratch. In my tests imported files pass both trusted checkers, and an
     imported file with a deliberately broken tree is rejected by both (§2).
2. **Concurrency.** With `--above` equal to the loop's `--extra-cap` (300,000), the side pass and the loop never select
   the same context, because a context's record in `TOO_BIG.txt` only grows and the side pass never writes that file.
   - Checked on the live packet at 02:37 (v148) and 02:50 (v149): the open contexts split into three disjoint rule
     sets with no gap. The `--ctx` lists of the two running fastbb2 processes contain none of the side-rule contexts.
   - The only write into the live packet is the checked import: a temporary file, then `os.link`, which never
     replaces a file (§3).
3. **Liveness.** Every open context falls under exactly one rule (frontier, extra worker or side pass). A context above
   the side cap is recorded in `<side>/TOO_BIG.txt`, which becomes the split list. The remaining liveness gaps are
   operational: N1, N2, N4 and N5 in §4.
4. **Memory.** My own measurement of the trusted Python replay is 6.56-7.04 KiB per node, which confirms AS's 6.6-6.9.
   - Model: peak ≈ 26 MiB + 6.6-7.0 KiB × nodes ≈ 51 × gz bytes.
   - fastbb2 itself needs only about 0.2 KB per node.
   - **Recommended side cap: 1,000,000 nodes.** The resulting files need up to about 7 GiB each in the trusted
     replay, so big contexts must be replayed by one worker at a time (§5).

Claims filed: `r-v12-review-1118` (this review) and `r-replay-mem-1118` (the memory measurement); no verdict yet.

Nothing here is a bound or a tree. All counts are COMPUTED (logs, receipts, my own read-only scripts and tests).
Extrapolations are HEURISTIC. (20,15) is not closed and ES(8) ≤ 307 is not reached.

## 1. What was reviewed

| file | sha256 | predecessor | diff |
|---|---|---|---|
| `highcap_v1.py` | `1642fb3b01840bd5…` | none (new) | read in full |
| `run_tree_v7.py` | `7bde01a9da358b05…` | `run_tree_v6.py` `d6608ce9…` | `diff -u`: docstring, `--inbox` option, one block after the witness checks (lines 166-176) |
| `continue34_v12.py` | `ab93d16fd1386710…` | `continue34_v11.py` `81d2c9e2…` | `diff -u`: docstring, `--inbox`, finder = `run_tree_v7.py`, `--inbox` passed through |
| `V12_NOTES.md` (draft) | `173c2e69de7143d6…` | | read; §§1-4 checked where they bear on (1)-(5) |

- The tested tool versions are the reviewed ones: AS's receipts carry `tool_sha256` 1642fb3b… and `runner_sha256`
  7bde01a9…, and so do mine.
- Context read for the review:
  - `fastbb2.cpp`: `runSolve`, `writeCtxFile`, `saveMasterTxt` and the claim files. The source is `2e7e0707…` and the
    binary `39b724a2…`, both as pinned in FASTBB20261113; the binary was not rebuilt.
  - `fresh_replay_v3.py`, `replay34_v2.py` (frontier, envelope, descriptor), `scripts/omission_tree.py`, VERIFY308's
    `tcheck_b35.cpp`, `audit_followup_rows_v4.py` (its witness lookup), and the select/probe stages of
    `cut34_v4.py`/`probe35_v2.py`.
  - The memory guard's policy (`memguard.sh`).
- Pinned hashes: `/home/jay/research/data/roadmap-20261115/pm1115/r1118/reviewed_sha256.txt`.

## 2. Soundness (task item 1)

**Code reading, `import_ctx` (highcap_v1 lines 80-96).** A side file `ctx-<c>.json.gz` enters the target only if all
of the following hold:
- the target has no file for c;
- sha256(side `master.txt`) = sha256(target `master.txt`). `master.txt` holds no paths, only the master tree,
  certificates, contexts and pseudo-costs, so the same master means the same context numbering;
- the gz header `{context, missing, occupied}` equals the target's `contexts.json` entry for c;
- the body of the `rows.txt` the side solved with is a line prefix of the body of the version named by the target's
  `master.json` at import time.

The copy goes to `.import-ctx-<c>.<pid>.tmp` (fdatasync, sha256 compared with the source) and is linked in with
`os.link`, which fails rather than replace. Nothing in the import checks the tree itself; by design, the final replay
does that.

**The trusted replay is the gate, and imported files pass it.**
- `fresh_replay_v3` derives the context paths from `master.json` itself (`replay34_v2.frontier`). It checks each
  file's descriptor against its path and replays every leaf with `check_tree` on the final rows. It also requires the
  files to equal the master frontier exactly.
- A ctx file stores its leaves' (row, weight) pairs and capacity inline, so it is self-contained. A file made on an
  older, prefix row version replays on any later version, exactly like the loop's own older files.

**Tests** (my namespace `runs/b35s20/bb-r1118*`, copies of the live master files; outputs in
`/home/jay/research/data/roadmap-20261115/pm1115/r1118/`):

| test | what | result |
|---|---|---|
| T1 | `highcap_v1 --target=bb-r1118t --side=bb-r1118t-hc --ctx=1526,1516 --import` (unit `esr-ags-hct1`) | both closed and `imported`. The imported bytes equal the side bytes and also **equal the live loop's own files for 1516/1526** (sha `4d063e22…`, `7cf0aee7…`; fastbb2 is deterministic for a given master and rows) |
| T1b | trusted replay steps of `fresh_replay_v3.one` (`read_json`, `descriptor`, `envelope`, `check_tree`; my harness `replay_mem_r.py`) on the imported files, rows b35s20-v148 | **PASS**, minimum margin 1, pending 14 = path length |
| T1c | VERIFY308's `tcheck_b35` (rebuilt here, `g++ -O2`; rows from its `prep_rows.py`) on the test target | 1516, 1526 (and 870): 0 errors, margin 1. Global verdict NOT CONFIRMED only because 8,062 of 8,065 files are absent in the test target, as expected |
| T3 | cross-version: the side file of 1399 (solved with v148, 4,226 rows) `--import-only` into `bb-r1118w`, a copy of the live master files whose `master.json` named **v150** at 02:53 | `imported` (`target_version_at_import: b35s20-v150`). Trusted replay steps on v149 and v150 rows (4,242 / 4,258): **PASS**, margin 1 (`t3_crossver.out`) |
| T2a | first weighted leaf's weight list emptied, header kept; `--import-only` into `bb-r1118u` | **`imported`** (the import does not check trees). Then `check_tree` **REJECTS** it (`Nonpositive leaf margin at node 24`) and `tcheck_b35` rejects it (margin −471,240) |
| T2b | solved_with = b35s20-v610 (not a prefix of v148) | `refused: rows of b35s20-v610 are not a prefix of b35s20-v148` |
| T2c | the file of 1526 stored under the name `ctx-1527` | `refused: header differs from the target context` |
| T2d | side `master.txt` with one byte appended | `AssertionError: side master differs from target master` (nothing imported) |
| T2e | the target already has the context | `target already has the context` |
| | after T2 | target holds only its 2 files; no temporary file left |

So a wrong file can only make the final replay fail; it cannot make it pass.
- What the import gates protect is the loop's bookkeeping. A wrong imported file would count as closed and never be
  re-attempted until the final replay fails on it.
- AS's negative controls (`pm1115/ags1116/neg_import*.sh` and `.out`; V12_NOTES §5 was never filled in) agree with T2.

**Witnesses** (`run_tree_v7` inbox block, test T5; unit `esr-ags-rt7t5`, receipt `runs/b35s20/r1118t5.json`):
- Before use, every inbox witness is re-checked exactly against the rows of the slice that takes it: 35 distinct
  holes, state 0 occupied, every row satisfied.
- My inbox held 4 files: a valid witness (1252), one cut by the v148 rows, the valid holes under a closed context, and
  a duplicate.
- Receipt: `taken: [w-1-valid]`, `cut_by_rows: 1`; the other two were skipped. My own exact check (`wcheck.py`) agrees
  on both of AS's witness files.
- In a round, an inbox witness is treated exactly like a frontier witness. select/probe use only its holes, rows still
  need cake_lpr, and the batch audit finds the round's `WITNESS.json.r<k>w<i>` by sha256.

## 3. Concurrency (task item 2)

- **Writes into the live packet.** I listed every write in `highcap_v1.py`. Writes into the target are the temporary
  copy, the `os.link` and the `unlink` of the temporary file, and nothing else.
  - fastbb2 runs only on the side packet: its `outdir` is the side folder, so claims, `WITNESS.json`,
    `witness-ctx-*.json` and `fastbb.log.jsonl` all go there.
  - The side pass writes its own `TOO_BIG.txt`, logs and inbox, never the target's `TOO_BIG.txt`, `master.json`,
    `contexts.json`, claim or witness files.
  - The target's `master.json`/`contexts.json` are read only. fastbb2 rewrites them with tmp + rename, so reads are
    atomic.
- **Can the loop select a context the side pass is solving?** Not with `--above` = the loop's `--extra-cap`.
  - Frontier (run_tree_v6) = open contexts with record ≤ 150,000; extra worker = record in (150,000, 300,000];
    side = record > 300,000.
  - A record is a maximum over append-only lines, and only the loop appends to the target's file, so a context once
    above 300,000 stays there for the loop.
  - Live check (`sel_check.py`, own code, read-only; `live/sel_check_0237.out`, `live/sel_check_0250.out`):

    | time | open | frontier | extra | side | gap | running `--ctx` lists ∩ side |
    |---|---|---|---|---|---|---|
    | 02:37 (v148) | 6,312 | 6,243 | 65 | 4 (96, 100, 132, 152) | none | ∅ (frontier 6,342 listed, extra 67) |
    | 02:50 (v149) | 6,084 | 6,010 | 69 | 5 (96, 100, 132, 152, 220) | none | ∅ (frontier 6,230 listed, extra 71) |
- **If both ever wrote `ctx-<c>.json.gz`** (only possible with a smaller `--above`, or after a loop restart with a
  larger `--extra-cap`):
  - The import uses `link`, so it never replaces a file: it reports `target already has the context` or `target closed
    it meanwhile`.
  - fastbb2 skips a context whose file exists when it picks it. It renames its own finished file into place, so a
    worker that started before the import replaces the imported file with its own.
  - Both files are complete (tmp + rename/link) and valid outputs of the same fastbb2 for the same descriptor, and with
    equal rows they are byte-identical (T1).
  - Cost: duplicate work and a stale sha256 line in `imports.jsonl`. A replay running at that moment would report
    `file changed during check`, and a rerun fixes it.

## 4. Liveness (task item 3) and notes

Every open context is covered (no gap on live data). Notes, most important first; none is a soundness issue:
- **N1, the side pass exits when nothing is selectable** (`if not sel: break`). New contexts above 300,000 appear at
  the end of extra-worker slices (220 at 02:39). The §6 command reruns the pass every 10 min in a shell loop until
  17:50. Each round first runs `--import-only`, which imports any side file left unimported by a stop during an
  invocation. Tested (unit `esr-ags-wraptest`): the first round closed and imported 1399; later rounds found nothing
  and the loop ended on time.
- **N2, side-pass witnesses need v12 (or a checked start receipt) to reach a round.** Under v11 they wait in the inbox
  and in `status.json` (`stuck_on_valid_witness`). The side pass skips such a context until appended rows cut its
  witness. They are not lost, but nothing consumes them automatically before the switch (§6.2).
- **N3, contexts above the side cap are recorded only in `runs/b35s20/bb-hc1/TOO_BIG.txt`.** `status.json` does not list
  them. They are the split list for the successor-packet `--split-open` step (V12_NOTES §2), and nobody attempts them
  until then.
- **N4, end phase (inherited from v11, S1R's note D).**
  - The extra worker runs only while the frontier fastbb2 runs. Once the frontier list is empty, the band
    150,000-300,000 is attempted by nobody, and the v11 loop ends with `OPEN … only too-big contexts left`.
  - AS's HEURISTIC lower estimate (53 thread-hours on 16 Nov) puts that in the late morning at the earliest, with 6
    frontier threads.
  - Then restart the side pass on the same side packet with `--above=150000` (§6.3). The same side packet keeps its
    records, so there is no duplicate work.
- **N5, RSS-guard stop.** When the internal RSS guard stops fastbb2, the pass ends without recording the context, so a
  rerun retries the same context. fastbb2 needs about 22 MiB + 0.19 KB per node (AS's test runs: 45 MiB at 125,902 and
  50.5 MiB at 153,043 nodes; live extra worker high-water mark 66.5 MiB). At the 1,000,000 cap that is about 0.2 GiB,
  so this does not happen with `--rss-mib=600`.
- **N6, memory-guard track.** `esr-lo-highcap-1` is in track `lo` (3,200 MB) with the loop (unit peak 421 MB so far
  tonight; it never exceeded the 2,000 MB lo budget of 15-16 Nov). The guard stops the **largest** unit of a track
  that goes over budget, which is the loop, not the side pass. With about 0.25 GB for the side pass the headroom is at
  least 0.9 GB.
- **N7, footgun.**
  - `--side=bb/` or `--side=./bb` normalises to the target folder and passes the assert (`a.side!=a.target`,
    `SIDE.parent==RUN`). fastbb2 would then run on the live packet and the side logs would land inside it.
  - `--inbox` can also point anywhere.
  - Use exactly the §6 command. A future version should assert `SIDE.resolve()!=TGT.resolve()`.
- **N8, `run_tree_v7` with a malformed inbox file** (test T5b, unit `esr-ags-rt7t5b`).
  - The inbox block raises (JSONDecodeError, KeyError or assert) after the finder has run, so the receipt is not
    written. The slice's too-big records are lost: the context_too_big event of T5b never reached `TOO_BIG.txt`. The
    loop's finder stage returns non-zero and the loop ends.
  - Only `highcap_v1` writes the inbox, with validated JSON via tmp + `os.link`. Never put files there by hand.
  - If it happens: move the bad file out of `w-*.json`, then restart with `--start-version`.
- **N9, small items.**
  - A stop during an import can leave `.import-ctx-<c>.<pid>.tmp` in the live packet. Its name starts with `.`, so
    neither the `ctx-*.json.gz` globs nor `tcheck_b35` (which treats unexpected `ctx-*` names as fatal) see it.
  - `status.json` is not written atomically.
  - The `w1 not cut` warning of continue34 can name an inbox witness when the frontier found none.
  - Imported contexts do not appear in the target's `fastbb.log.jsonl`. Count closures by ctx files.
  - The batch audit's glob `runs/*/bb*/WITNESS.json*` also matches side-packet witness files of identical bytes. The
    audit result is unchanged; S1R noted the same for test files.

## 5. Memory and replay plan (task item 4)

**Own measurement** (`replay_mem_r.py`: one fresh child per context, `ru_maxrss`, the exact steps of
`fresh_replay_v3.one`; live files read-only, rows b35s20-v148; unit `esr-ags-replaymem1`, `t7_replaymem.out`):

| context | nodes | gz MB | peak after JSON load | peak total | KiB per node above the 26 MiB baseline | check |
|---|---|---|---|---|---|---|
| 1601 | 50,973 | 7.33 | 326.6 MiB | 362.0 MiB | 6.75 | PASS, margin 1 |
| 10 | 71,959 | 10.86 | 469.8 MiB | 520.5 MiB | 7.04 | PASS, margin 1 |
| 181 | 95,215 | 13.03 | 566.8 MiB | 635.7 MiB | 6.56 | PASS, margin 1 |

- Context 1601 reproduces AS's 361 MiB.
- Most of the peak is `json.load` (Python objects); `check_tree` adds about 0.7 KiB per node.
- The ratio is about 51 × the gz size, while `replay34_v2`'s own estimate (40 × gz + 80 MB) is low for big files.
- Time: about 45-50 µs per node on one thread.
- HEURISTIC extrapolation: 300k nodes ≈ 2.0 GiB, 600k ≈ 4.0 GiB, 1M ≈ 6.7-6.9 GiB per context and per worker. This is
  consistent with AS's context 188 (209,667 nodes) passing 1,384 MiB.

**Recommended side cap: 1,000,000.**
- In the extra worker's logs `c144s2.x`-`c148s3.x`, 31 contexts closed at 153,791-259,639 nodes and 5 went over
  300,000. Under any light tail, most contexts above 300,000 should close well below 1M (HEURISTIC).
- An attempt costs at most about 19 min of one thread.
- Every file stays replayable by one Python worker within about 7 GiB.
- Contexts that do not close at 1M go to the split list (N3).

**Replay plan for big contexts** (for the final fresh replay; nothing to do tonight):
- Today the largest live file is 36.8 MB gz (ctx-254), about 1.9 GiB in the Python replay. 159 files are over 15 MB gz.
- The big contexts cluster at low IDs (33, 96-254), and `fresh_replay_v3` hands `sorted(PATHS)` to `Pool(NW)` in
  chunks of 8. So NW workers can hold NW big files at once.
- Option A, no new code: `fresh_replay_v3.py <packet> <input folder> <outdir> 1` (one worker) in a unit with MemoryMax ≈ 1.25 × (0.03 GB + 51 × the
  largest gz size). That is about 9 GB once a 1M-node file exists, so run it after N66 frees memory or with the
  owner's OK.
  - Wall time ≈ 45-50 µs × total nodes. The 1,964 files present at 02:47 hold 78.7 M nodes ≈ 1.05 h; the whole slice is
    probably 3-5 h.
- Option B: a small reviewed wrapper around the same `one(c)`. Files over 15 MB gz run one at a time, the rest with
  NW = 6 at about 0.8 GiB each. This is new code in the trusted path and needs its own review.
- In both cases `tcheck_b35` remains the cheap second check (VERIFY308: 558 MB for 15.5 M nodes).

## 6. Launch commands (task item 5)

### 6.1 Side pass against the live loop (the main session decides and launches; I launched nothing against `bb`)

```bash
systemd-run --user --unit=esr-lo-highcap-1 -p CPUQuota=100% -p MemoryMax=800M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=$(( $(date -d '2026-11-18 18:05' +%s) - $(date +%s) )) --nice=10 \
  --working-directory=/home/jay/research/data/es308-20261114 \
  -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 \
  /bin/bash -c 'PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python; T=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/tools; A="--slice=20 --budget=35 --target=bb --side=bb-hc1 --deadline=2026-11-18T18:00:00+09:00"; while [ $(date +%s) -lt $(date -d "2026-11-18 17:50" +%s) ]; do $PY -B $T/highcap_v1.py $A --import-only; $PY -B $T/highcap_v1.py $A --above=300000 --cap=1000000 --rss-mib=600 --import; sleep 600; done'
```

- 1 thread. Memory about 0.25 GB (fastbb2 about 0.2 GiB at 1M nodes, Python about 40 MB), so MemoryMax 800M stays
  above the 80 % rule. The internal guard (600 MiB) trips before the memory guard's 95 % point (760 MB).
- `--above=300000` must equal the loop's `--extra-cap`. If the loop is restarted with other caps or on another
  packet (for example a `--split-open` successor), restart this unit with the new value and target.
- The side packet is `runs/b35s20/bb-hc1` (created on the first run as byte copies of the live master files). Logs,
  receipts, `imports.jsonl` and `solved_with.json` go to `runs/b35s20/bb-hc1-logs/`. Witnesses go to
  `runs/b35s20/bb-hc1-inbox/w-*.json`.
- Progress: `cat runs/b35s20/bb-hc1-logs/status.json` and `journalctl --user -u esr-lo-highcap-1`.
- Stop: `systemctl --user stop esr-lo-highcap-1`. This is safe at any time. A stop during an import can leave one
  `.import-ctx-*.tmp` in `bb` (N9). It is harmless; the main session may leave it or remove it once the unit has
  stopped. A context closed but not imported is imported by the next `--import-only`.
- The selectable set at 02:50 was 96, 100, 132, 152 and 220.

### 6.2 Is the inbox (v12) needed, or can witnesses go to a later restart with `--start-receipt`?

- **Closures need neither.** They are imported directly; this is most of the side pass's value.
- **Witnesses need one of the two.**
  - `--start-receipt` works with v11 unchanged, but there is no tool for it.
    - continue34_v11 trusts the receipt's `independent_exact_row_check: PASS` flags. It only asserts that
      `command[2]` is the current version's `rows.txt` and that `bb` is the packet.
    - So a hand-built receipt needs a script that rechecks every side witness against the current rows, which is
      exactly v7's inbox block. Otherwise a witness already cut gives an empty batch, and if no row is accepted the
      round ends with OPEN and the loop stops.
    - It is also one-shot: witnesses found later need another restart.
  - **v12 is the cleaner route.** It rechecks on every slice and automatically, and it was reviewed here.
- **Recommendation: do not stop the live loop for this.** Launch §6.1 now. Switch to v12 at the loop's next restart:
  its deadline at 18:00, or earlier if it ends with OPEN in the end phase (N4). The switch command uses the live
  loop's options plus `--inbox`:

```bash
# after esr-lo-b35s20v11c has stopped; V = the 'version' of the last event (FINISHED) in
# /home/jay/research/data/es308-20261114/continuation-b35s20v11c/events.json. If the stop came inside a round, use
# that round's receipt with --start-receipt (v9 procedure), unchanged in v12.
systemd-run --user --unit=esr-lo-b35s20v12a -p CPUQuota=700% -p MemoryMax=3G -p MemorySwapMax=0 \
  -p RuntimeMaxSec=<to the new deadline + 15 min> --nice=10 --working-directory=/home/jay/research/data/es308-20261114 \
  -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  /home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/tools/continue34_v12.py \
  --deadline=<new deadline> --start-version=V --slice=20 --budget=35 --bb=bb --threads=6 --max-ctx-nodes=150000 \
  --slice-seconds=600 --max-witnesses=12 --accept-per-witness=8 --probe-minutes=6 --probe-procs=4 \
  --extra-cap=300000 --extra-threads=1 --inbox=/home/jay/research/data/es308-20261114/runs/b35s20/bb-hc1-inbox \
  --out=continuation-b35s20v12a
```

  Never pass AS's test inbox (`bb-v12test-hc-inbox`) or my test inboxes to the live loop.

### 6.3 End phase (N4)

When the loop has ended, rerun §6.1 with `--above=150000` and the same `--side=bb-hc1`. This takes the 150k-300k band
plus everything not yet done, with no duplicate work. Keep `--above=300000` while any loop with `--extra-cap=300000`
runs.

In the end phase, a v12 loop with an empty frontier ends at once (`OPEN`) unless the inbox holds a valid witness. So it
must be restarted, with `--start-version` = its last version, whenever the side pass has left new witnesses. Nothing
automates that cycle yet (open item).

## 7. Observations (COMPUTED, not new results)

- O1: For a given master and rows, the side pass's files are byte-identical to the loop's own files (T1: 1516, 1526).
  In the target, an import cannot be told apart from a loop closure.
- O2: AS's test witness for context 1252 (`bb-v12test-hc-inbox/w-20261116T185058-c1252.json`, found at 153,043 nodes
  on b35s20-v701 rows, whose body equals live v148's) satisfies every row of live b35s20-v149 and b35s20-v150 (4,242 / 4,258
  rows, own check `w1252_v149.out`).
  - In the live loop, 1252 is in the extra worker's band (recorded at 150,001 in c148s1), so the live rows cannot
    close without a further round for it.
  - The loop will find this witness itself when its extra worker reaches 1252.

## 8. Files

- Work folder `/home/jay/research/data/roadmap-20261115/pm1115/r1118/` (`SHA256SUMS` there):
  - `NOTES.md` (step log), `reviewed_sha256.txt`;
  - `sel_check.py` and `live/` (command lines of the running fastbb2 processes, two checks);
  - `replay_mem_r.py`, `wcheck.py`, `t2_neg.sh`;
  - outputs `t1_*`, `t2_*`, `t3_crossver.out`, `t5_rt7.out`, `t5b_rt7.out`, `t7_replaymem.out`, `w1252_v149.out`;
  - `tcheck/` (rebuilt `tcheck_b35`, rows, per-context tables).
- Test namespace in `/home/jay/research/data/es308-20261114/runs/b35s20/`: `bb-r1118t*`, `bb-r1118u*`, receipts
  `r1118t5.json/.log`, `r1118t5b.log`; `bb-r1118w*` (T3). These are test data and are never to be used as live inputs.
- Units (all stopped): `esr-ags-hct1`, `esr-ags-rt7t5`, `esr-ags-rt7t5b`, `esr-ags-replaymem1`, `esr-ags-wraptest`.

## 9. Not checked

- AS's §1 throughput numbers.
- A full v12 round: AS ran one (v701, inbox witness 1252); its appended rows equal live v148's.
- fastbb2's internals beyond the file and selection logic.
- A rebuild of the fastbb2 binary.
- A 1M-node context, whose memory is extrapolated.

## Resume

- Read this file and `/home/jay/research/data/roadmap-20261115/pm1115/r1118/NOTES.md`.
- Reproduce the live check: `python3 /home/jay/research/data/roadmap-20261115/pm1115/r1118/sel_check.py
  /home/jay/research/data/es308-20261114/runs/b35s20/bb 150000 300000 300000 1000000`.
