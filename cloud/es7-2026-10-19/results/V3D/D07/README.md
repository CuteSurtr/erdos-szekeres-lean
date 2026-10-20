# V3D D07: shard 7 of 24

Machine D07, 4 cores, 15 GB RAM (see env.txt). Started 15:22 UTC, run finished by 16:47 UTC on 2026-10-20 (budget 2.5 h).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source as /opt/bin/cadical.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`, as /opt/bin/cake_lpr. The bundled example prints `s VERIFIED UNSAT`.
- verify/v3 at commit bdf319c (bdf319cfb8b20bfacc951a0d6032ceeda85b8bf5).
- F regenerated with gen_etv.py and mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit Z = a71d30d (a71d30d58c21f637bcd4666f17b0bf7b7044a5bb).
- Work list results/V3D/worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches).
- Cross-check at 3e4dbaae3: the rebuilt manifest Mzd.jsonl has sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 and 70215 lines (matches, 0 problems). All 22682 work-list (case, lits) pairs occur in it. PASS. Details in inputs.txt.

## Run
`v3_check.py --shard 7 --nshards 24 --skip-covers --jobs 4 --cap 1800`, OUT in /opt/work/out (outside the checkout), copied to out.jsonl here.

## Results
- Shard leaves: 945. Records: 945, all distinct.
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0.
- No REJECTED leaves with an empty cake_lpr field, so step 4 had no rechecks.
- Solve time: sum 14588.9 s, median 9.73 s, max 234.94 s.
- Check time (cake_lpr): sum 3637.2 s, median 2.88 s, max 21.81 s.
- No SAT, REJECTED or TIMEOUT leaves to report.
