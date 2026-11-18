# Addendum 15 Nov 2026 afternoon: (20,15) loop v10b and its batch audits (track U2)

**Final status, recounted at 18:41 KST: the loop finished normally at its 18:40 deadline (`FINISHED` at 18:39:42,
not stopped, unit result success; 21 h 36 min CPU in 5 h 27 min). From 13:12 it ran 5 rounds and made five appends
(v139: 32 rows in 4 batches; v140, v141: 8 rows in 1 batch each; v142, v143: 16 rows in 2 batches each). All 10
batches were independently audited: 80/80 rows CERTIFIED, the audit's own encoder agreed 80/80, the fresh cake_lpr run
accepted 80/80, and every row cuts its witness. (20,15) now has 507 CERTIFIED rows in 53 batches (427 in 43 before
today). Closed contexts: 998 of 8,065 (555 at 09:35). (20,15) is not closed, so ES(8) ≤ 307 is not reached.** Written by track U2 for the main session to merge into README.md (README.md not edited).

## Loop (not touched by U2)

- Unit `esr-lo-b35s20v10b`, started 13:12:22, 4 threads, MemoryMax 2 G, loop deadline 18:40:
  `tools/continue34_v10.py --deadline=2026-11-15T18:40:00+09:00 --start-version=138
  --start-receipt=runs/b35s20/c138s1.json --slice=20 --budget=35 --bb=bb --threads=4 --max-ctx-nodes=150000
  --slice-seconds=600 --max-witnesses=12 --accept-per-witness=8 --probe-minutes=6 --probe-procs=4
  --out=continuation-b35s20v10b`, working directory W = `/home/jay/research/data/es308-20261114`.
- Events: `W/continuation-b35s20v10b/events.json`.

## Audit method (the same as the 09:04 audit)

- This morning's unit `esr-vfy-a35v134` (journal, 09:02:48) ran `audit/audit_followup_rows_v4.py <batch>`
  (SHA-256 `f0df1c0f…`, encoder `audit/residual_encoder.py` `db7b2deb…`) once per batch, output `W/audit-<batch>.out`.
  The script re-encodes every row with its own encoder (hash must equal the CNF hash), re-runs cake_lpr on the
  stored CNF and LRAT and requires the exact line `s VERIFIED UNSAT`, re-checks the witness against the input rows
  and records whether each row cuts it. Output: `audit/cuts-<batch>/{replay.jsonl,summary.json}` (new folders) and the
  fresh cake_lpr stdout files in `W/audit/cuts-<batch>/`.
- U2 runs exactly that, one systemd unit per batch, one at a time: `esr-vfy-u2-<batch>`, CPUQuota 50 %, MemoryMax 1 G,
  MemorySwapMax 0 (launcher `/home/jay/research/data/roadmap-20261115/pm1115/u2/run_audit.sh`, `7657da38…`; the only
  additions are `python -B` and single-thread BLAS variables). Peak memory per unit about 450 MB.
- Every summary is checked: label CERTIFIED and rows = own-encoder matches = fresh cake_lpr acceptances = rows
  cutting the witness.
- Extra cross-check, U2's own read-only code `/home/jay/research/data/roadmap-20261115/pm1115/u2/check_appends.py`
  (`61c5c5d9…`): for every append event of the loop, `inputs/b35s20-v<k>/extra.json` equals `b35s20-v<k-1>` plus
  exactly the rows of that round's audited batches (old rows unchanged, rhs 1, no duplicates, none missing); every
  fresh cake_lpr stdout contains the exact line `s VERIFIED UNSAT`; every row misses all holes of its batch's witness
  (taken from the loop's batch event); every `witness_already_cut` witness misses some new row of its round.
  Negative control: a fake witness that meets rows of `v139w1u` is flagged (2 rows).

## Audited batches (15 Nov afternoon)

| batch | round | witness context | rows | own encoder | fresh cake_lpr | cut witness | audit finished |
|---|---|---|---|---|---|---|---|
| v139w1u | 139 | 570 | 8 | 8 | 8 | 8 | 13:25:09 |
| v139w2u | 139 | 586 | 8 | 8 | 8 | 8 | 13:25:19 |
| v139w3u | 139 | 600 | 8 | 8 | 8 | 8 | 13:25:23 |
| v139w4u | 139 | 614 | 8 | 8 | 8 | 8 | 13:25:29 |
| v140w1u | 140 | 710 | 8 | 8 | 8 | 8 | 14:35:33 |
| v141w1u | 141 | 812 | 8 | 8 | 8 | 8 | 15:44:14 |
| v142w1u | 142 | 1040 | 8 | 8 | 8 | 8 | 16:47:53 |
| v142w2u | 142 | 1046 | 8 | 8 | 8 | 8 | 16:48:00 |
| v143w1u | 143 | 1040 | 8 | 8 | 8 | 8 | 17:45:15 |
| v143w2u | 143 | 1063 | 8 | 8 | 8 | 8 | 17:45:21 |

Round 139 (this morning's receipt `c138s1`) had 5 witnesses; the fifth (`v139w5`, context 621) was already cut by the
round's other rows, so it has no batch (checked). Round 140 (finder `c139s1`, 13:13-14:34) and round 141 (finder
`c140s1`, 14:35-15:43) logged 1 witness each. Round 142 (finder `c141s1`, 15:44-16:46) logged 3 witnesses; the third
(`v142w3`, context 1060) was already cut by the round's other rows (checked). Round 143 (finder `c142s1`,
16:47-17:44) logged 2 witnesses. The last finder (`c143s1`, 17:45-18:39) logged no witness (receipt exit 4: time
limit reached with open contexts, many over the 150,000-node cap), so round 143 never started. Appended rows checked
against the audited rows: v139 32 = 32, v140 8 = 8, v141 8 = 8, v142 16 = 16, v143 16 = 16. The final audit pass
after the loop ended (18:39:56) found no unaudited batch, and the cross-check passed again at 18:41.

## Counts

| | before today (09:35) | final (18:41) |
|---|---|---|
| closed contexts (`runs/b35s20/bb/ctx-*.json.gz`) | 555 of 8,065 | 998 of 8,065 |
| rounds since 13:12 | | 5 round events, versions 138-142 (the first re-processes this morning's receipt `c138s1`) |
| new batches / rows appended | | 10 / 80 (appends v139-v143) |
| (20,15) CERTIFIED rows, recounted from the audit summaries | 427 in 43 batches | 507 in 53 batches |
| rows in the newest input | 4,099 (`b35s20-v138`) | 4,179 (`b35s20-v143`) |

## Files

- Audit records (new folders): `audit/cuts-<batch>/replay.jsonl` and `summary.json` for every batch in the table;
  fresh cake_lpr stdout/stderr in `W/audit/cuts-<batch>/`; audit logs `W/audit-<batch>.out`.
- U2 work folder `/home/jay/research/data/roadmap-20261115/pm1115/u2/`: `run_audit.sh` (`7657da38…`), `cycle.sh`
  (`96d390a1…`; waits for an append event, audits the new batches, runs the cross-check), `check_appends.py`
  (`61c5c5d9…`), `recount.py` (`531f8b0d…`; recount from the audit summaries), `units.log` (start/end of every
  audit unit), `audit-<batch>.rc` (exit codes), `check-latest.jsonl` (latest cross-check output).
- The loop's own files (certificates, CNFs, LRATs, inputs) are untouched; nothing was deleted.

## Resume

Rule from `continue34_v10.py`: if the last `round` event (version V, receipt R) has no later append, resume with
`--start-version=V --start-receipt=R`; if the round's rows were already appended as version V+1, resume with
`--start-version=V+1` and no `--start-receipt` (the loop then starts with a finder slice). Re-using a round that was
already appended fails safely: `append_cuts_v2.py` refuses an existing version folder (`mkdir(exist_ok=False)`).

Final: the last `round` event is version 142 with receipt `runs/b35s20/c142s1.json`, and its rows are already
appended as `b35s20-v143`. The finder that followed (`c143s1`) has no witness. So resume with
`tools/continue34_v10.py --start-version=143 --slice=20 --budget=35 --bb=bb --threads=<t> --max-ctx-nodes=150000
--slice-seconds=600 --max-witnesses=12 --accept-per-witness=8 --probe-minutes=6 --probe-procs=4
--deadline=<new> --out=<new folder>`, with no `--start-receipt`. The loop then starts with a finder slice, tag
`c143s2`. Throughput note: every finder start re-walks the open contexts from context 0. Here that took about 60 of
the roughly 65 minutes in each round, and it is why the last finder found nothing in its 54 minutes.

## Units started by U2

There were 10 audit units, `esr-vfy-u2-v139w1u` … `esr-vfy-u2-v143w2u`. They ran one at a time, each for 4-8 s, with
CPUQuota 50 %, MemoryMax 1 G and peaks of 438-454 MB including page cache (journal). All exited 0, and none is left running
(checked at 18:41). U2 did not touch the loop unit or any other unit.
