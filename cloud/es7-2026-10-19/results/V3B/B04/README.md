# V3B B04: second acceptance pass of mirror sub-case (ii), shard 4 of 16

Run 2026-10-20, 11:25Z to 13:58Z, on a 4-core VM with 15 GB RAM (`env.txt`). Followed `results/V3B/TASK.md` at 066eaa9 with V=B04, i=4, N=16, H=3, Z=066eaa9.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, at /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`), at /opt/bin/cake_lpr. Its bundled example prints `s VERIFIED UNSAT`.
- F.cnf regenerated with gen_etv.py and mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- Input commit 066eaa9 (worktree /opt/in). verify/v3 at bdf319c (worktree /opt/v3src).
- jtree1/2/3 came from WAVE1/2/3 (all three exist at 066eaa9). WAVE1 gave 119 dirs and 30151 leaf lines (71 records skipped), WAVE2 gave 86 dirs and 5156 lines, WAVE3 gave 5 dirs and 232 lines.
- v3_manifest.py: leaves 35153, cases with leaves 253, problems 0.
  - M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
  - C.jsonl sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe
- Step 3 read 21 JSONL files (V3T/** and V3A/*/out.jsonl; no V3B out.jsonl existed at Z) and found 10121 VERIFIED leaf keys. That leaves n = 25032 records in Mt.jsonl.
  - Mt.jsonl sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7
  - The script is `mkMt.py`. Full details are in `inputs.txt`.

## Run
`v3_check.py --root /opt/in/cloud/es7-2026-10-19 --base /opt/work/F.cnf --manifest /opt/work/Mt.jsonl --shard 4 --nshards 16 --skip-covers --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800`. OUT was kept outside the checkout and copied to `out.jsonl` at each commit.

## Results (shard 4: 1565 leaves, idx ≡ 4 mod 16, across 100 cases)
| verdict | count |
|---|---|
| VERIFIED | 1565 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

- Every record has rc 20 and `cake_lpr` = `s VERIFIED UNSAT`. Every record's (case, lits) matches the record with the same idx in Mt.jsonl, and every idx of the shard has a record.
- No REJECTED leaf had an empty `cake_lpr` field, so step 5 needed no rechecks.
- Solve time: sum 29488.6 s, median 10.76 s, max 313.61 s.
- Check time: sum 6612.0 s, median 3.13 s, max 22.36 s.
- The largest LRAT proof was 241 MB.
- No SAT, REJECTED or TIMEOUT leaves.
- Covers were not checked here (`--skip-covers`, as the task says).
