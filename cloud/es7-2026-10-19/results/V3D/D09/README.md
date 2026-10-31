# V3D D09: shard 9 of 24

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F = m33k7int.sub.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d; verify/v3 at bdf319c.
- Work list sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: manifest sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines, 0 problems (matches); all 22682 work-list (case, lits) occur in it.

## Results (out.jsonl)

| verdict | count |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

All 945 leaves of the shard checked; 0 unchecked. No rechecks needed (no REJECTED with empty cake_lpr).

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 21220.37 | 12.68 | 296.86 |
| check | 4242.62 | 3.13 | 24.01 |

Run wall time about 1 h 47 min (15:24 to 17:11 UTC, 2026-10-20), 4 jobs, cap 1800 s.
