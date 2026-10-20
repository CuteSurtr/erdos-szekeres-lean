# V3D D02: shard 2 of 24

Fourth acceptance pass of mirror sub-case (ii), leaves of `results/V3D/worklist.jsonl`.

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F = `/opt/work/F.cnf`, regenerated with gen_etv.py + mirgen.py, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = a71d30d; verify/v3 at bdf319c.
- worklist.jsonl sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: v3_manifest gives Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines, problems 0 (matches); all 22682 work-list (case, lits) occur in it. Details in inputs.txt.
- Run: `v3_check.py --shard 2 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:24 to about 16:57 UTC on 2026-10-20.

## Result

Shard leaves: 945. Checked: 945 (6 cases). Unchecked: 0.

| verdict | count |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

No REJECTED leaf had an empty `cake_lpr` field, so step 4 had no rechecks.

Times (seconds): solve sum 18092.61, median 11.27, max 402.14; check sum 3838.77, median 2.89, max 29.21.

No SAT, REJECTED or TIMEOUT leaves.
