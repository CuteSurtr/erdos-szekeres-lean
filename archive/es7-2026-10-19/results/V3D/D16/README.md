# V3D D16 (shard 16 of 24)

- Tools: CaDiCaL 3.0.1 commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F = /opt/work/F.cnf regenerated with gen_etv.py + mirgen.py, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d58c21f637bcd4666f17b0bf7b7044a5bb; verify/v3 at commit bdf319c.
- Work list results/V3D/worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (matches); every work-list (case, lits) occurs in it (0 missing). See inputs.txt.

Run: `v3_check.py --shard 16 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:53 to 17:18 UTC, ran to completion.

Results (out.jsonl, 945 records, one per leaf of this shard):
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0; unchecked 0.
- Every record has cake_lpr = `s VERIFIED UNSAT`; no rechecks needed (no REJECTED with empty cake_lpr).
- solve time: sum 16108.3 s, median 10.7 s, max 266.22 s.
- check time: sum 4048.1 s, median 3.31 s, max 22.51 s.
