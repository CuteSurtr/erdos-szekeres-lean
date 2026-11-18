# VERIFY_V12: claim `as-replay-mem-1116` only (memory of the trusted Python replay; verifier VB, 18 Nov 2026, 02:47-02:55 KST)

**Verdict: CONFIRMED.**
- Both measurements are reproduced with an own measuring script. The node counts equal the claim's: 50,973 and
  209,667. ctx-1601 peaks at 361.6 MiB from a 26.5 MiB baseline (claim: 361 and 26).
- ctx-188 completes its check (minimum margin 1, 14 pending = its path), but only with more memory than the claimed
  stop point. Its peak is **1,392.2 MiB** (ru_maxrss; `/usr/bin/time` 1,425,628 KiB), above the 1,384 MB at which the
  guard stopped the claim's run.
- The rate per node is 6.59-6.73 KiB above the baseline and 6.80-7.26 KiB including it (claim: "about 6.6-6.9 KiB").
- The guard stop is in the logs: `memguard-20261116.log` line 18 and the unit's journal show SIGTERM "on client
  request" at 18:29:41, with no OOM kill.
- The extrapolation to 300k / 1M / 3M nodes (about 2 / 6.7 / 20 GiB) is linear in these two points and stays
  **HEURISTIC**, as labelled.

**Scope.** This file verifies only claim `as-replay-mem-1116`. It is **not** a review of the v12 tools: that is
track R's V12_REVIEW.md, which was in progress when this was written.

## 1. Claim

- The trusted replay step of `fresh_replay_v3.py` is `one(c)`: `replay34_v2.read_json`, `descriptor`, `envelope`,
  then `omission_tree.check_tree` over the 4,226 rows of b35s20-v148.
- It needs about 6.6-6.9 KiB of resident memory per tree node of the ctx file:
  - ctx-1601 (50,973 nodes) peaked at 361 MiB;
  - ctx-188 (209,667 nodes, 29.1 MB gz, 88.2 MB JSON) went above 1,384 MiB, and the guard stopped it at 18:29:41.
- HEURISTIC extrapolation: about 2 / 6.7 / 20 GiB at 300k / 1M / 3M nodes.
- Label: COMPUTED (two measurements); the extrapolation is HEURISTIC.

## 2. Method

`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/as-replay-mem-1116/`

- `vb_mem.py` is my own script; the claim's `replay_mem.py` was read but not used. Each measurement is a fresh process:
  - `parse`: own node count, `len(json['nodes'])` of the decompressed gz JSON, and the peak RSS of decompression plus
    `json.loads` alone;
  - `full`: the steps of `one(c)` in the order above. The rows are the source catalogue plus
    `inputs/b35s20-v148/extra.json`; PATHS come from a private copy of the live `master.json` (SHA-256 `592c6c29…`);
    the budget is 35. `ru_maxrss` is read after each step.
- `run.sh` ran all four measurements in one unit, `esr-agv-vb-replmem` (95 %, MemoryMax 2700M, 26 s), each under
  `/usr/bin/time`. The ctx files are unchanged since 16 Nov 18:23, with SHA-256 `c3fe65c2…` (1601) and `55156e59…`
  (188).

## 3. Results (`W/mem.jsonl`)

| ctx | nodes | gz / JSON bytes | parse-only peak MiB | baseline MiB | after load MiB | after check MiB | `/usr/bin/time` max RSS KiB | KiB/node (above baseline / total) | check | s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1601 | 50,973 | 7,334,082 / 22,051,767 | 347.5 | 26.5 | 325.9 | **361.6** | 370,232 | 6.73 / 7.26 | min margin 1, pending 14 (path 14) | 3.4 |
| 188 | 209,667 | 29,105,144 / 88,218,326 | 1,319.5 | 42.2 | 1,239.9 | **1,392.2** | 1,425,628 | 6.59 / 6.80 | min margin 1, pending 14 (path 14) | 13.7 |

- The JSON parse alone accounts for about 90 % of the peak.
- Linear extrapolation at 6.6-6.8 KiB per node: 300k nodes ≈ 1.9-2.0 GiB, 1M ≈ 6.3-6.5 GiB, 3M ≈ 19-19.5 GiB, plus a
  baseline of about 30-45 MiB. This matches the claim's numbers. It is HEURISTIC: the real growth with tree shape and
  file layout is not measured.
- Minor wording point: the claim says the guard stopped the unit "at 95 % of its limit".
  - 95 % is the guard's threshold.
  - The value at the stop was 1,384 of 1,400 MB (98.9 %), so the guard overshot its threshold between two polls.
  - This changes nothing in the claim.

## 4. Files

| file | SHA-256 |
|---|---|
| `W/vb_mem.py` | see `W/SHA256SUMS` |
| `W/run.sh`, `W/mem.jsonl`, `W/inputs.sha256`, `W/master_snapshot.json` | see `W/SHA256SUMS` |
