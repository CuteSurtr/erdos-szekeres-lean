# V3D D15 (shard 15 of 24)

- Tools: CaDiCaL 3.0.1 commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`).
- F = /opt/work/F.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d58c21f637bcd4666f17b0bf7b7044a5bb; verify/v3 at commit bdf319c.
- Work list `results/V3D/worklist.jsonl` sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (match); all 22682 work-list (case, lits) pairs occur in it. PASS. Details in inputs.txt.

## Result

Shard 15 of 24 has 945 leaves. All 945 were checked (out.jsonl keys = shard indices exactly), run finished on its own (17:2x UTC).

| verdict | count |
|---|---|
| VERIFIED | 945 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

Times (seconds): solve sum 16407.2, median 9.85, max 241.77; check sum 3822.2, median 2.95, max 24.15.

No SAT, REJECTED or TIMEOUT leaves, so no re-checks (step 4) were needed.
