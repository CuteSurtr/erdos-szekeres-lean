# V11 review: the skip list for the (20,15) finder (track S1R, 15 Nov 2026, 20:22-20:45 KST)

**Verdict: READY WITH NOTES.**
- The change cannot make the loop accept a wrong row or wrongly close a context.
- The round path after the finder (witness checks, cut34/probe35/append) is unchanged.
- The test wrote nothing into the live packet, the live inputs or the live cut folders.
- The notes cover liveness: near the end the extra worker gets little or no time, so the standalone pass is needed. They also cover wording and two harmless cross-reads.
- None of the notes blocks the switch.

**Claim.** Filed as `s1r-v11-review` at 20:35:50 (`pm1115/claims/s1r-v11-review.claim.json`). VS **CONFIRMED** it at 20:40:39:
- parts B and C at COMPUTED, with VS's own read-only code;
- parts A and D by VS's own reading of the code.

Report: [VERIFY_V11_REVIEW.md](VERIFY_V11_REVIEW.md).

**The live loop was switched after these checks.** The main session started `esr-lo-b35s20v11a` (continue34_v11, `--start-version=144`,
3 frontier threads plus 1 extra, extra cap 300,000) at 20:36:29, after stopping v10c during finder c144s1 (exit −15, `FINISHED stopped=True`
at 20:36:27). So §5 describes the live packet as of 20:34. In particular, the live packet has had a `TOO_BIG.txt` since 20:36:29.

Read-only at 20:41 (COMPUTED):
- **Live record.** 3,391 lines. 77 of them are tagged c143s2 and 44 are tagged c144s1; each count equals that log's too-big events, so the stopped finder's
  log was included.
- **First v11 frontier.** c144s2 closed 4 contexts in its first 299 s (1123 and 1124 among them; todo 6,947). Before the switch, each round's
  first 41-54 min went to re-walking recorded contexts.

**Labels.** Statements about code come from reading it. My own checks are COMPUTED: counts and set equalities from logs, receipts and file times, using my own scripts (§8). Nothing here is a bound or a tree. (20,15) is not closed. This review neither starts nor stops anything, and it changed no existing file.

**What I reviewed** (SHA-256 recomputed at 20:22):

| file | SHA-256 |
|---|---|
| `run_tree_v6.py` | `d6608ce9f4d8282468debc1fac2343d03217a29af49621dfd3bb4a2c750c0da3` |
| `continue34_v11.py` | `81d2c9e26ef858f3bf63c9b04477bdf9ad1e38bd29151c59357412e9bc5d2d7f` |
| `init_too_big_v1.py` | `2964a09386ae1eabb71afc64592bbc70a94a34576ddd488ca32895cfe8a69219` |
| `run_tree_v5.py` (base) | `ce1e9b4e4d44113ca19bc5eddc785e5cd5d9a5f9ef3fb836210bc75385e27693` |
| `continue34_v10.py` (base; the live v10c loop runs it) | `8f37ddfcc990bedeb1e0febf8bf40a549eb8a3da3ae92863d015565319108d0e` |
| `cut34_v4.py` (unchanged) | `906db1631569e3e1cf445e00213d1b8e6a3f5c099bdc2e5ce86304fc6789f2b8` |
| `probe35_v2.py` (unchanged) | `b9948e959a0b1a9a2521bd662ae42962f5eeb41859adaf539a3f054e17ee29ca` |
| `append_cuts_v2.py` (unchanged) | `5f0d190514732a910d754e167478529d0ced19f2cdf5f4530bc554c2661131fc` |
| `FASTBB20261113/tools/fastbb2.cpp` (source read) | `2e7e0707b3cc40acd10806c03a8aabbbdb7a59ebd6e4d99d7a7035d5df9c1b18` |

I did not rebuild `bin/fastbb2` (`39b724a2…`), so the statement that it is built from this source comes from the earlier records.

## 1. Diffs (COMPUTED)

- My own `diff -u` of v5 → v6 and of v10 → v11 is byte-identical to the diffs printed in [V11_NOTES.md](V11_NOTES.md) §1 and to the saved files
  `pm1115/s1/run_tree_v5_v6.diff` and `continue34_v10_v11.diff` (only the header lines were not compared).
- continue34_v11 differs from v10 in only three places: the docstring, two argparse lines, and the finder call (`run_tree_v6.py`, plus
  `--extra-cap`/`--extra-threads` when set). Unchanged:
  - the select, probe, certify and append calls and their arguments;
  - the receipt, candidate and witness asserts;
  - the snapshot step;
  - the resume logic.

## 2. Check (1): no wrong row, no wrong closure

- **Context files.** Only fastbb2 writes them: `writeCtxFile` (`.tmp`, then rename), called after a context's `expand` finished without a
  witness, too-big or stop exception. v6 changes only three things in the fastbb2 command:
  - the `only` list (`--ctx`), which decides which contexts go into `todo`;
  - for the extra worker, `--threads`;
  - for the extra worker, `--max-ctx-nodes`.

  No v6 code writes or deletes a ctx file, and nothing reads `TOO_BIG.txt` as "closed". The record only feeds the two
  selection lines (`lst`, `xl`).
- **No false COMPUTED_CLOSED.** The loop logs `COMPUTED_CLOSED` only when the frontier receipt has no witness and exit 0. fastbb2 returns 0
  only when every context of the *full* master has a ctx file: `all = closedFiles == m.ctxs.size() && !haveWitness`, counted over `m.ctxs`
  and not over the selection. With any open context skipped, the exit is 4 or 5, never 0. u610d (todo 0) exited 5. The loop never reads the
  extra worker's exit code; it is kept only in the receipt's `extra.exit`.
- **`--ctx=-1`.** fastbb2 reads each comma-separated piece with `atoi` into `only`. The value −1 matches no context ID, because IDs are ≥ 0. An empty `--ctx=`
  would leave `only` empty, which means all contexts; v6 never passes it. u610d confirms: todo 0.
- **Extra-worker command.** It differs from the frontier command only in threads, `--max-ctx-nodes` and `--ctx`. Everything else is the same:
  the rows file, the packet, `--slice=1`, `--on-witness=continue`, the time limit and the search options. COMPUTED on the c600s1 and c601s1
  receipts.
- **Rows.** They still come only through `cut34_v4.py certify`, which requires the literal `s VERIFIED UNSAT` line, and `append_cuts_v2.py`.
  A witness from either worker only steers candidate selection.
- **Trusted replay.** `audit/fresh_replay_v3.py` reads `master.json`, `contexts.json` and `ctx-*.json.gz` and requires them to cover the master.
  It never sees `TOO_BIG.txt` or a `.x.log`. A stale or wrong record line can only leave a context unattempted, and the replay then fails safe.

## 3. Check (2): the witness and row path behaves as before

- **Witness checks.** The packet `WITNESS.json` check and the per-witness exact row check in run_tree_v6 are the v5 lines. The only change
  is the list they run over: now the WITNESS events of both logs. Both workers read the same input folder, so every witness is checked
  against the round's rows (the 2,650 base rows plus `extra.json`).
- **Downstream tools.** `cut34_v4.py`, `probe35_v2.py` and `append_cuts_v2.py` were last modified on 14 Nov. continue34_v11 calls them with
  v10's arguments, and the live v10c loop calls the same three files.
- **What does differ** (none of it touches a row):
  - the receipt has new fields;
  - `witnesses` can now include extra-worker witnesses, frontier witnesses first;
  - `--witness-grace` and `--stop-witnesses` count both logs;
  - `todo` and `processed` count the frontier only.

## 4. Check (3): can the skip list hide a context for good?

- **Every open context can still be reached.** No context is ever marked closed by the record, and some mode selects every open context
  once its cap is high enough:
  - the frontier at cap C takes every open context whose largest record is ≤ C, unrecorded ones included;
  - the extra worker takes the range (C, X];
  - `--too-big-only` at cap Y takes (0, Y].

  So the only contexts the loop never attempts at fixed caps are those recorded above its extra cap (96 and 100 in the test). The notes
  say these need the standalone pass before the final replay can pass (V11_NOTES §2, last paragraph; §5, first bullet), and the replay
  fails safe until then.
- **Split-open.** A later `--split-open` run gives the open contexts new IDs, starting above the old maximum. The old lines then match no
  open context, and the new contexts have no record. That is harmless.
- **Liveness: the extra worker runs only while the frontier process runs** (it starts after the frontier's `start` event and is halted when the frontier ends). This
  corrects V11_NOTES §5, second bullet.
  - **Empty frontier selection.** run_tree_v6 passes `--ctx=-1`, and fastbb2 exits right after its start event. The extra worker gets at most
    about one poll interval (1 s) or does not start at all. The loop then logs `OPEN` ("finder ended without a witness") and `FINISHED`.
  - **Other early slice ends.** The extra worker can be halted before it finishes a context in three cases:
    - the frontier runs out of contexts early;
    - `--stop-witnesses` (12) is reached quickly;
    - the deadline arrives.

    Its context in progress is then started again from scratch in the next slice.
  - **Where §5 is too strong.** "Each slice then finishes at least one extra-worker context …, so the worker cannot get stuck" holds only
    when both conditions are met: the slice ends by the witness grace (≥ 600 s live), and the worker's attempt fits in it (about 340 s for
    300,000 nodes at A2's rate). It does not hold in the cases above.
  - **Consequence.** Expect the v11 loop to stop with `OPEN` once the frontier list runs dry. From then on only the standalone
    `--too-big-only` pass (V11_NOTES §4, step 4) works on the recorded contexts. This is about progress, not soundness.
- **Receipt field.** In `--too-big-only` mode, `skipped_known_too_big` is open minus selected, so it also counts contexts with no record. In
  u610c it is 58: 28 contexts recorded above 40,000 plus 30 never recorded. COMPUTED.

## 5. Check (4): the test namespace was separate (COMPUTED; files read 20:24-20:34)

**Live packet `runs/b35s20/bb`.** 54 entries changed since 19:00, each traced to the live loop:
- **43 ctx files.** Their set equals the 43 `closed` events of the live finder c143s2. The live finder c144s1 had closed none by 20:34.
  - The extra worker's closed contexts 0, 33, 51, 80, 81 and 97 have no live ctx file.
  - The test frontier closed 31 contexts. Live c143s2 also closed 30 of them in its own run, 19:47-19:56: 1069, 1074-1094 and 1096-1103.
  - The 31st, 1095, is still open in the live packet. It is c143s2's witness context, and the test closed it only with its test rows
    (v601).
- **Witness files.** `witness-ctx-1095.json` (19:53:07) and `witness-ctx-1106.json` (19:56:30) are c143s2's two WITNESS events. The test's
  witness for context 1095 is in `bb-v11test/witness-ctx-1095.json` (19:53:46). It has the same holes because the rows are the same.
- **Round and start files.**
  - `WITNESS.json.r144w1` and `r144w2` (20:03:08, 20:03:31) belong to live batches v144w1 and v144w2 in
    `continuation-b35s20v10c/events.json`.
  - `master.json` and `contexts.json` (20:03:59) were rewritten at the start of c144s1.
  - `fastbb.log.jsonl` (20:02:12) has the same mtime as c143s2.log.
- **Claim files.** Every claim file names pid 2635418, the live c144s1 fastbb2 on `b35s20-v144`.
- **No record.** The live packet has no `TOO_BIG.txt`.

**Other live folders.**
- **`W/inputs` since 19:00.** Test inputs: `b35s20-v600` (19:10:17), `v610` (19:31:43) and `v601` (19:59:13). Live: `b35s20-v144` (20:03:59,
  the `CERTIFIED_ROWS_APPENDED` event). The live `v143` was last written at 17:45:04, and v600 equals it byte for byte (rows `e8584de6…`, extra
  `3313ff96…`).
- **`W/cuts-v1*` since 19:00.** Only `cuts-v144w1u` and `cuts-v144w2u` changed (76 entries each), and both are live batches.
- **Test files at W level.** `cuts-v601w1u`, `candidates-v601w1{,p,u}.json`, `accepted-v601m.json` and `continuation-b35s20v11test`.

**Test runs.**
- Every fastbb2 command in the test receipts (c600s1 and c601s1, both workers; u610a-d) writes to `bb-v11test` or `bb-v11test2` and reads rows
  from v600, v601 or v610.
- The test packet's files are separate inodes (link count 1), so they are copies, not hard links. `copy_packet.py` opens the live files
  read-only.

**Shared folders.** The test sits in the live folders under its own version numbers, as the v9 test did with v50x. Three things follow from
that; none changes a live result:
- **Batch audit.** `audit/audit_followup_rows_v4.py` finds a batch's witness by SHA-256 over `runs/*/bb*/WITNESS.json*`, and that pattern
  also covers `bb-v11test*`. The test file `bb-v11test/WITNESS.json.r601w1` is byte-identical to the live `bb/WITNESS.json.r144w1`
  (`124cf196…`), so the audit of live batch v144w1 will match both. It sorts by name, takes `WITNESS.json.r144w1`, and freezes only the
  matched bytes, so its result cannot change.
- **Test packet provenance.** The test input v600 is a byte copy of v143. Its `rows.txt` header, and so the test packet's
  `master.json.v600-snapshot`, therefore names the live `inputs/b35s20-v143/extra.json`. That file is only read, and its bytes are the same.
- **Newest input.** `W/inputs` now lists v610 as the highest version. Read the resume version from `events.json`, as the notes do, and
  never from a directory listing.

## 6. My checks of S1's test numbers (COMPUTED; `check_sel.py`, 20:33)

- **Record.** I rebuilt the record from the 45 live receipts written before 19:10 whose packet is the live one: 3,270 too-big events. As a
  multiset they equal the first 3,270 lines of `bb-v11test/TOO_BIG.txt`. The SHA-256 of those lines is `08a7a1f8…`, the same as c600s1's
  `skip_file_sha256_before`. Lines 3,271-3,272 are `96 300001 c600s1.x` and `100 300001 c601s1.x`.
- **c600s1.**
  - Selection: 7,067 open contexts. The frontier `--ctx` list is exactly the open contexts minus those recorded above 150,000 (6,992, in
    master order). The extra list is exactly the open contexts with a record in (150,000, 300,000] (75).
  - Frontier: no event names a skipped context, and it had 0 too-big events.
  - Extra worker: every event lies in its list. It closed 0, 33, 51, 80, 81 and 97, and recorded 96 at 300,001.
  - Witness: one, at context 1095; the exact row check passed.
- **c601s1.** The record SHA matches the receipt. Of 7,036 open contexts the frontier took 6,967 and skipped 69; the extra list held 68. No
  frontier event names a skipped context. The extra worker recorded 100 at 300,001.
- **u610a-d.** As stated in V11_NOTES §3.3:
  - selected 36, 32, 6 and 0 contexts;
  - too-big events 24, 28, 30 and 31 in u610a, then 32 and 33 in u610b, all at about 20,000 nodes, and 24 at 40,001 in u610c;
  - u610d passed `--ctx=-1`, had todo 0 and exited 5.

## 7. Smaller points (no action needed before the switch)

- **Natural-end `WITNESS.json` from the extra worker** (untested, as the notes say). The worst case:
  - continue34's warning "w1 (the packet WITNESS.json) not cut" names the wrong witness;
  - the next finder stops at once on a packet witness that no row cut (`old_witness_still_valid`), which costs one quick round.

  It never produces a wrong row.
- **Claim files.** `clearStaleClaims` deletes a claim file whose PID it cannot read, so it would also delete one the other process has just
  created but not yet written. The two lists are disjoint, so no context can be taken twice.
- **`master.json` / `contexts.json`.** The extra worker starts only after the frontier's `start` event. fastbb2 prints that event after
  writing both files and clearing stale claims. Both files are built deterministically from `master.txt` and the rows header, so the
  rewrite is byte-identical. continue34's snapshot assert would stop the loop if it were not.
- **Argument length.** `--ctx` is passed as one argv string: about 40 KB at 8,065 contexts. Linux limits a single argument to 128 KiB, so a
  packet with roughly 25,000 or more contexts would make the call fail. That would be a crash, not a wrong result.
- **Memory.**
  - The live 4-thread fastbb2 peaked at 201-207 MB (receipts c141s1-c143s2). A 3 + 1 split adds one 1-thread process, which used about
    70-75 MB in the test.
  - The v10c unit's peak is 702 MB under its MemoryMax of 2G. The 2G in the switch command is enough.
  - The memory guard's lo track allows 2,000 MB, so v10c and v11 must never run at the same time. The notes already say to stop v10c first.
- **Switch order.** Create the live record after v10c has stopped and before v11 starts (V11_NOTES §4, steps 1-3). If step 2 is skipped,
  the first v11 slice re-walks the recorded contexts as v10 did and starts `TOO_BIG.txt` itself. `init_too_big_v1.py` then refuses to run
  because the file exists, and the older events enter the record only when those contexts are attempted again. That costs time, not
  soundness.
- **Not checked: replay cost of large contexts.** The extra worker's 261k-node contexts produce ctx files of 28-37 MB gz; the largest live
  files are about 21 MB. Before the 3,000,000-node standalone pass, estimate the trusted replay's memory per context (Python JSON).

## 8. Files and what I did not check

My own scripts (read-only, foreground, under a minute each, single-threaded BLAS) are in
`/home/jay/research/data/roadmap-20261115/pm1115/s1r/`:

| file | SHA-256 | what it checks |
|---|---|---|
| `check_sel.py` | `8e4c12aba4193a032676c3df475f876a0576ce192a4c41f787ddd34947b5132d` | the record, the selections and the unit test |
| `check_sel.out` | `112db3f2f516854795cda296f305b28295b300d2055b1a33618887102f5d285c` | its output |
| `check_sep.py` | `2dbac299dddbc3a7573ebd233bfe3f4854c8b97bfa6d620feb8b8f5f30e553b6` | separation from the live folders |
| `check_sep.out` | `8b556c2bbd95e85e838849df90e39a423483c82acc50719c7c1e45ee4ec92afa` | its output |

Not checked by me:
- the rebuild of `bin/fastbb2` from `fastbb2.cpp`;
- a cake_lpr re-run of the 8 test rows (VB did one);
- the live re-walk timings and throughput numbers of V11_NOTES §3.2 (COMPUTED/HEURISTIC there);
- the switch itself;
- any run of v6 by me (I started no unit).
