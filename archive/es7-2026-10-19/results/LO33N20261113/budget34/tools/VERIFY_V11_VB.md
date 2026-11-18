# VERIFY_V11_VB: verdict on claim s1-v11-test-results (verifier VB, 15 November 2026, 20:17-20:20 KST)

**Verdict: CONFIRMED at the claimed label COMPUTED** (a tool test; the test rows are not audited and must not be counted
for (20,15)). Every number of parts (1)-(4) and the test-run timings of part (5) were re-derived by VB's own read-only
code from the receipts, logs and records; the 8 test rows' certificates were re-checked by fresh cake_lpr runs. Not
re-derived by VB: the live-round timings of part (5) (41.3-54.2 min; VS confirmed the c139s1-c143s1 values in
VERIFY_V11.md for claim s1-v11-skiplist, c143s2's 54.2 min is checked by nobody), the unit's memory peak (648.1 MB) and
wall times. This file is new (VERIFY_V11.md is VS's verdict on s1-v11-skiplist and is unchanged).

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/s1-v11-test/`; data in `/home/jay/research/data/es308-20261114/`)

Own script `V/vb_v11.py` (SHA-256 `190409dd…`, output `V/vb_v11.out` `cd3fede9…`):

1. **Slice c600s1** (`runs/b35s20/c600s1.json`, `.log`, `.x.log`): receipt open_at_start 7,067, selected 6,992,
   skipped_known_too_big 75 (as claimed). The frontier's `--ctx` list (6,992) and the extra worker's (75) are disjoint
   and together are the 7,067 open contexts; caps 150,000 and 300,000. Frontier events: start 1, closed 25 (contexts
   1069, 1074-1094, 1096-1098), WITNESS 1 (context 1095, 35,404 nodes; the receipt's exact row check PASS over 4,179
   rows), **0 too-big events, and no event on any of the 75 listed contexts or on any context recorded in `TOO_BIG.txt`
   before the run**. The 75 extra contexts are exactly recorded contexts with a record above 150,000 nodes before the
   run (all 75 are). Extra worker: closed 0, 33, 51, 80, 81, 97 with 201,333 / 261,085 / 167,479 / 207,593 / 177,829 /
   209,095 nodes (all in (150,000, 300,000]), and `context_too_big` 96 at 300,001 = cap + 1, recorded in `TOO_BIG.txt` as
   `96 300001 c600s1.x`.
2. **Test rows**: `inputs/b35s20-v601/rows.txt` = the 4,179 rows of v600 in the same order plus 8 appended rows (4,187);
   the 8 appended rows equal the supports of `accepted-v601m.json` (rhs 1, length 13); **each support is disjoint from
   the 35 holes** of `bb-v11test/WITNESS.json.r601w1` (context 1095). Each `cuts-v601w1u/<i>/cake.log` has exactly one
   line `s VERIFIED UNSAT`. **Fresh cake_lpr** (unit `esr-agv-vb-cake-v11rows`, heap 400 MB) on each
   `cuts-v601w1u/<i>/system.cnf` with S1's kept `pm1115/s1/lrat-v601w1u/<i>.system.lrat.zst` streamed through a FIFO:
   exactly one line `s VERIFIED UNSAT` in 8 of 8, and each decompressed stream is byte-identical (SHA-256) to
   `cuts-v601w1u/<i>/system.lrat` (2,066,306-2,320,642 bytes). (VB did not review the `cut34_v4` row encoding; the rows
   are TEST rows.)
3. **Slice c601s1** (on v601): open_at_start 7,036, selected 6,967, skipped 69 (= 75 − the 6 closed); extra list 68
   contexts, without 96 (recorded at 300,001), so 96 is open but in neither list; lists disjoint. Frontier: closed 1095
   (78,565 nodes), 1099-1103, 0 too-big events, no event on a recorded context; extra worker: `context_too_big` 100 at
   300,001, recorded as `100 300001 c601s1.x`. The receipt has no stop reason (ended by SIGTERM, as the claim says).
4. **Unit test** (`bb-v11test2`, input v610): u610a (cap 20,000) recorded 24, 28, 30, 31 (events at 20,001-20,003 nodes;
   records tagged u610a: exactly these four); u610b skipped 32 = 28 + 4 and its `--ctx` list starts at 32; u610c
   (`--too-big-only`, cap 40,000) selected exactly {24, 28, 30, 31, 32, 33}; u610d (`--too-big-only`, cap 10,000)
   selected nothing, `--ctx=-1`, exit 5 after 1.0 s.
5. **Test timings**: c600s1's first contexts closed at 4.1, 6.7 and 7.7 min (1069, 1074, 1075), so the first
   never-attempted context started after 7.7 min; c601s1 closed 1095 at 2.0 min. Close rates 25 / 47.28 min = 31.7 per
   hour and 6 / 11.92 min = 30.2 per hour, as claimed (HEURISTIC comparison with live rounds not re-derived).

## Files (V as above)

| file | SHA-256 |
|---|---|
| `V/vb_v11.py` | `190409dde4496bbe582c6991336f9beca4db6aec1e9befa46f08c3703239a0a3` |
| `V/vb_v11.out` | `cd3fede96ded03c9f718099e9244eafe1fc8829aa974412ae3fe70896786c55e` |
| `V/jobs.txt` (8 re-runs) / `V/cake/rerun.jsonl` | `2485681664aabbae532fa495c102fc540c48aacf03df2cae84aa9e524cc69fab` / `9a3c7b689dcd5a41354991f97ec9444768af6f0113e61f9a645ac9e76f556bc7` |

Nothing in `/home/jay/research/data/es308-20261114/` was written or changed by VB; the live (20,15) loop was not touched.
