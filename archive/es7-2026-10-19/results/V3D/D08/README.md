# V3D D08: shard 8 of 24

Fourth acceptance pass of mirror sub-case (ii), following `results/V3D/TASK.md` (commit a71d30d).

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See `tools.txt`.
- F = m33k7int.sub.cnf regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (match).
- Input commit Z = a71d30d; verify/v3 at bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match).
- Cross-check at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (match); all 22682 work-list (case, lits) occur in it. See `inputs.txt`.

Run: `v3_check.py --shard 8 --nshards 24 --skip-covers --jobs 4 --cap 1800`, 15:27 to 17:25 UTC 2026-10-20. Output `out.jsonl`.

## Results

- Leaves in shard: 945 (6 cases). All checked; 0 unchecked.
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0.
- No REJECTED leaf with an empty cake_lpr field, so no step-4 rechecks were needed.
- Solve time: sum 22458.6 s, median 13.7 s, max 366.37 s.
- Check time (cake_lpr): sum 4352.0 s, median 3.15 s, max 26.92 s.
