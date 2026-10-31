# V3D D21: shard 21 of 24, fourth acceptance pass of mirror sub-case (ii)

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d; verify/v3 at bdf319c.
- Work list results/V3D/worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (match).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (match); all 22682 work-list (case, lits) occur in it. PASS. See inputs.txt.

## Result
Command: `v3_check.py --root $ROOT --base /opt/work/F.cnf --manifest $ROOT/results/V3D/worklist.jsonl --shard 21 --nshards 24 --skip-covers --jobs 4 --cap 1800`.

- Leaves in shard: 945. Records in out.jsonl: 945 (945 distinct idx).
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- Every record has cake_lpr `s VERIFIED UNSAT`. No re-checks were needed (step 4).
- Solve time: sum 17545.6 s, median 12.04 s, max 358.29 s.
- Check time (cake_lpr): sum 4396.6 s, median 3.49 s, max 26.54 s.
- Run time: 16:18 to about 17:50 UTC on 2026-10-20 (4 cores, 15 GB).
