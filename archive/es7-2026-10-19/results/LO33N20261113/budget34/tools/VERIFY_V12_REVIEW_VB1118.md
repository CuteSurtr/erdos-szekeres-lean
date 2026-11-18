# VERIFY_V12_REVIEW_VB1118: claim `r-replay-mem-1118` only (verifier VB, 18 Nov 2026, 03:06-03:12 KST)

The verify file named in the claim, VERIFY_V12_REVIEW.md, already held VS's verdict on another claim, so this file
carries the suffix `_VB1118`.

**Verdict: CONFIRMED** for the three measurements, with an **own** measuring script; R's `replay_mem_r.py` was not
used.
- The node counts, the peaks and the per-node rates agree with the claim to within 0.4 MiB. All three replays pass
  (minimum margin 1, 14 pending = the path).
- The extrapolation is linear in these points and stays **HEURISTIC**, as labelled.
- **Not checked:** the sentence on fastbb2's own memory ("about 22 MiB + 0.19 KB per node", high-water mark 66.5 MiB).
  It rests on AS's receipts, which were not re-run here.

## Method

`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/r-replay-mem-1118/`

- `vb_mem.py` is the same own script as for claim `as-replay-mem-1116` (VERIFY_V12.md). Each measurement is a fresh
  process:
  - `parse`: decompression plus `json.loads` only;
  - `full`: the steps of `fresh_replay_v3.one(c)`, i.e. `replay34_v2.read_json`, `descriptor`, `envelope` and
    `check_tree(154, ROWS, 35, …)`, with rows from the catalogue plus `b35s20-v148/extra.json` and PATHS from a private
    copy of the live master (`master_snapshot.json`, SHA-256 in `W/inputs.sha256`).
- `ru_maxrss` is sampled after each step, and `/usr/bin/time` checks it independently.
- Unit `esr-agv-vb-rmem` (95 %, 1500M, 23 s).

## Results (`W/mem.jsonl`)

| ctx | nodes (own count) | gz bytes | gz SHA-256 = claim's | json.load peak MiB (claim) | baseline MiB | peak after check MiB (claim) | KiB/node above baseline (claim) | check |
|---|---|---|---|---|---|---|---|---|
| 1601 | 50,973 | 7,334,082 | `c3fe65c2…` yes | 326.4 (326.6) | 26.6 | **362.2** (362.0) | 6.74 (6.75) | min margin 1, pending 14 = path |
| 10 | 71,959 | 10,863,525 | `09c0d6e4…` yes | 470.2 (469.8) | 25.8 | **520.6** (520.5) | 7.04 (7.04) | min margin 1, pending 14 = path |
| 181 | 95,215 | 13,031,672 | `547e8e0b…` yes | 566.0 (566.8) | 27.0 | **635.4** (635.7) | 6.54 (6.56) | min margin 1, pending 14 = path |

- `/usr/bin/time` max RSS: 370,900 / 533,100 / 650,608 KiB, in line with the ru_maxrss values (`W/mem.jsonl`).
- Peak over gz size: 362.2 MiB ≈ 379.8 MB, 51.8× the 7.33 MB file; 545.9 MB, 50.3× the 10.86 MB file; 666.3 MB,
  51.1× the 13.03 MB file. This matches "about 51×".
- A parse alone (decompress + `json.loads`) peaks at 347 / 497 / 599 MiB in a separate process.
- These agree with the 16 Nov measurements of claim `as-replay-mem-1116`: ctx-188 at 1,392.2 MiB, 6.59 KiB/node.
  Over five contexts the rate is 6.5-7.0 KiB per node above the baseline.

## Files

`W/vb_mem.py`, `W/run.sh`, `W/mem.jsonl`, `W/inputs.sha256`, `W/master_snapshot.json`; SHA-256 in `W/SHA256SUMS`.
