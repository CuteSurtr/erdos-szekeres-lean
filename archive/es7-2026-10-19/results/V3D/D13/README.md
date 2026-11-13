# V3D D13 (shard 13 of 24)

Task: `results/V3D/TASK.md` as committed at a71d30d (V = D13, i = 13, N = 24, H = 2.5, Z = a71d30d).

- Tools: CaDiCaL 3.0.1 commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F = /opt/work/F.cnf, regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = a71d30d; verify/v3 at bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (match); all 22682 work-list (case, lits) occur in it. See inputs.txt.

Run: `v3_check.py --shard 13 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:53 to 17:11 UTC, finished.

Results (out.jsonl, 945 leaf records, 945 distinct keys):
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0. Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`.
- Unchecked leaves of this shard: 0 of 945.
- No REJECTED leaf with an empty cake_lpr field, so no step-4 rechecks.
- solve_s: sum 14000.4 s, median 9.20 s, max 273.89 s.
- check_s: sum 3457.0 s, median 2.80 s, max 24.91 s.
