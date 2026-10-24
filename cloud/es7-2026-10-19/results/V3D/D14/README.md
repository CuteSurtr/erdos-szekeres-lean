# V3D D14: shard 14 of 24

Fourth acceptance pass of mirror sub-case (ii), following `results/V3D/TASK.md` (commit a71d30d) with V = D14, i = 14, N = 24, H = 2.5.

## Setup
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with `make cake_lpr`. The bundled example prints `s VERIFIED UNSAT`.
- F regenerated (gen_etv.py + mirgen.py): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d. verify/v3 taken from commit bdf319c.
- Work list `results/V3D/worklist.jsonl`: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check against the manifest rebuilt at 3e4dbaae3: Mzd.jsonl sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8, 70215 lines (matches). All 22682 work-list (case, lits) pairs occur in it.
- Machine: 4 cores, 15 GB RAM. Ran with `--jobs 4 --cap 1800 --skip-covers`.

## Result
- Shard 14 has 945 leaves. All 945 were checked; none are left unchecked.
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0.
- No REJECTED leaves had an empty cake_lpr field, so step 4 (rechecks) had nothing to do.
- Solve time: 18851.2 s in total, median 10.86 s, max 342.96 s.
- Check time (cake_lpr): 4190.6 s in total, median 3.18 s, max 23.83 s.
- Run time: 15:53 to about 17:25 UTC on 2026-10-20.

Per-leaf records are in `out.jsonl`.
