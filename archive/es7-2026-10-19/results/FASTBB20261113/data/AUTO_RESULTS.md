# AUTO_RESULTS: slice runs of track G2 (generated file)

Generated 2026-11-14 03:00:32 KST by `tools/auto_results.py` from the run files in `/home/jay/research/data/fastbb-20261113/p2/runs/` (see README §8). It summarizes those files; it adds no new argument. A slice is CLOSED (EXACT TREE) only if its DONE.json says so (complete piecewise replay by `tools/verify_slice.py` with the semantic row checks); "replay 2" is the second replay by `tools/replay_split.py`.

| slice t | pair | state | nodes | leaves | min margin | pending | contexts | extra rows | witnesses killed | rows appended | replay 2 | extra SHA-256 | contexts digest |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 21 | (63, 58) | CLOSED (EXACT TREE) | 19,333,541 | 9,666,771 | 1 | 1 | 8,175 | 645 | 11 | 29 | agree | `7e7fc843d16b8e673924fd9a4fe060482d3cea3508699e7a3c7dd1ae58e90f69` | `0715763257a108096a6f9722f7fc96bbed0457141f91dfcec106681924a95a62` |
| 22 | (62, 59) | CLOSED (EXACT TREE) | 32,328,319 | 16,164,160 | 1 | 1 | 4,096 | 757 | 35 | 112 | agree | `3add175a238f20fc295bc25cffde5fe6f7005c0b1e453892c8d14a3324fada51` | `a1e1ff34e0b619a9accb8a7dd3dd4b20431b990af4a015322f0f84e269623317` |
| 20 | (64, 57) | CLOSED (EXACT TREE) | 3,044,395 | 1,522,198 | 1 | 1 | 8,001 | 757 | 0 | 0 | agree | `cf6c7c967164f16f0085eb4b885cedfb33e5bbaf1f89b97e61bc605c1a946383` | `4c70ca83cdbbdefad9ad4b26e99ff98b4b576cdcf093c8b70611f9cb433f8f53` |
| 23 | (61, 60) | CLOSED (EXACT TREE) | 18,890,255 | 9,445,128 | 1 | 1 | 4,096 | 814 | 8 | 57 | agree | `2a6d3757b2dd2176a8c79a6b627aa2277e67c41413c85e87d6c8093a2469c9bc` | `556ebcb8e931b2e3f077b118048e7aeb0464d7dcb6a2c38a8135ea930023b0fe` |

## Re-certification with kept proofs (`tools/recert_keep.py`, output `W/p2/proofs/`)

- 705 rows re-certified (2026-11-14 01:15:15): 705 cake_lpr `s VERIFIED UNSAT`, 705 regenerated CNF hashes equal to the record, 705 LRAT hashes equal to the record; not verified: []; 50 rows skipped because their proofs were already kept when certified (`W/killtools/proofs/`).

Chain log: `W/p2/runs/chain.log`. Conclusions are drawn in README §1.5 only for slices whose state above is CLOSED (EXACT TREE); for slice 22 see README §1.5 (pair (65, 59) with the verified N66 ≤ 59).
