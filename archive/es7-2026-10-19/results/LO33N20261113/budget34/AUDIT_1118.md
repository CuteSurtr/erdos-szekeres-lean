# AUDIT_1118: independent audit of the (20,15) row batches appended on 18 November 2026 (track AU)

**Status: running. The driver audits each new batch as it appears; the live table below is rewritten by the driver
after every audit, append check and hourly sample. A FAIL would appear as a banner above this headline and as claim
`agu-fail-<batch>-1118`.** Per row the label is CERTIFIED only when all three audit checks pass (own encoder, fresh
cake_lpr line, witness cut). Loop progress rates are HEURISTIC.

Milestones (written by hand; the live table below is authoritative):
- 03:40: rounds 149-153 audited, 12 batches and 96 rows, all CERTIFIED. Two witnesses had no batch because the
  round's other rows had already cut them. The 5 append checks all exited 0. Running total: 71 batches, 650 rows.
  - Closed contexts: 2,229 at 03:35, +485 in the hour before; 1,652 at the loop start at 02:24:39.
  - HEURISTIC: at that rate, the 5,766 open contexts not recorded above 150k would take about 12 h. That is about
    15:30, before the loop's 18:00 deadline, if the rate held; it need not.

- 04:30: the v11c loop was stopped from outside at 04:29:00, at a safe point: the events show finder c155s1 exit
  -15, then `FINISHED` with `stopped: true`. It was replaced at 04:29:21 by `esr-lo-b35s20v12a`:
  - `continue34_v12.py --start-version=155 --threads=9 --extra-threads=3 --inbox=runs/b35s20/bb-hc1-inbox`, output
    `continuation-b35s20v12a`, deadline 18:00;
  - beside it runs the high-cap side pass `esr-lo-highcap-1` (`highcap_v1.py`, side packet `bb-hc1`; it imports
    closed contexts into `bb` and sends its witnesses to the inbox);
  - v12 differs from v11 only in its finder and the inbox (diff read). Batch names, cuts folders, events and the append
    path are unchanged, so the same audit applies.
  - All v11c batches v149-v155 were audited before the swap: 20 batches and 160 rows, all CERTIFIED. 5 witnesses had
    no batch (already cut by their round's rows). The 7 append checks all exited 0. Running total: 79 batches, 714 rows.
  - Closed contexts: 2,559 at 04:29 (368 per hour over 03:35-04:29). The 4 open contexts recorded above 300k at 03:35
    were 0 at 04:32.

Claims: `agu-1118-v149` (round 149) was filed at 02:39:53; its `time` field says 02:41 because it was written
ahead. A final claim covering v150 and later is filed at the end.

## Statement

Every row batch `cuts-v<k>w<i>u` that the live (20,15) loop certifies today is re-checked independently of the loop:
- loop: unit `esr-lo-b35s20v11c`, `tools/continue34_v11.py --start-version=148`, output
  `W/continuation-b35s20v11c` (W = `/home/jay/research/data/es308-20261114`), deadline 18 Nov 18:00;
- audited: each row (support over the 154 residual states, rhs 1) is CERTIFIED by its own CaDiCaL LRAT proof and a
  fresh cake_lpr run, its CNF is the audit's own byte-for-byte re-encoding, and it cuts the witness of its batch.
- Scope: these are additional rows only. No finite exclusion and no ES(8) bound follows from them; (20,15) is not
  closed, so ES(8) ≤ 307 is not reached.

## Model and soundness of the check

- `audit/audit_followup_rows_v4.py` (the house audit, SHA-256 `f0df1c0f…`) re-encodes each row with its own encoder
  `audit/residual_encoder.py` (`db7b2deb…`; no finder or original encoder imported). The SHA-256 of the
  re-encoding must equal the hash of the loop's CNF.
- It runs a fresh `cake_lpr` on the stored CNF and LRAT and requires the exact line `s VERIFIED UNSAT`; the hashes of
  the CNF and the LRAT must not change during the run.
- It re-checks the batch's witness (the WITNESS file is matched by SHA-256) against all input rows: 35 holes,
  F20/Lo15, state 0 occupied. It also records whether each row cuts the witness. A rhs-1 row is violated by a hole
  set H exactly when its support misses H.
- The driver then re-reads the audit's outputs with its own code (`validate`):
  - label CERTIFIED;
  - rows = own-encoder matches = fresh acceptances = rows cutting the witness = |accepted.json| = replay lines;
  - the replay rows equal the accepted rows, in order;
  - every fresh stdout file contains the literal line;
  - every row misses all holes of the witness written in the loop's batch event.
- After each append, U2's read-only `check_appends.py` (`61c5c5d9…`) checks two things:
  - `inputs/b35s20-v<k>/extra.json` = `v<k-1>` + exactly the audited rows of that round (old rows unchanged);
  - a witness with no batch of its own (`witness_already_cut`) is cut by a new row.

## Method

- Invocation is as on 15 Nov (main session 09:04 and 22:40; U2's `run_audit.sh`): one process per batch, because the
  script sets a 300 MiB soft address-space limit.
  - Each batch runs in its own unit `esr-agu-<batch>`: CPUQuota 45 %, MemoryMax 1G, MemorySwapMax 0, RuntimeMaxSec
    ≤ 600, nice 10, single-thread BLAS variables.
  - Command: `python -B audit/audit_followup_rows_v4.py <batch>`; log `au1118/audit-<batch>.out`, exit code
    `au1118/audit-<batch>.rc`.
- Driver `au1118/au_driver.py` in unit `esr-agu-driver` (CPUQuota 5 %, MemoryMax 300M), with
  au1118 = `/home/jay/research/data/roadmap-20261115/pm1115/au1118`.
  - Versions:
    - `d3902699…`, 02:34:43-02:35:18: one progress sample only.
    - `7487ef27…`, 02:35:18-02:41: audited v149w1u and v149w2u and ran the v149 append check.
    - `6c8abcf7…`, 02:41:07-04:29:37: audited v150-v155. Its main loop survives exceptions, which are logged to
      `errors.jsonl` and shown at the top of this file, and it uses a per-process temp file for rendering. It exited
      as designed when the v11c loop finished.
    - `50c9517a…`, unit `esr-agu-driver2`, from 04:32:10: the current file. It follows several continuation folders,
      `--out continuation-b35s20v11c continuation-b35s20v12a`. It also follows any `continuation-b35s20*` folder
      modified since `--since` (04:29:00); in such a discovered folder only live-namespace batches count (v1xx, cuts
      folder in W). It keys append checks per folder, samples all `esr-lo-*` units and the bb-hc1 side record, and
      runs to the deadline.
    - The `audit` and `validate` functions are byte-identical in all four versions. The superseded files were not
      kept; only their hashes are recorded here.
  - It polls `events.json` every 20 s and audits each `batch` event that has a `cuts` folder as soon as it appears,
    which is before the round's append.
  - It runs one audit at a time and launches none after 08:11.
  - Track total: CPUQuota 50 %, MemoryMax 1.3 G (budget 1.4 G; guard track `agu` = 1,500 MB).
- **Where the audit writes, and collisions.**
  - It writes `budget34/audit/cuts-<batch>/{replay.jsonl,summary.json}` (record) and `W/audit/cuts-<batch>/` (fresh
    cake_lpr stdout/stderr and a frozen witness copy).
  - It refuses an existing `replay.jsonl`.
  - Before each run the driver requires that neither folder exists. Checked at 02:31: no `cuts-v149*` folder anywhere.
    The test namespaces v5xx, v6xx and v7xx (`cuts-v501…`, `cuts-v601w1u`, `cuts-v701w1u`) cannot collide with live
    versions 149 and up.
  - An existing folder is treated as audited elsewhere: it is re-validated and never re-run. If it still does not
    validate after 15 min, it is reported as COLLISION.
- Never touched: the loop, its folders and its files. W is only read, apart from the audit's own `W/audit/cuts-<batch>/`.
- Progress is sampled read-only at the start, then hourly and at the end:
  - closed = number of `runs/b35s20/bb/ctx-<c>.json.gz` files;
  - total = length of `contexts.json`;
  - open > 150k (> 300k) = contexts without a ctx file whose largest `nodes_so_far` in `TOO_BIG.txt` exceeds 150,000
    (300,000);
  - closes per hour = the difference between consecutive samples (HEURISTIC).
- Baseline before the loop: 1,652 closed at the 16 Nov stop; the loop restarted at 02:24:39. Running totals before
  today: **59 batches and 554 CERTIFIED rows up to v148**, recounted at 02:30 from the 59 audit summaries v101-v148
  (all CERTIFIED, rows = own encoder = fresh acceptances).

## Live audit table (auto-generated by `au_driver.py`, 2026-11-18 10:15:24 KST)

| batch | round | witness ctx | rows | own encoder | fresh cake_lpr | cut witness | verdict | audit finished | unit |
|---|---|---|---|---|---|---|---|---|---|
| v149w1u | 149 | 1765 | 8 | 8 | 8 | 8 | **CERTIFIED** | 02:38:46 | esr-agu-v149w1u |
| v149w2u | 149 | 1829 | 8 | 8 | 8 | 8 | **CERTIFIED** | 02:39:17 | esr-agu-v149w2u |
| v150w1u | 150 | 1867 | 8 | 8 | 8 | 8 | **CERTIFIED** | 02:52:32 | esr-agu-v150w1u |
| v150w2u | 150 | 2060 | 8 | 8 | 8 | 8 | **CERTIFIED** | 02:53:02 | esr-agu-v150w2u |
| v151w1u | 151 | 2104 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:11:50 | esr-agu-v151w1u |
| v151w2u | 151 | 2107 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:12:18 | esr-agu-v151w2u |
| v151w3 | 151 | 2112 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v151w4u | 151 | 2149 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:12:48 | esr-agu-v151w4u |
| v152w1u | 152 | 2168 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:25:14 | esr-agu-v152w1u |
| v152w2 | 152 | 2166 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v152w3u | 152 | 2178 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:25:42 | esr-agu-v152w3u |
| v152w4u | 152 | 2185 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:26:09 | esr-agu-v152w4u |
| v153w1u | 153 | 2178 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:37:38 | esr-agu-v153w1u |
| v153w2u | 153 | 2288 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:38:09 | esr-agu-v153w2u |
| v154w1u | 154 | 2322 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:51:58 | esr-agu-v154w1u |
| v154w2u | 154 | 2327 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:52:23 | esr-agu-v154w2u |
| v154w3u | 154 | 2350 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:52:48 | esr-agu-v154w3u |
| v154w4 | 154 | 2349 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v154w5u | 154 | 2358 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:53:14 | esr-agu-v154w5u |
| v154w6u | 154 | 2374 | 8 | 8 | 8 | 8 | **CERTIFIED** | 03:53:40 | esr-agu-v154w6u |
| v154w7 | 154 | 2375 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v155w1u | 155 | 2565 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:20:47 | esr-agu-v155w1u |
| v155w2u | 155 | 2576 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:21:13 | esr-agu-v155w2u |
| v155w3u | 155 | 2598 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:21:39 | esr-agu-v155w3u |
| v155w4 | 155 | 2601 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v156w1u | 156 | 2616 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:40:35 | esr-agu-v156w1u |
| v156w2u | 156 | 2630 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:41:00 | esr-agu-v156w2u |
| v156w3 | 156 | 2617 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v156w4 | 156 | 2640 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v156w5 | 156 | 2633 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v156w6 | 156 | 2657 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v156w7u | 156 | 2681 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:41:27 | esr-agu-v156w7u |
| v157w1u | 157 | 2706 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:54:14 | esr-agu-v157w1u |
| v157w2u | 157 | 2761 | 8 | 8 | 8 | 8 | **CERTIFIED** | 04:54:40 | esr-agu-v157w2u |
| v158w1u | 158 | 2916 | 8 | 8 | 8 | 8 | **CERTIFIED** | 05:07:46 | esr-agu-v158w1u |
| v158w2u | 158 | 3108 | 8 | 8 | 8 | 8 | **CERTIFIED** | 05:08:12 | esr-agu-v158w2u |
| v159w1u | 159 | 4144 | 8 | 8 | 8 | 8 | **CERTIFIED** | 05:37:59 | esr-agu-v159w1u |
| v159w2u | 159 | 4176 | 8 | 8 | 8 | 8 | **CERTIFIED** | 05:38:26 | esr-agu-v159w2u |
| v159w3u | 159 | 4211 | 8 | 8 | 8 | 8 | **CERTIFIED** | 05:38:53 | esr-agu-v159w3u |
| v159w4 | 159 | 4215 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v160w1u | 160 | 4221 | 8 | 8 | 8 | 8 | **CERTIFIED** | 05:52:00 | esr-agu-v160w1u |
| v160w2 | 160 | 1797 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v161w1u | 161 | 4514 | 8 | 8 | 8 | 8 | **CERTIFIED** | 06:18:07 | esr-agu-v161w1u |
| v161w2u | 161 | 4615 | 8 | 8 | 8 | 8 | **CERTIFIED** | 06:18:32 | esr-agu-v161w2u |
| v162w1u | 162 | 4680 | 8 | 8 | 8 | 8 | **CERTIFIED** | 06:37:38 | esr-agu-v162w1u |
| v162w2u | 162 | 4112 | 8 | 8 | 8 | 8 | **CERTIFIED** | 06:38:05 | esr-agu-v162w2u |
| v163w1u | 163 | 4787 | 8 | 8 | 8 | 8 | **CERTIFIED** | 06:59:52 | esr-agu-v163w1u |
| v163w2u | 163 | 4820 | 8 | 8 | 8 | 8 | **CERTIFIED** | 07:00:19 | esr-agu-v163w2u |
| v164w1u | 164 | 4952 | 8 | 8 | 8 | 8 | **CERTIFIED** | 07:11:27 | esr-agu-v164w1u |
| v164w2 | 164 | 4946 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v165w1u | 165 | 5234 | 8 | 8 | 8 | 8 | **CERTIFIED** | 07:29:15 | esr-agu-v165w1u |
| v165w2u | 165 | 5299 | 8 | 8 | 8 | 8 | **CERTIFIED** | 07:29:41 | esr-agu-v165w2u |
| v165w3 | 165 | 5298 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v165w4 | 165 | 5302 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v165w5u | 165 | 5321 | 8 | 8 | 8 | 8 | **CERTIFIED** | 07:30:07 | esr-agu-v165w5u |
| v166w1u | 166 | 5763 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:01:14 | esr-agu-v166w1u |
| v166w2 | 166 | 4702 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v167w1u | 167 | 6193 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:33:20 | esr-agu-v167w1u |
| v167w2 | 167 | 6191 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v167w3u | 167 | 6202 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:33:28 | esr-agu-v167w3u |
| v167w4u | 167 | 6194 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:33:35 | esr-agu-v167w4u |
| v167w5 | 167 | 6209 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v167w6u | 167 | 6230 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:33:43 | esr-agu-v167w6u |
| v167w7u | 167 | 6208 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:33:49 | esr-agu-v167w7u |
| v167w8u | 167 | 6260 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:33:57 | esr-agu-v167w8u |
| v167w9u | 167 | 6264 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:34:04 | esr-agu-v167w9u |
| v167w10 | 167 | 6265 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v167w11 | 167 | 6261 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v167w12 | 167 | 6267 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v168w1u | 168 | 6193 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:36:51 | esr-agu-v168w1u |
| v168w2u | 168 | 6291 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:37:17 | esr-agu-v168w2u |
| v169w1u | 169 | 7122 | 8 | 8 | 8 | 8 | **CERTIFIED** | 08:56:23 | esr-agu-v169w1u |
| v169w2 | 169 | 7140 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |
| v169w3 | 169 | 7143 |  |  |  |  | **no batch** (witness already cut by earlier rows of the round) |  |  |

**Running totals for (20,15): 111 batches and 970 CERTIFIED rows** (59 / 554 up to v148, plus 52 / 416 from v149 on).

Append cross-checks (U2 `check_appends.py`, read-only):

- 2026-11-18T02:39:17+09:00 (continuation-b35s20v11c, append 1 = v149): exit 0: `{"appended_rows_checked": 16, "batches_checked": 2, "failures": []}`
- 2026-11-18T02:53:03+09:00 (continuation-b35s20v11c, append 2 = v150): exit 0: `{"appended_rows_checked": 32, "batches_checked": 4, "failures": []}`
- 2026-11-18T03:12:49+09:00 (continuation-b35s20v11c, append 3 = v151): exit 0: `{"appended_rows_checked": 56, "batches_checked": 7, "failures": []}`
- 2026-11-18T03:26:10+09:00 (continuation-b35s20v11c, append 4 = v152): exit 0: `{"appended_rows_checked": 80, "batches_checked": 10, "failures": []}`
- 2026-11-18T03:38:10+09:00 (continuation-b35s20v11c, append 5 = v153): exit 0: `{"appended_rows_checked": 96, "batches_checked": 12, "failures": []}`
- 2026-11-18T03:53:41+09:00 (continuation-b35s20v11c, append 6 = v154): exit 0: `{"appended_rows_checked": 136, "batches_checked": 17, "failures": []}`
- 2026-11-18T04:21:39+09:00 (continuation-b35s20v11c, append 7 = v155): exit 0: `{"appended_rows_checked": 160, "batches_checked": 20, "failures": []}`
- 2026-11-18T04:41:27+09:00 (continuation-b35s20v12a, append 1 = v156): exit 0: `{"appended_rows_checked": 24, "batches_checked": 3, "failures": []}`
- 2026-11-18T04:54:41+09:00 (continuation-b35s20v12a, append 2 = v157): exit 0: `{"appended_rows_checked": 40, "batches_checked": 5, "failures": []}`
- 2026-11-18T05:08:13+09:00 (continuation-b35s20v12a, append 3 = v158): exit 0: `{"appended_rows_checked": 56, "batches_checked": 7, "failures": []}`
- 2026-11-18T05:38:53+09:00 (continuation-b35s20v12a, append 4 = v159): exit 0: `{"appended_rows_checked": 80, "batches_checked": 10, "failures": []}`
- 2026-11-18T05:52:01+09:00 (continuation-b35s20v12a, append 5 = v160): exit 0: `{"appended_rows_checked": 88, "batches_checked": 11, "failures": []}`
- 2026-11-18T06:18:33+09:00 (continuation-b35s20v12a, append 6 = v161): exit 0: `{"appended_rows_checked": 104, "batches_checked": 13, "failures": []}`
- 2026-11-18T06:38:06+09:00 (continuation-b35s20v12a, append 7 = v162): exit 0: `{"appended_rows_checked": 120, "batches_checked": 15, "failures": []}`
- 2026-11-18T07:00:20+09:00 (continuation-b35s20v12a, append 8 = v163): exit 0: `{"appended_rows_checked": 136, "batches_checked": 17, "failures": []}`
- 2026-11-18T07:11:28+09:00 (continuation-b35s20v12a, append 9 = v164): exit 0: `{"appended_rows_checked": 144, "batches_checked": 18, "failures": []}`
- 2026-11-18T07:30:08+09:00 (continuation-b35s20v12a, append 10 = v165): exit 0: `{"appended_rows_checked": 168, "batches_checked": 21, "failures": []}`
- 2026-11-18T08:01:15+09:00 (continuation-b35s20v12a, append 11 = v166): exit 0: `{"appended_rows_checked": 176, "batches_checked": 22, "failures": []}`
- 2026-11-18T08:34:05+09:00 (continuation-b35s20v12b, append 1 = v167): exit 0: `{"appended_rows_checked": 56, "batches_checked": 7, "failures": []}`
- 2026-11-18T08:37:18+09:00 (continuation-b35s20v12b, append 2 = v168): exit 0: `{"appended_rows_checked": 72, "batches_checked": 9, "failures": []}`
- 2026-11-18T08:56:24+09:00 (continuation-b35s20v12b, append 3 = v169): exit 0: `{"appended_rows_checked": 80, "batches_checked": 10, "failures": []}`

## Loop progress, read-only samples (rates HEURISTIC)

| time | closed / total | open | open > 150k | open > 300k | TOO_BIG lines | open in bb-hc1 TOO_BIG (max nodes) | closes per hour since previous sample | esr-lo units | last event |
|---|---|---|---|---|---|---|---|---|---|
| 02:34:44 | 1738 / 8065 | 6327 | 70 | 4 | 3419 |  |  | active |    |
| 02:35:19 | 1744 / 8065 | 6321 | 70 | 4 | 3419 |  | 617 | active |    |
| 03:35:30 | 2229 / 8065 | 5836 | 70 | 4 | 3434 |  | 484 | active | CERTIFIED_ROWS_APPENDED  03:25:47 |
| 04:29:20 | 2559 / 8065 | 5506 | 62 | 0 | 3442 |  | 368 | inactive | FINISHED  04:29:00 |
| 05:29:33 | 4107 / 8065 | 3958 | 38 | 0 | 3452 | 0 (0) | 1542 | esr-lo-b35s20v12a esr-lo-highcap-1 | CERTIFIED_ROWS_APPENDED  05:07:57 |
| 06:29:53 | 4634 / 8065 | 3431 | 32 | 1 | 3492 | 0 (0) | 524 | esr-lo-b35s20v12a esr-lo-highcap-1 | CERTIFIED_ROWS_APPENDED  06:18:19 |
| 07:30:08 | 5287 / 8065 | 2778 | 42 | 1 | 3542 | 0 (0) | 650 | esr-lo-b35s20v12a esr-lo-highcap-1 | CERTIFIED_ROWS_APPENDED  07:29:54 |
| 08:15:15 | 6180 / 8065 | 1885 | 30 | 1 | 3554 | 0 (0) | 1188 | esr-lo-b35s20v12a esr-lo-highcap-1 | CERTIFIED_ROWS_APPENDED  08:01:06 |
| 09:15:24 | 8052 / 8065 | 13 | 13 | 1 | 3584 | 1 (1000002) | 1867 | esr-lo-hcpass169b | FINISHED  08:56:31 |
| 10:15:24 | 8064 / 8065 | 1 | 1 | 1 | 3585 | 1 (1000002) | 12 |  | FINISHED  08:56:31 |

## Controls

- `au_driver.py --selftest`, 02:33, PASS.
  - Positive controls: the four v11a batches v145w1u-v148w1u, audited by the main session on 15 Nov, validate.
  - Negative controls: the same check rejects batch v148w1u when the witness meets its rows, and rejects a missing
    batch.
- The house audit keeps its own controls (encoder identity, literal cake line, exact witness row check); they are
  unchanged.

## Files and hashes

| file | SHA-256 |
|---|---|
| `budget34/audit/audit_followup_rows_v4.py` | `f0df1c0f5b38b735226a9b813b3f5f78d0b91ee27c300c15ffccf5c5fa1ffc12` |
| `budget34/audit/residual_encoder.py` | `db7b2deba4ae55ff50f25d1e52843734591f5e7d1339a53e45e8811866e7365c` |
| `budget34/audit/pool_audit.py` | `62dfea696b8cd2c1261047661cba5f828ee2e5a2306df3524ba7741b339b7993` |
| `pm1115/u2/check_appends.py` | `61c5c5d9de1c8b6c67691701be19726811316a709aafeea978582f02f91c56fd` |
| `pm1115/au1118/au_driver.py` | see `au1118/SHA256SUMS` |

Work folder `au1118` = `/home/jay/research/data/roadmap-20261115/pm1115/au1118/`:
- `audits.jsonl`: one line per batch;
- `checks.jsonl` and `check-latest.jsonl`: append cross-checks;
- `progress.jsonl`: samples;
- `audit-<batch>.out` and `.rc`: per-batch log and exit code;
- `driver.log`: the driver's stdout.

## What remains

- (20,15) is not closed. The high-cap pass over the contexts recorded above 300k is still owed (`tools/V11_NOTES.md`
  §4).
- Batches certified after the driver's 08:11 launch cut-off are audited by the resume command below.

## Resume

Audit every batch not yet in `au1118/audits.jsonl`. The driver resumes from its JSONL files and never re-runs an audited
batch. Change only the deadline (it must end before the unit's RuntimeMaxSec):

```bash
AU=/home/jay/research/data/roadmap-20261115/pm1115/au1118
systemd-run --user --unit=esr-agu-driver3 -p CPUQuota=5% -p MemoryMax=300M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=<seconds until deadline + 5 min> --nice=10 --working-directory=$AU \
  -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 /bin/bash -c \
  "/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B $AU/au_driver.py \
   --deadline=<ISO time, e.g. 2026-11-18T17:55:00+09:00> \
   --out continuation-b35s20v11c continuation-b35s20v12a <any newer loop folder> \
   --since=<ISO time of the previous driver's stop> >> $AU/driver.log 2>&1"
```

- Before starting, update `au_wait.sh` (it watches `esr-agu-driver2`) if you use it.
- Keep the track total at CPUQuota 50 %: driver 5 % plus one audit unit at 45 %.
- To re-render this file only: `python -B $AU/au_driver.py --render-only`.
