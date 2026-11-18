# VERIFY_V12_REVIEW: verdict on claim r-v12-review-1118 (verifier VS, 18 November 2026, 03:00-03:05 KST)

**Verdict: CONFIRMED.** Every part of R's review that VS re-checked agrees with the code and the data:
- the code reading (A);
- the tests (B), re-run with the trusted replay function itself;
- the live selection check (C), redone with VS's own read-only code at 03:01:57.

VS found no soundness or concurrency problem beyond R's notes N1-N9, which are operational. As the claim says, no
bound or tree follows. VS launched nothing against the live packet and wrote nothing into W.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/r-v12/`; W = `/home/jay/research/data/es308-20261114`)

1. **Hashes of the reviewed tools.** `highcap_v1.py` is 1642fb3b…, `run_tree_v7.py` 7bde01a9… and `continue34_v12.py`
   ab93d16f…. Their predecessors are `run_tree_v6.py` d6608ce9… and `continue34_v11.py` 81d2c9e2….
2. **Diffs.**
   - `diff -u run_tree_v6.py run_tree_v7.py`: the docstring, the `--inbox` option, and one block placed after the
     witness checks and before `result['witnesses']` and the too-big recording. That block:
     - reads the run's rows (catalog plus the run's `extra.json`) and the inbox files `w-*.json` in name order;
     - stops at `--stop-witnesses`;
     - skips a witness whose context has a ctx file, and duplicate hole sets;
     - asserts 35 distinct holes with state 0 occupied;
     - skips a witness that some row cuts;
     - writes nothing into the inbox.

     An exception there happens before the too-big lines are appended, which is note N8.
   - `diff -u continue34_v11.py continue34_v12.py`: the docstring, `--inbox`, the finder `run_tree_v7.py`, and
     `--inbox` passed through. Nothing else changes.
3. **Every write in `highcap_v1.py`** (read in full). Writes into the target are only these:
   - line 88: the temporary `.import-ctx-<c>.<pid>.tmp`, with fdatasync and a sha256 compare;
   - line 92: `os.link`, which raises FileExistsError rather than replace;
   - lines 91/93/94: `unlink` of the temporary file.

   The import refuses when any of these fails:
   - the target lacks a file for c;
   - the side and target `master.txt` have equal sha256;
   - the gz header equals the target's `contexts.json` entry;
   - the solved-with rows body is a line prefix of the target version's body.

   All other writes go to `<side>` (fastbb2 outdir, `TOO_BIG.txt`, the WITNESS rename), `<side>-logs` (logs,
   `status.json`, `solved_with.json`, `imports.jsonl`) or the inbox (tmp + link).

   N7 is real: `--side=bb/` passes `a.side!=a.target` and `SIDE.parent==RUN`, and then SIDE equals TGT.
4. **Selection rules from the code.**
   - `run_tree_v6.py` lines 62-64: open = contexts without a ctx file; frontier = record ≤ `--max-ctx-nodes` (a missing
     record counts as 0); extra = `--max-ctx-nodes` < record ≤ `--extra-cap`.
   - `highcap_v1.selected`: record > `--above`, read from complete lines only.
   - Records are maxima over append-only lines. The loop appends them (lines 161-163) only after both of its workers
     have halted at the end of a slice.
   - So with `--above` = `--extra-cap`, the loop never again selects a context once the side pass can select it, and
     the three bands partition the open contexts.
5. **Live check, VS's own code** (`V/vs_selcheck.py`, read-only, 03:01:57, `V/selcheck_0301.out`).
   - Of 8,065 contexts, 2,028 have ctx files and **6,037 are open = 5,962 frontier + 70 extra + 5 side** (96, 100, 132,
     152, 220). **There is no gap**; 266 contexts have records, the largest 300,002.
   - The two running fastbb2 processes, read from `/proc/<pid>/cmdline`, both have outdir `bb`:
     - frontier: `--max-ctx-nodes=150000`, 6,001 contexts listed;
     - extra: `--max-ctx-nodes=300000`, 70 contexts listed.

     **Neither lists a side context.** The side set equals R's at 02:50.
6. **Trusted replay of the test files.** `V/vs_replay_one.py` imports `audit/fresh_replay_v3.py` with the packet and
   version as arguments and calls its own `one(c)`: descriptor, envelope, `check_tree` with pending = path length, and
   an unchanged-file assert. It creates and writes nothing. Results (`V/replay_tests.out`):

   | packet | rows | context | result |
   |---|---|---|---|
   | `bb-r1118t` | b35s20-v148 | 1516 | PASS, margin 1, 2,035 nodes, sha 4d063e22… |
   | `bb-r1118t` | b35s20-v148 | 1526 | PASS, margin 1, 2,021 nodes, sha 7cf0aee7… |
   | `bb-r1118u` (T2a, tree broken on purpose) | b35s20-v148 | 1526 | **REJECTED**: `Nonpositive leaf margin at node 24` |
   | `bb-r1118u` | b35s20-v148 | 1516 | PASS (control) |
   | `bb-r1118w` (T3, master names v150) | b35s20-v150 | 1399 (solved with v148, imported) | PASS, margin 1, 2,093 nodes |

   - The SHA-256 values of `bb-r1118t/ctx-1516` and `ctx-1526` **equal the live `bb` files** (4d063e22…, 7cf0aee7…), so
     fastbb2 output is byte-identical for the same master and rows.
   - `bb-r1118w/ctx-1399` equals `bb-r1118t/ctx-1399` (cbef7613…), as `imports.jsonl` records.
   - The memory peak was about 47 MiB.
7. **Negative imports.** R's `t2_neg.out` shows:
   - T2a imported;
   - T2b refused (rows not a prefix);
   - T2c refused (header);
   - T2d AssertionError (side master);
   - T2e "target already has the context".

   `bb-r1118u` holds only `ctx-1516` and `ctx-1526` and no hidden temporary file (`ls -la`). The refusals match
   `import_ctx` lines 82-93.
8. **Inbox witnesses (T5).** VS's own exact check (`V/inbox_check.out`) is against the catalog plus the extra rows of
   v148 (4,226 rows) and v150 (4,258 rows):
   - `w-1-valid-c1252` passes;
   - `w-2-cut-c1252` fails a row;
   - `w-3-closedctx-c1526` belongs to a context closed in `bb-r1118t`;
   - `w-4-dup-c1252` repeats a hole set.

   This matches receipt `runs/b35s20/r1118t5.json`: `taken: [w-1-valid-c1252.json]`, `cut_by_rows: 1`. `w-1` also
   satisfies all v150 rows, which agrees with the review's O2.

## Not checked

- T1 itself: highcap_v1 was not re-run. Its products were checked through the hashes and the replays.
- T1c (`tcheck_b35`), T5b (code reading only), the wrapper test, and fastbb2's internals.
- The memory figures of §5, which are claim `r-replay-mem-1118`.
- AS's throughput numbers.

## Files

`V/vs_selcheck.py` (93cd6600…cf21), `V/vs_replay_one.py` (dbac5671…66c1), `V/replay_tests.out` (6a453eb5…3bfa),
`V/inbox_check.out` (f339a750…b800), `V/selcheck_0301.out` (3e4499e6…7b14).
