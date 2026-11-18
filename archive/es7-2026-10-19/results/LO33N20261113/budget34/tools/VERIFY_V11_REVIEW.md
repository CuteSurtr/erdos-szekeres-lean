**Verdict: CONFIRMED** (claim `s1r-v11-review`, filed by S1R; verifier VS, 15 November 2026, 20:36-20:42 KST). Parts
(B) and (C) are confirmed at the label COMPUTED by VS's own read-only code (`vs_s1r.py`), and parts (A) and (D) by VS's
own reading of the code. Two notes:
(1) Since the claim was filed, the live loop was switched to v11 (unit `esr-lo-b35s20v11a`, active 20:36:29). That run
created `bb/TOO_BIG.txt` (mtime 20:36:29) and rewrote `master.json`, `contexts.json` and the claim files. So (C)'s "no
TOO_BIG.txt" was true at the claim's time (20:34) but no longer is. The count of 54 changed entries and the claim-file
pid can only be checked for consistency, not re-derived.
(2) The fastbb2 statements rest on the record's source `FASTBB20261113/tools/fastbb2.cpp`. `bin/fastbb2` was not
rebuilt from it.

# VERIFY_V11_REVIEW: second check of S1R's review of the v11 skip list

Tool hashes as claimed: `run_tree_v6.py` `d6608ce9…`, `continue34_v11.py` `81d2c9e2…`, `init_too_big_v1.py`
`2964a093…`.

## (A) Code reading (VS)

- run_tree_v6 changes only the `--ctx` argument of fastbb2. For the extra worker it also changes the thread count
  (`cmd[4]`) and `--max-ctx-nodes`; `xcmd` is `cmd` otherwise.
- run_tree_v6 writes the log(s), the receipt and the TOO_BIG append. It opens ctx files only read-only, to release them
  from the cache (`os.open(q, O_RDONLY)`, fdatasync, fadvise); that loop is unchanged from v5. It never writes or deletes
  a ctx file.
- continue34_v11 notes `COMPUTED_CLOSED` only if the receipt has no witness and `r['exit'] == 0`, where `exit` is the
  frontier child's exit code.
- fastbb2 `runSolve` returns 2 or 3 on errors and witnesses. At the end it returns 3 (witness), 4 (too big), or
  `all ? 0 : 5`, where `all = closedFiles == m.ctxs.size() && !haveWitness`. Here closedFiles counts the ctx files of
  **all** master contexts, not of the selection. So an open skipped context forces exit ≠ 0, and it can never yield
  COMPUTED_CLOSED.
- The witness, exact-row, cut34_v4, probe35_v2 and append_cuts_v2 paths are unchanged (both diffs read).

## (B) COMPUTED, own code

| item | VS |
|---|---|
| regenerated diffs vs V11_NOTES §1 code blocks and the saved diffs | equal (both pairs) |
| first 3,270 lines of `bb-v11test/TOO_BIG.txt` | SHA-256 `08a7a1f8…` = c600s1 `skip_file_sha256_before`; VS's own rebuild from the 45 live receipted logs is byte-identical (VERIFY_V11.md) |
| first 3,271 lines (adds `96 300001 c600s1.x`) | `4aeedccf…` = c601s1 `skip_file_sha256_before` |
| c600s1 lists, recomputed from contexts.json, the ctx files present at its start (19:11:30) and the 3,270-line record | frontier **6,992** and extra **75** both equal the receipt's command lists in content and order |
| c601s1 lists (start 19:59:13, 3,271-line record) | frontier **6,967** and extra **68** equal; the receipt says open 7,036, selected 6,967, skipped 69 (= 68 + context 96 at 300,001) |
| frontier events on skipped contexts / extra events outside the extra list | 0 / 0 in both slices |
| u610a | frontier, cap 20,000, 92 s: skipped 28 (recorded at 50k), selected 36; recorded 24, 28, 30, 31 (20,001-20,003); 32 abandoned, not recorded |
| u610b | skipped 32 = 28 + 4; todo starts at 32; recorded 32 and 33; 34 abandoned |
| u610c | `--too-big-only`, cap 40,000: `--ctx=24,28,30,31,32,33`; recorded 24 at 40,001; 28 abandoned |
| u610d | `--too-big-only`, cap 10,000: `--ctx=-1`, start todo 0, exit 5 after 1 s; no `WITNESS.json` in bb-v11test2 |

## (C) COMPUTED, separation (state now, 20:40, plus file times)

- **Live ctx files.** 43 ctx files in `runs/b35s20/bb` were written after 19:00 and by 20:34:59. They are exactly the
  43 closed events of live c143s2. c144s1 has no closed event at all, even now.
- **Live witness files.**
  - `witness-ctx-1095.json` (19:53:07) and `witness-ctx-1106.json` (19:56:30) are c143s2's two WITNESS events.
  - `WITNESS.json.r144w1/w2` (20:03) are the receipt witnesses (contexts 1095, 1106) of round v144. Its logs (append,
    certify, select, probe) are in `continuation-b35s20v10c/`.
- **The count of 54.** It is consistent with 43 ctx + 4 witness files + master.json, contexts.json, fastbb.log.jsonl
  + 4 claim files (c144s1 ran 4 threads). The three master/log files and the claims were rewritten at 20:36 by the v11
  switch, so the count cannot be re-derived now; see note (1).
- **Inputs changed since 19:00.** `b35s20-v144` (20:03:59, live), and the test inputs `b35s20-v600` (19:10:17), `v601`
  (19:59:13) and `v610` (19:31:43). All three `b35s20-v143` files are from 17:45:04.
- **cuts-v1\* changed since 19:00.** Only `cuts-v144w1u` (20:03:31) and `cuts-v144w2u` (20:03:58).
- **Test commands.** Every test fastbb2 command (c600s1, c601s1 and their extra workers; u610a-d) has packet argument
  `bb-v11test` or `bb-v11test2`.

## (D) Correction and notes (VS's reading plus the receipts)

- **The correction is right.**
  - The extra worker is started only inside the frontier's `while child.poll() is None` loop, after the frontier's
    `start` event, and it is halted after the frontier exits.
  - With `--ctx=-1` the frontier exits at once (u610d: 1 s, exit 5). The extra worker then gets at most about 1 s,
    the receipt has no witness and exit ≠ 0, and continue34 notes `OPEN`.
  - Stops by `--stop-witnesses`, the time limit or an early frontier exit also halt the extra worker mid-context. So
    "cannot get stuck" holds only for slices long enough for one extra attempt.
- **`skipped_known_too_big` in `--too-big-only` mode.** It is `len(opn) − len(lst)`, so it counts unrecorded contexts
  too. In u610c: 58 = 28 recorded above the cap + 30 never recorded (34 recorded contexts before u610c, 64 open).
- **Witness glob.** `audit_followup_rows_v4.py` line 33 globs `runs/*/bb*/WITNESS.json*`, and this matches
  `bb-v11test/WITNESS.json.r601w1`. That file is byte-identical to live `bb/WITNESS.json.r144w1` (SHA-256
  `124cf196…`). The audit keeps only files whose SHA-256 equals the candidate's, then takes the first by name
  (`…r144w1` sorts first) and uses the same bytes, so its result cannot change.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/vs/s1r-v11-review/`)

| file | SHA-256 |
|---|---|
| `vs_s1r.py` | `5a4b74f724e3a029f2dd3d959425ca38b18201daa9a963b1651a699cdcceb058` |
| `vs_s1r.json` (all values above) | `4bdd480c640a6d3e024c068cc93bab2ba477fe2e0932697018b941796b637b07` |

Everything was read-only and run in the foreground (under 2 s). No unit was started and no git action was taken.
