# V3D D17: shard 17 of 24 (fourth acceptance pass, mirror sub-case (ii))

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F = /opt/work/F.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Inputs at commit a71d30d; verify/v3 at commit bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (match); all 22682 work-list (case, lits) occur in it. Passed.
- Run: `v3_check.py --shard 17 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:52 to about 17:25 UTC.

## Results (out.jsonl)

| verdict | count |
|---|---|
| VERIFIED (cake_lpr `s VERIFIED UNSAT`) | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

The shard has 945 leaves and all 945 are checked, so none are left unchecked. No rechecks were needed.

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 17084.0 | 10.20 | 291.06 |
| check | 3985.1 | 3.09 | 23.57 |

No SAT, REJECTED or TIMEOUT leaves.
