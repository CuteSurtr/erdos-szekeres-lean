# V12 notes: a concurrent high-cap side pass and a witness inbox for the (20,15) loop (track AS, 16 Nov 2026)

**Status 19:00 KST: draft, tests running. Implemented as new files and tested only in a separate namespace; NOT switched
live.** The live loop `esr-lo-b35s20v11b`, its packet `runs/b35s20/bb`, its inputs and its cut folders were only read.
Labels: measurements and test counts are COMPUTED (from logs, receipts and my own read-only scripts); forecasts are
HEURISTIC. No bound and no tree is claimed; (20,15) is not closed and ES(8) ≤ 307 is not reached.

**Summary.**
- **Measurement (§1).** In the v11 loop the finder takes 98.7 % of the wall time; select + probe + certify + append
  take 99 s in 2 h 3 min (1.3 %). The frontier loses about 1.5 % of its thread time at slice stops, the extra worker
  about 13 %. Throughput 232 closes per wall-hour over 15 Nov 20:36-22:39 plus tonight's first slice (3 + 1 threads).
- **Replay memory (§2), a constraint on any high-cap pass.** The trusted Python replay (`fresh_replay_v3.one`) needs
  about 6 KB per tree node: 51k nodes 335 MB; a 210k-node file went over 1.38 GB. So 300k ≈ 2 GB, 1M ≈ 6.5 GB and 3M ≈
  20 GB per context (HEURISTIC extrapolation). **The 3,000,000-node pass of V11_NOTES §4 would produce context files
  the trusted replay cannot check within the 24 GB machine budget.**
- **Design (§3).** `highcap_v1.py`: a side pass that runs at the same time as the loop, one fastbb2 invocation per
  context in its own packet, importing closures into the live packet under explicit checks, and leaving its witnesses in
  an inbox. `run_tree_v7.py` + `continue34_v12.py`: the loop takes still-valid inbox witnesses into its rounds.
- **Tests (§5)** in the namespace `inputs/b35s20-v70x`, `runs/b35s20/bb-v12test*`, `continuation-b35s20v12test`.

## 1. Tonight's loop, measured read-only (COMPUTED)

Script `/home/jay/research/data/roadmap-20261115/pm1115/ags1116/measure_v11.py` (mine, read-only; output
`measure_1848.out` in the same folder). Sources: `W/continuation-b35s20v11a|b/events.json`, the finder logs and
receipts `W/runs/b35s20/c14*.{log,x.log,json}`, and `runs/b35s20/bb/TOO_BIG.txt`. A slice starts at receipt
`finished - seconds`; "unaccounted" = threads x wall - (seconds of closed contexts) - (nodes of too-big and witness
attempts / the slice's node rate). That is mostly the work lost when the slice stops a worker in mid-context.

| finder slice | start | wall s | frontier closes | frontier nodes/thread-s | frontier too-big | witnesses | extra-worker closes / too-big | closes per wall-hour | frontier unaccounted | extra unaccounted |
|---|---|---|---|---|---|---|---|---|---|---|
| c144s2 | 15 Nov 20:36:29 | 769 | 17 | 890 | 5 | 1 | 3 / 0 | 93.6 | 7.9 % | 23 s |
| c145s1 | 20:49:39 | 2,548 | 76 | 850 | 11 | 1 | 7 / 2 | 117.3 | 0.4 % | 206 s |
| c146s1 | 21:32:33 | 1,299 | 45 | 878 | 7 | 1 | 3 / 1 | 133.0 | 1.0 % | 193 s |
| c147s1 | 21:54:39 | 732 | 42 | 861 | 0 | 1 | 2 / 0 | 216.4 | 2.3 % | 286 s |
| c148s1 | 22:07:18 | 1,943 (deadline) | 261 | 878 | 1 | 0 | 7 / 1 | 496.6 | 0.4 % | 173 s |
| c148s2 (tonight, running at 18:48) | 16 Nov 18:19:33 | 1,706 so far | 126 | 898 | 2 | 0 | 7 / 0 | 280.7 | 0.9 % | 82 s |

- **Time split of the loop** (v11a, 2 h 3 min): finder 7,292 s; select 2 s, probe 48 s, certify 48 s, append 1 s. The
  round work is **1.3 %** of the wall time (each round 20-30 s; probe35 ends in 10-15 s, far below its 6-minute limit).
  Tonight's loop had only its first finder slice by 18:48.
- **Throughput:** 238.5 closes per wall-hour over all six slices (567 frontier + 29 extra-worker closes in 2.5 h);
  frontier node rate 874 nodes per thread-second.
- **Losses at slice stops:** frontier 1.3 % of its thread time (small contexts, about 33k nodes on average); the extra
  worker 10.7 % (it restarts its 150k-300k-node context from scratch in every slice).
- **TOO_BIG.txt growth:** 3,391 lines at the v11 switch (15 Nov 20:36) → 3,419 at 18:48 (+28: frontier 25, extra 3,
  all at 150,001-150,003 or 300,001-300,002). Open contexts recorded above 150,000: 77 at 18:25, 72 at 18:48 (the extra
  worker closes about 11-15 per hour of them); above 300,000: **4** (96, 100, 132, 152).
- **Rounds (all history, 48 appended rounds):** no batch with zero accepted rows and no witness left uncut since the
  probe was added on 14 Nov.
- **Remaining frontier (HEURISTIC):** the 6,428 open contexts not recorded above 150k, weighted by the mean size of the
  closed contexts of their |missing| stratum (from the finder logs), come to about 165 M nodes, i.e. about 53
  thread-hours at 871 nodes per thread-second: about 18 h at 3 frontier threads, 13 h at 4, 6.6 h at 8. The means
  come from contexts that closed under the caps, so this is a lower estimate; A2's model (174 M) agrees.

## 2. Replay memory per context (COMPUTED; extrapolation HEURISTIC)

`/home/jay/research/data/roadmap-20261115/pm1115/ags1116/replay_mem.py` runs exactly `fresh_replay_v3.one`'s steps
(`replay34_v2.read_json`, `descriptor`, `envelope`, `omission_tree.check_tree` with the 4,226 rows of v148) on single
live ctx files, read-only, in unit `esr-ags-replaymem` (MemoryMax 1400M):

| context | nodes | gz MB | peak RSS | result |
|---|---|---|---|---|
| 1601 | 50,973 | 7.3 | 361 MiB (26 MiB before loading) | margin 1, 14 pending (the path), 2.2 s |
| 188 | 209,667 | 29.1 | **over 1,384 MiB**: the memory guard stopped the unit at 95 % of its limit (no OOM kill) | not finished |

That is about 6.6-6.9 KiB per node (Python dicts and lists of the JSON; the 88 MB JSON of context 188 is 420 bytes
per node). Extrapolated: **300k nodes ≈ 2 GiB, 1M ≈ 6.7 GiB, 3M ≈ 20 GiB per context and per replay worker.** The
C++ checker `tcheck_b35` is much leaner (VERIFY308: 558 MB for all 15.5 M nodes of the budget-34 slice 20), but the
trusted replay is the Python one. Consequences:
- The 3,000,000-node pass of V11_NOTES §4 would make files that the trusted replay can only check with nearly the
  whole 24 GB research budget for one worker. A cap of 1,000,000 keeps every file below about 7 GiB in the replay;
  then the final `fresh_replay_v3.py` should run the large contexts with few workers (it uses `Pool(NW)` over
  `sorted(PATHS)` with chunksize 8, so large contexts can meet in one batch).
- Already now the extra worker's 200k-300k-node files need 1.4-2 GiB each in the replay (about 100 such files by the
  end). The final replay must be sized for that.
- Contexts that stay above the side-pass cap should be split, not solved whole: at the end, when only they remain open,
  a successor packet with `--split-open` (the 14 Nov budget-34 procedure, `prepare_successor.py`, written for
  `runs/s20`) gives each one 2^L smaller contexts (§6.4).

## 3. Design: a side pass that runs with the loop

New files (the loop's own files are unchanged; v11 keeps working as it is):

| file | role |
|---|---|
| `tools/highcap_v1.py` | the side pass (finder only) |
| `tools/run_tree_v7.py` | `run_tree_v6.py` + `--inbox=DIR`: still-valid side-pass witnesses join the finder receipt |
| `tools/continue34_v12.py` | `continue34_v11.py` calling `run_tree_v7.py` and passing `--inbox` |

SHA-256 values and the exact diffs are in §3.4.

### 3.1 `highcap_v1.py`

- **Its own packet.** `runs/b35s20/<side>` (a new folder) receives byte copies of the target's `master.txt`,
  `master.json` and `contexts.json` at the first start. fastbb2 then resumes the same master, so context numbers and
  descriptors are the target's. It never runs fastbb2 on the target, so the target's `master.json`, `contexts.json`,
  claim files and `WITNESS.json` are never touched (the conflict named in V11_NOTES §5, third bullet, cannot arise).
- **One context per fastbb2 invocation**, with exactly run_tree_v6's search options (`solve <rows> 35 1 2048 <side>
  --slice=1 --on-witness=continue --time-limit=<to the deadline> --max-ctx-nodes=<cap> --ktop=16 --dtop=8 --klow=4
  --sbiter=1000 --ctx=<c>`). An invocation ends when its context closes, is too big at the cap, or has a witness. So
  no work is lost at slice ends (the extra worker loses about 11 %, §1), and every invocation starts on the newest rows.
- **Rows:** the version named by the target's `master.json` (`"extra"`), re-read before every invocation. That is the
  version of the loop's newest finder, always a completely appended version. Input hashes (rows.txt, extra.json, the
  source, the fastbb2 binary) are compared before and after each invocation, as in run_tree.
- **Selection,** recomputed before every invocation: open target contexts (no `ctx-<c>.json.gz` in the target) whose
  largest line in the target's `TOO_BIG.txt` exceeds `--above`, minus those recorded in the side packet's own
  `TOO_BIG.txt` above `--cap`, minus those whose last side witness (`<side>/witness-ctx-<c>.json`, written by fastbb2)
  still satisfies every row of the current version, in ID order. With `--above` equal to the loop's largest cap
  (v11 live: `--extra-cap=300000`) the loop never selects these contexts, so the two never work on the same context.
  `--part=k/m` splits the contexts between several side passes (one side packet each).
- **After each invocation:**
  - `closed`: with `--import`, the ctx file is copied into the target if all checks pass (§3.2);
  - `context_too_big`: a line `<c> <nodes_so_far> h<k>` in the SIDE packet's `TOO_BIG.txt` (the target's record is
    only read);
  - `WITNESS`: the same exact row check as run_tree (35 distinct holes, state 0 occupied, every row of the version);
    then a new file `<inbox>/w-<time>-c<ctx>.json` with holes, context, version and log;
  - the packet `WITNESS.json` that fastbb2 writes at a natural end is renamed `WITNESS.json.before-h<k+1>` before the
    next invocation (otherwise fastbb2 would stop at once with `old_witness_still_valid`);
  - a receipt `<side>-logs/h<k>.json` (command, exit, input hashes, events, import result, inbox files) and
    `status.json` (counts, selectable contexts, contexts waiting on a valid witness).
- **Guards:** child RLIMIT_AS 1,400 MiB (as run_tree), an RSS/swap guard (default 1,000 MiB), an outer wall guard,
  and a stop when an invocation gives no result for its context.
- `--import-only` imports the side packet's closed contexts without running anything (for a pass run without
  `--import`, or after a refused import).

### 3.2 The import (`import_ctx`)

A ctx file closed in the side packet enters the target only if all of the following hold, checked at import time:
1. the target has no `ctx-<c>.json.gz` yet;
2. the side packet's `master.txt` is byte-identical to the target's (the runner also asserts this at start);
3. the header of the gz file (`{"context": c, "missing": [...], "occupied": [...]}`) equals the target's
   `contexts.json` entry for c;
4. the body of the `rows.txt` the side invocation solved with (its 4,2xx row lines after the 8-line header) is a line
   prefix of the body of the `rows.txt` of the version that the target's `master.json` names at import time.

The copy goes to `.import-ctx-<c>.<pid>.tmp` in the target (a name outside `ctx-*.json.gz`, so no fastbb2, run_tree or
replay sees it), is fsynced and compared by SHA-256 with the source, and is then put in place with `os.link`, which
fails rather than replace an existing file. Every import adds a line to `<side>-logs/imports.jsonl` (context, SHA-256,
bytes, solved-with version, target version). The bytes are exactly fastbb2's output.

### 3.3 The inbox in the loop (`run_tree_v7.py`, `continue34_v12.py`)

At the end of each finder slice, after its own witnesses, run_tree_v7 reads `DIR/w-*.json` in name order and adds an
entry to the receipt's `witnesses` only if its context is still open in the packet, its holes are not already in the
list, and it passes the same exact row check as the finder's own witnesses against this slice's rows. Entries cut by
a later row are skipped (counted in `inbox.cut_by_rows`). The total is capped at `--stop-witnesses` (the loop's
`--max-witnesses`), so no taken entry is left out of the round. Nothing is written into DIR; an entry is taken again
in a later round only while no appended row cuts it, the same way the frontier re-finds an uncut witness. The receipt
freezes the round's list, so an interrupted round resumes with `--start-receipt` exactly as before. continue34_v12
only passes `--inbox`; the round code is v11's. Inbox entries do not end a slice: they wait for the slice's end (the
next own witness plus `--slice-seconds`, or the end of the frontier list).

## 4. Why it is sound

- **Context files.** Every file the import adds is a byte copy of a file that the unchanged fastbb2 wrote (tmp +
  rename) for a context it closed in a packet whose `master.txt` is the target's, with the run_tree search options
  and a version whose rows are a line prefix of the target's rows at import time. A ctx file stores only its context
  descriptor and the tree (row indices and integer weights at the leaves); it names no version. Rows are append-only
  (`append_cuts_v2.py` asserts the prefix; checked again here per import), so the file stays valid for every later
  version, exactly like a context the loop closed on an older version. The trusted path is unchanged:
  `fresh_replay_v3.py` and `tcheck_b35` re-check every ctx file from scratch against the final rows and require the
  files to cover the master frontier. A wrong file could only make that replay fail, never pass.
- **Nothing in the target is rewritten.** The side pass never runs fastbb2 on the target. Its only write into the
  target is the link of a new `ctx-<c>.json.gz` (plus the temporary file, removed after the link). It does not write
  the target's `TOO_BIG.txt`, `master.json`, `contexts.json`, `WITNESS.json*` or claim files.
- **No interference with the loop.** The loop's selections are fixed at each slice start from its record and the ctx
  files present. A context recorded above the loop's largest cap is never selected by the loop (v6/v7 selection), and
  only such contexts are selected by the side pass, so no context is solved by both. If one ever were (for example an
  `--above` below the loop's extra cap), the cost is duplicate work, not a wrong file: the import skips a context
  whose file exists, a fastbb2 worker skips such a context when it picks it, and if both finish, fastbb2's rename
  replaces one valid file by another. The loop's
  `inputs changed during finder` assert covers only input files, not the packet.
- **COMPUTED_CLOSED** still requires fastbb2's own count over the full master (`closedFiles == m.ctxs.size()`), now
  including imported files; the final replay is still required.
- **Witnesses only steer row generation.** An inbox witness enters a round only after the exact row check against
  that round's rows; a row's validity rests on its own cake_lpr certificate (`cut34_v4.py certify`,
  `append_cuts_v2.py`: literal `s VERIFIED UNSAT`, hashes), never on the witness. The batch audit finds the round's
  `WITNESS.json.r<k>w<i>` in the live packet as before.
- **The side packet's files are not evidence.** Its record, witnesses and logs are COMPUTED finder output. A context
  that it closed but did not import (import off or refused) stays open in the target.

## 5. Tests

(filled in below)

## 6. Launch and switch commands

(filled in below)

## 7. Other speedups

(filled in below)

## 8. Caveats and what remains

(filled in below)
