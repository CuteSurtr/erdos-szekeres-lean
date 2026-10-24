# V3D D19: shard 19 of 24 (fourth acceptance pass, mirror sub-case (ii))

Run 2026-10-20, 16:18 to 17:39 UTC, on 4 cores with 15 GB RAM (env.txt).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`). Its bundled example prints `s VERIFIED UNSAT`.
- F was regenerated with gen_etv.py and mirgen.py. sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z: a71d30d58c21f637bcd4666f17b0bf7b7044a5bb. verify/v3 was used as of commit bdf319c.
- Work list results/V3D/worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check against 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (matches). All 22682 work-list records' (case, lits) occur in it. **PASS** (details in inputs.txt).

## Results (out.jsonl, sha256 75b1dfcaa220683c4edd0f8aca5564c49a185c3c08ba5fe1b3cdd2f69ba76859)
Command: `v3_check.py --shard 19 --nshards 24 --skip-covers --jobs 4 --cap 1800`

| verdict | leaves |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

- All 945 leaves of this shard are VERIFIED, and each has cake_lpr output `s VERIFIED UNSAT`. No leaf was trivially closed by its case cube.
- Solve time (CaDiCaL): sum 15325 s (4.26 h), median 9.85 s, max 282.86 s.
- Check time (cake_lpr): sum 3805 s (1.06 h), median 3.03 s, max 25.07 s.
- No SAT, REJECTED or TIMEOUT leaves, so step 4 (rechecks) had nothing to do.
